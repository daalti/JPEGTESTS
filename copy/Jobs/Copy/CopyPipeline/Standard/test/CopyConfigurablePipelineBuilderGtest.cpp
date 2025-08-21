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
#include "MockIResourceSetupHelper.h"

#include "ConvertToScanTypeHelper.h"
#include "Fs.h"
#include "MockIScanDevice.h"
#include "MockIScanPipeline.h"
#include "TestSystemServices.h"
#include "PageData.h"

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
using PageData                          = dune::imaging::pipeobjects::PageData;   

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
using MockIResourceSetupHelper       = dune::scan::Jobs::Scan::MockIResourceSetupHelper;

using ConvertToScanTypeHelper = dune::scan::types::ConvertToScanTypeHelper;

class GivenANewCopyPipelineStandard : public GivenCopyPipelineResources
{
  public:

    GivenANewCopyPipelineStandard() : component_(nullptr), systemServices_(nullptr), componentManager_(nullptr) {};

    virtual void SetUp() override;

    virtual void TearDown() override;

  protected:
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
    std::shared_ptr<MockIResourceSetupHelper> resourceSetupHelper_ = std::make_shared<MockIResourceSetupHelper>();
    std::shared_ptr<MockIIPADeviceIntents> ipaDeviceIntent_ = std::make_shared<MockIIPADeviceIntents>();
    std::shared_ptr<MockIImageImporterIntents> imageImporterIntent_ = std::make_shared<MockIImageImporterIntents>();
    std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> resourceList;                    
};

void GivenANewCopyPipelineStandard::SetUp()
{
    
    services_.imagePersister = static_cast<IImagePersister*>(imagePersister_.get());
    services_.imageProcessor = static_cast<IImageProcessor *>(imageProcessor_.get());
    services_.markingFilterService = static_cast<IMarkingFilter *>(markingFilter_.get());
    services_.layoutFilterService = static_cast<ILayoutFilter *>(layoutFilter_.get());
    services_.rtpFilterService = static_cast<IResourceService*>(rtpFilterService_.get());
    services_.printDevice = static_cast<IPrintDevice*>(printDevice_.get());
    services_.pageAssembler = static_cast<IPageAssembler*>(pageAssembler_.get());
    services_.ipaDeviceService = static_cast<IIPADevice *>(ipaDevice_.get());
    services_.imageImporter = static_cast<IImageImporter *>(imageImporter_.get());

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

    ON_CALL(*imageImporter_, getResourceService())
        .WillByDefault(Return(static_cast<IResourceService *>(imageImporterResourceService_.get())));
    
    ON_CALL(*ipaDevice_, getResourceService())
        .WillByDefault(Return(static_cast<IResourceService *>(ipaDeviceResourceService_.get())));
    
    ON_CALL(*ipaDeviceResourceService_, getTicket()).WillByDefault(Return(ipaDeviceTicket_));
    ON_CALL(*imageImporterResourceService_, getTicket()).WillByDefault(Return(imageImporterTicket_));

    ON_CALL(*imageProcessorTicket_, getCompletionState()).WillByDefault(Return(CompletionStateType::SUCCESS));
    ON_CALL(*pageAssemblerTicket_, getCompletionState()).WillByDefault(Return(CompletionStateType::SUCCESS));
    ON_CALL(*imagePersisterTicket_ , getCompletionState()).WillByDefault(Return(CompletionStateType::SUCCESS));
    ON_CALL(*scanDeviceTicket_ , getCompletionState()).WillByDefault(Return(CompletionStateType::SUCCESS));
    ON_CALL(*ipaDeviceTicket_ , getCompletionState()).WillByDefault(Return(CompletionStateType::SUCCESS));
    ON_CALL(*imageImporterTicket_, getCompletionState()).WillByDefault(Return(CompletionStateType::SUCCESS));


    ON_CALL(*scanDeviceResourceService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::SCAN_DEVICE_SERVICE));
    ON_CALL(*imagePersisterResourceService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::IMAGE_PERSISTER));
    ON_CALL(*rtpFilterService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::RTP_FILTER_SERVICE));
    ON_CALL(*printDeviceResourceService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::PRINT_DEVICE_SERVICE));
    ON_CALL(*imageProcessorResourceService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::IMAGE_PROCESSOR));
    ON_CALL(*pageAssemblerResourceService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::PAGE_ASSEMBLER_SERVICE));
    ON_CALL(*imageRetrieverService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::IMAGE_RETRIEVER));
    ON_CALL(*markingFilterService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::MARKING_FILTER));
    ON_CALL(*layoutFilterService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::LAYOUT_FILTER));
    ON_CALL(*ipaDeviceResourceService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::IPA_DEVICE));
    ON_CALL(*imageImporterResourceService_ , getResourceServiceType()).WillByDefault(Return(dune::job::ResourceServiceType::IMAGE_IMPORTER));


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
    ON_CALL(*ipaDeviceTicket_, getResourceServiceId()).WillByDefault(ReturnRef(ipaDeviceId_));
    ON_CALL(*imageImporterTicket_, getResourceServiceId()).WillByDefault(ReturnRef(imageImporterId_));

    // Setup ScanDeviceTicket
    ON_CALL(*scanDeviceTicket_, getIntent()).WillByDefault(Return(scanDeviceIntent_));
    ON_CALL(*imageImporterTicket_, getIntents()).WillByDefault(Return(imageImporterIntent_));

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

    ON_CALL(*ipaDeviceTicket_, getIntents()).WillByDefault(Return(ipaDeviceIntent_));    

    ON_CALL(*colorDirector_, createColorEngineProxy(_)).WillByDefault(ReturnNew<MockIColorEngine>());
    ON_CALL(*colorDirector_, createImageColorEngineProxy(_)).WillByDefault(ReturnNew<MockIImageColorEngine>());

    ON_CALL(*scanPipeline_, createScanPipelineBuilder()).WillByDefault(Return(scanPipelineBuilder_));
    ON_CALL(*scanPipeline_, createCommonResourceSetupHelper()).WillByDefault(Return(resourceSetupHelper_));

    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(Return(dune::scan::Jobs::Scan::ScanStage::NONE));
    // Create pipequeue and resource list.
    ON_CALL(*scanPipeline_, createPipeQueuesAndResourceList(_, _, _, _, _, _, _, _))
        .WillByDefault(Invoke(
            [&](std::vector<std::pair<dune::scan::Jobs::Scan::ResourceName, dune::scan::Jobs::Scan::IScanPipeline::ResourceDetails>>
                                                                                 resourceList,
                std::vector<std::vector<std::shared_ptr<dune::job::IResourceInstanceProxy>>> &resourceProxySections,
                std::vector<std::shared_ptr<dune::job::IPipeQueueCancel>> &      pipeQueues,
                std::map<dune::scan::Jobs::Scan::ResourceName, std::shared_ptr<dune::job::PipeQueue<ImageContainer>>>
                &persistedResources,
                std::function<void(std::shared_ptr<dune::job::IDequeue<ImageContainer>>)> func, std::string dataStore,
                std::string &persistedPath, std::shared_ptr<dune::job::IJobTicket> jobTicket) {

                std::shared_ptr<dune::job::IEnqueue<ImageContainer>>                                      lastEnqueuer = nullptr;
                std::shared_ptr<dune::job::IDequeue<ImageContainer>>                                      lastDequeuer = nullptr;
                std::shared_ptr<dune::job::IEnqueue<ImageContainer>>                                      enqueuer = nullptr;
                std::shared_ptr<dune::job::IDequeue<ImageContainer>>                                      dequeuer = nullptr;
                std::shared_ptr<dune::job::PipeQueue<ImageContainer>> pipeQueue;
                std::shared_ptr<dune::job::IDequeue<PageData>>                                            lastPageDataDequeuer = nullptr;

                for (auto item = resourceList.begin(); item != resourceList.end(); ++item)
                {
                    if(item->second.resourceData->reset)
                    {
                        item->second.resourceInstanceProxy->reset();
                    }
                    if (item->second.resourceData->jobletBoudary != dune::job::JobletBoundary::UNDEFINED)
                    {
                        item->second.resourceInstanceProxy->setJobletBoundary(item->second.resourceData->jobletBoudary);
                    }
                    
                    GTEST_CHECKPOINTA("ScanPipelineStandard: onBuildPipeline: PipelineResource : %s\n", item->second.resourceInstanceProxy->getResourceServiceId().c_str());
                    
                    if(static_cast<std::vector<std::vector<std::shared_ptr<dune::job::IResourceInstanceProxy>>>::size_type>(item->second.resourceData->section) > resourceProxySections.size())
                    {
                        //New section to be created
                        std::vector<std::shared_ptr<dune::job::IResourceInstanceProxy>> resourceProxySection;
                        resourceProxySections.push_back(resourceProxySection);
                    }

                    //Check section value
                    assert_msg(static_cast<std::vector<std::vector<std::shared_ptr<dune::job::IResourceInstanceProxy>>>::size_type>(item->second.resourceData->section) <= resourceProxySections.size(), "Wrong defined sections values in configuration file");
                    //Add resource to the defined section
                    resourceProxySections[item->second.resourceData->section - 1].push_back(item->second.resourceInstanceProxy);

                    if (item->second.resourceData->isPipeQueueRequired)
                    {
                        if (item->second.resourceData->pipeType == PipeObjectType::IMAGECONTAINER)
                        {
                            if (item->second.resourceData->persistentPipe && !dataStore.empty())
                            {
                                if (item->second.resourceData->usePipeList && jobTicket != nullptr)
                                {
                                    // PipeList is used for a preview pipeline to be able to do operations like move and delete
                                    GTEST_CHECKPOINTA("Creating PipeList");
                                    auto pipeList = dune::job::PipeQueueFactory<ImageContainer>::createPipeList(dataStore, 0);
                                    jobTicket->setPipeListOperations(pipeList);
                                    pipeQueue = pipeList;
                                }
                                else if(item->second.resourceData->usePipeTee > 1)
                                {
                                    GTEST_CHECKPOINTA("Creating PipeTee");
                                    pipeQueue = dune::job::PipeQueueFactory<ImageContainer>::createPipeTee(dataStore, 0);
                                }
                                else
                                {
                                    GTEST_CHECKPOINTA("Creating persisted ImageContainer Object");
                                    pipeQueue = dune::job::PipeQueueFactory<ImageContainer>::createPipeQueue(true, dataStore, 0);
                                }

                                persistedPath = pipeQueue->getPersistentPath();
                                jobTicket->setPersistentPipePath(persistedPath);// setting persistent path in job ticket for any segment to use it
                                GTEST_CHECKPOINTA("Persisted Path : %s", persistedPath.c_str());
                            }
                            else
                            {
                                GTEST_CHECKPOINTA("Creating ImageContainer Object");
                                pipeQueue = dune::job::PipeQueueFactory<ImageContainer>::createPipeQueue();
                            }

                            assert_msg(pipeQueue != nullptr, "Failed to create pipeQueue object");

                            if (item->second.resourceData->reusePipeQueue)
                            {
                                auto iterator = persistedResources.find(item->first);
                                if (iterator != persistedResources.end())
                                {
                                    pipeQueue = iterator->second;
                                }
                                else
                                {
                                    GTEST_CHECKPOINTA("ScanPipelineStandard: createPipeQueuesAndResourceList: PipelineResource creating persisted pipe : %s\n", item->second.resourceInstanceProxy->getResourceServiceId().c_str());
                                    persistedResources.insert({item->first, pipeQueue});
                                }
                            }
                        }
                        else if (item->second.resourceData->pipeType == PipeObjectType::ATTACHMENTOBJECT || 
                                    item->second.resourceData->pipeType == PipeObjectType::PAGEDATA)
                        {
                            GTEST_CHECKPOINTA("Creating Attachment Object");
                            assert_msg(func != nullptr, "func pointer should not be null for Attachment object");

                            if (item->second.resourceData->fromPipe != ResourceName::NONE)
                            {
                                func(nullptr);
                            }
                            else
                            {
                                func(lastDequeuer);
                            }
                            break;  // exit the loop. Send device will take care from here.
                        }

                        if (item->second.resourceData->isSegmentFirstResource)
                        {
                            GTEST_CHECKPOINTA("Creating dequeuer and enqueuer for the first resource in the segment");

                            if (item->second.resourceData->queuingFlag == QueuingFlag::BOTH)
                            {
                                if (item->second.resourceData->toPipe != ResourceName::NONE &&
                                    item->second.resourceData->openForAppending)
                                {
                                    enqueuer = pipeQueue->reopenForAppending();
                                }
                                else
                                {
                                    enqueuer = pipeQueue->openForEnqueuing();
                                }
                                if (item->second.resourceData->fromPipe != ResourceName::NONE)
                                {
                                    auto iterator = persistedResources.find(item->second.resourceData->fromPipe);
                                    if (iterator != persistedResources.end())
                                    {
                                        GTEST_CHECKPOINTA("Creating dequeuer and enqueuer from the persisted resource in the segment");
                                        if (item->second.resourceData->reloadResource)
                                        {
                                            // Reload persisten pipe
                                            bool pipeReloaded = false;
                                            // Obtain the current start time
                                            std::time_t startTime = std::time(nullptr);
                                            // difftime is to avoid infinite loop if it exceeds 1 minute
                                            while (!pipeReloaded && std::difftime(std::time(nullptr), startTime) < 10)
                                            {
                                                try
                                                {
                                                    // CHECKPOINTA_STR("ScanPipelineStandard: onBuildPipeline: PipelineResource : %s\n", item->second.resourceInstanceProxy->getResourceServiceId().c_str());
                                                    // CHECKPOINTA_STR("ScanPipelineStandard: onBuildPipeline: PipelineResource : %d\n", iterator->first);
                                                    // Update last dequeuer as the first resource needs read from the persisted pipe
                                                    lastDequeuer = iterator->second->reload();
                                                    pipeReloaded = true;
                                                } catch (const std::exception &e)
                                                {
                                                    GTEST_CHECKPOINTA(
                                                        "SendPipelineBuilder: CreatePipeQueuesAndResourceList -- pipe not ready to "
                                                        "be reloaded.");
                                                    // This sleep is to avoid an excessive amount of retries in the reload method.
                                                    std::this_thread::sleep_for(std::chrono::milliseconds(100));
                                                }
                                            }

                                            dequeuer = pipeQueue->openForDequeuing();
                                        }
                                        else
                                        {
                                            GTEST_CHECKPOINTA("Nested else Creating dequeuer and enqueuer for the first resource in the segment");
                                            lastDequeuer = iterator->second->openForDequeuing();
                                            dequeuer = pipeQueue->openForDequeuing();
                                        }
                                    }
                                    else
                                    {
                                        GTEST_CHECKPOINTA("Else Creating dequeuer and enqueuer for the first resource in the segment");
                                    }
                                }
                                else if(item->second.resourceData->useTicketPersistentPath)
                                {
                                    GTEST_CHECKPOINTA("Use Ticket persistent path to create a last dequeuer");
                                    try
                                    {
                                        auto pipe_ImagePersisterData_ = dune::job::PipeQueueFactory<ImageContainer>::createPipeQueue(persistedPath);
                                        lastDequeuer = pipe_ImagePersisterData_->openForDequeuing();
                                        pipeQueues.push_back(pipe_ImagePersisterData_);
                                        dequeuer = pipeQueue->openForDequeuing();
                                    }
                                    catch(const exception &e)
                                    {
                                        GTEST_CHECKPOINTA("Persistent Pipe path not available  - %s - Ending the job",e.what());
                                        resourceProxySections.clear();
                                        break;
                                    }
                                }
                                else if(item->second.resourceData->usePageDataPipe)
                                {
                                    GTEST_CHECKPOINTA("Use PageData pipe to create a last dequeuer %s", persistedPath.c_str());
                                    auto pipe_ImagePersisterData_ = dune::job::PipeQueueFactory<PageData>::createPipeQueue(persistedPath);
                                    lastPageDataDequeuer = pipe_ImagePersisterData_->openForDequeuing();
                                    lastDequeuer = nullptr;
                                    pipeQueues.push_back(pipe_ImagePersisterData_);
                                    dequeuer = pipeQueue->openForDequeuing();
                                }
                                else
                                {
                                    dequeuer = pipeQueue->openForDequeuing();
                                }
                            }
                            else if (item->second.resourceData->queuingFlag == QueuingFlag::ENQUEUE)
                            {
                                if (item->second.resourceData->toPipe != ResourceName::NONE &&
                                    item->second.resourceData->openForAppending)
                                {
                                    enqueuer = pipeQueue->reopenForAppending();
                                }
                                else
                                {
                                    enqueuer = pipeQueue->openForEnqueuing();
                                }
                            }
                            else if (item->second.resourceData->queuingFlag == QueuingFlag::DEQUEUE)
                            {
                                if (item->second.resourceData->fromPipe != ResourceName::NONE)
                                {
                                    auto iterator = persistedResources.find(item->second.resourceData->fromPipe);
                                    if (iterator != persistedResources.end())
                                    {
                                        if (item->second.resourceData->reloadResource)
                                        {
                                            // Reload persisten pipe
                                            bool pipeReloaded = false;
                                            while (!pipeReloaded)
                                            {
                                                try
                                                {
                                                    lastDequeuer = iterator->second->reload();
                                                    pipeReloaded = true;
                                                } catch (const exception &e)
                                                {
                                                    GTEST_CHECKPOINTA(
                                                        "SendPipelineBuilder: CreatePipeQueuesAndResourceList -- pipe not ready to "
                                                        "be reloaded.");
                                                }
                                            }

                                            dequeuer = pipeQueue->openForDequeuing();
                                        }
                                        else
                                        {
                                            dequeuer = iterator->second->openForDequeuing();
                                        }
                                    }
                                }
                                else
                                {
                                    dequeuer = pipeQueue->openForDequeuing();
                                }
                            }
                        }
                        else
                        {
                            GTEST_CHECKPOINTA("Creating dequeuer and enqueuer for the remaining resource in the segment");

                            if (item->second.resourceData->queuingFlag == QueuingFlag::BOTH)
                            {
                                if (item->second.resourceData->toPipe != ResourceName::NONE &&
                                    item->second.resourceData->openForAppending)
                                {
                                    enqueuer = pipeQueue->reopenForAppending();
                                }
                                else
                                {
                                    enqueuer = pipeQueue->openForEnqueuing();
                                }

                                if (item->second.resourceData->fromPipe != ResourceName::NONE)
                                {
                                    auto iterator = persistedResources.find(item->second.resourceData->fromPipe);
                                    if (iterator != persistedResources.end())
                                    {
                                        GTEST_CHECKPOINTA("Nested else Creating dequeuer and enqueuer for the resource in the segment");
                                        lastDequeuer = iterator->second->openForDequeuing();
                                        dequeuer = pipeQueue->openForDequeuing();
                                    }
                                    else
                                    {
                                        GTEST_CHECKPOINTA("Else Creating dequeuer and enqueuer for the resource in the segment");
                                    }
                                }
                                else
                                {
                                    dequeuer = pipeQueue->openForDequeuing();
                                }
                            }
                            else if (item->second.resourceData->queuingFlag == QueuingFlag::ENQUEUE)
                            {
                                if (item->second.resourceData->toPipe != ResourceName::NONE &&
                                    item->second.resourceData->openForAppending)
                                {
                                    GTEST_CHECKPOINTA("Creating dequeuer and enqueuer for the remaining resource in the segment reopen for appending");
                                    enqueuer = pipeQueue->reopenForAppending();
                                }
                                else
                                {
                                    enqueuer = pipeQueue->openForEnqueuing();
                                }
                            }
                            else if (item->second.resourceData->queuingFlag == QueuingFlag::DEQUEUE)
                            {
                                dequeuer = pipeQueue->openForDequeuing();
                            }
                        }
                    }

                    GTEST_CHECKPOINTA("Calling resource setup function");
                    assert_msg(item->second.resourceSetupFunction != nullptr, "resource setup function should not be null");

                    // Call the setup funtion using fucntion pointer.
                    (item->second.resourceSetupFunction)({enqueuer, lastDequeuer, lastPageDataDequeuer});

                    if (item->second.resourceData->setKeep)
                    {
                        item->second.resourceInstanceProxy->setKeep(true);
                    }
                    else
                    {
                        item->second.resourceInstanceProxy->setKeep(false);
                    }

                    if (pipeQueue != nullptr)
                    {
                        // Avoid pushing null items.
                        pipeQueues.push_back(pipeQueue);
                    }

                    lastEnqueuer = enqueuer;
                    lastDequeuer = dequeuer;
                }

}));

    systemServices_ = new TestSystemServices();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyPipelineStandardConfig.fbs", productTestFileName.c_str());

    component_ = new CopyPipelineStandard("CopyPipelineStandard");

    ASSERT_TRUE(component_ != nullptr);
}

void GivenANewCopyPipelineStandard::TearDown()
{
    delete component_;
    delete systemServices_;
}
///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyPipelineStandardOfMMK : Add test cases related to MMK here
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyPipelineStandardOfMMK :public GivenANewCopyPipelineStandard
{
  public:

    GivenAConnectedCopyPipelineStandardOfMMK() {};

    virtual void SetUp() override;

    virtual void TearDown() override;
};

void GivenAConnectedCopyPipelineStandardOfMMK::SetUp()
{
    productTestFileName = "./testResources/CopyPipelineStandardMMK.json";
    GivenANewCopyPipelineStandard::SetUp();

    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
    ON_CALL(*scanPipeline_, getResourceList(_)).WillByDefault(Return(resourceList));
    scanPipelineConfig_->pipelineBuilderConfig->previewSettings->refreshPreviewSupported = true;
}

void GivenAConnectedCopyPipelineStandardOfMMK::TearDown()
{
    GivenANewCopyPipelineStandard::TearDown();
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenHomeSmbPipelineBuilderIsCreated_ThenNoErrors)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    ASSERT_NE(nullptr, services_.resourceManager);
    auto pipelineBuilder = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    ASSERT_NE(nullptr, pipelineBuilder);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenHomeSmbPipelineWithDiskBufferingIsBuiltWithNoIntentsManager_ThenPipelineIsCorrectlyComposedAndNoIntentsManagerIsUsed)
{
   auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setPagesPerSheet(CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);

    auto pipelineBuilder = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto copypipeline = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(pipelineBuilder);
    ASSERT_NE(nullptr, pipelineBuilder);

    copypipeline->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenOnBuildPipelineCalledJobNameSetToIDCardCopy)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setPagesPerSheet(CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);

    auto pipelineBuilder = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto copypipeline = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(pipelineBuilder);
    ASSERT_NE(nullptr, pipelineBuilder);

    copypipeline->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    EXPECT_EQ(jobTicket->getJobName(), "IDCardCopy");
}


TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenHomeSmbIsConfiguredWithLegalSize_ScanExtentsSetCorreclty)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    uint32_t xExtentValue;
    uint32_t yExtentValue;
    jobTicket->getIntent()->setInputMediaSizeId(MediaSizeId::LEGAL);
    ASSERT_NE(nullptr, jobTicket);

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

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);

    auto scanDeviceTicket = std::static_pointer_cast<IScanDeviceTicket>(first_section[0]->getResourceTicket());
    auto sdIntent = scanDeviceTicket->getIntent();

    EXPECT_EQ(xExtentValue, 2432);
    EXPECT_EQ(yExtentValue, 4082);

    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    
    EXPECT_EQ(0, sections.size());
    EXPECT_EQ(true, jobTicket->isPrintAlignmentChangeRequired());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenHomeSmbIsConfiguredExecutedAgain_ScanExtentsSetCorrecltyEachTime)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    uint32_t xExtentValue;
    uint32_t yExtentValue;
    ASSERT_NE(nullptr, jobTicket);

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

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    jobTicket->setSegmentType(SegmentType::PrepareSegment);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    EXPECT_EQ(jobTicket->getSegmentType(), SegmentType::PrepareSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);

    EXPECT_EQ(xExtentValue, 2432);
    EXPECT_EQ(yExtentValue, 3182);

    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(0, sections.size());

    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    EXPECT_EQ(jobTicket->getSegmentType(), SegmentType::PrepareSegment);
    resources = sections[0];
    EXPECT_EQ(2, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);

    EXPECT_EQ(xExtentValue, 2432);
    EXPECT_EQ(yExtentValue, 3182);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenHomeSmbPipelineIsBuilt_ThenPipelineIsCorrectlyComposed_ForRetry)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setCopies(2);

    jobTicket->setStorePath("/tmp");


    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);

    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);
    EXPECT_EQ(second_section[0]->getKeep(), true);
    EXPECT_EQ(second_section[1]->getKeep(), true);
    EXPECT_EQ(second_section[2]->getKeep(), true);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::UNCOMPRESSED);
    EXPECT_EQ(jobTicket->getIntent()->getPrintingOrder(), dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);

    jobTicket->setExecutionMode(dune::job::ExecutionMode::RETRY);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    second_section = sections[0];

    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);

    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    
    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenHomeSmbPipelineIsBuiltForGlassMultiStage_ThenPipelineIsCorrectlyComposed_ForRetry)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);
    jobTicket->getIntent()->setCopies(2);

    jobTicket->setStorePath("/tmp");

    std::shared_ptr<IEnqueueIntf>  pipe;

    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );


    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);

    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(2, first_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(first_section[0]->getKeep(), true);
    EXPECT_EQ(first_section[1]->getKeep(), true);
    EXPECT_EQ(jobTicket->getIntent()->getPrintingOrder(), dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);

    // Imagepersister queue's is closed for testing purpose to avoid the Fail related with ::reopenForAppending()
    // when the pipe is not closed
    pipe->closeForEnqueuing();

    // -> Stage::ScanSecondPage
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedSecondPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    
    // -> Stage::PrintAllPages
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    resources = sections[0];
    EXPECT_EQ(4, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(resources[2]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(resources[3]->getResourceServiceId(), printDeviceId_);

    jobTicket->setExecutionMode(dune::job::ExecutionMode::RETRY);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    second_section = sections[0];

    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[3]->getResourceServiceId(), printDeviceId_);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenHomeSmbPipelineIsBuiltFor2UpORIDCardWithGlass_ThenPipelineIsCorrectlyComposed_ForRetry)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    jobTicket->getIntent()->setCopies(2);

    jobTicket->setStorePath("/tmp");

    std::shared_ptr<IEnqueueIntf>  pipe;

    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    // Expectations
    EXPECT_CALL(*layoutFilterIntent_, setSequencingParams(_))
        .WillRepeatedly(Invoke([](const dune::imaging::Resources::LayoutSequencingParams& sequencingParams) -> void {
            EXPECT_EQ(2, sequencingParams.collationCopies);
            EXPECT_EQ(1, sequencingParams.uncollationCopies);
            EXPECT_EQ(8, sequencingParams.pagesNeededToSequence);
            EXPECT_EQ(false, sequencingParams.waitForSheet);
            EXPECT_EQ(false, sequencingParams.updateDetails);
            EXPECT_EQ(2, sequencingParams.imagesPerSheet);
        }));
    EXPECT_CALL(*layoutFilterIntent_, setNupLayout(_))
        .WillRepeatedly(Invoke([](const dune::imaging::types::NUpParams nUpParams) -> void {
            EXPECT_EQ(dune::imaging::types::NumberUp::ID_CARD, nUpParams.getMode());
        }));
    EXPECT_CALL(*layoutFilterIntent_, setImageRotation(_))
        .WillRepeatedly(Invoke([](const dune::imaging::types::RotationCW& rotation) -> void {
            EXPECT_EQ(dune::imaging::types::RotationCW::ROTATE_0, rotation);
        }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);

    ASSERT_NE(nullptr, pipelineBuilder);

    // -> Stage::ScanFirstPage
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(3, first_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(first_section[0]->getKeep(), true);
    EXPECT_EQ(first_section[1]->getKeep(), true);
    EXPECT_EQ(first_section[2]->getKeep(), true);
    EXPECT_EQ(jobTicket->getIntent()->getPrintingOrder(), dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);

    // Imagepersister queue's is closed for testing purpose to avoid the Fail related with ::reopenForAppending()
    // when the pipe is not closed
    pipe->closeForEnqueuing();

    jobTicket->setExecutionMode(dune::job::ExecutionMode::RETRY);

    // -> Stage::ScanSecondPage
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedSecondPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(3, resources.size());

    // -> Stage::PrintAllPages
    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    resources = sections[0];
    EXPECT_EQ(3, resources.size());

    second_section = resources;    

    EXPECT_EQ(second_section[0]->getResourceServiceId(), layoutFilterId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);

    second_section = sections[0];

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    EXPECT_EQ(second_section[0]->getResourceServiceId(), layoutFilterId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);

}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenHomeSmbPipelineIsBuiltFor2UpWithGlass_correctMFRasterizerMemoryClientIsSet)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setCopies(2);

    jobTicket->setStorePath("/tmp");

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;

    EXPECT_CALL(*layoutFilterInterfaces_, setPipelineMemoryClientCreator(_))

        .WillRepeatedly(

            testing::Invoke(
                [this, &pipelineMemoryClientCreator](
                    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {
                    pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;
                }));

    std::shared_ptr<IEnqueueIntf>  pipe;

    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );
    dune::imaging::Resources::SpecificPadding specificPadding;
    EXPECT_CALL(*imageProcessorIntent_, setSpecificPadding(_))

        .WillRepeatedly(

            testing::Invoke([this, &specificPadding](dune::imaging::Resources::SpecificPadding value) -> void {

                specificPadding = value;

            }));

    // -> Stage::ScanFirstPage
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);

    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(3, first_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    // Imagepersister queue's is closed for testing purpose to avoid the Fail related with ::reopenForAppending()
    // when the pipe is not closed
    pipe->closeForEnqueuing();

    jobTicket->setExecutionMode(dune::job::ExecutionMode::RETRY);

    // -> Stage::ScanSecondPage
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedSecondPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(3, resources.size());

    // -> Stage::PrintAllPages
    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    resources = sections[0];
    EXPECT_EQ(3, resources.size());

    EXPECT_EQ(printDeviceMemoryClientCreator_.get(), pipelineMemoryClientCreator);
    EXPECT_EQ(specificPadding.overridePadding, false);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenHomeSmb2UpPipelineIsBuilt_ThenPipelineIsCorrectlyComposed_ForRetry)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Uncollate);
    jobTicket->getIntent()->setPrintingOrder(dune::imaging::types::PrintingOrder::FIRST_PAGE_ON_TOP);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    jobTicket->setStorePath("/tmp");

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);

    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), layoutFilterId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);
    EXPECT_EQ(second_section[0]->getKeep(), true);
    EXPECT_EQ(second_section[1]->getKeep(), true);
    EXPECT_EQ(second_section[2]->getKeep(), true);
    EXPECT_EQ(jobTicket->getIntent()->getPrintingOrder(), dune::imaging::types::PrintingOrder::FIRST_PAGE_ON_TOP);

    jobTicket->setExecutionMode(dune::job::ExecutionMode::RETRY);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    second_section = sections[0];

    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);

    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    
    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenHomesmb2upGlassPipelineIsBuild_ThenRotationNotAllowed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    jobTicket->setStorePath("/tmp");

    std::shared_ptr<IEnqueueIntf>  pipe;

    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    // No rotation
    EXPECT_CALL(*layoutFilterIntent_, setImageRotation(_))
        .WillRepeatedly(Invoke([](const dune::imaging::types::RotationCW& rotation) -> void {
            EXPECT_EQ(dune::imaging::types::RotationCW::ROTATE_0, rotation);
        }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);

    ASSERT_NE(nullptr, pipelineBuilder);

    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    // Imagepersister queue's is closed for testing purpose to avoid the Fail related with ::reopenForAppending()
    // when the pipe is not closed
    pipe->closeForEnqueuing();

    jobTicket->setExecutionMode(dune::job::ExecutionMode::RETRY);

    // -> Stage::ScanSecondPage
    pipelineBuilder->onBuildPipeline(PromptType::FlatbedSecondPage, PromptResponseType::Response_01, SegmentType::FinalSegment);

    // -> Stage::PrintAllPages
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenHomeSmb2UpGlassPipelineIsBuilt_ThenSpecificRotationIsNotCalled)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    jobTicket->setStorePath("/tmp");

    EXPECT_CALL(*imageProcessorIntent_, setSpecificRotation(_)).Times(0);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);

    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenHomeSmb2UpUncollateMultipleCopiesPipelineIsBuilt_ThenPipelineIsCorrectlyComposed_ForRetry)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Uncollate);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    jobTicket->setStorePath("/tmp");

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), layoutFilterId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineIsBuiltForCopyPreviewIsOff_MakeSureYccColourSpaceAreSet)
{
    ON_CALL(*scanDeviceIntent_, getScanInYcc()).WillByDefault(Return(true));
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setImagePreview(dune::scan::types::ImagePreview::Disable);
    jobTicket->setPreviewMode(false);

    MockIScannerCapabilities mockScanCap;
    jobTicket->setScanCapabilitiesInterface(&mockScanCap);
    // simulate isImagingOperationSupported imaging operation supported in ScanDevice
    EXPECT_CALL(mockScanCap, isImagingOperationSupported(_, _))
        .WillRepeatedly(DoAll(SetArgReferee<1>(true), Return(APIResult::OK)));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(3, resources.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imagePersisterTicket_.get());

    auto scanDeviceTicket = std::static_pointer_cast<IScanDeviceTicket>(resources[0]->getResourceTicket());
    auto sdIntent = scanDeviceTicket->getIntent();
    EXPECT_EQ(sdIntent->getScanInYcc(), true);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineIsBuiltForCopyPreviewIsOn_MakeSureYccColourSpaceAreNotSet)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Uncollate);
    jobTicket->getIntent()->setImagePreview(dune::scan::types::ImagePreview::Enable);
    jobTicket->setPreviewMode(true);

    MockIScannerCapabilities mockScanCap;
    jobTicket->setScanCapabilitiesInterface(&mockScanCap);
    // simulate isImagingOperationSupported imaging operation supported in ScanDevice
    EXPECT_CALL(mockScanCap, isImagingOperationSupported(_, _))
        .WillRepeatedly(DoAll(SetArgReferee<1>(true), Return(APIResult::OK)));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());

    auto scanDeviceTicket = std::static_pointer_cast<IScanDeviceTicket>(resources[0]->getResourceTicket());
    auto sdIntent = scanDeviceTicket->getIntent();
    EXPECT_EQ(sdIntent->getScanInYcc(), false);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenGlassMultipleCopies1To2IsPerformed_CorrectCollatedAndUncollatedCopiesAreSet)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
    jobTicket->getIntent()->setCopies(2);

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

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreatorImageRetriever;

    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreatorImageRetriever](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreatorImageRetriever = pipelineMemoryClientCreator_value;

            }));

    // Fail in ImagePersister in the Stage::ScanSecondPage: C++ exception with description "INVALID OPERATION. 
    // PipeQueue<PO>::reopenForAppending() can't reopen queue that has not been closed for enqueueing." thrown in the test body.
    // We take the pipe to close it and avoid this issue
    std::shared_ptr<IEnqueueIntf>  pipe;

    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );
            
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // -> Stage::ScanFirstPage
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imagePersisterId_);

    // Imagepersister queue's is closed for testing purpose to avoid the Fail related with ::reopenForAppending()
    // when the pipe is not closed
    pipe->closeForEnqueuing();

    // -> Stage::ScanSecondPage
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedSecondPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    resources = sections[0];
    EXPECT_EQ(2, resources.size());
    
    // -> Stage::PrintAllPages
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    resources = sections[0];
    EXPECT_EQ(4, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(resources[2]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(resources[3]->getResourceServiceId(), printDeviceId_);

    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    
    EXPECT_EQ(0, sections.size());
    EXPECT_EQ(imageProcessorMemoryClientCreator_.get(), pipelineMemoryClientCreatorImageRetriever);
    EXPECT_EQ(collationCopies,   2);
    EXPECT_EQ(uncollationCopies, 1);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenADFMultipleCopies2UpIsPerformed_CorrectCollatedAndUncollatedCopiesAreSet)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Uncollate);

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

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), layoutFilterId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);

    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenADFMultipleCopies2UpIsPerformed_CorrectPrintingOrderIsSet)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Uncollate);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), layoutFilterId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);

    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenHomeSmbPreScanJobIsBuildBasicCopyPipeline_JobTicketSettingsFilledCorreclty)
{
    // For Copy pipeline
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setInputMediaSizeId(MediaSizeId::ANY);
    jobTicket->getIntent()->setScanSource(ScanSource::GLASS);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);

    EXPECT_EQ(jobTicket->isPreScanJob(), false);
    EXPECT_EQ(jobTicket->getSegmentType(), SegmentType::FinalSegment);

}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenHomeSmbPreviewSegmentExecuteWith2_2sidedCopyBasic_AllSegmentExecuteSuccess)
{
    // For Copy Selene pipeline
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setInputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);

    // Scan_First_Page Segment Executed
    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    resources = sections[0];
    EXPECT_EQ(2, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    EXPECT_EQ(resources[0]->getJobletBoundary(), dune::job::JobletBoundary::UNDEFINED);
    EXPECT_EQ(resources[1]->getJobletBoundary(), dune::job::JobletBoundary::UNDEFINED);

}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK,
       WhenHomeSmbPreviewSegmentExecuteWith2_2sidedCopyBasic_PreviewModeIsSetTrue)
{
    // For Copy Selene pipeline
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setInputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);

    auto copypipeline =
        component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false,
                                          maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);

    // Scan_First_Page Segment Executed
    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    resources = sections[0];
    EXPECT_EQ(2, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    EXPECT_EQ(resources[0]->getJobletBoundary(), dune::job::JobletBoundary::UNDEFINED);
    EXPECT_EQ(resources[1]->getJobletBoundary(), dune::job::JobletBoundary::UNDEFINED);
    EXPECT_EQ(jobTicket->getPreviewMode(), true);

}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenPrepareSegmentExecuteResourceAllocate_FinalSegmentExecute)
{
    // For Copy basic pipeline
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);

    resources[1]->allocate();

    EXPECT_EQ(resources[1]->getState(), ResourceInstanceProxy::StateType::Allocating);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);
    EXPECT_EQ(jobTicket->getPreviewMode(), true);

    EXPECT_EQ(first_section[2]->getJobletBoundary(), dune::job::JobletBoundary::START);
    EXPECT_EQ(second_section[2]->getJobletBoundary(), dune::job::JobletBoundary::END);
    
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    
    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenPrepareSegment_FinalSegmentExecute)
{
    // For Copy basic pipeline
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setCopies(2);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);

    EXPECT_EQ(first_section[2]->getJobletBoundary(), dune::job::JobletBoundary::START);
    EXPECT_EQ(second_section[2]->getJobletBoundary(), dune::job::JobletBoundary::END);
    
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    
    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineIsExecutedTwice_ZeroResourcesReturn)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);

    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    
    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineIsBuiltFor2_2Copy_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);
    jobTicket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineIsBuiltFor2_1Copy_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);
    jobTicket->getIntent()->setOutputPlexMode(dune::imaging::types::Plex::SIMPLEX);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineIsBuiltForIDCardCopy_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);

    auto copypipeline =
        component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false,
                                          maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(3, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[2].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);

    auto scanDeviceTicket = std::static_pointer_cast<IScanDeviceTicket>(resources[0]->getResourceTicket());
    auto sdIntent = scanDeviceTicket->getIntent();

    auto imagePersisterTicket = std::static_pointer_cast<IImagePersisterTicket>(resources[1]->getResourceTicket());
    auto ipIntent = imagePersisterTicket->getIntent();
    EXPECT_EQ(ipIntent->getJpegHwEnable(), false);
    EXPECT_EQ(ipIntent->getJpegVqEnable(), false);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineIsBuiltFor2UpFlatbed_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    auto copypipeline =
        component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false,
                                          maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(3, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[2].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);

    auto scanDeviceTicket = std::static_pointer_cast<IScanDeviceTicket>(resources[0]->getResourceTicket());
    auto sdIntent = scanDeviceTicket->getIntent();

    auto imagePersisterTicket = std::static_pointer_cast<IImagePersisterTicket>(resources[1]->getResourceTicket());
    auto ipIntent = imagePersisterTicket->getIntent();
    EXPECT_EQ(ipIntent->getJpegHwEnable(), false);
    EXPECT_EQ(ipIntent->getJpegVqEnable(), false);
}


TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineIsBuiltForBestMode_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    bool jpegHwEnable;
    EXPECT_CALL(*imagePersisterIntent_, setJpegHwEnable(_))

        .WillRepeatedly(

            testing::Invoke([this, &jpegHwEnable](bool value) -> void {

                jpegHwEnable = value;

            }));

    EXPECT_CALL(*imagePersisterIntent_, getJpegHwEnable())

        .WillRepeatedly(

            testing::Invoke([this, &jpegHwEnable]() -> bool {

                return jpegHwEnable ;

            }));

    bool jpegVqEnable;
    EXPECT_CALL(*imagePersisterIntent_, setJpegVqEnable(_))

        .WillRepeatedly(

            testing::Invoke([this, &jpegVqEnable](bool value) -> void {

                jpegVqEnable = value;

            }));

    EXPECT_CALL(*imagePersisterIntent_, getJpegVqEnable())

        .WillRepeatedly(

            testing::Invoke([this, &jpegVqEnable]() -> bool {

                return jpegVqEnable;

            }));


    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::OneUp);
    jobTicket->getIntent()->setCopyQuality(PrintQuality::BEST);

    auto copypipeline =
        component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false,
                                          maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(6, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[2].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);

    auto scanDeviceTicket = std::static_pointer_cast<IScanDeviceTicket>(resources[0]->getResourceTicket());
    auto sdIntent = scanDeviceTicket->getIntent();

    auto imagePersisterTicket = std::static_pointer_cast<IImagePersisterTicket>(resources[2]->getResourceTicket());
    auto ipIntent = imagePersisterTicket->getIntent();
    EXPECT_EQ(ipIntent->getJpegHwEnable(), true);
    EXPECT_EQ(ipIntent->getJpegVqEnable(), true);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenADF2UpPipelineIsBuilt_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), layoutFilterId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenADF2UpPipelineIsBuilt_correctMFRasterizerMemoryClientIsSet)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);
    
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;

    EXPECT_CALL(*layoutFilterInterfaces_, setPipelineMemoryClientCreator(_))

        .WillRepeatedly(

            testing::Invoke(
                [this, &pipelineMemoryClientCreator](
                    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {
                    pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;
                }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(printDeviceMemoryClientCreator_.get(), pipelineMemoryClientCreator);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineIsBuilt_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);
    
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineUnCollateIsBuilt_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Uncollate);
    jobTicket->getIntent()->setCopies(2);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
    EXPECT_EQ(jobTicket->getIntent()->getPrintingOrder(), dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);
}


TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineUnCollateIsBuilt_ThenPipelineFirstStageResourcesSetKeepValuesAreUnchanged)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Uncollate);
    jobTicket->getIntent()->setCopies(2);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
        EXPECT_EQ(first_section[i]->getKeep(), false);  // MMK configuration specifies false for all first stage resources.
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
    EXPECT_EQ(jobTicket->getIntent()->getPrintingOrder(), dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);
}


TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineCollateIsBuilt_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    int compressionFactor = 0;

    ASSERT_NE(nullptr, jobTicket);
    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreatorImageRetriever;

    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreatorImageRetriever](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreatorImageRetriever = pipelineMemoryClientCreator_value;

            }));

    uint32_t setMaxCollatePages;
    EXPECT_CALL(*scanDeviceIntent_, setAdfMaxPagesToScan(_))

        .WillRepeatedly(
            testing::Invoke([this, &setMaxCollatePages](uint32_t value)->void {
                setMaxCollatePages = value;
            }));
    bool performSequenceOperation;
    uint32_t collationCopies;
    uint32_t uncollationCopies;
    uint32_t pagesToSequence;
    EXPECT_CALL(*imageRetrieverIntent_, setSequencingParams(_))

        .WillRepeatedly(

            testing::Invoke([this, &performSequenceOperation, &collationCopies, &uncollationCopies, &pagesToSequence](
                                std::shared_ptr<dune::imaging::Resources::SequencingParams> sequencingParams) -> void {
                performSequenceOperation = (sequencingParams != nullptr);
                collationCopies = sequencingParams ? sequencingParams->collationCopies : 0;
                uncollationCopies = sequencingParams ? sequencingParams->uncollationCopies : 0;
                pagesToSequence = sequencingParams ? sequencingParams->pagesNeededToSequence : 0;
            }));

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setCompressionFactor(80);

    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    EXPECT_CALL(*imagePersisterIntent_, setCompressionFactor(_))

        .WillRepeatedly(

            testing::Invoke([this, &compressionFactor](int value) -> void {

                compressionFactor = value;

            }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);
    
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::UNCOMPRESSED);
    EXPECT_EQ(jobTicket->getIntent()->getPrintingOrder(), dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    EXPECT_EQ(compressionFactor, 80);
    EXPECT_EQ(pagesToSequence, 8);
    EXPECT_EQ(printDeviceMemoryClientCreator_.get(), pipelineMemoryClientCreatorImageRetriever);
    EXPECT_EQ(setMaxCollatePages, 24);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineCollateIsBuilt_ThenPipelineFirstStageResourcesAreSetKeepTrue)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    int compressionFactor = 0;

    ASSERT_NE(nullptr, jobTicket);
    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreatorImageRetriever;

    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreatorImageRetriever](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreatorImageRetriever = pipelineMemoryClientCreator_value;

            }));

    uint32_t setMaxCollatePages;
    EXPECT_CALL(*scanDeviceIntent_, setAdfMaxPagesToScan(_))

        .WillRepeatedly(
            testing::Invoke([this, &setMaxCollatePages](uint32_t value)->void {
                setMaxCollatePages = value;
            }));
    bool performSequenceOperation;
    uint32_t collationCopies;
    uint32_t uncollationCopies;
    uint32_t pagesToSequence;
    EXPECT_CALL(*imageRetrieverIntent_, setSequencingParams(_))

        .WillRepeatedly(

            testing::Invoke([this, &performSequenceOperation, &collationCopies, &uncollationCopies, &pagesToSequence](
                                std::shared_ptr<dune::imaging::Resources::SequencingParams> sequencingParams) -> void {
                performSequenceOperation = (sequencingParams != nullptr);
                collationCopies = sequencingParams ? sequencingParams->collationCopies : 0;
                uncollationCopies = sequencingParams ? sequencingParams->uncollationCopies : 0;
                pagesToSequence = sequencingParams ? sequencingParams->pagesNeededToSequence : 0;
            }));

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setCompressionFactor(80);

    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    EXPECT_CALL(*imagePersisterIntent_, setCompressionFactor(_))

        .WillRepeatedly(

            testing::Invoke([this, &compressionFactor](int value) -> void {

                compressionFactor = value;

            }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
        EXPECT_EQ(first_section[i]->getKeep(), true);
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);
    
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::UNCOMPRESSED);
    EXPECT_EQ(jobTicket->getIntent()->getPrintingOrder(), dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    EXPECT_EQ(compressionFactor, 80);
    EXPECT_EQ(pagesToSequence, 8);
    EXPECT_EQ(printDeviceMemoryClientCreator_.get(), pipelineMemoryClientCreatorImageRetriever);
    EXPECT_EQ(setMaxCollatePages, 24);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineCollateIsBuiltAndMorePagesDetectedForCollateContinue_ThenPipelineIsCorrectlyComposedTheSecondTime)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    int compressionFactor = 0;

    ASSERT_NE(nullptr, jobTicket);
    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreatorImageRetriever;

    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreatorImageRetriever](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreatorImageRetriever = pipelineMemoryClientCreator_value;

            }));

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setCompressionFactor(80);

    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    EXPECT_CALL(*imagePersisterIntent_, setCompressionFactor(_))

        .WillRepeatedly(

            testing::Invoke([this, &compressionFactor](int value) -> void {

                compressionFactor = value;

            }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());
    sections =
        pipelineBuilder->onBuildPipeline(PromptType::MorePagesDetectedForCollate, PromptResponseType::Response_01, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);
    
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::UNCOMPRESSED);
    EXPECT_EQ(jobTicket->getIntent()->getPrintingOrder(), dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    EXPECT_EQ(compressionFactor, 80);
    EXPECT_EQ(printDeviceMemoryClientCreator_.get(), pipelineMemoryClientCreatorImageRetriever);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineCollateIsBuiltAndMorePagesDetectedForCollateCancel_ThenPipelineIsCorrectlyCancelled)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    int compressionFactor = 0;

    ASSERT_NE(nullptr, jobTicket);
    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreatorImageRetriever;

    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreatorImageRetriever](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreatorImageRetriever = pipelineMemoryClientCreator_value;

            }));

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setCompressionFactor(80);

    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    EXPECT_CALL(*imagePersisterIntent_, setCompressionFactor(_))

        .WillRepeatedly(

            testing::Invoke([this, &compressionFactor](int value) -> void {

                compressionFactor = value;

            }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());
    
    sections =
        pipelineBuilder->onBuildPipeline(PromptType::MorePagesDetectedForCollate, PromptResponseType::Response_03, SegmentType::FinalSegment);
    
    EXPECT_EQ(0, sections.size());
    EXPECT_EQ(dune::job::CompletionStateType::CANCELED,jobTicket->getCompletionState());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenBasicPipelineScalingIsBuilt_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;

    ASSERT_NE(nullptr, jobTicket);
    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreatorImageRetriever;

    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreatorImageRetriever](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreatorImageRetriever = pipelineMemoryClientCreator_value;

            }));
    jobTicket->getIntent()->setScaleSelection(dune::scan::types::ScanScaleSelectionEnum::CUSTOM);
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setCopies(2);

    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenPreScanPipelineIsBuilt_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    int compressionFactor = 0;

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setCompressionFactor(80);
    jobTicket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);

    auto scanDeviceResult = std::make_shared<MockIScanDeviceResult>();
    EXPECT_CALL(*scanDeviceTicket_, getScanDeviceResult()).WillRepeatedly(Return(scanDeviceResult));

    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    EXPECT_CALL(*imagePersisterIntent_, setCompressionFactor(_))

        .WillRepeatedly(

            testing::Invoke([this, &compressionFactor](int value) -> void {

                compressionFactor = value;

            }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    pipelineBuilder->setSimulatorJob(false);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());
    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, first_section.size());
    EXPECT_EQ(3, second_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }

    GTEST_CHECKPOINTA("second_section resources\n");
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resources %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(first_section[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(second_section[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(second_section[1]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(second_section[2]->getResourceServiceId(), printDeviceId_);
    
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
    EXPECT_EQ(jobTicket->getIntent()->getPrintingOrder(), dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    EXPECT_EQ(compressionFactor, 80);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfMMK, WhenPreScanPipelineIsBuilt_ThenPreviewPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    int compressionFactor = 0;

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setCopies(2);
    jobTicket->getIntent()->setCompressionFactor(80);
    jobTicket->getIntent()->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);

    auto scanDeviceResult = std::make_shared<MockIScanDeviceResult>();
    EXPECT_CALL(*scanDeviceTicket_, getScanDeviceResult()).WillRepeatedly(Return(scanDeviceResult));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), true, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    pipelineBuilder->setSimulatorJob(false);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());
    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    first_section = sections[0];
    EXPECT_EQ(2, first_section.size());

    EXPECT_EQ(first_section[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(first_section[1]->getResourceServiceId(), imageProcessorId_);
    
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyPipelineStandardOfPro : Add test cases related to MMK here
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyPipelineStandardOfPro :public GivenANewCopyPipelineStandard
{
  public:

    GivenAConnectedCopyPipelineStandardOfPro() {};

    virtual void SetUp() override;

    virtual void TearDown() override;
};

void GivenAConnectedCopyPipelineStandardOfPro::SetUp()
{
    productTestFileName = "./testResources/CopyPipelineStandardPro.json";
    GivenANewCopyPipelineStandard::SetUp();

    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
    ON_CALL(*scanPipeline_, getResourceList(_)).WillByDefault(Return(resourceList));
    scanPipelineConfig_->pipelineBuilderConfig->previewSettings->refreshPreviewSupported = true;
}

void GivenAConnectedCopyPipelineStandardOfPro::TearDown()
{
    GivenANewCopyPipelineStandard::TearDown();
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineBuilderIsCreated_ThenNoErrors)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    ASSERT_NE(nullptr, services_.resourceManager);
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineWithDiskBufferingIsBuiltWithNoIntentsManager_ThenPipelineIsCorrectlyComposedAndNoIntentsManagerIsUsed)
{
   auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // In this configuration, the intent manager should try to set a value,
    // but because the intent manager is null, the intent should only be called once before setting the value
    EXPECT_CALL(*imageRetrieverTicket_, getIntent()).WillOnce(InvokeWithoutArgs([this]() {
        EXPECT_CALL(*imageRetrieverIntent_, setMediaPointers(mediaInterface_.get(), mediaSettingsInterface_.get(), mediaInfoInterface_.get(),nullptr)).Times(1);
        return imageRetrieverIntent_;
    }));

    // Execute pipeline with ImageRetriever
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe_value->closeForEnqueuing();
            })
    );
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    pipelineBuilder->onBuildPipeline(PromptType::FlatbedSecondPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuilt_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(5, resources.size());
    EXPECT_EQ(5, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);
    EXPECT_EQ(resources[2]->getResourceTicket().get(), pageAssemblerTicket_.get());
    EXPECT_EQ(resourcesTicket[2].resourceType, dune::job::IIntentsManager::ResourceType::PAGE_ASSEMBLER_SERVICE);
    EXPECT_EQ(resources[3]->getResourceTicket().get(), rtpFilterTicket_.get());
    EXPECT_EQ(resourcesTicket[3].resourceType, dune::job::IIntentsManager::ResourceType::RTP_FILTER_SERVICE);
    EXPECT_EQ(resources[4]->getResourceTicket().get(), printDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[4].resourceType, dune::job::IIntentsManager::ResourceType::PRINT_DEVICE_SERVICE);
    
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
    EXPECT_EQ(false, jobTicket->isPrintAlignmentChangeRequired());
    //ideally we should check the serviceId
    // EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    // EXPECT_EQ(resources[1]->getResourceServiceId(), pageAssemblerId_);
    // EXPECT_EQ(resources[2]->getResourceServiceId(), printDeviceId_);

}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuiltForColla6teFlatbed_ThenPipelineHasCorrectCollateMode)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setCopies(2);

    ASSERT_NE(nullptr, jobTicket);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(5, resources.size());
    EXPECT_EQ(5, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);
    EXPECT_EQ(resources[2]->getResourceTicket().get(), pageAssemblerTicket_.get());
    EXPECT_EQ(resourcesTicket[2].resourceType, dune::job::IIntentsManager::ResourceType::PAGE_ASSEMBLER_SERVICE);
    EXPECT_EQ(resources[3]->getResourceTicket().get(), rtpFilterTicket_.get());
    EXPECT_EQ(resourcesTicket[3].resourceType, dune::job::IIntentsManager::ResourceType::RTP_FILTER_SERVICE);
    EXPECT_EQ(resources[4]->getResourceTicket().get(), printDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[4].resourceType, dune::job::IIntentsManager::ResourceType::PRINT_DEVICE_SERVICE);
    
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
    EXPECT_EQ(false, jobTicket->isPrintAlignmentChangeRequired());
    //ideally we should check the serviceId
    // EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    // EXPECT_EQ(resources[1]->getResourceServiceId(), pageAssemblerId_);
    // EXPECT_EQ(resources[2]->getResourceServiceId(), printDeviceId_);

}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineWith2upBuiltUsingLayoutFilter_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    ASSERT_NE(nullptr, jobTicket);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(7, resources.size());
    EXPECT_EQ(7, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);// Because the scan disk buffering is active, the image retriever is of the buffering type
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[2].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(resources[3]->getResourceTicket().get(), layoutFilterTicket_.get());
    EXPECT_EQ(resourcesTicket[3].resourceType, dune::job::IIntentsManager::ResourceType::LAYOUT_FILTER);// Because the scan disk buffering is active, the image retriever is of the buffering type
    EXPECT_EQ(resources[4]->getResourceTicket().get(), pageAssemblerTicket_.get());
    EXPECT_EQ(resourcesTicket[4].resourceType, dune::job::IIntentsManager::ResourceType::PAGE_ASSEMBLER_SERVICE);
    EXPECT_EQ(resources[5]->getResourceTicket().get(), rtpFilterTicket_.get());
    EXPECT_EQ(resourcesTicket[5].resourceType, dune::job::IIntentsManager::ResourceType::RTP_FILTER_SERVICE);
    EXPECT_EQ(resources[6]->getResourceTicket().get(), printDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[6].resourceType, dune::job::IIntentsManager::ResourceType::PRINT_DEVICE_SERVICE);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuilt_ScanDeviceIntentFilledCorrectly)
{
    ON_CALL(*scanDeviceIntent_, getOriginalMediaType()).WillByDefault(Return(dune::scan::types::OriginalMediaType::PHOTO_PAPER));
    ON_CALL(*scanDeviceIntent_, getColorMode()).WillByDefault(Return(ColorMode::GRAYSCALE));
    ON_CALL(*scanDeviceIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::GLASS));

    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)); 
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];

    for (int i = 0; i < (int)resources.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, resources[i]->getResourceServiceId().c_str());
    }
    std::shared_ptr<MockIScanDeviceTicket>  scanTicket = std::static_pointer_cast<MockIScanDeviceTicket>(resources[0]->getResourceTicket());

    //add the scan intents to be checked as needed here
    auto scanIntent = scanTicket->getIntent();
    EXPECT_EQ(scanIntent->getOriginalMediaType(),  dune::scan::types::OriginalMediaType::PHOTO_PAPER);
    EXPECT_EQ(scanIntent->getColorMode(),  ColorMode::GRAYSCALE);
    EXPECT_EQ(scanIntent->getScanSource(),  dune::scan::types::ScanSource::GLASS);
}




TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuilt_ScanDeviceIntentMediaTypesFilledBasedOnPrintMediaTypes)
{

    //Get the copy job ticket
    //set the outputMedia type to dune::imaging::types::MediaIdType::HPPHOTO
    //mapImagingMediaTypeToScanMediaType will be called exactly once
    //when the Copypipeline is built, the scanDeviceIntent original media type should be dune::scan::types::OriginalMediaType::PHOTO_PAPER

    ON_CALL(*scanDeviceIntent_, getOriginalMediaType()).WillByDefault(Return(dune::scan::types::OriginalMediaType::PHOTO_PAPER));

    EXPECT_CALL(*scanPipeline_, mapImagingMediaTypeToScanMediaType(dune::imaging::types::MediaIdType::HPPHOTO))
    .Times(1)
    .WillOnce(Return(dune::scan::types::OriginalMediaType::PHOTO_PAPER));

    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::HPPHOTO);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];

    for (int i = 0; i < (int)resources.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, resources[i]->getResourceServiceId().c_str());
    }
    std::shared_ptr<MockIScanDeviceTicket>  scanTicket = std::static_pointer_cast<MockIScanDeviceTicket>(resources[0]->getResourceTicket());

    auto scanIntent = scanTicket->getIntent();
    EXPECT_EQ(scanIntent->getOriginalMediaType(),  dune::scan::types::OriginalMediaType::PHOTO_PAPER);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuilt_ScanDeviceIntentMapQualityFilledBasedOnPrintQuality)
{

    //Get the copy job ticket
    //set the PrintQuality to dune::imaging::types::PrintQuality::DRAFT
    //mapCopyQualityToScanMapQuality will be called exactly once
    //when the Copypipeline is built, the scanDeviceIntent ScanMapQuality type should be dune::scan::types::OriginalMediaType::FAST

    ON_CALL(*scanDeviceIntent_, getScanMapQuality()).WillByDefault(Return(dune::scan::types::ScanMapQualityEnum::BEST));

    EXPECT_CALL(*scanPipeline_, mapCopyQualityToScanMapQuality(dune::imaging::types::PrintQuality::BEST))
    .Times(1)
    .WillOnce(Return(dune::scan::types::ScanMapQualityEnum::BEST));

    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setCopyQuality(dune::imaging::types::PrintQuality::BEST);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];

    for (int i = 0; i < (int)resources.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, resources[i]->getResourceServiceId().c_str());
    }
    std::shared_ptr<MockIScanDeviceTicket>  scanTicket = std::static_pointer_cast<MockIScanDeviceTicket>(resources[0]->getResourceTicket());

    auto scanIntent = scanTicket->getIntent();
    EXPECT_EQ(scanIntent->getScanMapQuality(),  dune::scan::types::ScanMapQualityEnum::BEST);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenPipelineIsBuiltForAutoCrop_ThenPipelineStageSetCorrectly)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    jobIntent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    jobIntent->setScaleToFitEnabled(true);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(5, resources.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuiltForOriginalSizeSetToAny_ThenPipelineCompletesSuccessfully)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    jobIntent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];

    for (int i = 0; i < (int)resources.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, resources[i]->getResourceServiceId().c_str());
    }
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuiltWithColorModeSetToBlackAndWhite_ThenSimpleThresholdingIsDisabled)
{
    ON_CALL(*scanDeviceIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::GLASS));

    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    auto jobIntent = jobTicket->getIntent();
    jobIntent->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobIntent->setColorMode(dune::imaging::types::ColorMode::BLACKANDWHITE);
    bool thresholdEnabled = false;
    int thresholdValue = 0;

    EXPECT_CALL(*imageProcessorIntent_, setSimpleThresholdingNeeded(_,_))
        .WillOnce(
            testing::Invoke([this, &thresholdEnabled, &thresholdValue](bool enable, int threshold) -> void {
                thresholdEnabled = enable;
                thresholdValue = threshold;
            })
        );

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    EXPECT_EQ(thresholdEnabled, false);
    EXPECT_EQ(thresholdValue, 128); // 128 is the default parameter for threshold in setSimpleThresholdingNeeded
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuiltForTwoPagesPerSheetJobFromAdfUsingLayoutFilter_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setPagesPerSheet(CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];

    for (int i = 0; i < (int)resources.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, resources[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(7, resources.size());
    EXPECT_EQ(7, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);
    EXPECT_EQ(resources[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(resourcesTicket[2].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(resources[3]->getResourceServiceId(), layoutFilterId_);
    EXPECT_EQ(resourcesTicket[3].resourceType, dune::job::IIntentsManager::ResourceType::LAYOUT_FILTER);
    EXPECT_EQ(resources[4]->getResourceServiceId(), pageAssemblerId_);
    EXPECT_EQ(resourcesTicket[4].resourceType, dune::job::IIntentsManager::ResourceType::PAGE_ASSEMBLER_SERVICE);
    EXPECT_EQ(resources[5]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(resourcesTicket[5].resourceType, dune::job::IIntentsManager::ResourceType::RTP_FILTER_SERVICE);
    EXPECT_EQ(resources[6]->getResourceServiceId(), printDeviceId_);
    EXPECT_EQ(resourcesTicket[6].resourceType, dune::job::IIntentsManager::ResourceType::PRINT_DEVICE_SERVICE);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuiltWithDifferentMediaSizes_ThenNoErrors)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    auto jobIntent = jobTicket->getIntent();

    EXPECT_CALL(*scanDeviceTicket_, getIntent()).WillRepeatedly(Return(scanDeviceIntent_));
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _));
    //
    // Test that we're getting Letterd dimensions

    jobIntent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    std::vector<PipelineBuilderBase::ResourceInstanceProxies> pipelineSectionResources = pipelineBuilder->onBuildPipeline(
        PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    //
    // Test that we're getting A4 dimensions

    jobIntent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    pipelineSectionResources = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse,
                                                 SegmentType::FinalSegment);

    //
    // Test that we're getting A5 dimensions

    jobIntent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A5);
    pipelineSectionResources = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse,
                                                 SegmentType::FinalSegment);

    //
    // For legal, I expect adfLoaded to be set to false which will force the
    // legal size scan to a letter sized scan.

    jobIntent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LEGAL);
    pipelineSectionResources = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse,
                                                 SegmentType::FinalSegment);

    //
    // Test any other enumeration than Letter, Legal, A4, A5 resolve to letter dimensions for now.

    jobIntent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::CUSTOM);
    pipelineSectionResources = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse,
                                                 SegmentType::FinalSegment);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenJobTypeIs2PagesPerSheet_ThenSetFirstStageChoosesCorrectly)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    jobIntent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobIntent->setScanSource(dune::scan::types::ScanSource::GLASS);
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _));
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment)[0];
    // Stage currentStage = pipelineBuilder->currentStageOfPipeline();
    // EXPECT_EQ(currentStage, Stage::ScanSecondPage);  //Should be ScanSecondPage after finishing the first page and ready to scan the next page on the next build pipeline call
    // EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsCreated_ThenMarkingFilterIntentIsCalled)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    auto jobIntent = jobTicket->getIntent();

    EXPECT_CALL(*markingFilterTicket_, getIntent()).WillRepeatedly(Return(markingFilterIntent_));
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsCreatedUsingLayoutFilter_ThenLayoutFilterIntentIsCalled)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    auto jobIntent = jobTicket->getIntent();

    EXPECT_CALL(*layoutFilterTicket_, getIntent()).WillRepeatedly(Return(layoutFilterIntent_));
    EXPECT_CALL(*layoutFilterTicket_, getInterfaces()).WillRepeatedly(Return(layoutFilterInterfaces_));
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuiltForPreview_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    for (int i = 0; i < (int)resources.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, resources[i]->getResourceServiceId().c_str());
    }

    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());
    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuiltWithAutoDeskewInScanDevice_ThenImageProcessorIsNotConfiguredForAutoDeskew)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->getIntent()->setAutoDeskew(true);

    MockIScannerCapabilities mockScanCap;
    jobTicket->setScanCapabilitiesInterface(&mockScanCap);
    // simulate AutoDeskew imaging operation supported in ScanDevice
    EXPECT_CALL(mockScanCap, isImagingOperationSupported(_, _))
        .WillRepeatedly(DoAll(SetArgReferee<1>(true), Return(APIResult::OK)));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // must be configured in ScanDevice, not in ImageProcessor
    EXPECT_CALL(*scanDeviceIntent_, setAutoDeskew(_)).Times(1);
    EXPECT_CALL(*imageProcessorIntent_, setUseAutoDeskew(_)).Times(0);
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _));
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuiltWithoutAutoDeskewInScanDevice_ThenImageProcessorIsConfiguredForAutoDeskew)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->getIntent()->setAutoDeskew(true);

    MockIScannerCapabilities mockScanCap;
    jobTicket->setScanCapabilitiesInterface(&mockScanCap);
    // simulate AutoDeskew imaging operation not supported in ScanDevice
    EXPECT_CALL(mockScanCap, isImagingOperationSupported(_, _))
        .WillRepeatedly(DoAll(SetArgReferee<1>(false), Return(APIResult::OK)));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // must be configured in ImageProcessor, not in ScanDevice
    EXPECT_CALL(*scanDeviceIntent_, setAutoDeskew(_)).Times(0);
    EXPECT_CALL(*imageProcessorIntent_, setUseAutoDeskew(_)).Times(1);
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _));
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuiltWithBackgroundColorRemovalInScanDevice_ThenScanDeviceIsConfiguredForBackgroundColorRemoval)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->getIntent()->setBackgroundColorRemoval(true);

    MockIScannerCapabilities mockScanCap;
    jobTicket->setScanCapabilitiesInterface(&mockScanCap);
    // simulate BackgroundColorRemoval imaging operation supported in ScanDevice
    EXPECT_CALL(mockScanCap, isImagingOperationSupported(_, _))
        .WillRepeatedly(DoAll(SetArgReferee<1>(true), Return(APIResult::OK)));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // must be configured in ScanDevice, not in ImageProcessor
    EXPECT_CALL(*scanDeviceIntent_, setBackgroundRemoval(_)).Times(1);
    scanPipelineConfig_->imageQuality = true;
    // expect backgroundRemovalType to be set to BGREM_NONE in ImageProcessor (unconfigured)
    // NOTE: using Field matcher doesn't seem to compile
    EXPECT_CALL(*imageProcessorIntent_, setImageQualityValues(_))
        .WillOnce([](std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> valuesTable) {
            ASSERT_EQ(valuesTable->backgroundRemovalType, dune::imaging::types::BackgroundRemovalType::BGREM_NONE);
        });
    
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _));
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuiltWithoutBackgroundColorRemovalInScanDevice_ThenImageProcessorIsConfiguredForBackgroundColorRemoval)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->getIntent()->setBackgroundColorRemoval(true);

    MockIScannerCapabilities mockScanCap;
    jobTicket->setScanCapabilitiesInterface(&mockScanCap);
    // simulate BackgroundColorRemoval imaging operation not supported in ScanDevice
    EXPECT_CALL(mockScanCap, isImagingOperationSupported(_, _))
        .WillRepeatedly(DoAll(SetArgReferee<1>(false), Return(APIResult::OK)));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // must be configured in ImageProcessor, not in ScanDevice
    EXPECT_CALL(*scanDeviceIntent_, setBackgroundRemoval(_)).Times(0);
    scanPipelineConfig_->imageQuality = true;
    // expect backgroundRemovalType to be set to BGREM_AUTOCTX in ImageProcessor
    // NOTE: using Field matcher doesn't seem to compile
    EXPECT_CALL(*imageProcessorIntent_, setImageQualityValues(_))
        .WillOnce([](std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> valuesTable) {
            ASSERT_EQ(valuesTable->backgroundRemovalType, dune::imaging::types::BackgroundRemovalType::BGREM_AUTOCTX);
        });

    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _));
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuiltWithBackgroundNoiseRemovalInScanDevice_ThenScanDeviceIsConfiguredForBackgroundNoiseRemoval)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->getIntent()->setBackgroundNoiseRemoval(true);

    MockIScannerCapabilities mockScanCap;
    jobTicket->setScanCapabilitiesInterface(&mockScanCap);
    // simulate BackgroundNoiseRemoval imaging operation supported in ScanDevice
    EXPECT_CALL(mockScanCap, isImagingOperationSupported(_, _))
        .WillRepeatedly(DoAll(SetArgReferee<1>(true), Return(APIResult::OK)));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    EXPECT_CALL(*scanDeviceIntent_, setScanNoiseRemoval(_)).Times(1);
    scanPipelineConfig_->imageQuality = true;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _));

    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPipelineIsBuiltWithoutBackgroundNoiseRemovalInScanDevice_ThenScanDeviceIsNotConfiguredForBackgroundNoiseRemoval)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    jobTicket->getIntent()->setBackgroundNoiseRemoval(false);

    MockIScannerCapabilities mockScanCap;
    jobTicket->setScanCapabilitiesInterface(&mockScanCap);
    // simulate BackgroundNoiseRemoval imaging operation not supported in ScanDevice
    EXPECT_CALL(mockScanCap, isImagingOperationSupported(_, _))
        .WillRepeatedly(DoAll(SetArgReferee<1>(false), Return(APIResult::OK)));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    EXPECT_CALL(*scanDeviceIntent_, setScanNoiseRemoval(_)).Times(0);
    scanPipelineConfig_->imageQuality = true;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _));
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenBasicPipelineIsBuiltForPreview_ThenPipelineIsCorrectlyComposed)
{

    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);

    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, When2PagesPerSheetPipelineExecuteUsingLayoutFilter_ValidJobLetIsDefined)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    EXPECT_CALL(*layoutFilterInterfaces_, setPipelineMemoryClientCreator(_))
        .WillRepeatedly(testing::Invoke([this](dune::imaging::IPipelineMemoryClientCreator* memoryCreator) -> void {
            EXPECT_EQ(pageAssemblerMemoryClientCreator_.get(), memoryCreator);
        }));

    EXPECT_CALL(*pageAssembler_, getRasterFormatNegotiator(_))
        .Times(2)
        .WillRepeatedly(Return(static_cast<MockIRasterFormatNegotiator*>(
            rasterNegotiator_.get())));  // 1 for processor, 1 for layout filter

    EXPECT_CALL(*imagePersister_, getRasterFormatSelector(_))
        .WillOnce(Return(static_cast<MockIRasterFormatSelector*>(rasterSelector_.get())));  // 1 for processor
    EXPECT_CALL(*imagePersister_, getRasterFormatNegotiator(_))
        .WillOnce(Return(static_cast<MockIRasterFormatNegotiator*>(rasterNegotiator_.get())));  // 1 for processor

    jobTicket->getIntent()->setPagesPerSheet(CopyOutputNumberUpCount::TwoUp);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(7, resources.size());
    EXPECT_EQ(7, resourcesTicket.size());


    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);
    EXPECT_EQ(resources[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(resourcesTicket[2].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(resources[3]->getResourceServiceId(), layoutFilterId_);
    EXPECT_EQ(resourcesTicket[3].resourceType, dune::job::IIntentsManager::ResourceType::LAYOUT_FILTER);
    EXPECT_EQ(resources[4]->getResourceServiceId(), pageAssemblerId_);
    EXPECT_EQ(resourcesTicket[4].resourceType, dune::job::IIntentsManager::ResourceType::PAGE_ASSEMBLER_SERVICE);
    EXPECT_EQ(resources[5]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(resourcesTicket[5].resourceType, dune::job::IIntentsManager::ResourceType::RTP_FILTER_SERVICE);
    EXPECT_EQ(resources[6]->getResourceServiceId(), printDeviceId_);
    EXPECT_EQ(resourcesTicket[6].resourceType, dune::job::IIntentsManager::ResourceType::PRINT_DEVICE_SERVICE);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);

    EXPECT_EQ(resources[1]->getJobletBoundary(), dune::job::JobletBoundary::START);
    EXPECT_EQ(resources[6]->getJobletBoundary(), dune::job::JobletBoundary::END);
    
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPreviewSegmentExecutesAgain_ThenhandleRefreshPreviewIsCalled)
{

    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillRepeatedly(::testing::SaveArg<1>(&resourcesTicket));

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
    
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(0, sections.size());

    EXPECT_CALL(*scanPipeline_, handleRefreshPreview(_)).Times(1);
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());
    resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPreviewSegmentExecuteWith2_2sided_AllSegmentExecuteSuccess)
{
    // For Copy Selene pipeline
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setInputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillRepeatedly(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);

    // Scan_First_Page Segment Executed
    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    EXPECT_EQ(resources[0]->getJobletBoundary(), dune::job::JobletBoundary::UNDEFINED);
    EXPECT_EQ(resources[1]->getJobletBoundary(), dune::job::JobletBoundary::UNDEFINED);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProFinalSegmentExecuteWith2_2sided_AllSegmentExecuteSuccess)
{
    // For Copy Selene pipeline
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setInputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // Scan_First_Page Segment Executed
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    EXPECT_EQ(resources[0]->getJobletBoundary(), dune::job::JobletBoundary::UNDEFINED);
    EXPECT_EQ(resources[1]->getJobletBoundary(), dune::job::JobletBoundary::UNDEFINED);

}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProFinalSegmentExecuteWith2_2sided_PromptResponse02Selected)
{
    // For Copy Selene pipeline
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setInputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // Scan_First_Page Segment Executed
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    EXPECT_EQ(resources[0]->getJobletBoundary(), dune::job::JobletBoundary::UNDEFINED);
    EXPECT_EQ(resources[1]->getJobletBoundary(), dune::job::JobletBoundary::UNDEFINED);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::FlatbedSecondPage, PromptResponseType::Response_03, SegmentType::FinalSegment);
    
    EXPECT_EQ(0, sections.size());
    EXPECT_EQ(dune::job::CompletionStateType::CANCELED,jobTicket->getCompletionState());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPrepareSegmentExecuteForUnCollate_AllResourcesAllocated)
{
    // For Copy Selene pipeline
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setCopies(5);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Uncollate);
    jobTicket->setSegmentType(SegmentType::PrepareSegment);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).Times(2).WillRepeatedly(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    EXPECT_EQ(jobTicket->getSegmentType(), SegmentType::PrepareSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);

    // Scan_First_Page Segment Executed
    jobTicket->setSegmentType(SegmentType::FinalSegment);
    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    resources = sections[0];
    EXPECT_EQ(5, resources.size());
    EXPECT_EQ(5, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(resources[2]->getResourceServiceId(), pageAssemblerId_);
    EXPECT_EQ(resources[3]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(resources[4]->getResourceServiceId(), printDeviceId_);

    EXPECT_EQ(resources[0]->getJobletBoundary(), dune::job::JobletBoundary::UNDEFINED);
    EXPECT_EQ(resources[1]->getJobletBoundary(), dune::job::JobletBoundary::UNDEFINED);
    EXPECT_EQ(resources[2]->getJobletBoundary(), dune::job::JobletBoundary::START);
    EXPECT_EQ(resources[3]->getJobletBoundary(), dune::job::JobletBoundary::UNDEFINED);
    EXPECT_EQ(resources[4]->getJobletBoundary(), dune::job::JobletBoundary::END);

    // Finished
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    
    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProFinalSegmentExecute_RawFileFormatSelected)
{
    // For Copy Selene pipeline
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);
    dune::imaging::types::FileFormat fileFormat;

    EXPECT_CALL(*imagePersisterIntent_, setFileFormat(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileFormat](dune::imaging::types::FileFormat value) -> void {

                fileFormat = value;

            }));

    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setInputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    // Scan_First_Page Segment Executed
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    // DUNE-114562 re-implemented Flatbed prescan in simulator
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    EXPECT_EQ(resources[0]->getJobletBoundary(), dune::job::JobletBoundary::UNDEFINED);
    EXPECT_EQ(resources[1]->getJobletBoundary(), dune::job::JobletBoundary::UNDEFINED);
    EXPECT_EQ(jobTicket->getSegmentType(), SegmentType::FinalSegment);

    EXPECT_EQ(fileFormat, dune::imaging::types::FileFormat::ZLIB);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProIsConfiguredExecutedAgain_ScanIntentsSetCorreclty)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    jobTicket->getIntent()->setScanSource(ScanSource::GLASS);
    uint32_t xExtentValue;
    uint32_t yExtentValue;
    ASSERT_NE(nullptr, jobTicket);

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
    EXPECT_CALL(*imageProcessorIntent_, setOutputCanvasTable(_)).Times(0);

    bool addborderRequired{true};
    EXPECT_CALL(*imageProcessorIntent_, setAddBorderRequired(_))

        .WillRepeatedly(

            testing::Invoke([this, &addborderRequired](uint32_t value) -> void {

                addborderRequired = value;

            }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(5, resources.size());
    EXPECT_EQ(5, resourcesTicket.size());

    EXPECT_EQ(xExtentValue, 2432);
    EXPECT_EQ(yExtentValue, 3182);
    EXPECT_EQ(addborderRequired, false);

}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProPreScanJobIsBuild_JobTicketSettingsFilledCorreclty)
{
    // For Copy Selene pipeline
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setInputMediaSizeId(MediaSizeId::ANY);
    jobTicket->getIntent()->setScanSource(ScanSource::GLASS);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(5, resources.size());
    EXPECT_EQ(5, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);

    EXPECT_EQ(jobTicket->isPreScanJob(), false);
    EXPECT_EQ(jobTicket->getDefaultMediaSize(), dune::imaging::types::MediaSizeId::LETTER);
    EXPECT_EQ(jobTicket->getPrescannedHeight(), 0);
    EXPECT_EQ(jobTicket->getPrescannedWidth(), 0);
    EXPECT_EQ(jobTicket->getSegmentType(), SegmentType::FinalSegment);

}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeSmbIsConfiguredExecutedAgain_ScanExtentsSetCorrecltyEachTime)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    uint32_t xExtentValue;
    uint32_t yExtentValue;
    ASSERT_NE(nullptr, jobTicket);

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

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    jobTicket->setSegmentType(SegmentType::PrepareSegment);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    EXPECT_EQ(jobTicket->getSegmentType(), SegmentType::PrepareSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);

    EXPECT_EQ(xExtentValue, 2432);
    EXPECT_EQ(yExtentValue, 3182);

    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(0, sections.size());

    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    EXPECT_EQ(jobTicket->getSegmentType(), SegmentType::PrepareSegment);
    resources = sections[0];
    EXPECT_EQ(2, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);

    EXPECT_EQ(xExtentValue, 2432);
    EXPECT_EQ(yExtentValue, 3182);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProSegmentExecute_For_2_2Sided_duplex_twoUp)
{
    // For Copy Selene pipeline
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);
    std::shared_ptr<IEnqueueIntf>  pipe;

    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {

                pipe = pipe_value;

            }));            

    EXPECT_CALL(*imageProcessorTicket_, setPipelineMemoryClientCreator(_))
        .WillRepeatedly(testing::Invoke([this](dune::imaging::IPipelineMemoryClientCreator* memoryCreator) -> void {
            EXPECT_EQ(persisterMemoryClientCreator_.get(), memoryCreator);
        }));

    EXPECT_CALL(*layoutFilterInterfaces_, setPipelineMemoryClientCreator(_))
        .WillRepeatedly(testing::Invoke([this](dune::imaging::IPipelineMemoryClientCreator* memoryCreator) -> void {
            EXPECT_EQ(pageAssemblerMemoryClientCreator_.get(), memoryCreator);
        }));
    
    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setInputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillRepeatedly(::testing::SaveArg<1>(&resourcesTicket));
    // Scan_First_Page Segment Executed
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(3, resourcesTicket.size());
    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(resources[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    //close the imagepersister queue for testing purpose
    pipe->closeForEnqueuing();

     sections =
        pipelineBuilder->onBuildPipeline(PromptType::FlatbedSecondPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

     resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(3, resourcesTicket.size());
    //close the imagepersister queue for testing purpose
    pipe->closeForEnqueuing();

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::FlatbedSecondPage, PromptResponseType::Response_01, SegmentType::FinalSegment);

    EXPECT_EQ(1, sections.size());

     resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(3, resourcesTicket.size());
    //close the imagepersister queue for testing purpose
    pipe->closeForEnqueuing();

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::FlatbedSecondPage, PromptResponseType::Response_01, SegmentType::FinalSegment);

    EXPECT_EQ(1, sections.size());

     resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(3, resourcesTicket.size());

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    EXPECT_EQ(1, sections.size());

     resources = sections[0];
    EXPECT_EQ(4, resources.size());
    EXPECT_EQ(4, resourcesTicket.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenAnyPreviousResourceStateIsNotFailedCallingOnBuildPipelineReturnsNonEmptyResources)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    jobIntent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobIntent->setScanSource(dune::scan::types::ScanSource::GLASS);
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _));
    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    auto resources = sections[0];
    EXPECT_NE(0, resources.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenAnyPreviousResourceStateIsFailedCallingOnBuildPipelineReturnsEmptyResources)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    jobIntent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobIntent->setScanSource(dune::scan::types::ScanSource::GLASS);

    EXPECT_CALL(*pageAssemblerTicket_, getCompletionState()).Times(2).WillRepeatedly(Return(CompletionStateType::FAILED));

    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenImagePersisterResourceStateIsFailedCallingOnBuildPipelineReturnsEmptyResources)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    jobIntent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobIntent->setScanSource(dune::scan::types::ScanSource::GLASS);

    EXPECT_CALL(*pageAssemblerTicket_, getCompletionState()).Times(2).WillRepeatedly(Return(CompletionStateType::FAILED));

    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenImageProcessorResourceStateIsFailedCallingOnBuildPipelineReturnsEmptyResources)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    jobIntent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobIntent->setScanSource(dune::scan::types::ScanSource::GLASS);

    EXPECT_CALL(*pageAssemblerTicket_, getCompletionState()).Times(2).WillRepeatedly(Return(CompletionStateType::FAILED));

    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenScanDeviceResourceStateIsFailedCallingOnBuildPipelineReturnsEmptyResources)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    jobIntent->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobIntent->setScanSource(dune::scan::types::ScanSource::GLASS);

    EXPECT_CALL(*pageAssemblerTicket_, getCompletionState()).Times(2).WillRepeatedly(Return(CompletionStateType::FAILED));

    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    EXPECT_EQ(0, sections.size());
}
TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenOnBuildPipelineIsCalledScanAndPageAssemblerResolutionsAreSetProperlyADF)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    jobIntent->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    auto outputXResolution = Resolution::E300DPI;
    auto outputYResolution = Resolution::E300DPI;
    jobIntent->setOutputXResolution(outputXResolution);
    jobIntent->setOutputYResolution(outputYResolution);

    Resolution  YResolution;
    Resolution  XResolution;
    Resolution  PaResoultion;

    EXPECT_CALL(*scanDeviceIntent_, setOutputXResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &XResolution](Resolution value) -> void {

                XResolution = value;

            }));
    EXPECT_CALL(*scanDeviceIntent_, setOutputYResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &YResolution](Resolution value) -> void {

                YResolution = value;

            }));
    
    EXPECT_CALL(*pageAssemblerIntent_, setResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &PaResoultion](Resolution value) -> void {

                PaResoultion = value;

            }));
            

    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];

    for (int i = 0; i < (int)resources.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, resources[i]->getResourceServiceId().c_str());
    }
    
    EXPECT_EQ(5, resources.size());
    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(resources[2]->getResourceServiceId(), pageAssemblerId_);
    EXPECT_EQ(resources[3]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(resources[4]->getResourceServiceId(), printDeviceId_);

    EXPECT_EQ(XResolution, outputXResolution);
    EXPECT_EQ(YResolution, outputYResolution);
    EXPECT_EQ(PaResoultion, outputXResolution);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenOnBuildPipelineIsCalledScanAndPageAssemblerResolutionsAreSetProperlyFlatbed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setInputPlexMode(Plex::DUPLEX);
    jobIntent->setScanSource(dune::scan::types::ScanSource::GLASS);
    auto outputXResolution = Resolution::E600DPI;
    auto outputYResolution = Resolution::E600DPI;
    jobIntent->setOutputXResolution(outputXResolution);
    jobIntent->setOutputYResolution(outputYResolution);

    Resolution  YResolution;
    Resolution  XResolution;

    EXPECT_CALL(*pageAssemblerTicket_, setPipelineMemoryClientCreator(_)).Times(0);

    EXPECT_CALL(*scanDeviceIntent_, setOutputXResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &XResolution](Resolution value) -> void {

                XResolution = value;

            }));
    EXPECT_CALL(*scanDeviceIntent_, setOutputYResolution(_))

        .WillRepeatedly(

            testing::Invoke([this, &YResolution](Resolution value) -> void {

                YResolution = value;

            }));
            

    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];

    for (int i = 0; i < (int)resources.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, resources[i]->getResourceServiceId().c_str());
    }
    
    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    EXPECT_EQ(XResolution, outputXResolution);
    EXPECT_EQ(YResolution, outputYResolution);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProSegmentExecute_ForBasicCopy_correctMemoryClientIsSet)
{
    // For Copy Selene pipeline
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);
    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;

    EXPECT_CALL(*pageAssemblerTicket_, setPipelineMemoryClientCreator(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);

    ASSERT_NE(nullptr, pipelineBuilder);

    // Scan_First_Page Segment Executed
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(5, resources.size());

    EXPECT_EQ(printDeviceMemoryClientCreator_.get(), pipelineMemoryClientCreator);

}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenHomeProSegmentExecute_For2UpCopy_correctMFRasterizerMemoryClientIsSet)
{
    // For Copy Selene pipeline
    auto jobTicket = std::make_shared<CopyJobTicket>();
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    ASSERT_NE(nullptr, jobTicket);

    EXPECT_CALL(*layoutFilterInterfaces_, setPipelineMemoryClientCreator(_))
        .WillRepeatedly(testing::Invoke([this](dune::imaging::IPipelineMemoryClientCreator* memoryCreator) -> void {
            EXPECT_EQ(pageAssemblerMemoryClientCreator_.get(), memoryCreator);
        }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);

    ASSERT_NE(nullptr, pipelineBuilder);

    // Scan_First_Page Segment Executed
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(7, resources.size());

}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenADFMultipleCopies2UpIsPerformed_CorrectPrintingOrderIsSet)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);
    
    std::shared_ptr<dune::imaging::Resources::SequencingParams> sequencingParams;
    std::shared_ptr<dune::imaging::Resources::SequencingParams> sequencingParams1{std::make_shared<dune::imaging::Resources::SequencingParams>()};

    EXPECT_CALL(*imageRetrieverIntent_, setSequencingParams(_)).WillRepeatedly(
        testing::Invoke([this, &sequencingParams](std::shared_ptr<dune::imaging::Resources::SequencingParams> value) -> void {
            sequencingParams = value;
        })
    );

    ON_CALL(*imageRetrieverIntent_, getSequencingParams()).WillByDefault(Return(sequencingParams1));      
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // Execute pipeline with ImageRetriever
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe_value->closeForEnqueuing();
            })
    );
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    pipelineBuilder->onBuildPipeline(PromptType::FlatbedSecondPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    
    // Check Printing Order value
    EXPECT_EQ(sequencingParams1->printingOrder, dune::imaging::types::PrintingOrder::FIRST_PAGE_ON_TOP);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenADFMultipleCopies2UpIsPerformed_SequencingParamsIsNotSetUp)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setCopies(20);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Uncollate);
    
    // For Selene "setSequencingParams()" should be nullptr, as copies as performed by PrintDevice
    EXPECT_CALL(*layoutFilterIntent_, setSequencingParams(_))
        .WillRepeatedly(Invoke([](const dune::imaging::Resources::LayoutSequencingParams& sequencingParams) -> void {
            EXPECT_EQ(1, sequencingParams.collationCopies);
            EXPECT_EQ(1, sequencingParams.uncollationCopies);
        }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    EXPECT_EQ(7, first_section.size());

    GTEST_CHECKPOINTA("first_section resources\n");
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }
}

