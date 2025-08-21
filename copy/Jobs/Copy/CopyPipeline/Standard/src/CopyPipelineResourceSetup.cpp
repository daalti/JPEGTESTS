////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyPipelineResourceSetup.cpp
 * @brief  CopyPipelineResourceSetup for Copy jobs
 * @author Shubham Khandelwal
 * @date   2023-04-15
 *
 * (C) Copyright 2023 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "CopyPipelineResourceSetup.h"

#include "common_debug.h"

#include "CopyPipelineResourceSetup_TraceAutogen.h"

#include "IImageRetrieverIntent.h"
#include "IIntentsManager.h"
#include "IPipelineBuilder.h"
#include "IScannerMedia.h"
#include "MediaHelper.h"
#include "ResourceInstanceProxy.h"
#include "SelectionHelper.h"
#include "IJobQueue.h"
#include "IJob.h"
#include "IPrint.h"
#include "ICapabilitiesFactory.h"
#include "Capabilities.h"
#include <arpa/inet.h>
#include "ILocaleProvider.h"
#include "ILocale.h"
#include <time.h>

using namespace std;
using dune::job::IPipelineBuilder;
using dune::job::IResourceInstanceProxy;
using dune::job::IResourceService;
using dune::job::ResourceInstanceProxy;
using dune::job::ResourceInstanceProxyAgent;
using dune::imaging::types::Resolution;
using dune::imaging::types::BookletFormat;
using OriginalMediaType = dune::scan::types::OriginalMediaType;
using PlexSide = dune::imaging::types::PlexSide;
using IScanPipeline = dune::scan::Jobs::Scan::IScanPipeline;
using IIntentsManager = dune::job::IIntentsManager;
using SelectionHelper = dune::print::mediaHandlingAssets::types::SelectionHelper;
using IDateTime = dune::framework::core::time::IDateTime;
using StampType = dune::imaging::types::StampType;


#define NO_SCALE_PERCENT 100
#define INCLUDE_MARGIN_PERCENT 97
#define RES_CONVERT(len, from, to) (((int )(len) * (int )(to)) / (int )(from)) 

const uint32_t DEFAULT_STRIP_HEIGHT = 32;
const uint32_t DISK_BUFFERING_STRIP_HEIGHT = 64; // 64 height each strip from retriever
const uint32_t ENTERPRISE_DEFAULT_STRIP_HEIGHT = 128;
const uint32_t ENTERPRISE_BORDER_MARGIN = 128;
const uint32_t LFP_DEFAULT_STRIP_HEIGHT = 256;
namespace dune { namespace copy { namespace Jobs { namespace Copy {

CopyPipelineResourceSetup::CopyPipelineResourceSetup(
        std::shared_ptr<ICopyJobTicket> ticket,
        const ServicesPackage& services, bool hasSharedPaperPath,
        IScanPipeline* scanPipeline, Product prePrintConfiguration,
        bool copyBasicPipeline, const MaxLengthConfig& maxLengthConfig, IDateTime* dateTime)
    : scanPipeline_{scanPipeline},
      services_{services},
      maxLengthConfig_{maxLengthConfig},
      copyIntent_{ticket->getIntent()},
      ticket_{ticket},
      hasSharedPaperPath_{hasSharedPaperPath},
      copyBasicPipeline_{copyBasicPipeline},
      prePrintConfiguration_{prePrintConfiguration},
      dateTime_{dateTime}
{
    CHECKPOINTA("CopyPipelineResourceSetup::CopyPipelineResourceSetup constructor");

    CHECKPOINTA("CopyPipelineResourceSetup: copyBasicPipeline= %d", (int) copyBasicPipeline_);

    #if defined(JPEG_HARDWARE_AVAILABLE)
        CHECKPOINTA("CopyPipelineResourceSetup: non-simulator job");
        simJob_ = false;
    #endif
    if (prePrintConfiguration_ == Product::ENTERPRISE)
    {
        copyEnterprisePipeline_ = true;
        #if defined(EFIVAR_EXIST)
        CHECKPOINTA("CopyPipelineResourceSetup: non-simulator job - ENTERPRISE");
        simJob_ = false;
        #endif
    }
    currentStage_ = Stage::Setup;
    scanPipelineConfig_ = scanPipeline_->getScanPipelineConfiguration();
}

void CopyPipelineResourceSetup::setupImageProcessorIntent(std::shared_ptr<IImageProcessorIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig)
{
    CHECKPOINTA("CopyPipelineResourceSetup: setupImageProcessorIntent - entry");

    // Adding White Borders on the scanned image is not required for ADF and Flatbed
    if (copyIntent_->getScanSource() == dune::scan::types::ScanSource::MDF)
    {
        intent->setAddBorderRequired(true);

        // HomePro doesn't use the output canvas
        intent->setOutputCanvasTable(copyIntent_->getOutputCanvas());
    }
    else if (copyBasicPipeline_ &&
             (copyIntent_->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp) &&
             (copyIntent_->getScanSource() != dune::scan::types::ScanSource::GLASS))
    {
        dune::imaging::Resources::SpecificRotation specificRotation;
        specificRotation.overrideRotation = true;
        specificRotation.rotation = 90;
        intent->setSpecificRotation(specificRotation);
        intent->setAddBorderRequired(false);
        CHECKPOINTA("CopyPipelineResourceSetup: setupImageProcessorTicket - Specific Rotation will be performed.");
    }
    else
    {
        intent->setAddBorderRequired(false);
    }

    if ((collateMode_ == CollateMode::COMPRESSED || copyBasicPipeline_) 
            && segmentType_ == SegmentType::FinalSegment 
            && (copyIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::OneUp))
    {
        intent->setIgnoreWhitespaceAdd(true);
    }

    intent->setFlowType(dune::imaging::Resources::FlowType::COPY);
    intent->setUseEdgeRemoval ( scanPipelineConfig_->edgeRemoval  );
    if (!isAutoDeskewSupportedOnScanDevice())
    {
        // configure AutoDeskew if ImageProcessor is being used to do the
        // operation (instead of using ScanDevice)
        intent->setUseAutoDeskew( copyIntent_->getAutoDeskew() );
    }
    intent->setUseImageQuality( scanPipelineConfig_->imageQuality );

    if ((copyIntent_->getColorMode() == ColorMode::BLACKANDWHITE) &&
        ((prePrintConfiguration_ == Product::HOME_PRO) &&
         (copyIntent_->getScanSource() == dune::scan::types::ScanSource::MDF)))
    {
        // [Beam] Scan device does not natively support black and white. Instead
        // it provides an 8-bit grayscale image that will be simple thresholded
        // with the Image Processor.
        intent->setSimpleThresholdingNeeded(true, thresholdOverride_);
    }
    else
    {
        intent->setSimpleThresholdingNeeded(false);
    }

    // setup Output Scale for Imaging
    if(!isScaleSupportedOnScanDevice())
    {
        CHECKPOINTA("CopyPipelineResourceSetup: setupImageProcessorIntent - setScale Parameters in ImageProcessoor");
        dune::imaging::types::PrintScaleT printScaleTable = dune::imaging::types::PrintScaleT();
        printScaleTable.xScalePercent = copyIntent_->getXScalePercent();
        printScaleTable.yScalePercent = copyIntent_->getYScalePercent();
        if (copyIntent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD)
        {
            printScaleTable.scaleSelection = scanPipeline_->parseScanScaleSelectionTypeToImagingScaleSelectionType(
                dune::scan::types::ScanScaleSelectionEnum::NONE);
        }
        else
        {
            printScaleTable.scaleSelection =
                scanPipeline_->parseScanScaleSelectionTypeToImagingScaleSelectionType(copyIntent_->getScaleSelection());
        }
        printScaleTable.scaleToOutput = copyIntent_->getScaleToOutput();
        printScaleTable.scaleToSize = copyIntent_->getScaleToSize();
        printScaleTable.upScaleStrategy = resourceConfig->upScaleStrategy;
        printScaleTable.downScaleStrategy = resourceConfig->downScaleStrategy;
        // For future, when aspect ratio edition can be added as true / false.  For the moment, the option is maintain always true.
        // Also add a way to select how we are determinig the scale to be used. For the moment, IGNORE_IDENTITY_THEN_MIN.
        // printScaleTable.maintainAspectRatio = intent->getMaintainAspectRatio();
        // printScaleTable.maintainRatioStrategy = dune::imaging::types::MaintainStrategy::IGNORE_IDENTITY_THEN_MIN
        CHECKPOINTA("CopyPipelineResourceSetup: setupImageProcessorIntent - setScale Parameters in ImageProcessoor xScalePercent %d", (uint32_t)printScaleTable.xScalePercent);
        CHECKPOINTA("CopyPipelineResourceSetup: setupImageProcessorIntent - setScale Parameters in ImageProcessoor yScalePercent %d", (uint32_t)printScaleTable.yScalePercent);
        CHECKPOINTA("CopyPipelineResourceSetup: setupImageProcessorIntent - setScale Parameters in ImageProcessoor scaleSelection %d", (uint32_t)printScaleTable.scaleSelection);
        CHECKPOINTA("CopyPipelineResourceSetup: setupImageProcessorIntent - setScale Parameters in ImageProcessoor scaleToOutput %d", (uint32_t)printScaleTable.scaleToOutput);
        CHECKPOINTA("CopyPipelineResourceSetup: setupImageProcessorIntent - setScale Parameters in ImageProcessoor scaleToSize %d", (uint32_t)printScaleTable.scaleToSize);
        intent->setPrintScale(printScaleTable);

    }

    // Setup detect original scan size based on resource configuration
    intent->setDetectOriginalScanSize(resourceConfig->detectOriginalScanSize);

    // Set CheckImageRotation
    if (copyEnterprisePipeline_)
    {
        intent->setCheckImageRotation(false);
    }
    else
    {
        // Review if config setup image rotation
        intent->setCheckImageRotation(resourceConfig->performRotation);
    }

    // Set ImageQualityValues
    if( scanPipelineConfig_->imageQuality )
    {
        std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> iqTable =
         std::make_shared<dune::imaging::types::ImageQualityProcessingTableT>();

        iqTable->originalContentType = copyIntent_->getOriginalContentType();
        iqTable->mediaIdType         = scanPipeline_->parseScanMediaTypeToImagingMediaType( copyIntent_->getOriginalMediaType() );
        iqTable->blackEnhancements = copyIntent_->getBlackEnhancementLevel();

        // Background Removal Setup
        if(!isBackgroundColorRemovalSupportedOnScanDevice() && copyIntent_->getBackgroundColorRemoval())
        {
            if(copyIntent_->getOriginalMediaType() == OriginalMediaType::DARK_BLUEPRINTS && 
                copyIntent_->getColorMode() == dune::imaging::types::ColorMode::GRAYSCALE)
            {
                // Setup background removal as HP
                iqTable->backgroundRemovalType = dune::imaging::types::BackgroundRemovalType::BGREM_AUTOHP;
            }
            else
            {
                // Setup background color removal as contex removal for the moment
                iqTable->backgroundRemovalType = dune::imaging::types::BackgroundRemovalType::BGREM_AUTOCTX;
            }

            iqTable->backgroundDensity = copyIntent_->getBackgroundColorRemovalLevel();
        }
        else
        {
            // Use "none" when no background removal is selected, and not allow select a level, always will be 0
            iqTable->backgroundRemovalType = dune::imaging::types::BackgroundRemovalType::BGREM_NONE;
        }

        iqTable->backgroundDensity = copyIntent_->getBackgroundColorRemovalLevel();  

        // Update iqTable invert colors if ImagingOperation::InvertColors is not supported by the scan device.
        if(!isInvertColorsSupportedOnScanDevice())
        {
            CHECKPOINTA("CopyPipelineResourceSetup: setupImageProcessorIntent - Invert colors updated");
            iqTable->negative = copyIntent_->getInvertColors();
        }

        intent->setImageQualityValues( iqTable );
    }

    CHECKPOINTA("CopyPipelineResourceSetup: setupImageProcessorIntent - exit");
}

void CopyPipelineResourceSetup::setupImageProcessorPreviewIntent(std::shared_ptr<IImageProcessorIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig)
{
    CHECKPOINTA("CopyPipelineResourceSetup: setupImageProcessorPreviewIntent - entry");

    intent->setFlowType(dune::imaging::Resources::FlowType::PREVIEW);
    intent->setUseEdgeRemoval(scanPipelineConfig_->edgeRemoval);
    intent->setUseImageQuality(scanPipelineConfig_->imageQuality);
    intent->setComputeScale(dune::imaging::Resources::ComputeScale::RESOLUTION);
    intent->setThumbnailResolution(scanPipelineConfig_->thumbnailResolution);
    intent->setPreviewIsNeeded(true);

    //If AutoDeskew is supported in the scan device, it will not use AutoDeskew in ImageProcessor
    if (!isAutoDeskewSupportedOnScanDevice()){
        intent->setUseAutoDeskew( copyIntent_->getAutoDeskew() );
    }

    // Set ImageQualityValues
    if( scanPipelineConfig_->imageQuality )
    {
        std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> iqTable =
         std::make_shared<dune::imaging::types::ImageQualityProcessingTableT>();

        iqTable->originalContentType = copyIntent_->getOriginalContentType();
        iqTable->mediaIdType         = scanPipeline_->parseScanMediaTypeToImagingMediaType( copyIntent_->getOriginalMediaType() );
        iqTable->blackEnhancements = copyIntent_->getBlackEnhancementLevel();

        // Background Removal Setup
        if(!isBackgroundColorRemovalSupportedOnScanDevice() && copyIntent_->getBackgroundColorRemoval())
        {
            if(copyIntent_->getOriginalMediaType() == OriginalMediaType::DARK_BLUEPRINTS)
            {
                // Setup background removal as HP
                iqTable->backgroundRemovalType = dune::imaging::types::BackgroundRemovalType::BGREM_AUTOHP;
            }
            else
            {
                // Setup background color removal as contex removal for the moment
                iqTable->backgroundRemovalType = dune::imaging::types::BackgroundRemovalType::BGREM_AUTOCTX;
            }

            iqTable->backgroundDensity = copyIntent_->getBackgroundColorRemovalLevel();
        }
        else
        {
            // Use "none" when no background removal is selected, and not allow select a level, always will be 0
            iqTable->backgroundRemovalType = dune::imaging::types::BackgroundRemovalType::BGREM_NONE;
        }
        
        iqTable->backgroundDensity = copyIntent_->getBackgroundColorRemovalLevel();  

        // Update iqTable invert colors if ImagingOperation::InvertColors is not supported by the scan device.
        if(!isInvertColorsSupportedOnScanDevice())
        {
            CHECKPOINTA("CopyPipelineResourceSetup: setupImageProcessorPreviewIntent - Invert colors updated");
            iqTable->negative = copyIntent_->getInvertColors();
        }

        intent->setImageQualityValues( iqTable );
    }

    // Setup detect original scan size based on resource configuration
    intent->setDetectOriginalScanSize(resourceConfig->detectOriginalScanSize);

    CHECKPOINTA("CopyPipelineResourceSetup: setupImageProcessorPreviewIntent - exit");
}

void CopyPipelineResourceSetup::setupScanDeviceIntent(std::shared_ptr<IScanDeviceIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig)
{
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent - entry");
    DUNE_UNUSED(resourceConfig);
    bool autoCropSupported = isAutoCropSupportedOnScanDevice();
    auto jobTicketHandler = ticket_->getHandler();
    intent->setScanImagingProfile(dune::scan::types::ScanImagingProfileType::COPY);
    intent->setScanSource(ConvertToScanTypeHelper::resolveScanSource(copyIntent_->getInputPlexMode(), copyIntent_->getScanSource()));
    intent->setColorMode(copyIntent_->getColorMode());
    intent->setOriginalContentOrientation(copyIntent_->getContentOrientation());
    intent->setOriginalContentType(copyIntent_->getOriginalContentType());
    intent->setOriginalMediaType(copyIntent_->getOriginalMediaType());
    intent->setScanOutputInterleaved(false);
    intent->setScanFeedOrientation(copyIntent_->getScanFeedOrientation());
    intent->setInterleavedObjectMap(true);
    intent->setMultipleNumberOfLinesRequired(256);
    intent->setRequiredWidthAlignment(32);
    intent->setBrightness(copyIntent_->getBrightness());
    intent->setAutoRelease(copyIntent_->getAutoRelease());
    intent->setScanAcquisitionsSpeed(copyIntent_->getScanAcquisitionsSpeed());
    intent->setIsPreviewScan(false);
    intent->setAutoTone(copyIntent_->getAutoTone());
    intent->setAutoToneLevel(copyIntent_->getAutoToneLevel());
    intent->setAutoPaperColorRemoval(copyIntent_->getAutoPaperColorRemoval());
    intent->setAutoPaperColorRemovalLevel(copyIntent_->getAutoPaperColorRemovalLevel());

    if (prePrintConfiguration_ == Product::ENTERPRISE)
    {
        // To Do : This can be removed once we will call evelve prompt in case of any media size selected 
        DetectMediaFromSensor();
    }

    auto outputMediaSizeId = copyIntent_->getOutputMediaSizeId();
    // Output MediaSize should not be Any
    if (copyIntent_->getOutputMediaSizeId() == MediaSizeId::ANY && prePrintConfiguration_ == Product::ENTERPRISE)
    {
        copyIntent_->setMatchOriginalOutputMediaSizeId(copyIntent_->getInputMediaSizeId());
        outputMediaSizeId = copyIntent_->getInputMediaSizeId();
        CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent - Output Media Size is set to Input Media Size");
    }    

    if(collateMode_ != CollateMode::NONE && maxPagesToCollate_ > 1)
    {
        intent->setAdfMaxPagesToScan(maxPagesToCollate_);
    }
    else
    {
        intent->setAdfMaxPagesToScan(0);
    }

    CHECKPOINTC("CopyPipelineResourceSetup::setupScanDeviceIntent: copyIntent_->getScanCalibrationType() = %d",
        static_cast<int>(copyIntent_->getScanCalibrationType()));

    intent->setScanCalibrationType(copyIntent_->getScanCalibrationType());

    if (autoCropSupported && (copyIntent_->getInputMediaSizeId() == MediaSizeId::ANY)) //prescan is assumed if pipe is a null pointer
    {
        CHECKPOINTA("CopyPipelineResourceSetup: AutoCrop set to true");
        intent->setAutoCrop(true);
    }

    if (copyIntent_->getScanSource() == ScanSource::GLASS && prePrintConfiguration_ == Product::HOME_PRO)
    {
        CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent - set collate to uncollate");
        copyIntent_->setCollate(SheetCollate::Uncollate);
    }
    
    if (copyIntent_->getInputPlexMode() == dune::imaging::types::Plex::DUPLEX)
    {
        intent->setScanPagesFlipUpEnabled(copyIntent_->getScanPagesFlipUpEnabled());
    }
    // if scan source is glass and plex mode is duplex, set the scan duplex side appropriately
    if (copyIntent_->getScanSource() == ScanSource::GLASS && copyIntent_->getInputPlexMode() == dune::imaging::types::Plex::DUPLEX)
    {
        if(getFlatbedDuplexScanBackSide())
        {
            CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent - Flatbed Duplex - set duplex side to BACK");
            intent->setScanDuplexSide(dune::scan::types::DuplexSideEnum::BackSide);
        }
        else
        {
            CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent - Flatbed Duplex - set duplex side to FRONT");
            intent->setScanDuplexSide(dune::scan::types::DuplexSideEnum::FrontSide);
        }
    }
    if (copyIntent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD)
    {
        CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent - ID Card - Change orientation LONGEDGE to SHORTEDGE");
        intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::SHORTEDGE);
    }
    else if (ticket_->getIntent()->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::BOOKMODE)
    {
        intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::LONGEDGE);
    }
    else
    {
        intent->setScanFeedOrientation(copyIntent_->getScanFeedOrientation());  // short/long edge feeding
    }
    //set X and Y resolution to 300 when it is set to 150
    if ((copyIntent_->getOutputXResolution()== dune::imaging::types::Resolution::E150DPI)&&
        (copyIntent_->getOutputYResolution()== dune::imaging::types::Resolution::E150DPI)&&
        (prePrintConfiguration_ == Product::HOME_PRO)&&
        (copyIntent_->getScanSource() == dune::scan::types::ScanSource::MDF))
    {
        copyIntent_->setOutputXResolution(dune::imaging::types::Resolution::E300DPI);
        copyIntent_->setOutputYResolution(dune::imaging::types::Resolution::E300DPI);
    }

