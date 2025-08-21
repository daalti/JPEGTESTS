#ifndef DUNE_COPY_PIPELINERESOURCESETUP_H
#define DUNE_COPY_PIPELINERESOURCESETUP_H
////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyPipelineResourceSetup.h
 * @brief  resource setup methods.h
 * @author Shubham Khandelwal
 * @date   2023-04-16
 *
 * (C) Copyright 2023 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include <memory>

#include "gtest/gtest_prod.h"

#include "ConvertToScanTypeHelper.h"
#include "CopyPipelineStandardConfig_generated.h"
#include "ICopyJobTicket.h"
#include "ICopyPipelineBuilderAdapter.h"
#include "IImagePersisterTicket.h"
#include "IImageProcessorTicket.h"
#include "IImageRetrieverTicket.h"
#include "IJobTicketHandler.h"
#include "ILayoutFilterTicket.h"
#include "ILayoutFilterIntent.h"
#include "IMarkingFilterTicket.h"
#include "IMediaAttributes.h"
#include "IPageAssemblerTicket.h"
#include "IPrintDeviceIntent.h"
#include "IRtpFilterTicket.h"
#include "IScanDeviceTicket.h"
#include "IIPADeviceTicket.h"
#include "IScanPipeline.h"
#include "ImageContainer.h"
#include "ScanPipelineConfig_generated.h"
#include "IDateTime.h"

//margin at one end
#define DEFAULT_MARGIN_AT_300DPI 50
#define DPI300              300

namespace dune { namespace imaging { namespace Resources {
class SequencingParams;
}}}  // namespace dune::imaging::Resources

namespace dune { namespace copy { namespace Jobs { namespace Copy {

using dune::imaging::Resources::IImagePersisterIntent;
using dune::imaging::Resources::IImageProcessorIntent;
using dune::imaging::Resources::IImageRetrieverIntent;
using dune::imaging::Resources::IMarkingFilterIntent;
using dune::imaging::Resources::IPageAssemblerIntent;
using dune::job::PromptResponseType;
using dune::job::PromptType;
using dune::job::SegmentType;
using dune::print::Resources::IPrintDeviceIntent;
using dune::print::Resources::IRtpFilterIntent;
using dune::scan::Resources::IScanDeviceIntent;
using dune::scan::Resources::IScanDeviceTicket;
using dune::scan::Resources::IIPADeviceTicket;
using dune::scan::Resources::IIPADeviceIntents;
using dune::scan::types::ScanSource;
using ConvertToScanTypeHelper = dune::scan::types::ConvertToScanTypeHelper;
using MarginsParameters = dune::print::engine::IMedia::MarginsParameters;
using Margins = dune::imaging::types::Margins;
using NUpParams = dune::imaging::types::NUpParams;
using WatermarkParams = dune::imaging::types::WatermarkParams;
using IDateTime = dune::framework::core::time::IDateTime;
using StampType = dune::imaging::types::StampType;

class ICopyJobTicket;
using dune::scan::Jobs::Scan::IScanPipeline;

// Copy pipeline Stages
enum Stage
{
    Setup                    = 0,
    PreScan,
    Scan_PageAssembler_Print, 
    ScanFirstPage,            
    ScanSecondPage,          
    Scan_Basic_Print,
    PrintAllPages,            
    ScanPage,
    PrintPage,
    DirectCopy,
    Reprint,
    Retry,
    StopPreview,
    Preview,
    Finished             
};

// copy pipeline collate mode
enum CollateMode
{
  NONE = 0,
  COMPRESSED,
  UNCOMPRESSED
}; 

class CopyPipelineResourceSetup
{
  public:

    CopyPipelineResourceSetup(std::shared_ptr<ICopyJobTicket> ticket,
                        const ServicesPackage& services,
                        bool hasSharedPaperPath,
                        dune::scan::Jobs::Scan::IScanPipeline* scanPipeline,
                        Product prePrintConfiguration,
                        bool copyBasicPipeline,
                        const MaxLengthConfig& maxLengthConfig,
                        IDateTime* dateTime);

    /**
    * @brief setup the scan device intent from copy job ticket intent and resource config
    * @param intent scan device intent
    * @param resourceConfig resource configuration
    */
    void setupScanDeviceIntent(std::shared_ptr<IScanDeviceIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig);

    /**
    * @brief setup the ipa device intent from copy job ticket intent and resource config
    * @param intent i[a] device intent
    * @param resourceConfig resource configuration
    */
    void setupIPADeviceIntent(std::shared_ptr<IIPADeviceIntents> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig);


