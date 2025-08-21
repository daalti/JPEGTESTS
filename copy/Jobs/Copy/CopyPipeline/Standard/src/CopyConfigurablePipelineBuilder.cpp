////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyConfigurablePipelineBuilder.cpp
 * @brief  CopyConfigurablePipelineBuilder for Copy jobs
 * @author Shubham Khandelwal
 * @date   2023-03-15
 *
 * (C) Copyright 2023 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "common_debug.h"

#include "CopyConfigurablePipelineBuilder_TraceAutogen.h"

#include "IColorDirector.h"
#include "IColorEngine.h"
#include "IImageColorEngine.h"
#include "IImagePersisterTicket.h"
#include "IImageProcessorTicket.h"
#include "IImageRetrieverTicket.h"
#include "IRtpFilterTicket.h"
#include "IScanPipeline.h"
#include "IIntentsManager.h"
#include "MediaHelper.h"
#include "ResourceInstanceProxy.h"
#include "CopyConfigurablePipelineBuilder.h"
#include "ICopyPipelineBuilderAdapter.h"
#include "IntentsManagerHelper.h"
#include "IImageRetrieverIntent.h"
#include "IImageImporterTicket.h"
#include "IPipeMetaInfo.h"


using namespace std;
using dune::job::IPipelineBuilder;
using dune::job::IResourceInstanceProxy;
using dune::job::IResourceService;
using dune::job::ResourceInstanceProxy;
using dune::job::ResourceInstanceProxyAgent;
using dune::imaging::types::Resolution;
using PlexSide = dune::imaging::types::PlexSide;
using IScanPipeline = dune::scan::Jobs::Scan::IScanPipeline;
using IIntentsManager = dune::job::IIntentsManager;
using ICopyAdapter = dune::copy::cdm::ICopyAdapter;

namespace dune { namespace copy { namespace Jobs { namespace Copy {

CopyConfigurablePipelineBuilder::CopyConfigurablePipelineBuilder(
    std::shared_ptr<ICopyJobTicket> ticket, const ServicesPackage &services, bool hasSharedPaperPath,
    IScanPipeline *scanPipeline, Product prePrintConfiguration, bool copyBasicPipeline,
    const MaxLengthConfig &maxLengthConfig, IIntentsManager *intentsManager, IDateTime *dateTime,
    bool multiPageSupportedFromFlatbed, ICopyAdapter *copyAdapter, bool layoutFilterEnabled)
    : BaseTemplate{ticket, services.resourceManager, dateTime},
      services_{services},
      scanDeviceInstanceProxy_{std::make_shared<ResourceInstanceProxy>(
          *ticket, *services.scanDeviceService->getResourceService(), getAgentAdapter())},
      imageProcessorProxy_{std::make_shared<ResourceInstanceProxy>(
          *ticket, *services.imageProcessor->getResourceService(), getAgentAdapter())},
      rtpFilterProxy_{std::make_shared<ResourceInstanceProxy>(*ticket, *services.rtpFilterService, getAgentAdapter())},
      printDeviceInstanceProxy_{std::make_shared<ResourceInstanceProxy>(
          *ticket, *services.printDevice->getResourceService(), getAgentAdapter())},
      intent_{ticket->getIntent()},
      ticket_{ticket},
      scanPipeline_{scanPipeline},
      intentsManager_{intentsManager},
      copyAdapter_{copyAdapter},
      prePrintConfiguration_{prePrintConfiguration},
      maxLengthConfig_{maxLengthConfig},
      copyBasicPipeline_{copyBasicPipeline},
      hasSharedPaperPath_{hasSharedPaperPath},
      multiPageSupportedFromFlatbed_{multiPageSupportedFromFlatbed},
      layoutFilterEnabled_{layoutFilterEnabled}
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder<%08X>::CopyConfigurablePipelineBuilder", getShortId());
    
    CHECKPOINTA("CopyConfigurablePipelineBuilder: copyBasicPipeline= %d", (int) copyBasicPipeline_);

    #if defined(JPEG_HARDWARE_AVAILABLE)
        CHECKPOINTA("CopyConfigurablePipelineBuilder: non-simulator job");
        simJob_ = false;
    #endif
    if (prePrintConfiguration_ == Product::ENTERPRISE)
    {
        copyEnterprisePipeline_ = true;
        #if defined(EFIVAR_EXIST)
        CHECKPOINTA("CopyConfigurablePipelineBuilder: non-simulator job - ENTERPRISE");
        simJob_ = false;
        #endif
    }
    assert_msg( scanDeviceInstanceProxy_ != nullptr, "CopyConfigurablePipelineBuilder: scanDevice Proxy is null" );
    assert_msg( imageProcessorProxy_ != nullptr, "CopyConfigurablePipelineBuilder: imageProcessor Proxy is null" );
    assert_msg( rtpFilterProxy_ != nullptr, "CopyConfigurablePipelineBuilder: rtpFilter Proxy is null" );
    assert_msg( printDeviceInstanceProxy_ != nullptr, "CopyConfigurablePipelineBuilder: printDevice Proxy is null" );
    allResources_.push_back(scanDeviceInstanceProxy_);
    allResources_.push_back(imageProcessorProxy_);
    allResources_.push_back(rtpFilterProxy_);
    allResources_.push_back(printDeviceInstanceProxy_);

    // Get scanner pipeline configuration
    assert_msg( scanPipeline_ != nullptr , "CopyConfigurablePipelineBuilder: scan Pipeline is null");
    scanPipelineConfig_ = scanPipeline_->getScanPipelineConfiguration();

    if (!copyBasicPipeline_)
    {
        //For designjet products, pageAssembler resource is not being instantiated by the print graph
        if(services.pageAssembler != nullptr)
        {
            dune::job::IResourceService* pageAssemblerIService = services.pageAssembler->getResourceService();
            pageAssemblerInstanceProxy_ = std::make_shared<ResourceInstanceProxy>(*ticket, *pageAssemblerIService, getAgentAdapter());
            allResources_.push_back(pageAssemblerInstanceProxy_);
        }
        if(scanPipelineConfig_->scanDiskBuffering)
        {
            bufferingImagePersisterProxy_ = std::make_shared<ResourceInstanceProxy>(*ticket, *services.imagePersister->getResourceService(), getAgentAdapter());
            bufferingImageRetrieverProxy_ = std::make_shared<dune::job::ResourceInstanceProxy>(*ticket, *services.imageRetrieverService, getAgentAdapter());
            assert_msg( bufferingImagePersisterProxy_ != nullptr, "CopyConfigurablePipelineBuilder: BufferimagePersister Proxy is null" );
            assert_msg( bufferingImageRetrieverProxy_ != nullptr, "CopyConfigurablePipelineBuilder: buffer image retriever Proxy is null" );
            allResources_.push_back(bufferingImagePersisterProxy_);
            allResources_.push_back(bufferingImageRetrieverProxy_);

            imageProcessorPreviewProxy_ = std::make_shared<dune::job::ResourceInstanceProxy>(*ticket, *services.imageProcessor->getResourceService(), getAgentAdapter());
            bufferingFinalSegmentImageRetrieverProxy_ = std::make_shared<dune::job::ResourceInstanceProxy>(*ticket, *services.imageRetrieverService, getAgentAdapter());
            assert_msg( imageProcessorPreviewProxy_ != nullptr, "CopyConfigurablePipelineBuilder: image processor preview Proxy is null" );
            assert_msg( bufferingFinalSegmentImageRetrieverProxy_ != nullptr, "CopyConfigurablePipelineBuilder: image retriever Proxy is null" );
            allResources_.push_back(bufferingFinalSegmentImageRetrieverProxy_);
            allResources_.push_back(imageProcessorPreviewProxy_);
        }
    }

    if(copyEnterprisePipeline_)
    {
        if(services.ipaDeviceService != nullptr)
        {
            ipaDeviceInstanceProxy_ = std::make_shared<ResourceInstanceProxy>(*ticket, *services.ipaDeviceService->getResourceService(), getAgentAdapter());
            allResources_.push_back(ipaDeviceInstanceProxy_);
        }
        if(services.imageImporter != nullptr)
        {
            imageImporterProxy_ = std::make_shared<ResourceInstanceProxy>(*ticket, *services.imageImporter->getResourceService(), getAgentAdapter());
            allResources_.push_back(imageImporterProxy_);
        }
        imageHandler_ = std::make_shared<dune::imaging::ImageHandler>(ticket.get());
    }

    imagePersisterProxy_ = std::make_shared<ResourceInstanceProxy>(*ticket, *services.imagePersister->getResourceService(), getAgentAdapter());
    imageRetrieverProxy_ = std::make_shared<dune::job::ResourceInstanceProxy>(*ticket, *services.imageRetrieverService, getAgentAdapter());
    markingFilterInstanceProxy_ = std::make_shared<ResourceInstanceProxy>(*ticket, *services.markingFilterService->getResourceService(), getAgentAdapter());
    layoutFilterInstanceProxy_ = std::make_shared<ResourceInstanceProxy>(
        *ticket, *services.layoutFilterService->getResourceService(), getAgentAdapter());
    assert_msg( imagePersisterProxy_ != nullptr , "CopyConfigurablePipelineBuilder: image persister Proxy is null");
    assert_msg( imageRetrieverProxy_ != nullptr , "CopyConfigurablePipelineBuilder: image retriever Proxy is null");
    assert_msg( markingFilterInstanceProxy_ != nullptr, "CopyConfigurablePipelineBuilder: makring filter Proxy is null" );
    assert_msg(layoutFilterInstanceProxy_ != nullptr, "CopyConfigurablePipelineBuilder: layout filter Proxy is null");
    allResources_.push_back(imagePersisterProxy_);
    allResources_.push_back(imageRetrieverProxy_);
    allResources_.push_back(markingFilterInstanceProxy_);
    allResources_.push_back(layoutFilterInstanceProxy_);
    if (scanPipeline_ != nullptr)
    {
        scanPipelineConfig_ = scanPipeline_->getScanPipelineConfiguration();
        scanPipelineBuilder_ = scanPipeline_->createScanPipelineBuilder();
        resourceSetupHelper_ = scanPipeline_->createCommonResourceSetupHelper();
    }
    resourceSetup_ = std::make_unique<CopyPipelineResourceSetup>(ticket_, services_, hasSharedPaperPath, scanPipeline, prePrintConfiguration, copyBasicPipeline, maxLengthConfig, dateTime);
    currentStage_ = Stage::Setup;
}

CopyConfigurablePipelineBuilder::ResourceInstanceProxiesSection CopyConfigurablePipelineBuilder::onInitialize()
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder: OnInitialization");
    if(ticket_->getExecutionMode() == dune::job::ExecutionMode::NORMAL)
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder: OnInitialization add Scan Device");
        resources_.push_back(scanDeviceInstanceProxy_);
    }
    else if (ticket_->getExecutionMode() == dune::job::ExecutionMode::RETRIEVE)
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder: OnInitialization diable Toast message for Enterprise");
        ticket_->setNativeJobStatusAlertsStatus(false);
    }
    if(prePrintConfiguration_ == Product::ENTERPRISE)
    {
        CHECKPOINTC("CopyConfigurablePipelineBuilder: OnInitialization Set all prompt completed false");
        ticket_->setAllPromptsCompleted(false);
    }
    return {resources_};
}

void CopyConfigurablePipelineBuilder::onJobCompletion(dune::job::JobCompletionPackage& completionPackage)
{
    CHECKPOINTC("CopyConfigurablePipelineBuilder: onJobCompletion");
    if(promptCanceled_)
    {
        completionPackage.setCompletionState(jobCompletionState_);
    }
    else if (ticket_->getIntent()->getScanNumberPages() == 0
        && ticket_->getExecutionMode() != dune::job::ExecutionMode::RETRIEVE
        && ticket_->getScanCalibrationType() == dune::imaging::types::ScanCalibrationType::UNKNOWN
        && ticket_->getCompletionState() == dune::job::CompletionStateType::SUCCESS)
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder: onJobCompletion Changed state to FAILED, ScanNumberPages is 0");
        completionPackage.setCompletionState(dune::job::CompletionStateType::FAILED);
    }
}


void CopyConfigurablePipelineBuilder::freeDoneAllocatedResources()
{
    for (auto resourceInstance : allResources_)
    {
        if (resourceInstance->getState() == IResourceInstanceProxy::StateType::DoneStillAllocated)
        {
            CHECKPOINTC("CopyConfigurablePipelineBuilder::freeDoneAllocatedResources freing resource %u",
                        static_cast<int>(resourceInstance->getShortId()));
            resourceInstance->setKeep(false);
            resourceInstance->free();
        }
    }
}

void CopyConfigurablePipelineBuilder::hold()
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder::hold");
    
    // Free all DoneStillAllocated resources
    freeDoneAllocatedResources();

    // Reset final resources by creating them again
    imageRetrieverProxy_ = std::make_shared<dune::job::ResourceInstanceProxy>(*ticket_, *services_.imageRetrieverService, getAgentAdapter());
    printDeviceInstanceProxy_ = std::make_shared<dune::job::ResourceInstanceProxy>(*ticket_, *services_.printDevice->getResourceService(), getAgentAdapter());
    
    // Add the resources to the all resources list. This way they will be freed when the job is done.
    allResources_.push_back(imageRetrieverProxy_);
    allResources_.push_back(printDeviceInstanceProxy_);
}