    MarginsParameters marginParams;
    marginParams.setMediaSource(copyIntent_->getOutputMediaSource());
    Margins mediaMargins = std::get<1>(services_.mediaInterface->getMargins(marginParams));

    auto orientation = dune::imaging::types::MediaOrientation::PORTRAIT;
    if (copyIntent_->getScanFeedOrientation() == dune::scan::types::ScanFeedOrientation::LONGEDGE)
    {
        orientation = dune::imaging::types::MediaOrientation::LANDSCAPE;
    }

    //SCALING CASES - Fit To Page
    //If the input and output media sizes are different, and the output media size is not ANY, then we need to scale the input to fit the output
    //Output media size Any means that the output media size is the same as the input media size
    if (copyIntent_->getInputMediaSizeId() != outputMediaSizeId && (outputMediaSizeId != MediaSizeId::ANY))
    {
        CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: scaleToFit: inputMediaSizeId = %d, outputMediaSizeId = %d", copyIntent_->getInputMediaSizeId(), copyIntent_->getOutputMediaSizeId());
        if (copyIntent_->getScaleToFitEnabled())
        {
            int dpi = 0;
            if (prePrintConfiguration_ == Product::HOME_PRO)
            {
                dpi = ConvertToScanTypeHelper::getResolutionIntFromEnum(Resolution::E300DPI);
            }
            else
            {
                dpi = ConvertToScanTypeHelper::getResolutionIntFromEnum(copyIntent_->getOutputXResolution());
            }
            //setup prescan if input media size is automatic
            if (copyIntent_->getInputMediaSizeId() == MediaSizeId::ANY && intent->getScanSource() == dune::scan::types::ScanSource::GLASS)
            {
                intent->setAutoCrop(true);
            }
            //Give the output region to the scan device ticket for scaleToFit calculations
            topMargin_ = mediaMargins.getTop().get(dpi);
            bottomMargin_ = mediaMargins.getBottom().get(dpi);
            leftMargin_ = mediaMargins.getLeft().get(dpi);
            rightMargin_ = mediaMargins.getRight().get(dpi);

            auto outWidthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(outputMediaSizeId, orientation);
            intent->setOutXExtent(outWidthAndHeight.width.get(dpi) - (leftMargin_ + rightMargin_));
            intent->setOutYExtent(outWidthAndHeight.height.get(dpi) - (topMargin_ + bottomMargin_));
            
            if (prePrintConfiguration_ == Product::ENTERPRISE){
                auto inWidthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(copyIntent_->getInputMediaSizeId(), orientation);
                uint32_t fitToPagePercent = ConvertToScanTypeHelper::getScalingForScaleToFit(inWidthAndHeight.width.get(dpi), inWidthAndHeight.height.get(dpi), outWidthAndHeight.width.get(dpi), outWidthAndHeight.height.get(dpi));

                fitToPagePercent = fitToPagePercent / 1000;
                

                if(copyIntent_->getFitToPageIncludeMargin()){
                    CHECKPOINTC("CopyPipelineResourceSetup::setupScanDeviceIntent: includeMargin");
                    fitToPagePercent = fitToPagePercent * INCLUDE_MARGIN_PERCENT / NO_SCALE_PERCENT;
                }

                intent->setXScalePercent(fitToPagePercent);
                intent->setYScalePercent(fitToPagePercent);
                copyIntent_->setXScalePercent(fitToPagePercent);
                copyIntent_->setYScalePercent(fitToPagePercent);
                CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: scaleToFit: scaleFactor = %d", fitToPagePercent);
            }
            CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: scaleToFit: dpi = %d, margin = %d, outXExtent = %d, outYExtent = %d", dpi, (leftMargin_ + rightMargin_), intent->getOutXExtent(), intent->getOutYExtent());
        }
    }

    if (prePrintConfiguration_ == Product::HOME_PRO && segmentType_ == SegmentType::PrepareSegment)
    {
        intent->setOutputXResolution(Resolution::E100DPI);
        intent->setOutputYResolution(Resolution::E100DPI);
        intent->setIsPreviewScan(true);
    }
    else
    {
        intent->setOutputXResolution(copyIntent_->getOutputXResolution());
        intent->setOutputYResolution(copyIntent_->getOutputYResolution());
    }

    //Set scan capute mode to scan device intent
    dune::scan::types::ScanCaptureModeType captureMode = copyIntent_->getScanCaptureMode();
    intent->setScanCaptureMode(captureMode);
    intent->setBookMode(copyIntent_->getBookMode());
    CHECKPOINTA("CopyPipelineResourceSetup:: setupScanDeviceIntent - Scan data interleaved = %d", intent->getScanOutputInterleaved());


    // Eventually we'll want to move this piece into a library that can be shared
    // between fax, copy, and send as appropriate.  Right now all three job types
    // are implementing this same setup code which seems unnecessary.
    if(copyIntent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::BOOKMODE)
    {
        scanPipeline_->setupScanDeviceForBookMode(intent, copyIntent_);
    }
    else if( intent->getScanSource() == dune::scan::types::ScanSource::GLASS &&
        copyIntent_->getInputMediaSizeId() == MediaSizeId::LEGAL && !copyBasicPipeline_)
    {
        setupScanRegion(intent, dune::imaging::types::MediaSizeId::LETTER, copyIntent_->getScanFeedOrientation(), intent->getOutputXResolution(), captureMode);
    }
    else
    {
        if (prePrintConfiguration_ == Product::HOME_PRO) 
        { 
            setupScanRegion(intent, copyIntent_->getInputMediaSizeId(), copyIntent_->getScanFeedOrientation(), Resolution::E300DPI, captureMode); 
            setupScanMargins(intent, Resolution::E300DPI, true, true);
        }
        else if (prePrintConfiguration_ == Product::ENTERPRISE)
        {
            if (copyIntent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD)
            {
                setupScanRegion(intent, copyIntent_->getInputMediaSizeId(), dune::scan::types::ScanFeedOrientation::SHORTEDGE, copyIntent_->getOutputXResolution(), captureMode);
                setupScanMargins(intent, Resolution::E600DPI, false, true);
            }
            else
            {
                setupScanRegion(intent, copyIntent_->getInputMediaSizeId(), copyIntent_->getScanFeedOrientation(), copyIntent_->getOutputXResolution(), captureMode);
                setupScanMargins(intent, Resolution::E600DPI, true, true);
            }            
        }
        else { setupScanRegion(intent, copyIntent_->getInputMediaSizeId(), copyIntent_->getScanFeedOrientation(), copyIntent_->getOutputXResolution(), captureMode); }
    }