    /**
    * @brief setup the image processor intent from copy job ticket intent and resource config
    * @param intent image processor intent
    * @param resourceConfig resource configuration
    */
    void setupImageProcessorIntent(std::shared_ptr<IImageProcessorIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig);

    /**
    * @brief setup the marking filter intent from copy job ticket intent and resource config
    * @param intent marking filter intent
    * @param resourceConfig resource configuration
    */
    void setupMarkingFilterIntent(std::shared_ptr<IMarkingFilterIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig);

    /**
     * @brief setup the layout filter intent from copy job ticket intent and resource config
     * @param intent layout filter intent
     * @param resourceConfig resource configuration
     */
    void setupLayoutFilterIntent(std::shared_ptr<dune::imaging::Resources::ILayoutFilterIntent> intent,
                                 std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>       resourceConfig);

    /**
    * @brief setup the page assembler intent from copy job ticket intent and resource config
    * @param intent page assembler intent
    * @param resourceConfig resource configuration
    */
    void setupPageAssemblerIntent(std::shared_ptr<IPageAssemblerIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig);
    
    /**
    * @brief setup the image persister intent from copy job ticket intent and resource config
    * @param intent image persister intent
    * @param resourceConfig resource configuration
    */
    void setupImagePersisterIntent(std::shared_ptr<IImagePersisterIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig);
    
    /**
    * @brief setup the image retriever intent from copy job ticket intent and resource config
    * @param intent image retriever intent
    * @param resourceConfig resource configuration
    */
    void setupImageRetrieverIntent(std::shared_ptr<IImageRetrieverIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig);
    
    /**
    * @brief setup the buffer image persister intent from copy job ticket intent and resource config
    * @param intent buffer image persister intent
    * @param resourceConfig resource configuration
    */
    void setupBufferingImagePersisterIntent(std::shared_ptr<IImagePersisterIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig);
    
    /**
    * @brief setup the buffer image retriever intent from copy job ticket intent and resource config
    * @param intent image retriever intent
    * @param resourceConfig resource configuration
    */
    void setupBufferingImageRetrieverIntent(std::shared_ptr<IImageRetrieverIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig);

    // /**
    // * @brief setup the image persister preview intent from copy job ticket intent and resource config
    // * @param intent image persister intent
    // * @param resourceConfig resource configuration
    // */
    // void setupImagePersisterPreviewIntent(std::shared_ptr<IImagePersisterIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig);

    /**
    * @brief setup the image processor preview intent from copy job ticket intent and resource config
    * @param intent image processor intent
    * @param resourceConfig resource configuration
    */
    void setupImageProcessorPreviewIntent(std::shared_ptr<IImageProcessorIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig);

    /**
    * @brief setup the rtp filter intent from copy job ticket intent and resource config
    * @param intent rtp filter intent
    * @param resourceConfig resource configuration
    */
    void setupRtpFilterTicketIntent(std::shared_ptr<IRtpFilterIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig);

    /**
    * @brief setup the print device intent from copy job ticket intent and resource config
    * @param intent print device intent
    * @param resourceConfig resource configuration
    */
    void setupPrintDeviceIntent(std::shared_ptr<IPrintDeviceIntent> intent, std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> resourceConfig);

    /**
    * @brief setup the current stage of pipeline
    * @param currentStage current stage of pipeline
    */
    void setCurrentStage(Stage currentStage);

    /**
    * @brief setup the collate mode of pipeline
    * @param collateMode compression type
    */
    void setCollateMode(CollateMode collateMode);

    /**
    * @brief set the current segment of pipeline
    * @param segment type
    */
    void setSegmentType(SegmentType segmentType);

    /**
    * @brief set the thresold override value
    * @param segment type
    */
    void setThresholdOverride(const int threshold) { thresholdOverride_ = threshold; };

    /**
    * @brief set the top specific padding override value
    * @param topSpecificPadding the specific padding to apply
    */

    void setTopSpecificPadding(float topSpecificPadding) { topSpecificPadding_ = topSpecificPadding; };

    /**
    * @brief set the top specific padding override value
    * @param bottomSpecificPadding the specific padding to apply
    */

    void setBottomSpecificPadding(float bottomSpecificPadding) { bottomSpecificPadding_ = bottomSpecificPadding; };