TEST_F(GivenAConnectedCopyPipelineStandardOfPro, WhenAddPageMaxPageReached_ResourceInstanceFreeIsCalled)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    std::shared_ptr<IEnqueueIntf>  pipe;
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    pipelineBuilder->setMaxFlatbedDuplexPages(1);
    // -> Stage::ScanFirstPage
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();
    // -> Stage::ScanSecondPage
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedDuplexAddPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    resources = sections[0];
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    //As max Page is reached the resource setkeep should be set to False
    for (int i = 0; i < (int)resources.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, resources[i]->getResourceServiceId().c_str());
        EXPECT_EQ(resources[i]->getKeep(), false);
    }
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyPipelineStandardOfBeam : Add test cases related to MMK here
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyPipelineStandardOfBeam :public GivenANewCopyPipelineStandard
{
  public:

    GivenAConnectedCopyPipelineStandardOfBeam() {};

    virtual void SetUp() override;

    virtual void TearDown() override;
};

void GivenAConnectedCopyPipelineStandardOfBeam::SetUp()
{
    productTestFileName = "./testResources/CopyPipelineStandardBeam.json";
    GivenANewCopyPipelineStandard::SetUp();

    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
    ON_CALL(*scanPipeline_, getResourceList(_)).WillByDefault(Return(resourceList));
}

void GivenAConnectedCopyPipelineStandardOfBeam::TearDown()
{
    GivenANewCopyPipelineStandard::TearDown();
}

TEST_F(GivenAConnectedCopyPipelineStandardOfBeam, WhenBeamIsConfiguredExecutedAgain_ScanIntentsSetCorrectly_And_ResourcesAreFreed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    jobTicket->getIntent()->setScanSource(ScanSource::MDF);
    uint32_t xExtentValue;
    uint32_t yExtentValue;
    ASSERT_NE(nullptr, jobTicket);

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

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, true, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(1, resources.size());
    EXPECT_EQ(1, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), scanDeviceId_);

    // verify resources are not held after scan stage
    EXPECT_EQ(resources[0]->getKeep(), false);

    EXPECT_EQ(xExtentValue, 2432);
    EXPECT_EQ(yExtentValue, 3182);
    EXPECT_EQ(false, jobTicket->isPrintAlignmentChangeRequired());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfBeam, WhenHomeProMdfPiplineIsBuiltForOutputSizeSetToAny_ThenPipelineCompletesSuccessfully)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    jobIntent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    jobIntent->setScanSource(dune::scan::types::ScanSource::MDF);
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, true, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];

    for (int i = 0; i < (int)resources.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, resources[i]->getResourceServiceId().c_str());
    }
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfBeam, WhenHomeProMdfPipelineIsBuildWithOriginalContentTypeSetToBlueprint_ThenScanDeviceIntentInputMediaTypeIsSetToBlueprint)
{
    ON_CALL(*scanDeviceIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::MDF));
    dune::scan::types::OriginalMediaType mediaTypeValue;

    auto jobTicket = std::make_shared<CopyJobTicket>();
    EXPECT_CALL(*scanDeviceIntent_, setOriginalMediaType(_))
        .WillRepeatedly(
            testing::Invoke([this, &mediaTypeValue](dune::scan::types::OriginalMediaType value) -> void {
                mediaTypeValue = value;
            }));

    ASSERT_NE(nullptr, jobTicket);
    auto jobIntent = jobTicket->getIntent();
    jobIntent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    jobIntent->setScanSource(dune::scan::types::ScanSource::MDF);
    jobIntent->setOriginalMediaType(dune::scan::types::OriginalMediaType::BLUEPRINTS);
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, true, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    EXPECT_EQ(dune::scan::types::OriginalMediaType::BLUEPRINTS, mediaTypeValue);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfBeam, WhenHomeProMdfPipelineIsBuiltWithColorModeSetToBlackAndWhite_ThenSimpleThresholdingIsEnabled)
{
    ON_CALL(*scanDeviceIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::MDF));

    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    auto jobIntent = jobTicket->getIntent();
    jobIntent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    jobIntent->setScanSource(dune::scan::types::ScanSource::MDF);
    jobIntent->setColorMode(dune::imaging::types::ColorMode::BLACKANDWHITE);
    thresholdOverride_ = 220;
    bool thresholdEnabled = false;
    int thresholdValue = 0;

    EXPECT_CALL(*imageProcessorIntent_, setSimpleThresholdingNeeded(_,_))
        .WillOnce(
            testing::Invoke([this, &thresholdEnabled, &thresholdValue](bool enable, int threshold) -> void {
                thresholdEnabled = enable;
                thresholdValue = threshold;
            })
        );

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, true, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    //pipelineBuilder->setThresholdOverride(thresholdOverride_);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    EXPECT_EQ(thresholdEnabled, true);
    EXPECT_EQ(thresholdValue, thresholdOverride_);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfBeam, WhenHomeProMdfPipelineIsBuiltWithColorModeSetToGrayscale_ThenSimpleThresholdingIsDisabled)
{
    ON_CALL(*scanDeviceIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::MDF));

    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    auto jobIntent = jobTicket->getIntent();
    jobIntent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    jobIntent->setScanSource(dune::scan::types::ScanSource::MDF);
    jobIntent->setColorMode(dune::imaging::types::ColorMode::GRAYSCALE);
    bool thresholdEnabled = false;
    int thresholdValue = 0;

    EXPECT_CALL(*imageProcessorIntent_, setSimpleThresholdingNeeded(_,_))
        .WillOnce(
            testing::Invoke([this, &thresholdEnabled, &thresholdValue](bool enable, int threshold) -> void {
                thresholdEnabled = enable;
                thresholdValue = threshold;
            })
        );

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, true, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    EXPECT_EQ(thresholdEnabled, false);
    EXPECT_EQ(thresholdValue, 128); // 128 is the default parameter for threshold in setSimpleThresholdingNeeded
}

TEST_F(GivenAConnectedCopyPipelineStandardOfBeam, WhenHomeProMdfPipelineIsBuiltWithColorModeSetToColor_ThenSimpleThresholdingIsDisabled)
{
    ON_CALL(*scanDeviceIntent_, getScanSource()).WillByDefault(Return(dune::scan::types::ScanSource::MDF));

    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    auto jobIntent = jobTicket->getIntent();
    jobIntent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    jobIntent->setScanSource(dune::scan::types::ScanSource::MDF);
    jobIntent->setColorMode(dune::imaging::types::ColorMode::COLOR);
    bool thresholdEnabled = false;
    int thresholdValue = 0;

    EXPECT_CALL(*imageProcessorIntent_, setSimpleThresholdingNeeded(_,_))
        .WillOnce(
            testing::Invoke([this, &thresholdEnabled, &thresholdValue](bool enable, int threshold) -> void {
                thresholdEnabled = enable;
                thresholdValue = threshold;
            })
        );

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, true, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    
    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    EXPECT_EQ(thresholdEnabled, false);
    EXPECT_EQ(thresholdValue, 128); // 128 is the default parameter for threshold in setSimpleThresholdingNeeded
}

TEST_F(GivenAConnectedCopyPipelineStandardOfBeam, WhenpiplelineconfiguredforBeamitCreatesAPersistentPipe)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);
    jobTicket->setStorePath("/tmp");
    jobIntent->setScanSource(dune::scan::types::ScanSource::MDF);
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, true, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    
    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    boost::filesystem::path persistentPath(jobTicket->getPersistentPipePath());
    EXPECT_EQ(jobTicket->getStorePath(),persistentPath.parent_path());
    //Verify that Image is persisted fine and can be reloaded 
    ASSERT_NO_THROW(dune::job::PipeQueueFactory<ImageContainer>::createPipeQueue(jobTicket->getPersistentPipePath()));
}

TEST_F(GivenAConnectedCopyPipelineStandardOfBeam, WhenReprintExecutionModeCalledForBeamItReprintsSuccessfully)
{
    auto dummyPipeQueue =dune::job::PipeQueueFactory<ImageContainer>::createPipeQueue(true,"/tmp", 0);

    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);
    jobIntent->setScanSource(dune::scan::types::ScanSource::MDF);
    jobTicket->setExecutionMode(dune::job::ExecutionMode::RERUN);
    jobTicket->setPersistentPipePath(dummyPipeQueue->getPersistentPath());

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, true, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    
    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(4, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), imageProcessorId_);
    EXPECT_EQ(resources[2]->getResourceServiceId(), rtpFilterServiceId_);
    EXPECT_EQ(resources[3]->getResourceServiceId(), printDeviceId_);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfBeam, WhenRerunExecutionModeCalledForBeamAndPersistedPipeDoesnotexistsFailTheJob)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);

    jobTicket->setExecutionMode(dune::job::ExecutionMode::RERUN);
    jobTicket->setPersistentPipePath("/tmp/nonexistentpipe/path");
    jobIntent->setScanSource(dune::scan::types::ScanSource::MDF);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, true, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    
    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    
    EXPECT_EQ(0, sections.size());
    EXPECT_EQ(dune::job::CompletionStateType::FAILED,jobTicket->getCompletionState());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfBeam, WhenBuildingAPipeline_ThenThereIsOnlyAScanDeviceResourceInTheFirstStage)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);
    jobIntent->setScanSource(dune::scan::types::ScanSource::MDF);
    jobTicket->setStorePath("/tmp");
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, true, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    auto firstSection = sections[0];
    ASSERT_EQ(1, firstSection.size()) << "There should be only 1 resource in the first stage";

    auto firstResourceId = firstSection[0]->getResourceServiceId();
    EXPECT_EQ(scanDeviceId_, firstResourceId) << "The resource in the first stage should be scan device";
};

TEST_F(GivenAConnectedCopyPipelineStandardOfBeam, WhenBuildingAPipeline_ThenThereAreTheCorrectFourResourcesInTheSecondStage)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);
    jobIntent->setScanSource(dune::scan::types::ScanSource::MDF);
    jobTicket->setStorePath("/tmp");
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, true, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment); //Ignore the first stage

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    auto firstSection = sections[0];

    ASSERT_EQ(4, firstSection.size()) << "There should be only 4 resources in the second stage";
    auto firstResourceId  = firstSection[0]->getResourceServiceId();
    auto secondResourceId = firstSection[1]->getResourceServiceId();
    auto thirdResourceId  = firstSection[2]->getResourceServiceId();
    auto fourthResourceId = firstSection[3]->getResourceServiceId();

    EXPECT_EQ(imageRetrieverId_, firstResourceId)   << "The first resource in the second stage should be image retriever";
    EXPECT_EQ(imageProcessorId_, secondResourceId)  << "The second resource in the second stage should be image processor";
    EXPECT_EQ(rtpFilterServiceId_, thirdResourceId) << "The third resource in the second stage should be rtp filter service";
    EXPECT_EQ(printDeviceId_, fourthResourceId)     << "The fourth resource in the second stage should be print device";
};

TEST_F(GivenAConnectedCopyPipelineStandardOfBeam, WhenBuildingAPipeline_ThenTheFilepathIsSetOnTheScanIntent)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);
    jobIntent->setScanSource(dune::scan::types::ScanSource::MDF);
    jobTicket->setStorePath("/tmp");
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, true, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    EXPECT_CALL(*scanDeviceIntent_, setFilePath("/tmp"));
    EXPECT_CALL(*scanDeviceIntent_, setFileName("scan_from_sbb"));
    EXPECT_CALL(*scanDeviceIntent_, setFileFormat(dune::imaging::types::FileFormat::JPEG));

    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
};

TEST_F(GivenAConnectedCopyPipelineStandardOfBeam, WhenBeamPipelineIsBuiltForScanCalibration_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    jobTicket->setScanCalibrationType(dune::imaging::types::ScanCalibrationType::SCANNER_USER_CALIBRATION);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, true, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(1, resources.size());
    EXPECT_EQ(1, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
};

TEST_F(GivenAConnectedCopyPipelineStandardOfBeam, WhenPipelineIsBuildCorrect_MemoryClientIsAllocatedToImageProcessor)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);
    auto jobIntent = jobTicket->getIntent();
    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreatorImageProcessor;
    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreatorImageRetriever;

    EXPECT_CALL(*imageProcessorTicket_, setPipelineMemoryClientCreator(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreatorImageProcessor](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreatorImageProcessor = pipelineMemoryClientCreator_value;

            }));
    
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreatorImageRetriever](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreatorImageRetriever = pipelineMemoryClientCreator_value;

            }));
    
    EXPECT_CALL(*imageRetrieverTicket_, setPrintIntentsFactoryInterface(_));

    jobIntent->setScanSource(dune::scan::types::ScanSource::MDF);
    jobTicket->setStorePath("/tmp");
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::HOME_PRO, services_, scanPipeline_.get(), false, true, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);

    ASSERT_NE(nullptr, pipelineBuilder);

    pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment); //Ignore the first stage

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    auto firstSection = sections[0];

    ASSERT_EQ(4, firstSection.size()) << "There should be only 4 resources in the second stage";
    auto firstResourceId  = firstSection[0]->getResourceServiceId();
    auto secondResourceId = firstSection[1]->getResourceServiceId();
    auto thirdResourceId  = firstSection[2]->getResourceServiceId();
    auto fourthResourceId = firstSection[3]->getResourceServiceId();

    EXPECT_EQ(imageRetrieverId_, firstResourceId)   << "The first resource in the second stage should be image retriever";
    EXPECT_EQ(imageProcessorId_, secondResourceId)  << "The second resource in the second stage should be image processor";
    EXPECT_EQ(rtpFilterServiceId_, thirdResourceId) << "The third resource in the second stage should be rtp filter service";
    EXPECT_EQ(printDeviceId_, fourthResourceId)     << "The fourth resource in the second stage should be print device";

    EXPECT_EQ(printDeviceMemoryClientCreator_.get(), pipelineMemoryClientCreatorImageProcessor);
    EXPECT_EQ(imageProcessorMemoryClientCreator_.get(), pipelineMemoryClientCreatorImageRetriever);

}
///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyPipelineStandardOfJupiter : Add test cases related to Jupiter here
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyPipelineStandardOfJupiter :public GivenANewCopyPipelineStandard
{
  public:

    GivenAConnectedCopyPipelineStandardOfJupiter() {};

    virtual void SetUp() override;

    virtual void TearDown() override;

    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> imageRetrieverBuffer_{nullptr};
};

void GivenAConnectedCopyPipelineStandardOfJupiter::SetUp()
{
    productTestFileName = "./testResources/CopyPipelineStandardJupiter.json";
    GivenANewCopyPipelineStandard::SetUp();

    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

     //Set direct copy behaviour
    ON_CALL(mockICopyAdapter_, getCopyMode()).WillByDefault(Return(dune::cdm::copy_1::configuration::CopyMode::printAfterScanning));
    //Fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    auto scanDeviceConfig1 = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    scanDeviceConfig1->resourceId = dune::scan::Jobs::Scan::ResourceName::SCANDEVICE;
    scanDeviceConfig1->pipeType = dune::scan::Jobs::Scan::PipeObjectType::IMAGECONTAINER;
    scanDeviceConfig1->jobletBoudary = dune::job::JobletBoundary::UNDEFINED;
    scanDeviceConfig1->isSegmentFirstResource = true;
    scanDeviceConfig1->isPipeQueueRequired = true;
    scanDeviceConfig1->queuingFlag = QueuingFlag::BOTH;


    auto imagePersisterBuffer = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    imagePersisterBuffer->resourceId = dune::scan::Jobs::Scan::ResourceName::IMAGEPERSISTERDISKBUFFERING;
    imagePersisterBuffer->pipeType = dune::scan::Jobs::Scan::PipeObjectType::IMAGECONTAINER;
    imagePersisterBuffer->jobletBoudary = dune::job::JobletBoundary::UNDEFINED;
    imagePersisterBuffer->isPipeQueueRequired = true;
    imagePersisterBuffer->queuingFlag = QueuingFlag::BOTH;
    imagePersisterBuffer->reusePipeQueue = true;
    imagePersisterBuffer->persistentPipe = true;

    imageRetrieverBuffer_ = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    imageRetrieverBuffer_->resourceId = dune::scan::Jobs::Scan::ResourceName::IMAGERETRIEVERDISKBUFFERING;
    imageRetrieverBuffer_->pipeType = dune::scan::Jobs::Scan::PipeObjectType::IMAGECONTAINER;
    imageRetrieverBuffer_->jobletBoudary = dune::job::JobletBoundary::UNDEFINED;
    imageRetrieverBuffer_->isPipeQueueRequired = true;
    imageRetrieverBuffer_->queuingFlag = QueuingFlag::BOTH;

    auto imageProcessorConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    imageProcessorConfig->resourceId = dune::scan::Jobs::Scan::ResourceName::IMAGEPROCESSORPREVIEW;
    imageProcessorConfig->pipeType = dune::scan::Jobs::Scan::PipeObjectType::IMAGECONTAINER;
    imageProcessorConfig->jobletBoudary = dune::job::JobletBoundary::UNDEFINED;
    imageProcessorConfig->isSegmentFirstResource = false;
    imageProcessorConfig->isPipeQueueRequired = true;
    imageProcessorConfig->queuingFlag = QueuingFlag::ENQUEUE;

    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersisterBuffer);
    resourceList.push_back(imageRetrieverBuffer_);
    resourceList.push_back(imageProcessorConfig);

    ON_CALL(*scanPipeline_, getResourceList(_)).WillByDefault(Return(resourceList));

}

void GivenAConnectedCopyPipelineStandardOfJupiter::TearDown()
{
    GivenANewCopyPipelineStandard::TearDown();
}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiter, WhenReprintExecutionModeCalledForJupiter_ItReprintsSuccessfully)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    auto dummyPipeQueue =dune::job::PipeQueueFactory<ImageContainer>::createPipeQueue(true,"/tmp", 0);

    jobTicket->setExecutionMode(dune::job::ExecutionMode::RERUN);
    jobTicket->setPersistentPipePath(dummyPipeQueue->getPersistentPath());
    
    jobTicket->getIntent()->setAutoRotate(true);
    
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);

    ASSERT_NE(nullptr, pipelineBuilder);

    // Expected calls.
    EXPECT_CALL(*imageRetrieverIntent_, setPerformAutoRotation(true)).Times(AtLeast(1));
    EXPECT_CALL(*imageRetrieverIntent_, setAutoRotationTolerance(14)).Times(AtLeast(1));

    std::shared_ptr<dune::imaging::Resources::SequencingParams> sequencingParams;
    std::shared_ptr<dune::imaging::Resources::SequencingParams> sequencingParams1{std::make_shared<dune::imaging::Resources::SequencingParams>()};

    EXPECT_CALL(*imageRetrieverIntent_, setSequencingParams(_)).WillRepeatedly(
        testing::Invoke([this, &sequencingParams](std::shared_ptr<dune::imaging::Resources::SequencingParams> value) -> void {
            sequencingParams = value;
        })
    );

    ON_CALL(*imageRetrieverIntent_, getSequencingParams()).WillByDefault(Return(sequencingParams1)); 

    PipelineBuilderBase::ResourceInstanceProxiesSection sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceServiceId(), imageRetrieverId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), printDeviceId_);
    EXPECT_EQ(sequencingParams1->updateDetails, true);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiter, WhenRerunExecutionModeCalledForJupiterAndPersistedPipeDoesnotexists_FailTheJob)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);

    jobTicket->setExecutionMode(dune::job::ExecutionMode::RERUN);
    jobTicket->setPersistentPipePath("/tmp/nonexistentpipe/path");

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    
    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    
    EXPECT_EQ(0, sections.size());
    EXPECT_EQ(dune::job::CompletionStateType::FAILED,jobTicket->getCompletionState());
    EXPECT_EQ(false, jobTicket->isPrintAlignmentChangeRequired());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiter, WhenPipleLineConfiguredForJupiter_ItCreatesAPersistentPipe)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    std::shared_ptr<IEnqueueIntf>  pipeEnque;
    std::shared_ptr<IDequeueIntf> pipeDequeue;

    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeEnque](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {

                pipeEnque = pipe_value;

            }));
    
    EXPECT_CALL(*imageRetrieverTicket_, setDequeueInterface(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeDequeue](std::shared_ptr<IDequeueIntf>  pipe_value) -> void {

                pipeDequeue = pipe_value;

            }));

    jobTicket->getIntent()->setGeneratePreview(true);
    scanPipeline_->scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->scanDiskBuffering = true;
    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::JOBBUILD);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    
    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(4, resources.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());//DiskBuffering persister
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imageRetrieverTicket_.get());//DiskBuffering retriever
    EXPECT_EQ(resources[3]->getResourceTicket().get(), imageProcessorTicket_.get());

    pipeEnque->closeForEnqueuing();
    pipeDequeue->closeForDequeuing();
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());
    resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(2, second_section.size());
    
    boost::filesystem::path persistentPath(jobTicket->getPersistentPipePath());
    EXPECT_EQ(jobTicket->getStorePath(),persistentPath.parent_path());
    //Verify that Image is persisted fine and can be reloaded
    ASSERT_NO_THROW(dune::job::PipeQueueFactory<ImageContainer>::createPipeQueue(jobTicket->getPersistentPipePath()));
}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiter, WhenPipleLineConfiguredForJupiterEditPreview_ThePreviewPathIsUpdated)
{
    auto uid = dune::framework::core::Uuid{"557c10b7-e752-45a3-80c0-7e604f7af170"};
    auto jobTicket = std::make_shared<CopyJobTicket>();
    jobTicket->setMediaInterface(mediaInterface_.get());
    auto jobTicketHandler = jobTicket->getHandler();

    auto pageTicketHandler =  jobTicketHandler->addPage(uid);

    std::shared_ptr<dune::copy::Jobs::Copy::ICopyPageTicket> pageTicket = std::static_pointer_cast<dune::copy::Jobs::Copy::ICopyPageTicket>(jobTicket->getPage(uid));
    std::shared_ptr<dune::imaging::types::IImagingIntent> imagingIntent =
        std::make_shared<dune::imaging::types::ImagingIntent>();
    
    auto newBrightnessIntent = std::make_shared<dune::imaging::types::BrightnessIntent>();
    newBrightnessIntent->brightness = 10;
    imagingIntent->setBrightnessIntent(newBrightnessIntent);
    pageTicket->setImagingIntent(imagingIntent);

    ASSERT_NE(nullptr, jobTicket);
    std::shared_ptr<IEnqueueIntf>  pipeEnque;
    std::shared_ptr<IDequeueIntf> pipeDequeue;

    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeEnque](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {

                pipeEnque = pipe_value;

            }));
    
    EXPECT_CALL(*imageRetrieverTicket_, setDequeueInterface(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeDequeue](std::shared_ptr<IDequeueIntf>  pipe_value) -> void {

                pipeDequeue = pipe_value;

            }));

    jobTicket->getIntent()->setGeneratePreview(true);
    scanPipeline_->scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->scanDiskBuffering = true;
    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::JOBBUILD);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    
    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(4, resources.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());//DiskBuffering persister
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imageRetrieverTicket_.get());//DiskBuffering retriever
    EXPECT_EQ(resources[3]->getResourceTicket().get(), imageProcessorTicket_.get());

    pipeEnque->closeForEnqueuing();
    pipeDequeue->closeForDequeuing();
    // jobTicket->setStorePath("./testResources/557c10b7-e752-45a3-80c0-7e604f7af170/EditPreviewImage.jpeg");
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());
    resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(2, second_section.size());
    
    boost::filesystem::path persistentPath(jobTicket->getPersistentPipePath());
    EXPECT_EQ(jobTicket->getStorePath(),persistentPath.parent_path());
    //Verify that Image is persisted fine and can be reloaded
    ASSERT_NO_THROW(dune::job::PipeQueueFactory<ImageContainer>::createPipeQueue(jobTicket->getPersistentPipePath()));

}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiter, WhenLfpPipelineIsBuiltForPreview_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;

    ASSERT_NE(nullptr, jobTicket);
    jobTicket->getIntent()->setGeneratePreview(true);

    //Activate scanDiskBuffering in the mocked config.
    scanPipeline_->scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->scanDiskBuffering = true;

    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))
        .WillRepeatedly(
            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {
                notificationStrat = value;
            }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(4, resources.size());
    EXPECT_EQ(4, resourcesTicket.size());

    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());//DiskBuffering persister
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imageRetrieverTicket_.get());//DiskBuffering retriever
    EXPECT_EQ(resourcesTicket[2].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_RETRIEVER_BUFFERING);// Because the scan disk buffering is active, the image retriever is of the buffering type
    EXPECT_EQ(resources[3]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resourcesTicket[3].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiter, WhenBasicPipelineIsIntialize_ThenScannerResourceIsAdded)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onInitialize();

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];

    EXPECT_EQ(1, resources.size());
    EXPECT_EQ(true, jobTicket->getAllPromptsCompleted());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiter, WhenStageIsFinishedAndExecutionIsNormalAfterResume_ThenResourcesListIsEmpty)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    std::shared_ptr<IEnqueueIntf> pipeEnqueue;
    std::shared_ptr<IDequeueIntf> pipeDequeue;

    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeEnqueue](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {

                pipeEnqueue = pipe_value;

            }));
    
    EXPECT_CALL(*imageRetrieverTicket_, setDequeueInterface(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeDequeue](std::shared_ptr<IDequeueIntf>  pipe_value) -> void {

                pipeDequeue = pipe_value;

            }));

    jobTicket->getIntent()->setGeneratePreview(true);
    scanPipeline_->scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->scanDiskBuffering = true;
    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::JOBBUILD);
    jobTicket->getIntent()->setAutoRotate(true);

    EXPECT_CALL(*imageRetrieverIntent_, setPerformAutoRotation(true)).Times(AtLeast(2)); // One for normal execution, one for Retry.

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    
    // Build prepare segment.
    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    pipeEnqueue->closeForEnqueuing();
    pipeDequeue->closeForDequeuing();

    // Build final segment.
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    // Expected 2 sections.
    EXPECT_EQ(2, sections.size());
    
    boost::filesystem::path persistentPath(jobTicket->getPersistentPipePath());
    EXPECT_EQ(jobTicket->getStorePath(),persistentPath.parent_path());
    
    // Prepare pipelineBuilder for the retry.
    jobTicket->setExecutionMode(dune::job::ExecutionMode::RESUME);
    pipelineBuilder->retry();

    // Build final segment.
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    // Expected one section.
    EXPECT_EQ(1, sections.size());
    
    // ImageRetriever, PrintDevice.
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());

    // Normal execution after a retry.
    jobTicket->setExecutionMode(dune::job::ExecutionMode::NORMAL);
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    // No resources are pushed into the list ( ie the resource list is empty ).
    EXPECT_EQ(0, sections.size());
}