    if(isScaleSupportedOnScanDevice())
    {
        //considering the scaling cases 2up, Fit to Page and Custom percentage. The selections are mutually exclusive

        int dpi = 0;
        dpi = (prePrintConfiguration_ == Product::HOME_PRO) ? ConvertToScanTypeHelper::getResolutionIntFromEnum(Resolution::E300DPI) : ConvertToScanTypeHelper::getResolutionIntFromEnum(copyIntent_->getOutputXResolution());

        auto outWidthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(outputMediaSizeId, orientation);
        if (copyIntent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD)
        {
            intent->setXScalePercent(NO_SCALE_PERCENT);
            intent->setYScalePercent(NO_SCALE_PERCENT);
        }
        else
        {
            topMargin_ = mediaMargins.getTop().get(dpi);
            bottomMargin_ = mediaMargins.getBottom().get(dpi);
            leftMargin_ = mediaMargins.getLeft().get(dpi);
            rightMargin_ = mediaMargins.getRight().get(dpi);

            intent->setXScalePercent(copyIntent_->getXScalePercent());
            intent->setYScalePercent(copyIntent_->getYScalePercent());
            CHECKPOINTA("CopyPipelineResourceSetup: copyIntent_ scale: %d, %d", copyIntent_->getXScalePercent(), copyIntent_->getYScalePercent());

            // N-up scale
            if (copyIntent_->getPagesPerSheet() == CopyOutputNumberUpCount::TwoUp || copyIntent_->getPagesPerSheet() == CopyOutputNumberUpCount::FourUp)
            {
                // Give the output region to the scan device ticket for scaleToFit calculations
                CHECKPOINTC("CopyPipelineResourceSetup::setupScanDeviceIntent: N-up case");

                // Finding the region we need to scale the scan to. 
                // For that first finding the printable region minus the print margins 
                // The desired width output of the scaled image is equal to the height minus margins and paddings
                // divided by 2 because of the rotation .                
                // The desired height output of the scaled image is equal to the width ,minus margins and padding 
                // Note that the padding is applied per image 

                
                // get specific padding values - convert from mm to 300 dpi resolution 
                uint32_t topPad = RES_CONVERT(topSpecificPadding_*10, 254, 300);
                uint32_t bottomPad = RES_CONVERT(bottomSpecificPadding_*10, 254, 300);
                uint32_t leftPad = RES_CONVERT(leftSpecificPadding_*10, 254, 300);
                uint32_t rightPad = RES_CONVERT(rightSpecificPadding_*10, 254, 300);
                CHECKPOINTA("CopyPipelineResourceSetup:: topPad %d, bottomPad %d, leftPad %d, rightPad %d", topPad, bottomPad, leftPad, rightPad );

                uint32_t printableWidthMinusMargins = outWidthAndHeight.width.get(dpi) - (leftMargin_ + rightMargin_);
                uint32_t printableHeightMinusMargins = outWidthAndHeight.height.get(dpi) - (topMargin_ + bottomMargin_);
                uint32_t printableWidthPerImage = printableWidthMinusMargins - (leftPad + rightPad);
                uint32_t printableHeightPerImage = printableHeightMinusMargins/2 - (topPad + bottomPad);

                uint32_t rotatedX = printableHeightPerImage;
                uint32_t rotatedY = printableWidthPerImage;

                uint64_t scaleFactor = 0;

                if(prePrintConfiguration_ == Product::ENTERPRISE)
                {
                    outWidthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(outputMediaSizeId);

                    uint32_t outlong = 0, outshort = 0;
                    uint32_t inlong = 0, inshort = 0;
                    if(outWidthAndHeight.height.get(dpi) >= outWidthAndHeight.width.get(dpi))
                    {
                        outlong = outWidthAndHeight.height.get(dpi)- (bottomMargin_ + topMargin_ + topPad + bottomPad);
                        outshort = outWidthAndHeight.width.get(dpi)- (leftMargin_ + rightMargin_ + leftPad + rightPad);
                    }
                    else
                    {
                        outlong = outWidthAndHeight.width.get(dpi)- (leftMargin_ + rightMargin_ + leftPad + rightPad);
                        outshort = outWidthAndHeight.height.get(dpi)- (bottomMargin_ + topMargin_ + topPad + bottomPad);
                    }
                    
                    if (copyIntent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::BOOKMODE)
                    {
                        inlong = intent->getXExtent();
                        inshort = intent->getYExtent() / 2;
                    }
                    else if(intent->getXExtent() >= intent->getYExtent())
                    {
                        inlong = intent->getXExtent();
                        inshort = intent->getYExtent();
                    }
                    else
                    {
                        inlong = intent->getYExtent();
                        inshort = intent->getXExtent();
                    }

                    if (copyIntent_->getPagesPerSheet() == CopyOutputNumberUpCount::TwoUp)
                    {
                        scaleFactor = ConvertToScanTypeHelper::getScalingForScaleToFit(
                            inshort, inlong, outlong/2 - ENTERPRISE_BORDER_MARGIN, outshort- ENTERPRISE_BORDER_MARGIN);
                    }
                    else //copyIntent_->getPagesPerSheet() == CopyOutputNumberUpCount::FourUp
                    {
                        scaleFactor = ConvertToScanTypeHelper::getScalingForScaleToFit
                            (inshort, inlong, outshort/2 - ENTERPRISE_BORDER_MARGIN, outlong/2 - ENTERPRISE_BORDER_MARGIN);
                    }

                    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent scaleFactor:%d,  in:(w %d, h %d), out:(w %d, h %d)", scaleFactor, inshort, inlong, outshort, outlong);

                    scaleFactor = scaleFactor / 1000;
                    intent->setXScalePercent(scaleFactor);
                    intent->setYScalePercent(scaleFactor);
                    copyIntent_->setXScalePercent(scaleFactor);
                    copyIntent_->setYScalePercent(scaleFactor);
                }
                else
                {
                    scaleFactor = ConvertToScanTypeHelper::getScalingForScaleToFit(intent->getXExtent(), 
                                                                                        intent->getYExtent(), 
                                                                                        rotatedX, 
                                                                                        rotatedY);
                    
                    scaleFactor = scaleFactor/1000;
                    intent->setXScalePercent(scaleFactor);
                    intent->setYScalePercent(scaleFactor);
                    //recalc the outextents based on the scaleFactor. The scale factor is the min of the x and y scalefactors. 
                    rotatedX = (intent->getXExtent() * scaleFactor)/100;
                    rotatedY = (intent->getYExtent() * scaleFactor)/100;
                    intent->setOutXExtent(rotatedX);
                    intent->setOutYExtent(rotatedY);
                    
                }
                
                CHECKPOINTA("CopyPipelineResourceSetup: InXExtent = %d, InYExtent = %d, OutXExtent = %d, OutYExtent = %d, scale = %d",
                    intent->getXExtent(), intent->getYExtent(), intent->getOutXExtent(), intent->getOutYExtent(), scaleFactor);
                CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent Margins Top - %d , Bottom - %d, Left - %d, Right - %d",
                    topMargin_, bottomMargin_, leftMargin_, rightMargin_);
            }

            // Fit to page
            // This is added to avoid the "Custom Percentage" code below when set to "Fit to page" in the enterprise model.
            else if (copyIntent_->getScaleSelection() == dune::scan::types::ScanScaleSelectionEnum::FITTOPAGE)
            {
                CHECKPOINTA("CopyPipelineResourceSetup: Scale percent already updated, xScalePercent = %d, yScalePercent = %d",
                    intent->getXScalePercent(), intent->getYScalePercent());
            }
            
            // Custom Percentage
            else if (intent->getXScalePercent() != NO_SCALE_PERCENT ||
                      intent->getYScalePercent() != NO_SCALE_PERCENT)
            {
                intent->setOutXExtent(outWidthAndHeight.width.get(dpi) - (leftMargin_ + rightMargin_));
                intent->setOutYExtent(outWidthAndHeight.height.get(dpi) - (topMargin_ + bottomMargin_));
                CHECKPOINTA(
                    "CopyPipelineResourceSetup: BEFORE: InXExtent = %d, InYExtent = %d, OutXExtent = %d, OutYExtent = "
                    "%d, scale = %d",
                    intent->getXExtent(), intent->getYExtent(), intent->getOutXExtent(), intent->getOutYExtent(),
                    intent->getXScalePercent());

                // adjust the scan region based on scaling percentage
                uint32_t xin = intent->getXExtent();
                uint32_t yin = intent->getYExtent();
                uint32_t xout = intent->getOutXExtent();
                uint32_t yout = intent->getOutYExtent();
                ConvertToScanTypeHelper::resolveScanExtentsBasedOnScaling(xin, yin, xout, yout,
                                                                          (intent->getXScalePercent() * 1000));
                intent->setXExtent(xin);
                intent->setYExtent(yin);
                intent->setOutXExtent(xout);
                intent->setOutYExtent(yout);
                CHECKPOINTA(
                    "CopyPipelineResourceSetup: InXExtent = %d, InYExtent = %d, OutXExtent = %d, OutYExtent = %d",
                    intent->getXExtent(), intent->getYExtent(), intent->getOutXExtent(), intent->getOutYExtent());
            }
            else if (ticket_->shouldBeBorderless() &&
                     outputMediaSizeId == copyIntent_->getInputMediaSizeId())
            {
                //Get correct scaling values to convert from scan extents to output extents
                //Even in 1 to 1 borderless, scan still requires to clip by its risky margins and must be scaled to output extents
                auto outXExtent = outWidthAndHeight.width.get(dpi);
                auto outYExtent = outWidthAndHeight.height.get(dpi);
                auto scaleValueX = ConvertToScanTypeHelper::getScaleFactor(intent->getXExtent(), outXExtent);
                auto scaleValueY = ConvertToScanTypeHelper::getScaleFactor(intent->getYExtent(), outYExtent);

                intent->setXScalePercent(scaleValueX);
                intent->setYScalePercent(scaleValueY);
                intent->setOutXExtent(outXExtent);
                intent->setOutYExtent(outYExtent);
                CHECKPOINTA("CopyPipelineResourceSetup: borderless case, OutXExtent = %d, OutYExtent = %d, xScalePercent = %d, yScalePercent = %d",
                    intent->getOutXExtent(), intent->getOutYExtent(), intent->getXScalePercent(), intent->getYScalePercent());
            }
        }
    } //isScaleSupportedOnScanDevice

    bool copy_1Up = copyIntent_->getPagesPerSheet() == CopyOutputNumberUpCount::OneUp;
    if ((collateMode_ == CollateMode::COMPRESSED || copyBasicPipeline_) 
            && segmentType_ == SegmentType::FinalSegment && copy_1Up)  
            //Need to scan RGB for preview
            //twoup cannot currenlty use HW jpeg encoding, this will have to be fixed later on
    {
        //we need to request YCC data from Scanner
        intent->setScanInYcc(TRUE);
    }
    else
    {
        intent->setScanInYcc(FALSE);
    }

    if (copyIntent_->getBlankPageDetection() != dune::scan::types::BlankDetectEnum::Disable && isBlankPageDetectionSupported())
    {
        intent->setBlankPageDetect(copyIntent_->getBlankPageDetection());
    }

    //
    // These attributes are being hard coded for now.  Eventually we'll want to query
    // these values from the page assembler.
    if (copyEnterprisePipeline_)
    {
        if (simJob_)
        {
            intent->setCompressionType(dune::scan::Resources::CompressionType::NONE);
            intent->setRequestObjectMap(false);
        }
        else
        {
            intent->setCompressionType(dune::scan::Resources::CompressionType::GRAFIT);
            intent->setRequestObjectMap(true);
        }
    }
    else
    {
        intent->setCompressionType(dune::scan::Resources::CompressionType::NONE);
    }
    // Set the Media type
    if(prePrintConfiguration_ == HOME_PRO && copyIntent_->getScanSource() != dune::scan::types::ScanSource::MDF)
    {
        intent->setOriginalMediaType(scanPipeline_->mapImagingMediaTypeToScanMediaType(copyIntent_->getOutputMediaIdType()));
    }
    else
    {
        intent->setOriginalMediaType(copyIntent_->getOriginalMediaType());
    }

    // Update intent invert colors if ImagingOperation::InvertColors is not supported by imaging.
    if(isInvertColorsSupportedOnScanDevice())
    {
        CHECKPOINTA("CopyPipelineResourceSetup::setupScanDeviceIntent - Invert colors updated");
        intent->setNegative(copyIntent_->getInvertColors());
    }

    if(autoCropSupported && copyIntent_->getInputMediaSizeId() == MediaSizeId::ANY)
    {
        CHECKPOINTA("CopyPipelineResourceSetup::setupScanDeviceIntent - AutoCrop enabled setting extents");

        static constexpr auto xExtentPos = 0;
        static constexpr auto yExtentPos = 1;
        auto maxXYExtent = scanPipeline_->getMaxXYExtent(copyIntent_->getScanSource(), copyIntent_->getLongPlotScan());
        const auto xExtent = std::get<xExtentPos>(maxXYExtent);
        const auto yExtent = std::get<yExtentPos>(maxXYExtent);

        CHECKPOINTA("CopyPipelineResourceSetup::setupScanDeviceIntent - Auto Crop Max X and Y values %d, %d",xExtent, yExtent);
        if ((xExtent != 0) && (yExtent != 0))
        {
            intent->setXExtent(xExtent);
            intent->setYExtent(yExtent);
        }
        else
        {
            CHECKPOINTA("CopyPipelineResourceSetup::setupScanDeviceIntent - AutoCrop extents are not valid");
        }
    
        CHECKPOINTA("CopyPipelineResourceSetup::setupScanDeviceIntent - AutoCrop extents set to %d, %d",
                        intent->getXExtent(), intent->getYExtent());
    }

    // Setup additional ScanDevice-side image operations
    if (isAutoDeskewSupportedOnScanDevice())
    {
        intent->setAutoDeskew(copyIntent_->getAutoDeskew());
    }

    if (isBackgroundColorRemovalSupportedOnScanDevice())
    {
        intent->setBackgroundRemoval(copyIntent_->getBackgroundColorRemoval());
    }

    if (isBackgroundCleanupSupportedOnScanDevice())
    {
        intent->setBackgroundCleanup(copyIntent_->getBackgroundRemoval());
    }

    if (isBackgroundNoiseRemovalSupportedOnScanDevice())
    {
        intent->setScanNoiseRemoval(copyIntent_->getBackgroundNoiseRemoval());
    }
    //set scanMapQuality based on copyQuality    
    intent->setScanMapQuality(scanPipeline_->mapCopyQualityToScanMapQuality(copyIntent_->getCopyQuality()));

    /* setup Prescan for ID Card copy job */
    // if (copyIntent_->getScanSource() == dune::scan::types::ScanSource::GLASS &&
    //     copyIntent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD)
    // {
    //     CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent - prescan needed");
    //     intent->setAutoCrop(true);
    // }
    
    if (autoCropSupported && copyIntent_->getEdgeToEdgeScan() == true) {
        intent->setAutoCrop(false);
        CHECKPOINTA("CopyPipelineResourceSetup::setupScanDeviceIntent - Edge to edge scan is enabled, disabling auto crop\n");
    }

    //Add filepath for Scan to file instead of scan to strips
    if ((prePrintConfiguration_ == Product::HOME_PRO) &&  (copyIntent_->getScanSource() == dune::scan::types::ScanSource::MDF))
    {
        intent->setFilePath(ticket_->getStorePath());
        intent->setFileName("scan_from_sbb");
        intent->setFileFormat(dune::imaging::types::FileFormat::JPEG);
    }

    intent->setScanMediaSizeId(copyIntent_->getInputMediaSizeId());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: ColorMode:               %d", (uint32_t)intent->getColorMode());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: ScanSource:              %d", (uint32_t)intent->getScanSource());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: ContentType:             %d", (uint32_t)intent->getOriginalContentType());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: Media type:              %d", (uint32_t)intent->getOriginalMediaType());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: XScalePercent:           %d", (uint32_t)intent->getXScalePercent());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: YScalePercent:           %d", (uint32_t)intent->getYScalePercent());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: XResolution:             %d", (uint32_t)intent->getOutputXResolution());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: YResolution:             %d", (uint32_t)intent->getOutputYResolution());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: autocrop:                %d", (uint32_t)intent->getAutoCrop());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: XExtent:                 %d", intent->getXExtent());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: YExtent:                 %d", intent->getYExtent());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: OutXExtent:              %d", intent->getOutXExtent());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: OutYExtent:              %d", intent->getOutYExtent());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: XOffset:                 %d", intent->getXOffset());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: YOffset:                 %d", intent->getYOffset());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: Brightness:              %d", intent->getBrightness());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: Negative:                %d",   intent->getNegative());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: scanInYcc:               %d", intent->getScanInYcc());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: Margins Top -            %d , Bottom - %d, Left - %d, Right - %d",topMargin_, bottomMargin_, leftMargin_, rightMargin_);
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: AutoDeskew:              %d", intent->getAutoDeskew());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: BackgroundColorRemoval:  %d", intent->getBackgroundRemoval());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: BackgroundNoiseRemoval:  %d", intent->getScanNoiseRemoval());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: ScanMapQuality:          %d", intent->getScanMapQuality());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent: AdfMaxPagesToScan:       %d", intent->getAdfMaxPagesToScan());

    CHECKPOINTA("CopyPipelineResourceSetup: setupScanDeviceIntent - exit");
}