void CopyConfigurablePipelineBuilder::interrupt()
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder::interrupt");
    
    // Free all DoneStillAllocated resources
    freeDoneAllocatedResources();

    // Reset final resources by creating them again
    imageRetrieverProxy_ = std::make_shared<dune::job::ResourceInstanceProxy>(*ticket_, *services_.imageRetrieverService, getAgentAdapter());
    printDeviceInstanceProxy_ = std::make_shared<dune::job::ResourceInstanceProxy>(*ticket_, *services_.printDevice->getResourceService(), getAgentAdapter());
    
    // Add the resources to the all resources list. This way they will be freed when the job is done.
    allResources_.push_back(imageRetrieverProxy_);
    allResources_.push_back(printDeviceInstanceProxy_);
}

void CopyConfigurablePipelineBuilder::populateResourceDetails(
    std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> resourceList)
{
    // If jobLet is set to a resource which is enabled on the basis of condition
    //use this property to set jobLet boundary to next resource
    bool addJobLetToNextResource = false;
    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails onEntry");

    resourcesSetupList_.clear();

    useImageProcessor_ = false;
    useMarkingFilter_ = false;

    for (auto resource = resourceList.begin(); resource != resourceList.end(); ++resource)
    {
        using ResourceName = dune::scan::Jobs::Scan::ResourceName;
        auto resourceName = resource->get()->resourceId;
        CHECKPOINTA("CopyConfigurablePipelineBuilder::populateResourceDetails()::Entry, %d", resourceName);

        // TODO: Need to move to another function
        if(addJobLetToNextResource)
        {
            resource->get()->jobletBoudary = dune::job::JobletBoundary::START;
            addJobLetToNextResource = false;
        }

        // If it's a preview resource and has START jobLet move jobLet to Next resource
        if(previewJob_)
        {
            if(resourceName == ResourceName::IMAGEPROCESSOR  && resource->get()->jobletBoudary == dune::job::JobletBoundary::START)
            {
                CHECKPOINTA("CopyConfigurablePipelineBuilder::populateResourceDetails():: joblet is set to preview resource move joblet");
                resource->get()->jobletBoudary = dune::job::JobletBoundary::UNDEFINED;
                addJobLetToNextResource = true;
            }
        }

        // Resolve EnabledIf condtion
        if(resource->get()->enabledIf.size() > 0)
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder::populateResourceDetails()::enabledIf");
            
            if(resolveEnabledIfProperty(resource->get()->enabledIf))
            {
                CHECKPOINTA("CopyConfigurablePipelineBuilder::populateResourceDetails()::enabledIf resource is added ");
            }
            else if (useImagePersister_ && resourceName == ResourceName::LAYOUTFILTER)
            {
                CHECKPOINTA(
                    "CopyConfigurablePipelineBuilder::populateResourceDetails()::enabledIf LayoutFilter not required, "
                    "changing it by ImageRetriever");
                resource->get()->resourceId = ResourceName::IMAGERETRIEVER;
                resourceName = resource->get()->resourceId;
            }
            else
            {
                if(resource->get()->jobletBoudary == dune::job::JobletBoundary::START)
                {
                    addJobLetToNextResource = true;
                }
                CHECKPOINTA("CopyConfigurablePipelineBuilder::populateResourceDetails()::enabledIf resource not required ");
                continue;
            }
        }

        // add the resources
        switch (resourceName)
        {
            case ResourceName::SCANDEVICE:
                {
                    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails ScanDevice");
                    scanDeviceConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get()));
                    IScanPipeline::ResourceDetails scanResourceDetails = {scanDeviceInstanceProxy_,
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                        std::bind(&CopyConfigurablePipelineBuilder::setupScanDevice, this, std::placeholders::_1)};

                    resourcesSetupList_.push_back(std::make_pair(
                        ResourceName::SCANDEVICE, scanResourceDetails));
                    break;
                }
            case ResourceName::IPADEVICE:
                {
                    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails IPADevice");
                    ipaDeviceConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get()));
                    IScanPipeline::ResourceDetails ipaResourceDetails = {ipaDeviceInstanceProxy_,
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                        std::bind(&CopyConfigurablePipelineBuilder::setupIPADevice, this, std::placeholders::_1)};
                    resourcesSetupList_.push_back(std::make_pair(
                        ResourceName::IPADEVICE, ipaResourceDetails));
                    break;
                }
            case ResourceName::IMAGEIMPORTER:
                {
                    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails ImageImporter");
                    imageImporterConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get()));
                    IScanPipeline::ResourceDetails imageImporterDetails = {imageImporterProxy_,
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                        std::bind(&CopyConfigurablePipelineBuilder::setupImageImporter, this, std::placeholders::_1)};
                    resourcesSetupList_.push_back(std::make_pair(
                        ResourceName::IMAGEIMPORTER, imageImporterDetails));
                    break;
                }
            case ResourceName::IMAGEPROCESSOR:
                {
                    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails ImageProcessor");
                    imageProcessorConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get()));
                    IScanPipeline::ResourceDetails ipResourceDetails = {imageProcessorProxy_,
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                        std::bind(&CopyConfigurablePipelineBuilder::setupImageProcessorTicket, this, std::placeholders::_1)};
                    resourcesSetupList_.push_back(std::make_pair(ResourceName::IMAGEPROCESSOR, ipResourceDetails));
                    useImageProcessor_ = true;
                }
                break;
            case ResourceName::IMAGEPROCESSORPREVIEW:
                {
                    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails ImageProcessorPreview");
                    imageProcessorConfig_ =
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get()));
                    
                    if (imageProcessorPreviewProxy_)
                    {
                        CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails ImageProcessorPreview");
                        IScanPipeline::ResourceDetails ippResourceDetails = {imageProcessorPreviewProxy_,
                                std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                                std::bind(&CopyConfigurablePipelineBuilder::setupImageProcessorPreview, this, std::placeholders::_1)};
                        resourcesSetupList_.push_back(std::make_pair(
                            ResourceName::IMAGEPROCESSORPREVIEW, ippResourceDetails));

                    }
                    else
                    {
                        CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails ImageProcessor with preview method");
                        IScanPipeline::ResourceDetails ippResourceDetails = {imageProcessorProxy_,
                                std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                                std::bind(&CopyConfigurablePipelineBuilder::setupImageProcessorPreview, this, std::placeholders::_1)};
                        resourcesSetupList_.push_back(std::make_pair(
                            ResourceName::IMAGEPROCESSORPREVIEW, ippResourceDetails));

                    }
                    useImageProcessor_ = true;
                }
                break;
            case ResourceName::IMAGEPERSISTER:
                {
                    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails ImagePersiter");
                    imagePersisterConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get()));
                    IScanPipeline::ResourceDetails iperResourceDetails = {imagePersisterProxy_,
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                        std::bind(&CopyConfigurablePipelineBuilder::setupImagePersister, this, std::placeholders::_1)};
                    resourcesSetupList_.push_back(std::make_pair(
                        ResourceName::IMAGEPERSISTER, iperResourceDetails));
                    useImagePersister_ = true;
                }
                break;
            case ResourceName::IMAGEPERSISTERDISKBUFFERING:
                {
                    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails onEntry ImagePersisterDiskBuffering");
                    imagePersisterDiskBufferingConfig_ =
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get()));
                    IScanPipeline::ResourceDetails ipdfResourceDetails = {bufferingImagePersisterProxy_,
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                        std::bind(&CopyConfigurablePipelineBuilder::setupBufferingImagePersister, this,
                                    std::placeholders::_1)};
                    resourcesSetupList_.push_back(std::make_pair(
                        ResourceName::IMAGEPERSISTERDISKBUFFERING, ipdfResourceDetails));
                    useImagePersister_ = true;
                }
                break;
            case ResourceName::IMAGERETRIEVER:
                {
                    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails onEntry ImageRetriever");
                    imageRetrieverConfig_ =
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get()));
                    IScanPipeline::ResourceDetails irResourceDetails = {imageRetrieverProxy_,
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                        std::bind(&CopyConfigurablePipelineBuilder::setupImageRetriever, this,
                                    std::placeholders::_1)};
                    resourcesSetupList_.push_back(std::make_pair(
                        ResourceName::IMAGERETRIEVER, irResourceDetails));
                }
                break;
            case ResourceName::IMAGERETRIEVERDISKBUFFERING:
                {
                    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails onEntry ImageRetrieverDiskBuffering");
                    imageRetrieverDiskBufferingConfig_ =
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get()));
                    IScanPipeline::ResourceDetails irdfResourceDetails = {bufferingImageRetrieverProxy_,
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                        std::bind(&CopyConfigurablePipelineBuilder::setupBufferingImageRetriever, this,
                                    std::placeholders::_1)};
                    resourcesSetupList_.push_back(std::make_pair(
                        ResourceName::IMAGERETRIEVERDISKBUFFERING, irdfResourceDetails));
                }
                break;
            case ResourceName::IMAGERETRIEVERFINALDISKBUFFERING:
                {
                    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails onEntry ImageRetrieverFinalDiskBuffering");
                    imageRetrieverFinalDiskBufferingConfig_ =
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get()));
                    IScanPipeline::ResourceDetails irfdbResourceDetails = {bufferingFinalSegmentImageRetrieverProxy_,
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                        std::bind(&CopyConfigurablePipelineBuilder::setupFinalBufferingImageRetriever, this,
                                    std::placeholders::_1)};
                    resourcesSetupList_.push_back(std::make_pair(
                        ResourceName::IMAGERETRIEVERFINALDISKBUFFERING, irfdbResourceDetails));
                }
                break;
            case ResourceName::PAGEASSEMBLER:
                {
                    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails onEntry Page Assembler");
                    pageAssemblerConfig_ =
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get()));
                    IScanPipeline::ResourceDetails paResourceDetails = {pageAssemblerInstanceProxy_,
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                        std::bind(&CopyConfigurablePipelineBuilder::setupPageAssembler, this, std::placeholders::_1)};
                    resourcesSetupList_.push_back(std::make_pair(
                        ResourceName::PAGEASSEMBLER, paResourceDetails));
                }
                break;
            case ResourceName::RTPFILTER:
                {
                    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails onEntry RTPFilter");
                    IScanPipeline::ResourceDetails rtpResourceDetails = {rtpFilterProxy_,
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                        std::bind(&CopyConfigurablePipelineBuilder::setupRtpFilterTicket, this, std::placeholders::_1)};
                    resourcesSetupList_.push_back(std::make_pair(
                        ResourceName::RTPFILTER, rtpResourceDetails));
                }
                break;
            case ResourceName::MARKINGFILTER:
                {
                    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails onEntry MarkingFilter");
                    markingFilterConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get()));
                    IScanPipeline::ResourceDetails mfResourceDetails = {markingFilterInstanceProxy_,
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                        std::bind(&CopyConfigurablePipelineBuilder::setupMarkingFilter, this, std::placeholders::_1)};
                    resourcesSetupList_.push_back(std::make_pair(
                        ResourceName::MARKINGFILTER, mfResourceDetails));
                    useMarkingFilter_ = true;
                }
                break;
            case ResourceName::LAYOUTFILTER:
                {
                    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails onEntry LayoutFilter");
                    layoutFilterConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get()));
                    IScanPipeline::ResourceDetails layoutFilterResourceDetails = {
                        layoutFilterInstanceProxy_,
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                        std::bind(&CopyConfigurablePipelineBuilder::setupLayoutFilter, this, std::placeholders::_1)};
                    resourcesSetupList_.push_back(
                        std::make_pair(ResourceName::LAYOUTFILTER, layoutFilterResourceDetails));
                    useLayoutFilter_ = true;
                }
                break;
            case ResourceName::PRINTDEVICE:
                {
                    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails onEntry PrintDevice");
                    printDeviceConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get()));
                    IScanPipeline::ResourceDetails pdResourceDetails = {
                        printDeviceInstanceProxy_,
                        std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())),
                        std::bind(&CopyConfigurablePipelineBuilder::setupPrintDevice, this, std::placeholders::_1)};
                    resourcesSetupList_.push_back(std::make_pair(ResourceName::PRINTDEVICE, pdResourceDetails));
                }
                break;
            default:
                CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails no resource");
                assert_msg( false, "CopyConfigurablePipelineBuilder: no resource added" );
                break;
        }
    }
    CHECKPOINTA("CopyConfigurablePipelineBuilder: populateResourceDetails onExit");
    
}

void CopyConfigurablePipelineBuilder::setJobName()
{
    if(ticket_->getPrePrintConfiguration() == Product::HOME_PRO)
    {
        if(ticket_->getIntent()->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD)
        {
            ticket_->setJobName("IDCardCopy");
            CHECKPOINTC("CopyConfigurablePipelineBuilder::setJobName IDCardCopy");
        }
        else
        {
            ticket_->setJobName("Copy");
            CHECKPOINTC("CopyConfigurablePipelineBuilder::setJobName Copy");
        }
    }
}

void CopyConfigurablePipelineBuilder::setResourceSetupConfiguration()
{
    resourceSetup_->setCurrentStage(currentStage_);
    resourceSetup_->setCollateMode(collateMode_);
    resourceSetup_->setSegmentType(segmentType_);
    resourceSetup_->setThresholdOverride(thresholdOverride_);
    resourceSetup_->setTopSpecificPadding(topSpecificPadding_);
    resourceSetup_->setBottomSpecificPadding(bottomSpecificPadding_);
    resourceSetup_->setLeftSpecificPadding(leftSpecificPadding_);
    resourceSetup_->setRightSpecificPadding(rightSpecificPadding_);
    resourceSetup_->setPageCountBeforeSequencing(pageCountBeforeSequencing_);
    resourceSetup_->setMaxPagesToCollate(maxPagesToCollate_);
}

