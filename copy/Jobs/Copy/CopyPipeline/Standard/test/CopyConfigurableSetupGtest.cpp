/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyPipelineStandardGtestMain.cpp
 * @date   Mon, 27 Feb 2023 13:43:04 +0530
 * @brief   Configurable Copy Pipeline 
 *
 * (C) Copyright 2023 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyPipelineUwAdapter.h"
#include "gmock/gmock.h"
#include "gtest/gtest.h"

#include "common_debug.h"

#include "ConstraintsGroup.h"
#include "ConvertToScanTypeHelper.h"
#include "CopyConfigurablePipelineBuilder.h"
#include "CopyPipelineStandard.h"
#include "CopyPipelineTestFixture.h"
#include "Fs.h"
#include "GTestConfigHelper.h"
#include "MockICopyAdapter.h"
#include "MockIImagePersister.h"
#include "MockILayoutFilterIntent.h"
#include "MockIMediaAttributes.h"
#include "MockIMediaHandlingMgr.h"
#include "MockIPageAssembler.h"
#include "MockIPrintDevice.h"
#include "MockIPrintIntentsFactory.h"
#include "MockIResourceManagerClient.h"
#include "MockIResourceService.h"
#include "MockICopyJobTicket.h"
#include "IScanPipeline.h"
#include "MockIScanPipelineBuilder.h"

#include "ConvertToScanTypeHelper.h"
#include "Fs.h"
#include "MockIScanDevice.h"
#include "MockIScanPipeline.h"
#include "TestSystemServices.h"
#include "MockIDequeue.h"
#include "MockIEnqueue.h"

using ComponentFlavorUid                = dune::framework::component::ComponentFlavorUid;
using MockIPageAssembler                = dune::imaging::Resources::MockIPageAssembler;
using MockIPrintDevice                  = dune::print::Resources::MockIPrintDevice;
using MockIPrintIntentsFactory          = dune::print::engine::MockIPrintIntentsFactory;
using MockIResourceManagerClient        = dune::job::MockIResourceManagerClient;
using MockIResourceService              = dune::job::MockIResourceService;
using MockIScanDevice                   = dune::scan::Resources::MockIScanDevice;
using MockIPrintMedia                   = dune::print::engine::MockIMedia;
using MockIMediaAttributes              = dune::imaging::asset::MockIMediaAttributes;
using CopyPipelineStandard              = dune::copy::Jobs::Copy::CopyPipelineStandard;
using MockICopyAdapter                  = dune::copy::cdm::MockICopyAdapter;

using TestSystemServices    = dune::framework::component::TestingUtil::TestSystemServices;
// General namespaces
using ComponentFlavorUid    = dune::framework::component::ComponentFlavorUid;
using IComponent            = dune::framework::component::IComponent;
using IComponentManager     = dune::framework::component::IComponentManager;
using SysTrace              = dune::framework::core::dbg::SysTrace;
using CheckpointLevel       = SysTrace::CheckpointLevel;
using SystemServices        = dune::framework::component::SystemServices;

// Mock namespaces
using MockIPageAssembler            = dune::imaging::Resources::MockIPageAssembler;
using MockIImagePersister           = dune::imaging::Resources::MockIImagePersister;
using MockIPrintDevice              = dune::print::Resources::MockIPrintDevice;
using MockIPrintIntentsFactory      = dune::print::engine::MockIPrintIntentsFactory;
using MockIResourceManagerClient    = dune::job::MockIResourceManagerClient;
using MockIResourceService          = dune::job::MockIResourceService;
using MockIScanDevice               = dune::scan::Resources::MockIScanDevice;
using MockIPrintMedia               = dune::print::engine::MockIMedia;
using MockIMediaAttributes          = dune::imaging::asset::MockIMediaAttributes;
using MockIMediaHandlingMgr         = dune::print::mediaHandlingAssets::MockIMediaHandlingMgr;
using MockIScanPipelineBuilder      = dune::scan::Jobs::Scan::MockIScanPipelineBuilder;

using ConvertToScanTypeHelper = dune::scan::types::ConvertToScanTypeHelper;


class FakeCopyConfigurablePipelineBuilder : public dune::copy::Jobs::Copy::CopyConfigurablePipelineBuilder
{

public:

    FakeCopyConfigurablePipelineBuilder(std::shared_ptr<ICopyJobTicket> ticket, const ServicesPackage& services,
                                    bool hasSharedPaperPath, dune::scan::Jobs::Scan::IScanPipeline* scanPipeline,
                                    Product prePrintConfiguration, bool copyBasicPipeline,
                                    const MaxLengthConfig& maxLengthConfig, dune::job::IIntentsManager* intentsManager,
                                    IDateTime* dateTime, bool multiPageSupportedFromFlatbed,
                                    dune::copy::cdm::ICopyAdapter* copyApdater, bool layoutFilterEnabled):
                                    dune::copy::Jobs::Copy::CopyConfigurablePipelineBuilder(ticket, services, hasSharedPaperPath, scanPipeline, 
                                    prePrintConfiguration, copyBasicPipeline, maxLengthConfig, intentsManager, dateTime, multiPageSupportedFromFlatbed, copyApdater, layoutFilterEnabled)
                                {
                                    imagePersisterDiskBufferingConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
                                    imageRetrieverDiskBufferingConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
                                    imageRetrieverFinalDiskBufferingConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
                                    imagePersisterConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
                                    imageRetrieverConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
                                    imageProcessorConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
                                    pageAssemblerConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
                                    markingFilterConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
                                    layoutFilterConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
                                    scanDeviceConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
                                    printDeviceConfig_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();


                                }
    /**
    * @brief Reads the passed segemnt's resource list from config file
    * @return Return list of reosurces.
    */
    std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> getResourceListF(
        dune::scan::Jobs::Scan::PipelineSegmentType segmentType)
        {
            return getResourceList(segmentType);
        }
    
    /**
    * @brief populate the resource details and add them in the resource list with the there setup method
    * @param resourceList pass the resource list
    */
    void populateResourceDetailsF(std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> resourceList)
    {
        populateResourceDetails(resourceList);
    }