void CopyPipelineResourceSetup::setupIPADeviceIntent(std::shared_ptr<IIPADeviceIntents> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig)
{
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent - entry");
    intent->setScanImagingProfile(dune::scan::types::ScanImagingProfileType::COPY);
    intent->setScanSource(ConvertToScanTypeHelper::resolveScanSource(copyIntent_->getInputPlexMode(), copyIntent_->getScanSource()));
    intent->setColorMode(copyIntent_->getColorMode());
    intent->setOriginalContentOrientation(copyIntent_->getContentOrientation());
    intent->setOriginalContentType(copyIntent_->getOriginalContentType());
    intent->setBrightness(copyIntent_->getBrightness());
    intent->setAutoTone(copyIntent_->getAutoTone());
    intent->setAutoToneLevel(copyIntent_->getAutoToneLevel());
    intent->setAutoPaperColorRemoval(copyIntent_->getAutoPaperColorRemoval());
    intent->setAutoPaperColorRemovalLevel(copyIntent_->getAutoPaperColorRemovalLevel());
    intent->setBlankPageDetect(copyIntent_->getBlankPageDetection());
    intent->setRequestObjectMap(true);
    intent->setMultipleNumberOfLinesRequired(256);

    if (copyIntent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD)
    {
        CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent - ID Card - Change orientation LONGEDGE to SHORTEDGE");
        intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::SHORTEDGE);
    }
    else if (ticket_->getIntent()->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::BOOKMODE)
    {
        intent->setScanFeedOrientation(dune::scan::types::ScanFeedOrientation::LONGEDGE);
    }
    else
    {
        intent->setScanFeedOrientation(copyIntent_->getScanFeedOrientation());  // short/long edge feeding
    }

    auto orientation = dune::imaging::types::MediaOrientation::PORTRAIT;
    if (copyIntent_->getScanFeedOrientation() == dune::scan::types::ScanFeedOrientation::LONGEDGE)
    {
        orientation = dune::imaging::types::MediaOrientation::LANDSCAPE;
    }


    // Set default offset values in copy operations (100 pixels)
    // Adjusts scan start position to ensure proper margin handling and accurate image alignment
    // Based on the values and input margin, final left/right/top/bottom margins will be calculated within the CPB.
    intent->setXOffset(100); // X-axis offset: left margin adjustment
    intent->setYOffset(100); // Y-axis offset: top margin adjustment

    intent->setOutputXResolution(copyIntent_->getOutputXResolution());
    intent->setOutputYResolution(copyIntent_->getOutputYResolution());
    //setupScanMargins(intent, Resolution::E600DPI, true, true);   

    intent->setScaleToFitEnabled(copyIntent_->getScaleToFitEnabled());

    if(isScaleSupportedOnScanDevice())
    {
        //considering the scaling cases 2up, Fit to Page and Custom percentage. The selections are mutually exclusive

        int dpi = 0;
        dpi = ConvertToScanTypeHelper::getResolutionIntFromEnum(copyIntent_->getOutputXResolution());

        auto outWidthAndHeight = dune::imaging::types::convertMediaSizeIdToWidthAndHeight(copyIntent_->getOutputMediaSizeId(), orientation);

        // Set actual media size without considering margins for accurate scale factor calculation in IPA device
        // This is required for layout calculations such as N-up, booklet, and fit-to-size operations
        intent->setOutXExtent(outWidthAndHeight.width.get(dpi));   // Output width (pixels)
        intent->setOutYExtent(outWidthAndHeight.height.get(dpi));  // Output height (pixels)

        if (copyIntent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD)
        {
            intent->setXScalePercent(NO_SCALE_PERCENT);
            intent->setYScalePercent(NO_SCALE_PERCENT);

            // For ID card scans, scale to fit is not applicable
            intent->setScaleToFitEnabled(false);
        }
        else
        {
            // Initialize scale ratio to 100% (will be recalculated later by IPA device)
            // IPA device determines optimal scale factor in case below
            // - Scale to Fit
            // - N-up
            // - Booklet
            intent->setXScalePercent(copyIntent_->getXScalePercent());
            intent->setYScalePercent(copyIntent_->getYScalePercent());
        }
    }

    intent->setPagesPerSheet(copyIntent_->getPagesPerSheet());
    intent->setBookletFormat(copyIntent_->getBookletFormat());

    intent->setInputMediaSizeId(copyIntent_->getInputMediaSizeId());

    if (simJob_)
    {
        intent->setCompressionType(dune::scan::Resources::CompressionType::NONE);
        intent->setRequestObjectMap(false);
    }
    else
    {
        intent->setCompressionType(dune::scan::Resources::CompressionType::GRAFIT);
        intent->setRequestObjectMap(true);
    }   
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: ColorMode:               %d", (uint32_t)intent->getColorMode());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: ScanSource:              %d", (uint32_t)intent->getScanSource());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: ContentType:             %d", (uint32_t)intent->getOriginalContentType());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: XScalePercent:           %d", (uint32_t)intent->getXScalePercent());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: YScalePercent:           %d", (uint32_t)intent->getYScalePercent());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: XResolution:             %d", (uint32_t)intent->getOutputXResolution());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: YResolution:             %d", (uint32_t)intent->getOutputYResolution());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: XExtent:                 %d", intent->getXExtent());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: YExtent:                 %d", intent->getYExtent());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: OutXExtent:              %d", intent->getOutXExtent());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: OutYExtent:              %d", intent->getOutYExtent());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: XOffset:                 %d", intent->getXOffset());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: YOffset:                 %d", intent->getYOffset());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: Brightness:              %d", intent->getBrightness()); 
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: AutoTone:                %d", intent->getAutoTone());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: AutoToneLevel:           %d", intent->getAutoToneLevel());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: PagePerSheet:            %d", intent->getPagesPerSheet());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: BookletFormat:           %d", intent->getBookletFormat());
    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent: FitToPage:               %d", intent->getScaleToFitEnabled());


    CHECKPOINTA("CopyPipelineResourceSetup: setupIPADeviceIntent - exit");
}
void CopyPipelineResourceSetup::DetectMediaFromSensor()
{
    CHECKPOINTC("CopyPipelineResourceSetup: DetectMediaFromSensor - entry  copyIntent_->getInputMediaSizeId() %d  output media size = %d",(int)copyIntent_->getInputMediaSizeId(), (int)copyIntent_->getOutputMediaSizeId());

    if ( copyIntent_->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::ANY &&
         prePrintConfiguration_ == Product::ENTERPRISE ) // Enterprise & Original Size : Any
    {
        dune::scan::scanningsystem::IMedia *scanMedia = ticket_->getScanMediaInterface();
        dune::scan::types::ScanSource ticketScanSource = ticket_->getIntent()->getScanSource();
        std::pair<dune::imaging::types::MediaSizeId, dune::imaging::types::MediaOrientation> mediaDetected;

        auto scanSources = scanMedia->getInputs();
       
        CHECKPOINTC("CopyPipelineResourceSetup::DetectMediaFromSensor - Scan Source ticketScanSource %d", (int)ticketScanSource);
        for (const auto& scanSource : scanSources)
        {
            if (scanSource->getType() == ticketScanSource)
            {
                mediaDetected = scanSource->getMediaDetectionStatus(); // get current media info
                CHECKPOINTC("CopyPipelineResourceSetup::DetectMediaFromSensor - printScanMediaDetectionStatus [%s,%s]",
                    dune::imaging::types::EnumNameMediaSizeId(mediaDetected.first),
                    dune::imaging::types::EnumNameMediaOrientation(mediaDetected.second));
                break;
            }
        }
        
        if (ticket_->getIntent()->getInputMediaSizeId() != mediaDetected.first)
        {
            // Scan Media Size
            CHECKPOINTC("CopyPipelineResourceSetup::DetectMediaFromSensor - setInputMediaSizeId = %d", (int)mediaDetected.first);
            ticket_->getIntent()->setInputMediaSizeId(mediaDetected.first);
       
            if(ticket_->getIntent()->getOutputMediaSizeId() == dune::imaging::types::MediaSizeId::ANY)
            {
                ticket_->getIntent()->setMatchOriginalOutputMediaSizeId(mediaDetected.first);
                CHECKPOINTC("CopyPipelineResourceSetup::DetectMediaFromSensor - setMatchOriginalOutputMediaSizeId = %d", (int)mediaDetected.first);
            }
            
            // Scan Feed Orientation
            dune::scan::types::ScanFeedOrientation scanFeedOrientation;
            if (dune::imaging::types::MediaOrientation::LANDSCAPE == mediaDetected.second)
            {
                scanFeedOrientation = dune::scan::types::ScanFeedOrientation::LONGEDGE;
            }
            else
            {
                scanFeedOrientation = dune::scan::types::ScanFeedOrientation::SHORTEDGE;
            }

            if (ticket_->getIntent()->getScanFeedOrientation() != scanFeedOrientation)
            {
                ticket_->getIntent()->setScanFeedOrientation(scanFeedOrientation);
            }
        }
    }
    else
    {
        CHECKPOINTC("CopyPipelineResourceSetup::DetectMediaFromSensor - Not Enterprise Or input media not Any size");
    }

    CHECKPOINTC("CopyPipelineResourceSetup: DetectMediaFromSensor - exit");
}
void CopyPipelineResourceSetup::setupMarkingFilterIntent(std::shared_ptr<IMarkingFilterIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig)
{
    CHECKPOINTA("CopyPipelineResourceSetup::setupMarkingFilterIntent - ENTRY");
    CHECKPOINTA("CopyPipelineResourceSetup::setupMarkingFilterIntent after get intent from MF ticket");
    DUNE_UNUSED(resourceConfig);
    auto mfSettings = intent->getFilterSettings();
    CHECKPOINTA("CopyPipelineResourceSetup::setupMarkingFilterIntent after get filter settings from intent");
    if (mfSettings == nullptr)
    {
        assert(mfSettings == nullptr);
        CHECKPOINTA("CopyPipelineResourceSetup::setupMarkingFilterIntent mfSettings is null");
    }
    else
    {
        mfSettings->setPlex(copyIntent_->getInputPlexMode());
        mfSettings->setContentOrientation(copyIntent_->getContentOrientation());
        if (copyIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::TwoUp)
        {
            mfSettings->setNumberUpTilePlacementType(dune::imaging::types::NumberUpTilePlacementType::LeftToRightNupTilePlacement);
            mfSettings->setNumberUpPresentationDirection(dune::imaging::types::NumberUpPresentationDirection::ToRightToBottom);
            mfSettings->setCopyOutputNumberUpCount(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
        }
        else if (copyIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::FourUp)
        {
            mfSettings->setNumberUpTilePlacementType(dune::imaging::types::NumberUpTilePlacementType::LeftToRightNupTilePlacement);
            mfSettings->setNumberUpPresentationDirection(copyIntent_->getNumberUpPresentationDirection());
            mfSettings->setCopyOutputNumberUpCount(dune::imaging::types::CopyOutputNumberUpCount::FourUp);
        }
        else
        {
            mfSettings->setNumberUpTilePlacementType(dune::imaging::types::NumberUpTilePlacementType::IDCardScanTilePlacement);
            mfSettings->setNumberUpPresentationDirection(dune::imaging::types::NumberUpPresentationDirection::ToRightToBottom);
            mfSettings->setCopyOutputNumberUpCount(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
        }
        // Borders around N-up images
        mfSettings->setImageBorder(copyIntent_->getImageBorder());

        CHECKPOINTA("CopyPipelineResourceSetup::setupMarkingFilterIntent after assigning filter settings in MF settings");
        intent->setFilterSettings(mfSettings);

    }
    
    CHECKPOINTA("CopyPipelineResourceSetup::setupMarkingFilterIntent after set filter settings");

    CHECKPOINTA("CopyPipelineResourceSetup::setupMarkingFilterIntent - EXIT");
}

void CopyPipelineResourceSetup::setupLayoutFilterIntent(std::shared_ptr<dune::imaging::Resources::ILayoutFilterIntent> intent,
                                                        std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>)
{
    CHECKPOINTA("CopyPipelineResourceSetup::setupLayoutFilterIntent - ENTRY");

    // Set Sequencing Params
    dune::imaging::Resources::LayoutSequencingParams layoutSequencingParams{};
    std::shared_ptr<dune::imaging::Resources::SequencingParams> sequencingParams{getSequencingParams()};
    if (sequencingParams)
    {
        layoutSequencingParams.collationCopies = sequencingParams->collationCopies;
        layoutSequencingParams.uncollationCopies = sequencingParams->uncollationCopies;
        layoutSequencingParams.pagesNeededToSequence = sequencingParams->pagesNeededToSequence;
        layoutSequencingParams.updateDetails = sequencingParams->updateDetails;
        layoutSequencingParams.booklet = sequencingParams->booklet;
    }
    layoutSequencingParams.imagesPerSheet = getImagesPerSheet();
    layoutSequencingParams.waitForSheet = false;
    
    // Set Intents
    intent->setSequencingParams(layoutSequencingParams);
    intent->setNupLayout(getNUpParameters());

    if (copyIntent_->getImageBorder() == dune::imaging::types::ImageBorder::DefaultLineBorder)
    {
        intent->setImageBorders(dune::imaging::types::ImageBorders::PRINT_BORDERS);
    }

    for(const auto& location : dune::imaging::types::EnumValuesStampLocation()){
        auto stampParams = getStampParametersLocation(location);
        if(stampParams != nullptr){
            intent->addStamp(*stampParams);
        }
    }

    dune::imaging::types::WatermarkParams watermarkParams{getWatermarkParameters()};
    intent->setWatermark(watermarkParams);    

    if (copyEnterprisePipeline_)
    {
        // Currently use RowPipe for GrafitTile, so requires to decompress image always.
        intent->setDecompressImage(true);
    } 
    else
    {
        // Note that getRotationAngle return a value from 0 to 3 and LayoutFilter use RotationCW
        intent->setImageRotation(dune::imaging::types::RotationCW(getRotationAngle() * 90));
    }

    CHECKPOINTA("CopyPipelineResourceSetup::setupLayoutFilterIntent - EXIT");
}

void CopyPipelineResourceSetup::setupPageAssemblerIntent(std::shared_ptr<IPageAssemblerIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig)
{
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent - ENTRY");
    DUNE_UNUSED(resourceConfig);

    doPrintEarlyWarning(intent);

    if(copyIntent_->getOutputMediaSizeId() == dune::imaging::types::MediaSizeId::ANY && 
       prePrintConfiguration_ == Product::ENTERPRISE) // Enterprise & Original Size : Any
    {
        intent->setOutputMediaSizeId(copyIntent_->getMatchOriginalOutputMediaSizeId());
    }
    else 
    {
        intent->setOutputMediaSizeId(copyIntent_->getOutputMediaSizeId());
    }
    
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: InputMediaSize %d", (uint32_t)copyIntent_->getInputMediaSizeId());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: OutputMediaSize %d", (uint32_t)copyIntent_->getOutputMediaSizeId());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: AnyOutputMediaSize %d", (uint32_t)copyIntent_->getMatchOriginalOutputMediaSizeId());

    intent->setOutputDuplexMode(copyIntent_->getOutputPlexMode());
    if(collateMode_ == CollateMode::UNCOMPRESSED)
    {
        intent->setCollatedCopies(copyIntent_->getCopies());

    }
    else if (collateMode_ == CollateMode::COMPRESSED)
    {
        intent->setCollatedCopies(1);
    }
    else
    {
        intent->setUnCollatedCopies(copyIntent_->getCopies());
    }

    intent->setOutputMediaSource(copyIntent_->getOutputMediaSource());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: OutputMediaSource %d", (uint32_t)copyIntent_->getOutputMediaSource());
    intent->setOutputMediaType(copyIntent_->getOutputMediaIdType());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: OutputMediaType %d", (uint32_t)copyIntent_->getOutputMediaIdType());

    intent->setJobType(dune::job::JobType::COPY);
    intent->setPlexBindingType(copyIntent_->getOutputPlexBinding());
    intent->setResolution(copyIntent_->getOutputXResolution());
    intent->setPrintQuality(PrintQuality::NORMAL);
    intent->setCopyQuality(copyIntent_->getCopyQuality());
    intent->setOriginalContentType(copyIntent_->getOriginalContentType());

    if (isMixedSizeOriginals())
    {
        intent->setMixedMediaOutput(true);
    }

    MarginsParameters marginParams;
    marginParams.setMediaSource(copyIntent_->getOutputMediaSource());
    Margins mediaMargins = std::get<1>(services_.mediaInterface->getMargins(marginParams));
    uint32_t res = ConvertToScanTypeHelper::getResolutionIntFromEnum(intent->getResolution());
    topMargin_ = mediaMargins.getTop().get(res);
    bottomMargin_ = mediaMargins.getBottom().get(res);
    leftMargin_ = mediaMargins.getLeft().get(res);
    rightMargin_ = mediaMargins.getRight().get(res);

    intent->setTopMargin(topMargin_);
    intent->setBottomMargin(bottomMargin_);
    intent->setLeftMargin(leftMargin_);
    intent->setRightMargin(rightMargin_);

    intent->setInputDuplexMode(copyIntent_->getInputPlexMode());
    intent->setContentOrientation(copyIntent_->getContentOrientation());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: MediaSizeId: %d", (uint32_t)intent->getOutputMediaSizeId());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: InDuplexMode: %d", (uint32_t)intent->getInputDuplexMode());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: OutputDuplexMode: %d", (uint32_t)intent->getOutputDuplexMode());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: CollatedCopies: %d", intent->getCollatedCopies());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: UncollatedCopies: %d", intent->getUnCollatedCopies());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: MediaSource: %d", (uint32_t)intent->getOutputMediaSource());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: MediaType: %d", (uint32_t)intent->getOutputMediaType());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: PlexBinding: %d", (uint32_t)intent->getPlexBindingType());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: Resolution: %d", (uint32_t)intent->getResolution());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: PrintQuality: %d", (uint32_t)intent->getPrintQuality());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: CopyQuality: %d", (uint32_t)intent->getCopyQuality());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: OriginalContentType: %d", (uint32_t)intent->getOriginalContentType());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: ContentType: %d", (uint32_t)intent->getContentOrientation());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: MixedMediaOutput: %d", (uint32_t)intent->getMixedMediaOutput());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent: Margins Top - %d , Bottom - %d, Left - %d, Right - %d",topMargin_, bottomMargin_, leftMargin_, rightMargin_);
    CHECKPOINTA("CopyPipelineResourceSetup: setupPageAssemblerIntent - EXIT");
}