void CopyConfigurablePipelineBuilder::setCopyPipelineForNonEnterprise(PromptType promptType, PromptResponseType responseType,
                                                   SegmentType segmentType)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder: setCopyPipelineForNonEnterprise");
    pipelineSections_.clear();

    //Handle prompt if one was just responded to
    if (promptType != PromptType::None)
    {
        handlePromptResponse(responseType, promptType);
    }

    // Set the First Stage of pipeline
    if ((currentStage_ == Stage::Setup || ((currentStage_ == Stage::Preview || currentStage_ == Stage::StopPreview) && segmentType == SegmentType::FinalSegment)))
    {
        setFirstStage();
    }

    if(currentStage_ == Stage::Finished || isPreviousResourceStateFailed())
    {
        resourceConfig_.clear();
        return ;
    }
    
    
    auto previousSegmentType_ = segmentType_;
    segmentType_ = segmentType;
    
    assert_msg(copyPipelineConfiguration_->pipelineSegements.size() != 0,
                "CopyConfigurablePipeline::onBuildPipeline()-  pipeline config is null");

    // Scan maintenance
    if (ticket_->getScanCalibrationType() != imaging::types::ScanCalibrationType::UNKNOWN)
    {
        CHECKPOINTC("CopyConfigurablePipelineBuilder::onBuildPipeline - SCAN CALIBRATION %d - entry", ticket_->getScanCalibrationType());

        intent_->setScanCalibrationType(ticket_->getScanCalibrationType());
        resourceConfig_ = getResourceList(dune::scan::Jobs::Scan::PipelineSegmentType::MAINTENANCE_SEGMENT);

        //currentStage_ = Stage::Finished;
        nextStage_ = Stage::Finished;

        CHECKPOINTC("CopyConfigurablePipelineBuilder::onBuildPipeline - SCAN CALIBRATION - exit");
    }
    else if (currentStage_ == Stage::PreScan)
    {
        //setup scandevice with autocrop turned on
        CHECKPOINTC("CopyConfigurablePipelineBuilder: onBuildPipeline PreScan");

        ResourceInstanceProxies firstSection;
        pipelineSections_.push_back(firstSection);
        //Add it to the first section of the pipeline
        pipelineSections_[0].push_back(scanDeviceInstanceProxy_);
        pipelinePolicy_ = dune::job::PipelinePolicy::allocate_and_start;

        setupScanDevice({nullptr, nullptr});
        scanDeviceInstanceProxy_->setKeep(true);
        prescanJob_ = true;
        // Call set first stage method to set next stage after prescan
        setFirstStage();
        nextStage_ = currentStage_;
    }
    else if (segmentType == SegmentType::PrepareSegment)
    {
        currentStage_ = Stage::Preview;
        CHECKPOINTC("CopyConfigurablePipelineBuilder: onBuildPipeline PrepareSegment");
        resetAllocatedResources();
        if(previousSegmentType_ == SegmentType::PrepareSegment && scanPipelineConfig_->pipelineBuilderConfig->previewSettings->refreshPreviewSupported) 
        {
            scanPipeline_->handleRefreshPreview(ticket_);
        }
            
        if (scanPipelineConfig_->pipelineBuilderConfig->previewSettings->savePreviewMode)
        {
            ticket_->setPreviewMode(true);
            previewJob_ = true;
        }

        //Check copy mode value
        if(copyAdapter_ && copyAdapter_->getCopyMode() == dune::cdm::copy_1::configuration::CopyMode::printWhileScanning
            && prePrintConfiguration_ == Product::LFP)
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder: onBuildPipeline Print while scanning copy mode");
            resourceConfig_ = getResourceList(dune::scan::Jobs::Scan::PipelineSegmentType::DIRECT_JOB_SEGMENT);
            nextStage_ = Stage::DirectCopy;
        }
        
        else
        {
            resourceConfig_ = scanPipeline_->getResourceList(dune::scan::Jobs::Scan::PipelineSegmentType::PREPARE_SEGMENT);
            nextStage_ = Stage::StopPreview;
        }
        
    }

    else if (currentStage_ == Stage::ScanFirstPage || currentStage_ == Stage::ScanPage)
    {
        CHECKPOINTC("CopyConfigurablePipelineBuilder: onBuildPipeline ScanFirstPage || ScanPage");
        numScanPages_ = 1;

        if (previewJob_)
        {
            resetAllocatedResources();
        }

        // Use LayoutFilter's tests pipelines if requested
        dune::scan::Jobs::Scan::PipelineSegmentType pipelineSegmentType{
            dune::scan::Jobs::Scan::PipelineSegmentType::MULTIPAGE_SEGMENT_ONE};
        if (layoutFilterEnabled_ &&
            findSegment(dune::scan::Jobs::Scan::PipelineSegmentType::TEST_MULTIPAGE_SEGMENT_ONE_LAYOUT_FILTER) &&
            isLayoutFilterNeeded(
                dune::scan::Jobs::Scan::PipelineSegmentType::TEST_MULTIPAGE_SEGMENT_THREE_LAYOUT_FILTER))
        {
            pipelineSegmentType = dune::scan::Jobs::Scan::PipelineSegmentType::TEST_MULTIPAGE_SEGMENT_ONE_LAYOUT_FILTER;
            useLayoutFilter_ = true;
        }
        resourceConfig_ = getResourceList(pipelineSegmentType);
        ticket_->setFirstScanStarted(true);
        if (currentStage_ == Stage::ScanPage)
        {
            nextStage_ = Stage::PrintAllPages;
        }
        else
        {
            nextStage_ = Stage::ScanSecondPage;
        }
    }
    else if (currentStage_ == Stage::ScanSecondPage)
    {
        numScanPages_++;
        CHECKPOINTA("CopyConfigurablePipelineBuilder::onBuildPipeline ScanSecondPage - Current page: %d",
                    numScanPages_);

        dune::scan::Jobs::Scan::PipelineSegmentType pipelineSegmentType{
            dune::scan::Jobs::Scan::PipelineSegmentType::MULTIPAGE_SEGMENT_TWO};
        if (layoutFilterEnabled_ &&
            findSegment(dune::scan::Jobs::Scan::PipelineSegmentType::TEST_MULTIPAGE_SEGMENT_TWO_LAYOUT_FILTER) &&
            isLayoutFilterNeeded(
                dune::scan::Jobs::Scan::PipelineSegmentType::TEST_MULTIPAGE_SEGMENT_THREE_LAYOUT_FILTER))
        {
            pipelineSegmentType = dune::scan::Jobs::Scan::PipelineSegmentType::TEST_MULTIPAGE_SEGMENT_TWO_LAYOUT_FILTER;
            useLayoutFilter_ = true;
        }
        resourceConfig_ = getResourceList(pipelineSegmentType);

        // Reset Resources
        scanDeviceInstanceProxy_->reset();
        if (useLayoutFilter_)
        {
            imageProcessorProxy_->reset();
        }
        imagePersisterProxy_->reset();
    }
    else if (currentStage_ == Stage::PrintAllPages)
    {
        CHECKPOINTC("CopyConfigurablePipelineBuilder: onBuildPipeline PrintAllPages");
        ticket_->setFirstScanStarted(false);

        dune::scan::Jobs::Scan::PipelineSegmentType pipelineSegmentType{
            dune::scan::Jobs::Scan::PipelineSegmentType::MULTIPAGE_SEGMENT_THREE};
        if (layoutFilterEnabled_ &&
            isLayoutFilterNeeded(
                dune::scan::Jobs::Scan::PipelineSegmentType::TEST_MULTIPAGE_SEGMENT_THREE_LAYOUT_FILTER))
        {
            pipelineSegmentType =
                dune::scan::Jobs::Scan::PipelineSegmentType::TEST_MULTIPAGE_SEGMENT_THREE_LAYOUT_FILTER;
            useLayoutFilter_ = true;
        }
        resourceConfig_ = getResourceList(pipelineSegmentType);
        nextStage_ = Stage::Finished;
    }
    else if (currentStage_ == Stage::Reprint)
    {
        CHECKPOINTC("CopyConfigurablePipelineBuilder: onBuildPipeline Reprint");
        // Relase the scan resource as not required for reprint
        services_.scanDeviceService->releaseResource();
        // Set the Print Intents for reprint
        ticket_->setPrintIntentsFactory(services_.printIntentsFactory);

        persistentPipePath_ = ticket_->getPersistentPipePath();
        resourceConfig_ = getResourceList(dune::scan::Jobs::Scan::PipelineSegmentType::RERUN);
        nextStage_ = Stage::Finished;
    }
    else if (segmentType == SegmentType::FinalSegment)
    {
        CHECKPOINTC("CopyConfigurablePipelineBuilder: onBuildPipeline FinalSegment");
        
        //In case of direct copy, we do not need to allocate any resources in the final segment
        resourceConfig_.clear();
        if(currentStage_ != Stage::DirectCopy)
        {
            resetAllocatedResources();

            dune::scan::Jobs::Scan::PipelineSegmentType pipelineSegmentType{
                dune::scan::Jobs::Scan::PipelineSegmentType::FINAL_SEGMENT};
            if (layoutFilterEnabled_ &&
                isLayoutFilterNeeded(dune::scan::Jobs::Scan::PipelineSegmentType::TEST_FINAL_SEGMENT_LAYOUT_FILTER))
            {
                pipelineSegmentType = dune::scan::Jobs::Scan::PipelineSegmentType::TEST_FINAL_SEGMENT_LAYOUT_FILTER;
                useLayoutFilter_ = true;
            }
            resourceConfig_ = getResourceList(pipelineSegmentType);
        }
        
        nextStage_ = Stage::Finished;
        //TODO: refactor this code
        if(prePrintConfiguration_ == Product::LFP)
        {
            // When we are on a multipage process, and from user is set Final Segment.
            // We will advise Scan Device Service to release the resource and final normally at its execution.
            CHECKPOINTA("CopyConfigurablePipelineBuilder::onBuildPipeline release scan resource");
            services_.scanDeviceService->releaseResource();

            // Call this method to update the previewImage Path with new edit image path 
            //(if editOperation is applied on the image)
            scanPipeline_->updatePreviewImagePathIfEdited(ticket_);
        }
    }
    else
    {
        //TODO: Create adefault pipeline or assert?
    }

    if (nextStage_ == Stage::Finished)
    {
        ticket_->setJobCompleting(true);
    }
}