    /**
    * @brief setup the scan device ticket for scan resource
    * @param data it has the enqueue and dequeue
    */
    void setupScanDeviceF(IScanPipeline::PipeQueueInterface data)
    {
        setupScanDevice(data);
    }

    /**
    * @brief setup the image processor ticket for image processor resource
    * @param data it has the enqueue and dequeue
    */
    void setupImageProcessorTicketF(IScanPipeline::PipeQueueInterface data)
    {
        setupImageProcessorTicket(data);
    }

    /**
    * @brief setup the marking filter ticket for marking filter resource
    * @param data it has the enqueue and dequeue
    */
    void setupMarkingFilterF(IScanPipeline::PipeQueueInterface data)
    {
        setupMarkingFilter(data);
    }

    /**
     * @brief setup the layout filter ticket for layout filter resource
     * @param data it has the enqueue and dequeue
     */
    void setupLayoutFilterF(IScanPipeline::PipeQueueInterface data)
    {
        setupLayoutFilter(data);
    }

    /**
    * @brief setup the page assembler ticket for page assembler resource
    * @param data it has the enqueue and dequeue
    */
    void setupPageAssemblerF(IScanPipeline::PipeQueueInterface data)
    {
        setupPageAssembler(data);
    }

    /**
    * @brief setup the image persister ticket for image persister resource
    * @param data it has the enqueue and dequeue
    */
    void setupImagePersisterF(IScanPipeline::PipeQueueInterface data)
    {
        setupImagePersister(data);
    }

    /**
    * @brief setup the image retriever ticket for image retriever resource
    * @param data it has the enqueue and dequeue
    */
    void setupImageRetrieverF(IScanPipeline::PipeQueueInterface data)
    {
        setupImageRetriever(data);
    }

    /**
    * @brief setup the buffer image persister ticket for image persiter resource
    * @param data it has the enqueue and dequeue
    */
    void setupBufferingImagePersisterF(IScanPipeline::PipeQueueInterface data)
    {
        setupBufferingImagePersister(data);
    }

    /**
    * @brief setup the buffer image retriever ticket for image retriever resource
    * @param data it has the enqueue and dequeue
    */
    void setupBufferingImageRetrieverF(IScanPipeline::PipeQueueInterface data)
    {
        setupBufferingImageRetriever(data);
    }

    /**
    * @brief setup the final buffering image retriever ticket for image retriever resource
    * @param data it has the enqueue and dequeue
    */
    void setupFinalBufferingImageRetrieverF(IScanPipeline::PipeQueueInterface data)
    {
        setupFinalBufferingImageRetriever(data);
    }

    /**
    * @brief setup the image processor preview ticket for image processor resource
    * @param data it has the enqueue and dequeue
    */
    void setupImageProcessorPreviewF(IScanPipeline::PipeQueueInterface data)
    {
        setupImageProcessorPreview(data);
    }

    /**
    * @brief setup the rtp filter ticket for rtp filter resource
    * @param data it has the enqueue and dequeue
    */
    void setupRtpFilterTicketF(IScanPipeline::PipeQueueInterface data)
    {
        setupRtpFilterTicket(data);
    }

    /**
    * @brief setup the print device ticket for print device resource
    * @param data it has the enqueue and dequeue
    */
    void setupPrintDeviceF(IScanPipeline::PipeQueueInterface data)
    {
        setupPrintDevice(data);
    }

    // /**
    // * @brief set collate mode on the basis of job ticket setting
    // */
    // void setCollateModeF()
    // {
    //     setCollateMode();
    // }

    /**
    * @brief set first stage of the pipeline on the basis of the job ticket setting and configuration
    */
    void setFirstStageF()
    {
        setFirstStage();
    }

    /**
    * @brief fill the copy pipeline set setting in the job ticket, So, it can be used in print intent
    */
    void fillCopyPipelineJobTicketSettingsF()
    {
        fillCopyPipelineJobTicketSettings();
    }

    /**
    * @brief check if previous resource state is failed or not
    * @return return true value if preview resource is failed
    */
    bool isPreviousResourceStateFailedF()
    {
        return isPreviousResourceStateFailed();
    }

    /**
    * @brief reset allocated reources for next stage/segment
    */
    void resetAllocatedResourcesF()
    {
        resetAllocatedResources();
    }

    /**
    * @brief resolve the condition and check if it is supported as per the job ticket, if yes return true
    * @param condition string value of condition
    * @return boolean value
    */
    bool resolveEnabledIfPropertyF(std::vector<std::string> conditions)
    {
        return resolveEnabledIfProperty(conditions);
    }

    /**
    * @brief get pre scanned width from scan device ticket
    * @return return width
    */
    uint32_t getPrescannedWidthF()
    {
        return getPrescannedWidth();
    }

    /**
    * @brief get pre scanned height from scan device ticket
    * @return return height
    */
    uint32_t getPrescannedHeightF()
    {
        return getPrescannedHeight();
    }

    /**
    * @brief update resource ticket by using intent Manager
    */
    void updateResourcesTicketF()
    {
        updateResourcesTicket();
    }

    /**
    * @brief fill resource ticket for each resource type
    * @param resources resource list
    * @return retrun list of the resource ticket for each resource
    */
    std::vector<dune::job::IIntentsManager::ResourceTicket> fillResourcesTicket(const ResourceInstanceProxies &resources)
    {
        return fillResourcesTicket(resources);
    }

    /**
    * @brief handle response from prompt
    * @param responseType response from prompt
    */
    void handlePromptResponseF(PromptResponseType responseType, PromptType promptType)
    {
        handlePromptResponse(responseType, promptType);
    }

    void setJobNameF()
    {
        setJobName();
    }

    void setResourceSetupConfigurationF()
    {
        setResourceSetupConfiguration();
    }

    void setCopyPipelineForNonEnterpriseF(PromptType promptType, PromptResponseType responseType,
                                                   SegmentType segmentType)
                                                   {
                                                         setCopyPipelineForNonEnterprise(promptType, responseType, segmentType);
                                                   }
    