void CopyPipelineResourceSetup::setupRtpFilterTicketIntent(std::shared_ptr<IRtpFilterIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig)
{
    CHECKPOINTA("CopyPipelineResourceSetup::setupRtpFilterTicketIntent");
    
    DUNE_UNUSED(intent);
    DUNE_UNUSED(resourceConfig);

    CHECKPOINTA("CopyPipelineResourceSetup::setupRtpFilterTicketIntent Done");
}

void CopyPipelineResourceSetup::setupPrintDeviceIntent(std::shared_ptr<IPrintDeviceIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig)
{
    CHECKPOINTA("CopyPipelineResourceSetup: setupPrintDeviceIntent - ENTRY");
    DUNE_UNUSED(resourceConfig);

    bool mustHonorCollatedCopies_ = false;

    //In case Copy doing the collate hence set collated copies to 1
    if(copyBasicPipeline_)
    {
        intent->setIsCollationJob(false);
        intent->setCollationCopies(1);
        intent->setUncollatedCopies(1);
    }
    else if(collateMode_ == CollateMode::UNCOMPRESSED)
    {
        intent->setIsCollationJob(true);
        intent->setCollationCopies(copyIntent_->getCopies());
    }
    else if (collateMode_ == CollateMode::COMPRESSED)
    {
        intent->setIsCollationJob(false);
        intent->setCollationCopies(1);
    }
    else
    {
        intent->setUncollatedCopies(copyIntent_->getCopies());
    }

    intent->setJobType(dune::job::JobType::COPY);

    intent->setJobPageCount(copyIntent_->getCopies());
    intent->setJobOffsetMode(copyIntent_->getJobOffsetMode());

    CHECKPOINTC("CopyPipelineResourceSetup: setupPrintDeviceIntent: CollationCopies %d", intent->getCollationCopies(mustHonorCollatedCopies_));
    CHECKPOINTC("CopyPipelineResourceSetup: setupPrintDeviceIntent: uncollatedCopies %d", intent->getUncollatedCopies());
    CHECKPOINTC("CopyPipelineResourceSetup: setupPrintDeviceIntent: IsCollationJob %d", intent->isCollationJob());
    CHECKPOINTC("CopyPipelineResourceSetup: setupPrintDeviceIntent: JobPageCount %d", intent->getJobPageCount());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPrintDeviceIntent: OutputMediaType %d", (uint32_t)copyIntent_->getOutputMediaIdType());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPrintDeviceIntent: JobOffset %d", (uint32_t)copyIntent_->getJobOffsetMode());
    CHECKPOINTA("CopyPipelineResourceSetup: setupPrintDeviceIntent - EXIT");
}

void CopyPipelineResourceSetup::setupImagePersisterIntent(std::shared_ptr<IImagePersisterIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig)
{
    CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - ENTRY");
    intent->setFileName(resourceConfig->fileName);
    intent->setStripHeight(DEFAULT_STRIP_HEIGHT);
    if (copyIntent_->getCopyQuality() == PrintQuality::BEST)
    {
        intent->setStripHeight(DEFAULT_STRIP_HEIGHT * 2);
    }
    intent->setNotificationStrategy(resourceConfig->notificationStrategy);
    if (copyIntent_->getColorMode() == ColorMode::GRAYSCALE)
    {
        intent->setEncodeJpegInRGB(false);
    }

    switch (prePrintConfiguration_)
    {
        case Product::LFP:
                CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - LFP");
                intent->setResolutionMode(dune::imaging::types::Resolution::E600DPI); // 200, 300 & 600 will be scaled to 600 dpi
                intent->setColorMode(dune::imaging::types::ColorMode::COLOR); // For now only supported color, in future use copyIntent_->getColorMode()
                intent->setStripHeight(LFP_DEFAULT_STRIP_HEIGHT);
            break;
        case Product::HOME_PRO:
            CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - HOME_PRO");
            if (copyIntent_->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp)
            {
                CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - HomePro - Not OneUp");
                intent->setFileFormat(dune::imaging::types::FileFormat::JPEG);
            }
            else
            {
                CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - it is OneUp");
                // For OneUp and copyBasicPipeline, is correct the GRAFIT format? -> It should be tested
                if (copyBasicPipeline_ == true)
                {
                    CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - setting JPEG");
                    intent->setEncodeJpegInRGB(false); // Enable jpeg h/w for moreto

                }
            }
            break;
        case Product::ENTERPRISE:
            intent->setStripHeight(ENTERPRISE_DEFAULT_STRIP_HEIGHT);
            intent->setUsableImageDetection(true);
            break;
        default:
            intent->setFileFormat(dune::imaging::types::FileFormat::CGRFT);
            break;
    }

    // Checking for a collation job after everything else is setup because collate could be an additional ask on previous setup
    // Basic copy pipeline is common for both collate and uncollate
    if ((collateMode_ == CollateMode::COMPRESSED) || (copyBasicPipeline_))
    {
        CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - compressed or basicopy");
        intent->setCompressionFactor(copyIntent_->getCompressionFactor());
        CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - compressionFactor = %d", intent->getCompressionFactor());
        if (copyBasicPipeline_)
        {
            if((currentStage_ == Stage::Scan_Basic_Print) &&
            (copyIntent_->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp))
            {
                CHECKPOINTC("CopyPipelineResourceSetup::setupImagePersister - set the strategy to ON_COMPLETED for ADF + 2Up");
                intent->setNotificationStrategy(dune::imaging::types::NotificationStrategy::ON_COMPLETED);        
            }
            else
            {
                intent->setNotificationStrategy(dune::imaging::types::NotificationStrategy::ON_STARTED);
            }
            intent->setJpegHwEnable(false); //disable the jpeg HW block for Encoding
        }
        else
        {
            intent->setJpegHwEnable(true); //enable the jpeg HW block for Encoding
            intent->setStripHeight(DEFAULT_STRIP_HEIGHT * 4);
        }
        if(copyIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::OneUp)
        {
            //twoup cannot currenlty use HW jpeg encoding, this will have to be fixed later on
            intent->setJpegHwEnable(true); //enable the jpeg HW block for Encoding
            intent->setStripHeight(DEFAULT_STRIP_HEIGHT * 4);
            // if quality is set to BEST and it is a duplex job we want to enable VQ on basicPipelines. 
            // Also set VQ enabled for collate on homepro non-basicpipelines 
            // But note that VQ will be enabled only if the ImagePersister config has it enabled as well
            if((copyIntent_->getCopyQuality() == PrintQuality::BEST) || (collateMode_ == CollateMode::COMPRESSED && !copyBasicPipeline_))
            {
                CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - setting VQ");
                intent->setJpegVqEnable(true); 
                intent->setNotificationStrategy(dune::imaging::types::NotificationStrategy::ON_COMPLETED);
            }
        }
    }

    if (copyIntent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::BOOKMODE &&
        copyIntent_->getContentOrientation() == dune::imaging::types::ContentOrientation::PORTRAIT)
    {
        intent->setNotificationStrategy(dune::imaging::types::NotificationStrategy::ON_COMPLETED);  
        intent->setReorderType(dune::imaging::types::Reorder::SWAP);
    }
    
    if (copyIntent_->getBlankPageDetection() == dune::scan::types::BlankDetectEnum::DetectAndSupress)
    {
        // for waiting end image result to suppress blank page
        intent->setNotificationStrategy(dune::imaging::types::NotificationStrategy::ON_COMPLETED);
        intent->setBlankPageSuppression(true);
    }

    if (simJob_ && prePrintConfiguration_ != Product::LFP) { intent->setFileFormat(dune::imaging::types::FileFormat::ZLIB); } //Can't do JPEG compression in sim currently.
    CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - filename = %s", intent->getFileName().c_str());
    CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - fileFormat = %d", intent->getFileFormat());
    CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - colorMode = %d", intent->getColorMode());
    CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - CompressionFactor = %d", intent->getCompressionFactor());
    CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - encodeJpegInRGB = %d", intent->getEncodeJpegInRGB());
    CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - JpegHwEnable = %d", intent->getJpegHwEnable());
    CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - JpegVqEnable = %d", intent->getJpegVqEnable());
    CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - NotificationStrategy = %d", intent->getNotificationStrategy());
    CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - StripHeight = %d", intent->getStripHeight());
    CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - ResolutionMode = %d", intent->getResolutionMode()); 
    CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterIntent - EXIT");
}

void CopyPipelineResourceSetup::setupBufferingImagePersisterIntent(std::shared_ptr<IImagePersisterIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig)
{
    DUNE_UNUSED(resourceConfig);
    intent->setFileName("persistBufferRaster");

    switch (prePrintConfiguration_)
    {
        case Product::LFP:
            intent->setStripHeight(DISK_BUFFERING_STRIP_HEIGHT);
            intent->setFileFormat(dune::imaging::types::FileFormat::RAW);
            break;
        case Product::ENTERPRISE:
            intent->setFileFormat(dune::imaging::types::FileFormat::TGRFT);
            intent->setStripHeight(ENTERPRISE_DEFAULT_STRIP_HEIGHT);
            if (simJob_) { intent->setFileFormat(dune::imaging::types::FileFormat::ZLIB);}
            break;
        default:
            intent->setStripHeight(DISK_BUFFERING_STRIP_HEIGHT);
            intent->setFileFormat(dune::imaging::types::FileFormat::RAW);
            break;
    }
    intent->setNotificationStrategy(dune::imaging::types::NotificationStrategy::ON_STARTED);
    if (copyEnterprisePipeline_)
    {
        intent->setNotificationStrategy(dune::imaging::types::NotificationStrategy::ON_COMPLETED);
    }
    
    if (copyIntent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::BOOKMODE &&
        copyIntent_->getContentOrientation() == dune::imaging::types::ContentOrientation::PORTRAIT)
    {
        intent->setNotificationStrategy(dune::imaging::types::NotificationStrategy::ON_COMPLETED);  
        intent->setReorderType(dune::imaging::types::Reorder::SWAP);
    }
}

void CopyPipelineResourceSetup::setupImageRetrieverIntent(std::shared_ptr<IImageRetrieverIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig)
{
    CHECKPOINTA("CopyPipelineResourceSetup::setupImageRetrieverIntent - ENTRY");

    intent->setGenerateStripImage(true);
    intent->setScanImagingProfile(dune::scan::types::ScanImagingProfileType::COPY);
    if (ticket_->getExecutionMode() == dune::job::ExecutionMode::RETRIEVE && prePrintConfiguration_ == Product::ENTERPRISE)
    {
        intent->setRemoveImageWhenFinish(false);
    }
    else
    {
        intent->setRemoveImageWhenFinish(true);
    }
    intent->setRotationAngle(getRotationAngle());
    intent->setPerformRotation(resourceConfig->performRotation);
    intent->setScaleDownFactor(1);
    intent->setWorkingStrips(3);
    auto mediaHandlingMgrPointer = resourceConfig->doMediaHandlingCheck ? services_.mediaHandlingMgr : nullptr;
    CHECKPOINTB("CopyPipelineResourceSetup::setupImageRetrieverIntent - mediaHandlingMgrPointer is %s", mediaHandlingMgrPointer ? "set" : "a nullptr");
    intent->setMediaPointers(services_.mediaInterface, services_.mediaHandlingSettings, services_.mediaInfo, mediaHandlingMgrPointer);

    // We can have multiple Retriever in the same pipeline and don't need all of them to allow
    // to auto rotate. So we set imageRetrieverAllowAutoRotation as true in the config to those we want.
    // to auto rotate tolerance > 0. So we set autoRotationWidthRollMatchingTolerance as 14 (3.5mm) in the config to those we want.
    // And for those, we set the value that is present in the intent.
    bool performAutoRotation = resourceConfig->imageRetrieverAllowAutoRotation ? copyIntent_->getAutoRotate() : false;
    intent->setPerformAutoRotation(performAutoRotation);

    CHECKPOINTC("CopyPipelineResourceSetup::setupImageRetrieverIntent autoRotationWidthRollMatchingTolerance in Cin --> %d", resourceConfig->autoRotationWidthRollMatchingTolerance);
    intent->setAutoRotationTolerance(resourceConfig->autoRotationWidthRollMatchingTolerance);

    // For Beam
    if (hasSharedPaperPath_)
    {
        intent->setRemoveImageWhenFinish(false);
    }

    // Set rotation angle 1 if it's 2up job
    if (copyIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::TwoUp
        && copyEnterprisePipeline_ == false)
    {
        intent->setAllowPrintIntentRotation(false);
        // intent->setScaleDownFactor(2);
    }

    // Checking for a collation job after everything else is setup because collate could be an additional ask on previous setup
    // For Basic pipeline, ImageRetriver will handle collation and uncollation
    if(copyBasicPipeline_ == true)
    {
        // Set for print duplex cases
        if(copyIntent_->getOutputPlexMode()== dune::imaging::types::Plex::DUPLEX)
        {
            intent->setDuplexJob(true);
            
            // For Marconi, checking for Duplex rotation should be performed in case of NOT nUp
            // Duplex Rotation is in case of PlexSide::SECOND && PlexBinding::LONG_EDGE -> Rotation = 180 degrees
            if (copyIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::OneUp)
            {
                intent->setCheckDuplexRotation(true);
                CHECKPOINTA("CopyPipelineResourceSetup::setupImageRetrieverIntent - Check Duplex Rotation");
                if(simJob_)
                {
                    intent->setCheckDuplexRotation(false);
                }
            }            
        }
        // For Victoria and low end mem products do not keep image for one up uncollated multipage copy
        // jobs, it may cause memory constraints issues and hange the copy job.
        if ((copyIntent_->getCopies()== 1) && (copyIntent_->getCollate() == SheetCollate::Uncollate))
        {
            CHECKPOINTA("CopyPipelineBuilder: setRemoveImageWhenFinish: Remove image for Uncollate");
            intent->setRemoveImageWhenFinish(true);
        }
        else
        {
            CHECKPOINTA("CopyPipelineBuilder: setRemoveImageWhenFinish:  Do not Remove image");
            intent->setRemoveImageWhenFinish(false);
        }
    }
    else if (collateMode_ == CollateMode::COMPRESSED || prePrintConfiguration_ == Product::LFP)
    {
        intent->setRemoveImageWhenFinish(false);

        if(copyIntent_->getOutputPlexMode()== dune::imaging::types::Plex::DUPLEX)
        {
            intent->setDuplexJob(true);
        }
    }

    // Set Sequencing Params
    auto sequencingParameters = getSequencingParams();
    if (sequencingParameters)
        sequencingParameters->performMediaHandling = resourceConfig->doMediaHandlingCheck;
    intent->setSequencingParams(sequencingParameters);
    
    CHECKPOINTA("CopyPipelineResourceSetup::setupImageRetrieverIntent collateMode_: %d", (uint32_t)collateMode_);

    CHECKPOINTA("CopyPipelineResourceSetup::setupImageRetrieverIntent - EXIT");
}