    /**
    * @brief set the top specific padding override value
    * @param leftSpecificPadding the specific padding to apply
    */

    void setLeftSpecificPadding(float leftSpecificPadding) { leftSpecificPadding_ = leftSpecificPadding; };

    /**
    * @brief set the top specific padding override value
    * @param rightSpecificPadding the specific padding to apply
    */

    void setRightSpecificPadding(float rightSpecificPadding) { rightSpecificPadding_ = rightSpecificPadding; };

    /**
    * @brief set the number of pages to wait before sequencing config value
    * @param pageCountBeforeSequencing the specific count to apply
    */
    void setPageCountBeforeSequencing(uint32_t pageCountBeforeSequencing) { pageCountBeforeSequencing_ = pageCountBeforeSequencing; };

    /**
    * @brief set the max pages to collate config value
    * @param maxPagesToCollate the specific max pages to collate to apply
    */
    
    void setMaxPagesToCollate(uint32_t maxPagesToCollate) { maxPagesToCollate_ = maxPagesToCollate; };

    /**
     * @brief set the duplex side information for flatbed 
     * @param flatbedDuplexBackSide duplex backside true/false
     * 
     */
    void setFlatbedDuplexScanBackSide(bool flatbedDuplexBackSide) { flatbedDuplexBackSide_ = flatbedDuplexBackSide; };

    /**
    * @brief get the duplex side information for flatbed
    * @return duplex backside true/false
    */
    bool getFlatbedDuplexScanBackSide() { return flatbedDuplexBackSide_; };

  private:
    dune::scan::Jobs::Scan::IScanPipeline*                        scanPipeline_ {nullptr};
    const ServicesPackage&                                        services_;
    const MaxLengthConfig&                                        maxLengthConfig_;
    std::shared_ptr<ICopyJobIntent>                               copyIntent_;
    std::shared_ptr<ICopyJobTicket>                               ticket_;
    std::shared_ptr<dune::scan::Jobs::Scan::ScanPipelineConfigT>  scanPipelineConfig_{nullptr};
    
    bool                                                          hasSharedPaperPath_{false};
    bool                                                          copyBasicPipeline_{false};
    bool                                                          copyEnterprisePipeline_{false};
    bool                                                          simJob_{true};
    int                                                           thresholdOverride_{0};
    Product                                                       prePrintConfiguration_{Product::HOME_PRO}; ///< Print configuration value for copy pipeline
    CollateMode                                                   collateMode_{CollateMode::NONE};
    SegmentType                                                   segmentType_{SegmentType::FinalSegment};
    Stage                                                         currentStage_ = Stage::Setup;
    uint32_t                                                      topMargin_{0};
    uint32_t                                                      bottomMargin_{0};
    uint32_t                                                      leftMargin_{0};
    uint32_t                                                      rightMargin_{0};
    float                                                         topSpecificPadding_{0.0};
    float                                                         bottomSpecificPadding_{0.0};
    float                                                         leftSpecificPadding_{0.0};
    float                                                         rightSpecificPadding_{0.0};
    uint32_t                                                      pageCountBeforeSequencing_{0};
    uint32_t                                                      maxPagesToCollate_{0};
    IDateTime*                                                    dateTime_{nullptr};
    bool                                                          flatbedDuplexBackSide_{false};

    /**
     * @brief setup scan region Xextent yextent, and offsets
     * @param sdIntent scan device intent
     * @param mediaSize scan device media size id
     * @param orientation scan device orientation
     * @param resolution  scan device resolution
     * @param mode scan device mode
     */
    void setupScanRegion(std::shared_ptr<IScanDeviceIntent>     sdintent,
                        dune::imaging::types::MediaSizeId       mediaSize,
                        dune::scan::types::ScanFeedOrientation  orientation,
                        dune::imaging::types::Resolution        resolution,
                        dune::scan::types::ScanCaptureModeType  mode);

    /**
     * @brief 
     * 
     * @param resolution resolution of scan extents
     * @param includePrintMargins should print margins be considered
     * @param includeScanMargins should scan margins be considered
     */
    void setupScanMargins(std::shared_ptr<IScanDeviceIntent> sdintent,
                          dune::imaging::types::Resolution resolution, 
                          bool includePrintMargins, 
                          bool includeScanMargins);

    /**
     * @brief Checks if the invert color operation is supported on the scan device
     * @returns true if the invert colors operation is supported on the scan device
     */
    bool isInvertColorsSupportedOnScanDevice();
    