    void freeAllocatedResourcesF()
    {
        freeAllocatedResources();
    }

    void setReourcesTrueForCollateF()
    {
        setReourcesTrueForCollate();
    }

    void setPrintingOrderForCollateF()
    {
        setPrintingOrderForCollate();
    }
    /**
     * @brief Free the kept done and allocated resources 
     */
    void freeDoneAllocatedResourcesF()
    {
        freeDoneAllocatedResources();
    }

    /**
     * @brief Find if a segment is on configuration
     *
     * @param segment Segment to find
     * @return Pointer to the segment if found, false otherwise
     */
    dune::scan::Jobs::Scan::CustomBuildPipelineT* findSegmentF(
        const dune::scan::Jobs::Scan::PipelineSegmentType& segment)
        {
            return findSegment(segment);
        }

    /**
     * @brief Check if Layout Filter is needed for this job
     *
     * @param segment Segment to check if LayoutFilter is needed
     * @return true If LayoutFilter is needed, false otherwise
     */
    bool isLayoutFilterNeededF(const dune::scan::Jobs::Scan::PipelineSegmentType& segment)
    {
        return isLayoutFilterNeeded(segment);
    }

    void setCollateMode(CollateMode collateMode)
    {
        collateMode_ = collateMode;
    }
};



class GivenCopyConfigurableSetupGtest : public GivenCopyPipelineResources
{
    public:
        GivenCopyConfigurableSetupGtest() = default;
        virtual void SetUp() override;

        virtual void TearDown() override;

    protected:

    std::shared_ptr<FakeCopyConfigurablePipelineBuilder> fakePipelineBuilder;
    std::shared_ptr<CopyJobTicket> jobTicket;
    MockIResourceManagerClient                                              mockIResourceManagerClient_;
    MockIImagePersister                                                     mockIImagePersister_;
    MockIPageAssembler                                                      mockIPageAssembler_;
    MockIPrintDevice                                                        mockIPrintDevice_;
    MockIPrintIntentsFactory                                                mockIPrintIntentsFactory_;
    MockIResourceService                                                    mockIResourceService_;
    MockIMediaAttributes                                                    mockIMediaAttributes_;
    MockIScanDevice                                                         mockIScanDevice_;
    MockIScanPipeline                                                       mockIScanPipeline_{};
    MockIPrintMedia                                                         mockIPrintMedia_{};
    MockICopyAdapter                                                        mockICopyAdapter_{};
    dune::copy::Jobs::Copy::CopyPipelineStandard                            * component_;
    TestSystemServices                                                      * systemServices_;
    dune::framework::component::IComponentManager                           * componentManager_;
    std::string                                                             productTestFileName{"./testResources/CopyPipelineStandardMMK.json"};    

    std::shared_ptr<MockIScanDeviceIntent> scanDeviceIntent_ = std::make_shared<MockIScanDeviceIntent>();
    std::shared_ptr<MockIImagePersisterIntent> imagePersisterIntent_ = std::make_shared<MockIImagePersisterIntent>();
    std::shared_ptr<MockIImageRetrieverIntent> imageRetrieverIntent_ = std::make_shared<MockIImageRetrieverIntent>();
    std::shared_ptr<MockIPrintDeviceIntent> printDeviceIntent_ = std::make_shared<MockIPrintDeviceIntent>();
    std::shared_ptr<MockIPageAssemblerIntent> pageAssemblerIntent_ = std::make_shared<MockIPageAssemblerIntent>();
    std::shared_ptr<MockIMarkingFilterIntent> markingFilterIntent_ = std::make_shared<MockIMarkingFilterIntent>();
    std::shared_ptr<MockIMarkingFilterSettings> markingFilterSettings_ = std::make_shared<MockIMarkingFilterSettings>();
    std::shared_ptr<MockILayoutFilterIntent> layoutFilterIntent_ = std::make_shared<MockILayoutFilterIntent>();
    std::shared_ptr<MockILayoutFilterInterfaces> layoutFilterInterfaces_ = std::make_shared<MockILayoutFilterInterfaces>();
    std::shared_ptr<MockIImageProcessorIntent> imageProcessorIntent_ = std::make_shared<MockIImageProcessorIntent>();
    std::shared_ptr<MockIScannerCapabilities> scannerCapabilities_ = std::make_shared<MockIScannerCapabilities>();
    std::shared_ptr<MockIIntentsManager> mockIntentsManager_ = std::make_shared<MockIIntentsManager>();
    std::shared_ptr<dune::scan::Jobs::Scan::ScanPipelineConfigT> scanPipelineConfig_ = std::make_shared<dune::scan::Jobs::Scan::ScanPipelineConfigT>();
    std::shared_ptr<MockIScanPipelineBuilder> scanPipelineBuilder_ = std::make_shared<MockIScanPipelineBuilder>();
    std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> resourceList;
    std::shared_ptr<dune::job::MockIDequeue<ImageContainer>>    mockIDequeue_{nullptr};
    std::shared_ptr<dune::job::MockIEnqueue<ImageContainer>>    mockIEnqueue_{nullptr};
};