void CopyPipelineResourceSetup::setupBufferingImageRetrieverIntent(std::shared_ptr<IImageRetrieverIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig)
{
    CHECKPOINTA("CopyPipelineResourceSetup::setupBufferingImageRetrieverIntent - ENTRY");
    intent->setGenerateStripImage(true);
    intent->setScanImagingProfile(dune::scan::types::ScanImagingProfileType::COPY);
    intent->setRemoveImageWhenFinish(resourceConfig->removeImageWhenFinish);
    intent->setRotationAngle(0);
    intent->setPerformRotation(resourceConfig->performRotation);
    intent->setScaleDownFactor(1);
    intent->setWorkingStrips(3);
    if(prePrintConfiguration_ == Product::ENTERPRISE)
    {
        intent->setDecompressImage(true);
    }
    auto mediaHandlingMgrPointer = resourceConfig->doMediaHandlingCheck ? services_.mediaHandlingMgr : nullptr;
    CHECKPOINTB("CopyPipelineResourceSetup::setupBufferingImageRetrieverIntent - mediaHandlingMgrPointer is %s", mediaHandlingMgrPointer ? "set" : "a nullptr");
    intent->setMediaPointers(services_.mediaInterface, services_.mediaHandlingSettings, services_.mediaInfo, mediaHandlingMgrPointer);
    intent->setPerformMediaHandlingChecks(resourceConfig->doMediaHandlingCheck);

    CHECKPOINTA("CopyPipelineResourceSetup::setupBufferingImageRetrieverIntent - EXIT");
}
void CopyPipelineResourceSetup::setupScanRegion(std::shared_ptr<IScanDeviceIntent>    sdintent,
                                        dune::imaging::types::MediaSizeId       mediaSize,
                                        dune::scan::types::ScanFeedOrientation  orientation,
                                        dune::imaging::types::Resolution        resolution,
                                        dune::scan::types::ScanCaptureModeType  mode)
{
    

    // TODO - resolution split into X and Y, calculation below needs update
    uint32_t resolutionInt = ConvertToScanTypeHelper::getResolutionIntFromEnum(resolution);

    CHECKPOINTA("CopyPipelineResourceSetup::setupScanRegion Height after maxExtent Validation: mediaSize:%d, orientation:%d, resolutionInt:%d"
    , mediaSize, orientation, resolutionInt);

    auto xyExtent = ConvertToScanTypeHelper::resolveXYExtent(mediaSize, orientation, resolution);
    uint32_t width = std::get<0>(xyExtent);
    uint32_t height = std::get<1>(xyExtent);
    height = ConvertToScanTypeHelper::resolveMaxExtentWithLength(height, maxLengthConfig_.scanMaxCm, resolutionInt); //copy only has a max length so no more parameters needed
    CHECKPOINTA("CopyPipelineResourceSetup::setupScanRegion Height after maxExtent Validation: %d", height);

    // If edgeToEdgeScan is true, xExtend_ option changes to MAX
    if(copyIntent_->getEdgeToEdgeScan())
    {
        CHECKPOINTA("CopyPipelineResourceSetup: setupScanRegion: edgeToEdge is true -> MAX XExtent");
        // Let the scan to set the MAX
        sdintent->setXExtent(0);
    }
    else // Configure the extents in 600 units
    {
        sdintent->setXExtent(width);
    }

    if (mode == dune::scan::types::ScanCaptureModeType::IDCARD)
    {
        if(copyBasicPipeline_)
        {
            CHECKPOINTA("CopyPipelineResourceSetup: setupScanRegion: copyBasicPipeline_ is true -> remove specific padding value from height %d", height);
            uint32_t topPad = RES_CONVERT(topSpecificPadding_*10, 254, 300);
            uint32_t bottomPad = RES_CONVERT(bottomSpecificPadding_*10, 254, 300);
            uint32_t printableHeightMinusMargins = height - RES_CONVERT((topMargin_ + bottomMargin_)*10, 254, 300);
            uint32_t printableHeightPerImage = printableHeightMinusMargins/2 - (topPad + bottomPad);

            sdintent->setYExtent(printableHeightPerImage);
        }
        else
        {
            sdintent->setYExtent((height / 2));
        }
    }
    else
    {
        sdintent->setYExtent(height);
    }

    CHECKPOINTA("CopyPipelineResourceSetup: setupScanRegion: XExtent: %d", sdintent->getXExtent());
    CHECKPOINTA("CopyPipelineResourceSetup: setupScanRegion: YExtent: %d", sdintent->getYExtent());
}

void CopyPipelineResourceSetup::setupScanMargins(std::shared_ptr<IScanDeviceIntent> sdintent,
                                                    dune::imaging::types::Resolution resolution, 
                                                    bool includePrintMargins, 
                                                    bool includeScanMargins)
{
    CHECKPOINTA("CopyPipelineResourceSetup: SetupScanMargins - ENTRY");
    //Get Print Margin values
    uint32_t resolutionInt = ConvertToScanTypeHelper::getResolutionIntFromEnum(resolution);
    MarginsParameters marginParams;
    marginParams.setMediaSource(copyIntent_->getOutputMediaSource());
    Margins mediaMargins = std::get<1>(services_.mediaInterface->getMargins(marginParams));
    uint32_t printTop = 0;
    uint32_t printBottom = 0;
    uint32_t printLeft = 0;
    uint32_t printRight = 0;
    if(includePrintMargins)
    {
        CHECKPOINTA("CopyPipelineResourceSetup: SetupScanMargins - includePrintMargins");
        printTop = mediaMargins.getTop().get(resolutionInt);
        printBottom = mediaMargins.getBottom().get(resolutionInt);
        printLeft = mediaMargins.getLeft().get(resolutionInt);
        printRight = mediaMargins.getRight().get(resolutionInt);
        CHECKPOINTA("CopyPipelineResourceSetup: SetupScanMargins - PrintMargins: Top - %d, Bottom - %d, Left - %d, Right - %d", printTop, printBottom, printLeft, printRight);
    }

    //Get Scan Margin values
    Margins scanMargins = scanPipeline_->getScanMargins(copyIntent_->getScanSource());
    uint32_t scanTop = 0;
    uint32_t scanBottom = 0;
    uint32_t scanLeft = 0;
    uint32_t scanRight = 0;
    if(includeScanMargins)
    {
        CHECKPOINTA("CopyPipelineResourceSetup: SetupScanMargins - includeScanMargins");
        scanTop = scanMargins.getTop().get(resolutionInt);
        scanBottom = scanMargins.getBottom().get(resolutionInt);
        scanLeft = scanMargins.getLeft().get(resolutionInt);
        scanRight = scanMargins.getRight().get(resolutionInt);
        CHECKPOINTA("CopyPipelineResourceSetup: SetupScanMargins - ScanMargins: Top - %d, Bottom - %d, Left - %d, Right - %d", scanTop, scanBottom, scanLeft, scanRight);
    }
    else
    {
        scanTop = 0;
        scanBottom = 0;
        scanLeft = 0;
        scanRight = 0;
    }

    auto top = std::max(printTop, scanTop);
    auto bottom = std::max(printBottom, scanBottom);
    auto left = std::max(printLeft, scanLeft);
    auto right = std::max(printRight, scanRight);
    auto xExtent = sdintent->getXExtent();
    auto yExtent = sdintent->getYExtent();

    sdintent->setXOffset(left);
    sdintent->setYOffset(top);
    sdintent->setXExtent(xExtent - (left + right));
    sdintent->setYExtent(yExtent - (top + bottom));
    CHECKPOINTA("CopyPipelineResourceSetup: SetupScanMargins: XOffset: %d, YOffset: %d, XExtent: %d, YExtent: %d", 
                    sdintent->getXOffset(), sdintent->getYOffset(), sdintent->getXExtent(), sdintent->getYExtent());
}

void CopyPipelineResourceSetup::setCurrentStage(Stage currentStage)
{
    currentStage_ = currentStage;
    CHECKPOINTA("CopyPipelineResourceSetup::setCurrentStage - to %d", currentStage_);
}

void CopyPipelineResourceSetup::setCollateMode(CollateMode collateMode)
{
    collateMode_ = collateMode;
}

void CopyPipelineResourceSetup::setSegmentType(SegmentType segmentType)
{
    segmentType_ = segmentType;
}

// NOT USED CURRENTLY
// void CopyPipelineResourceSetup::setupImagePersisterPreviewIntent(std::shared_ptr<IImagePersisterIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig)
// {

//     CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterPreviewIntent - ENTRY");
//     DUNE_UNUSED(resourceConfig);
//     intent->setFileName("preview_");
//     intent->setFileFormat(dune::imaging::types::FileFormat::JPEG);
//     intent->setNotificationStrategy(dune::imaging::types::NotificationStrategy::ON_STARTED);
//     intent->setStripHeight(64);  // Height by default, could be optimized, check if 256 as IsfPersister
//     intent->setSavePreviewMode(true);


//     CHECKPOINTA("CopyPipelineResourceSetup::setupImagePersisterPreviewIntent - EXIT");
// }


//Checks if the inverts color operation is suppoerted by imaging
bool CopyPipelineResourceSetup::isInvertColorsSupportedOnScanDevice()
{
    bool isSupported = false;
    auto scanCapabilities = ticket_->getScanCapabilitiesInterface();

    if(scanCapabilities != nullptr)
    {
        auto response = scanCapabilities->isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::InvertColors, isSupported);
        CHECKPOINTA("CopyPipelineResourceSetup::isInvertColorsSupportedOnScanDevice - isImagingOperationSupported response is %d, - isSupported? %d",
        static_cast<int>(response), static_cast<int>(isSupported));
        isSupported = (response == APIResult::OK) && isSupported;
    }
    else
    {
        CHECKPOINTA("CopyPipelineResourceSetup::isInvertColorsSupportedOnScanDevice - Scan scanCapabilities unavailable!");
    }

    return isSupported;
}

// Check if auto crop is supported
bool CopyPipelineResourceSetup::isAutoCropSupportedOnScanDevice()
{
    bool isSupported = false;
    auto scanCapabilities = ticket_->getScanCapabilitiesInterface();

    if(scanCapabilities != nullptr)
    {
        auto response = scanCapabilities->isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoCrop, isSupported);
        CHECKPOINTA("CopyPipelineResourceSetup::isAutoCropSupportedOnScanDevice - isImagingOperationSupported response is %d, - isSupported? %d",
        static_cast<int>(response), static_cast<int>(isSupported));
        isSupported = (response == APIResult::OK) && isSupported;
    }
    else
    {
        CHECKPOINTA("CopyPipelineResourceSetup::isAutoCropSupportedOnScanDevice - Scan scanCapabilities unavailable!");
    }

    return isSupported;
}

// Check if scale is supported
bool CopyPipelineResourceSetup::isScaleSupportedOnScanDevice()
{
    bool isSupported = false;
    auto scanCapabilities = ticket_->getScanCapabilitiesInterface();

    if(scanCapabilities != nullptr)
    {
        auto response = scanCapabilities->isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::Scale, isSupported);
        CHECKPOINTA("CopyPipelineResourceSetup::isScaleSupportedOnScanDevice - isImagingOperationSupported response is %d, - isSupported? %d",
        static_cast<int>(response), static_cast<int>(isSupported));
        isSupported = (response == APIResult::OK) && isSupported;
    }
    else
    {
        CHECKPOINTA("CopyPipelineResourceSetup::isScaleSupportedOnScanDevice - Scan scanCapabilities unavailable!");
    }

    return isSupported;
}

// Check if auto deskew is supported
bool CopyPipelineResourceSetup::isAutoDeskewSupportedOnScanDevice()
{
    bool isSupported = false;
    auto scanCapabilities = ticket_->getScanCapabilitiesInterface();

    if(scanCapabilities != nullptr)
    {
        auto response = scanCapabilities->isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::AutoDeskew, isSupported);
        CHECKPOINTA("CopyPipelineResourceSetup::isAutoDeskewSupportedOnScanDevice - isImagingOperationSupported response is %d, - isSupported? %d",
        static_cast<int>(response), static_cast<int>(isSupported));
        isSupported = (response == APIResult::OK) && isSupported;
    }
    else
    {
        CHECKPOINTA("CopyPipelineResourceSetup::isAutoDeskewSupportedOnScanDevice - Scan scanCapabilities unavailable!");
    }

    return isSupported;
}

// Check if background color removal is supported on ScanDevice
bool CopyPipelineResourceSetup::isBackgroundColorRemovalSupportedOnScanDevice()
{
    bool isSupported = false;
    auto scanCapabilities = ticket_->getScanCapabilitiesInterface();

    if(scanCapabilities != nullptr)
    {
        auto response = scanCapabilities->isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundColorRemoval, isSupported);
        CHECKPOINTA("CopyPipelineResourceSetup::isBackgroundColorRemovalSupportedOnScanDevice - isImagingOperationSupported response is %d, - isSupported? %d",
        static_cast<int>(response), static_cast<int>(isSupported));
        isSupported = (response == APIResult::OK) && isSupported;
    }
    else
    {
        CHECKPOINTA("CopyPipelineResourceSetup::isBackgroundColorRemovalSupportedOnScanDevice - Scan scanCapabilities unavailable!");
    }

    return isSupported;
}

// Check if background noise removal is supported on ScanDevice
bool CopyPipelineResourceSetup::isBackgroundNoiseRemovalSupportedOnScanDevice()
{
    bool isSupported = false;
    auto scanCapabilities = ticket_->getScanCapabilitiesInterface();

    if(scanCapabilities != nullptr)
    {
        auto response = scanCapabilities->isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundNoiseRemoval, isSupported);
        CHECKPOINTA("CopyPipelineResourceSetup::isBackgroundNoiseRemovalSupportedOnScanDevice - isImagingOperationSupported response is %d, - isSupported? %d",
        static_cast<int>(response), static_cast<int>(isSupported));
        isSupported = (response == APIResult::OK) && isSupported;
    }
    else
    {
        CHECKPOINTA("CopyPipelineResourceSetup::isBackgroundNoiseRemovalSupportedOnScanDevice - Scan scanCapabilities unavailable!");
    }

    return isSupported;
}

// Check if background cleanup is supported on ScanDevice
bool CopyPipelineResourceSetup::isBackgroundCleanupSupportedOnScanDevice()
{
    bool isSupported = false;
    auto scanCapabilities = ticket_->getScanCapabilitiesInterface();

    if(scanCapabilities != nullptr)
    {
        auto response = scanCapabilities->isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BackgroundCleanup, isSupported);
        CHECKPOINTA("CopyPipelineResourceSetup::isBackgroundCleanupSupportedOnScanDevice - isImagingOperationSupported response is %d, - isSupported? %d",
        static_cast<int>(response), static_cast<int>(isSupported));
        isSupported = (response == APIResult::OK) && isSupported;
    }
    else
    {
        CHECKPOINTA("CopyPipelineResourceSetup::isBackgroundCleanupSupportedOnScanDevice - Scan scanCapabilities unavailable!");
    }

    return isSupported;
}

// Checks if the input media is mixed size
bool CopyPipelineResourceSetup::isMixedSizeOriginals()
{
    bool isMSO = false;
    MediaSizeId mediaSize = copyIntent_->getInputMediaSizeId();

    if ((mediaSize == MediaSizeId::MIXED_LETTER_LEGAL)  ||
        (mediaSize == MediaSizeId::MIXED_LETTER_LEDGER) ||
        (mediaSize == MediaSizeId::MIXED_A4_A3))
    {
        isMSO = true;
    }

    return isMSO;
}

