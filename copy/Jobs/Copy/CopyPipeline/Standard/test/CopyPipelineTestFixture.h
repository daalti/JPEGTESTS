///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyPipelineTestFixture.h
 * @author Shubham Khandelwal
 * @date   25-04-2021
 * @brief  unit Test fixture setup 
 *
 * (C) Copyright 2019 HP Inc.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "gmock/gmock.h"
#include "gtest/gtest.h"

#include "CopyJobTicket.h"
#include "CopyPipelineResourceSetup.h"
#include "ErrorManager.h"
#include "IColorTransform.h"
#include "IResourceClient.h"
#include "JobFrameworkTypes.h"
#include "MockICapabilities.h"
#include "MockIColorDirector.h"
#include "MockIColorEngine.h"
#include "MockIImageColorEngine.h"
#include "MockIImagePersister.h"
#include "MockIImagePersisterTicket.h"
#include "MockIImageProcessor.h"
#include "MockIImageProcessorTicket.h"
#include "MockIImageRetrieverTicket.h"
#include "MockIIntentsManager.h"
#include "MockILayoutFilter.h"
#include "MockILayoutFilterIntent.h"
#include "MockILayoutFilterTicket.h"
#include "MockIMarkingFilter.h"
#include "MockIMarkingFilterTicket.h"
#include "MockIMedia.h"
#include "MockIMediaAttributes.h"
#include "MockIMediaHandlingSettings.h"
#include "MockIMediaInfo.h"
#include "MockIPageAssembler.h"
#include "MockIPageAssemblerTicket.h"
#include "MockIPipelineMemoryClientCreator.h"
#include "MockIPrintDevice.h"
#include "MockIPrintDeviceIntent.h"
#include "MockIPrintDeviceTicket.h"
#include "MockIRasterFormatNegotiator.h"
#include "MockIRasterFormatSelector.h"
#include "MockIResourceClientAgent.h"
#include "MockIResourceClientTicket.h"
#include "MockIResourceManagerClient.h"
#include "MockIResourceService.h"
#include "MockIResourceTicket.h"
#include "MockIRtpFilterTicket.h"
#include "MockIScanDevice.h"
#include "MockIScanDeviceTicket.h"
#include "MockIScanPipeline.h"
#include "ScanPipelineConfig_generated.h"
#include "TestSystemServices.h"
#include "MockIIPADeviceTicket.h"
#include "MockIIPADevice.h"
#include "MockIImageImporterTicket.h"
#include "MockIImageImporter.h"
#include "IImageImporter.h"

using namespace dune::copy::Jobs::Copy;

using ::testing::_;
using ::testing::AtLeast;
using ::testing::DoAll;
using ::testing::Eq;
using ::testing::Field;
using ::testing::Invoke;
using ::testing::InvokeWithoutArgs;
using ::testing::Return;
using ::testing::ReturnNew;
using ::testing::ReturnRef;
using ::testing::SetArgReferee;
using dune::scan::Jobs::Scan::ResourceName;
using dune::scan::Jobs::Scan::QueuingFlag;
using dune::scan::Jobs::Scan::PipeObjectType;

using dune::imaging::MockIPipelineMemoryClientCreator;
using dune::imaging::MockIRasterFormatNegotiator;
using dune::imaging::MockIRasterFormatSelector;
using dune::imaging::color::IColorTransform;
using dune::imaging::color::MockIColorDirector;
using dune::imaging::color::MockIColorEngine;
using dune::imaging::color::MockIImageColorEngine;
using dune::imaging::Resources::IImagePersisterTicket;
using dune::imaging::Resources::IImageRetrieverTicket;
using dune::imaging::Resources::MockIImagePersister;
using dune::imaging::Resources::MockIImagePersisterIntent;
using dune::imaging::Resources::MockIImagePersisterTicket;
using dune::imaging::Resources::MockIImageProcessor;
using dune::imaging::Resources::MockIImageProcessorIntent;
using dune::imaging::Resources::MockIImageProcessorTicket;
using dune::imaging::Resources::MockIImageRetrieverIntent;
using dune::imaging::Resources::MockIImageRetrieverTicket;
using dune::imaging::Resources::MockIMarkingFilter;
using dune::imaging::Resources::MockIMarkingFilterIntent;
using dune::imaging::Resources::MockIMarkingFilterTicket;
using dune::imaging::Resources::MockIMarkingFilterSettings;
using dune::imaging::Resources::MockILayoutFilter;
using dune::imaging::Resources::MockILayoutFilterIntent;
using dune::imaging::Resources::MockILayoutFilterInterfaces;
using dune::imaging::Resources::MockILayoutFilterTicket;
using dune::imaging::Resources::MockIPageAssembler;
using dune::imaging::Resources::MockIPageAssemblerIntent;
using dune::imaging::Resources::MockIPageAssemblerTicket;
using dune::imaging::asset::MockIMediaAttributes;
using dune::print::engine::MockIMedia;
using dune::print::engine::MockIMediaInfo;
using dune::print::mediaHandlingAssets::MockIMediaHandlingSettings;
using dune::job::SegmentType;
using dune::job::MockIResourceClientAgent;
using dune::job::MockIResourceManagerClient;
using dune::job::MockIResourceService;
using dune::job::MockIResourceTicket;
using dune::job::PromptResponseType;
using dune::job::PromptType;
using dune::print::Resources::MockIRtpFilterTicket;
using dune::print::Resources::MockIPrintDevice;
using dune::print::Resources::MockIPrintDeviceIntent;
using dune::print::Resources::MockIPrintDeviceTicket;
using dune::print::Resources::MockIPrintDevice;
using dune::imaging::color::MockIColorDirector;
using dune::imaging::Resources::MockIImagePersister;
using dune::imaging::color::MockIColorEngine;
using dune::imaging::color::IColorTransform;
using dune::imaging::color::MockIImageColorEngine;
using dune::scan::Jobs::Scan::MockIScanPipeline;
using Margins = dune::imaging::types::Margins;
using Distance = dune::imaging::types::Distance;