void GivenCopyConfigurableSetupGtest::SetUp()
{
    GivenCopyPipelineResources::SetUp();
    services_.imagePersister = static_cast<IImagePersister*>(imagePersister_.get());
    services_.imageProcessor = static_cast<IImageProcessor *>(imageProcessor_.get());
    services_.markingFilterService = static_cast<IMarkingFilter *>(markingFilter_.get());
    services_.layoutFilterService = static_cast<ILayoutFilter *>(layoutFilter_.get());
    services_.rtpFilterService = static_cast<IResourceService*>(rtpFilterService_.get());
    services_.printDevice = static_cast<IPrintDevice*>(printDevice_.get());
    services_.pageAssembler = static_cast<IPageAssembler*>(pageAssembler_.get());

    services_.resourceManager = managerClient_.get();
    services_.scanDeviceService = static_cast<IScanDevice *>(scanDeviceService_.get());
    services_.imageRetrieverService = imageRetrieverService_.get();
    services_.colorDirector = colorDirector_.get();
    services_.mediaAttributes = mediaAttributes_.get();
    services_.mediaInterface = mediaInterface_.get();
    services_.mediaInfo = mediaInfoInterface_.get();
    services_.mediaHandlingSettings = mediaSettingsInterface_.get();
    services_.intentsManager = mockIntentsManager_.get();

    maxLengthConfig_.scanMaxCm = 8000; 

    auto scanDeviceConfig1 = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    scanDeviceConfig1->resourceId = dune::scan::Jobs::Scan::ResourceName::SCANDEVICE;
    scanDeviceConfig1->pipeType = dune::scan::Jobs::Scan::PipeObjectType::IMAGECONTAINER;
    scanDeviceConfig1->jobletBoudary = dune::job::JobletBoundary::UNDEFINED;
    scanDeviceConfig1->isSegmentFirstResource = true;
    scanDeviceConfig1->isPipeQueueRequired = true;
    scanDeviceConfig1->queuingFlag = QueuingFlag::BOTH;
    scanDeviceConfig1->setKeep = true;

    auto imageProcessorConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    imageProcessorConfig->resourceId = dune::scan::Jobs::Scan::ResourceName::IMAGEPROCESSORPREVIEW;
    imageProcessorConfig->pipeType = dune::scan::Jobs::Scan::PipeObjectType::IMAGECONTAINER;
    imageProcessorConfig->jobletBoudary = dune::job::JobletBoundary::UNDEFINED;
    imageProcessorConfig->isSegmentFirstResource = false;
    imageProcessorConfig->isPipeQueueRequired = true;
    imageProcessorConfig->queuingFlag = QueuingFlag::ENQUEUE;
    imageProcessorConfig->setKeep = true;

    scanPipelineConfig_->pipelineBuilderConfig = std::make_unique<dune::scan::Jobs::Scan::PipelineBuilderConfigT>();
    scanPipelineConfig_->pipelineBuilderConfig->previewSettings = std::make_unique<dune::scan::Jobs::Scan::PreviewSettingsT>();
    scanPipelineConfig_->pipelineBuilderConfig->previewSettings->savePreviewMode = true;
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imageProcessorConfig);
    mockIDequeue_ = std::make_shared<MockIDequeue<ImageContainer>>();
    mockIEnqueue_ = std::make_shared<MockIEnqueue<ImageContainer>>();



    //ON_CALL(*scanPipeline_, getResourceList(_)).WillByDefault(Return(resourceList));
    ON_CALL(*mediaInterface_, getMargins(_))
        .WillByDefault(Return(std::tuple<APIResult, Margins>(APIResult::OK, desiredMargins_)));
    ON_CALL(*scanPipeline_, getScanPipelineConfiguration()).WillByDefault(Return(scanPipelineConfig_));
    ON_CALL(*mediaAttributes_, getColdResetMediaSize()).WillByDefault(Return(static_cast<uint32_t>(dune::imaging::types::MediaSizeId::LETTER)));

    ON_CALL(*managerClient_, getResourceClientTicket()).WillByDefault(Return(clientTicket_));
    ON_CALL(*managerClient_, registerResourceClient(_, _))
        .WillByDefault(DoAll(Invoke([this](std::shared_ptr<IResourceClientTicket> t, std::shared_ptr<IResourceClient> c) {
                            resourceClient_ = c;
                        }),
                        Return(agent_)));
    ON_CALL(*managerClient_, requestMemoryAllocationToken(_,_,_,_,_)).WillByDefault(Return(true));

    ON_CALL(*scanDeviceResourceService_, getTicket()).WillByDefault(Return(scanDeviceTicket_));
    ON_CALL(*scanDeviceService_, getResourceService()).WillByDefault(Return(static_cast<IResourceService*>(scanDeviceResourceService_.get())));

    ON_CALL(*imageRetrieverService_, getTicket()).WillByDefault(Return(imageRetrieverTicket_));

    ON_CALL(*markingFilterService_, getTicket()).WillByDefault(Return(markingFilterTicket_));
    ON_CALL(*markingFilter_, getResourceService()).WillByDefault(Return(static_cast<IResourceService*>(markingFilterService_.get())));
    ON_CALL(*markingFilter_, getPipelineMemoryClientCreator()).WillByDefault(Return(markingFilterMemoryClientCreator_.get()));

    ON_CALL(*layoutFilterService_, getTicket()).WillByDefault(Return(layoutFilterTicket_));
    ON_CALL(*layoutFilter_, getResourceService()).WillByDefault(Return(static_cast<IResourceService*>(layoutFilterService_.get())));

    ON_CALL(*pageAssemblerResourceService_, getTicket()).WillByDefault(Return(pageAssemblerTicket_));
    ON_CALL(*pageAssembler_, getResourceService()).WillByDefault(Return(static_cast<IResourceService*>(pageAssemblerResourceService_.get())));
    ON_CALL(*pageAssembler_, getPipelineMemoryClientCreator()).WillByDefault(Return(pageAssemblerMemoryClientCreator_.get()));
    ON_CALL(*pageAssembler_, getRasterFormatNegotiator(_)).WillByDefault(Return(static_cast<MockIRasterFormatNegotiator*>(rasterNegotiator_.get())));
    ON_CALL(*pageAssembler_, getRasterFormatSelector(_)).WillByDefault(Return(static_cast<MockIRasterFormatSelector*>(rasterSelector_.get())));

    ON_CALL(*imagePersisterResourceService_, getTicket()).WillByDefault(Return(imagePersisterTicket_));
    ON_CALL(*imagePersister_, getResourceService()).WillByDefault(Return(static_cast<IResourceService*>(imagePersisterResourceService_.get())));
    ON_CALL(*imagePersister_, getPipelineMemoryClientCreator()).WillByDefault(Return(persisterMemoryClientCreator_.get()));
    ON_CALL(*imagePersister_, getRasterFormatNegotiator(_)).WillByDefault(Return(static_cast<MockIRasterFormatNegotiator*>(rasterNegotiator_.get())));
    ON_CALL(*imagePersister_, getRasterFormatSelector(_)).WillByDefault(Return(static_cast<MockIRasterFormatSelector*>(rasterSelector_.get())));

    ON_CALL(*rtpFilterService_, getTicket()).WillByDefault(Return(rtpFilterTicket_));
    ON_CALL(*rtpFilterTicket_, getResourceServiceId()).WillByDefault(ReturnRef(rtpFilterServiceId_));

    ON_CALL(*printDeviceResourceService_, getTicket()).WillByDefault(Return(printDeviceTicket_));
    ON_CALL(*printDevice_, getResourceService()).WillByDefault(Return(static_cast<IResourceService*>(printDeviceResourceService_.get())));
    ON_CALL(*printDevice_, getRasterFormatNegotiator(_)).WillByDefault(Return(static_cast<MockIRasterFormatNegotiator*>(rasterNegotiator_.get())));
    ON_CALL(*printDevice_, getRasterFormatSelector(_)).WillByDefault(Return(static_cast<MockIRasterFormatSelector*>(rasterSelector_.get())));
    ON_CALL(*printDevice_, getPipelineMemoryClientCreator()).WillByDefault(Return(printDeviceMemoryClientCreator_.get()));

    ON_CALL(*imageProcessorResourceService_, getTicket()).WillByDefault(Return(imageProcessorTicket_));
    ON_CALL(*imageProcessor_, getResourceService())
        .WillByDefault(Return(static_cast<IResourceService *>(imageProcessorResourceService_.get())));
    ON_CALL(*imageProcessor_, getPipelineMemoryClientCreator())
        .WillByDefault(Return(imageProcessorMemoryClientCreator_.get()));

    ON_CALL(*imageProcessorTicket_, getCompletionState()).WillByDefault(Return(CompletionStateType::SUCCESS));
    ON_CALL(*pageAssemblerTicket_, getCompletionState()).WillByDefault(Return(CompletionStateType::SUCCESS));
    ON_CALL(*imagePersisterTicket_ , getCompletionState()).WillByDefault(Return(CompletionStateType::SUCCESS));
    ON_CALL(*scanDeviceTicket_ , getCompletionState()).WillByDefault(Return(CompletionStateType::SUCCESS));


    ON_CALL(*scanDeviceResourceService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::SCAN_DEVICE_SERVICE));
    ON_CALL(*imagePersisterResourceService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::IMAGE_PERSISTER));
    ON_CALL(*rtpFilterService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::RTP_FILTER_SERVICE));
    ON_CALL(*printDeviceResourceService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::PRINT_DEVICE_SERVICE));
    ON_CALL(*imageProcessorResourceService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::IMAGE_PROCESSOR));
    ON_CALL(*pageAssemblerResourceService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::PAGE_ASSEMBLER_SERVICE));
    ON_CALL(*imageRetrieverService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::IMAGE_RETRIEVER));
    ON_CALL(*markingFilterService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::MARKING_FILTER));
    ON_CALL(*layoutFilterService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::LAYOUT_FILTER));


    // Configure Mock ResourceTicket with each ResourceServiceId
    ON_CALL(*scanDeviceTicket_, getResourceServiceId()).WillByDefault(ReturnRef(scanDeviceId_));
    ON_CALL(*imagePersisterTicket_, getResourceServiceId()).WillByDefault(ReturnRef(imagePersisterId_));
    ON_CALL(*imageRetrieverTicket_, getResourceServiceId()).WillByDefault(ReturnRef(imageRetrieverId_));
    ON_CALL(*imageProcessorTicket_, getResourceServiceId()).WillByDefault(ReturnRef(imageProcessorId_));
    ON_CALL(*markingFilterTicket_, getResourceServiceId()).WillByDefault(ReturnRef(markingFilterId_));
    ON_CALL(*layoutFilterTicket_, getResourceServiceId()).WillByDefault(ReturnRef(layoutFilterId_));
    ON_CALL(*pageAssemblerTicket_, getResourceServiceId()).WillByDefault(ReturnRef(pageAssemblerId_));
    ON_CALL(*rtpFilterTicket_, getResourceServiceId()).WillByDefault(ReturnRef(rtpFilterServiceId_));
    ON_CALL(*printDeviceTicket_, getResourceServiceId()).WillByDefault(ReturnRef(printDeviceId_));

    // Setup ScanDeviceTicket
    ON_CALL(*scanDeviceTicket_, getIntent()).WillByDefault(Return(scanDeviceIntent_));

    //Setup ImagePersister Ticket
    ON_CALL(*imagePersisterTicket_, getIntent()).WillByDefault(Return(imagePersisterIntent_));
    //Setup ImageRetriever Ticket
    ON_CALL(*imageRetrieverTicket_, getIntent()).WillByDefault(InvokeWithoutArgs([this]() {
        EXPECT_CALL(*imageRetrieverIntent_, setMediaPointers(mediaInterface_.get(), mediaSettingsInterface_.get(), mediaInfoInterface_.get(),nullptr)).Times(1);
        return imageRetrieverIntent_;
    }));
    ON_CALL(*imagePersisterIntent_, getFileName()).WillByDefault(ReturnRef(defaultString_));
    ON_CALL(*imagePersisterIntent_, getFileType()).WillByDefault(ReturnRef(defaultString_));

    // Setup MarkingFilter Ticket
    ON_CALL(*markingFilterTicket_, getIntent()).WillByDefault(Return(markingFilterIntent_));
    // Setup MarkingFilter Settings
    ON_CALL(*markingFilterIntent_, getFilterSettings()).WillByDefault(Return(markingFilterSettings_));
    // Setup LayoutFilter Ticket
    ON_CALL(*layoutFilterTicket_, getIntent()).WillByDefault(Return(layoutFilterIntent_));
    ON_CALL(*layoutFilterTicket_, getInterfaces()).WillByDefault(Return(layoutFilterInterfaces_));    
    // Setup PageAssembler Ticket
    ON_CALL(*pageAssemblerTicket_, getIntent()).WillByDefault(Return(pageAssemblerIntent_));
    // Setup PrintDevice Ticket
    ON_CALL(*printDeviceTicket_, getIntent()).WillByDefault(Return(printDeviceIntent_));

    ON_CALL(*imageProcessorTicket_, getIntent()).WillByDefault(Return(imageProcessorIntent_));

    ON_CALL(*colorDirector_, createColorEngineProxy(_)).WillByDefault(ReturnNew<MockIColorEngine>());
    ON_CALL(*colorDirector_, createImageColorEngineProxy(_)).WillByDefault(ReturnNew<MockIImageColorEngine>());

    ON_CALL(*scanPipeline_, createScanPipelineBuilder()).WillByDefault(Return(scanPipelineBuilder_));
    jobTicket = std::make_shared<CopyJobTicket>();

    systemServices_ = new TestSystemServices();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyPipelineStandardConfig.fbs", "./testResources/CopyPipelineStandardMMK.json");
}