TEST_F(GivenAConnectedCopyPipelineStandardOfJupiter, WhenPipelineConfiguredForLFP_ItCreatesAPersistentPipe_AndThenResume)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    std::shared_ptr<IEnqueueIntf>  pipeEnque;
    std::shared_ptr<IDequeueIntf> pipeDequeue;

    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeEnque](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {

                pipeEnque = pipe_value;

            }));
    
    EXPECT_CALL(*imageRetrieverTicket_, setDequeueInterface(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeDequeue](std::shared_ptr<IDequeueIntf>  pipe_value) -> void {

                pipeDequeue = pipe_value;

            }));

    jobTicket->getIntent()->setGeneratePreview(true);
    scanPipeline_->scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->scanDiskBuffering = true;
    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::JOBBUILD);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    
    //Build prepare segment
    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(4, resources.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());//DiskBuffering persister
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imageRetrieverTicket_.get());//DiskBuffering retriever
    EXPECT_EQ(resources[3]->getResourceTicket().get(), imageProcessorTicket_.get());

    pipeEnque->closeForEnqueuing();
    pipeDequeue->closeForDequeuing();

    //Build final segment
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    //Expected 2 sections
    EXPECT_EQ(2, sections.size());
    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreatorImageRetriever;

    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreatorImageRetriever](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreatorImageRetriever = pipelineMemoryClientCreator_value;

            }));
    
    //First section --> ImageRetriever, ImageProcessor, Imagepersister
    resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imagePersisterTicket_.get());

    //Second section --> ImageRetriever, PrintDevice
    resources = sections[1];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), printDeviceTicket_.get());
    
    boost::filesystem::path persistentPath(jobTicket->getPersistentPipePath());
    EXPECT_EQ(jobTicket->getStorePath(),persistentPath.parent_path());
    
    //Verify that Image is persisted fine and can be reloaded
    ASSERT_NO_THROW(dune::job::PipeQueueFactory<ImageContainer>::createPipeQueue(jobTicket->getPersistentPipePath()));

    // Prepare pipelineBuilder for the retry.
    jobTicket->setExecutionMode(dune::job::ExecutionMode::RETRY);
    pipelineBuilder->retry();

    //Build final segment
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    //Expected one sections
    EXPECT_EQ(1, sections.size());
    
    //ImageRetriever, PrintDevice
    resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), printDeviceTicket_.get());
    EXPECT_EQ(resources[0]->getKeep(), true );
    EXPECT_EQ(resources[1]->getKeep(), true );
}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiter, WhenStageIsFinishedAndExecutionIsNormalAfterRetry_ThenResourcesListIsEmpty)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    std::shared_ptr<IEnqueueIntf> pipeEnqueue;
    std::shared_ptr<IDequeueIntf> pipeDequeue;

    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeEnqueue](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {

                pipeEnqueue = pipe_value;

            }));
    
    EXPECT_CALL(*imageRetrieverTicket_, setDequeueInterface(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeDequeue](std::shared_ptr<IDequeueIntf>  pipe_value) -> void {

                pipeDequeue = pipe_value;

            }));

    jobTicket->getIntent()->setGeneratePreview(true);
    scanPipeline_->scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->scanDiskBuffering = true;
    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::JOBBUILD);
    jobTicket->getIntent()->setAutoRotate(true);

    EXPECT_CALL(*imageRetrieverIntent_, setPerformAutoRotation(true)).Times(AtLeast(2)); // One for normal execution, one for Retry.

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    
    // Build prepare segment.
    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    pipeEnqueue->closeForEnqueuing();
    pipeDequeue->closeForDequeuing();

    // Build final segment.
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    // Expected 2 sections.
    EXPECT_EQ(2, sections.size());
    
    boost::filesystem::path persistentPath(jobTicket->getPersistentPipePath());
    EXPECT_EQ(jobTicket->getStorePath(),persistentPath.parent_path());
    
    // Prepare pipelineBuilder for the retry.
    jobTicket->setExecutionMode(dune::job::ExecutionMode::RETRY);
    pipelineBuilder->retry();

    // Build final segment.
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    // Expected one section.
    EXPECT_EQ(1, sections.size());
    
    // ImageRetriever, PrintDevice.
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());

    // Normal execution after a retry.
    jobTicket->setExecutionMode(dune::job::ExecutionMode::NORMAL);
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    // No resources are pushed into the list ( ie the resource list is empty ).
    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiter, WhenPipelineConfiguredForLFP_ItCreatesAPersistentPipe_AndThenRetry)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    std::shared_ptr<IEnqueueIntf>  pipeEnque;
    std::shared_ptr<IDequeueIntf> pipeDequeue;

    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeEnque](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {

                pipeEnque = pipe_value;

            }));
    
    EXPECT_CALL(*imageRetrieverTicket_, setDequeueInterface(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeDequeue](std::shared_ptr<IDequeueIntf>  pipe_value) -> void {

                pipeDequeue = pipe_value;

            }));

    jobTicket->getIntent()->setGeneratePreview(true);
    scanPipeline_->scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->scanDiskBuffering = true;
    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::JOBBUILD);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    
    //Build prepare segment
    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(4, resources.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());//DiskBuffering persister
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imageRetrieverTicket_.get());//DiskBuffering retriever
    EXPECT_EQ(resources[3]->getResourceTicket().get(), imageProcessorTicket_.get());

    pipeEnque->closeForEnqueuing();
    pipeDequeue->closeForDequeuing();

    //Build final segment
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    //Expected 2 sections
    EXPECT_EQ(2, sections.size());
    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreatorImageRetriever;

    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreatorImageRetriever](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreatorImageRetriever = pipelineMemoryClientCreator_value;

            }));
    
    //First section --> ImageRetriever, ImageProcessor, Imagepersister
    resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imagePersisterTicket_.get());

    //Second section --> ImageRetriever, PrintDevice
    resources = sections[1];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), printDeviceTicket_.get());
    
    boost::filesystem::path persistentPath(jobTicket->getPersistentPipePath());
    EXPECT_EQ(jobTicket->getStorePath(),persistentPath.parent_path());
    
    //Verify that Image is persisted fine and can be reloaded
    ASSERT_NO_THROW(dune::job::PipeQueueFactory<ImageContainer>::createPipeQueue(jobTicket->getPersistentPipePath()));

    // Prepare pipelineBuilder for the retry.
    jobTicket->setExecutionMode(dune::job::ExecutionMode::RETRY);
    pipelineBuilder->retry();

    //Build final segment
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    //Expected one sections
    EXPECT_EQ(1, sections.size());
    
    //ImageRetriever, PrintDevice
    resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), printDeviceTicket_.get());
    EXPECT_EQ(resources[0]->getKeep(), true );
    EXPECT_EQ(resources[1]->getKeep(), true );
}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiter, WhenJupiterPipelineIsBuiltForScanCalibration_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::MDF);
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::JOBBUILD);
    jobTicket->setScanCalibrationType(dune::imaging::types::ScanCalibrationType::SCANNER_USER_CALIBRATION);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, true, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(1, resources.size());
    EXPECT_EQ(1, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
};

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiter, BackgroundRemovalAutoHPOperationInImageProcessor)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    ASSERT_NE(nullptr, jobTicket);    

    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))
        .WillRepeatedly(
            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {
                notificationStrat = value;
            }));
    
    ON_CALL(*scanPipeline_, getResourceList(_)).WillByDefault(Return(resourceList));
    
    scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->imageQuality = true; // required for setupImageProcessor to be called

    MockIScannerCapabilities mockScanCap;
    jobTicket->setScanCapabilitiesInterface(&mockScanCap);
    ON_CALL(*scanPipeline_, getScanCapabilitiesInterface()).WillByDefault(Return(&mockScanCap));
    EXPECT_CALL(mockScanCap, isImagingOperationSupported(_, _))
        .WillRepeatedly(DoAll(SetArgReferee<1>(false), Return(APIResult::OK)));

    jobTicket->getIntent()->setBackgroundColorRemoval(true);
    jobTicket->getIntent()->setOriginalMediaType(dune::scan::types::OriginalMediaType::DARK_BLUEPRINTS);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    EXPECT_CALL(*imageProcessorIntent_, setImageQualityValues(_))
        .WillOnce([](std::shared_ptr<dune::imaging::types::ImageQualityProcessingTableT> valuesTable) {
            ASSERT_EQ(valuesTable->backgroundRemovalType, dune::imaging::types::BackgroundRemovalType::BGREM_AUTOHP);
        });
    
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(4, resources.size());
    EXPECT_EQ(4, resourcesTicket.size());

    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());//DiskBuffering persister
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imageRetrieverTicket_.get());//DiskBuffering retriever
    EXPECT_EQ(resourcesTicket[2].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_RETRIEVER_BUFFERING);// Because the scan disk buffering is active, the image retriever is of the buffering type
    EXPECT_EQ(resources[3]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resourcesTicket[3].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

class GivenAConnectedCopyPipelineStandardOfJupiterInDirectCopy :public GivenANewCopyPipelineStandard
{
  public:

    GivenAConnectedCopyPipelineStandardOfJupiterInDirectCopy() {};

    virtual void SetUp() override;

    virtual void TearDown() override;

    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> imageRetrieverBuffer_{nullptr};
};

void GivenAConnectedCopyPipelineStandardOfJupiterInDirectCopy::SetUp()
{
    productTestFileName = "./testResources/CopyPipelineStandardJupiter.json";
    GivenANewCopyPipelineStandard::SetUp();

    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    //Set direct copy behaviour
    ON_CALL(mockICopyAdapter_, getCopyMode()).WillByDefault(Return(dune::cdm::copy_1::configuration::CopyMode::printWhileScanning));
    //Fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}

void GivenAConnectedCopyPipelineStandardOfJupiterInDirectCopy::TearDown()
{
    GivenANewCopyPipelineStandard::TearDown();
}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiterInDirectCopy, WhenLfpPipelineIsBuilt_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->getIntent()->setGeneratePreview(true);
    scanPipeline_->scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->scanDiskBuffering = true;
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::JOBBUILD);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(4, sections.size());

    //First section --> ScanDevice, ImagePersisterDB, (pipeTee) - ImageRetrieverDB, ImageProcessor
    //                                                          - ImageRetrieverDB, ImageProcessor, ImagePersister
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());
    
    //Second section --> (pipeTee) - ImageRetrieverDB, ImageProcessorPreview
    resources = sections[1];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());

    //Third section --> (pipeTee) - ImageRetrieverDB, ImageProcessor, ImagePersister
    resources = sections[2];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imagePersisterTicket_.get());

    //Last section --> ImageRetriever, PrintDevice
    resources = sections[3];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), printDeviceTicket_.get());

    //Build final segment
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    //All resources were set in the pipeline in the prepare segment, so when the final segment is built, we dont need to add any resource
    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiterInDirectCopy, WhenPipelineConfiguredForLFP_ItCreatesAPersistentPipe_AndThenRetry)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    std::shared_ptr<IEnqueueIntf>  pipeEnque;
    std::shared_ptr<IDequeueIntf> pipeDequeue;

    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeEnque](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {

                pipeEnque = pipe_value;

            }));
    
    EXPECT_CALL(*imageRetrieverTicket_, setDequeueInterface(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeDequeue](std::shared_ptr<IDequeueIntf>  pipe_value) -> void {

                pipeDequeue = pipe_value;

            }));

    jobTicket->getIntent()->setGeneratePreview(true);
    scanPipeline_->scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->scanDiskBuffering = true;
    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::JOBBUILD);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    
    //Build prepare segment
    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(4, sections.size());

    //First section --> ScanDevice, ImagePersisterDB, (pipeTee) - ImageRetrieverDB, ImageProcessor
    //                                                          - ImageRetrieverDB, ImageProcessor, ImagePersister
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());
    
    //Second section --> (pipeTee) - ImageRetrieverDB, ImageProcessorPreview
    resources = sections[1];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());

    //Third section --> (pipeTee) - ImageRetrieverDB, ImageProcessor, ImagePersister
    resources = sections[2];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imagePersisterTicket_.get());

    //Last section --> ImageRetriever, PrintDevice
    resources = sections[3];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), printDeviceTicket_.get());

    pipeEnque->closeForEnqueuing();
    pipeDequeue->closeForDequeuing();

    //Build final segment
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    //All resources were set in the pipeline in the prepare segment, so when the final segment is built, we dont need to add any resource
    EXPECT_EQ(0, sections.size());
    
    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreatorImageRetriever;

    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreatorImageRetriever](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreatorImageRetriever = pipelineMemoryClientCreator_value;

            }));
    
    boost::filesystem::path persistentPath(jobTicket->getPersistentPipePath());
    EXPECT_EQ(jobTicket->getStorePath(),persistentPath.parent_path());
    
    //Verify that Image is persisted fine and can be reloaded
    ASSERT_NO_THROW(dune::job::PipeQueueFactory<ImageContainer>::createPipeQueue(jobTicket->getPersistentPipePath()));

    // Prepare pipelineBuilder for the retry.
    jobTicket->setExecutionMode(dune::job::ExecutionMode::RETRY);
    pipelineBuilder->retry();

    //Build final segment
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    //Expected one sections
    EXPECT_EQ(1, sections.size());
    
    //ImageRetriever, PrintDevice
    resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), printDeviceTicket_.get());
    EXPECT_EQ(resources[0]->getKeep(), true );
    EXPECT_EQ(resources[1]->getKeep(), true );
}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiterInDirectCopy, WhenPipelineConfiguredForLFP_ItCreatesAPersistentPipe_AndThenResume)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    std::shared_ptr<IEnqueueIntf>  pipeEnque;
    std::shared_ptr<IDequeueIntf> pipeDequeue;

    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeEnque](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {

                pipeEnque = pipe_value;

            }));
    
    EXPECT_CALL(*imageRetrieverTicket_, setDequeueInterface(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeDequeue](std::shared_ptr<IDequeueIntf>  pipe_value) -> void {

                pipeDequeue = pipe_value;

            }));

    jobTicket->getIntent()->setGeneratePreview(true);
    scanPipeline_->scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->scanDiskBuffering = true;
    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::JOBBUILD);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    
    //Build prepare segment
    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(4, sections.size());

    //First section --> ScanDevice, ImagePersisterDB, (pipeTee) - ImageRetrieverDB, ImageProcessor
    //                                                          - ImageRetrieverDB, ImageProcessor, ImagePersister
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());
    
    //Second section --> (pipeTee) - ImageRetrieverDB, ImageProcessorPreview
    resources = sections[1];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());

    //Third section --> (pipeTee) - ImageRetrieverDB, ImageProcessor, ImagePersister
    resources = sections[2];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imagePersisterTicket_.get());

    //Last section --> ImageRetriever, PrintDevice
    resources = sections[3];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), printDeviceTicket_.get());

    pipeEnque->closeForEnqueuing();
    pipeDequeue->closeForDequeuing();

    //Build final segment
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    //All resources were set in the pipeline in the prepare segment, so when the final segment is built, we dont need to add any resource
    EXPECT_EQ(0, sections.size());
    
    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreatorImageRetriever;

    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreatorImageRetriever](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreatorImageRetriever = pipelineMemoryClientCreator_value;

            }));
    
    boost::filesystem::path persistentPath(jobTicket->getPersistentPipePath());
    EXPECT_EQ(jobTicket->getStorePath(),persistentPath.parent_path());
    
    //Verify that Image is persisted fine and can be reloaded
    ASSERT_NO_THROW(dune::job::PipeQueueFactory<ImageContainer>::createPipeQueue(jobTicket->getPersistentPipePath()));

    // Prepare pipelineBuilder for the retry.
    jobTicket->setExecutionMode(dune::job::ExecutionMode::RESUME);
    pipelineBuilder->retry();

    //Build final segment
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    //Expected one sections
    EXPECT_EQ(1, sections.size());
    
    //ImageRetriever, PrintDevice
    resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(resources[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resources[1]->getResourceTicket().get(), printDeviceTicket_.get());
    EXPECT_EQ(resources[0]->getKeep(), true );
    EXPECT_EQ(resources[1]->getKeep(), true );
}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiterInDirectCopy, WhenPipelineConfiguredForLFPWithPersistentPipe_withInterrupt) {

    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);
    std::shared_ptr<IEnqueueIntf>  pipeEnque;
    std::shared_ptr<IDequeueIntf> pipeDequeue;

    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeEnque](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {

                pipeEnque = pipe_value;

            }));
    
    EXPECT_CALL(*imageRetrieverTicket_, setDequeueInterface(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipeDequeue](std::shared_ptr<IDequeueIntf>  pipe_value) -> void {

                pipeDequeue = pipe_value;

            }));

    jobTicket->getIntent()->setGeneratePreview(true);
    scanPipeline_->scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->scanDiskBuffering = true;
    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::JOBBUILD);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    
    //Build prepare segment
    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(4, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    resources = sections[1];
    EXPECT_EQ(2, resources.size());
    resources = sections[2];
    EXPECT_EQ(3, resources.size());
    resources = sections[3];
    EXPECT_EQ(2, resources.size());

    pipeEnque->closeForEnqueuing();
    pipeDequeue->closeForDequeuing();
    
    //Build final segment
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    //All resources were set in the pipeline in the prepare segment, so when the final segment is built, we dont need to add any resource
    EXPECT_EQ(0, sections.size());
    
    auto resourcesBeforeInterrupt = pipelineBuilder->getAllResources();

    //Interrupt the pipeline
    pipelineBuilder->interrupt();
   
    // Interrupt should add 2 resources to the allResources vector
    auto resourcesAfterInterrupt = pipelineBuilder->getAllResources();
    EXPECT_EQ(resourcesBeforeInterrupt.size() + 2, resourcesAfterInterrupt.size());
}

class GivenAConnectedCopyPipelineStandardOfJupiterWithMediaHandlingConfigured : public GivenAConnectedCopyPipelineStandardOfJupiter
{
public:
    virtual void SetUp() override;
    virtual void TearDown() override;