using dune::scan::Resources::MockIScanDeviceIntent;
using dune::scan::Resources::MockIScanDeviceTicket;
using dune::scan::Resources::MockIScanDevice;
using dune::scan::Resources::MockIScanDeviceResult;
using MockIIntentsManager = dune::job::MockIIntentsManager;
using TestSystemServices = dune::framework::component::TestingUtil::TestSystemServices;

using dune::imaging::Resources::IImagePersister;
using dune::imaging::Resources::IImageProcessor;
using dune::imaging::Resources::IMarkingFilter;
using dune::imaging::Resources::ILayoutFilter;
using dune::imaging::Resources::IPageAssembler;
using dune::imaging::asset::IMediaAttributes;
using dune::print::Resources::IRtpFilter;
using dune::print::Resources::IPrintDevice;
using dune::scan::Resources::IScanDevice;
using dune::scan::scanningsystem::MockIScannerCapabilities;
using dune::scan::Resources::IIPADevice;
using dune::scan::Resources::MockIIPADevice;
using dune::scan::Resources::MockIIPADeviceTicket;
using dune::scan::Resources::MockIIPADeviceIntents;
using dune::imaging::Resources::MockIImageImporterTicket;
using dune::imaging::Resources::MockIImageImporterIntents;
using dune::imaging::Resources::MockIImageImporter;
using dune::imaging::Resources::IImageImporter;

class GivenCopyPipelineResources : public ::testing::Test
{
  public:
    GivenCopyPipelineResources(){};
    ServicesPackage services_{nullptr};
    MaxLengthConfig maxLengthConfig_{};
    bool multiPageSupportedFromFlatbed_{false};
    int thresholdOverride_{0};

    virtual void SetUp() {};

    virtual void TearDown() {};

    // ResourceServiceIds
    std::string scanDeviceId_{"scanDevice"};
    std::string printDeviceId_{"printDevice"};
    std::string pageAssemblerId_{"pageAssembler"};
    std::string markingFilterId_{"markingFilter"};
    std::string layoutFilterId_{"layoutFilter"};
    std::string imagePersisterId_{"imagePersister"};
    std::string imageRetrieverId_{"imageRetriever"};
    std::string imageProcessorId_{"imageProcessor"};
    std::string rtpFilterServiceId_{"rtpFilterService"};
    std::string ipaDeviceId_{"ipaDevice"};
    std::string imageImporterId_{"imageImporter"};

    std::shared_ptr<TestSystemServices> systemServices_{std::make_shared<TestSystemServices>()};
    std::shared_ptr<MockIResourceManagerClient> managerClient_{std::make_shared<MockIResourceManagerClient>()};
    std::shared_ptr<MockIResourceClientAgent> agent_{std::make_shared<MockIResourceClientAgent>()};
    std::shared_ptr<MockIResourceClientTicket> clientTicket_{std::make_shared<MockIResourceClientTicket>()};

    // ResourceServices
    std::shared_ptr<MockIResourceService> scanDeviceResourceService_{std::make_shared<MockIResourceService>()};
    std::shared_ptr<MockIResourceService> imagePersisterResourceService_{std::make_shared<MockIResourceService>()};
    std::shared_ptr<MockIResourceService> rtpFilterService_{std::make_shared<MockIResourceService>()};
    std::shared_ptr<MockIResourceService> printDeviceResourceService_{std::make_shared<MockIResourceService>()};
    std::shared_ptr<MockIResourceService> imageProcessorResourceService_{std::make_shared<MockIResourceService>()};
    std::shared_ptr<MockIResourceService> pageAssemblerResourceService_{std::make_shared<MockIResourceService>()};
    std::shared_ptr<MockIResourceService> imageRetrieverService_{std::make_shared<MockIResourceService>()};
    std::shared_ptr<MockIResourceService> markingFilterService_{std::make_shared<MockIResourceService>()};
    std::shared_ptr<MockIResourceService> layoutFilterService_{std::make_shared<MockIResourceService>()};
    std::shared_ptr<MockIResourceService> ipaDeviceResourceService_{std::make_shared<MockIResourceService>()};
    std::shared_ptr<MockIResourceService> imageImporterResourceService_{std::make_shared<MockIResourceService>()};
    