void GivenCopyConfigurableSetupGtest::TearDown()
{
    delete systemServices_;
    GivenCopyPipelineResources::TearDown();
}

TEST_F(GivenCopyConfigurableSetupGtest, WhenSetJobNameIsCalledForHomepro_ThenJobNameIsSet)
{
    jobTicket->setPrePrintConfiguration(Product::HOME_PRO);
    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, false, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);
    fakePipelineBuilder->setJobNameF();
    EXPECT_EQ(jobTicket->getJobName(), "Copy");
    

    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD); 
    fakePipelineBuilder->setJobNameF();
    EXPECT_EQ(jobTicket->getJobName(), "IDCardCopy");
}

TEST_F(GivenCopyConfigurableSetupGtest, WhenSetJobNameIsCalledForEnterpriseLFP_ThenJobNameIsSet)
{
    jobTicket->setPrePrintConfiguration(Product::ENTERPRISE);
    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);
    fakePipelineBuilder->setJobNameF();
    EXPECT_EQ(jobTicket->getJobName(), "");

    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD); 
    fakePipelineBuilder->setJobNameF();
    EXPECT_EQ(jobTicket->getJobName(), "");

    jobTicket->setPrePrintConfiguration(Product::LFP);
    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::ENTERPRISE, false, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);
    fakePipelineBuilder->setJobNameF();
    EXPECT_EQ(jobTicket->getJobName(), "");

    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD); 
    fakePipelineBuilder->setJobNameF();
    EXPECT_EQ(jobTicket->getJobName(), "");
}