CopyConfigurablePipelineBuilder::ResourceInstanceProxiesSection CopyConfigurablePipelineBuilder::onBuildPipeline(
    PromptType promptType, PromptResponseType responseType, SegmentType segmentType)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder::onBuildPipeline onEntry");
    CHECKPOINTA("CopyConfigurablePipelineBuilder::onBuildPipeline: currentStage_:%d, segmentType:%d, executionMode:%d", currentStage_, segmentType, ticket_->getExecutionMode());
    // Set the job name
    setJobName();
    setCollateMode();
    resources_.clear();
    pipelineSections_.clear();
    
    // Prepare segment works similar as Final Segment
    // So, in case of pro device return empty list once preview segment is executed.
    if(currentStage_ == Stage::StopPreview && segmentType == SegmentType::PrepareSegment)
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder: onBuildPipeline: StopPreview");
        currentStage_ = Stage::Preview;
        pipelineSections_.clear();
        if(prePrintConfiguration_== Product::ENTERPRISE)
        {
            ticket_->setPreviewMode(true);
            ticket_->setFirstScanStarted(false);
        }
        return pipelineSections_;
    }

    if (currentStage_ == Stage::Finished && 
        (ticket_->getExecutionMode() == dune::job::ExecutionMode::RETRY || 
         ticket_->getExecutionMode() == dune::job::ExecutionMode::RESUME))
    {
        //set excution mode back to normal. So, next time pipeline is not created
        ticket_->setExecutionMode(dune::job::ExecutionMode::NORMAL);
        persistentPipePath_ = ticket_->getPersistentPipePath();
        currentStage_ = Stage::Retry;
    }

    if (currentStage_ == Stage::Retry)
    {
        CHECKPOINTC("CopyConfigurablePipelineBuilder: onBuildPipeline Retry");
        // Set the Print Intents for reprint
        ticket_->setPrintIntentsFactory(services_.printIntentsFactory);

        dune::scan::Jobs::Scan::PipelineSegmentType pipelineSegmentType{
            dune::scan::Jobs::Scan::PipelineSegmentType::RETRY};
        if (layoutFilterEnabled_ &&
            isLayoutFilterNeeded(dune::scan::Jobs::Scan::PipelineSegmentType::TEST_RETRY_LAYOUT_FILTER))
        {
            pipelineSegmentType = dune::scan::Jobs::Scan::PipelineSegmentType::TEST_RETRY_LAYOUT_FILTER;
            useLayoutFilter_ = true;
        }
        resourceConfig_ = getResourceList(pipelineSegmentType);

        //if it's a retry pipeline - ALL the resources need to be RESET and setkeep need to be set as true

        nextStage_ = Stage::Finished;
    }

    else if (ticket_->getExecutionMode() == dune::job::ExecutionMode::RETRIEVE)
    {
        if(currentStage_ != Stage::Finished)
        {
            if (ticket_->getInputPipeMetaInfo())
            {
                populateJobTicketWithJobMetaInfo(ticket_->getInputPipeMetaInfo());
            }
            ticket_->setPrintIntentsFactory(services_.printIntentsFactory);
            persistentPipePath_ = ticket_->getPersistentPipePath();
            CHECKPOINTA("CopyConfigurablePipelineBuilder: onBuildPipeline: RETRIEVE execution mode %s", persistentPipePath_.c_str());
            resourceConfig_ = getResourceList(dune::scan::Jobs::Scan::PipelineSegmentType::RETRIEVE);
            nextStage_ = Stage::Finished;
        }
    }    
    // For Enterprise products, the pipeline is built by the scan pipeline builder 
    // In future other products will also follow the same pattern
    else if (prePrintConfiguration_ == Product::ENTERPRISE)
    {
        // if copy output ple mode is duplex request scan pipeline to create multiscan
        if(ticket_->getIntent()->getOutputPlexMode() == dune::imaging::types::Plex::DUPLEX && ticket_->getIntent()->getScanSource() == dune::scan::types::ScanSource::GLASS)
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder: onBuildPipeline: Duplex mode");
            scanPipelineBuilder_->setMultiScanPipeline(true);
        }
        auto scanStage = scanPipelineBuilder_->buildScanPipeline(promptType, responseType, segmentType, ticket_->getIntent(), resourceConfig_);

        switch (scanStage)
        {
            // In Case of None Scan Stage Respective pipeline need to handle it
            case dune::scan::Jobs::Scan::ScanStage::NONE:
                resourceConfig_ = getResourceList(dune::scan::Jobs::Scan::PipelineSegmentType::FINAL_SEGMENT);                
                ticket_->setAllPromptsCompleted(true);
                nextStage_ = Stage::Finished;
                break;
        
            case dune::scan::Jobs::Scan::ScanStage::FinishedPreviewMultiScan:
                CHECKPOINTA("CopyConfigurablePipelineBuilder: onBuildPipeline: Preview is finished execute the last segment");
                nextStage_ = Stage::Finished;
                ticket_->setFirstScanStarted(false);
                ticket_->setAllPromptsCompleted(true);
                freeAllocatedResources();
                resourceConfig_ = getResourceList(dune::scan::Jobs::Scan::PipelineSegmentType::PREVIEW_FINAL_SEGMENT);
                break;
        
            case dune::scan::Jobs::Scan::ScanStage::StopPreviewStage:
                CHECKPOINTA("CopyConfigurablePipelineBuilder: onBuildPipeline: StopPreviewStage");
                nextStage_ = currentStage_;
                ticket_->setFirstScanStarted(false);
                ticket_->setPreviewMode(true);
                break;

            case dune::scan::Jobs::Scan::ScanStage::FirstScanStage:
            case dune::scan::Jobs::Scan::ScanStage::MultiScanStage:
                CHECKPOINTA("CopyConfigurablePipelineBuilder: onBuildPipeline: scan pipeline will handle the First/Multi ScanStage - set firstScanStarted");
                ticket_->setFirstScanStarted(true);
                nextStage_ = currentStage_;
                if(scanStage == dune::scan::Jobs::Scan::ScanStage::MultiScanStage)
                {
                    //after the first scan, subsequent sides will be toggling between front and back
                    flatbedDuplexBackSide_ = !flatbedDuplexBackSide_ ;
                }
                break;
            
            case dune::scan::Jobs::Scan::ScanStage::PreviewStage:
            case dune::scan::Jobs::Scan::ScanStage::MultiPreviewStage:
                CHECKPOINTA("CopyConfigurablePipelineBuilder: onBuildPipeline: scan pipeline will handle the stage set Preview/MultiPreview Stage");
                ticket_->setFirstScanStarted(true);
                ticket_->setPreviewMode(false);
                if ((ticket_->getIntent()->getPromptForMorePages() ||
                   (ticket_->getIntent()->getInputPlexMode() == dune::imaging::types::Plex::DUPLEX ||  ticket_->getIntent()->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp) || 
                   (ticket_->getIntent()->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::BOOKMODE) || (ticket_->getIntent()->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD)) &&
                    ticket_->getIntent()->getScanSource() == dune::scan::types::ScanSource::GLASS)
                {
                    nextStage_ = currentStage_;
                }
                else
                {
                    nextStage_ = Stage::StopPreview;
                }
                
                break;
        
            case dune::scan::Jobs::Scan::ScanStage::FinishedFinalMultiScan:
                nextStage_ = Stage::Finished;
                ticket_->setFirstScanStarted(false);
                ticket_->setAllPromptsCompleted(true);
                //Need to have some better way to handel the prompt states
                ticket_->setPreviewMode(true);
                freeAllocatedResources();
                scanDeviceInstanceProxy_->setKeep(false);
                imagePersisterProxy_->setKeep(false);
                resourceConfig_ = getResourceList(dune::scan::Jobs::Scan::PipelineSegmentType::MULTIPAGE_SEGMENT_THREE);
                break;

            case dune::scan::Jobs::Scan::ScanStage::Cancelled:
                promptCanceled_ = true;
                resources_.clear();
                jobCompletionState_ = dune::job::CompletionStateType::CANCELED;
                ticket_->setFirstScanStarted(false);
                ticket_->setAllPromptsCompleted(true);
                ticket_->setCompletionState(jobCompletionState_);
                freeAllocatedResources();
                nextStage_ = Stage::Finished;
                currentStage_ = Stage::Finished;
                break;

            case dune::scan::Jobs::Scan::ScanStage::EmptyDone:
                resources_.clear();
                ticket_->setFirstScanStarted(false);
                if(segmentType == SegmentType::PrepareSegment)
                {
                    nextStage_ = Stage::StopPreview;
                }
                else
                {
                    freeAllocatedResources();
                    nextStage_ = Stage::Finished;
                    currentStage_ = Stage::Finished;
                }
                break;
            default:
                CHECKPOINTA("CopyConfigurablePipelineBuilder: onBuildPipeline: scan pipeline will handle the stage");
                break;
            }
    }
    else
    {
        setCopyPipelineForNonEnterprise(promptType, responseType, segmentType);  
    }

    
    if(currentStage_ == Stage::Finished || (isPreviousResourceStateFailed()&& currentStage_ != Stage::Retry))
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder: onBuildPipeline: Finished or isPreviousResourceStateFailed");
        pipelineSections_.clear();
        return pipelineSections_;
    }
    // Set the resource setup configuration
    setResourceSetupConfiguration();

    populateResourceDetails(resourceConfig_);
    scanPipeline_->createPipeQueuesAndResourceList(resourcesSetupList_, pipelineSections_, PipelineBuilderBase::pipeQueues_,
                                                   persistedResourceList, nullptr, ticket_->getStorePath(),
                                                   persistentPipePath_, ticket_);

    ticket_->setPersistentPipePath(persistentPipePath_);

    //if resource list is empty fail the job
    if(pipelineSections_.size() == 0 || pipelineSections_[0].size() == 0)
    {
        jobCompletionState_ = dune::job::CompletionStateType::FAILED;
        ticket_->setCompletionState(jobCompletionState_);
    }
    //set pipeline policy
    applyPipelinePolicy();

    setPrintingOrderForCollate();
    setReourcesTrueForCollate();

    // set the currentStage as nextStage
    CHECKPOINTA("CopyConfigurablePipelineBuilder: onBuildPipeline: Setting Stage from %d to %d", (int)currentStage_, (int)nextStage_);
    currentStage_ = nextStage_;

    auto size = pipelineSections_.size();
    for(decltype(size) i = 0; i < size; i++)
    {
        for(auto &resource : pipelineSections_[i])
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder::onBuildPipeline Section: %d PipelineResource: %s\n", i + 1, resource->getResourceServiceId().c_str());
        }
    }

    fillCopyPipelineJobTicketSettings();

    // update the resource ticket through intent manager
    updateResourcesTicket();

    return pipelineSections_;
}

void CopyConfigurablePipelineBuilder::setPrintingOrderForCollate()
{
    //set the Printing order
    //if it's a collate mode then print in reverse order for Home segment
    if (currentStage_ == Stage::Scan_Basic_Print)
    {
        if (intent_->getCollate() == SheetCollate::Collate && intent_->getScanSource() != dune::scan::types::ScanSource::GLASS)
        {
            dune::print::engine::PageOrientation pageOrientation{dune::print::engine::MediaHelper::getMediaOrientation(
                services_.mediaInterface, ticket_->getIntent()->getOutputDestination())};
            
            ticket_->getIntent()->setPrintingOrder(pageOrientation == dune::print::engine::PageOrientation::FACE_UP
                                        ? dune::imaging::types::PrintingOrder::FIRST_PAGE_ON_TOP
                                        : dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);
            
            CHECKPOINTA("CopyConfigurablePipeline: onBuildPipeline set Printing order for MMK job");
        }
    }
}
void CopyConfigurablePipelineBuilder::setReourcesTrueForCollate()
{
    // Override configuration and mark first stage resource as setKeep for Collate jobs.
    if(maxPagesToCollate_ > 0)
    {
        if(collateMode_ != CollateMode::NONE)
        {
            for (auto &proxy : pipelineSections_[0])
            {
                CHECKPOINTA_STR("CopyConfigurablePipelineBuilder: onBuildPipeline: Override setKeep to true for : %s\n", proxy->getResourceServiceId().c_str());
                proxy->setKeep(true);
            }
        }
    }
}

void CopyConfigurablePipelineBuilder::applyPipelinePolicy()
{
    switch (pipelinePolicy_)
    {
        case dune::job::PipelinePolicy::allocate_all_then_start:
            pipelinePolicy(PipelinePolicy::allocate_all_then_start);
            break;
        case dune::job::PipelinePolicy::allocate_and_start:
            pipelinePolicy(PipelinePolicy::allocate_and_start);
            break;
        case dune::job::PipelinePolicy::allocate_only:
            pipelinePolicy(PipelinePolicy::allocate_only);
            break;
        case dune::job::PipelinePolicy::undefined:
            pipelinePolicy(PipelinePolicy::undefined);
            break;
        default:
            pipelinePolicy(PipelinePolicy::allocate_and_start);
    }

    CHECKPOINTA("CopyConfigurablePipelineBuilder: applyPipelinePolicy: PipelinePolicy: %d", pipelinePolicy_);
}

void CopyConfigurablePipelineBuilder::populateJobTicketWithJobMetaInfo(std::shared_ptr<dune::job::IPipeMetaInfo> pipeMetaInfo)
{
    CHECKPOINTC("CopyConfigurablePipelineBuilder::populateJobTicketWithJobMetaInfo() Enter");
    auto jobData = pipeMetaInfo.get()->getJobMetaInfo();
    if (!jobData)
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder::populateJobTicketWithJobMetaInfo(): Error!!! JobData is null. Cannot populate CopyJobTicket with job meta info.");
        return;
    }

    intent_->setInputMediaSizeId(jobData->lastPageMediaSize);
    auto scanCaptureMode = intent_->getScanCaptureMode();
    if (jobData->captureMode == dune::job::CaptureModeType::STANDARD)
    {
        scanCaptureMode = dune::scan::types::ScanCaptureModeType::STANDARD;
    }
    else if (jobData->captureMode == dune::job::CaptureModeType::IDCARD)
    {
        scanCaptureMode = dune::scan::types::ScanCaptureModeType::IDCARD;
    }
    else if (jobData->captureMode == dune::job::CaptureModeType::BOOKMODE)
    {
        scanCaptureMode = dune::scan::types::ScanCaptureModeType::BOOKMODE;
    }
    intent_->setScanCaptureMode(scanCaptureMode);
    CHECKPOINTC("CopyConfigurablePipelineBuilder::populateJobTicketWithJobMetaInfo() scanCaptureMode %d", static_cast<int>(scanCaptureMode));
}

std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> CopyConfigurablePipelineBuilder::getResourceList(
    dune::scan::Jobs::Scan::PipelineSegmentType segmentType)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder::getResourceList()::Entry");
    std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> resourceList;

    for (auto item = copyPipelineConfiguration_->pipelineSegements.begin();
         item != copyPipelineConfiguration_->pipelineSegements.end(); ++item)
    {
        if (item->get()->pipelineSegmentType == segmentType)
        {
            pipelinePolicy_ = item->get()->pipelinePolicy;
            for (auto resource = item->get()->resourceInstanceProxyList.begin();
                 resource != item->get()->resourceInstanceProxyList.end(); ++resource)
            {
                CHECKPOINTA("CopyConfigurablePipelineBuilder::getResourceList()::Entry, %d", resource->get()->resourceId);
                resourceList.push_back(std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>(*(resource->get())));
            }
            break;
        }
    }
    CHECKPOINTA("CopyConfigurablePipelineBuilder::getResourceList()::Exit");
    return resourceList;
}

void CopyConfigurablePipelineBuilder::setPipelineConfig(dune::scan::Jobs::Scan::PipelineBuilderConfigT* pipelineConfig)
{
    assert_msg(pipelineConfig != nullptr,
                   "CopyConfigurablePipelineBuilder::onBuildPipeline()- scanPipeline_ pipline config is null");
    copyPipelineConfiguration_ = pipelineConfig;
}

void CopyConfigurablePipelineBuilder::setupImageImporter(IScanPipeline::PipeQueueInterface data)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupImageImporter onEntry");
    auto imageImporterTicket = std::static_pointer_cast<dune::imaging::Resources::IImageImporterTicket>(
        imageImporterProxy_->getResourceTicket());
    resourceSetupHelper_->setupImageImporter(data.pageDataDequeuer_, 
                                             data.enqueuer_, imageImporterTicket, imageHandler_);
}