    std::shared_ptr<MockIMediaHandlingMgr> mockIMediaHandlingMgr_{nullptr};
};

void GivenAConnectedCopyPipelineStandardOfJupiterWithMediaHandlingConfigured::SetUp()
{
    GivenAConnectedCopyPipelineStandardOfJupiter::SetUp();
    mockIMediaHandlingMgr_ = std::make_shared<MockIMediaHandlingMgr>();
    services_.mediaHandlingMgr = mockIMediaHandlingMgr_.get();
}

void GivenAConnectedCopyPipelineStandardOfJupiterWithMediaHandlingConfigured::TearDown()
{
    GivenAConnectedCopyPipelineStandardOfJupiter::TearDown();
}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiterWithMediaHandlingConfigured,WhenConfigOfResourceHasDoMediaHandlingCheckToFalseAndOnBuildPipelineIsCalled_ThenNoMediaHandlingIsSetInImageRetrieverIntentAndbuildPipelineIsBuildedOK)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);
    jobTicket->getIntent()->setGeneratePreview(true);

    //Activate scanDiskBuffering in the mocked config.
    scanPipeline_->scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->scanDiskBuffering = true;
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(4, resources.size());
    EXPECT_EQ(4, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());//DiskBuffering persister
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imageRetrieverTicket_.get());//DiskBuffering retriever
    EXPECT_EQ(resourcesTicket[2].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_RETRIEVER_BUFFERING);// Because the scan disk buffering is active, the image retriever is of the buffering type
    EXPECT_EQ(resources[3]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resourcesTicket[3].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfJupiterWithMediaHandlingConfigured,WhenConfigOfResourceHasDoMediaHandlingCheckToTrueAndOnBuildPipelineIsCalled_ThenMediaHandlingIsSetInImageRetrieverIntentAndbuildPipelineIsBuildedOK)
{
    imageRetrieverBuffer_->doMediaHandlingCheck = true;
    EXPECT_CALL(*imageRetrieverTicket_, getIntent()).WillRepeatedly(Return(imageRetrieverIntent_));
    EXPECT_CALL(*imageRetrieverIntent_, setMediaPointers(mediaInterface_.get(), mediaSettingsInterface_.get(), mediaInfoInterface_.get(), mockIMediaHandlingMgr_.get())).Times(1);

    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);
    jobTicket->getIntent()->setGeneratePreview(true);

    //Activate scanDiskBuffering in the mocked config.
    scanPipeline_->scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->scanDiskBuffering = true;
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(4, resources.size());
    EXPECT_EQ(4, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());//DiskBuffering persister
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(resources[2]->getResourceTicket().get(), imageRetrieverTicket_.get());//DiskBuffering retriever
    EXPECT_EQ(resourcesTicket[2].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_RETRIEVER_BUFFERING);// Because the scan disk buffering is active, the image retriever is of the buffering type
    EXPECT_EQ(resources[3]->getResourceTicket().get(), imageProcessorTicket_.get());
    EXPECT_EQ(resourcesTicket[3].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PROCESSOR);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyPipelineStandardOfEnterprise : Add test cases related to Enterprise here
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyPipelineStandardOfEnterprise :public GivenANewCopyPipelineStandard
{
  public:

    GivenAConnectedCopyPipelineStandardOfEnterprise() {};
    std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> resourceList;
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> scanDeviceConfig1 = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> imagePersister1 = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> scanDeviceConfig2 = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT> imagePersister2 = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    
    virtual void SetUp() override;

    virtual void TearDown() override;
};

void GivenAConnectedCopyPipelineStandardOfEnterprise::SetUp()
{
    productTestFileName = "./testResources/CopyPipelineStandardEnterprise.json";
    GivenANewCopyPipelineStandard::SetUp();

    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
    scanDeviceConfig1->resourceId = dune::scan::Jobs::Scan::ResourceName::SCANDEVICE;
    scanDeviceConfig1->jobletBoudary = dune::job::JobletBoundary::UNDEFINED;
    scanDeviceConfig1->setKeep = true;
    scanDeviceConfig1->isSegmentFirstResource = true;
    scanDeviceConfig1->pipeType = dune::scan::Jobs::Scan::PipeObjectType::IMAGECONTAINER;
    scanDeviceConfig1->queuingFlag = QueuingFlag::BOTH;
    scanDeviceConfig1->isPipeQueueRequired = true;
    scanDeviceConfig1->reusePipeQueue = false;
    scanDeviceConfig1->openForAppending = false;
    
    scanDeviceConfig2->resourceId = dune::scan::Jobs::Scan::ResourceName::SCANDEVICE;
    scanDeviceConfig2->jobletBoudary = dune::job::JobletBoundary::UNDEFINED;
    scanDeviceConfig2->setKeep = true;
    scanDeviceConfig2->isSegmentFirstResource = true;
    scanDeviceConfig2->pipeType = dune::scan::Jobs::Scan::PipeObjectType::IMAGECONTAINER;
    scanDeviceConfig2->queuingFlag = QueuingFlag::BOTH;
    scanDeviceConfig2->isPipeQueueRequired = true;
    scanDeviceConfig2->reusePipeQueue = false;
    scanDeviceConfig2->openForAppending = false;
    scanDeviceConfig2->reset = true;

    imagePersister1->resourceId = dune::scan::Jobs::Scan::ResourceName::IMAGEPERSISTER;
    imagePersister1->jobletBoudary = dune::job::JobletBoundary::UNDEFINED;
    imagePersister1->notificationStrategy = dune::imaging::types::NotificationStrategy::ON_STARTED;
    imagePersister1->toPipe = dune::scan::Jobs::Scan::ResourceName::IMAGERETRIEVER;
    imagePersister1->setKeep = true;
    imagePersister1->isSegmentFirstResource = false;
    imagePersister1->pipeType = dune::scan::Jobs::Scan::PipeObjectType::IMAGECONTAINER;
    imagePersister1->isPipeQueueRequired = true;
    imagePersister1->queuingFlag = QueuingFlag::ENQUEUE;
    imagePersister1->reusePipeQueue = true;
    imagePersister1->persistentPipe = true;
    imagePersister1->openForAppending = false;
    
    imagePersister2->resourceId = dune::scan::Jobs::Scan::ResourceName::IMAGEPERSISTER;
    imagePersister2->jobletBoudary = dune::job::JobletBoundary::START;
    imagePersister2->notificationStrategy = dune::imaging::types::NotificationStrategy::ON_STARTED;
    imagePersister2->toPipe = dune::scan::Jobs::Scan::ResourceName::IMAGERETRIEVER;
    imagePersister2->setKeep = true;
    imagePersister2->isSegmentFirstResource = false;
    imagePersister2->pipeType = dune::scan::Jobs::Scan::PipeObjectType::IMAGECONTAINER;
    imagePersister2->isPipeQueueRequired = true;
    imagePersister2->queuingFlag = QueuingFlag::ENQUEUE;
    imagePersister2->reusePipeQueue = true;
    imagePersister2->persistentPipe = true;
    imagePersister2->openForAppending = true;
    imagePersister2->reset = true;
    

    scanPipeline_->scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->scanDiskBuffering = true;

    ON_CALL(*scanPipeline_, getResourceList(_)).WillByDefault(Return(resourceList));
    multiPageSupportedFromFlatbed_ = true;
}

void GivenAConnectedCopyPipelineStandardOfEnterprise::TearDown()
{
    GivenANewCopyPipelineStandard::TearDown();
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenBasicPipelineIsIntialize_ThenScannerResourceIsAdded)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onInitialize();

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];

    EXPECT_EQ(1, resources.size());
    EXPECT_EQ(false, jobTicket->getAllPromptsCompleted());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenBasicPipelineIsIntializeAndExecutionModeIsRetriever_ThenScannerResourceIsNotAdded)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setExecutionMode(dune::job::ExecutionMode::RETRIEVE);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onInitialize();

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];

    EXPECT_EQ(0, resources.size());
    EXPECT_EQ(false, jobTicket->areNativeJobStatusAlertsEnabled());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenBasicPipelineOnJobCompletionWithNoScanNumberPages_ThenCompletedStateIsFailed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanNumberPages(0);
    jobTicket->setCompletionState(CompletionStateType::SUCCESS);
    jobTicket->setScanCalibrationType(dune::imaging::types::ScanCalibrationType::UNKNOWN);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    dune::job::JobCompletionPackage completionPackage;
    pipelineBuilder->onJobCompletion(completionPackage);

    EXPECT_EQ(CompletionStateType::FAILED, completionPackage.getCompletionState());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenBasicPipelineOnJobCompletionWithNoScanNumberPagesAndCalJobType_ThenJobStateNotChanged)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanNumberPages(0);
    jobTicket->setCompletionState(CompletionStateType::SUCCESS);
    jobTicket->setScanCalibrationType(dune::imaging::types::ScanCalibrationType::SCANNER_USER_CALIBRATION);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    dune::job::JobCompletionPackage completionPackage;
    pipelineBuilder->onJobCompletion(completionPackage);

    EXPECT_EQ(CompletionStateType::UNDEFINED, completionPackage.getCompletionState());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuilt_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);
    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);

    ON_CALL(*pageAssemblerResourceService_, getState()).WillByDefault(Return(dune::job::ResourceServiceStateType::ALLOCATABLE));
    ON_CALL(*printDeviceResourceService_, getState()).WillByDefault(Return(dune::job::ResourceServiceStateType::ALLOCATABLE));

    bool basicCopyMode = false;
    EXPECT_CALL(*pageAssemblerIntent_, setBasicCopyMode(_))
        .WillRepeatedly(
            testing::Invoke([this, &basicCopyMode](bool value) -> void {
                basicCopyMode = value;
            }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    pipelineBuilder->setSimulatorJob(false);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }
    
    EXPECT_EQ(1, first_section.size());
    EXPECT_EQ(2, second_section.size());
    EXPECT_EQ(3, resourcesTicket.size());

    EXPECT_EQ(first_section[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(second_section[0]->getResourceTicket().get(), pageAssemblerTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::PAGE_ASSEMBLER_SERVICE);
    EXPECT_EQ(second_section[1]->getResourceTicket().get(), printDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[2].resourceType, dune::job::IIntentsManager::ResourceType::PRINT_DEVICE_SERVICE);

    EXPECT_EQ(true, basicCopyMode);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltWithADFSource_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);

    ON_CALL(*pageAssemblerResourceService_, getState()).WillByDefault(Return(dune::job::ResourceServiceStateType::ALLOCATABLE));
    ON_CALL(*printDeviceResourceService_, getState()).WillByDefault(Return(dune::job::ResourceServiceStateType::ALLOCATABLE));

    bool basicCopyMode = false;
    EXPECT_CALL(*pageAssemblerIntent_, setBasicCopyMode(_))
        .WillRepeatedly(
            testing::Invoke([this, &basicCopyMode](bool value) -> void {
                basicCopyMode = value;
            }));

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    pipelineBuilder->setSimulatorJob(false);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }
    
    EXPECT_EQ(2, first_section.size());
    EXPECT_EQ(3, second_section.size());
    EXPECT_EQ(5, resourcesTicket.size());

    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_COMPLETED);
    EXPECT_EQ(jobTicket->getIntent()->getPrintingOrder(), dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);

    EXPECT_EQ(first_section[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(first_section[1]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(second_section[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resourcesTicket[2].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_RETRIEVER_PRINTING);
    EXPECT_EQ(second_section[1]->getResourceTicket().get(), pageAssemblerTicket_.get());
    EXPECT_EQ(resourcesTicket[3].resourceType, dune::job::IIntentsManager::ResourceType::PAGE_ASSEMBLER_SERVICE);
    EXPECT_EQ(second_section[2]->getResourceTicket().get(), printDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[4].resourceType, dune::job::IIntentsManager::ResourceType::PRINT_DEVICE_SERVICE);

    EXPECT_EQ(false, basicCopyMode);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltWithScanAhead_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);

    ON_CALL(*pageAssemblerResourceService_, getState()).WillByDefault(Return(dune::job::ResourceServiceStateType::NOT_ALLOCATABLE));
    ON_CALL(*printDeviceResourceService_, getState()).WillByDefault(Return(dune::job::ResourceServiceStateType::NOT_ALLOCATABLE));

    bool basicCopyMode = false;
    EXPECT_CALL(*pageAssemblerIntent_, setBasicCopyMode(_))
        .WillRepeatedly(
            testing::Invoke([this, &basicCopyMode](bool value) -> void {
                basicCopyMode = value;
            }));

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    pipelineBuilder->setSimulatorJob(false);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
    }
    
    EXPECT_EQ(2, first_section.size());
    EXPECT_EQ(3, second_section.size());
    EXPECT_EQ(5, resourcesTicket.size());

    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_COMPLETED);
    EXPECT_EQ(jobTicket->getIntent()->getPrintingOrder(), dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP);

    EXPECT_EQ(first_section[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(first_section[1]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(second_section[0]->getResourceTicket().get(), imageRetrieverTicket_.get());
    EXPECT_EQ(resourcesTicket[2].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_RETRIEVER_PRINTING);
    EXPECT_EQ(second_section[1]->getResourceTicket().get(), pageAssemblerTicket_.get());
    EXPECT_EQ(resourcesTicket[3].resourceType, dune::job::IIntentsManager::ResourceType::PAGE_ASSEMBLER_SERVICE);
    EXPECT_EQ(second_section[2]->getResourceTicket().get(), printDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[4].resourceType, dune::job::IIntentsManager::ResourceType::PRINT_DEVICE_SERVICE);

    EXPECT_EQ(false, basicCopyMode);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltWithCollate_ThenResourcesAreNotOverriddenToSetKeepTrue)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setInputPlexMode(dune::imaging::types::Plex::SIMPLEX);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());
    EXPECT_EQ(true, jobTicket->getAllPromptsCompleted());

    PipelineBuilderBase::ResourceInstanceProxies first_section = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section = sections[1];
    for (int i = 0; i < (int)first_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, first_section[i]->getResourceServiceId().c_str());
        EXPECT_EQ(first_section[i]->getKeep(), false);
    }
    for (int i = 0; i < (int)second_section.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, second_section[i]->getResourceServiceId().c_str());
        EXPECT_EQ(second_section[i]->getKeep(), true);
    }
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuilt_FileFormatSetForImagePersister)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setCopies(2);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    dune::imaging::types::FileFormat fileFormat;
    EXPECT_CALL(*imagePersisterIntent_, setFileFormat(_))

        .WillRepeatedly(

            testing::Invoke([this, &fileFormat](dune::imaging::types::FileFormat value) -> void {

                fileFormat = value;

            }));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());
    
    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::UNCOMPRESSED);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuilt_ThenPipelineIsCorrectlyComposed_ForRetry)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);
    jobTicket->getIntent()->setCollate(dune::copy::SheetCollate::Collate);
    jobTicket->getIntent()->setCopies(2);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);

    ASSERT_NE(nullptr, pipelineBuilder);

    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(2, sections.size());


    jobTicket->setExecutionMode(dune::job::ExecutionMode::RETRY);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    auto first_section = sections[0];
    EXPECT_EQ(1, first_section.size());
    EXPECT_EQ(first_section[0]->getResourceServiceId(), printDeviceId_);

    jobTicket->setExecutionMode(dune::job::ExecutionMode::RETRY);
    EXPECT_CALL(*pageAssemblerTicket_, getCompletionState()).Times(1).WillRepeatedly(Return(CompletionStateType::FAILED));

    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    
    EXPECT_EQ(1, sections.size());

    first_section = sections[0];
    EXPECT_EQ(1, first_section.size());
    EXPECT_EQ(first_section[0]->getResourceServiceId(), printDeviceId_);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltFor2UpFlatbed_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setCopies(2);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());
    
    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::UNCOMPRESSED);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltForPreview_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setCopies(2);
    scanPipelineConfig_->pipelineBuilderConfig->previewSettings->refreshPreviewSupported = true;

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::PreviewStage;
                                            })
                                        ));
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillRepeatedly(::testing::SaveArg<1>(&resourcesTicket));

    // 2up - flatbed use case, prompt until user says done
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());
    
    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::UNCOMPRESSED);
    EXPECT_EQ(jobTicket->getPreviewMode(), false);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(jobTicket->getPreviewMode(), false);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    // One up Flatbed use case, one time exuction of resources
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::OneUp);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(jobTicket->getPreviewMode(), false);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(0, sections.size());
    EXPECT_EQ(jobTicket->getPreviewMode(), true);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), false);

    // Multi Flatbed 
    jobTicket->getIntent()->setPromptForMorePages(true);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());
    
    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::UNCOMPRESSED);
    EXPECT_EQ(jobTicket->getPreviewMode(), false);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(jobTicket->getPreviewMode(), false);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    // check for ADF duplex Mode 
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::ADF_DUPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    jobTicket->getIntent()->setPromptForMorePages(false);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());
    
    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::UNCOMPRESSED);
    EXPECT_EQ(jobTicket->getPreviewMode(), false);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(0, sections.size());
    EXPECT_EQ(jobTicket->getPreviewMode(), true);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), false);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltForBookModePreview_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::BOOKMODE);
    jobTicket->getIntent()->setCopies(2);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::PreviewStage;
                                            })
                                        ));
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillRepeatedly(::testing::SaveArg<1>(&resourcesTicket));

    // BOOK Mode - flatbed use case, prompt until user says done
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());
    
    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::UNCOMPRESSED);
    EXPECT_EQ(jobTicket->getPreviewMode(), false);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());
    resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());
    EXPECT_EQ(jobTicket->getPreviewMode(), false);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());
    resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());
    EXPECT_EQ(jobTicket->getPreviewMode(), false);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltForIDcardPreview_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    jobTicket->getIntent()->setCopies(2);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::MultiPreviewStage;
                                            })
                                        ));
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillRepeatedly(::testing::SaveArg<1>(&resourcesTicket));

    // BOOK Mode - flatbed use case, prompt until user says done
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());
    
    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::UNCOMPRESSED);
    EXPECT_EQ(jobTicket->getPreviewMode(), false);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());
    resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());
    EXPECT_EQ(jobTicket->getPreviewMode(), false);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);

    sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment);
    EXPECT_EQ(1, sections.size());
    resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());
    EXPECT_EQ(jobTicket->getPreviewMode(), false);
    EXPECT_EQ(jobTicket->isFirstScanStarted(), true);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltForIDCardCopy_ThenPipelineIsCorrectlyComposed)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    EXPECT_CALL(*mockIntentsManager_, updateResourceIntents(_, _)).WillOnce(::testing::SaveArg<1>(&resourcesTicket));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(2, resourcesTicket.size());

    EXPECT_EQ(resources[0]->getResourceTicket().get(), scanDeviceTicket_.get());
    EXPECT_EQ(resourcesTicket[0].resourceType, dune::job::IIntentsManager::ResourceType::SCAN_DEVICE_SERVICE);
    EXPECT_EQ(resources[1]->getResourceTicket().get(), imagePersisterTicket_.get());
    EXPECT_EQ(resourcesTicket[1].resourceType, dune::job::IIntentsManager::ResourceType::IMAGE_PERSISTER);

    auto scanDeviceTicket = std::static_pointer_cast<IScanDeviceTicket>(resources[0]->getResourceTicket());
    auto sdIntent = scanDeviceTicket->getIntent();

    auto imagePersisterTicket = std::static_pointer_cast<IImagePersisterTicket>(resources[1]->getResourceTicket());
    auto ipIntent = imagePersisterTicket->getIntent();
    EXPECT_EQ(ipIntent->getJpegHwEnable(), false);
    EXPECT_EQ(ipIntent->getJpegVqEnable(), false);

}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltForGlassMultiStage_ThenTenPagesAreScanned)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(Plex::SIMPLEX);
    jobTicket->getIntent()->setOutputPlexMode(Plex::SIMPLEX);
    jobTicket->getIntent()->setCopies(2);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    std::shared_ptr<IEnqueueIntf>  pipe;
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    // -> Stage::ScanFirstPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::UNCOMPRESSED);
    
    // Imagepersister queue's is closed for testing purpose to avoid the Fail related with ::reopenForAppending()
    // when the pipe is not closed
    pipe->closeForEnqueuing();
    
    for(uint32_t i=1; i< pipelineBuilder->getMaxFlatbedDuplexPages(); i++)
    {
        // -> Stage::ScanSecondPage
        resourceList.clear();
        resourceList.push_back(scanDeviceConfig2);
        resourceList.push_back(imagePersister2);
    
        ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
                ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                            std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                                {
                                                    resourceList_ = resourceList;
                                                    return dune::scan::Jobs::Scan::ScanStage::MultiScanStage;
                                                })
                                            ));
        sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedAddPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
        resources = sections[0];
        EXPECT_EQ(1, sections.size());
        EXPECT_EQ(2, resources.size());
        EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
        pipe->closeForEnqueuing();
    }
    //EXPECT_EQ(jobTicket->isFirstScanStarted(), false);
    
    // -> Stage::PrintAllPages
    resourceList.clear();
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FinishedFinalMultiScan;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());

    resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(pageAssemblerMemoryClientCreator_.get(), pipelineMemoryClientCreator);
    EXPECT_EQ(true, jobTicket->getAllPromptsCompleted());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltFor2UpFlatbed_Then10PagesAreScanned)
{
    
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    //jobTicket->getIntent()->setInputPlexMode(Plex::SIMPLEX);
    //jobTicket->getIntent()->setOutputPlexMode(Plex::SIMPLEX);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    std::shared_ptr<IEnqueueIntf>  pipe;
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // -> Stage::ScanFirstPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();
    
    for(uint32_t i=1; i< pipelineBuilder->getMaxFlatbedDuplexPages(); i++)
    {
    // -> Stage::ScanSecondPage
        resourceList.clear();
        resourceList.push_back(scanDeviceConfig2);
        resourceList.push_back(imagePersister2);
    
        ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
                ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                            std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                                {
                                                    resourceList_ = resourceList;
                                                    return dune::scan::Jobs::Scan::ScanStage::MultiScanStage;
                                                })
                                            ));
        sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedAddPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
        resources = sections[0];
        EXPECT_EQ(1, sections.size());
        EXPECT_EQ(2, resources.size());
        EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
        pipe->closeForEnqueuing();
    }
    //EXPECT_EQ(jobTicket->isFirstScanStarted(), false);

    // -> Stage::PrintAllPages
    resourceList.clear();
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FinishedFinalMultiScan;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());
    resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(true, jobTicket->getAllPromptsCompleted());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltFor2UpFlatbed_ThenCancelJobShoudlReleaseResources)
{
    
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    //jobTicket->getIntent()->setInputPlexMode(Plex::SIMPLEX);
   // jobTicket->getIntent()->setOutputPlexMode(Plex::SIMPLEX);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    std::shared_ptr<IEnqueueIntf>  pipe;
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // -> Stage::ScanFirstPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    EXPECT_EQ(pipelineBuilder->getCollateMode(), CollateMode::NONE);
    pipe->closeForEnqueuing();

    // -> Stage::ScanSecondPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig2);
    resourceList.push_back(imagePersister2);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::MultiScanStage;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedAddPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    resources = sections[0];
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();
    
    // -> Stage::PrintAllPages
    resourceList.clear();
    
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::Cancelled;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedAddPage, PromptResponseType::Response_03, SegmentType::FinalSegment);

    EXPECT_EQ(jobTicket->getCompletionState(), dune::job::CompletionStateType::CANCELED);
    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltForGlassFlatbed_ThenCancelJobShoudlReleaseResources)
{
    
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(Plex::SIMPLEX);
    jobTicket->getIntent()->setOutputPlexMode(Plex::SIMPLEX);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    std::shared_ptr<IEnqueueIntf>  pipe;
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // -> Stage::ScanFirstPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();

    // -> Stage::ScanSecondPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig2);
    resourceList.push_back(imagePersister2);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::MultiScanStage;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedAddPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    resources = sections[0];
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();
    
    // -> Stage::PrintAllPages
    resourceList.clear();
    
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::Cancelled;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedAddPage, PromptResponseType::Response_03, SegmentType::FinalSegment);

    EXPECT_EQ(jobTicket->getCompletionState(), dune::job::CompletionStateType::CANCELED);
    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltForDuplexOutputFlatbed_Then10PagesAreScanned)
{    
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(Plex::SIMPLEX);
    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    std::shared_ptr<IEnqueueIntf>  pipe;
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // -> Stage::ScanFirstPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    EXPECT_CALL(*scanPipelineBuilder_, setMultiScanPipeline(true)).Times(11);
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();

    for(uint32_t i=1; i< pipelineBuilder->getMaxFlatbedDuplexPages(); i++)
    {
    // -> Stage::ScanSecondPage
        resourceList.clear();
        resourceList.push_back(scanDeviceConfig2);
        resourceList.push_back(imagePersister2);
    
        ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
                ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                            std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                                {
                                                    resourceList_ = resourceList;
                                                    return dune::scan::Jobs::Scan::ScanStage::MultiScanStage;
                                                })
                                            ));
        sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedAddPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
        resources = sections[0];
        EXPECT_EQ(1, sections.size());
        EXPECT_EQ(2, resources.size());
        EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
        pipe->closeForEnqueuing();
    }
    //EXPECT_EQ(jobTicket->isFirstScanStarted(), false);

    // -> Stage::PrintAllPages
    resourceList.clear();
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FinishedFinalMultiScan;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());
    resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(pageAssemblerMemoryClientCreator_.get(), pipelineMemoryClientCreator);
    EXPECT_EQ(true, jobTicket->getAllPromptsCompleted());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltForDuplexInputFlatbed_Then10PagesAreScanned)
{    
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    std::shared_ptr<IEnqueueIntf>  pipe;
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // -> Stage::ScanFirstPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();

    for(uint32_t i=1; i<pipelineBuilder->getMaxFlatbedDuplexPages(); i++)
    {
        // -> Stage::ScanSecondPage
        resourceList.clear();
        resourceList.push_back(scanDeviceConfig2);
        resourceList.push_back(imagePersister2);
   
        ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
                ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                            std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                                {
                                                    resourceList_ = resourceList;
                                                    return dune::scan::Jobs::Scan::ScanStage::MultiScanStage;
                                                })
                                            ));
        sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedDuplexAddPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
        resources = sections[0];
        EXPECT_EQ(1, sections.size());
        EXPECT_EQ(2, resources.size());
        EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
        pipe->closeForEnqueuing();
    }
    ///EXPECT_EQ(jobTicket->isFirstScanStarted(), false);

    // -> Stage::PrintAllPages
    resourceList.clear();
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FinishedFinalMultiScan;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    EXPECT_EQ(1, sections.size());
    resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(pageAssemblerMemoryClientCreator_.get(), pipelineMemoryClientCreator);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltForDuplexOutputFlatbed_ThenCancelJobShoudlReleaseResources)
{
    
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(Plex::SIMPLEX);
    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    std::shared_ptr<IEnqueueIntf>  pipe;
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // -> Stage::ScanFirstPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();

    // -> Stage::ScanSecondPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig2);
    resourceList.push_back(imagePersister2);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::MultiScanStage;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedAddPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    resources = sections[0];
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();
    
    // -> Stage::PrintAllPages
    resourceList.clear();
    
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::Cancelled;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedAddPage, PromptResponseType::Response_03, SegmentType::FinalSegment);

    EXPECT_EQ(jobTicket->getCompletionState(), dune::job::CompletionStateType::CANCELED);
    EXPECT_EQ(0, sections.size());
    EXPECT_EQ(true, jobTicket->getAllPromptsCompleted());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltForIDCardFrontDoneThenEmptyDoneAndEmptyResources)
{
    
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(Plex::SIMPLEX);
    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setScanCaptureMode(dune::scan::types::ScanCaptureModeType::IDCARD);
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // -> Stage::ScanFirstPage
    resourceList.clear();
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::EmptyDone;
                                            })
                                        ));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);


    EXPECT_EQ(false, jobTicket->isFirstScanStarted());
    EXPECT_EQ(0, sections.size());
    EXPECT_EQ(true, jobTicket->getAllPromptsCompleted());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltForDuplexInputFlatbed_ThenCancelJobShoudlReleaseResources)
{
    
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    std::shared_ptr<IEnqueueIntf>  pipe;
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // -> Stage::ScanFirstPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();

    // -> Stage::ScanSecondPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig2);
    resourceList.push_back(imagePersister2);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::MultiScanStage;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedDuplexAddPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    resources = sections[0];
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();
    
    // -> Stage::PrintAllPages
    resourceList.clear();
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::Cancelled;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedDuplexAddPage, PromptResponseType::Response_03, SegmentType::FinalSegment);

    EXPECT_EQ(jobTicket->getCompletionState(), dune::job::CompletionStateType::CANCELED);
    EXPECT_EQ(0, sections.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltFor2UpFlatbed_ThenDoneShoudlFinishJob)
{
    
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);
    //jobTicket->getIntent()->setInputPlexMode(Plex::SIMPLEX);
   // jobTicket->getIntent()->setOutputPlexMode(Plex::SIMPLEX);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    std::shared_ptr<IEnqueueIntf>  pipe;
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // -> Stage::ScanFirstPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();

    // -> Stage::ScanSecondPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig2);
    resourceList.push_back(imagePersister2);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::MultiScanStage;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedAddPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    resources = sections[0];
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();
    
    // -> Stage::PrintAllPages
    resourceList.clear();
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FinishedFinalMultiScan;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedAddPage, PromptResponseType::Response_02, SegmentType::FinalSegment);

    //Job Should move to printing with done Response
    EXPECT_EQ(1, sections.size());
    resources = sections[0];
    EXPECT_EQ(3, resources.size());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenTicketModeIsRetrieve_CorrectResourcesAreAdded)
{
    auto dummyPipeQueue =dune::job::PipeQueueFactory<ImageContainer>::createPipeQueue(true,"/tmp", 0);

    auto jobTicket = std::make_shared<CopyJobTicket>();
    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");

    auto pipeMetaInfo = std::make_shared<dune::job::PipeMetaInfo>();
    dune::job::JobMetaInfoDataT data;
    data.lastPageMediaSize = dune::imaging::types::MediaSizeId::A4;
    data.captureMode   = dune::job::CaptureModeType::IDCARD;
    pipeMetaInfo->setJobMetaInfo(data);
    jobTicket->setInputPipeMetaInfo(pipeMetaInfo);

    auto jobIntent = jobTicket->getIntent();
    ASSERT_NE(nullptr, jobIntent);
    jobTicket->setExecutionMode(dune::job::ExecutionMode::RETRIEVE);
    jobTicket->setPersistentPipePath(dummyPipeQueue->getPersistentPath());

    ON_CALL(*pageAssemblerResourceService_, getState()).WillByDefault(Return(dune::job::ResourceServiceStateType::ALLOCATABLE));
    ON_CALL(*printDeviceResourceService_, getState()).WillByDefault(Return(dune::job::ResourceServiceStateType::ALLOCATABLE));

    bool basicCopyMode = false;
    EXPECT_CALL(*pageAssemblerIntent_, setBasicCopyMode(_))
        .WillRepeatedly(
            testing::Invoke([this, &basicCopyMode](bool value) -> void {
                basicCopyMode = value;
            }));
    
    EXPECT_CALL(*imageImporterIntent_, setRequestedImageType(_)).Times(0);
    EXPECT_CALL(*imageImporterIntent_, setImageSetter(_)).Times(0);

    EXPECT_CALL(*ipaDeviceTicket_, setEnqueue(_));
    EXPECT_CALL(*ipaDeviceTicket_, setDequeue(_));

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    pipelineBuilder->setSimulatorJob(false);

    auto sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    ASSERT_FALSE(sections.empty());
    EXPECT_EQ(1, sections.size());

    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    EXPECT_EQ(6, resources.size());

    EXPECT_EQ(resources[0]->getResourceServiceId(), imageImporterId_);
    EXPECT_EQ(resources[1]->getResourceServiceId(), ipaDeviceId_);
    EXPECT_EQ(resources[2]->getResourceServiceId(), imagePersisterId_);
    EXPECT_EQ(resources[3]->getResourceServiceId(), layoutFilterId_);
    EXPECT_EQ(resources[4]->getResourceServiceId(), pageAssemblerId_);
    EXPECT_EQ(resources[5]->getResourceServiceId(), printDeviceId_);
    
    EXPECT_EQ(false, basicCopyMode);
    EXPECT_EQ(dune::imaging::types::MediaSizeId::A4, jobTicket->getIntent()->getInputMediaSizeId());
    EXPECT_EQ(dune::scan::types::ScanCaptureModeType::IDCARD, jobTicket->getIntent()->getScanCaptureMode());
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltForSimplexFlatbed_ThenDoneShoudlFinishJob)
{
    
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(Plex::SIMPLEX);
    jobTicket->getIntent()->setOutputPlexMode(Plex::SIMPLEX);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    std::shared_ptr<IEnqueueIntf>  pipe;
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // -> Stage::ScanFirstPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();

    // -> Stage::ScanSecondPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig2);
    resourceList.push_back(imagePersister2);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::MultiScanStage;
                                            })
                                        ));
    
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedAddPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    resources = sections[0];
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();

    // -> Stage::PrintAllPages
    resourceList.clear();
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FinishedFinalMultiScan;
                                            })
                                        ));
    
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedAddPage, PromptResponseType::Response_02, SegmentType::FinalSegment);

    //Job Should move to printing with done Response
    EXPECT_EQ(1, sections.size());
    resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(pageAssemblerMemoryClientCreator_.get(), pipelineMemoryClientCreator);
  }

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltForDuplexOutput_ThenDoneShoudlFinishJob)
{
    
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(Plex::SIMPLEX);
    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    std::shared_ptr<IEnqueueIntf>  pipe;
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // -> Stage::ScanFirstPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();

    // -> Stage::ScanSecondPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig2);
    resourceList.push_back(imagePersister2);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::MultiScanStage;
                                            })
                                        ));
    
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedAddPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    resources = sections[0];
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();
    
    // -> Stage::PrintAllPages
    resourceList.clear();
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FinishedFinalMultiScan;
                                            })
                                        ));
    
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedAddPage, PromptResponseType::Response_02, SegmentType::FinalSegment);

    //Job Should move to printing with done Response
    EXPECT_EQ(1, sections.size());
    resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(pageAssemblerMemoryClientCreator_.get(), pipelineMemoryClientCreator);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltForDuplexInput_ThenDoneShoudlFinishJob)
{
    
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    std::shared_ptr<IEnqueueIntf>  pipe;
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // -> Stage::ScanFirstPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();

    // -> Stage::ScanSecondPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig2);
    resourceList.push_back(imagePersister2);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::MultiScanStage;
                                            })
                                        ));
    
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedDuplexAddPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    resources = sections[0];
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();

    // -> Stage::PrintAllPages
    resourceList.clear();
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FinishedFinalMultiScan;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedDuplexAddPage, PromptResponseType::Response_02, SegmentType::FinalSegment);

    //Job Should move to printing with done Response
    EXPECT_EQ(1, sections.size());
    resources = sections[0];
    EXPECT_EQ(3, resources.size());
    EXPECT_EQ(pageAssemblerMemoryClientCreator_.get(), pipelineMemoryClientCreator);
}

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenEnterprisePipelineIsBuiltForDuplexInputFlatbed_ThenJobTicketBacksideWillBeSetCorrectly)
{  
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    std::shared_ptr<IEnqueueIntf>  pipe;
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);

    // -> Stage::ScanFirstPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
    
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                            std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    EXPECT_EQ(jobTicket->getFlatbedDuplexScanSide(), dune::scan::types::DuplexSideEnum::FrontSide);
    pipe->closeForEnqueuing();

    // -> Stage::ScanSecondPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig2);
    resourceList.push_back(imagePersister2);
    
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                            std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::MultiScanStage;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedDuplexAddPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    resources = sections[0];
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();
    
    // -> Stage::PrintAllPages
    resourceList.clear();
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                            std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::Cancelled;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedDuplexAddPage, PromptResponseType::Response_03, SegmentType::FinalSegment);
    EXPECT_EQ(jobTicket->getFlatbedDuplexScanSide(), dune::scan::types::DuplexSideEnum::BackSide);

}
  