TEST_F(GivenCopyConfigurableSetupGtest, WhenSetupScanDeviceIsCalledForProSMB_ScanExtentAreSetCorrectly)
{
    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);

    uint32_t xExtentValue;
    uint32_t yExtentValue;
    EXPECT_CALL(*scanDeviceIntent_, setXExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &xExtentValue](uint32_t value) -> void {

                xExtentValue = value;

            }));

    EXPECT_CALL(*scanDeviceIntent_, setYExtent(_))

        .WillRepeatedly(

            testing::Invoke([this, &yExtentValue](uint32_t value) -> void {

                yExtentValue = value;

            }));

    EXPECT_CALL(*scanDeviceIntent_, getXExtent())

        .WillRepeatedly(

            testing::Invoke([this, &xExtentValue]() -> uint32_t {

                return xExtentValue;

            }));

    EXPECT_CALL(*scanDeviceIntent_, getYExtent())

        .WillRepeatedly(

            testing::Invoke([this, &yExtentValue]() -> uint32_t {

                return yExtentValue;

            }));

    fakePipelineBuilder->setupScanDeviceF({mockIEnqueue_, mockIDequeue_});

    EXPECT_EQ(xExtentValue, 2432);
    EXPECT_EQ(yExtentValue, 3182);
    
    jobTicket->getIntent()->setInputMediaSizeId(MediaSizeId::LEGAL);
    fakePipelineBuilder->setupScanDeviceF({mockIEnqueue_, mockIDequeue_});

    EXPECT_EQ(xExtentValue, 2432);
    EXPECT_EQ(yExtentValue, 4082);
}

TEST_F(GivenCopyConfigurableSetupGtest, WhenHomeSmbIsConfiguredWithDuplexMode_ImageRetrieverSetDuplexIsSetTrue)
{
    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);
    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);

    EXPECT_CALL(*imageRetrieverIntent_, setDuplexJob(true)).Times(1);
    fakePipelineBuilder->setupImageRetrieverF({mockIEnqueue_, mockIDequeue_});
    
}

TEST_F(GivenCopyConfigurableSetupGtest, WhenHomeSmbIsConfiguredWith2upGlass_RotationIsNotSet)
{
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);

    // No rotation
    EXPECT_CALL(*layoutFilterIntent_, setImageRotation(_))
        .WillRepeatedly(Invoke([](const dune::imaging::types::RotationCW& rotation) -> void {
            EXPECT_EQ(dune::imaging::types::RotationCW::ROTATE_0, rotation);
        }));

    fakePipelineBuilder->setupLayoutFilterF({mockIEnqueue_, mockIDequeue_});
}

TEST_F(GivenCopyConfigurableSetupGtest, WhenHomeSmbIsConfiguredWith2upADF_PaddingIsApplied)
{
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);
    jobTicket->setStorePath("/tmp");

    dune::imaging::Resources::SpecificPadding specificPadding;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificPadding(_))

        .WillRepeatedly(

            testing::Invoke([this, &specificPadding](dune::imaging::Resources::SpecificPadding value) -> void {

                specificPadding = value;

            }));

    dune::imaging::Resources::SpecificRotation specificRotation;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &specificRotation](dune::imaging::Resources::SpecificRotation value) -> void {

                specificRotation = value;

            }));

    fakePipelineBuilder->setupImageProcessorTicketF({mockIEnqueue_, mockIDequeue_});
}