bool isStampContentsSet(const std::shared_ptr<ICopyJobIntent>& intent_){
    // Check if stamp contents are set
    bool ret{false};
    ret = (intent_->getStampTopLeft().stampContents.empty() || intent_->getStampTopLeft().stampContents[0]->stampId == dune::imaging::types::StampType::NONE) && 
          (intent_->getStampTopCenter().stampContents.empty() || intent_->getStampTopCenter().stampContents[0]->stampId == dune::imaging::types::StampType::NONE) && 
          (intent_->getStampTopRight().stampContents.empty() || intent_->getStampTopRight().stampContents[0]->stampId == dune::imaging::types::StampType::NONE) && 
          (intent_->getStampBottomLeft().stampContents.empty() || intent_->getStampBottomLeft().stampContents[0]->stampId == dune::imaging::types::StampType::NONE) && 
          (intent_->getStampBottomCenter().stampContents.empty() || intent_->getStampBottomCenter().stampContents[0]->stampId == dune::imaging::types::StampType::NONE) && 
          (intent_->getStampBottomRight().stampContents.empty() || intent_->getStampBottomRight().stampContents[0]->stampId == dune::imaging::types::StampType::NONE); 

    return !ret;
}

bool CopyConfigurablePipelineBuilder::resolveEnabledIfProperty(std::vector<std::string> conditions)
{
    bool duplexInput = intent_->getInputPlexMode() == dune::imaging::types::Plex::DUPLEX;
    bool duplexOutput = intent_->getOutputPlexMode() == dune::imaging::types::Plex::DUPLEX;
    bool idCardJob = intent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD;
    bool nUpJob = intent_->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp;
    bool watermarkJob = intent_->getWatermarkSettings().type != dune::imaging::types::WatermarkType::NONE;
    bool stampJob = isStampContentsSet(intent_);
    bool scanAheadJob = services_.pageAssembler->getResourceService()->getState() != dune::job::ResourceServiceStateType::ALLOCATABLE
                        || services_.printDevice->getResourceService()->getState() != dune::job::ResourceServiceStateType::ALLOCATABLE
                        || intent_->getScanSource() != ScanSource::GLASS;

    bool resourceRequired{false};

    for (auto &condition: conditions) 
    {
        if(condition == "2Up" && intent_->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp)
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder: resolveEnabledIfProperty add 2Up resource");
            resourceRequired = true;
            break;
        }
        else if((condition == "2UpGlass" || condition == "IDCardGlass")  && (intent_->getScanSource() == ScanSource::GLASS) && (idCardJob || nUpJob))
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder: resolveEnabledIfProperty add 2UpORIDCardWithGlass resource");
            resourceRequired = true;
            break;
        }
        else if(condition == "IDCard" && (intent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD))
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder: resolveEnabledIfProperty add 2UpORIDCard resource");
            resourceRequired = true;
            break;
        }
        else if(condition == "Collate" && (collateMode_ == CollateMode::COMPRESSED))
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder: resolveEnabledIfProperty add CollateOR2Up resource");
            resourceRequired = true;
            break;
        }
        else if(condition == "GlassMultiStage" &&(intent_->getScanSource() == ScanSource::GLASS) && (duplexInput || duplexOutput ||
            idCardJob || nUpJob) )
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder: resolveEnabledIfProperty add Glass resource");
            resourceRequired = true;
            break;
        }
        else if((condition == "Watermark") && (watermarkJob || stampJob))
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder: resolveEnabledIfProperty add watermark resource");
            resourceRequired = true;
            break;
        }
        else if (condition == "ScanAhead" && scanAheadJob)
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder: resolveEnabledIfProperty add ScanAhead resource");
            resourceRequired = true;
            break;
        }
        // If not a simulator job add the resources in the pipeline 
        else if (condition == "NotSimJob" && !simJob_)
        {
            CHECKPOINTB("CopyConfigurablePipelineBuilder: resolveEnabledIfProperty add NotSimJob resource");
            resourceRequired = true;
            break;
        }
        else
        {
            // for the case of non simulator job, the pipeline need to be build with 300 DPI
            CHECKPOINTA("CopyConfigurablePipelineBuilder: resolveEnabledIfProperty NOT Valid Condition ");
            if(condition == "NotSimJob" && simJob_)
            {
                intent_->setOutputXResolution(dune::imaging::types::Resolution::E300DPI);
                intent_->setOutputYResolution(dune::imaging::types::Resolution::E300DPI);
            }
        }
    }

    return resourceRequired;
}

void CopyConfigurablePipelineBuilder::updateResourcesTicket()
{
    if(services_.intentsManager)
    {
        std::vector<IIntentsManager::ResourceTicket> resourcesTicket;
        for(auto section : pipelineSections_)
        {
            std::vector<IIntentsManager::ResourceTicket> lastSectionTicket;
            lastSectionTicket = fillResourcesTicket(section);

            resourcesTicket.insert(resourcesTicket.end(),lastSectionTicket.begin(), lastSectionTicket.end());
        }

        IIntentsManager::JobIntent jobIntent;
        jobIntent.PrintingOrder = ticket_->getIntent()->getPrintingOrder();

        services_.intentsManager->updateResourceIntents(jobIntent, resourcesTicket);
    }
}

std::vector<IIntentsManager::ResourceTicket> CopyConfigurablePipelineBuilder::fillResourcesTicket(const ResourceInstanceProxies &resources)
{
    std::vector<IIntentsManager::ResourceTicket> resourcesTicket;
    for (size_t i = 0; i < resources.size(); i++)
    {
        auto resourceType = IIntentsManager::ResourceType::UNDEFINED;

        if(resources[i] ==  bufferingImageRetrieverProxy_)
        {
            resourceType = IIntentsManager::ResourceType::IMAGE_RETRIEVER_BUFFERING;
        }
        else if(resources[i] ==  imageRetrieverProxy_)
        {
            resourceType = IIntentsManager::ResourceType::IMAGE_RETRIEVER_PRINTING;
        }

        else
        {
            resourceType = dune::print::IntentsManagerHelper::convertResourceServiceTypeToIIntentsManagerResourceType(resources[i]->getResourceServiceType());
        }


        IIntentsManager::ResourceTicket resource {resourceType, resources[i]->getResourceTicket()};
        resourcesTicket.push_back(resource);
    }

    return resourcesTicket;
}

void CopyConfigurablePipelineBuilder::setupImageProcessorTicket(IScanPipeline::PipeQueueInterface data)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupImageProcessorTicket - entry");

    // we would need to downcast the resource instance ticket from resource proxy.
    auto imageProcessorTicket = std::static_pointer_cast<dune::imaging::Resources::IImageProcessorTicket>(
        imageProcessorProxy_->getResourceTicket());
    assert_msg( imageProcessorTicket != nullptr , "CopyConfigurablePipelineBuilder: image ProcessorTicket is null");

    std::unique_ptr<dune::imaging::color::IColorEngine> colorEngine =
    services_.colorDirector->createColorEngine(dune::imaging::color::OutputRenderDeviceId::PRINT_DEVICE);
    assert_msg(colorEngine != nullptr, "CopyConfigurablePipelineBuilder: color engine is null");

    std::unique_ptr<dune::imaging::color::IImageColorEngine> imageColorEngine =
        services_.colorDirector->createImageColorEngine(dune::imaging::color::OutputRenderDeviceId::PRINT_DEVICE);
    assert_msg(imageColorEngine != nullptr, "CopyConfigurablePipelineBuilder: image color engine is null");

    dune::imaging::IRasterFormatSelector *rasterFormatSelector = nullptr;
    dune::imaging::IRasterFormatNegotiator *rasterFormatNegotiator = nullptr;
    dune::imaging::IRasterFormatNegotiator      *nextRasterFormatNegotiator = nullptr;
    dune::imaging::IPipelineMemoryClientCreator *imageProcessorMemClientCreator = nullptr;

    // Layout Filter
    if (useLayoutFilter_)
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder: setupImageProcessorTicket: Layout Filter");

        if (pageAssemblerInstanceProxy_ != nullptr)
        {
            nextRasterFormatNegotiator = services_.pageAssembler->getRasterFormatNegotiator();
        }
        else
        {
            nextRasterFormatNegotiator = services_.printDevice->getRasterFormatNegotiator();
        }
        assert_msg(nextRasterFormatNegotiator != nullptr,
                   "CopyConfigurablePipelineBuilder: raster format negotiator is null");
        rasterFormatSelector = services_.imagePersister->getRasterFormatSelector(nextRasterFormatNegotiator);
        assert_msg(rasterFormatSelector != nullptr, "CopyConfigurablePipelineBuilder: raster format selector is null");
        rasterFormatNegotiator = services_.imagePersister->getRasterFormatNegotiator(nextRasterFormatNegotiator);
        assert_msg(rasterFormatNegotiator != nullptr,
                   "CopyConfigurablePipelineBuilder: rasterformat negotiator is null");
        imageProcessorMemClientCreator = services_.imagePersister->getPipelineMemoryClientCreator();
    }

    // MMK , jupiter require image persister memory client
    else if (prePrintConfiguration_ == Product::LFP || currentStage_ == Stage::Scan_Basic_Print)
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder: setupImageProcessorTicket: MMK , jupiter require image persister memory client");
        auto printDeviceRasterFormatNegotiator = services_.printDevice->getRasterFormatNegotiator();
        assert_msg(printDeviceRasterFormatNegotiator != nullptr, "CopyConfigurablePipelineBuilder: raster format negotiator is null");
        rasterFormatSelector = services_.imagePersister->getRasterFormatSelector(printDeviceRasterFormatNegotiator);
        assert_msg(rasterFormatSelector != nullptr, "CopyConfigurablePipelineBuilder: raster format selector is null");
        rasterFormatNegotiator = services_.imagePersister->getRasterFormatNegotiator(printDeviceRasterFormatNegotiator);
        assert_msg(rasterFormatNegotiator != nullptr, "CopyConfigurablePipelineBuilder: rasterformat negotiator is null");
        imageProcessorMemClientCreator = services_.imagePersister->getPipelineMemoryClientCreator();
    }
    // MMK Flatbed duplex and 2up copy require print device memory client
    else if ((copyBasicPipeline_ && currentStage_ == Stage::PrintAllPages ) || hasSharedPaperPath_)
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder: setupImageProcessorTicket: Copy Basic Pipeline /Beam - PrintAllPages");
        rasterFormatSelector = services_.printDevice->getRasterFormatSelector();
        assert(rasterFormatSelector != nullptr);
        rasterFormatNegotiator = services_.printDevice->getRasterFormatNegotiator();
        assert(rasterFormatNegotiator != nullptr);
        imageProcessorMemClientCreator = services_.printDevice->getPipelineMemoryClientCreator();
    }
    // For other pipelines setup page assembler as memory client
    else
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder: setupImageProcessorTicket: Product is Selene or Enterprise type");
        rasterFormatSelector = services_.pageAssembler->getRasterFormatSelector();
        rasterFormatNegotiator = services_.pageAssembler->getRasterFormatNegotiator();
        imageProcessorMemClientCreator = services_.pageAssembler->getPipelineMemoryClientCreator();
    }
    // Set the ImageProcessorTicket
    imageProcessorTicket->setDequeue(data.dequeuer_);
    imageProcessorTicket->setEnqueue(data.enqueuer_);
    imageProcessorTicket->setPipelineMemoryClientCreator(imageProcessorMemClientCreator);
    imageProcessorTicket->setRasterFormatSelector(rasterFormatSelector);
    imageProcessorTicket->setRasterFormatNegotiator(rasterFormatNegotiator);
    imageProcessorTicket->setRenderingRequirements(services_.renderingRequirements);
    imageProcessorTicket->setMediaInterface(services_.mediaInterface);
    imageProcessorTicket->setColorEngine(std::move(colorEngine));
    imageProcessorTicket->setImageColorEngine(std::move(imageColorEngine));

    // Look in the config table what colorspace corresponds to the colorMode and mediaType given.
    dune::imaging::types::IccColorSpace color_space = dune::imaging::types::IccColorSpace::UNKNOWN;
    if (scanPipeline_)
    {
        auto scanCapabilities = scanPipeline_->getScanCapabilitiesInterface();
        if (scanCapabilities)
        {
            scanCapabilities->getColorSpaceFromColorModeAndMediaType(color_space, intent_->getColorMode(), intent_->getOriginalMediaType());
        }
    }
    imageProcessorTicket->setSourceICC(color_space);

    // Set the ImageProcessorIntent
    auto imageProcessorIntent = imageProcessorTicket->getIntent();

    resourceSetup_->setupImageProcessorIntent(imageProcessorIntent, imageProcessorConfig_);
    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupImageProcessorTicket - exit");
}

void CopyConfigurablePipelineBuilder::setupImageProcessorPreview(IScanPipeline::PipeQueueInterface data)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupImageProcessorPreview - entry");

    // we would need to downcast the resource instance ticket from resource proxy.
    std::shared_ptr<dune::imaging::Resources::IImageProcessorTicket> imageProcessorTicket;
    if (imageProcessorPreviewProxy_)
    {
        imageProcessorTicket = std::static_pointer_cast<dune::imaging::Resources::IImageProcessorTicket>(imageProcessorPreviewProxy_->getResourceTicket());
    }
    else
    {
        imageProcessorTicket = std::static_pointer_cast<dune::imaging::Resources::IImageProcessorTicket>(imageProcessorProxy_->getResourceTicket());
    }
    assert( imageProcessorTicket != nullptr );

    std::unique_ptr<dune::imaging::color::IColorEngine> colorEngine =
        services_.colorDirector->createColorEngine(dune::imaging::color::OutputRenderDeviceId::PRINT_DEVICE);
    assert(colorEngine != nullptr);

    std::unique_ptr<dune::imaging::color::IImageColorEngine> imageColorEngine =
        services_.colorDirector->createImageColorEngine(dune::imaging::color::OutputRenderDeviceId::PRINT_DEVICE);
    assert(imageColorEngine != nullptr);

    // Set the ImageProcessorTicket
    imageProcessorTicket->setDequeue(data.dequeuer_);

    dune::imaging::types::IccColorSpace color_space = dune::imaging::types::IccColorSpace::UNKNOWN;
    if (scanPipeline_)
    {
        auto scanCapabilities = scanPipeline_->getScanCapabilitiesInterface();
        if (scanCapabilities)
        {
            scanCapabilities->getColorSpaceFromColorModeAndMediaType(color_space, intent_->getColorMode(), intent_->getOriginalMediaType());
        }
    }
    imageProcessorTicket->setSourceICC(color_space);

    imageProcessorTicket->setMediaInterface(services_.mediaInterface);
    imageProcessorTicket->setColorEngine(std::move(colorEngine));
    imageProcessorTicket->setImageColorEngine(std::move(imageColorEngine));

    // Set the ImageProcessorIntent
    auto imageProcessorIntent = imageProcessorTicket->getIntent();
    resourceSetup_->setupImageProcessorPreviewIntent(imageProcessorIntent, imageProcessorConfig_);

    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupImageProcessorPreview - exit");
}