    std::shared_ptr<MockIMediaAttributes> mediaAttributes_{std::make_shared<MockIMediaAttributes>()};
    std::shared_ptr<MockIMedia>           mediaInterface_{std::make_shared<MockIMedia>()};
    std::shared_ptr<MockIMediaInfo>       mediaInfoInterface_{std::make_shared<MockIMediaInfo>()};
    std::shared_ptr<MockIMediaHandlingSettings> mediaSettingsInterface_{std::make_shared<MockIMediaHandlingSettings>()};

    std::shared_ptr<MockIImagePersister> imagePersister_{std::make_shared<MockIImagePersister>()};
    std::shared_ptr<MockIMarkingFilter> markingFilter_{std::make_shared<MockIMarkingFilter>()};
    std::shared_ptr<MockILayoutFilter> layoutFilter_{std::make_shared<MockILayoutFilter>()};
    std::shared_ptr<MockIPrintDevice> printDevice_{std::make_shared<MockIPrintDevice>()};
    std::shared_ptr<MockIImageProcessor> imageProcessor_{std::make_shared<MockIImageProcessor>()};  // make uniq
    std::shared_ptr<MockIColorDirector> colorDirector_{std::make_shared<MockIColorDirector>()};//make uniq
    std::shared_ptr<MockIPageAssembler> pageAssembler_{std::make_shared<MockIPageAssembler>()};
    std::shared_ptr<MockIIPADevice> ipaDevice_{std::make_shared<MockIIPADevice>()};
    std::shared_ptr<MockIImageImporter> imageImporter_{std::make_shared<MockIImageImporter>()};

    std::shared_ptr<MockIPipelineMemoryClientCreator> printDeviceMemoryClientCreator_{std::make_shared<MockIPipelineMemoryClientCreator>()};
    std::shared_ptr<MockIPipelineMemoryClientCreator> imageProcessorMemoryClientCreator_{std::make_shared<MockIPipelineMemoryClientCreator>()};
    std::shared_ptr<MockIPipelineMemoryClientCreator> persisterMemoryClientCreator_{std::make_shared<MockIPipelineMemoryClientCreator>()};
    std::shared_ptr<MockIPipelineMemoryClientCreator> pageAssemblerMemoryClientCreator_{std::make_shared<MockIPipelineMemoryClientCreator>()};
    std::shared_ptr<MockIPipelineMemoryClientCreator> markingFilterMemoryClientCreator_{std::make_shared<MockIPipelineMemoryClientCreator>()};

    std::shared_ptr<MockIRasterFormatSelector> rasterSelector_{std::make_shared<MockIRasterFormatSelector>()};
    std::shared_ptr<MockIRasterFormatNegotiator> rasterNegotiator_{std::make_shared<MockIRasterFormatNegotiator>()};

    std::shared_ptr<MockIScanDevice> scanDeviceService_{std::make_shared<MockIScanDevice>()};

    // ResourceTickets
    std::shared_ptr<MockIScanDeviceTicket> scanDeviceTicket_{std::make_shared<MockIScanDeviceTicket>()};
    std::shared_ptr<MockIImagePersisterTicket> imagePersisterTicket_{std::make_shared<MockIImagePersisterTicket>()};
    std::shared_ptr<MockIImageRetrieverTicket> imageRetrieverTicket_{std::make_shared<MockIImageRetrieverTicket>()};
    std::shared_ptr<MockIRtpFilterTicket> rtpFilterTicket_{std::make_shared<MockIRtpFilterTicket>()};
    std::shared_ptr<MockIPrintDeviceTicket> printDeviceTicket_{std::make_shared<MockIPrintDeviceTicket>()};
    std::shared_ptr<MockIPageAssemblerTicket> pageAssemblerTicket_{std::make_shared<MockIPageAssemblerTicket>()};
    std::shared_ptr<MockIMarkingFilterTicket> markingFilterTicket_{std::make_shared<MockIMarkingFilterTicket>()};
    std::shared_ptr<MockILayoutFilterTicket>  layoutFilterTicket_{std::make_shared<MockILayoutFilterTicket>()};
    std::shared_ptr<MockIImageProcessorTicket> imageProcessorTicket_{std::make_shared<MockIImageProcessorTicket>()};
    std::shared_ptr<MockIIPADeviceTicket> ipaDeviceTicket_{std::make_shared<MockIIPADeviceTicket>()};
    std::shared_ptr<MockIImageImporterTicket> imageImporterTicket_{std::make_shared<MockIImageImporterTicket>()};

    // This is a pointer to the resourceClient registered to ResourceManagerClient
    // Needed to call allocated to ResourceService and ResourceInstance
    std::shared_ptr<IResourceClient> resourceClient_{};

    // Scan pipeline. Stores the pipeline configuration.
    std::shared_ptr<MockIScanPipeline> scanPipeline_{std::make_shared<MockIScanPipeline>()};
    Margins desiredMargins_{Distance(236, 1200), Distance(236, 1200), Distance(236, 1200), Distance(236, 1200)};

    std::string defaultString_{"GTESTDEFAULTSTRING"};
};