TEST_F(GivenCopyConfigurableSetupGtest, WhenHomeSmbIsConfiguredWith2upGlass_RotationIsNotApplied)
{
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);

    jobTicket->setStorePath("/tmp");

    dune::imaging::Resources::SpecificPadding specificPadding;

    EXPECT_CALL(*imageProcessorIntent_, setSpecificRotation(_)).Times(0);

    fakePipelineBuilder->setupImageProcessorTicketF({mockIEnqueue_, mockIDequeue_});
}

TEST_F(GivenCopyConfigurableSetupGtest, WhenHomeSmbIsConfiguredWith1upDuplex_CheckDuplexRoationApplied)
{
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::OneUp);
    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);
    jobTicket->setStorePath("/tmp");

    bool checkDuplexRotation;

    EXPECT_CALL(*imageRetrieverIntent_, setCheckDuplexRotation(_))

        .WillRepeatedly(

            testing::Invoke([this, &checkDuplexRotation](bool value) -> void {

                checkDuplexRotation = value;

            }));

    fakePipelineBuilder->setupImageRetrieverF({mockIEnqueue_, mockIDequeue_});

    EXPECT_EQ(checkDuplexRotation, false);
}

TEST_F(GivenCopyConfigurableSetupGtest, WhenHomeSmbIsConfiguredWithMultipleCopies_CorrectCollateAndUncollateCopiesSet)
{
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Uncollate);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setCopies(2);

    jobTicket->setStorePath("/tmp");
    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);

    uint32_t collationCopies;
    uint32_t uncollationCopies;
    bool perfromSequenceOperation;
    EXPECT_CALL(*imageRetrieverIntent_, setSequencingParams(_))

        .WillRepeatedly(

            testing::Invoke([this, &perfromSequenceOperation, &collationCopies, &uncollationCopies](
                                std::shared_ptr<dune::imaging::Resources::SequencingParams> sequencingParams) -> void {
                perfromSequenceOperation = (sequencingParams != nullptr);
                collationCopies = sequencingParams ? sequencingParams->collationCopies : 0;
                uncollationCopies = sequencingParams ? sequencingParams->uncollationCopies : 0;
            }));

    fakePipelineBuilder->setupImageRetrieverF({mockIEnqueue_, mockIDequeue_});

    EXPECT_EQ(collationCopies,   1);
    EXPECT_EQ(uncollationCopies, 2);

}

TEST_F(GivenCopyConfigurableSetupGtest, WhenHomeSmbADFMultipleCopies2upIsPerformed_CorrectCollateAndUncollateCopiesSet)
{
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Uncollate);
    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);

    // Expectations
    EXPECT_CALL(*layoutFilterIntent_, setSequencingParams(_))
        .WillRepeatedly(Invoke([](const dune::imaging::Resources::LayoutSequencingParams& sequencingParams) -> void {
            EXPECT_EQ(1, sequencingParams.collationCopies);
            EXPECT_EQ(2, sequencingParams.uncollationCopies);
            EXPECT_EQ(0, sequencingParams.pagesNeededToSequence);
            EXPECT_EQ(false, sequencingParams.waitForSheet);
            EXPECT_EQ(false, sequencingParams.updateDetails);
            EXPECT_EQ(2, sequencingParams.imagesPerSheet);
        }));
    EXPECT_CALL(*layoutFilterIntent_, setNupLayout(_))
        .WillRepeatedly(Invoke([](const dune::imaging::types::NUpParams nUpParams) -> void {
            EXPECT_EQ(dune::imaging::types::NumberUp::TWO_UP, nUpParams.getMode());
        }));
    EXPECT_CALL(*layoutFilterIntent_, setImageRotation(_))
        .WillRepeatedly(Invoke([](const dune::imaging::types::RotationCW& rotation) -> void {
            EXPECT_EQ(dune::imaging::types::RotationCW::ROTATE_0, rotation);
        }));

    fakePipelineBuilder->setupLayoutFilterF({mockIEnqueue_, mockIDequeue_});

}

TEST_F(GivenCopyConfigurableSetupGtest, WhenHomeSmbADFMultipleCopies2upIsPerformed_WhiteSpaceIgnoreSet)
{
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::OneUp);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Uncollate);
    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);

    bool ignoreWhiteSpaceValue = false;
    EXPECT_CALL(*imageProcessorIntent_, setIgnoreWhitespaceAdd(_))
        .WillOnce(
            testing::Invoke([this, &ignoreWhiteSpaceValue](bool value) -> void {

                ignoreWhiteSpaceValue = value;

            }));

    fakePipelineBuilder->setCollateMode(CollateMode::COMPRESSED);
    fakePipelineBuilder->setupImageProcessorTicketF({mockIEnqueue_, mockIDequeue_});
    EXPECT_EQ(ignoreWhiteSpaceValue, true);
}


TEST_F(GivenCopyConfigurableSetupGtest, WhenHomeSmbADF2upIsPerformed_correctMFRasterizerMemoryClientIsSet)
{
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;

    EXPECT_CALL(*layoutFilterInterfaces_, setPipelineMemoryClientCreator(_))

        .WillRepeatedly(

            testing::Invoke(
                [this, &pipelineMemoryClientCreator](
                    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {
                    pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;
                }));

    fakePipelineBuilder->setupLayoutFilterF({mockIEnqueue_, mockIDequeue_});
    EXPECT_EQ(printDeviceMemoryClientCreator_.get(), pipelineMemoryClientCreator);
}

TEST_F(GivenCopyConfigurableSetupGtest, WhenSetupImageProcessorIsCalledAndCapabilitiesIsNullptr_ThenIccIsUnknown)
{
    EXPECT_CALL(*scanPipeline_, getScanCapabilitiesInterface()).WillOnce(Return(nullptr));
    EXPECT_CALL(*imageProcessorTicket_, setSourceICC(dune::imaging::types::IccColorSpace::UNKNOWN)).Times(1);

    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);
    fakePipelineBuilder->setupImageProcessorTicketF({mockIEnqueue_, mockIDequeue_});
}