void CopyConfigurablePipelineBuilder::setupScanDevice(IScanPipeline::PipeQueueInterface data)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupScanDevice - entry");
    auto scanDeviceTicket = std::static_pointer_cast<IScanDeviceTicket>(scanDeviceInstanceProxy_->getResourceTicket());

    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupScanDevice - Output Media Size ID: %d", static_cast<int>(intent_->getOutputMediaSizeId()));

    auto sdIntent = scanDeviceTicket->getIntent();

    //Get job ticket handler and set print intents factory
    auto jobTicket = getJobTicket();
    jobTicket->setPrintIntentsFactory(services_.printIntentsFactory);
    // need to set the jobticket value, so that addPage will set the intents correctly
    if(flatbedDuplexBackSide_ && intent_->getScanSource() == dune::scan::types::ScanSource::GLASS)
    {
        jobTicket->setFlatbedDuplexScanSide(dune::scan::types::DuplexSideEnum::BackSide);
    }
    else
    {
        jobTicket->setFlatbedDuplexScanSide(dune::scan::types::DuplexSideEnum::FrontSide);
    }

    //Provide the scan side information to ResourceSetup
    resourceSetup_->setFlatbedDuplexScanBackSide(flatbedDuplexBackSide_);
    resourceSetup_->setupScanDeviceIntent(sdIntent, scanDeviceConfig_);

    auto defaultMediaSize = (dune::imaging::types::MediaSizeId)services_.mediaAttributes->getColdResetMediaSize();
    if (prescanJob_)
    {
        //In this section a prescan was done and we are attempting to use the edge detection values.
        auto preScanWidth = scanDeviceTicket->getScanDeviceResult()->getPrescannedWidth();
        auto preScanHeight = scanDeviceTicket->getScanDeviceResult()->getPrescannedHeight();
        CHECKPOINTA("CopyConfigurablePipelineBuilder: setupScanDevice - prescanHeight: %d, prescanWidth: %d", (int)preScanHeight, (int)preScanWidth);
        if (preScanWidth == 0 || preScanHeight == 0)
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder: setupScanDevice - ERROR prescan results returned with zero values");
            intent_->setInputMediaSizeId(defaultMediaSize);
        }
        else
        {
            //Create bucketlist for prescan original size
            std::vector<dune::imaging::types::MediaSizeId> AutoSizeBucketListConfig;
            AutoSizeBucketListConfig.push_back(defaultMediaSize);
            AutoSizeBucketListConfig.push_back(MediaSizeId::LEGAL);
            AutoSizeBucketListConfig.push_back(MediaSizeId::A3);
            AutoSizeBucketListConfig.push_back(MediaSizeId::LEDGER);

            intent_->setInputMediaSizeId(ConvertToScanTypeHelper::getClosestMediaSizeInBucketList(AutoSizeBucketListConfig, preScanWidth, preScanHeight, Resolution::E300DPI));
        }
        CHECKPOINTA("CopyConfigurablePipelineBuilder: setupScanDevice - mediaSize bucketized from prescan as: %d", (int)intent_->getInputMediaSizeId());
        sdIntent->setAutoCrop(false);
    }

    scanDeviceTicket->setEnqueueIntf(data.enqueuer_);

    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupScanDevice - exit");
}

void CopyConfigurablePipelineBuilder::setupIPADevice(IScanPipeline::PipeQueueInterface data)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupIPADevice - entry");
    auto ipaDeviceTicket = std::static_pointer_cast<dune::scan::Resources::IIPADeviceTicket>(ipaDeviceInstanceProxy_->getResourceTicket());
    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupIPADevice - after create IPA ticket");
    auto ipaIntent = ipaDeviceTicket->getIntents();
    ipaDeviceTicket->setPipelineMemoryClientCreator(services_.imagePersister->getPipelineMemoryClientCreator());

    resourceSetup_->setupIPADeviceIntent(ipaIntent, ipaDeviceConfig_);
    auto jobTicket = getJobTicket();
    jobTicket->setPrintIntentsFactory(services_.printIntentsFactory);
    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupIPADevice - after set filter settings");

    ipaDeviceTicket->setDequeue(data.dequeuer_);
    ipaDeviceTicket->setEnqueue(data.enqueuer_);
    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupIPADevice - after set enqueuer and dequeuer");

    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupIPADevice - exit");
}

void CopyConfigurablePipelineBuilder::setupMarkingFilter(IScanPipeline::PipeQueueInterface data)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupMarkingFilter - ENTRY");
    auto markingFilterTicket =
        std::static_pointer_cast<IMarkingFilterTicket>(markingFilterInstanceProxy_->getResourceTicket());
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupMarkingFilter after create MF ticket");
    auto mfIntent = markingFilterTicket->getIntent();

    // Configuring the PipelineMemoryClientCreator for the MarkingFilter Rasterizer
    if(pageAssemblerInstanceProxy_ != nullptr)
    {
        CHECKPOINTC("CopyConfigurablePipelineBuilder::setupMarkingFilter - set PageAssembler as memory client for the rasterizer");
        mfIntent->setMemoryClientCreatorForRasterizer(services_.pageAssembler->getPipelineMemoryClientCreator());
    }
    else if(currentStage_ == Stage::Scan_Basic_Print)
    {
        CHECKPOINTC("CopyConfigurablePipelineBuilder::setupMarkingFilter - set ImagePersister as memory client for the rasterizer");
        mfIntent->setMemoryClientCreatorForRasterizer(services_.imagePersister->getPipelineMemoryClientCreator());
    }
    else
    {
        CHECKPOINTC("CopyConfigurablePipelineBuilder::setupMarkingFilter - set PrintDevice as memory client for the rasterizer");
        mfIntent->setMemoryClientCreatorForRasterizer(services_.printDevice->getPipelineMemoryClientCreator());
    }

    resourceSetup_->setupMarkingFilterIntent(mfIntent, markingFilterConfig_);
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupMarkingFilter after set filter settings");
    markingFilterTicket->setDequeueIntf(data.dequeuer_);
    markingFilterTicket->setEnqueueIntf(data.enqueuer_);
    markingFilterTicket->setRasterFormatNegotiator(services_.printDevice->getRasterFormatNegotiator());
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupMarkingFilter after set enqueuer and dequeuer");

    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupMarkingFilter - EXIT");
}

void CopyConfigurablePipelineBuilder::setupLayoutFilter(IScanPipeline::PipeQueueInterface data)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupLayoutFilter - ENTRY");
    auto layoutFilterTicket =
        std::static_pointer_cast<dune::imaging::Resources::ILayoutFilterTicket>(layoutFilterInstanceProxy_->getResourceTicket());
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupLayoutFilter after create LF ticket");
    auto layoutFilterIntent = layoutFilterTicket->getIntent();

    // Configuring the Interfaces for the LayoutFilter
    dune::imaging::IRasterFormatSelector        *rasterFormatSelector = nullptr;
    dune::imaging::IRasterFormatNegotiator      *rasterFormatNegotiator = nullptr;
    dune::imaging::IPipelineMemoryClientCreator *memoryClientCreator = nullptr;
    if (pageAssemblerInstanceProxy_ != nullptr)
    {
        CHECKPOINTC("CopyConfigurablePipelineBuilder::setupLayoutFilter - set interfaces from PageAssembler");
        rasterFormatNegotiator = services_.pageAssembler->getRasterFormatNegotiator();
        memoryClientCreator = services_.pageAssembler->getPipelineMemoryClientCreator();
    }
    else
    {
        CHECKPOINTC("CopyConfigurablePipelineBuilder::setupLayoutFilter - set interfaces from PrintDevice as");
        rasterFormatNegotiator = services_.printDevice->getRasterFormatNegotiator();
        memoryClientCreator = services_.printDevice->getPipelineMemoryClientCreator();
    }
    auto layoutFilterInterfaces = layoutFilterTicket->getInterfaces();
    layoutFilterInterfaces->setRasterFormatNegotiator(rasterFormatNegotiator);
    layoutFilterInterfaces->setPipelineMemoryClientCreator(memoryClientCreator);
    layoutFilterInterfaces->setColorEngine(
        services_.colorDirector->createColorEngine(dune::imaging::color::OutputRenderDeviceId::PRINT_DEVICE));

    resourceSetup_->setupLayoutFilterIntent(layoutFilterIntent, layoutFilterConfig_);
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupLayoutFilter after set filter settings");
    layoutFilterInterfaces->setDequeue(data.dequeuer_);
    layoutFilterInterfaces->setEnqueue(data.enqueuer_);
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupLayoutFilter after set enqueuer and dequeuer");

    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupLayoutFilter - EXIT");
}

void CopyConfigurablePipelineBuilder::setupPageAssembler(IScanPipeline::PipeQueueInterface data)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupPageAssembler - ENTRY");
    auto pageAssemblerTicket =
        std::static_pointer_cast<IPageAssemblerTicket>(pageAssemblerInstanceProxy_->getResourceTicket());

    assert_msg(services_.printDevice->getRasterFormatSelector() != nullptr, "CopyConfigurablePipelineBuilder: print device raster format null");

    pageAssemblerTicket->setDequeue(data.dequeuer_);
    pageAssemblerTicket->setEnqueue(data.enqueuer_);
    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupPageAssembler: set print device as memory client");
    pageAssemblerTicket->setPipelineMemoryClientCreator(services_.printDevice->getPipelineMemoryClientCreator());
    pageAssemblerTicket->setRasterFormatSelector(services_.printDevice->getRasterFormatSelector());
    pageAssemblerTicket->setRasterFormatNegotiator(services_.printDevice->getRasterFormatNegotiator());

    pageAssemblerTicket->setPrintIntentsFactory(services_.printIntentsFactory);

    auto paIntent = pageAssemblerTicket->getIntent();
    if (copyEnterprisePipeline_
        && simJob_ == false
        && (ticket_->getExecutionMode() == dune::job::ExecutionMode::NORMAL)
        && (useImagePersister_ == false)
        && (useImageProcessor_ == false)
        && (useLayoutFilter_ == false))
    {
        paIntent->setBasicCopyMode(true);
        CHECKPOINTA("CopyConfigurablePipelineBuilder: setupPageAssembler BasicCopyMode = true");
    }
    else
    {
        paIntent->setBasicCopyMode(false);
        CHECKPOINTA("CopyConfigurablePipelineBuilder: setupPageAssembler BasicCopyMode = false");
    }
    resourceSetup_->setupPageAssemblerIntent(paIntent, pageAssemblerConfig_);

    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupPageAssembler - EXIT");
}

void CopyConfigurablePipelineBuilder::setupRtpFilterTicket(IScanPipeline::PipeQueueInterface data)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupRtpFilterTicket");
    // we would need to downcast the resource instance ticket from resource proxy.
    auto rtpFilterTicket = std::static_pointer_cast<dune::print::Resources::IRtpFilterTicket>(rtpFilterProxy_->getResourceTicket());

    assert(rtpFilterTicket != nullptr);
    assert_msg(data.dequeuer_ != nullptr, "CopyConfigurablePipelineBuilder: dequeuer is null");
    assert_msg(data.enqueuer_ != nullptr, "CopyConfigurablePipelineBuilder: enqueuer is null");
    // Set the RtpFilterTicket
    rtpFilterTicket->setDequeueIntf(data.dequeuer_);
    rtpFilterTicket->setEnqueueIntf(data.enqueuer_);

    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupRtpFilterTicket Done");
}

void CopyConfigurablePipelineBuilder::setupPrintDevice(IScanPipeline::PipeQueueInterface data)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupPrintDevice - ENTRY");
    auto printDeviceTicket = std::static_pointer_cast<IPrintDeviceTicket>(printDeviceInstanceProxy_->getResourceTicket());
    auto pdIntent = printDeviceTicket->getIntent();

    resourceSetup_->setupPrintDeviceIntent(pdIntent, printDeviceConfig_);

    printDeviceTicket->setImageContainerDequeuer(data.dequeuer_);
    CHECKPOINTA("CopyConfigurablePipelineBuilder: setupPrintDevice - EXIT");
}