// Check if blank page detection supported from scan device.
bool CopyPipelineResourceSetup::isBlankPageDetectionSupported()
{
    bool isSupported = false;
    auto scanCapabilities = ticket_->getScanCapabilitiesInterface();

    if(scanCapabilities != nullptr)
    {
        auto response = scanCapabilities->isImagingOperationSupported(dune::scan::scanningsystem::ImagingOperation::BlankPageDetection, isSupported);
        CHECKPOINTA("CopyPipelineResourceSetup::isBlankPageDetectionSupported - isImagingOperationSupported response is %d, - isSupported? %d",
        static_cast<int>(response), static_cast<int>(isSupported));
        isSupported = (response == APIResult::OK) && isSupported;
    }
    else
    {
        CHECKPOINTA("CopyPipelineResourceSetup::isBlankPageDetectionSupported - Scan scanCapabilities unavailable!");
    }

    return isSupported;
}

std::shared_ptr<dune::imaging::Resources::SequencingParams> CopyPipelineResourceSetup::getSequencingParams()
{
    // Don't change sequencingParams for Selene
    if ((copyIntent_->getCollate() == SheetCollate::Uncollate) && !hasSharedPaperPath_ &&
        (prePrintConfiguration_ == Product::HOME_PRO) && !copyBasicPipeline_)
    {
        CHECKPOINTC(
            "CopyPipelineResourceSetup::getSequencingParams - Selene case: it does not change sequencingParams");
        return nullptr;
    }

    // Set sequencing params
    std::shared_ptr<dune::imaging::Resources::SequencingParams> sequencingParams{
        std::make_shared<dune::imaging::Resources::SequencingParams>()};

    // For Enterprise, Collation feature will be supported by PrintDevice
    sequencingParams->collationCopies = copyEnterprisePipeline_ ? 1 : copyIntent_->getCopies();
    sequencingParams->uncollationCopies = 1;
    dune::imaging::types::BookletFormat bookletFormat = copyIntent_->getBookletFormat();
    if(bookletFormat == dune::imaging::types::BookletFormat::Off){
        sequencingParams->booklet = false;
    }else{
        sequencingParams->booklet = true;
    }

    // For Beam
    if (hasSharedPaperPath_)
    {
        sequencingParams->collationCopies = 1;
        sequencingParams->uncollationCopies = copyIntent_->getCopies();
    }

    // Checking for a collation job after everything else is setup because collate could be an additional ask on
    // previous setup For Basic pipeline, ImageRetriver will handle collation and uncollation
    if (copyBasicPipeline_ == true)
    {
        bool simpleJob = copyIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::OneUp &&
                         copyIntent_->getOutputPlexMode() != dune::imaging::types::Plex::DUPLEX &&
                         copyIntent_->getInputPlexMode() != dune::imaging::types::Plex::DUPLEX &&
                         copyIntent_->getScanCaptureMode() != dune::scan::types::ScanCaptureModeType::IDCARD;

        if (collateMode_ == CollateMode::NONE && copyIntent_->getScanSource() != dune::scan::types::ScanSource::GLASS)
        {
            sequencingParams->collationCopies = 1;
            sequencingParams->uncollationCopies = copyIntent_->getCopies();
            CHECKPOINTA("CopyPipelineResourceSetup::getSequencingParams - Basic pipeline: Set uncollated copies.");
        }
        else if (collateMode_ == CollateMode::NONE &&
                 copyIntent_->getScanSource() == dune::scan::types::ScanSource::GLASS && simpleJob)
        {
            sequencingParams->collationCopies = 1;
            sequencingParams->uncollationCopies = copyIntent_->getCopies();
            CHECKPOINTA(
                "CopyPipelineResourceSetup::getSequencingParams - Basic Glass pipeline: Set uncollated copies.");
        }
        else
        {
            sequencingParams->collationCopies = copyIntent_->getCopies();
            sequencingParams->uncollationCopies = 1;
            // We want to set the pagesToSequence only with collateMode
            if (pageCountBeforeSequencing_)
            {
                sequencingParams->pagesNeededToSequence = pageCountBeforeSequencing_;
            }
        }
    }
    else if (collateMode_ == CollateMode::COMPRESSED || prePrintConfiguration_ == Product::LFP)
    {
        if (collateMode_ == CollateMode::NONE)
        {
            sequencingParams->collationCopies = 1;
            sequencingParams->uncollationCopies = copyIntent_->getCopies();
        }
        else
        {
            // We want to set the pagesToSequence only with collateMode
            if (pageCountBeforeSequencing_)
            {
                sequencingParams->pagesNeededToSequence = pageCountBeforeSequencing_;
            }
        }
    }

    CHECKPOINTA("CopyPipelineResourceSetup::getSequencingParams collation Copies: %d",
                sequencingParams->collationCopies);
    CHECKPOINTA("CopyPipelineResourceSetup::getSequencingParams uncollation Copies: %d",
                sequencingParams->uncollationCopies);
    CHECKPOINTA("CopyPipelineResourceSetup::getSequencingParams pagesToSequence: %d",
                sequencingParams->pagesNeededToSequence);
    return sequencingParams;
}

uint32_t CopyPipelineResourceSetup::getRotationAngle()
{
    uint32_t rotationAngle{0};

    // Set rotation angle 1 if it's 2up job
    if (copyIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::TwoUp &&
        copyEnterprisePipeline_ == false)
    {
        CHECKPOINTB("CopyPipelineResourceSetup: getRotationAngle: Rotation for 2Up (not enterprise)");
        rotationAngle = 1;
    }

    // Checking for a collation job after everything else is setup because collate could be an additional ask on
    // previous setup For Basic pipeline, ImageRetriver will handle collation and uncollation
    if (copyBasicPipeline_ == true)
    {
        // For glass 2up job, Image Retriever need to do the rotation
        // In other cases rotation will be done by image processor
        if ((copyIntent_->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp) &&
            (copyIntent_->getScanSource() == dune::scan::scanningsystem::ScanSource::GLASS))
        {
            CHECKPOINTB("CopyPipelineResourceSetup: getRotationAngle: Rotation for Glass2Up");
            rotationAngle = 1;
        }
        else
        {
            CHECKPOINTB("CopyPipelineResourceSetup: getRotationAngle: Disabled rotation");
            rotationAngle = 0;
        }
    }

    // Disable rotation for IDCARD
    if (copyIntent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD)
    {
        CHECKPOINTB("CopyPipelineResourceSetup: getRotationAngle: Disabled rotation for IdCard");
        rotationAngle = 0;
    }

    // Disable rotation for simulator
    if (simJob_ && prePrintConfiguration_ != Product::LFP)
    {
        CHECKPOINTB("CopyPipelineResourceSetup: getRotationAngle: Disabled rotation for simulator");
        rotationAngle = 0;
    }
    CHECKPOINTA("CopyPipelineResourceSetup::getRotationAngle - Rotation Angle: %u", rotationAngle);
    return rotationAngle;
}


NUpParams CopyPipelineResourceSetup::getNUpParameters()
{
    // Get NumberUp
    dune::imaging::types::NumberUp numberUp = dune::imaging::types::NumberUp::ONE_UP;
    if (copyIntent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD)
    {
        numberUp = dune::imaging::types::NumberUp::ID_CARD;
    }
    else if (copyIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::TwoUp)
    {
        numberUp = dune::imaging::types::NumberUp::TWO_UP;
    }
    else if (copyIntent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::FourUp)
    {
        numberUp = dune::imaging::types::NumberUp::FOUR_UP;
    }
    else 
    {
        CHECKPOINTA("CopyPipelineResourceSetup::Unsupported PagesPerSheet");
    }

    dune::imaging::types::NumberUpPageOrder numberUpOrder = dune::imaging::types::NumberUpPageOrder::RIGHT_THEN_DOWN;
    if (numberUp == dune::imaging::types::NumberUp::FOUR_UP)
    {
        if (copyIntent_->getContentOrientation() == dune::imaging::types::ContentOrientation::LANDSCAPE)
        {
            switch (copyIntent_->getNumberUpPresentationDirection())
            {
                case dune::imaging::types::NumberUpPresentationDirection::ToBottomToLeft:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::LEFT_THEN_UP;
                    break;
                case dune::imaging::types::NumberUpPresentationDirection::ToBottomToRight:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::LEFT_THEN_DOWN;
                    break;
                case dune::imaging::types::NumberUpPresentationDirection::ToLeftToBottom:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::UP_THEN_LEFT;
                    break;
                case dune::imaging::types::NumberUpPresentationDirection::ToLeftToTop:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::UP_THEN_RIGHT;
                    break;
                case dune::imaging::types::NumberUpPresentationDirection::ToRightToBottom:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::DOWN_THEN_LEFT;
                    break;
                case dune::imaging::types::NumberUpPresentationDirection::ToRightToTop:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::DOWN_THEN_RIGHT;
                    break;
                case dune::imaging::types::NumberUpPresentationDirection::ToTopToLeft:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::RIGHT_THEN_UP;
                    break;
                case dune::imaging::types::NumberUpPresentationDirection::ToTopToRight:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::RIGHT_THEN_DOWN;
                    break;
                default:
                    CHECKPOINTA("CopyPipelineResourceSetup::Unsupported NumberUpPresentationDirection");
                    break;
            }
        }
        else
        {
            switch (copyIntent_->getNumberUpPresentationDirection())
            {
                case dune::imaging::types::NumberUpPresentationDirection::ToBottomToLeft:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::DOWN_THEN_LEFT;
                    break;
                case dune::imaging::types::NumberUpPresentationDirection::ToBottomToRight:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::DOWN_THEN_RIGHT;
                    break;
                case dune::imaging::types::NumberUpPresentationDirection::ToLeftToBottom:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::LEFT_THEN_DOWN;
                    break;
                case dune::imaging::types::NumberUpPresentationDirection::ToLeftToTop:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::LEFT_THEN_UP;
                    break;
                case dune::imaging::types::NumberUpPresentationDirection::ToRightToBottom:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::RIGHT_THEN_DOWN;
                    break;
                case dune::imaging::types::NumberUpPresentationDirection::ToRightToTop:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::RIGHT_THEN_UP;
                    break;
                case dune::imaging::types::NumberUpPresentationDirection::ToTopToLeft:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::UP_THEN_LEFT;
                    break;
                case dune::imaging::types::NumberUpPresentationDirection::ToTopToRight:
                    numberUpOrder = dune::imaging::types::NumberUpPageOrder::UP_THEN_RIGHT;
                    break;
                default:
                    CHECKPOINTA("CopyPipelineResourceSetup::Unsupported NumberUpPresentationDirection");
                    break;
            }
        }
    }

    return NUpParams{numberUp, numberUpOrder};
}

uint32_t CopyPipelineResourceSetup::getImagesPerSheet()
{
    dune::imaging::types::CopyOutputNumberUpCount pagesPerSheet = copyIntent_->getPagesPerSheet();
    if (copyIntent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD)
    {
        pagesPerSheet = dune::imaging::types::CopyOutputNumberUpCount::TwoUp;
    }

    uint32_t imagesPerSheet = 1;
    switch (pagesPerSheet)
    {
        case dune::imaging::types::CopyOutputNumberUpCount::OneUp:
            imagesPerSheet = 1;
            break;
        case dune::imaging::types::CopyOutputNumberUpCount::TwoUp:
            imagesPerSheet = 2;
            break;
        case dune::imaging::types::CopyOutputNumberUpCount::FourUp:
            imagesPerSheet = 4;
            break;
        case dune::imaging::types::CopyOutputNumberUpCount::EightUp:
            imagesPerSheet = 8;
            break;
        default:
            CHECKPOINTA("CopyPipelineResourceSetup::Not supported PagesPerSheet");
            break;
    }

    if (copyIntent_->getOutputPlexMode() == dune::imaging::types::Plex::DUPLEX
        && copyEnterprisePipeline_ == false)
    {
        imagesPerSheet = imagesPerSheet * 2;
    }

    return imagesPerSheet;
}

WatermarkParams CopyPipelineResourceSetup::getWatermarkParameters()
{
    dune::imaging::types::WatermarkSettingsT watermarkSettingsTable = copyIntent_->getWatermarkSettings();
    WatermarkParams watermarkParams;
    watermarkParams.text = "";
    if(watermarkSettingsTable.type == dune::imaging::types::WatermarkType::TEXT_WATERMARK){
        watermarkParams.text = watermarkSettingsTable.customText;
    }
    
    
    watermarkParams.typeface = watermarkSettingsTable.textFont;
    
    watermarkParams.fontColor = watermarkSettingsTable.textColor;
    watermarkParams.firstPageOnly = watermarkSettingsTable.onlyFirstPage;
    watermarkParams.fontSize = 300;
    switch(watermarkSettingsTable.textSize)
    {
    case dune::imaging::types::StampWatermarkTextSize::EIGHT_POINT:
        watermarkParams.fontSize = 80;
        break;
    case dune::imaging::types::StampWatermarkTextSize::TWELVE_POINT:
        watermarkParams.fontSize = 120;
        break;
    case dune::imaging::types::StampWatermarkTextSize::TWENTY_POINT:
        watermarkParams.fontSize = 200;
        break;
    case dune::imaging::types::StampWatermarkTextSize::THIRTY_POINT:
        watermarkParams.fontSize = 300;
        break;
    case dune::imaging::types::StampWatermarkTextSize::FORTY_POINT:
        watermarkParams.fontSize = 400;
        break;
    case dune::imaging::types::StampWatermarkTextSize::SIXTY_POINT:
        watermarkParams.fontSize = 500;
        break;
    default:
        CHECKPOINTA("CopyPipelineResourceSetup::getWatermarkParameters Unsupported watermark text size");
        break;
    }
    watermarkParams.isSecure = watermarkSettingsTable.type == dune::imaging::types::WatermarkType::SECURE_WATERMARK;
    watermarkParams.pattern = watermarkSettingsTable.backgroundPattern;

    watermarkParams.rotation = watermarkSettingsTable.rotate45 ? 315 : 0;
    watermarkParams.darkness = 51 * watermarkSettingsTable.darkness;

    return watermarkParams;
}