TEST_F(GivenCopyConfigurableSetupGtest, WhenSetupImageProcessorIsCalledAndCapabilitiesExistButReturnUknownIcc_ThenIccIsUnknown)
{
    auto iccColorSpaceExpected = dune::imaging::types::IccColorSpace::UNKNOWN;
    EXPECT_CALL(*scannerCapabilities_,getColorSpaceFromColorModeAndMediaType(_,_,_)).WillOnce(
        testing::Invoke(
            [this, &iccColorSpaceExpected] (
                dune::imaging::types::IccColorSpace& iccColorSpace,
                dune::imaging::types::ColorMode colorMode, 
                dune::scan::types::OriginalMediaType mediaType) -> APIResult 
            {
                iccColorSpace = iccColorSpaceExpected;
                return APIResult::OK;
            }));
    EXPECT_CALL(*scanPipeline_, getScanCapabilitiesInterface()).WillOnce(Return(static_cast<dune::scan::scanningsystem::IScannerCapabilities*>(scannerCapabilities_.get())));
    EXPECT_CALL(*imageProcessorTicket_, setSourceICC(iccColorSpaceExpected)).Times(1);

    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);
    fakePipelineBuilder->setupImageProcessorTicketF({mockIEnqueue_, mockIDequeue_});
}

TEST_F(GivenCopyConfigurableSetupGtest, WhenSetupImageProcessorIsCalledAndCapabilitiesExist_ThenIccIsTheExpected)
{
    auto iccColorSpaceExpected = dune::imaging::types::IccColorSpace::SRGB;
    EXPECT_CALL(*scannerCapabilities_,getColorSpaceFromColorModeAndMediaType(_,_,_)).WillOnce(
        testing::Invoke(
            [this, &iccColorSpaceExpected] (
                dune::imaging::types::IccColorSpace& iccColorSpace,
                dune::imaging::types::ColorMode colorMode, 
                dune::scan::types::OriginalMediaType mediaType) -> APIResult 
            {
                iccColorSpace = iccColorSpaceExpected;
                return APIResult::OK;
            }));
    EXPECT_CALL(*scanPipeline_, getScanCapabilitiesInterface()).WillOnce(Return(static_cast<dune::scan::scanningsystem::IScannerCapabilities*>(scannerCapabilities_.get())));
    EXPECT_CALL(*imageProcessorTicket_, setSourceICC(iccColorSpaceExpected)).Times(1);

    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);
    fakePipelineBuilder->setupImageProcessorTicketF({mockIEnqueue_, mockIDequeue_});
}

TEST_F(GivenCopyConfigurableSetupGtest, WhenSetupImageProcessorPreviewIsCalledAndCapabilitiesIsNullptr_ThenIccIsUnknown)
{
    EXPECT_CALL(*scanPipeline_, getScanCapabilitiesInterface()).WillOnce(Return(nullptr));
    EXPECT_CALL(*imageProcessorTicket_, setSourceICC(dune::imaging::types::IccColorSpace::UNKNOWN)).Times(1);

    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);
    fakePipelineBuilder->setupImageProcessorPreviewF({mockIEnqueue_, mockIDequeue_});
}

TEST_F(GivenCopyConfigurableSetupGtest, WhenSetupImageProcessorPreviewIsCalledAndCapabilitiesExistButReturnUknownIcc_ThenIccIsUnknown)
{
    auto iccColorSpaceExpected = dune::imaging::types::IccColorSpace::UNKNOWN;
    EXPECT_CALL(*scannerCapabilities_,getColorSpaceFromColorModeAndMediaType(_,_,_)).WillOnce(
        testing::Invoke(
            [this, &iccColorSpaceExpected] (
                dune::imaging::types::IccColorSpace& iccColorSpace,
                dune::imaging::types::ColorMode colorMode, 
                dune::scan::types::OriginalMediaType mediaType) -> APIResult 
            {
                iccColorSpace = iccColorSpaceExpected;
                return APIResult::OK;
            }));
    EXPECT_CALL(*scanPipeline_, getScanCapabilitiesInterface()).WillOnce(Return(static_cast<dune::scan::scanningsystem::IScannerCapabilities*>(scannerCapabilities_.get())));
    EXPECT_CALL(*imageProcessorTicket_, setSourceICC(iccColorSpaceExpected)).Times(1);

    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);
    fakePipelineBuilder->setupImageProcessorPreviewF({mockIEnqueue_, mockIDequeue_});
}

TEST_F(GivenCopyConfigurableSetupGtest, WhenSetupImageProcessorPreviewIsCalledAndCapabilitiesExist_ThenIccIsTheExpected)
{
    auto iccColorSpaceExpected = dune::imaging::types::IccColorSpace::SRGB;
    EXPECT_CALL(*scannerCapabilities_,getColorSpaceFromColorModeAndMediaType(_,_,_)).WillOnce(
        testing::Invoke(
            [this, &iccColorSpaceExpected] (
                dune::imaging::types::IccColorSpace& iccColorSpace,
                dune::imaging::types::ColorMode colorMode, 
                dune::scan::types::OriginalMediaType mediaType) -> APIResult 
            {
                iccColorSpace = iccColorSpaceExpected;
                return APIResult::OK;
            }));
    EXPECT_CALL(*scanPipeline_, getScanCapabilitiesInterface()).WillOnce(Return(static_cast<dune::scan::scanningsystem::IScannerCapabilities*>(scannerCapabilities_.get())));
    EXPECT_CALL(*imageProcessorTicket_, setSourceICC(iccColorSpaceExpected)).Times(1);

    fakePipelineBuilder = std::make_shared<FakeCopyConfigurablePipelineBuilder>(jobTicket, services_, false, scanPipeline_.get(), Product::HOME_PRO, true, maxLengthConfig_, mockIntentsManager_.get(), systemServices_->dateTime_, false, &mockICopyAdapter_, false);
    fakePipelineBuilder->setupImageProcessorPreviewF({mockIEnqueue_, mockIDequeue_});
}