void CopyConfigurablePipelineBuilder::setupImagePersister(IScanPipeline::PipeQueueInterface data)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupImagePersister - ENTRY");
    // we would need to downcast the resource instance ticket from resource proxy.
    auto imagePersisterTicket = std::static_pointer_cast<dune::imaging::Resources::IImagePersisterTicket>(imagePersisterProxy_->getResourceTicket());

    imagePersisterTicket->setDequeueIntf(data.dequeuer_);
    imagePersisterTicket->setEnqueueIntf(data.enqueuer_);

    auto imagePersisterIntent = imagePersisterTicket->getIntent();
    //Set the File Format in ImagePersisterIntent based on the file format in CopyPipelineConfiguration CSF
    CHECKPOINTC("CopyConfigurablePipelineBuilder::setupImagePersister File Format %d", (int)copyPipelineConfiguration_->fileFormat);
    imagePersisterIntent->setFileFormat(copyPipelineConfiguration_->fileFormat);
    resourceSetup_->setupImagePersisterIntent(imagePersisterIntent, imagePersisterConfig_); 
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupImagePersister - EXIT");
}

void CopyConfigurablePipelineBuilder::setupBufferingImagePersister(IScanPipeline::PipeQueueInterface data)
{
    auto imagePersisterTicket = std::static_pointer_cast<dune::imaging::Resources::IImagePersisterTicket>(bufferingImagePersisterProxy_->getResourceTicket());

    imagePersisterTicket->setDequeueIntf(data.dequeuer_);
    imagePersisterTicket->setEnqueueIntf(data.enqueuer_);

    auto imagePersisterIntent = imagePersisterTicket->getIntent();
    resourceSetup_->setupBufferingImagePersisterIntent(imagePersisterIntent, imageProcessorConfig_); 
}

void CopyConfigurablePipelineBuilder::setupImageRetriever(IScanPipeline::PipeQueueInterface data)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupImageRetriever - ENTRY");
    // we need to downcast the resource instance ticket from resource proxy.
    auto imageRetrieverTicket = std::static_pointer_cast<dune::imaging::Resources::IImageRetrieverTicket>(
                                                        imageRetrieverProxy_->getResourceTicket());

    assert_msg(data.dequeuer_ != nullptr, "CopyConfigurablePipelineBuilder: dequeuer is null");
    assert_msg(data.enqueuer_ != nullptr, "CopyConfigurablePipelineBuilder: enqueuer is null");
    imageRetrieverTicket->setDequeueInterface(data.dequeuer_);
    imageRetrieverTicket->setEnqueueInterface(data.enqueuer_);
    imageRetrieverTicket->setPrintIntentsFactoryInterface(services_.printIntentsFactory);

    auto imageRetrieverIntent = imageRetrieverTicket->getIntent();
    resourceSetup_->setupImageRetrieverIntent(imageRetrieverIntent, imageRetrieverConfig_);
    if(imageRetrieverIntent->getSequencingParams())
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder::setupImageRetriever ");
        imageRetrieverIntent->getSequencingParams()->printingOrder = printingOrder_;
        if(currentStage_ == Stage::Reprint)
        {
            imageRetrieverIntent->getSequencingParams()->updateDetails = true;
            CHECKPOINTA("CopyConfigurablePipelineBuilder::setupImageRetriever - Reprint");
        }
    }
    imageRetrieverTicket->setPipelineMemoryClient(services_.printDevice->getPipelineMemoryClientCreator());

    if (useLayoutFilter_)
    {
        dune::imaging::IPipelineMemoryClientCreator *memClientCreator{
            pageAssemblerInstanceProxy_ != nullptr ? services_.pageAssembler->getPipelineMemoryClientCreator()
                                                   : services_.printDevice->getPipelineMemoryClientCreator()};
        imageRetrieverTicket->setPipelineMemoryClient(memClientCreator);
        CHECKPOINTC("CopyConfigurablePipelineBuilder::setupImageRetriever useLayoutFilter_, setting up memory client");
    }
    else if (copyEnterprisePipeline_)
    {
        imageRetrieverIntent->setDecompressImage(true);
        imageRetrieverTicket->setPipelineMemoryClient(services_.pageAssembler->getPipelineMemoryClientCreator());
        CHECKPOINTC("CopyConfigurablePipelineBuilder::setupImageRetriever enterprisePipeline, setting up memory client - PageAssembler");
    }
    // For Beam , and multi stage job set image processor as pipeline memory client
    else if (hasSharedPaperPath_ || currentStage_ == Stage::PrintAllPages)
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder::setupImageRetriever - set ImageProcessor as memory client");
        imageRetrieverTicket->setPipelineMemoryClient(services_.imageProcessor->getPipelineMemoryClientCreator());
    }
    else if ((collateMode_ == CollateMode::COMPRESSED || intent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::TwoUp)
            && !copyBasicPipeline_)
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder::setupImageRetriever - set ImageProcessor as memory client");
        imageRetrieverTicket->setPipelineMemoryClient(services_.imageProcessor->getPipelineMemoryClientCreator());
    }

    imageRetrieverIntent->setIsMultiPartJob(isMultiplePrintJob_);
    
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupImageRetriever collateMode_: %d", (uint32_t)collateMode_);

    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupImageRetriever - EXIT");
}

void CopyConfigurablePipelineBuilder::setupBufferingImageRetriever(IScanPipeline::PipeQueueInterface data)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupBufferingImageRetriever - ENTRY");
    auto imageRetrieverTicket = std::static_pointer_cast<dune::imaging::Resources::IImageRetrieverTicket>(bufferingImageRetrieverProxy_->getResourceTicket());

    imageRetrieverTicket->setDequeueInterface(data.dequeuer_);
    imageRetrieverTicket->setEnqueueInterface(data.enqueuer_);
    imageRetrieverTicket->setPipelineMemoryClient(services_.imageProcessor->getPipelineMemoryClientCreator());

    auto imageRetrieverIntent = imageRetrieverTicket->getIntent();
    resourceSetup_->setupBufferingImageRetrieverIntent(imageRetrieverIntent, imageRetrieverDiskBufferingConfig_);
    imageRetrieverTicket->setIntent(imageRetrieverIntent);
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupBufferingImageRetriever - EXIT");
}

void CopyConfigurablePipelineBuilder::setupFinalBufferingImageRetriever(IScanPipeline::PipeQueueInterface data)
{
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupFinalBufferingImageRetriever - ENTRY");
    auto imageRetrieverTicket = std::static_pointer_cast<dune::imaging::Resources::IImageRetrieverTicket>(bufferingFinalSegmentImageRetrieverProxy_->getResourceTicket());

    assert_msg(data.dequeuer_ != nullptr, "CopyConfigurablePipelineBuilder: dequeuer is null");
    assert_msg(data.enqueuer_ != nullptr, "CopyConfigurablePipelineBuilder: enqueuer is null");

    imageRetrieverTicket->setDequeueInterface(data.dequeuer_);
    imageRetrieverTicket->setEnqueueInterface(data.enqueuer_);
    imageRetrieverTicket->setPipelineMemoryClient(services_.imageProcessor->getPipelineMemoryClientCreator());

    auto imageRetrieverIntent = imageRetrieverTicket->getIntent();
    resourceSetup_->setupBufferingImageRetrieverIntent(imageRetrieverIntent, imageRetrieverFinalDiskBufferingConfig_);
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setupFinalBufferingImageRetriever - EXIT");
}

void CopyConfigurablePipelineBuilder::setFirstStage()
{
    bool duplexInput = intent_->getInputPlexMode() == dune::imaging::types::Plex::DUPLEX;
    bool duplexOutput = intent_->getOutputPlexMode() == dune::imaging::types::Plex::DUPLEX;
    bool idCardJob = intent_->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD;
    bool nUpJob = intent_->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp;
    bool flatbedSource = intent_->getScanSource() == dune::scan::types::ScanSource::GLASS;
    bool mdfSource = intent_->getScanSource() == dune::scan::types::ScanSource::MDF;

    CHECKPOINTA("CopyConfigurablePipelineBuilder::setFirstStage - duplexInput: %d", duplexInput);
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setFirstStage - duplexOutput: %d", duplexOutput);
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setFirstStage - idCardJob: %d", idCardJob);
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setFirstStage - nUpJob: %d", nUpJob);
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setFirstStage - flatbedSource: %d, actual scan source: %d", flatbedSource, (uint32_t)intent_->getScanSource());
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setFirstStage - mdfSource: %d", mdfSource);

    CHECKPOINTA("CopyConfigurablePipelineBuilder::setFirstStage - Updating currentStage_ from %d", currentStage_);
    if (ticket_->getExecutionMode() == dune::job::ExecutionMode::RERUN)
    {
        currentStage_ = Stage::Reprint;
    }
    else if (flatbedSource)
    {
        if (duplexInput || duplexOutput || nUpJob || idCardJob)
        {
            currentStage_ = Stage::ScanFirstPage;
        }
        else
        {
            if (intent_->getInputMediaSizeId() == MediaSizeId::ANY && !intent_->getScaleToFitEnabled() && !prescanJob_)
            {
                currentStage_ = Stage::PreScan;
                // DUNE-114562 re-implemented Flatbed prescan in simulator
                if (simJob_)
                {
                    currentStage_ = (copyBasicPipeline_) ? Stage::Scan_Basic_Print : Stage::Scan_PageAssembler_Print;
                    intent_->setInputMediaSizeId(getDefaultMediaSize());
                    CHECKPOINTA("CopyConfigurablePipelineBuilder::setFirstStage - Prescan for sim is not supported");
                }
            }
            else
            {
                currentStage_ = (copyBasicPipeline_) ? Stage::Scan_Basic_Print : Stage::Scan_PageAssembler_Print;
            }
        }
    }
    else if (mdfSource && hasSharedPaperPath_)
    {
        currentStage_ = Stage::ScanPage;
    }
    else //ADF
    {
        currentStage_ = (copyBasicPipeline_) ? Stage::Scan_Basic_Print : Stage::Scan_PageAssembler_Print;
    }
    CHECKPOINTA("CopyConfigurablePipelineBuilder::setFirstStage - to %d", currentStage_);
}

CollateMode CopyConfigurablePipelineBuilder::getCollateMode() const
{
    return collateMode_;
}

// NOT USED CURRENTLY
// void CopyConfigurablePipelineBuilder::setupImagePersisterPreview(IScanPipeline::PipeQueueInterface data)
// {
//     CHECKPOINTA("CopyConfigurablePipelineBuilder::setupImagePersisterPreview - ENTRY");
//     // we would need to downcast the resource instance ticket from resource proxy.
//     auto imagePersisterTicket = std::static_pointer_cast<dune::imaging::Resources::IImagePersisterTicket>(imagePersisterProxy_->getResourceTicket());

//     imagePersisterTicket->setDequeueIntf(data.dequeuer_);
//     imagePersisterTicket->setEnqueueIntf(data.enqueuer_);

//     imagePersisterTicket->setStorePath("/tmp");

//     auto imagePersisterIntent = imagePersisterTicket->getIntent();
//     resourceSetup_->setupImagePersisterPreviewIntent(imagePersisterIntent, imagePersisterConfig_);


//     CHECKPOINTA("CopyConfigurablePipelineBuilder::setupImagePersisterPreview - EXIT");
// }

//The job can be collated only if collate has been selected and if the scan source is ADF
//and the number of copies is greater than 1
void CopyConfigurablePipelineBuilder::setCollateMode()
{
    CHECKPOINTA("setCollateMode: setting MaxCollatePages in ticket %d", maxPagesToCollate_);
    CHECKPOINTA("setCollateMode: Current collate value in ticket %d", (int)(intent_->getCollate() == SheetCollate::Collate));
    ticket_->setMaxCollatePages(maxPagesToCollate_);

    if( intent_->getCollate() == SheetCollate::Collate &&
        intent_->getCopies() > 1
    )
    {
        if(!copyEnterprisePipeline_ && intent_->getScanSource() == ScanSource::GLASS)
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder::setCollateMode Non-Enterprise product and Glass scan source - Not a Collate Job");
            collateMode_ = CollateMode::NONE;
            return;
        }
        else
        {
            #if defined (JPEG_HARDWARE_AVAILABLE)
                CHECKPOINTA("CopyConfigurablePipelineBuilder::setCollateMode - Compressed Collate Job");
                collateMode_ = CollateMode::COMPRESSED;
                return;
            #endif
            CHECKPOINTA("CopyConfigurablePipelineBuilder::setCollateMode - Uncompressed Collate Job");
            collateMode_ = CollateMode::UNCOMPRESSED;
        }
        
    }
    else
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder::setCollateMode - Not a Collate Job");
        collateMode_ = CollateMode::NONE;
    }
}

dune::imaging::types::MediaSizeId CopyConfigurablePipelineBuilder::getDefaultMediaSize()
{
    return (dune::imaging::types::MediaSizeId)services_.mediaAttributes->getColdResetMediaSize();
}

uint32_t CopyConfigurablePipelineBuilder::getPrescannedWidth()
{
    auto scanDeviceTicket = std::static_pointer_cast<IScanDeviceTicket>(scanDeviceInstanceProxy_->getResourceTicket());
    return scanDeviceTicket->getScanDeviceResult()->getPrescannedWidth();
}

uint32_t CopyConfigurablePipelineBuilder::getPrescannedHeight()
{
    auto scanDeviceTicket = std::static_pointer_cast<IScanDeviceTicket>(scanDeviceInstanceProxy_->getResourceTicket());
    return scanDeviceTicket->getScanDeviceResult()->getPrescannedHeight();
}