TEST_F(GivenAConnectedCopyPipelineStandardOfEnterprise, WhenAddPageMaxPageReached_ResourceInstanceFreeIsCalled)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);

    jobTicket->setStorePath("/tmp");
    jobTicket->getIntent()->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobTicket->getIntent()->setInputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setOutputPlexMode(Plex::DUPLEX);
    jobTicket->getIntent()->setPagesPerSheet(dune::imaging::types::CopyOutputNumberUpCount::TwoUp);

    dune::imaging::types::NotificationStrategy notificationStrat = dune::imaging::types::NotificationStrategy::NONE;
    EXPECT_CALL(*imagePersisterIntent_, setNotificationStrategy(_))

        .WillRepeatedly(

            testing::Invoke([this, &notificationStrat](dune::imaging::types::NotificationStrategy value) -> void {

                notificationStrat = value;

            }));

    std::shared_ptr<IEnqueueIntf>  pipe;
    EXPECT_CALL(*imagePersisterTicket_, setEnqueueIntf(_)).WillRepeatedly(
            testing::Invoke([this, &pipe](std::shared_ptr<IEnqueueIntf>  pipe_value) -> void {
                pipe = pipe_value;
            })
    );

    dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator;
    EXPECT_CALL(*imageRetrieverTicket_, setPipelineMemoryClient(_))

        .WillRepeatedly(

            testing::Invoke([this, &pipelineMemoryClientCreator](dune::imaging::IPipelineMemoryClientCreator* pipelineMemoryClientCreator_value) -> void {

                pipelineMemoryClientCreator = pipelineMemoryClientCreator_value;

            }));

    

    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::ENTERPRISE, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);
    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    pipelineBuilder->setMaxFlatbedDuplexPages(1);
    // -> Stage::ScanFirstPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersister1);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FirstScanStage;
                                            })
                                        ));
    
    PipelineBuilderBase::ResourceInstanceProxiesSection sections =
        pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);
    PipelineBuilderBase::ResourceInstanceProxies resources = sections[0];
    PipelineBuilderBase::ResourceInstanceProxies second_section;
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();

    // -> Stage::ScanSecondPage
    resourceList.clear();
    resourceList.push_back(scanDeviceConfig2);
    resourceList.push_back(imagePersister2);
   
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::MultiScanStage;
                                            })
                                        ));
    
    sections = pipelineBuilder->onBuildPipeline(PromptType::FlatbedDuplexAddPage, PromptResponseType::Response_01, SegmentType::FinalSegment);
    resources = sections[0];
    EXPECT_EQ(1, sections.size());
    EXPECT_EQ(2, resources.size());
    EXPECT_EQ(notificationStrat, dune::imaging::types::NotificationStrategy::ON_STARTED);
    pipe->closeForEnqueuing();

    // -> Stage::PrintAllPages
    resourceList.clear();
    ON_CALL(*scanPipelineBuilder_, buildScanPipeline(_,_,_,_,_)).WillByDefault(::testing::DoAll(
            ::testing::Invoke([&](PromptType promptType, PromptResponseType responseType, SegmentType segmentType, std::shared_ptr<dune::scan::Jobs::Scan::IScanJobIntent> scanIntent,
                                           std::vector<std::shared_ptr<dune::scan::Jobs::Scan::ResourceConfigT>> &resourceList_)
                                            {
                                                resourceList_ = resourceList;
                                                return dune::scan::Jobs::Scan::ScanStage::FinishedFinalMultiScan;
                                            })
                                        ));
    sections = pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::FinalSegment);

    //As max Page is reached the resource setkeep should be set to False
    for (int i = 0; i < (int)resources.size(); i++)
    {
        GTEST_CHECKPOINTA("Resource %d: %s\n", i, resources[i]->getResourceServiceId().c_str());
        EXPECT_EQ(resources[i]->getKeep(), false);
    }

    EXPECT_EQ(1, sections.size());
    resources = sections[0];
    EXPECT_EQ(3, resources.size());
}


class GivenAConnectedCopyPipelineStandardOfBasic :public GivenANewCopyPipelineStandard
{
  public:

    GivenAConnectedCopyPipelineStandardOfBasic() {};

    virtual void SetUp() override;

    virtual void TearDown() override;
};

void GivenAConnectedCopyPipelineStandardOfBasic::SetUp()
{
    productTestFileName = "./testResources/CopyPipelineStandardJupiter.json";
    GivenANewCopyPipelineStandard::SetUp();

    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    auto scanDeviceConfig1 = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    scanDeviceConfig1->resourceId = dune::scan::Jobs::Scan::ResourceName::NONE;
    scanDeviceConfig1->pipeType = dune::scan::Jobs::Scan::PipeObjectType::IMAGECONTAINER;
    scanDeviceConfig1->jobletBoudary = dune::job::JobletBoundary::UNDEFINED;
    scanDeviceConfig1->isSegmentFirstResource = true;
    scanDeviceConfig1->isPipeQueueRequired = true;
    scanDeviceConfig1->queuingFlag = QueuingFlag::BOTH;


    auto imagePersisterBuffer = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    imagePersisterBuffer->resourceId = dune::scan::Jobs::Scan::ResourceName::IMAGEPERSISTERDISKBUFFERING;
    imagePersisterBuffer->pipeType = dune::scan::Jobs::Scan::PipeObjectType::IMAGECONTAINER;
    imagePersisterBuffer->jobletBoudary = dune::job::JobletBoundary::UNDEFINED;
    imagePersisterBuffer->isPipeQueueRequired = true;
    imagePersisterBuffer->queuingFlag = QueuingFlag::BOTH;
    imagePersisterBuffer->reusePipeQueue = true;
    imagePersisterBuffer->persistentPipe = true;

    auto imageRetrieverBuffer = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    imageRetrieverBuffer->resourceId = dune::scan::Jobs::Scan::ResourceName::IMAGERETRIEVERDISKBUFFERING;
    imageRetrieverBuffer->pipeType = dune::scan::Jobs::Scan::PipeObjectType::IMAGECONTAINER;
    imageRetrieverBuffer->jobletBoudary = dune::job::JobletBoundary::UNDEFINED;
    imageRetrieverBuffer->isPipeQueueRequired = true;
    imageRetrieverBuffer->queuingFlag = QueuingFlag::BOTH;


    auto imageProcessorConfig = std::make_shared<dune::scan::Jobs::Scan::ResourceConfigT>();
    imageProcessorConfig->resourceId = dune::scan::Jobs::Scan::ResourceName::IMAGEPROCESSORPREVIEW;
    imageProcessorConfig->pipeType = dune::scan::Jobs::Scan::PipeObjectType::IMAGECONTAINER;
    imageProcessorConfig->jobletBoudary = dune::job::JobletBoundary::UNDEFINED;
    imageProcessorConfig->isSegmentFirstResource = false;
    imageProcessorConfig->isPipeQueueRequired = true;
    imageProcessorConfig->queuingFlag = QueuingFlag::ENQUEUE;

    resourceList.clear();
    resourceList.push_back(scanDeviceConfig1);
    resourceList.push_back(imagePersisterBuffer);
    resourceList.push_back(imageRetrieverBuffer);
    resourceList.push_back(imageProcessorConfig);

    ON_CALL(*scanPipeline_, getResourceList(_)).WillByDefault(Return(resourceList));

}

void GivenAConnectedCopyPipelineStandardOfBasic::TearDown()
{
    GivenANewCopyPipelineStandard::TearDown();
}

TEST_F(GivenAConnectedCopyPipelineStandardOfBasic, WhenLfpPipelineIsBuiltForPreviewWithResourceAsNone_ThenPipelineThrowAnAssert)
{
    auto jobTicket = std::make_shared<CopyJobTicket>();

    ASSERT_NE(nullptr, jobTicket);
    jobTicket->getIntent()->setGeneratePreview(true);

    //Activate scanDiskBuffering in the mocked config.
    scanPipeline_->scanPipelineConfig_->scanDiskBuffering = true;
    scanPipelineConfig_->scanDiskBuffering = true;
    auto copypipeline = component_->createPipelineBuilder(jobTicket, Product::LFP, services_, scanPipeline_.get(), false, false, maxLengthConfig_, systemServices_->dateTime_, multiPageSupportedFromFlatbed_);

    auto pipelineBuilder = std::static_pointer_cast<CopyConfigurablePipelineBuilder>(copypipeline);
    ASSERT_NE(nullptr, pipelineBuilder);
    std::vector<dune::job::IIntentsManager::ResourceTicket> resourcesTicket;
    ASSERT_DEATH(pipelineBuilder->onBuildPipeline(PromptType::None, PromptResponseType::NoResponse, SegmentType::PrepareSegment), "");
}