    /**
     * @brief Checks if the AutoCrop operation is supported on the scan device
     * @returns true if the AutoCrop colors operation is supported on the scan device
     */
    bool isAutoCropSupportedOnScanDevice();

    /**
     * @brief Check if the scaling operation is supported on scan device     
     * @return true if yes
     * @return false if no
     */
    bool isScaleSupportedOnScanDevice();

    /**
     * @brief Checks if the AutoDeskew operation is supported on the scan device
     * @returns true if the AutoDeskew operation is supported on the scan device
     */
    bool isAutoDeskewSupportedOnScanDevice();

    /**
     * @brief Checks if the AutoBackgroundColorRemoval operation is supported on the scan device
     * @returns true if the AutoBackgroundColorRemoval operation is supported on the scan device
     */
    bool isBackgroundColorRemovalSupportedOnScanDevice();

    /**
     * @brief Checks if the AutoBackgroundColorRemoval operation is supported on the scan device
     * @returns true if the AutoBackgroundColorRemoval operation is supported on the scan device
     */
    bool isBackgroundNoiseRemovalSupportedOnScanDevice();

    /**
     * @brief Checks if the input media is mixed size
     * @returns true if the input media is mixed size
     */
    bool isMixedSizeOriginals();

    /**
     * @brief Checks if scan device suppport blank page detection or not
     * @returns true if blank page detection supported from scan cpb
     */
    bool isBlankPageDetectionSupported();

    /**
     * @brief Checks if the Background Cleanup operation is supported on the scan device
     * @returns true if the Background Cleanup operation is supported on the scan device
     */
    bool isBackgroundCleanupSupportedOnScanDevice();

    /**
     * @brief in case of enterprise, if any is selected , check  the media is detected from sensor. And set detected media as input media.
     * @returns 
     */
    void DetectMediaFromSensor();

    /**
     * @brief Get the Sequencing Params
     *
     * @return std::shared_ptr<dune::imaging::Resources::SequencingParams> Sequencing Params
     */
    std::shared_ptr<dune::imaging::Resources::SequencingParams> getSequencingParams();

    /**
     * @brief Get the Rotation Angle to be performed by ImageRetriever / Layout Filter
     *
     * @return uint32_t Rotation Angle to be performed by ImageRetriever / Layout Filter
     */
    uint32_t getRotationAngle();

    /**
     * @brief Get the N-up Params
     *
     * @return dune::imaging::types::NUpParams(dune::imaging::types::NumberUp, dune::imaging::types::NumberUpPageOrder)
     */
    NUpParams getNUpParameters();

    /**
     * @brief Get the image number per sheet
     *
     * @return uint32_t The image number per sheet
     */
    uint32_t getImagesPerSheet();

    /**
     * @brief Get the Watermark Params
     *
     * @return dune::imaging::types::WatermarkParams
     */
    WatermarkParams getWatermarkParameters();

    /**
     * @brief Get the Stamp Params
     *
     * @return dune::imaging::types::StampParmas
     */
    std::unique_ptr<StampParams> getStampParametersLocation(const dune::imaging::types::StampLocation& location);

    /**
     * @brief Get the Text for StampType
     *
     * @return string
     */
    std::string getStampText(dune::imaging::types::StampContentT stampLocation);

    /**
     * @brief Get the DateAndTime Text
     *
     * @return string
     */
    std::string getlocaleDateAndTime(StampType stampType);

    /**
     * @brief Send print hint and set Ultra fast mode
     */
    void doPrintEarlyWarning(std::shared_ptr<IPageAssemblerIntent> intent, bool checkTray = true);

    FRIEND_TEST(GivenCopyPipelineResourcesSetup, WhenDoPrintEarlyWarningCalledWithoutCapability_UltraFastCopyModeDisabled);
    FRIEND_TEST(GivenCopyPipelineResourcesSetup, WhenDoPrintEarlyWarningCalledWithBasicModeFalse_UltraFastCopyModeDisabled);
    FRIEND_TEST(GivenCopyPipelineResourcesSetup, WhenDoPrintEarlyWarningCalledWithActiveJob_UltraFastCopyModeDisabled);
    FRIEND_TEST(GivenCopyPipelineResourcesSetup, WhenDoPrintEarlyWarningCalled_UltraFastCopyModeEnabled);
    
};

}}}}  // namespace dune::copy::Jobs::Copy
#endif // DUNE_COPY_PIPELINEBUILDER_H