void CopyConfigurablePipelineBuilder::fillCopyPipelineJobTicketSettings()
{
    if(ticket_)
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder: fillCopyPipelineJobTicketSettings set the properties - entry");
        ticket_->setPreScanJob(prescanJob_);
        ticket_->setDefaultMediaSize(getDefaultMediaSize());
        ticket_->setPrintAlignmentChangeRequired(copyBasicPipeline_);
        auto scanDeviceTicket = std::static_pointer_cast<IScanDeviceTicket>(scanDeviceInstanceProxy_->getResourceTicket());
        if ( scanDeviceTicket->getScanDeviceResult())
        {
            ticket_->setPrescannedHeight(getPrescannedHeight());
            ticket_->setPrescannedWidth(getPrescannedWidth());
            CHECKPOINTA("CopyConfigurablePipelineBuilder::fillCopyPipelineJobTicketSettings - getPrescannedHeight is %d",static_cast<int>(getPrescannedHeight()));
            CHECKPOINTA("CopyConfigurablePipelineBuilder::fillCopyPipelineJobTicketSettings - getPrescannedWidth is %d",static_cast<int>(getPrescannedWidth()));
        }
        CHECKPOINTA("CopyConfigurablePipelineBuilder::fillCopyPipelineJobTicketSettings - isPreScanJob is %d",static_cast<int>(prescanJob_));
        CHECKPOINTA("CopyConfigurablePipelineBuilder::fillCopyPipelineJobTicketSettings - getSegmentType is %d",static_cast<int>(segmentType_));
        CHECKPOINTA("CopyConfigurablePipelineBuilder::fillCopyPipelineJobTicketSettings - getDefaultMediaSize is %d",static_cast<int>(getDefaultMediaSize()));
        CHECKPOINTA("CopyConfigurablePipelineBuilder: fillCopyPipelineJobTicketSettings set the properties - exit");
    }
}

void CopyConfigurablePipelineBuilder::resetAllocatedResources()
{
    if (scanDeviceInstanceProxy_->getState() == ResourceInstanceProxy::StateType::DoneStillAllocated)
    {
        scanDeviceInstanceProxy_->reset();
    }
    if (imagePersisterProxy_->getState() == ResourceInstanceProxy::StateType::DoneStillAllocated)
    {
        imagePersisterProxy_->reset();
    }
    if (imageProcessorProxy_->getState() == ResourceInstanceProxy::StateType::DoneStillAllocated)
    {
        imageProcessorProxy_->reset();
    }
    if (imageRetrieverProxy_->getState() == ResourceInstanceProxy::StateType::DoneStillAllocated)
    {
        imageRetrieverProxy_->reset();
    }
    if (rtpFilterProxy_->getState() == ResourceInstanceProxy::StateType::DoneStillAllocated)
    {
        rtpFilterProxy_->reset();
    }
    if (printDeviceInstanceProxy_->getState() == ResourceInstanceProxy::StateType::DoneStillAllocated)
    {
        printDeviceInstanceProxy_->reset();
    }
}

void CopyConfigurablePipelineBuilder::freeAllocatedResources()
{
    // /* TODO: Copy pipeline should not be calling free directly.
    //    JobFramework is refactoring the code to support cleanup tracked by DUNE-84055
    //    Once done we can remove free.
    // */
    if (scanDeviceInstanceProxy_->getState() == ResourceInstanceProxy::StateType::DoneStillAllocated)
    {
        scanDeviceInstanceProxy_->setKeep(false);
        scanDeviceInstanceProxy_->free();
    }
    if (imagePersisterProxy_->getState() == ResourceInstanceProxy::StateType::DoneStillAllocated)
    {
        imagePersisterProxy_->setKeep(false);
        imagePersisterProxy_->free();
    }
    if (imageProcessorProxy_->getState() == ResourceInstanceProxy::StateType::DoneStillAllocated)
    {
        imageProcessorProxy_->setKeep(false);
        imageProcessorProxy_->free();
    }
    if (imageRetrieverProxy_->getState() == ResourceInstanceProxy::StateType::DoneStillAllocated)
    {
        imageRetrieverProxy_->setKeep(false);
        imageRetrieverProxy_->free();
    }
    if (rtpFilterProxy_->getState() == ResourceInstanceProxy::StateType::DoneStillAllocated)
    {
        rtpFilterProxy_->setKeep(false);
        rtpFilterProxy_->free();
    }
    if (printDeviceInstanceProxy_->getState() == ResourceInstanceProxy::StateType::DoneStillAllocated)
    {
        printDeviceInstanceProxy_->setKeep(false);
        printDeviceInstanceProxy_->free();
    }
    if (bufferingImagePersisterProxy_->getState() == ResourceInstanceProxy::StateType::DoneStillAllocated)
    {
        bufferingImagePersisterProxy_->setKeep(false);
        bufferingImagePersisterProxy_->free();
    }
    if(bufferingImageRetrieverProxy_->getState() == ResourceInstanceProxy::StateType::DoneStillAllocated)
    {
        bufferingImageRetrieverProxy_->setKeep(false);
        bufferingImageRetrieverProxy_->free();
    }

}

bool CopyConfigurablePipelineBuilder::isPreviousResourceStateFailed()
{
    if(pageAssemblerInstanceProxy_ != nullptr)
    {
        auto pageAssemblerTicket = std::static_pointer_cast<IPageAssemblerTicket>(pageAssemblerInstanceProxy_->getResourceTicket());
        if(pageAssemblerTicket->getCompletionState() == CompletionStateType::FAILED)
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder: Previous PageAssembler resource failed");
            return true;
        }
    }

    if(imagePersisterProxy_ != nullptr)
    {
        auto imagePersisterTicket = std::static_pointer_cast<dune::imaging::Resources::IImagePersisterTicket>(imagePersisterProxy_->getResourceTicket());
        if(imagePersisterTicket->getCompletionState() == CompletionStateType::FAILED)
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder: Previous ImagePersister resource failed");
            return true;
        }
    }

    if(imageProcessorProxy_ != nullptr)
    {
        auto imageProcessorTicket = std::static_pointer_cast<dune::imaging::Resources::IImageProcessorTicket>(imageProcessorProxy_->getResourceTicket());
        if(imageProcessorTicket->getCompletionState() == CompletionStateType::FAILED)
        {
            CHECKPOINTA("CopyConfigurablePipelineBuilder: Previous ImageProcessor resource failed");
            return true;
        }
    }
    auto scanDeviceTicket = std::static_pointer_cast<IScanDeviceTicket>(scanDeviceInstanceProxy_->getResourceTicket());
    if ((scanDeviceTicket->getCompletionState() == CompletionStateType::FAILED))
    {
        CHECKPOINTA("CopyConfigurablePipelineBuilder: Previous ScanDevice resource failed");
        return true;
    }
    return false;
}

void CopyConfigurablePipelineBuilder::handlePromptResponse(PromptResponseType responseType, PromptType promptType)
{
    CHECKPOINTC("CopyConfigurablePipelineBuilder::handlePromptResponse - Entry %d", numScanPages_);
    switch(responseType)
    {
        // Ok/Contiue
        case PromptResponseType::Response_01:
        {
            CHECKPOINTC("CopyConfigurablePipelineBuilder::handlePromptResponse Response - Ok");
            switch(promptType)
            {
                case PromptType::MorePagesDetectedForCollate:
                {
                    CHECKPOINTC("CopyConfigurablePipelineBuilder::handlePromptResponse Prompt - MorePagesDetectedForCollate");
                    currentStage_ = (copyBasicPipeline_) ? Stage::Scan_Basic_Print : Stage::Scan_PageAssembler_Print;;
                    ticket_->setJobCompleting(false);
                    isMultiplePrintJob_ = true;
                    break;
                }
                case PromptType::FlatbedDuplexAddPage:
                case PromptType::FlatbedAddPage:
                {
                    CHECKPOINTC("CopyConfigurablePipelineBuilder::handlePromptResponse Prompt - FlatbedAddPage Numner of scan pages: %d", numScanPages_);
                    currentStage_ = Stage::ScanSecondPage;
                    /*Handle Prompt Response is called at the begining of the onBuildPipeline entry.
                     Prompting should be done 1 less time and once limit is reached nextStage should be changed
                     So the current page is scanned*/
                    if (numScanPages_ < static_cast<int>(maxFlatbedDuplexPages_-1)) {
                        scanDeviceInstanceProxy_->setKeep(true);
                        imagePersisterProxy_->setKeep(true);
                    }
                    else {
                        nextStage_ = Stage::PrintAllPages;
                        ticket_->setFirstScanStarted(false);
                        scanDeviceInstanceProxy_->setKeep(false);
                        imagePersisterProxy_->setKeep(false);
                    }
                    break;
                }
                case PromptType::FlatbedSecondPage:
                {
                    CHECKPOINTC("CopyConfigurablePipelineBuilder::handlePromptResponse Prompt - FlatbedSecondPage Numner of scan pages: %d", numScanPages_);
                    if (intent_->getPagesPerSheet() == dune::imaging::types::CopyOutputNumberUpCount::TwoUp &&
                        intent_->getOutputPlexMode() == dune::imaging::types::Plex::DUPLEX &&
                        numScanPages_ < 3)
                    {
                        currentStage_ = Stage::ScanSecondPage;
                        scanDeviceInstanceProxy_->setKeep(true);
                        imagePersisterProxy_->setKeep(true);
                    }
                    else
                    {
                        nextStage_ = Stage::PrintAllPages;
                        ticket_->setFirstScanStarted(false);
                        scanDeviceInstanceProxy_->setKeep(false);
                        imagePersisterProxy_->setKeep(false);
                    }
                    break;
                }
                case PromptType::IdCardSecondSide:
                {
                    nextStage_ = Stage::PrintAllPages;
                    ticket_->setFirstScanStarted(false);
                    scanDeviceInstanceProxy_->setKeep(false);
                    imagePersisterProxy_->setKeep(false);
                    break;
                }

                default:
                    break;
            }
            break;
        }
        //Done
        case PromptResponseType::Response_02:
        {
            if(promptType == PromptType::FlatbedAddPage || promptType == PromptType::FlatbedDuplexAddPage)
            {
                CHECKPOINTC("CopyConfigurablePipelineBuilder::handlePromptResponse Response - Done");
                currentStage_ = Stage::PrintAllPages;
                ticket_->setFirstScanStarted(false);
                /* TODO: Copy pipeline should not be calling free directly.
                   JobFramework is refactoring the code to support cleanup tracked by DUNE-84055
                   Once done we can remove free.
                */
                scanDeviceInstanceProxy_->setKeep(false);
                imagePersisterProxy_->setKeep(false);
                scanDeviceInstanceProxy_->free();
                imagePersisterProxy_->free();
            }
            //For 2 button prompts Response 2 is cancel
            else
            {
                promptCanceled_ = true;
                pipelineSections_.clear();
                jobCompletionState_ = dune::job::CompletionStateType::CANCELED;
                ticket_->setFirstScanStarted(false);
                ticket_->setCompletionState(jobCompletionState_);
                currentStage_ = Stage::Finished;
            }
            break;
        }
        case PromptResponseType::Response_03:
        {
            CHECKPOINTC("CopyConfigurablePipelineBuilder::handlePromptResponse Response -03 - Cancel");
            promptCanceled_ = true;
            pipelineSections_.clear();
            jobCompletionState_ = dune::job::CompletionStateType::CANCELED;
            ticket_->setFirstScanStarted(false);
            ticket_->setCompletionState(jobCompletionState_);

            currentStage_ = Stage::Finished;
            break;
        }
        case PromptResponseType::NoResponse:
        {
            if (promptType != PromptType::MdfEjectPage)
            {
                CHECKPOINTC("CopyConfigurablePipelineBuilder::handlePromptResponse Response - NoResponse");
                promptCanceled_ = true;
                pipelineSections_.clear();
                jobCompletionState_ = dune::job::CompletionStateType::CANCELED;
                ticket_->setFirstScanStarted(false);
                ticket_->setCompletionState(jobCompletionState_);
                currentStage_ = Stage::Finished;
            }
             break;
         }
        default:
            CHECKPOINTC("CopyConfigurablePipelineBuilder::handlePromptResponse Response - None/Unhandled");
            break;
    }
    CHECKPOINTC("CopyConfigurablePipelineBuilder::handlePromptResponse - Exit");
}

dune::scan::Jobs::Scan::CustomBuildPipelineT *CopyConfigurablePipelineBuilder::findSegment(
    const dune::scan::Jobs::Scan::PipelineSegmentType &segment)
{
    auto it = std::find_if(
        copyPipelineConfiguration_->pipelineSegements.begin(), copyPipelineConfiguration_->pipelineSegements.end(),
        [&segment](const std::unique_ptr<dune::scan::Jobs::Scan::CustomBuildPipelineT> &segmentConfig) {
            return segmentConfig->pipelineSegmentType == segment;
        });
    return (it != copyPipelineConfiguration_->pipelineSegements.end()) ? it->get() : nullptr;
}

bool CopyConfigurablePipelineBuilder::isLayoutFilterNeeded(const dune::scan::Jobs::Scan::PipelineSegmentType &segment)
{
    // Find Pipeline Segment
    dune::scan::Jobs::Scan::CustomBuildPipelineT *pipeline{findSegment(segment)};
    if (!pipeline)
    {
        return false;
    }

    // Check Layout Filter is in pipeline segment
    auto it = std::find_if(pipeline->resourceInstanceProxyList.begin(), pipeline->resourceInstanceProxyList.end(),
                           [](const std::unique_ptr<dune::scan::Jobs::Scan::ResourceConfigT> &resource) {
                               return resource->resourceId == dune::scan::Jobs::Scan::ResourceName::LAYOUTFILTER;
                           });
    if (it == pipeline->resourceInstanceProxyList.end())
    {
        return false;
    }

    // Check if LayoutFilter is needed
    return resolveEnabledIfProperty((*it)->enabledIf);
}

}}}}  // namespace dune::copy::Jobs::Copy