std::unique_ptr<StampParams> CopyPipelineResourceSetup::getStampParametersLocation(const dune::imaging::types::StampLocation& location)
{
    dune::imaging::types::ScanStampLocationFbT stampLocation;
    auto outStamp = std::make_unique<StampParams>();

    switch(location){
        case dune::imaging::types::StampLocation::TOP_LEFT:
            stampLocation = copyIntent_->getStampTopLeft();
            outStamp->position = dune::imaging::types::PagePosition::UPPER_LEFT;
            break;
        case dune::imaging::types::StampLocation::TOP_CENTER: 
            stampLocation = copyIntent_->getStampTopCenter();
            outStamp->position = dune::imaging::types::PagePosition::UPPER_CENTER;
            break;
        case dune::imaging::types::StampLocation::TOP_RIGHT:
            stampLocation = copyIntent_->getStampTopRight();
            outStamp->position = dune::imaging::types::PagePosition::UPPER_RIGHT;
            break;
        case dune::imaging::types::StampLocation::BOTTOM_LEFT:
            stampLocation = copyIntent_->getStampBottomLeft();
            outStamp->position = dune::imaging::types::PagePosition::LOWER_LEFT;
            break;
        case dune::imaging::types::StampLocation::BOTTOM_CENTER:
            stampLocation = copyIntent_->getStampBottomCenter();
            outStamp->position = dune::imaging::types::PagePosition::LOWER_CENTER;
            break;
        case dune::imaging::types::StampLocation::BOTTOM_RIGHT:
            stampLocation = copyIntent_->getStampBottomRight();
            outStamp->position = dune::imaging::types::PagePosition::LOWER_RIGHT;
            break;
        default:
            CHECKPOINTA("dune::scan::Jobs::Scan::getStampParametersLocation -- Invalid stamp location");
            return nullptr;
    }
    

    auto size = stampLocation.stampContents.size();
    if(size > 0){
        for(auto &content : stampLocation.stampContents){
            content->customText = getStampText(*content);
            outStamp->stampContents.emplace_back(*content);
        }
    }else{
        CHECKPOINTA("dune::scan::Jobs::Scan::getStampParametersLocation -- No stamp content");
        return nullptr;
    }

    outStamp->typeface = stampLocation.stampTextFont;
    outStamp->fontColor = stampLocation.stampTextColor;

    switch(stampLocation.stampTextSize)
    {
    case dune::imaging::types::StampWatermarkTextSize::EIGHT_POINT:
        outStamp->fontSize = 80;
        break;
    case dune::imaging::types::StampWatermarkTextSize::TWELVE_POINT:
        outStamp->fontSize = 120;
        break;
    case dune::imaging::types::StampWatermarkTextSize::TWENTY_POINT:
        outStamp->fontSize = 200;
        break;
    case dune::imaging::types::StampWatermarkTextSize::THIRTY_POINT:
        outStamp->fontSize = 300;
        break;
    case dune::imaging::types::StampWatermarkTextSize::FORTY_POINT:
        outStamp->fontSize = 400;
        break;
    case dune::imaging::types::StampWatermarkTextSize::SIXTY_POINT:
        outStamp->fontSize = 500;
        break;
    default:
        CHECKPOINTA("CopyPipelineResourceSetup::getWatermarkParameters Unsupported watermark text size");
        return nullptr;
    }
    
    outStamp->whiteBackground = stampLocation.stampWhiteBackground;
    outStamp->startingPage = stampLocation.stampStartingPage;
    outStamp->startingNumber = stampLocation.stampStartingNumber;
    outStamp->numberOfDigits = stampLocation.stampNumberOfDigits;
    outStamp->pageNumberingStyle = stampLocation.stampPageNumberingStyle;
    
    return outStamp;
}

std::string CopyPipelineResourceSetup::getlocaleDateAndTime(StampType stampType){

    dune::localization::ILocaleProvider* localeProvider = ticket_->getLocalizationInterface();
    dune::localization::LocaleId localeId = localeProvider->deviceLocaleId();    
    std::shared_ptr<dune::localization::ILocale> locale = localeProvider->getLocale(localeId);

    dune::localization::DateFormat dateFormat = localeProvider->getDateFormat();
    dune::localization::TimeFormat timeFormat = localeProvider->getTimeFormat();

    std::string currentDateTimeFormatted = "";
    time_t stime = dateTime_->getSystemTime();
    tm sTmTime = *localtime(&stime);

    //locale->getDateTimeShort(sTmTime, dateFormat, timeFormat);
    if(stampType == StampType::DATE){
        currentDateTimeFormatted = locale->getDate(sTmTime, dateFormat);
    }else{
        currentDateTimeFormatted = locale->getDateTime(sTmTime, dateFormat, timeFormat);
    } 

    CHECKPOINTA("CopyPipelineResourceSetup::stampText date: %s.", currentDateTimeFormatted.c_str()); 
    return currentDateTimeFormatted;
}

std::string CopyPipelineResourceSetup::getStampText(dune::imaging::types::StampContentT stampContent){

    std::string result;
    StampType stampType = stampContent.stampId;

    switch (stampType)
    {
        case StampType::USER_NAME:
            result = ticket_->getSecurityContext()->getUserIdentity().fullyQualifiedUserName;
            break;
        case StampType::IP_ADDRESS:
            {
                if(services_.networkManager == nullptr){
                    CHECKPOINTA("CopyPipelineResourceSetup stamp: networkManager == nullptr");
                    result = "0.0.0.0";
                }
                else{
                    auto ipv4Config = services_.networkManager->getNetworkIPv4ConfigInterface("eth0");
                    if (ipv4Config != nullptr)
                    {
                        dune::io::net::core::IPv4AddrInfo addrInfo;
                        char printableIpv4[50];
                        ipv4Config->getIPv4AddrInfo(addrInfo);
                        inet_ntop(AF_INET, &(addrInfo.address_), printableIpv4, sizeof(printableIpv4));
                        result = printableIpv4;
                    }else{
                        result = "0.0.0.0";
                    }
                }
            }
            break;
        case StampType::PRODUCT_INFORMATION:
            {
                if(services_.deviceInfo == nullptr){
                    CHECKPOINTA("CopyPipelineResourceSetup stamp: deviceInfo == nullptr");
                    result = "";
                }else{
                    result = services_.deviceInfo->getMakeAndModelInfo().name + ":" + services_.deviceInfo->getSerialNumber();
                }
                
            }
            break;
        case StampType::DATE_AND_TIME:
        case StampType::DATE:
            result = getlocaleDateAndTime(stampContent.stampId);
            break;
        default:
            result = stampContent.customText;
            break;
    }

    CHECKPOINTA("CopyPipelineResourceSetup::stampText: (%s)", result.c_str());
    return result;
}

void CopyPipelineResourceSetup::doPrintEarlyWarning(std::shared_ptr<IPageAssemblerIntent> intent, bool checkTray)
{
    bool ufcMode = false;

    if (services_.engineCapabilitiesFactory == nullptr || services_.engineCapabilitiesFactory->getCapabilities() == nullptr)
    {
        CHECKPOINTA("CopyPipelineResourceSetup::doPrintEarlyWarning - EngineCapabilitiesFactory is null, setting ufcMode to false");
        intent->setUltraFastCopyMode(false);
        return;
    }

    bool preRunSupported = false;
    std::shared_ptr<dune::print::engine::Capabilities> capabilities = services_.engineCapabilitiesFactory->getCapabilities();
    APIResult result = capabilities->getEngineAttributeValue(dune::print::engine::EngineAttributeFieldType::PRE_RUN_SUPPORTED, preRunSupported);

    auto outMediaSource = copyIntent_->getOutputMediaSource();
    if (result == APIResult::OK && preRunSupported &&
        (outMediaSource != dune::imaging::types::MediaSource::AUTOSELECT)
        && (outMediaSource != dune::imaging::types::MediaSource::UNDEFINED))
    {
        auto trayCurrentMediaSize = checkTray ? 
                SelectionHelper::getTrayCurrentMediaSize(outMediaSource, ticket_->getMediaInterface())
                : copyIntent_->getOutputMediaSizeId();
        auto trayCurrentMediaOrientation = checkTray ? 
                SelectionHelper::getTrayCurrentMediaOrientation(outMediaSource, ticket_->getMediaInterface())
                : copyIntent_->getOutputMediaOrientation();
        auto trayCurrentMediaType = checkTray ? 
                SelectionHelper::getTrayCurrentMediaType(outMediaSource, ticket_->getMediaInterface()) 
                : copyIntent_->getOutputMediaIdType();
        uint32_t earlyWarningLevel = 2;
        uint32_t printStartTime = 1;

        if (copyIntent_->getOutputMediaSizeId() == trayCurrentMediaSize
            && copyIntent_->getOutputMediaOrientation() == trayCurrentMediaOrientation
            && copyIntent_->getOutputMediaIdType() == trayCurrentMediaType
            && (copyIntent_->getStapleOption() == dune::imaging::types::StapleOptions::NONE)                        //StapleOption
            && (copyIntent_->getPunchOption() == dune::imaging::types::PunchingOptions::NONE)                       //HolePunchOption
            && (copyIntent_->getFoldOption() == dune::imaging::types::FoldingOptions::NONE))                        //HolePunchOption
        {
            if (intent->getBasicCopyMode()     // This means that No image processing, No disk buffering in filters.
                && (copyIntent_->getScanSource() == dune::scan::types::ScanSource::GLASS)                           //ScanSource
                && ((copyIntent_->getColorMode() == dune::imaging::types::ColorMode::COLOR)                         //ColorMode
                    || (copyIntent_->getColorMode() == dune::imaging::types::ColorMode::GRAYSCALE)
                    || (copyIntent_->getColorMode() == dune::imaging::types::ColorMode::MONOCHROME))
                && ((copyIntent_->getOutputMediaSizeId() == dune::imaging::types::MediaSizeId::LETTER)              //OutputMediaSizeId
                    || (copyIntent_->getOutputMediaSizeId() == dune::imaging::types::MediaSizeId::A4))
                && (copyIntent_->getOutputMediaOrientation() == dune::imaging::types::MediaOrientation::LANDSCAPE)  //OutputMediaOrientation
                && (copyIntent_->getInputMediaSizeId() == copyIntent_->getOutputMediaSizeId())                      //InputMediaSizeId
                && (copyIntent_->getScanFeedOrientation() == dune::scan::types::ScanFeedOrientation::LONGEDGE)      //ScanFeedOrientation
                && (copyIntent_->getOutputMediaIdType() == dune::imaging::types::MediaIdType::STATIONERY)           //OutputMediaIdType
                && (copyIntent_->getOutputMediaSource() == dune::imaging::types::MediaSource::TRAY2)                //OutputMediaSource
                && (copyIntent_->getInputPlexMode() == dune::imaging::types::Plex::SIMPLEX)                         //InputPlexMode
                && (copyIntent_->getOutputPlexMode() == dune::imaging::types::Plex::SIMPLEX)                        //OutputPlexMode
                && (copyIntent_->getCopies() == 1))                                                                 //Copies
            {
                // Check active job in JobQueue
                if (services_.jobQueue != nullptr)
                {
                    bool existingActiveJob = false;
                    std::list<std::shared_ptr<IJob>> jobs{};
                    services_.jobQueue->getJobs(jobs);
                    for (auto &job : jobs)
                    {
                        if(job->getStateType() != JobStateType::CREATED 
                            && job->getStateType() != JobStateType::READY
                            && job->getStateType() != JobStateType::COMPLETED
                            && job->getStateType() != JobStateType::SCHEDULED)
                        {
                            // If there is an active job in JobQueue, then Set ufcMode to false
                            existingActiveJob = true;
                            CHECKPOINTC("CopyPipelineResourceSetup::doPrintEarlyWarning - existing ActiveJob, StateType = %d", (uint32_t)job->getStateType());
                            break;
                        }
                    }

                    // If there is no active job in JobQueue, then Set ufcMode to true
                    if (existingActiveJob == false)
                    {
                        ufcMode = true;
                        printStartTime = 2;
                    }
                }
            }
        
            // Send early warning to PrintDeviceEngine
            {
                auto orientation = dune::imaging::types::MediaOrientation::PORTRAIT;
                if (copyIntent_->getScanFeedOrientation() == dune::scan::types::ScanFeedOrientation::LONGEDGE)
                {
                    orientation = dune::imaging::types::MediaOrientation::LANDSCAPE;
                    
                }
                dune::imaging::types::WidthAndHeight widthAndHeight = 
                    dune::imaging::types::convertMediaSizeIdToWidthAndHeight(copyIntent_->getOutputMediaSizeId(), orientation);
                uint32_t resolution = ConvertToScanTypeHelper::getResolutionIntFromEnum(copyIntent_->getOutputXResolution());

                auto scanMediaSource = dune::imaging::types::MediaSource::ADF;
                if (copyIntent_->getScanSource() == dune::scan::types::ScanSource::GLASS)
                {
                    scanMediaSource = dune::imaging::types::MediaSource::FLATBED;
                }

                auto earlyWarningIntents = services_.printIntentsFactory->createPrintIntentsEarlyIntents();
                earlyWarningIntents->setValue(dune::print::engine::PrintIntentFieldType::EARLY_INTENTS_EARLY_WARNING_LEVEL, earlyWarningLevel);
                earlyWarningIntents->setValue(dune::print::engine::PrintIntentFieldType::JOB_TYPE, dune::job::JobType::COPY);
                earlyWarningIntents->setValue(dune::print::engine::PrintIntentFieldType::COLOR_MODE, copyIntent_->getColorMode());
                earlyWarningIntents->setValue(dune::print::engine::PrintIntentFieldType::PAGE_WIDTH, widthAndHeight.width.get(resolution));
                earlyWarningIntents->setValue(dune::print::engine::PrintIntentFieldType::PAGE_HEIGHT, widthAndHeight.height.get(resolution));
                earlyWarningIntents->setValue(dune::print::engine::PrintIntentFieldType::PAGE_UNITS, resolution);
                earlyWarningIntents->setValue(dune::print::engine::PrintIntentFieldType::MEDIA_TYPE, copyIntent_->getOutputMediaIdType());
                earlyWarningIntents->setValue(dune::print::engine::PrintIntentFieldType::TRAY_TYPE, copyIntent_->getOutputMediaSource());            
                earlyWarningIntents->setValue(dune::print::engine::PrintIntentFieldType::EARLY_INTENTS_SCAN_SOURCE, scanMediaSource);
                earlyWarningIntents->setValue(dune::print::engine::PrintIntentFieldType::PLEX_MODE, copyIntent_->getOutputPlexMode());
                earlyWarningIntents->setValue(dune::print::engine::PrintIntentFieldType::EARLY_INTENTS_PRINT_START_TIME, printStartTime);

                CHECKPOINTA("CopyPipelineResourceSetup::doPrintEarlyWarning - Send early warning to PrintDeviceEngine");
                services_.printEngine->earlyWarning(earlyWarningIntents);
            }            
        }

        CHECKPOINTC("CopyPipelineResourceSetup: doPrintEarlyWarning: getBasicCopyMode: %d", (uint32_t)intent->getBasicCopyMode());
        CHECKPOINTC("CopyPipelineResourceSetup: doPrintEarlyWarning: getScanSource: %d", (uint32_t)copyIntent_->getScanSource());
        CHECKPOINTC("CopyPipelineResourceSetup: doPrintEarlyWarning: getColorMode: %d", (uint32_t)copyIntent_->getColorMode());
        CHECKPOINTC("CopyPipelineResourceSetup: doPrintEarlyWarning: getOutputMediaSizeId: %d", (uint32_t)copyIntent_->getOutputMediaSizeId());
        CHECKPOINTC("CopyPipelineResourceSetup: doPrintEarlyWarning: getOutputMediaOrientation: %d", (uint32_t)copyIntent_->getOutputMediaOrientation());
        CHECKPOINTC("CopyPipelineResourceSetup: doPrintEarlyWarning: getInputMediaSizeId: %d", (uint32_t)copyIntent_->getInputMediaSizeId());
        CHECKPOINTC("CopyPipelineResourceSetup: doPrintEarlyWarning: getScanFeedOrientation: %d", (uint32_t)copyIntent_->getScanFeedOrientation());
        CHECKPOINTC("CopyPipelineResourceSetup: doPrintEarlyWarning: getOutputMediaIdType: %d", (uint32_t)copyIntent_->getOutputMediaIdType());
        CHECKPOINTC("CopyPipelineResourceSetup: doPrintEarlyWarning: getOutputMediaSource: %d", (uint32_t)copyIntent_->getOutputMediaSource());
        CHECKPOINTC("CopyPipelineResourceSetup: doPrintEarlyWarning: getInputPlexMode: %d", (uint32_t)copyIntent_->getInputPlexMode());
        CHECKPOINTC("CopyPipelineResourceSetup: doPrintEarlyWarning: getOutputPlexMode: %d", (uint32_t)copyIntent_->getOutputPlexMode());
        CHECKPOINTC("CopyPipelineResourceSetup: doPrintEarlyWarning: getCopies: %d", (uint32_t)copyIntent_->getCopies());
    }

    intent->setUltraFastCopyMode(ufcMode);
    CHECKPOINTA("CopyPipelineResourceSetup::doPrintEarlyWarning - UFC Mode: %d", ufcMode);
}

}}}}  // namespace dune::copy::Jobs::Copy
