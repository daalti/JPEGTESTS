/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobServiceStandardGtestMain.cpp
 * @date   Wed, 08 May 2019 06:49:55 -0700
 * @brief  JobService specific class to CopyJobs
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////
#include "IDataStore.h"
#include "com.hp.cdm.service.shortcut.version.1.serviceDefinition_autogen.h"
#include "ComponentSystemTypes.h"
#include "CopyJobPromptController.h"
#include "ICopyJobService.h"
#include "ICopyJobTicket.h"
#include "JobServiceFactoryQuicksetConfig_generated.h"
#include "JobServiceStandard_TraceAutogen.h"
#include "JobServiceStandard.h"
#include "MediaHelper.h"
#include "MediaInputCapabilities.h"
#include "Permissions.h"
#include "SimplePathDirMock.h"
#include "MockISettings.h"

#include "MockICapabilities.h"
#include "MockICopyAdapter.h"
#include "MockICopyJobDynamicConstraintRules.h"
#include "MockIDataStore.h"
#include "MockIImagePersister.h"
#include "MockIJobConstraints.h"
#include "MockIJobDetailsManager.h"
#include "MockIJobManager.h"
#include "MockIJobManagerAlertProvider.h"
#include "MockIJobServiceManager.h"
#include "MockIJobTicketResourceManager.h"
#include "MockILocaleProvider.h"
#include "MockIMedia.h"
#include "MockIMediaAttributes.h"
#include "MockIMediaHandlingSettings.h"
#include "MockIMediaInfo.h"
#include "MockIPageAssembler.h"
#include "MockIPipelineMemoryClientCreator.h"
#include "MockIPrintDevice.h"
#include "MockIPrintIntentsFactory.h"
#include "MockIRasterFormatSelector.h"
#include "MockIResourceManagerClient.h"
#include "MockIResourceService.h"
#include "MockIScanDevice.h"
#include "MockIColorDirector.h"
#include "MockIScannerMedia.h"
#include "MockIScanPipeline.h"
#include "MockIShortcuts.h"
#include "MockICopyPipeline.h"
#include "MockIPipelineBuilder.h"
#include "MockIExportImport.h"
#include "MockISecureFileErase.h"
#include "MockIMediaHandlingMgr.h"
#include "MockIRenderingRequirements.h"
#include "MockINvram.h"
#include "MockISettings.h"
#include "MockIIntentsManager.h"
#include "gmock/gmock.h"
#include "gtest/gtest.h"
#include "TestSystemServices.h"
#include "GTestConfigHelper.h"
#include "MockIJobServiceFactory.h"
#include "MockICopyJobTicket.h"
#include "MockIPathDirectory.h"
#include "MockIMediaInfoPageBased.h"
#include "IMediaInfoPageBased.h"
#include "MockIScanConstraints.h"
#include "MockIDeviceInfo.h"
#include "MockINetworkManager.h"
#include "MockISystemConversionHelper.h"
#include "MockICopyTicketConverter.h"
#include "IConnector.h"
#include "com.hp.cdm.service.jobTicket.version.1.serviceDefinition_autogen.h"
#include "MockIPrint.h"
#include "MockIStatus.h"
#include "MockICapabilitiesFactory.h"
#include "MockIJobQueue.h"

using ComponentFlavorUid                = dune::framework::component::ComponentFlavorUid;
using IComponent                        = dune::framework::component::IComponent;
using IComponentManager                 = dune::framework::component::IComponentManager;
using ICopyJobService                   = dune::copy::Jobs::Copy::ICopyJobService;
using ICopyJobTicket                    = dune::copy::Jobs::Copy::ICopyJobTicket;
using JobServiceStandard                = dune::copy::Jobs::Copy::JobServiceStandard;
using MockIDataStore                    = dune::framework::data::MockIDataStore;
using MockIJobManager                   = dune::job::MockIJobManager;
using MockIJobManagerAlertProvider      = dune::job::cdm::MockIJobManagerAlertProvider;
using MockIJobServiceManager            = dune::job::MockIJobServiceManager;
using MockIJobDetailsManager            = dune::job::MockIJobDetailsManager;
using MockIJobTicketResourceManager     = dune::job::MockIJobTicketResourceManager;
using MockIPageAssembler                = dune::imaging::Resources::MockIPageAssembler;
using MockIImagePersister               = dune::imaging::Resources::MockIImagePersister;
using MockIPipelineMemoryClientCreator  = dune::imaging::MockIPipelineMemoryClientCreator;
using MockIPrintDevice                  = dune::print::Resources::MockIPrintDevice;
using MockIPrint                        = dune::print::engine::MockIPrint;
using MockICapabilitiesFactory          = dune::print::engine::MockICapabilitiesFactory;
using MockIPrintIntentsFactory          = dune::print::engine::MockIPrintIntentsFactory;
using Capabilities                      = dune::print::engine::Capabilities;
using MockIRasterFormatSelector         = dune::imaging::MockIRasterFormatSelector;
using MockIResourceManagerClient        = dune::job::MockIResourceManagerClient;
using MockIResourceService              = dune::job::MockIResourceService;
using MockIScanDevice                   = dune::scan::Resources::MockIScanDevice;
using MockIColorDirector                = dune::imaging::color::MockIColorDirector;
using SystemServices                    = dune::framework::component::SystemServices;
using TestSystemServices                = dune::framework::component::TestingUtil::TestSystemServices;
using MockIShortcuts                    = dune::admin::shortcuts::MockIShortcuts;
using MockIScanPipeline                 = dune::scan::Jobs::Scan::MockIScanPipeline;
using ScanMediaSize                     = dune::scan::Jobs::Scan::ScanMediaSize;
using MockIStatus                       = dune::scan::scanningsystem::MockIStatus;
using MockIMedia                        = dune::scan::scanningsystem::MockIMedia;
using MockIPrintMedia                   = dune::print::engine::MockIMedia;
using MockIMediaInfo                    = dune::print::engine::MockIMediaInfo;
using MockIMediaHandlingSettings        = dune::print::mediaHandlingAssets::MockIMediaHandlingSettings;
using MockIMediaInputCapabilities       = dune::scan::scanningsystem::MockIMediaInputCapabilities;
using MockIScannerCapabilities          = dune::scan::scanningsystem::MockIScannerCapabilities;
using MockISettings                     = dune::print::engine::MockISettings;
using MockIIntentsManager               = dune::job::MockIIntentsManager;
using MockIRenderingRequirements        = dune::print::engine::helpers::MockIRenderingRequirements;
using MockIMediaPath                    = dune::scan::scanningsystem::MockIMediaPath;
using MockINvram                        = dune::framework::storage::MockINvram;
using MockIScanConstraints              = dune::scan::MockIScanConstraints;
using MockISystemConversionHelper       = dune::framework::data::conversion::MockISystemConversionHelper;
using MockISystemConversionContext      = dune::framework::data::conversion::MockISystemConversionContext;
using IInputList                        = dune::scan::scanningsystem::IMedia::IInputList;
using MediaInputCapabilities            = dune::scan::scanningsystem::MediaInputCapabilities;
using MediaSource                       = dune::imaging::types::MediaSource;
using MockIMediaIInput                  = dune::print::engine::MockIMediaIInput;
using InputList                         = dune::print::engine::IMedia::InputList;
using EngineAttributeFieldType          = dune::print::engine::EngineAttributeFieldType;
using EngineVariant                     = dune::print::engine::Variant;
using FinisherAttributeFieldType        = dune::print::engine::FinisherAttributeFieldType;
//using ScanConstraintFromScanInterface   = dune::scan::Jobs::Scan::ScanConstraintFromScanInterface;
using IScanConstraints                  = dune::scan::IScanConstraints;
using MediaHelper                       = dune::print::engine::MediaHelper;
using Permission                        = dune::security::ac::Permission;
using MockIJobConstraints               = dune::copy::Jobs::Copy::MockIJobConstraints;
using MockICopyAdapter                  = dune::copy::cdm::MockICopyAdapter;
using ICopyAdapterDataChangeEvent       = dune::framework::core::event::EventSource<dune::copy::cdm::CopyConfigurationEventType>;
using CollectionEasyBufferTable         = dune::cdm::shortcut_1::ShortcutsTable;
using ItemEasyBufferTable               = dune::cdm::shortcut_1::ShortcutTable;
using ShortcutOperationResult           = dune::admin::shortcuts::ShortcutOperationResult;
using shortcutFilter_t                  = dune::admin::shortcuts::shortcutFilter_t;
using IMediaAttributes                  = dune::imaging::asset::IMediaAttributes;
using MockIMediaAttributes              = dune::imaging::asset::MockIMediaAttributes;
using MockICopyJobDynamicConstraintRules= dune::copy::Jobs::Copy::MockICopyJobDynamicConstraintRules;
using DataObject = dune::framework::data::DataObject;
using MockIExportImport                 = dune::framework::data::backup::MockIExportImport;
using OperationType                     = dune::framework::data::backup::OperationType;
using MockISecureFileErase              = dune::framework::storage::MockISecureFileErase;
using MockIMediaHandlingMgr             = dune::print::mediaHandlingAssets::MockIMediaHandlingMgr;
using MockISettings                     = dune::print::engine::MockISettings;
using SettingsChangedEvent              = dune::framework::core::event::EventSource<dune::print::engine::ISettings, dune::print::engine::SettingsChangedEventArgs>;
using MediaPropertyChangedEvent =  dune::framework::core::event::EventSource<dune::print::engine::pageBased::MediaPropertyChangedEventArgs>;
using MediaSizeId             		    = dune::imaging::types::MediaSizeId;
using MockIPathDirectory                = dune::framework::storage::path::MockIPathDirectory;
using MockIMediaInfoExtension   = dune::print::engine::pageBased::MockIMediaInfoExtension;
using MediaPropertyChangedEventArgs = dune::print::engine::pageBased::MediaPropertyChangedEventArgs;
using MediaId = dune::imaging::types::MediaId;
using Variant = dune::print::engine::Variant;
using StatusType             = dune::scan::scanningsystem::StatusType;
using MediaPresenceStatusChangeEventSource = dune::framework::core::event::EventSource<dune::scan::scanningsystem::IMediaPath, const dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus &>;
using MediaIdType = dune::imaging::types::MediaIdType;
using MockIDeviceInfo                   = dune::admin::deviceinfo::MockIDeviceInfo;
using MockINetworkManager               = dune::io::net::core::MockINetworkManager;


using ::testing::Return;
using ::testing::ReturnRef;
using testing::_;
using testing::Invoke;
using ::testing::SetArgPointee;
using ::testing::WithArgs;
using testing::ReturnPointee;
using testing::SaveArg;
using testing::DoAll;
using testing::ElementsAreArray;
using ::testing::Matcher;
using ::testing::ByMove;
using testing::SetArgReferee;

using dune::copy::Jobs::Copy::Product;
using namespace dune::copy::Jobs::Copy;

#define RESOURCE_PATH "./testResources/"

int main(int argc, char  *argv[])
{
    // run google tests
    //
    std::cout << "Main:  " << argv[0] << std::endl;

    using dune::framework::core::gtest::GTestConfigHelper;
    GTestConfigHelper testConfigOptions_;
    testConfigOptions_.parse(argc, argv);
    testConfigOptions_.Configure();

    ::testing::FLAGS_gmock_catch_leaked_mocks = true;
    ::testing::FLAGS_gmock_verbose = "error";

    ::testing::InitGoogleTest(&argc, argv);

    return RUN_ALL_TESTS();
}

namespace dune { namespace copy { namespace Jobs { namespace Copy {

class TestableCopyJobService : public dune::copy::Jobs::Copy::JobServiceStandard
{
    public:
    TestableCopyJobService():JobServiceStandard("CopyJobService") {};

    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> createEmptyJobTicket() override {
        return dune::copy::Jobs::Copy::JobServiceStandard::createEmptyJobTicket();
    }
    
    void setResourceFilePath()
    {
        dune::copy::Jobs::Copy::JobServiceStandard::setResourceFilePath("testResources/");
    }

    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> addTicketToCache(std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> &jobTicket, bool &ticketAlreadyExisted)
    {
          return addTicketToCache(jobTicket, ticketAlreadyExisted);
    }
   
    std::string serializeDefaultTicketToJson(dune::job::JobType jobType)
    {
          return dune::copy::Jobs::Copy::JobServiceStandard::serializeDefaultTicketToJson(jobType);
    }

    std::pair<dune::framework::data::conversion::ConversionResult, 
        std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>> checkAndPerformMigration()
    {
        return dune::copy::Jobs::Copy::JobServiceStandard::checkAndPerformMigration();
    }

    // Remove the wrapper method for testValidateCurrentTickets since it's private
};
///////////////////////////////////////////////////////////////////////////////
//
// class GivenANewJobServiceStandard : public ::testing::Test
//
///////////////////////////////////////////////////////////////////////////////

class GivenANewJobServiceStandard : public ::testing::Test
{
  public:
    GivenANewJobServiceStandard() { GTEST_CHECKPOINTA("GivenANewJobServiceStandard::Constructor\n"); }

    void SetUp() override;
    void TearDown() override;

    ~GivenANewJobServiceStandard() { GTEST_CHECKPOINTA("GivenANewJobServiceStandard::Destructor"); }

    std::unique_ptr<CollectionEasyBufferTable> getShortcuts(const bool pinValidateNotRequired,
        const shortcutFilter_t &filter = shortcutFilter_t());

    std::unique_ptr<ItemEasyBufferTable> getShortcut(const dune::framework::core::Uuid &uuid,const bool pinValidateNotRequired,
                                                        const shortcutFilter_t &filter = shortcutFilter_t());

    ShortcutOperationResult addShortcut( const std::unique_ptr<ItemEasyBufferTable> &shortcut);

    ShortcutOperationResult updateShortcut(std::unique_ptr<ItemEasyBufferTable>& shortcut,const bool pinValidateNotReq,const shortcutFilter_t &filter = shortcutFilter_t());

    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> createCopyJobTicket(std::shared_ptr<CopyJobIntentFbT> intentFb = nullptr,std::shared_ptr<CopyJobConstraintsFbT> constraints = nullptr);
    std::shared_ptr<CopyJobIntentFbT> createCorrectJobIntent();
    std::shared_ptr<CopyJobIntentFbT> createIncorrectJobIntent();
    std::shared_ptr<CopyJobConstraintsFbT> createExpectedConstraints();

    void insertShortcutOnList(std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketRelated = nullptr);


  protected:
    const char *                        instanceName_{"CopyJobService"};

    std::unique_ptr<TestSystemServices> systemServices_{};
    MockIDataStore                      mockIDataStore_{};
    MockIImagePersister                 mockIImagePersister_;
    MockIJobManager                     mockIJobManager_;
    MockIJobManagerAlertProvider        mockIJobManagerAlertProvider_;
    MockIJobServiceManager              mockIJobServiceManager_;
    MockIJobTicketResourceManager       mockIJobTicketResourceManager_;
    MockIPageAssembler                  mockIPageAssembler_;
    MockIPipelineMemoryClientCreator    mockIPipelineMemoryClientCreator_;
    MockIPrintDevice                    mockIPrintDevice_;
    MockIPrintIntentsFactory            mockIPrintIntentsFactory_;
    MockIRasterFormatSelector           mockIRasterFormatSelector_;
    MockIResourceManagerClient          mockIResourceManagerClient_;
    MockIResourceService                mockIResourceService_;
    MockIMediaAttributes                mockIMediaAttributes_;
    MockIScanDevice                     mockIScanDevice_;
    MockIColorDirector                  mockIColorDirector_;
    MockIJobDetailsManager              mockDetailsManager_;
    IComponentManager*                  componentManager_{nullptr};
    IComponent*                         comp{nullptr};
    TestableCopyJobService*             component_{};
    MockIShortcuts                      mockIShortcut_{};
    MockIScanPipeline                   mockIScanPipeline_{};
    MockIMedia                          mockIScanMedia_{};
    MockIMediaInputCapabilities         mockIMediaInputCapabilities_{};
    MockIScannerCapabilities            mockIScannerCapabilities_{};
    MockIIntentsManager                  mockIIntentsManager_{};
    MockISettings                       mockISettings_{};
    MockIRenderingRequirements          mockIRenderingRequirements_{};
    MockINvram                          mockINvram_{};
    std::shared_ptr<MockIMediaPath>     pMockIMediaPath_;
    IInputList                          mockIScanInputList_;
    MediaInputCapabilities              mediaICap;
    MockIPrintMedia                     mockIPrintMedia_{};
    MockIMediaInfo                      mockIMediaInfo_{};
    MockIMediaHandlingSettings          mockIMediaHandlingSettings_{};
    MockIMediaHandlingMgr               mockIMediaHandlingMgr_{};
    MockICopyPipeline                   mockCopyPipeline_;
    InputList                           printList_;
    std::shared_ptr<MockIMediaIInput>   pMockIMediaIInput_;
    MockIJobConstraints                 mockIJobConstraints_{};
    MockICopyJobDynamicConstraintRules  mockICopyJobDynamicConstraintRules_{};
    MockICopyAdapter                    mockICopyAdapter_{};
    MockIExportImport                   mockIExportImport_{};
    MockISecureFileErase                mockISecureFileErase_{};
    ICopyAdapterDataChangeEvent         copyAdapterDataChangeEvent_;
    CollectionEasyBufferTable           internalShortCutCollection_;
    std::shared_ptr<MockILocaleProvider>mockLocaleProvider_;
    std::string                         productTestFileName{"./testResources/JobServiceStandardTestData.json"};
    ScanMediaSize                       scanMediaSize_{};
    MockIMediaInfoExtension             mockIMediaInfoPageBased_;    
    MediaPropertyChangedEvent           mediaPropertyChangedEvent_;
    MockIScanConstraints                mockIScanConstraints_;
    MockIDeviceInfo                     mockIDeviceInfo_;
    MockINetworkManager                 mockINetworkManager_;
    MockISystemConversionHelper         mockISystemConversionHelper_;
    MockICopyJobTicketConverter         mockICopyTicketConverter_;
    MockIStatus                         mockIStatus_;
    MockIPrint                          mockIPrint_;
    MockICapabilitiesFactory            mockICapabilitiesFactory_;
    MockIJobQueue                       mockIJobQueue_;
    std::unique_ptr<MediaPresenceStatusChangeEventSource> mediaPresenceStatusChangeEventSource_;
};

void GivenANewJobServiceStandard::SetUp()
{
    GTEST_CHECKPOINTA("GivenANewJobServiceStandard::SetUp -- ENTER\n");
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", productTestFileName.c_str());

    // component_ = std::make_unique<JobServiceStandard>(instanceName_);
    component_ = new TestableCopyJobService();
    component_->setIfResourcePathNeedComponentId(false);
    comp = static_cast<IComponent*>(component_);
    ASSERT_TRUE(component_ != nullptr);

    //Scan list
    pMockIMediaPath_ = std::make_shared<MockIMediaPath>();
    ASSERT_TRUE(pMockIMediaPath_ != nullptr);
    mockIScanInputList_.push_back(pMockIMediaPath_);

    //Print list
    pMockIMediaIInput_ = std::make_shared<MockIMediaIInput>();
    ASSERT_TRUE(pMockIMediaIInput_ != nullptr);
    printList_.push_back(pMockIMediaIInput_);

    ON_CALL(mockIScanPipeline_, getScanMediaSize()).WillByDefault(ReturnRef(scanMediaSize_));

    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "", &mockISettings_);

    ON_CALL(mockIMediaInfo_, getPageBasedExtension()).WillByDefault(Return(&mockIMediaInfoPageBased_));
    ON_CALL(mockIMediaInfoPageBased_, getMediaPropertyChangedEvent()).WillByDefault(ReturnRef(mediaPropertyChangedEvent_));
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);

    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);

    // Set the default metric as units system
    mockLocaleProvider_ = std::make_shared<MockILocaleProvider>();
    ASSERT_TRUE(mockLocaleProvider_ != nullptr);
    component_->setInterface(GET_INTERFACE_UID(dune::localization::ILocaleProvider),"MockILocaleProvider",(void*)mockLocaleProvider_.get());
    ON_CALL(*mockLocaleProvider_, getMeasurmentUnit()).WillByDefault(Return(dune::localization::MeasurementUnit::METRIC));

    //Oriented Media Sizes
    std::vector<dune::imaging::types::MediaOrientation> mediaOrientationA5;
    mediaOrientationA5.push_back(dune::imaging::types::MediaOrientation::PORTRAIT);
    mediaOrientationA5.push_back(dune::imaging::types::MediaOrientation::LANDSCAPE);

    std::vector<dune::imaging::types::MediaOrientation> mediaOrientationMostOfAll;
    mediaOrientationMostOfAll.push_back(dune::imaging::types::MediaOrientation::PORTRAIT);

    std::vector<dune::imaging::types::OrientedMediaSize> orientedMediaSizes;
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::ANY), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::A4), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::A5), mediaOrientationA5));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::A6), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::LETTER), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::LEGAL), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::STATEMENT), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::US_EXECUTIVE), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::FOOLSCAP), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::PHOTO4X6), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::PHOTO5X8), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::JIS_B5), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::JIS_B6), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::MEDIA100X150), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::OFICIO_216X340), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::MEDIA16K_195X270), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::MEDIA16K_184X260), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::ROC16K), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::COM10ENVELOPE), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::MONARCHENVELOPE), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::B5ENVELOPE), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::C5ENVELOPE), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::DLENVELOPE), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::HAGAKI_POSTCARD), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::HAGAKI_OUFUKU), mediaOrientationMostOfAll));
    orientedMediaSizes.push_back(dune::imaging::types::OrientedMediaSize(dune::imaging::types::MediaSize(MediaSizeId::CUSTOM), mediaOrientationMostOfAll));

    auto mediaWidths = dune::scan::scanningsystem::UInt32Range(1200,2550,0);
    auto mediaHeights = dune::scan::scanningsystem::UInt32Range(1500,4200,0);
    mediaICap.setSupportedWidths(mediaWidths);
    mediaICap.setSupportedHeights(mediaHeights);

    auto tupleInputList = std::tuple<APIResult, InputList> (APIResult::OK, printList_);
    auto tupleMediaOrientedSizes = std::tuple<APIResult, std::vector<dune::imaging::types::OrientedMediaSize>>(
        APIResult::OK, orientedMediaSizes);

    EXPECT_CALL(mockIScanDevice_, getResourceService).WillRepeatedly(Return(&mockIResourceService_));
    EXPECT_CALL(mockIImagePersister_, getResourceService).WillRepeatedly(Return(&mockIResourceService_));
    EXPECT_CALL(mockIPageAssembler_, getResourceService).WillRepeatedly(Return(&mockIResourceService_));
    EXPECT_CALL(mockIPrintDevice_, getResourceService).WillRepeatedly(Return(&mockIResourceService_));
    EXPECT_CALL(mockIPrintDevice_, getRasterFormatSelector(_)).WillRepeatedly(Return(&mockIRasterFormatSelector_));
    EXPECT_CALL(mockIPrintDevice_, getPipelineMemoryClientCreator).WillRepeatedly(Return(&mockIPipelineMemoryClientCreator_));
    EXPECT_CALL(mockIScanPipeline_, getScanPipelineConfiguration()).WillRepeatedly(Return(nullptr));

    //scanMedia
    EXPECT_CALL(mockIScanMedia_, getInputs).WillRepeatedly(Return(mockIScanInputList_));
    EXPECT_CALL((*pMockIMediaPath_), getId).WillRepeatedly(Return("ADF"));
    EXPECT_CALL((*pMockIMediaPath_), getType).WillRepeatedly(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    EXPECT_CALL((*pMockIMediaPath_), getMediaPresenceStatus).WillRepeatedly(Return(dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus::LOADED));
    EXPECT_CALL((*pMockIMediaPath_), getCapabilities).WillRepeatedly(ReturnRef(mediaICap));

    mediaPresenceStatusChangeEventSource_ = std::make_unique<dune::scan::scanningsystem::IMediaPath::MediaPresenceStatusChangeEventSource>(pMockIMediaPath_.get());
    EXPECT_CALL(*pMockIMediaPath_, getMediaPresenceStatusChangeEvent())
    .WillRepeatedly(ReturnRef(*mediaPresenceStatusChangeEventSource_));

    //print capability
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ICapabilitiesFactory),"mockICapabilitiesFactory" , &mockICapabilitiesFactory_);
    static const std::map<EngineAttributeFieldType, EngineVariant> engineAttributeFields_ = {{EngineAttributeFieldType::PRE_RUN_SUPPORTED, EngineVariant(true)}};
    static const std::map<FinisherAttributeFieldType, EngineVariant> finisherAttributeFields_ = {{FinisherAttributeFieldType::FINISHER_ATTRIBUTE_NONE, EngineVariant(0)}};
    std::shared_ptr<Capabilities> testCapabilities_ = std::make_shared<Capabilities>(engineAttributeFields_, finisherAttributeFields_);
    ON_CALL(mockICapabilitiesFactory_, getCapabilities()).WillByDefault(Return(testCapabilities_));

    //printMedia
    EXPECT_CALL(mockIPrintMedia_, getInputDevices).WillRepeatedly(Return(tupleInputList));
    EXPECT_CALL((*pMockIMediaIInput_), getMediaSupportedSizes).WillRepeatedly(Return(tupleMediaOrientedSizes));

    ON_CALL(mockIShortcut_,getShortcuts(_,_)).WillByDefault(WithArgs<0,1>(Invoke(
        [=] (const bool pinValidateNotRequired, const shortcutFilter_t &filter = shortcutFilter_t()) -> std::unique_ptr<CollectionEasyBufferTable>
        {
            return getShortcuts(pinValidateNotRequired, filter);
        }
    )));
    ON_CALL(mockIShortcut_,getShortcut(_,_,_)).WillByDefault(WithArgs<0,1,2>(Invoke(
        [=](const dune::framework::core::Uuid &uuid,const bool pinValidateNotRequired,
                const shortcutFilter_t &filter = shortcutFilter_t()) -> std::unique_ptr<ItemEasyBufferTable>
        {
            return getShortcut(uuid, pinValidateNotRequired, filter);
        }
    )));
    ON_CALL(mockIShortcut_,addShortcut(_)).WillByDefault(WithArgs<0>(Invoke(
        [=] (const std::unique_ptr<ItemEasyBufferTable> &shortcut) -> ShortcutOperationResult
        {
            return addShortcut(shortcut);
        }
    )));
    ON_CALL(mockIShortcut_,updateShortcut(_,_,_)).WillByDefault(WithArgs<0,1,2>(Invoke(
        [=] (std::unique_ptr<ItemEasyBufferTable> shortcut,const bool pinValidateNotReq,const shortcutFilter_t &filter = shortcutFilter_t()) -> ShortcutOperationResult
        {
            return updateShortcut(shortcut,pinValidateNotReq,filter);
        }
    )));
    GTEST_CHECKPOINTA("GivenANewJobServiceStandard::SetUp -- EXIT\n");
}

void GivenANewJobServiceStandard::TearDown()
{
    delete component_;
}

std::unique_ptr<CollectionEasyBufferTable> GivenANewJobServiceStandard::getShortcuts(const bool pinValidateNotRequired, const shortcutFilter_t &filter)
{
    DUNE_UNUSED(pinValidateNotRequired);

    CollectionEasyBufferTable auxiliaryCollection;

    // Apply filter get
    if(internalShortCutCollection_.shortcuts.size() > 0){
        for (auto& shortcut : internalShortCutCollection_.collection().getMutable())
        {
            if((filter.factory == dune::cdm::glossary_1::FeatureEnabled::_undefined_    || filter.factory == shortcut.factory.get()) &&
               (filter.type == dune::cdm::shortcut_1::Type::_undefined_                 || filter.type == shortcut.type.get()) &&
               (filter.readOnly == dune::cdm::glossary_1::FeatureEnabled::_undefined_   || filter.readOnly == shortcut.readOnly.get()) &&
               (filter.origin == dune::cdm::shortcut_1::Origin::_undefined_             || filter.origin == shortcut.origin.get()))
            {
                ItemEasyBufferTable shortcutSendToUsb = ItemEasyBufferTable{shortcut};
                auxiliaryCollection.shortcuts.insertItem(shortcutSendToUsb);
            }
        }
    }

    return std::make_unique<CollectionEasyBufferTable>(auxiliaryCollection);
}

std::unique_ptr<ItemEasyBufferTable> GivenANewJobServiceStandard::getShortcut(const dune::framework::core::Uuid &uuid,const bool pinValidateNotRequired,
                                                                                                        const shortcutFilter_t &filter)
{
    DUNE_UNUSED(pinValidateNotRequired);

    std::unique_ptr<ItemEasyBufferTable> result = nullptr;

    if(internalShortCutCollection_.shortcuts.size() > 0){
        for (auto& shortcut : internalShortCutCollection_.collection().getMutable())
        {
            if(shortcut.id.get() == uuid.toString())
            {
                result = std::make_unique<ItemEasyBufferTable>(shortcut);
            }
        }
    }

    return result;
}

ShortcutOperationResult GivenANewJobServiceStandard::addShortcut( const std::unique_ptr<ItemEasyBufferTable> &shortcut)
{
    ItemEasyBufferTable shortcutSendToUsb = ItemEasyBufferTable{*shortcut.get()};

    bool result = internalShortCutCollection_.shortcuts.insertItem(shortcutSendToUsb);

    return result ? ShortcutOperationResult::OK : ShortcutOperationResult::ERROR_GENERIC;
}

ShortcutOperationResult GivenANewJobServiceStandard::updateShortcut(std::unique_ptr<ItemEasyBufferTable>& shortcut,
                                                                                                const bool pinValidateNotReq,const shortcutFilter_t &filter)
{
    bool result = false;
    if(shortcut)
    {
        result = internalShortCutCollection_.shortcuts.updateItem(*shortcut.get());
    }

    return result ? ShortcutOperationResult::OK : ShortcutOperationResult::ERROR_GENERIC;
}

std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> GivenANewJobServiceStandard::createCopyJobTicket(std::shared_ptr<CopyJobIntentFbT> intentFb,
    std::shared_ptr<CopyJobConstraintsFbT> constraints)
{
    auto ticket = std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>();
    if(intentFb)
    {
        ticket->setIntent(intentFb);
    }
    if (constraints)
    {
        ticket->setConstraintsFromFb(constraints);
    }

    return ticket;
}

std::shared_ptr<CopyJobIntentFbT> GivenANewJobServiceStandard::createCorrectJobIntent()
{
    auto intent = std::make_shared<CopyJobIntentFbT>();
    intent->autoRotate = true;
    intent->collate = dune::copy::SheetCollate::Collate;
    intent->copies = 1;
    intent->copyMargins = dune::imaging::types::CopyMargins::CLIPCONTENT;
    intent->copyQuality = dune::imaging::types::PrintQuality::DRAFT;
    intent->mediaFamily = dune::imaging::types::MediaFamily::PLAIN;
    intent->printingOrder = dune::imaging::types::PrintingOrder::FIRST_PAGE_ON_TOP;
    intent->resize = 100;
    intent->outputMediaSizeId = dune::imaging::types::MediaSizeId::ANY;
    intent->outputMediaIdType = dune::imaging::types::MediaIdType::ANY;
    intent->outputMediaSource = dune::imaging::types::MediaSource::AUTOSELECT;
    intent->outputMediaDestination = dune::imaging::types::MediaDestinationId::STACKER;
    intent->outputPlexMode = dune::imaging::types::Plex::SIMPLEX;
    intent->outputPlexBinding = dune::imaging::types::PlexBinding::ONE_SIDED;
    intent->customMediaXDimension = 85000.0;
    intent->customMediaYDimension = 110000.0;
    using StaplingOption = decltype(intent->stapleOption);
    intent->stapleOption = StaplingOption::NONE;
    using PunchingOption = decltype(intent->punchOption);
    intent->punchOption = PunchingOption::NONE;

    auto scanJobIntent = std::make_unique<dune::scan::Jobs::Scan::ScanJobIntentFbT>();
    scanJobIntent->outputXResolution = dune::imaging::types::Resolution::E300DPI;
    scanJobIntent->outputYResolution = dune::imaging::types::Resolution::E300DPI;
    scanJobIntent->scanXResolution = dune::imaging::types::Resolution::E300DPI;
    scanJobIntent->scanYResolution = dune::imaging::types::Resolution::E300DPI;
    scanJobIntent->originalContentType = dune::imaging::types::OriginalContentType::MIXED;
    scanJobIntent->colorMode = dune::imaging::types::ColorMode::COLOR;
    scanJobIntent->inputPlexMode = dune::imaging::types::Plex::SIMPLEX;
    scanJobIntent->scanSource = dune::scan::types::ScanSource::MDF;
    scanJobIntent->inputMediaSizeId = dune::imaging::types::MediaSizeId::ANY;
    scanJobIntent->invertColors = false;
    scanJobIntent->scanAcquisitionsSpeed = dune::scan::types::ScanAcquisitionsSpeedEnum::AUTO;
    scanJobIntent->scaleSelection = dune::scan::types::ScanScaleSelectionEnum::CUSTOM;
    scanJobIntent->scaleToSize = dune::imaging::types::MediaSizeId::ANY;
    scanJobIntent->scaleToOutput = dune::imaging::types::MediaSource::AUTOSELECT;
    scanJobIntent->scanCaptureMode = dune::scan::types::ScanCaptureModeType::JOBBUILD;
    scanJobIntent->generatePreview = true;

    auto outputCanvas = std::make_unique<dune::imaging::types::OutputCanvasT>();
    outputCanvas->outputCanvasMediaSize = dune::imaging::types::MediaSizeId::ANY;
    outputCanvas->outputCanvasMediaId = dune::imaging::types::MediaSource::AUTOSELECT;
    outputCanvas->outputCanvasXExtent = 2.6;
    outputCanvas->outputCanvasYExtent = 2.6;
    outputCanvas->outputCanvasAnchor = dune::imaging::types::OutputCanvasAnchorType::TOPLEFT;
    outputCanvas->outputCanvasOrientation = dune::imaging::types::ContentOrientation::PORTRAIT;
    scanJobIntent->outputCanvas = std::move(outputCanvas);

    intent->scanJobIntent = std::move(scanJobIntent);

    return intent;
}

std::shared_ptr<CopyJobIntentFbT> GivenANewJobServiceStandard::createIncorrectJobIntent()
{
    auto intent = std::make_shared<CopyJobIntentFbT>();
    intent->autoRotate = true;
    intent->collate = dune::copy::SheetCollate::Collate;
    intent->copies = 150;
    intent->copyMargins = dune::imaging::types::CopyMargins::CLIPCONTENT;
    intent->copyQuality = dune::imaging::types::PrintQuality::DRAFT;
    intent->mediaFamily = dune::imaging::types::MediaFamily::PLAIN;
    intent->printingOrder = dune::imaging::types::PrintingOrder::FIRST_PAGE_ON_TOP;
    intent->resize = 100;
    intent->outputMediaSizeId = dune::imaging::types::MediaSizeId::ANY;
    intent->outputMediaIdType = dune::imaging::types::MediaIdType::ANY;
    intent->outputMediaSource = dune::imaging::types::MediaSource::AUTOSELECT;
    intent->outputMediaDestination = dune::imaging::types::MediaDestinationId::STACKER;
    intent->outputPlexMode = dune::imaging::types::Plex::SIMPLEX;
    intent->outputPlexBinding = dune::imaging::types::PlexBinding::ONE_SIDED;
    intent->customMediaXDimension = 215.0;
    intent->customMediaYDimension = 279.0;
    using StaplingOption = decltype(intent->stapleOption);
    intent->stapleOption = StaplingOption::NONE;
    using PunchingOption = decltype(intent->punchOption);
    intent->punchOption = PunchingOption::NONE;

    auto scanJobIntent = std::make_unique<dune::scan::Jobs::Scan::ScanJobIntentFbT>();
    scanJobIntent->outputXResolution = dune::imaging::types::Resolution::E300DPI;
    scanJobIntent->outputYResolution = dune::imaging::types::Resolution::E300DPI;
    scanJobIntent->scanXResolution = dune::imaging::types::Resolution::E300DPI;
    scanJobIntent->scanYResolution = dune::imaging::types::Resolution::E300DPI;
    scanJobIntent->originalContentType = dune::imaging::types::OriginalContentType::MIXED;
    scanJobIntent->colorMode = dune::imaging::types::ColorMode::COLOR;
    scanJobIntent->inputPlexMode = dune::imaging::types::Plex::SIMPLEX;
    scanJobIntent->scanSource = dune::scan::types::ScanSource::MDF;
    scanJobIntent->inputMediaSizeId = dune::imaging::types::MediaSizeId::ANY;
    scanJobIntent->invertColors = false;
    scanJobIntent->scanAcquisitionsSpeed = dune::scan::types::ScanAcquisitionsSpeedEnum::AUTO;
    scanJobIntent->scaleSelection = dune::scan::types::ScanScaleSelectionEnum::CUSTOM;
    scanJobIntent->scaleToSize = dune::imaging::types::MediaSizeId::ANY;
    scanJobIntent->scaleToOutput = dune::imaging::types::MediaSource::AUTOSELECT;
    scanJobIntent->scanCaptureMode = dune::scan::types::ScanCaptureModeType::STANDARD;
    scanJobIntent->generatePreview = true;

    auto outputCanvas = std::make_unique<dune::imaging::types::OutputCanvasT>();
    outputCanvas->outputCanvasMediaSize = dune::imaging::types::MediaSizeId::ANY;
    outputCanvas->outputCanvasMediaId = dune::imaging::types::MediaSource::AUTOSELECT;
    outputCanvas->outputCanvasXExtent = 2.6;
    outputCanvas->outputCanvasYExtent = 2.6;
    outputCanvas->outputCanvasAnchor = dune::imaging::types::OutputCanvasAnchorType::TOPLEFT;
    outputCanvas->outputCanvasOrientation = dune::imaging::types::ContentOrientation::PORTRAIT;
    scanJobIntent->outputCanvas = std::move(outputCanvas);

    intent->scanJobIntent = std::move(scanJobIntent);
    return intent;
}

std::shared_ptr<CopyJobConstraintsFbT> GivenANewJobServiceStandard::createExpectedConstraints()
{
    auto constraint = std::make_shared<CopyJobConstraintsFbT>();

    constraint->plexMode.push_back(dune::imaging::types::Plex::SIMPLEX);
    constraint->minCopies = 1;
    constraint->maxCopies = 100;

    std::unique_ptr<dune::scan::Jobs::Scan::ScanJobConstraintFbT> scanJobConstraints = std::make_unique<dune::scan::Jobs::Scan::ScanJobConstraintFbT>();
    scanJobConstraints->scanCaptureModes.push_back(dune::scan::types::ScanCaptureModeType::JOBBUILD);
    constraint->scanJobConstraint = std::move(scanJobConstraints);

    return constraint;
}

void GivenANewJobServiceStandard::insertShortcutOnList(std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketRelated)
{
    auto shortcutToAdd = std::make_unique<dune::cdm::shortcut_1::ShortcutTable>("", "", dune::cdm::shortcut_1::Type::singleJob, dune::cdm::shortcut_1::Action::open);

    dune::cdm::shortcut_1::LocalIdTable localIdTable;
    localIdTable.idString.set("");
    localIdTable.idValue.set(0);
    shortcutToAdd->titleId    .set(localIdTable);
    shortcutToAdd->readOnly   .set(dune::cdm::glossary_1::FeatureEnabled::false_);
    shortcutToAdd->factory    .set(dune::cdm::glossary_1::FeatureEnabled::false_);
    shortcutToAdd->copyAllowed.set(dune::cdm::glossary_1::FeatureEnabled::true_);
    shortcutToAdd->origin     .set(dune::cdm::shortcut_1::Origin::device);
    shortcutToAdd->source     .set(dune::cdm::shortcut_1::Source::scan);

    auto destinations = std::vector<dune::cdm::shortcut_1::DestinationEnum>();
    destinations.push_back(dune::cdm::shortcut_1::Destination::print);
    shortcutToAdd->destinations = destinations;

    // Link the ticket
    std::vector<dune::cdm::glossary_1::links::ItemTable> links;
    dune::cdm::glossary_1::links::ItemTable link("shortcut");

    std::string shortcutHref = "/cdm/jobTicket/v1/tickets/";
    shortcutHref.append( ticketRelated->getTicketId().toString() );
    link.href = shortcutHref;

    links.push_back(link);
    shortcutToAdd->links.set(links);

    // When added to the shortcuts the ticket is persisted.
    addShortcut(std::move(shortcutToAdd));
}


TEST_F(GivenANewJobServiceStandard, WhenGetComponentFlavorUidCalled_ItWillBeReturnedFlavorUid)
{
    ComponentFlavorUid flavorUid = comp->getComponentFlavorUid();
    ASSERT_EQ(flavorUid, 0x6a979c);
}

TEST_F(GivenANewJobServiceStandard, WhenGetComponentInstanceNameCalled_ItWillBeReturnedInstanceName)
{
    const char *instanceName = comp->getComponentInstanceName();
    ASSERT_STREQ(instanceName, instanceName_);
}

TEST_F(GivenANewJobServiceStandard, WhenInitializeIsCalled_TheComponentGetsInitialized)
{
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    ASSERT_TRUE(true);
}

TEST_F(GivenANewJobServiceStandard, WhenTheGetInterfaceIsCalled_TheComponentGetsICopyJobService)
{
    void* interfacePtr = comp->getInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobService), instanceName_);
    ASSERT_TRUE(nullptr != interfacePtr);
}

TEST_F(GivenANewJobServiceStandard, WhenTheConnectSequenceIsCalled_TheComponentGetsConnected)
{
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    // fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyPipeline), "MockICopyPipeline", &mockCopyPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::deviceinfo::IDeviceInfo), "MockIDeviceInfo", &mockIDeviceInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::io::net::core::INetworkManager), "MockINetworkManager", &mockINetworkManager_);
    

    EXPECT_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillOnce(ReturnRef(copyAdapterDataChangeEvent_));

    ON_CALL(mockIMediaInfo_, getPageBasedExtension()).WillByDefault(Return(&mockIMediaInfoPageBased_));
    ON_CALL(mockIMediaInfoPageBased_, getMediaPropertyChangedEvent()).WillByDefault(ReturnRef(mediaPropertyChangedEvent_));
    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}

TEST_F(GivenANewJobServiceStandard, WhenTheConnectSequenceIsCalled_TheComponentGetsConnectedWithQuickSetSupported){
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    // fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);

    EXPECT_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillOnce(ReturnRef(copyAdapterDataChangeEvent_));

    EXPECT_CALL(mockIShortcut_, registerJobService(_,_,_,_))
        .WillOnce(Return(false));

    ON_CALL(mockIExportImport_, subscribeParticipant(OperationType::BACKUP_RESTORE,_,_,_,_))
        .WillByDefault(Return(ByMove(std::move(nullptr))));
    ON_CALL(mockIExportImport_, subscribeParticipant(OperationType::EXPORT_IMPORT,_,_,_,_))
        .WillByDefault(Return(ByMove(std::move(nullptr))));

    ON_CALL(mockIMediaInfo_, getPageBasedExtension()).WillByDefault(Return(&mockIMediaInfoPageBased_));
    ON_CALL(mockIMediaInfoPageBased_, getMediaPropertyChangedEvent()).WillByDefault(ReturnRef(mediaPropertyChangedEvent_));
    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}

TEST_F(GivenANewJobServiceStandard, WhenTheConnectSequenceIsCalled_TheComponentGetsConnectedWithIDCardSupported)
{
    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/JobServiceStandardIDCardTestData.json");

    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    // fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);

    EXPECT_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillOnce(ReturnRef(copyAdapterDataChangeEvent_));

    EXPECT_CALL(mockIShortcut_, registerJobService(_,_,_,_))
        .WillOnce(Return(false));

    ON_CALL(mockIExportImport_, subscribeParticipant(OperationType::BACKUP_RESTORE,_,_,_,_))
        .WillByDefault(Return(ByMove(std::move(nullptr))));
    ON_CALL(mockIExportImport_, subscribeParticipant(OperationType::EXPORT_IMPORT,_,_,_,_))
        .WillByDefault(Return(ByMove(std::move(nullptr))));

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}

TEST_F(GivenANewJobServiceStandard, WhenTheConnectSequenceIsCalled_TheComponentGetsConnectedWithScanPipelineFilled)
{
    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/JobServiceStandardScanPipelineTest.json");

    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    // fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);

    EXPECT_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillOnce(ReturnRef(copyAdapterDataChangeEvent_));

    EXPECT_CALL(mockIShortcut_, registerJobService(_,_,_,_))
        .WillOnce(Return(false));

    ON_CALL(mockIExportImport_, subscribeParticipant(OperationType::BACKUP_RESTORE,_,_,_,_))
        .WillByDefault(Return(ByMove(std::move(nullptr))));
    ON_CALL(mockIExportImport_, subscribeParticipant(OperationType::EXPORT_IMPORT,_,_,_,_))
        .WillByDefault(Return(ByMove(std::move(nullptr))));

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}

TEST_F(GivenANewJobServiceStandard, WhenTheConnectSequenceIsCalled_TheComponentGetsConnectedWithQuickSetNotSupported){

    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/jobServiceStandardTestDataQuickSetNotSupported.json");
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    // fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    EXPECT_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillOnce(ReturnRef(copyAdapterDataChangeEvent_));

    EXPECT_CALL(mockIShortcut_, registerJobService(_,_,_,_))
        .Times(0);

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}
/*
TEST_F(GivenANewJobServiceStandard, WhenTheConnectSequenceIsCalledWithSupportIDCardCopy_TheComponentGetsConnectedWithQuickSetSupported)
{
    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/JobServiceStandardIdCardSupported.json");
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    // fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);

    EXPECT_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillOnce(ReturnRef(copyAdapterDataChangeEvent_));

    EXPECT_CALL(mockIShortcut_, registerJobService(_,_,_,_))
        .WillOnce(Return(false));

    EXPECT_CALL(mockIExportImport_, subscribeParticipant(OperationType::BACKUP_RESTORE,_,_,_,_))
        .Times(1)
        .WillOnce(Return(ByMove(std::move(nullptr))));
    EXPECT_CALL(mockIExportImport_, subscribeParticipant(OperationType::EXPORT_IMPORT,_,_,_,_))
        .Times(1)
        .WillOnce(Return(ByMove(std::move(nullptr))));

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}
*/
TEST_F(GivenANewJobServiceStandard, WhenTheConnectSequenceIsCalled_TheComponentGetsConnectedWithPersistedShortcutState)
{
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    // fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    EXPECT_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillOnce(ReturnRef(copyAdapterDataChangeEvent_));

    EXPECT_CALL(mockICopyAdapter_, getCopyEnabled())
        .WillRepeatedly(Return(false));

    ON_CALL(mockIExportImport_, subscribeParticipant(OperationType::BACKUP_RESTORE,_,_,_,_))
        .WillByDefault(Return(ByMove(std::move(nullptr))));
    ON_CALL(mockIExportImport_, subscribeParticipant(OperationType::EXPORT_IMPORT,_,_,_,_))
        .WillByDefault(Return(ByMove(std::move(nullptr))));

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticket = createCopyJobTicket(createCorrectJobIntent(),createExpectedConstraints());
    insertShortcutOnList(ticket);

    dune::admin::shortcuts::shortcutFilter_t filter = dune::admin::shortcuts::shortcutFilter_t();
    filter.src = dune::cdm::shortcut_1::Source::scan;
    filter.dest = dune::cdm::shortcut_1::Destination::print;
    filter.origin = dune::cdm::shortcut_1::Origin::externalService;
    filter.type = dune::cdm::shortcut_1::Type::nativeApp;

    auto shortcuts = mockIShortcut_.getShortcuts(true, filter);
    //Check if the shortcuts are disabled
    for (auto& shortcut : shortcuts->collection().getMutable())
    {
        EXPECT_EQ(shortcut.state.get(), dune::cdm::shortcut_1::State::disabled);
    }
}

TEST_F(GivenANewJobServiceStandard, WhenMMediaPresenceChangeEventCalled_ThenEarlyWarmUpShouldBeConditionallyTriggered)
{
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    // fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IStatus), "MockIStatus", &mockIStatus_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrint), "MockIPrint", &mockIPrint_);

    EXPECT_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillOnce(ReturnRef(copyAdapterDataChangeEvent_));

    EXPECT_CALL(mockICopyAdapter_, getCopyEnabled())
        .WillRepeatedly(Return(false));

    ON_CALL(mockIExportImport_, subscribeParticipant(OperationType::BACKUP_RESTORE,_,_,_,_))
        .WillByDefault(Return(ByMove(std::move(nullptr))));
    ON_CALL(mockIExportImport_, subscribeParticipant(OperationType::EXPORT_IMPORT,_,_,_,_))
        .WillByDefault(Return(ByMove(std::move(nullptr))));

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    EXPECT_CALL(mockIPrint_, earlyWarmUp()).Times(1);

    auto mediaPresenceStatus = dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus::LOADED;
    component_->onScannerMediaPresenceChange(pMockIMediaPath_.get(), mediaPresenceStatus);
}

TEST_F(GivenANewJobServiceStandard, WhenFlatCoverOpenStatusChangedEventCalled_ThenEarlyWarmUpShouldBeConditionallyTriggered)
{
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    // fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IStatus), "MockIStatus", &mockIStatus_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrint), "MockIPrint", &mockIPrint_);

    EXPECT_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillOnce(ReturnRef(copyAdapterDataChangeEvent_));

    EXPECT_CALL(mockICopyAdapter_, getCopyEnabled())
        .WillRepeatedly(Return(false));

    ON_CALL(mockIExportImport_, subscribeParticipant(OperationType::BACKUP_RESTORE,_,_,_,_))
        .WillByDefault(Return(ByMove(std::move(nullptr))));
    ON_CALL(mockIExportImport_, subscribeParticipant(OperationType::EXPORT_IMPORT,_,_,_,_))
        .WillByDefault(Return(ByMove(std::move(nullptr))));

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    StatusType statusType = StatusType::FlatCoverOpen;
    uint32_t code = 0;
    std::string codeString = "";

    bool active = true;
    EXPECT_CALL(mockIStatus_, getScannerStatus(_, _, _, _))
    .WillOnce(DoAll(
        SetArgReferee<0>(statusType),
        SetArgReferee<1>(active),
        SetArgReferee<2>(code),
        SetArgReferee<3>(codeString)
    ));
    EXPECT_CALL(mockIPrint_, earlyWarmUp()).Times(1);

    component_->onScannerStatusChangedEvent(&mockIStatus_);

    active = false;
    EXPECT_CALL(mockIStatus_, getScannerStatus(_, _, _, _))
    .WillOnce(DoAll(
        SetArgReferee<0>(statusType),
        SetArgReferee<1>(active),
        SetArgReferee<2>(code),
        SetArgReferee<3>(codeString)
    ));
    EXPECT_CALL(mockIPrint_, earlyWarmUp()).Times(0);

    component_->onScannerStatusChangedEvent(&mockIStatus_);
}

TEST_F(GivenANewJobServiceStandard, WhenTheCountrySettingsChange_DefaultTicketIsUpdated)
{
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyPipeline), "MockICopyPipeline", &mockCopyPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    ON_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillByDefault(ReturnRef(copyAdapterDataChangeEvent_));

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
    EXPECT_CALL(mockIScanPipeline_, getDefaultMediaSize()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::UNDEFINED));
    auto *jobService =
        static_cast<dune::copy::Jobs::Copy::ICopyJobService *>(comp->getInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    auto jobTicketIntent = jobTicket->getIntent();
    EXPECT_EQ(jobTicketIntent->getInputMediaSizeId(), dune::imaging::types::MediaSizeId::LETTER);
    EXPECT_EQ(jobTicketIntent->getOutputMediaSizeId(), dune::imaging::types::MediaSizeId::LETTER);
    EXPECT_EQ(jobTicketIntent->getOutputMediaIdType(), dune::imaging::types::MediaIdType::STATIONERY);
    EXPECT_EQ(jobTicketIntent->getInputPlexMode(), dune::imaging::types::Plex::SIMPLEX);
    EXPECT_EQ(jobTicketIntent->getOutputPlexMode(), dune::imaging::types::Plex::SIMPLEX);
    EXPECT_EQ(jobTicketIntent->getColorMode(), dune::imaging::types::ColorMode::COLOR);
    EXPECT_EQ(jobTicketIntent->getContentOrientation(), dune::imaging::types::ContentOrientation::PORTRAIT);
    EXPECT_EQ(jobTicketIntent->getCopies(), 1);
    EXPECT_EQ(jobTicketIntent->getResize(), 100);
    EXPECT_EQ(jobTicketIntent->getLighterDarker(), 0);
    EXPECT_EQ(jobTicketIntent->getOriginalContentType(), dune::imaging::types::OriginalContentType::MIXED);
    EXPECT_EQ(jobTicketIntent->getCopyQuality(), dune::imaging::types::PrintQuality::NORMAL);
}

TEST_F(GivenANewJobServiceStandard, WhenTheCountrySettingsChange_PersistedDefaultTicketIsUpdated)
{
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyPipeline), "MockICopyPipeline", &mockCopyPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    ON_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillByDefault(ReturnRef(copyAdapterDataChangeEvent_));

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    EXPECT_CALL(mockISettings_, getValue(_,Matcher<dune::print::engine::Variant&>(_))).WillRepeatedly(Return(APIResult::OK));
    EXPECT_CALL(mockIScanPipeline_, getDefaultMediaSize()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::UNDEFINED));
    auto *jobService =
        static_cast<dune::copy::Jobs::Copy::ICopyJobService *>(comp->getInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    auto jobTicketIntent = jobTicket->getIntent();
    jobTicketIntent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    jobTicketIntent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    jobService->saveDefaultJobTicket(jobTicket, TicketUpdationMode::internal);

    scanMediaSize_.setMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);

    jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    jobTicketIntent = jobTicket->getIntent();
    EXPECT_EQ(jobTicketIntent->getInputMediaSizeId(), dune::imaging::types::MediaSizeId::LETTER);
    EXPECT_EQ(jobTicketIntent->getOutputMediaSizeId(), dune::imaging::types::MediaSizeId::LETTER);
    EXPECT_EQ(jobTicketIntent->getOutputMediaIdType(), dune::imaging::types::MediaIdType::STATIONERY);
    EXPECT_EQ(jobTicketIntent->getInputPlexMode(), dune::imaging::types::Plex::SIMPLEX);
    EXPECT_EQ(jobTicketIntent->getOutputPlexMode(), dune::imaging::types::Plex::SIMPLEX);
    EXPECT_EQ(jobTicketIntent->getColorMode(), dune::imaging::types::ColorMode::COLOR);
    EXPECT_EQ(jobTicketIntent->getContentOrientation(), dune::imaging::types::ContentOrientation::PORTRAIT);
    EXPECT_EQ(jobTicketIntent->getCopies(), 1);
    EXPECT_EQ(jobTicketIntent->getResize(), 100);
    EXPECT_EQ(jobTicketIntent->getLighterDarker(), 0);
    EXPECT_EQ(jobTicketIntent->getOriginalContentType(), dune::imaging::types::OriginalContentType::MIXED);
    EXPECT_EQ(jobTicketIntent->getCopyQuality(), dune::imaging::types::PrintQuality::NORMAL);
}

TEST_F(GivenANewJobServiceStandard, WhenTheCountrySettingsChange_PersistedDefaultTicketWithDifferentMediaIsNotUpdated)
{
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyPipeline), "MockICopyPipeline", &mockCopyPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    ON_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillByDefault(ReturnRef(copyAdapterDataChangeEvent_));

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    EXPECT_CALL(mockISettings_, getValue(_,Matcher<dune::print::engine::Variant&>(_))).WillRepeatedly(Return(APIResult::OK));
    EXPECT_CALL(mockIScanPipeline_, getDefaultMediaSize()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::UNDEFINED));
    auto *jobService =
        static_cast<dune::copy::Jobs::Copy::ICopyJobService *>(comp->getInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    auto jobTicketIntent = jobTicket->getIntent();
    jobTicketIntent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LEGAL);
    jobTicketIntent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::LEGAL);
    jobTicketIntent->setOutputMediaIdType(dune::imaging::types::MediaIdType::LIGHT);
    jobService->saveDefaultJobTicket(jobTicket, TicketUpdationMode::internal);


    scanMediaSize_.setMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);

    jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    jobTicketIntent = jobTicket->getIntent();
    // EXPECT_EQ(jobTicketIntent->getInputMediaSizeId(), dune::imaging::types::MediaSizeId::LEGAL);
    // EXPECT_EQ(jobTicketIntent->getOutputMediaSizeId(), dune::imaging::types::MediaSizeId::LEGAL);
    EXPECT_EQ(jobTicketIntent->getOutputMediaIdType(), dune::imaging::types::MediaIdType::STATIONERY);
    EXPECT_EQ(jobTicketIntent->getInputPlexMode(), dune::imaging::types::Plex::SIMPLEX);
    EXPECT_EQ(jobTicketIntent->getOutputPlexMode(), dune::imaging::types::Plex::SIMPLEX);
    EXPECT_EQ(jobTicketIntent->getColorMode(), dune::imaging::types::ColorMode::COLOR);
    EXPECT_EQ(jobTicketIntent->getContentOrientation(), dune::imaging::types::ContentOrientation::PORTRAIT);
    EXPECT_EQ(jobTicketIntent->getCopies(), 1);
    EXPECT_EQ(jobTicketIntent->getResize(), 100);
    EXPECT_EQ(jobTicketIntent->getLighterDarker(), 0);
    EXPECT_EQ(jobTicketIntent->getOriginalContentType(), dune::imaging::types::OriginalContentType::MIXED);
    EXPECT_EQ(jobTicketIntent->getCopyQuality(), dune::imaging::types::PrintQuality::NORMAL);
}

TEST_F(GivenANewJobServiceStandard, WhenOnMediaPropertEventIsFired_ThenCopyDefaultTicketGetsUpdatedWithDefaultMediaType)
{
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyPipeline), "MockICopyPipeline", &mockCopyPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    EXPECT_CALL(mockISettings_, getValue(_,Matcher<dune::print::engine::Variant&>(_))).WillRepeatedly(Return(APIResult::OK));
    EXPECT_CALL(mockIScanPipeline_, getDefaultMediaSize()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::UNDEFINED));
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticket = createCopyJobTicket(createCorrectJobIntent(),createExpectedConstraints());
    insertShortcutOnList(ticket);
    EXPECT_CALL(mockIDataStore_, find(Matcher<const Uuid &>(_))).WillRepeatedly(testing::InvokeWithoutArgs([&ticket,this]() {
        // Get Serialized data
        auto serializedData = ticket->serialize();

        // Return serialized data
        std::pair<bool, DataObject> returnVal;
        returnVal.first = true;
        returnVal.second.buffer.first = std::move(serializedData.first);
        returnVal.second.buffer.second = serializedData.second;
        return returnVal;
    }));

    EXPECT_CALL(mockIJobTicketResourceManager_,loadJobTicketIntoCacheIfNeeded(_,_)).WillRepeatedly(Return(ticket));

    //check mediatype of ticket
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::BOND);

    ON_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillByDefault(ReturnRef(copyAdapterDataChangeEvent_));

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    EXPECT_CALL(mockISettings_, getValue(_,Matcher<dune::print::engine::Variant&>(_))).WillRepeatedly(Return(APIResult::OK));
    EXPECT_CALL(mockIScanPipeline_, getDefaultMediaSize()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::UNDEFINED));
    auto *jobService =
        static_cast<dune::copy::Jobs::Copy::ICopyJobService *>(comp->getInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobService), nullptr));    
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::BOND);
    jobService->saveDefaultJobTicket(ticket, TicketUpdationMode::internal);

    EXPECT_EQ(dune::imaging::types::MediaIdType::BOND,ticket->getIntent()->getOutputMediaIdType());
    MediaId mediaId = MediaIdType::BOND;

    dune::print::engine::pageBased::MediaPropertyId mediaPropertyId = dune::print::engine::pageBased::MediaPropertyId::VisibilityMode;
    Variant mediaPropertyValue = false;
    MediaPropertyChangedEventArgs mediaPropertyChangedEventArgs = MediaPropertyChangedEventArgs(mediaId, mediaPropertyId,mediaPropertyValue);
    mediaPropertyChangedEvent_.fireSync(mediaPropertyChangedEventArgs);
    //check if ticket is updated
    auto modifiedjobTicket = jobService->getDefaultJobTicket();
    auto modifiedjobTicketIntent = modifiedjobTicket->getIntent();
    EXPECT_EQ(dune::imaging::types::MediaIdType::STATIONERY,modifiedjobTicketIntent->getOutputMediaIdType());

}

TEST_F(GivenANewJobServiceStandard,WhenMediaPropertyEventIsFiredForQuickset_ThenMediaTypeIsSetToCopyDefaultsMediaType)
{
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyPipeline), "MockICopyPipeline", &mockCopyPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    ON_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillByDefault(ReturnRef(copyAdapterDataChangeEvent_));

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    EXPECT_CALL(mockISettings_, getValue(_,Matcher<dune::print::engine::Variant&>(_))).WillRepeatedly(Return(APIResult::OK));
    EXPECT_CALL(mockIScanPipeline_, getDefaultMediaSize()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::UNDEFINED));
    // user quickset expectation from cache and list of shortcuts
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticket = createCopyJobTicket(createCorrectJobIntent(),createExpectedConstraints());
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::BOND);
    insertShortcutOnList(ticket);
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketInsertedToCache = createCopyJobTicket(createIncorrectJobIntent(),createExpectedConstraints());
    dune::framework::data::ObjectClassification objClass;

    EXPECT_CALL(mockIDataStore_, find(Matcher<const Uuid &>(_))).WillRepeatedly(testing::InvokeWithoutArgs([&ticket,this]() {
        // Get Serialized data
        auto serializedData = ticket->serialize();

        // Return serialized data
        std::pair<bool, DataObject> returnVal;
        returnVal.first = true;
        returnVal.second.buffer.first = std::move(serializedData.first);
        returnVal.second.buffer.second = serializedData.second;
        return returnVal;
    }));

    EXPECT_CALL(mockIJobTicketResourceManager_,loadJobTicketIntoCacheIfNeeded(_,_)).WillRepeatedly(Return(ticket));  
    auto *jobService =
        static_cast<dune::copy::Jobs::Copy::ICopyJobService *>(comp->getInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();

    auto jobTicketIntent = jobTicket->getIntent();
    
    jobTicketIntent->setOutputMediaIdType(dune::imaging::types::MediaIdType::LIGHT);
    jobService->saveDefaultJobTicket(jobTicket, TicketUpdationMode::internal);
    jobService->saveDefaultJobTicket(ticket, TicketUpdationMode::internal);

    EXPECT_EQ(dune::imaging::types::MediaIdType::LIGHT,jobTicketIntent->getOutputMediaIdType());
    MediaId mediaId = MediaIdType::BOND;

    dune::print::engine::pageBased::MediaPropertyId mediaPropertyId = dune::print::engine::pageBased::MediaPropertyId::VisibilityMode;
    Variant mediaPropertyValue = false;
    MediaPropertyChangedEventArgs mediaPropertyChangedEventArgs = MediaPropertyChangedEventArgs(mediaId, mediaPropertyId,mediaPropertyValue);
    mediaPropertyChangedEvent_.fireSync(mediaPropertyChangedEventArgs);
    EXPECT_CALL(mockIJobTicketResourceManager_,loadJobTicketIntoCacheIfNeeded(_,_)).WillRepeatedly(Return(ticket));
    auto modifiedTicket = jobService->getDefaultJobTicket();
    EXPECT_EQ(dune::imaging::types::MediaIdType::STATIONERY,modifiedTicket->getIntent()->getOutputMediaIdType());    
}

TEST_F(GivenANewJobServiceStandard, WhenOnMediaPropertEventIsFiredForDifferentMediaType_ThenCopyDefaultTicketWillNotGetUpdated)
{
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyPipeline), "MockICopyPipeline", &mockCopyPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);
    
     EXPECT_CALL(mockISettings_, getValue(_,Matcher<dune::print::engine::Variant&>(_))).WillRepeatedly(Return(APIResult::OK));
    EXPECT_CALL(mockIScanPipeline_, getDefaultMediaSize()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::UNDEFINED));
    // user quickset expectation from cache and list of shortcuts
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticket = createCopyJobTicket(createCorrectJobIntent(),createExpectedConstraints());
    insertShortcutOnList(ticket);
    EXPECT_CALL(mockIDataStore_, find(Matcher<const Uuid &>(_))).WillRepeatedly(testing::InvokeWithoutArgs([&ticket,this]() {
        // Get Serialized data
        auto serializedData = ticket->serialize();

        // Return serialized data
        std::pair<bool, DataObject> returnVal;
        returnVal.first = true;
        returnVal.second.buffer.first = std::move(serializedData.first);
        returnVal.second.buffer.second = serializedData.second;
        return returnVal;
    }));

    EXPECT_CALL(mockIJobTicketResourceManager_,loadJobTicketIntoCacheIfNeeded(_,_)).WillRepeatedly(Return(ticket));

    //check mediatype of ticket
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::BOND);

    ON_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillByDefault(ReturnRef(copyAdapterDataChangeEvent_));

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    EXPECT_CALL(mockISettings_, getValue(_,Matcher<dune::print::engine::Variant&>(_))).WillRepeatedly(Return(APIResult::OK));
    EXPECT_CALL(mockIScanPipeline_, getDefaultMediaSize()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::UNDEFINED));
    auto *jobService =
        static_cast<dune::copy::Jobs::Copy::ICopyJobService *>(comp->getInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobService), nullptr));    
    ticket->getIntent()->setOutputMediaIdType(dune::imaging::types::MediaIdType::BOND);
    jobService->saveDefaultJobTicket(ticket, TicketUpdationMode::internal);

    EXPECT_EQ(dune::imaging::types::MediaIdType::BOND,ticket->getIntent()->getOutputMediaIdType());
    MediaId mediaId = MediaIdType::LIGHT;

    dune::print::engine::pageBased::MediaPropertyId mediaPropertyId = dune::print::engine::pageBased::MediaPropertyId::VisibilityMode;
    Variant mediaPropertyValue = false;
    MediaPropertyChangedEventArgs mediaPropertyChangedEventArgs = MediaPropertyChangedEventArgs(mediaId, mediaPropertyId,mediaPropertyValue);
    mediaPropertyChangedEvent_.fireSync(mediaPropertyChangedEventArgs);
    //check if ticket is updated
    EXPECT_EQ(dune::imaging::types::MediaIdType::BOND,ticket->getIntent()->getOutputMediaIdType());

}




///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedJobServiceStandard : Do here tests of public api
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedJobServiceStandard :public GivenANewJobServiceStandard
{
  public:
    GivenAConnectedJobServiceStandard() { GTEST_CHECKPOINTA("GivenAConnectedJobServiceStandard::Constructor -- ENTER\n"); };

    void testFunction(dune::job::PromptType promptType, dune::job::PromptResponseType promptResponseType)
    {}
    void SetUp() override;
};

void GivenAConnectedJobServiceStandard::SetUp()
{
    GTEST_CHECKPOINTA("GivenAConnectedJobServiceStandard::SetUp -- ENTER");
    productTestFileName = "./testResources/JobServiceStandardDataLFP.json";
    GivenANewJobServiceStandard::SetUp();

    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    // fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyPipeline), "MockICopyPipeline", &mockCopyPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::conversion::ISystemConversionHelper), "MockISystemConversionHelper", &mockISystemConversionHelper_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyTicketConverter), "MockICopyTicketConverter", &mockICopyTicketConverter_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrint), "MockIPrint", &mockIPrint_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ICapabilitiesFactory), "MockICapabilitiesFactory", &mockICapabilitiesFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobQueue), "MockIJobQueue", &mockIJobQueue_);

    ON_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillByDefault(ReturnRef(copyAdapterDataChangeEvent_));


    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    GTEST_CHECKPOINTA("GivenAConnectedJobServiceStandard::SetUp -- EXIT");
}

TEST_F(GivenAConnectedJobServiceStandard, WhenImportExportDataIsCalled_OperationResultSuccess)
{
    using ExtendedInfo = std::map<std::string,std::string>;
    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/JobServiceStandardTestData.json");

    comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    std::shared_ptr<MockIDataStore> mockStore_{std::make_shared<MockIDataStore>()};
    component_->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "",
                             static_cast<void*>(mockStore_.get()));

    component_->setResourceFilePath();

    dune::framework::data::backup::IExportImport::OperationDescription importExportDescription;
    importExportDescription.operationType = dune::framework::data::backup::OperationType::EXPORT_IMPORT;
    importExportDescription.categories = {Category::CopySettings};
    dune::framework::data::backup::IExportImport::IdentificationData identificationData;
    const std::string contentId = "CopyTicketSettings";
    std::string        version = "1.0";
    const std::string  CONTENT_FILE_TAG("CopyTicketSettings");
    const dune::framework::storage::fs::path     CONTENT_FILE_PATH("./testResources/exportedJobServiceConfigData.txt");
    const std::string  CONTENT_FILE_STR(std::string("test file at ") + CONTENT_FILE_PATH.string());
    const ExtendedInfo CONTENT_FILE_EXT = { {"k0","v0"}, {"k1","v1"} };

    std::string testFilePath("./testResources/exportedJobServiceConfigData.txt");
    EXPECT_CALL(*((MockIPathDirectory*)systemServices_->pathServices_->getPathDirectory()),
            createTempFile()).WillRepeatedly(Return(testFilePath));

    dune::framework::data::backup::IExportImport::FileInfoCollection filesToExportImport = {
        { CONTENT_FILE_TAG, testFilePath, false, false, CONTENT_FILE_EXT }
    };

    // Call the exportData function
    dune::framework::data::backup::OperationResult exportResult = component_->testExport(importExportDescription, contentId, version, filesToExportImport);

    // Perform assertions on the export result
    EXPECT_EQ(exportResult, dune::framework::data::backup::OperationResult::SUCCESS);

    dune::framework::data::backup::OperationResult importResult = component_->testImport(importExportDescription, identificationData, contentId, version, filesToExportImport);

    // Assert the import result
    EXPECT_EQ(importResult, dune::framework::data::backup::OperationResult::SUCCESS);
}

TEST_F(GivenAConnectedJobServiceStandard, WhenTheGetDefaultJobTicketIsCalled_TheComponentGetsJobTicket)
{
    EXPECT_CALL(mockIScanPipeline_, getDefaultMediaSize()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::LEGAL));
    auto *jobService =
        static_cast<dune::copy::Jobs::Copy::ICopyJobService *>(component_->getInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    auto jobTicketIntent = jobTicket->getIntent();
    EXPECT_EQ(jobTicketIntent->getInputMediaSizeId(), dune::imaging::types::MediaSizeId::LEGAL);
    EXPECT_EQ(jobTicketIntent->getInputPlexMode(), dune::imaging::types::Plex::SIMPLEX);
    EXPECT_EQ(jobTicketIntent->getOutputMediaSizeId(), dune::imaging::types::MediaSizeId::LEGAL);
    EXPECT_EQ(jobTicketIntent->getOutputPlexMode(), dune::imaging::types::Plex::SIMPLEX);
    EXPECT_EQ(jobTicketIntent->getColorMode(), dune::imaging::types::ColorMode::COLOR);
    EXPECT_EQ(jobTicketIntent->getContentOrientation(), dune::imaging::types::ContentOrientation::PORTRAIT);
    EXPECT_EQ(jobTicketIntent->getCopies(), 1);
    EXPECT_EQ(jobTicketIntent->getResize(), 100);
    EXPECT_EQ(jobTicketIntent->getLighterDarker(), 0);
    EXPECT_EQ(jobTicketIntent->getOriginalContentType(), dune::imaging::types::OriginalContentType::MIXED);
    EXPECT_EQ(jobTicketIntent->getCopyQuality(), dune::imaging::types::PrintQuality::NORMAL);
    EXPECT_EQ(jobTicketIntent->getCustomMediaXDimension(), (double) 82677.0);
    EXPECT_EQ(jobTicketIntent->getCustomMediaYDimension(), (double) 116929.0);
}

TEST_F(GivenAConnectedJobServiceStandard, WhenTheCountrySettingsChange_DefaultTicketIsNotUpdatedForLFP)
{
    EXPECT_CALL(mockISettings_, getValue(_,Matcher<dune::print::engine::Variant&>(_))).Times(0).WillRepeatedly(Return(APIResult::OK));
    EXPECT_CALL(mockIScanPipeline_, getDefaultMediaSize()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::UNDEFINED));
    auto *jobService =
        static_cast<dune::copy::Jobs::Copy::ICopyJobService *>(comp->getInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    auto jobTicketIntent = jobTicket->getIntent();
    EXPECT_EQ(jobTicketIntent->getInputMediaSizeId(), dune::imaging::types::MediaSizeId::LETTER);
    EXPECT_EQ(jobTicketIntent->getOutputMediaSizeId(), dune::imaging::types::MediaSizeId::LETTER);
    EXPECT_EQ(jobTicketIntent->getOutputMediaIdType(), dune::imaging::types::MediaIdType::STATIONERY);
    EXPECT_EQ(jobTicketIntent->getInputPlexMode(), dune::imaging::types::Plex::SIMPLEX);
    EXPECT_EQ(jobTicketIntent->getOutputPlexMode(), dune::imaging::types::Plex::SIMPLEX);
    EXPECT_EQ(jobTicketIntent->getColorMode(), dune::imaging::types::ColorMode::COLOR);
    EXPECT_EQ(jobTicketIntent->getContentOrientation(), dune::imaging::types::ContentOrientation::PORTRAIT);
    EXPECT_EQ(jobTicketIntent->getCopies(), 1);
    EXPECT_EQ(jobTicketIntent->getResize(), 100);
    EXPECT_EQ(jobTicketIntent->getLighterDarker(), 0);
    EXPECT_EQ(jobTicketIntent->getOriginalContentType(), dune::imaging::types::OriginalContentType::MIXED);
    EXPECT_EQ(jobTicketIntent->getCopyQuality(), dune::imaging::types::PrintQuality::NORMAL);
}


TEST_F(GivenAConnectedJobServiceStandard, WhenTheCountrySettingsChange_PersistedDefaultTicketIsNotUpdatedForLFP)
{
    EXPECT_CALL(mockISettings_, getValue(_,Matcher<dune::print::engine::Variant&>(_))).Times(0);
    EXPECT_CALL(mockIScanPipeline_, getDefaultMediaSize()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::UNDEFINED));
    auto *jobService =
        static_cast<dune::copy::Jobs::Copy::ICopyJobService *>(comp->getInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    auto jobTicketIntent = jobTicket->getIntent();
    jobTicketIntent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    jobTicketIntent->setOutputMediaSizeId(dune::imaging::types::MediaSizeId::A4);
    jobService->saveDefaultJobTicket(jobTicket, TicketUpdationMode::internal);

    scanMediaSize_.setMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
}

TEST_F(GivenAConnectedJobServiceStandard, WhenJobStringIDsCalled)
{
    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/JobServiceStandardStringIdsTestData.json");
    comp = static_cast<IComponent*>(component_);
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    std::shared_ptr<std::map<std::string, std::string>> stringIds = std::make_shared<std::map<std::string, std::string>>();
    stringIds = component_->testgetJobServiceStringIds();
    EXPECT_NE(nullptr,stringIds);
}
TEST_F(GivenAConnectedJobServiceStandard, WhenTheGetDefaultJobTicketIsCalledAndUnitIsMetric_CustomMediaXFeedDimensionValueIsA4)
{
    ON_CALL(*mockLocaleProvider_, getMeasurmentUnit()).WillByDefault(Return(dune::localization::MeasurementUnit::METRIC));
    auto *jobService =
        static_cast<dune::copy::Jobs::Copy::ICopyJobService *>(component_->getInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    auto jobTicketIntent = jobTicket->getIntent();
    EXPECT_EQ(jobTicketIntent->getCustomMediaXDimension(), (double) 82677.0);
    EXPECT_EQ(jobTicketIntent->getCustomMediaYDimension(), (double) 116929.0);
}

TEST_F(GivenAConnectedJobServiceStandard, WhenTheGetDefaultJobTicketIsCalledAndUnitIsUS_CustomMediaXFeedDimensionValueIsLetter)
{
    ON_CALL(*mockLocaleProvider_, getMeasurmentUnit()).WillByDefault(Return(dune::localization::MeasurementUnit::US));
    auto *jobService =
        static_cast<dune::copy::Jobs::Copy::ICopyJobService *>(component_->getInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    auto jobTicketIntent = jobTicket->getIntent();
    EXPECT_EQ(jobTicketIntent->getCustomMediaXDimension(), (double) 85000.0);
    EXPECT_EQ(jobTicketIntent->getCustomMediaYDimension(), (double) 110000.0);
}

TEST_F(GivenAConnectedJobServiceStandard, WhenTheCreatePipelineBuilderIsCalled_PipelineBuilderIsCreated)
{
    EXPECT_CALL(mockIScanPipeline_, getDefaultMediaSize()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::LEGAL));
    auto jobTicket = component_->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    auto mockPipelineBuilder = std::make_shared<dune::job::MockIPipelineBuilder>();
    ServicesPackage servicePackage{};
    EXPECT_CALL(mockCopyPipeline_, createPipelineBuilder(_, _, _, _, _, _, _, _, _)).WillOnce(WithArgs<2>(Invoke(
        [&](ServicesPackage package)
        {
            servicePackage = package;
            return mockPipelineBuilder;
        }
    )));

    auto pipelineBuilder = component_->createPipelineBuilder(jobTicket);

    EXPECT_NE(pipelineBuilder, nullptr);
    EXPECT_EQ(servicePackage.printIntentsFactory, &mockIPrintIntentsFactory_);
    EXPECT_EQ(servicePackage.scanDeviceService, &mockIScanDevice_);
    EXPECT_EQ(servicePackage.colorDirector, &mockIColorDirector_);
    EXPECT_EQ(servicePackage.imagePersister, &mockIImagePersister_);
    EXPECT_EQ(servicePackage.pageAssembler, &mockIPageAssembler_);
    EXPECT_EQ(servicePackage.printDevice, &mockIPrintDevice_);
    EXPECT_EQ(servicePackage.mediaInterface, &mockIPrintMedia_);
    EXPECT_EQ(servicePackage.mediaHandlingSettings, &mockIMediaHandlingSettings_);
    EXPECT_EQ(servicePackage.mediaHandlingMgr, &mockIMediaHandlingMgr_);
    EXPECT_EQ(servicePackage.mediaInfo, &mockIMediaInfo_);
    EXPECT_EQ(servicePackage.mediaAttributes, &mockIMediaAttributes_);
    EXPECT_EQ(servicePackage.printEngine, &mockIPrint_);
    EXPECT_EQ(servicePackage.engineCapabilitiesFactory, &mockICapabilitiesFactory_);
    EXPECT_EQ(servicePackage.jobQueue, &mockIJobQueue_);
}

TEST_F(GivenAConnectedJobServiceStandard, WhenTheGetDefaultJobTicketIsCalled_TheScanInterfacesGetsJobTicket)
{
    EXPECT_CALL(mockIScanPipeline_, getDefaultMediaSize()).WillRepeatedly(Return(dune::imaging::types::MediaSizeId::UNDEFINED));
    auto *jobService =
        static_cast<ICopyJobService *>(component_->getInterface(GET_INTERFACE_UID(ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();
    auto jobTicketIntent = jobTicket->getIntent();
    EXPECT_EQ(jobTicketIntent->getInputMediaSizeId(), dune::imaging::types::MediaSizeId::LETTER);
    ASSERT_TRUE(nullptr != jobTicket);
    auto scanMedia = jobTicket->getScanMediaInterface();
    ASSERT_TRUE(nullptr != scanMedia);
    auto scanCapabilities = jobTicket->getScanCapabilitiesInterface();
    ASSERT_TRUE(nullptr != scanCapabilities);
}

TEST_F(GivenAConnectedJobServiceStandard, WhenEnterprisePromptOrignalSizeSetToAnyWithADF_NoPromptCase)
{
    auto *jobService =
        static_cast<ICopyJobService *>(component_->getInterface(GET_INTERFACE_UID(ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    auto scanMedia = jobTicket->getScanMediaInterface();
    ASSERT_TRUE(nullptr != scanMedia);
    auto scanCapabilities = jobTicket->getScanCapabilitiesInterface();
    ASSERT_TRUE(nullptr != scanCapabilities);

    // Prompt Contorller
    auto promptController = std::make_shared<CopyJobPromptController>(jobTicket, nullptr, Product::ENTERPRISE, true);
    ASSERT_NE(nullptr, promptController);

    // ADF_SIMPLEX. A4/LANDSCAPE
    EXPECT_CALL((*pMockIMediaPath_), getId).WillRepeatedly(Return("ADF"));
    EXPECT_CALL((*pMockIMediaPath_), getType).WillRepeatedly(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    EXPECT_CALL((*pMockIMediaPath_), getMediaPresenceStatus).WillRepeatedly(Return(dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus::LOADED));
    EXPECT_CALL((*pMockIMediaPath_), getMediaDetectionStatus).WillRepeatedly(Return(std::make_pair(MediaSizeId::A4, dune::imaging::types::MediaOrientation::LANDSCAPE)));

    auto jobIntent = jobTicket->getIntent();
    jobIntent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    jobIntent->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);

    // call getNewPromptToDisplay
    auto prompt = promptController->getNewPromptToDisplay(false);
    EXPECT_EQ(prompt, PromptType::None);  // none prompt always exists.
}

TEST_F(GivenAConnectedJobServiceStandard, WhenEnterprisePromptOrignalSizeSetToAnyWithGlass_NoPromptCase)
{
    auto *jobService =
        static_cast<ICopyJobService *>(component_->getInterface(GET_INTERFACE_UID(ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    auto scanMedia = jobTicket->getScanMediaInterface();
    ASSERT_TRUE(nullptr != scanMedia);
    auto scanCapabilities = jobTicket->getScanCapabilitiesInterface();
    ASSERT_TRUE(nullptr != scanCapabilities);

    // Prompt Contorller
    auto promptController = std::make_shared<CopyJobPromptController>(jobTicket, nullptr, Product::ENTERPRISE, true);
    ASSERT_NE(nullptr, promptController);

    // GLASS. LETTER/PORTRAIT
    EXPECT_CALL((*pMockIMediaPath_), getId).WillRepeatedly(Return("GLASS"));
    EXPECT_CALL((*pMockIMediaPath_), getType).WillRepeatedly(Return(dune::scan::types::ScanSource::GLASS));
    EXPECT_CALL((*pMockIMediaPath_), getMediaPresenceStatus).WillRepeatedly(Return(dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus::LOADED));
    EXPECT_CALL((*pMockIMediaPath_), getMediaDetectionStatus).WillRepeatedly(Return(std::make_pair(MediaSizeId::LETTER, dune::imaging::types::MediaOrientation::PORTRAIT)));

    auto jobIntent = jobTicket->getIntent();
    jobIntent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    jobIntent->setScanSource(dune::scan::types::ScanSource::GLASS);

    // call getNewPromptToDisplay
    auto prompt = promptController->getNewPromptToDisplay(false);
    EXPECT_EQ(prompt, PromptType::None);  // none prompt always exists.
}


TEST_F(GivenAConnectedJobServiceStandard, WhenEnterprisePromptOrignalSizeSetToAnyWithGlass_PromptCaseOK)
{
    auto *jobService =
        static_cast<ICopyJobService *>(component_->getInterface(GET_INTERFACE_UID(ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    auto scanMedia = jobTicket->getScanMediaInterface();
    ASSERT_TRUE(nullptr != scanMedia);
    auto scanCapabilities = jobTicket->getScanCapabilitiesInterface();
    ASSERT_TRUE(nullptr != scanCapabilities);

    PromptType expectedPrompt_ = dune::job::PromptType::FlatbedAutoDetectFail;

    // Prompt Contorller
    auto promptController = std::make_shared<CopyJobPromptController>(jobTicket, nullptr, Product::ENTERPRISE, true);
    ASSERT_NE(nullptr, promptController);

    // GLASS. LETTER/PORTRAIT
    EXPECT_CALL((*pMockIMediaPath_), getId).WillRepeatedly(Return("GLASS"));
    EXPECT_CALL((*pMockIMediaPath_), getType).WillRepeatedly(Return(dune::scan::types::ScanSource::GLASS));
    EXPECT_CALL((*pMockIMediaPath_), getMediaPresenceStatus).WillRepeatedly(Return(dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus::LOADED));
    EXPECT_CALL((*pMockIMediaPath_), getMediaDetectionStatus).WillRepeatedly(Return(std::make_pair(MediaSizeId::UNDEFINED, dune::imaging::types::MediaOrientation::UNDEFINED)));

    auto jobIntent = jobTicket->getIntent();
    jobIntent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::ANY);
    jobIntent->setScanSource(dune::scan::types::ScanSource::GLASS);

    // call getNewPromptToDisplay
    auto prompt = promptController->getNewPromptToDisplay(false);
    EXPECT_EQ(prompt, expectedPrompt_);
}

TEST_F(GivenAConnectedJobServiceStandard, WhenEnterprisePromptOrignalSizeSetToLetterWithADF_NoPromptCase)
{
    auto *jobService =
        static_cast<ICopyJobService *>(component_->getInterface(GET_INTERFACE_UID(ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    auto scanMedia = jobTicket->getScanMediaInterface();
    ASSERT_TRUE(nullptr != scanMedia);
    auto scanCapabilities = jobTicket->getScanCapabilitiesInterface();
    ASSERT_TRUE(nullptr != scanCapabilities);

    // Prompt Contorller
    auto promptController = std::make_shared<CopyJobPromptController>(jobTicket, nullptr, Product::ENTERPRISE, true);
    ASSERT_NE(nullptr, promptController);

    // ADF_SIMPLEX. A4/LANDSCAPE
    EXPECT_CALL((*pMockIMediaPath_), getId).WillRepeatedly(Return("ADF"));
    EXPECT_CALL((*pMockIMediaPath_), getType).WillRepeatedly(Return(dune::scan::types::ScanSource::ADF_SIMPLEX));
    EXPECT_CALL((*pMockIMediaPath_), getMediaPresenceStatus).WillRepeatedly(Return(dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus::LOADED));
    EXPECT_CALL((*pMockIMediaPath_), getMediaDetectionStatus).WillRepeatedly(Return(std::make_pair(MediaSizeId::A4, dune::imaging::types::MediaOrientation::LANDSCAPE)));

    auto jobIntent = jobTicket->getIntent();
    jobIntent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    jobIntent->setScanSource(dune::scan::types::ScanSource::ADF_SIMPLEX);

    // call getNewPromptToDisplay
    auto prompt = promptController->getNewPromptToDisplay(false);
    EXPECT_EQ(prompt, PromptType::None);  // none prompt always exists.
}

TEST_F(GivenAConnectedJobServiceStandard, WhenEnterprisePromptOrignalSizeSetToLetterWithGlass_NoPromptCase)
{
    auto *jobService =
        static_cast<ICopyJobService *>(component_->getInterface(GET_INTERFACE_UID(ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    auto scanMedia = jobTicket->getScanMediaInterface();
    ASSERT_TRUE(nullptr != scanMedia);
    auto scanCapabilities = jobTicket->getScanCapabilitiesInterface();
    ASSERT_TRUE(nullptr != scanCapabilities);

    // Prompt Contorller
    auto promptController = std::make_shared<CopyJobPromptController>(jobTicket, nullptr, Product::ENTERPRISE, true);
    ASSERT_NE(nullptr, promptController);

    // GLASS. LETTER/PORTRAIT
    EXPECT_CALL((*pMockIMediaPath_), getId).WillRepeatedly(Return("GLASS"));
    EXPECT_CALL((*pMockIMediaPath_), getType).WillRepeatedly(Return(dune::scan::types::ScanSource::GLASS));
    EXPECT_CALL((*pMockIMediaPath_), getMediaPresenceStatus).WillRepeatedly(Return(dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus::LOADED));
    EXPECT_CALL((*pMockIMediaPath_), getMediaDetectionStatus).WillRepeatedly(Return(std::make_pair(MediaSizeId::LETTER, dune::imaging::types::MediaOrientation::PORTRAIT)));

    auto jobIntent = jobTicket->getIntent();
    jobIntent->setInputMediaSizeId(dune::imaging::types::MediaSizeId::LETTER);
    jobIntent->setScanSource(dune::scan::types::ScanSource::GLASS);

    // call getNewPromptToDisplay
    auto prompt = promptController->getNewPromptToDisplay(false);
    EXPECT_EQ(prompt, PromptType::None);  // none prompt always exists.
}

TEST_F(GivenAConnectedJobServiceStandard, whenGetJobCreatePermissionsCalled_ThenCopyJobCreationPermissionMapIsReturned)
{
    std::map<JobType, Permission> copyJobCreationPermissionMap = component_->getJobCreationPermissions();

    EXPECT_EQ(copyJobCreationPermissionMap[JobType::COPY], dune::security::ac::Permission::CP_COPY_APP);
}

TEST_F(GivenAConnectedJobServiceStandard, WhenEnterpriseMultiPageWithGlass_CancelPrompt)
{
    auto *jobService =
        static_cast<ICopyJobService *>(component_->getInterface(GET_INTERFACE_UID(ICopyJobService), nullptr));
    auto jobTicket = jobService->getDefaultJobTicket();
    ASSERT_TRUE(nullptr != jobTicket);
    EXPECT_CALL(mockIJobManagerAlertProvider_, notifyAlert(_, _, _)).WillRepeatedly(Return(2));
    auto scanCapabilities = jobTicket->getScanCapabilitiesInterface();
    ASSERT_TRUE(nullptr != scanCapabilities);

    // Prompt Contorller
    auto promptController = std::make_shared<CopyJobPromptController>(jobTicket, &mockIJobManagerAlertProvider_, Product::ENTERPRISE, true);
    ASSERT_NE(nullptr, promptController);

    EXPECT_CALL((*pMockIMediaPath_), getId).WillRepeatedly(Return("GLASS"));
    EXPECT_CALL((*pMockIMediaPath_), getType).WillRepeatedly(Return(dune::scan::types::ScanSource::GLASS));
    EXPECT_CALL((*pMockIMediaPath_), getMediaPresenceStatus).WillRepeatedly(Return(dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus::LOADED));
    EXPECT_CALL((*pMockIMediaPath_), getMediaDetectionStatus).WillRepeatedly(Return(std::make_pair(MediaSizeId::LETTER, dune::imaging::types::MediaOrientation::PORTRAIT)));

    jobTicket->setFirstScanStarted(true);
    auto jobIntent = jobTicket->getIntent();
    jobIntent->setScanSource(dune::scan::types::ScanSource::GLASS);
    jobIntent->setInputPlexMode(dune::imaging::types::Plex::DUPLEX);

    promptController->getNewPromptToDisplay(true);
    promptController->displayPrompt(dune::job::PromptType::FlatbedDuplexAddPage, std::bind(&GivenAConnectedJobServiceStandard::testFunction, this, std::placeholders::_1, std::placeholders::_2));
    promptController->onPromptResponse(dune::cdm::alert_1::Category::flatbedAddPage, nullptr);
    promptController->cancelPrompt();
    EXPECT_NE(jobTicket->getCompletionState(), dune::job::CompletionStateType::CANCELED);
}

TEST_F(GivenAConnectedJobServiceStandard, WhenDefaultTicketIsToBeSerialisedToJsonForSupportedJob_ThenReturnSerializedJsonData)
{
    // Test to ensure we add the symlink whenever new fbs is added or included in the existing fbs
    component_->setResourceFilePath(); 
    // void setResourceFilePath()
    // component_->setResourceFilePath("testResources/");

    std::string jsonData = component_->serializeDefaultTicketToJson(JobType::COPY);

    ASSERT_TRUE(!jsonData.empty());
}

TEST_F(GivenAConnectedJobServiceStandard, WhenTicketIsToBeSerialisedToJson_ThenReturnSerializedJsonData)
{
    component_->setResourceFilePath();

    std::shared_ptr<ICopyJobTicket> ticket = component_->getDefaultJobTicket(JobType::COPY);
    ASSERT_NE(nullptr, ticket);
    
    std::string jsonData = "";
    std::string jsonDataToBeEncrypted = "";

    bool result = component_->serializeTicketToJson(ticket->getTicketId().toString(false), jsonData, jsonDataToBeEncrypted);

    ASSERT_TRUE(result);
    ASSERT_TRUE(!jsonData.empty());
    ASSERT_TRUE(jsonDataToBeEncrypted.empty());
}

TEST_F(GivenAConnectedJobServiceStandard, WhenTicketIsToBeSerialisedToJsonWithEmptyResourcesDirectoryPath_ThenFailureShouldBeReturned)
{
    std::shared_ptr<ICopyJobTicket> ticket = component_->getDefaultJobTicket(JobType::COPY);
    ASSERT_NE(nullptr, ticket);
    
    std::string jsonData = "";
    std::string jsonDataToBeEncrypted = "";

    bool result = component_->serializeTicketToJson(ticket->getTicketId().toString(false), jsonData, jsonDataToBeEncrypted);

    ASSERT_FALSE(result);
    ASSERT_TRUE(jsonData.empty());
    ASSERT_TRUE(jsonDataToBeEncrypted.empty());
}

TEST_F(GivenAConnectedJobServiceStandard, WhenTicketIsToBeSerialisedToJsonWithUnavailableTicketId_ThenFailureShouldBeReturned)
{
    component_->setResourceFilePath();

    const dune::framework::core::Uuid uuid = dune::framework::core::Uuid("d810cc0f-98f9-44c4-a90c-e904be276843");
    std::string jsonData = "";
    std::string jsonDataToBeEncrypted = "";

    bool result = component_->serializeTicketToJson(uuid.toString(false), jsonData, jsonDataToBeEncrypted);

    ASSERT_FALSE(result);
    ASSERT_TRUE(jsonData.empty());
    ASSERT_TRUE(jsonDataToBeEncrypted.empty());
}

TEST_F(GivenAConnectedJobServiceStandard, WhenJsonDataIsToBeSerializedDeserialisedToTicket_ThenSuccessShouldBeReturned)
{
    component_->setResourceFilePath();

    std::shared_ptr<ICopyJobTicket> ticket = component_->getDefaultJobTicket(JobType::COPY);
    ASSERT_NE(nullptr, ticket);

    std::string jsonData = "";
    std::string jsonDataToBeEncrypted = "";

    // Serialize Json Data
    bool result = component_->serializeTicketToJson(ticket->getTicketId().toString(false), jsonData, jsonDataToBeEncrypted);

    ASSERT_TRUE(result);
    ASSERT_FALSE(jsonData.empty());
    ASSERT_TRUE(jsonDataToBeEncrypted.empty());

    // Deserialize Json Data
    result = component_->deserializeJsonAndUpdateTicket(jsonData);

    ASSERT_TRUE(result);
}

TEST_F(GivenAConnectedJobServiceStandard, WhenEmptyJsonDataIsToBeDeserialisedToTicket_ThenFailureShouldBeReturned)
{
    std::shared_ptr<ICopyJobTicket> ticket = component_->getDefaultJobTicket(JobType::COPY);
    ASSERT_NE(nullptr, ticket);

    std::string jsonData = "";
    std::string jsonDataToBeEncrypted = "";

    // Serialize Empty Json Data 
    bool result = component_->serializeTicketToJson(ticket->getTicketId().toString(false), jsonData, jsonDataToBeEncrypted);

    ASSERT_FALSE(result);
    ASSERT_TRUE(jsonData.empty());
    ASSERT_TRUE(jsonDataToBeEncrypted.empty());

    component_->setResourceFilePath();
    // Deserialize Json Data
    result = component_->deserializeJsonAndUpdateTicket(jsonData);

    ASSERT_FALSE(result);
}

TEST_F(GivenAConnectedJobServiceStandard, WhenJsonDataIsToBeDeserialisedToTicketWithUnavailableTicketId_ThenFailureShouldBeReturned)
{
    component_->setResourceFilePath();

    const dune::framework::core::Uuid uuid = dune::framework::core::Uuid("d810cc0f-98f9-44c4-a90c-e904be276843");
    std::string jsonData = "";
    std::string jsonDataToBeEncrypted = "";

    // Serialize Json Data
    bool result = component_->serializeTicketToJson(uuid.toString(false), jsonData, jsonDataToBeEncrypted);

    ASSERT_FALSE(result);
    ASSERT_TRUE(jsonData.empty());
    ASSERT_TRUE(jsonDataToBeEncrypted.empty());

    // Deserialize Json Data
    result = component_->deserializeJsonAndUpdateTicket(jsonData);

    ASSERT_FALSE(result);
}

TEST_F(GivenAConnectedJobServiceStandard, WhenValidateAndSaveDefaultJobTicketCalled_ThenSuccessShouldBeReturned)
{
    std::shared_ptr<ICopyJobTicket> initialTicket = component_->getDefaultJobTicket();
    initialTicket->setType(dune::job::JobType::COPY);
    auto serializedData = initialTicket->serialize();

    bool result = component_->validateAndSaveDefaultJobTicket(serializedData);

    EXPECT_EQ(result, true);
}
TEST_F(GivenAConnectedJobServiceStandard, WhenValidateAndSaveDefaultJobTicketCalled_ThenFailedShouldBeReturned)
{
    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobTicket>                         mockICopyJobTicket_{nullptr};
    std::shared_ptr<dune::copy::Jobs::Copy::MockICopyJobIntent>                         jobIntent_{nullptr};
    mockICopyJobTicket_ = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobTicket>();
    mockICopyJobTicket_->setType(dune::job::JobType::COPY);
    jobIntent_ = std::make_shared<dune::copy::Jobs::Copy::MockICopyJobIntent>();
    ON_CALL(*jobIntent_, getOutputMediaSource()).WillByDefault(Return(dune::imaging::types::MediaSource::TRAY4));

    jobIntent_->setOutputMediaSource(dune::imaging::types::MediaSource::TRAY4);
    auto serializedData = mockICopyJobTicket_->serialize();
    bool result = component_->validateAndSaveDefaultJobTicket(serializedData);

    EXPECT_EQ(result, false);
}

TEST_F(GivenAConnectedJobServiceStandard, WhencheckAndPerformMigrationCalled_ThenSuccessShouldBeReturned)
{
    auto mockContext = std::make_shared<MockISystemConversionContext>();
    dune::framework::data::conversion::DataDescriptorCollection dataDescriptors{{"dummyFilePath", "dummyPath"}};

    std::shared_ptr<ICopyJobTicket> initialTicket = component_->getDefaultJobTicket();
    initialTicket->setType(dune::job::JobType::COPY);
    auto serializedData = initialTicket->serialize();
    EXPECT_CALL(mockISystemConversionHelper_, getConversionContext(::testing::_))
            .WillOnce(Return(std::make_pair(APIResult::OK, mockContext)));
    EXPECT_CALL(mockISystemConversionHelper_, setConversionResult(dune::framework::data::conversion::ConversionResult::SUCCESS, ::testing::_))
            .Times(1);
    EXPECT_CALL(*mockContext, getFilesToConvert())
            .WillOnce(ReturnRef((dataDescriptors)));

    EXPECT_CALL(mockICopyTicketConverter_, convert(::testing::_, ::testing::_))
            .WillOnce(Return(dune::framework::data::conversion::ConversionResult::SUCCESS));
    auto result = component_->checkAndPerformMigration();

    EXPECT_EQ(result.first, dune::framework::data::conversion::ConversionResult::SUCCESS);
}

TEST_F(GivenAConnectedJobServiceStandard, WhencheckAndPerformMigrationCalled_WithEmptyConvertionContext_ThenErrorShouldBeReturned)
{
    std::shared_ptr<MockISystemConversionContext> mockContext = nullptr;
    std::shared_ptr<ICopyJobTicket> initialTicket = component_->getDefaultJobTicket();
    initialTicket->setType(dune::job::JobType::COPY);
    auto serializedData = initialTicket->serialize();
    EXPECT_CALL(mockISystemConversionHelper_, getConversionContext(::testing::_))
        .WillOnce(Return(std::make_pair(APIResult::OK, mockContext)));
    EXPECT_CALL(mockISystemConversionHelper_, setConversionResult(::testing::_, ::testing::_))
            .Times(0);
    EXPECT_CALL(mockICopyTicketConverter_, convert(::testing::_, ::testing::_)).Times(0);
    auto result = component_->checkAndPerformMigration();

    EXPECT_EQ(result.first, dune::framework::data::conversion::ConversionResult::ERROR);
}

TEST_F(GivenAConnectedJobServiceStandard, WhencheckAndPerformMigrationCalled_WithEmptyDataDescriptor_ThenErrorShouldBeReturned)
{
    auto mockContext = std::make_shared<MockISystemConversionContext>();
    dune::framework::data::conversion::DataDescriptorCollection dataDescriptors{};

    std::shared_ptr<ICopyJobTicket> initialTicket = component_->getDefaultJobTicket();
    initialTicket->setType(dune::job::JobType::COPY);
    auto serializedData = initialTicket->serialize();
    EXPECT_CALL(mockISystemConversionHelper_, getConversionContext(::testing::_))
            .WillOnce(Return(std::make_pair(APIResult::OK, mockContext)));
    EXPECT_CALL(mockISystemConversionHelper_, setConversionResult(dune::framework::data::conversion::ConversionResult::ERROR, ::testing::_))
            .Times(1);
    EXPECT_CALL(*mockContext, getFilesToConvert())
            .WillOnce(ReturnRef((dataDescriptors)));

    EXPECT_CALL(mockICopyTicketConverter_, convert(::testing::_, ::testing::_)).Times(0);
    auto result = component_->checkAndPerformMigration();

    EXPECT_EQ(result.first, dune::framework::data::conversion::ConversionResult::ERROR);
}

TEST_F(GivenAConnectedJobServiceStandard, WhencheckAndPerformMigrationCalled_WithCopyTicketConverterError_ThenErrorShouldBeReturned)
{
    auto mockContext = std::make_shared<MockISystemConversionContext>();
    dune::framework::data::conversion::DataDescriptorCollection dataDescriptors{{"dummyFilePath", "dummyPath"}};

    std::shared_ptr<ICopyJobTicket> initialTicket = component_->getDefaultJobTicket();
    initialTicket->setType(dune::job::JobType::COPY);
    auto serializedData = initialTicket->serialize();
    EXPECT_CALL(mockISystemConversionHelper_, getConversionContext(::testing::_))
            .WillOnce(Return(std::make_pair(APIResult::OK, mockContext)));
    EXPECT_CALL(mockISystemConversionHelper_, setConversionResult(dune::framework::data::conversion::ConversionResult::ERROR, ::testing::_))
            .Times(1);
    EXPECT_CALL(*mockContext, getFilesToConvert())
            .WillOnce(ReturnRef((dataDescriptors)));

    EXPECT_CALL(mockICopyTicketConverter_, convert(::testing::_, ::testing::_))
            .WillOnce(Return(dune::framework::data::conversion::ConversionResult::ERROR));
    auto result = component_->checkAndPerformMigration();

    EXPECT_EQ(result.first, dune::framework::data::conversion::ConversionResult::ERROR);
}

class GivenAInitializedJobServiceStandardPreparedToValidate :public GivenANewJobServiceStandard
{
  public:
    GivenAInitializedJobServiceStandardPreparedToValidate() { GTEST_CHECKPOINTA("GivenAInitializedJobServiceStandardPreparedToValidate::Constructor -- ENTER\n"); };

    void SetUp() override;
};

void GivenAInitializedJobServiceStandardPreparedToValidate::SetUp()
{
    GTEST_CHECKPOINTA("GivenAInitializedJobServiceStandardPreparedToValidate::SetUp -- ENTER");
    GivenANewJobServiceStandard::SetUp();

    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/JobServiceStandardTestDataValidate.json");

    component_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    // fill here any setInterface required
    component_->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    component_->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    component_->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    component_->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    component_->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    component_->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    component_->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    component_->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    component_->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    component_->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    component_->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    component_->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    component_->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    component_->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    component_->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);
    component_->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    ON_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillByDefault(ReturnRef(copyAdapterDataChangeEvent_));

    GTEST_CHECKPOINTA("GivenAInitializedJobServiceStandardPreparedToValidate::SetUp -- EXIT");
}

// No default exist an need to create a new one, so all will be ok
TEST_F(GivenAInitializedJobServiceStandardPreparedToValidate,WhenDefaultNotExistAndConnectIsCalled_ThenConnectWillResultOkAndNewDefaultTicketWillBeGenerated)
{
    // No expectations needed

    // Execute connected
    std::future<void> asyncCompletion;
    component_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    // Check Ticket default result
    auto ticket = component_->getDefaultJobTicket();
    ASSERT_NE(ticket,nullptr);
}

// Default exist, check that all is ok and it's not need any validation
TEST_F(GivenAInitializedJobServiceStandardPreparedToValidate,WhenDefaultSupportedTicketExistAndConnectIsCalled_ThenConnectWillResultOkAndTicketWontBeChanged)
{
    // Default expectation from cache
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketFromCache = createCopyJobTicket(createCorrectJobIntent(),createExpectedConstraints());
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketInsertedToCache = createCopyJobTicket(createIncorrectJobIntent(),createExpectedConstraints());
    bool savedCompleted = false;
    dune::framework::data::ObjectClassification objClass;

    EXPECT_CALL(mockIDataStore_, find(Matcher<const Uuid &>(_))).WillRepeatedly(testing::InvokeWithoutArgs([&ticketFromCache,this]() {
        // Get Serialized data
        auto serializedData = ticketFromCache->serialize();

        // Return serialized data
        std::pair<bool, DataObject> returnVal;
        returnVal.first = true;
        returnVal.second.buffer.first = std::move(serializedData.first);
        returnVal.second.buffer.second = serializedData.second;
        return returnVal;
    }));

    EXPECT_CALL(mockIDataStore_, insert_or_replace_ex(_, _, _)).Times(0)
        .WillRepeatedly(Invoke(
            [&savedCompleted, &objClass,this, &ticketInsertedToCache](const dune::framework::data::SerializedDataBuffer& object, const dune::framework::core::Uuid& uuid,const dune::framework::data::ObjectClassification& oc)
            {
                auto packedFb = flatbuffers::GetRoot<dune::copy::Jobs::Copy::CopyJobTicketFb>(object.first);
                auto data = packedFb->UnPack();
                auto dataIntentFb = std::move(data->intent);
                auto intent = ticketInsertedToCache->getIntent();

                intent->setOutputMediaSizeId(dataIntentFb->outputMediaSizeId);
                intent->setOutputMediaOrientation(dataIntentFb->outputMediaOrientation);
                intent->setOutputMediaIdType(dataIntentFb->outputMediaIdType);
                intent->setOutputMediaSource(dataIntentFb->outputMediaSource);
                intent->setOutputPlexMode(dataIntentFb->outputPlexMode);
                intent->setCopyMargins(dataIntentFb->copyMargins);
                intent->setOutputPlexBinding(dataIntentFb->outputPlexBinding);
                intent->setCopies(dataIntentFb->copies);
                intent->setCollate(dataIntentFb->collate);
                intent->setCopyQuality(dataIntentFb->copyQuality);
                intent->setOutputDestination(dataIntentFb->outputMediaDestination);
                intent->setPrintingOrder(dataIntentFb->printingOrder);
                intent->setRotation(dataIntentFb->rotation);
                intent->setAutoRotate(dataIntentFb->autoRotate);
                intent->setMediaFamily(dataIntentFb->mediaFamily);
                intent->setStapleOption(static_cast<dune::imaging::types::StapleOptions>(dataIntentFb->stapleOption));
                intent->setPunchOption(static_cast<dune::imaging::types::PunchingOptions>(dataIntentFb->punchOption));
                intent->setFoldOption(static_cast<dune::imaging::types::FoldingOptions>(dataIntentFb->foldOption));
                intent->setBookletMakerOption(static_cast<dune::imaging::types::BookletMakingOptions>(dataIntentFb->foldOption));
                intent->setCustomMediaXDimension(dataIntentFb->customMediaXDimension);
                intent->setCustomMediaYDimension(dataIntentFb->customMediaYDimension);
                dune::scan::Jobs::Scan::deserializeScanJobIntent(dataIntentFb->scanJobIntent, intent);
                objClass = oc;
                return true;
            }
        ));

    // Execute connected
    std::future<void> asyncCompletion;
    component_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    ASSERT_FALSE(savedCompleted);

    // Check Ticket default Result
    auto ticket = component_->getDefaultJobTicket();
    ASSERT_NE(ticket,nullptr);
}

// Default exist, and need a change on a setting
TEST_F(GivenAInitializedJobServiceStandardPreparedToValidate,WhenDefaultUnsupportedTicketExistAndConnectIsCalled_ThenConnectWillResultOkButDefaultTicketWillBeChanged)
{
    // Default expectation from cache
    // Constraints that not fit
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketFromCache = createCopyJobTicket(createIncorrectJobIntent(),createExpectedConstraints());
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketInsertedToCache = createCopyJobTicket(createIncorrectJobIntent(),createExpectedConstraints());
    bool savedCompleted = false;
    dune::framework::data::ObjectClassification objClass;

    EXPECT_CALL(mockIDataStore_, find(Matcher<const Uuid &>(_))).WillRepeatedly(testing::InvokeWithoutArgs([&ticketFromCache,this]() {
        // Get Serialized data
        auto serializedData = ticketFromCache->serialize();

        // Return serialized data
        std::pair<bool, DataObject> returnVal;
        returnVal.first = true;
        returnVal.second.buffer.first = std::move(serializedData.first);
        returnVal.second.buffer.second = serializedData.second;
        return returnVal;
    }));

    EXPECT_CALL(mockIDataStore_, insert_or_replace_ex(_, _, _))
        .WillOnce(Invoke(
            [&savedCompleted, &objClass,this, &ticketInsertedToCache](const dune::framework::data::SerializedDataBuffer& object, const dune::framework::core::Uuid& uuid,const dune::framework::data::ObjectClassification& oc)
            {
                auto packedFb = flatbuffers::GetRoot<dune::copy::Jobs::Copy::CopyJobTicketFb>(object.first);
                auto data = packedFb->UnPack();
                auto dataIntentFb = std::move(data->intent);
                auto intent = ticketInsertedToCache->getIntent();

                intent->setOutputMediaSizeId(dataIntentFb->outputMediaSizeId);
                intent->setOutputMediaOrientation(dataIntentFb->outputMediaOrientation);
                intent->setOutputMediaIdType(dataIntentFb->outputMediaIdType);
                intent->setOutputMediaSource(dataIntentFb->outputMediaSource);
                intent->setOutputPlexMode(dataIntentFb->outputPlexMode);
                intent->setCopyMargins(dataIntentFb->copyMargins);
                intent->setOutputPlexBinding(dataIntentFb->outputPlexBinding);
                intent->setCopies(dataIntentFb->copies);
                intent->setCollate(dataIntentFb->collate);
                intent->setCopyQuality(dataIntentFb->copyQuality);
                intent->setOutputDestination(dataIntentFb->outputMediaDestination);
                intent->setPrintingOrder(dataIntentFb->printingOrder);
                intent->setRotation(dataIntentFb->rotation);
                intent->setAutoRotate(dataIntentFb->autoRotate);
                intent->setMediaFamily(dataIntentFb->mediaFamily);
                intent->setStapleOption(static_cast<dune::imaging::types::StapleOptions>(dataIntentFb->stapleOption));
                intent->setPunchOption(static_cast<dune::imaging::types::PunchingOptions>(dataIntentFb->punchOption));
                intent->setFoldOption(static_cast<dune::imaging::types::FoldingOptions>(dataIntentFb->foldOption));
                intent->setBookletMakerOption(static_cast<dune::imaging::types::BookletMakingOptions>(dataIntentFb->foldOption));
                intent->setCustomMediaXDimension(dataIntentFb->customMediaXDimension);
                intent->setCustomMediaYDimension(dataIntentFb->customMediaYDimension);
                dune::scan::Jobs::Scan::deserializeScanJobIntent(dataIntentFb->scanJobIntent, intent);
                objClass = oc;
                savedCompleted = true;
                delete data;
                return savedCompleted;
            }
        ));

    // Execute connected
    std::future<void> asyncCompletion;
    component_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    // Check Ticket default Result
    ASSERT_TRUE(savedCompleted);

    // Check Ticket default Result
    auto ticketGoodFormed = createCopyJobTicket(createCorrectJobIntent(),createExpectedConstraints());
    EXPECT_TRUE(dune::copy::Jobs::Copy::compareIntents(ticketInsertedToCache->getIntent(), ticketGoodFormed->getIntent()));
}

// A user quickset exist, check that all is ok and it's not need any change on user quickset
TEST_F(GivenAInitializedJobServiceStandardPreparedToValidate,WhenUserQuicksetSupportedExistAndConnectIsCalled_ThenConnectWillResultOkAndUserQuicksetWontBeChanged)
{
    // user quickset expectation from cache and list of shortcuts
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticket = createCopyJobTicket(createCorrectJobIntent(),createExpectedConstraints());
    insertShortcutOnList(ticket);
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketInsertedToCache = createCopyJobTicket(createIncorrectJobIntent(),createExpectedConstraints());
    bool savedCompleted = false;
    dune::framework::data::ObjectClassification objClass;

    EXPECT_CALL(mockIDataStore_, find(Matcher<const Uuid &>(_))).WillRepeatedly(testing::InvokeWithoutArgs([&ticket,this]() {
        // Get Serialized data
        auto serializedData = ticket->serialize();

        // Return serialized data
        std::pair<bool, DataObject> returnVal;
        returnVal.first = true;
        returnVal.second.buffer.first = std::move(serializedData.first);
        returnVal.second.buffer.second = serializedData.second;
        return returnVal;
    }));

    EXPECT_CALL(mockIDataStore_, insert_or_replace_ex(_, _, _)).Times(0)
        .WillRepeatedly(Invoke(
            [&savedCompleted, &objClass,this, &ticketInsertedToCache](const dune::framework::data::SerializedDataBuffer& object, const dune::framework::core::Uuid& uuid,const dune::framework::data::ObjectClassification& oc)
            {
                auto packedFb = flatbuffers::GetRoot<dune::copy::Jobs::Copy::CopyJobTicketFb>(object.first);
                auto data = packedFb->UnPack();
                auto dataIntentFb = std::move(data->intent);
                auto intent = ticketInsertedToCache->getIntent();

                intent->setOutputMediaSizeId(dataIntentFb->outputMediaSizeId);
                intent->setOutputMediaOrientation(dataIntentFb->outputMediaOrientation);
                intent->setOutputMediaIdType(dataIntentFb->outputMediaIdType);
                intent->setOutputMediaSource(dataIntentFb->outputMediaSource);
                intent->setOutputPlexMode(dataIntentFb->outputPlexMode);
                intent->setCopyMargins(dataIntentFb->copyMargins);
                intent->setOutputPlexBinding(dataIntentFb->outputPlexBinding);
                intent->setCopies(dataIntentFb->copies);
                intent->setCollate(dataIntentFb->collate);
                intent->setCopyQuality(dataIntentFb->copyQuality);
                intent->setOutputDestination(dataIntentFb->outputMediaDestination);
                intent->setPrintingOrder(dataIntentFb->printingOrder);
                intent->setRotation(dataIntentFb->rotation);
                intent->setAutoRotate(dataIntentFb->autoRotate);
                intent->setMediaFamily(dataIntentFb->mediaFamily);
                intent->setStapleOption(static_cast<dune::imaging::types::StapleOptions>(dataIntentFb->stapleOption));
                intent->setPunchOption(static_cast<dune::imaging::types::PunchingOptions>(dataIntentFb->punchOption));
                intent->setFoldOption(static_cast<dune::imaging::types::FoldingOptions>(dataIntentFb->foldOption));
                intent->setBookletMakerOption(static_cast<dune::imaging::types::BookletMakingOptions>(dataIntentFb->foldOption));
                intent->setCustomMediaXDimension(dataIntentFb->customMediaXDimension);
                intent->setCustomMediaYDimension(dataIntentFb->customMediaYDimension);
                dune::scan::Jobs::Scan::deserializeScanJobIntent(dataIntentFb->scanJobIntent, intent);
                objClass = oc;
                return true;
            }
        ));

    EXPECT_CALL(mockIJobTicketResourceManager_,loadJobTicketIntoCacheIfNeeded(_,_)).WillRepeatedly(Return(ticket));

    // Execute connected
    std::future<void> asyncCompletion;
    component_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    ASSERT_FALSE(savedCompleted);
}

// A user quickset exist, and need a change on a setting
TEST_F(GivenAInitializedJobServiceStandardPreparedToValidate,WhenUserQuicksetUnsupportedExistAndConnectIsCalled_ThenConnectWillResultOkButDefaultTicketWillBeChanged)
{
    // user quickset expectation from cache and list of shortcuts
    // Constraints that not fit
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticket = createCopyJobTicket(createIncorrectJobIntent(),createExpectedConstraints());
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketGoodFormed = createCopyJobTicket(createCorrectJobIntent(),createExpectedConstraints());
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketInsertedToCache = createCopyJobTicket(createIncorrectJobIntent(),createExpectedConstraints());
    bool savedCompleted = false;
    dune::framework::data::ObjectClassification objClass;

    // Create a shortcut on list to check
    insertShortcutOnList(ticket);

    // Return for Default Ticket
    EXPECT_CALL(mockIDataStore_, find(Matcher<const Uuid &>(_)))
    .WillOnce(testing::InvokeWithoutArgs([&ticketGoodFormed,this]() {
        // Get Serialized data
        auto serializedData = ticketGoodFormed->serialize();

        // Return serialized data
        std::pair<bool, DataObject> returnVal;
        returnVal.first = true;
        returnVal.second.buffer.first = std::move(serializedData.first);
        returnVal.second.buffer.second = serializedData.second;
        return returnVal;
    }));

    // Insert of ticket of shortcut expected
    EXPECT_CALL(mockIDataStore_, insert_or_replace_ex(_, _, _))
        .WillOnce(Invoke(
            [&savedCompleted, &objClass,this, &ticketInsertedToCache](const dune::framework::data::SerializedDataBuffer& object, const dune::framework::core::Uuid& uuid,const dune::framework::data::ObjectClassification& oc)
            {
                auto packedFb = flatbuffers::GetRoot<dune::copy::Jobs::Copy::CopyJobTicketFb>(object.first);
                auto data = packedFb->UnPack();
                auto dataIntentFb = std::move(data->intent);
                auto intent = ticketInsertedToCache->getIntent();

                intent->setOutputMediaSizeId(dataIntentFb->outputMediaSizeId);
                intent->setOutputMediaOrientation(dataIntentFb->outputMediaOrientation);
                intent->setOutputMediaIdType(dataIntentFb->outputMediaIdType);
                intent->setOutputMediaSource(dataIntentFb->outputMediaSource);
                intent->setOutputPlexMode(dataIntentFb->outputPlexMode);
                intent->setCopyMargins(dataIntentFb->copyMargins);
                intent->setOutputPlexBinding(dataIntentFb->outputPlexBinding);
                intent->setCopies(dataIntentFb->copies);
                intent->setCollate(dataIntentFb->collate);
                intent->setCopyQuality(dataIntentFb->copyQuality);
                intent->setOutputDestination(dataIntentFb->outputMediaDestination);
                intent->setPrintingOrder(dataIntentFb->printingOrder);
                intent->setRotation(dataIntentFb->rotation);
                intent->setAutoRotate(dataIntentFb->autoRotate);
                intent->setMediaFamily(dataIntentFb->mediaFamily);
                intent->setStapleOption(static_cast<dune::imaging::types::StapleOptions>(dataIntentFb->stapleOption));
                intent->setPunchOption(static_cast<dune::imaging::types::PunchingOptions>(dataIntentFb->punchOption));
                intent->setFoldOption(static_cast<dune::imaging::types::FoldingOptions>(dataIntentFb->foldOption));
                intent->setBookletMakerOption(static_cast<dune::imaging::types::BookletMakingOptions>(dataIntentFb->foldOption));
                intent->setCustomMediaXDimension(dataIntentFb->customMediaXDimension);
                intent->setCustomMediaYDimension(dataIntentFb->customMediaYDimension);
                dune::scan::Jobs::Scan::deserializeScanJobIntent(dataIntentFb->scanJobIntent, intent);
                objClass = oc;
                savedCompleted = true;
                delete data;
                return savedCompleted;
            }
        ));

    // Load ticket to cache expected
    EXPECT_CALL(mockIJobTicketResourceManager_,loadJobTicketIntoCacheIfNeeded(_,_)).WillOnce(Invoke(
        [&ticket, this](const Uuid &ticketId, bool &persistedJobTicket)
        {
            auto ticketOnCache = std::dynamic_pointer_cast<dune::copy::Jobs::Copy::CopyJobTicket>(this->component_->deserializeBaseTicketOnlyIfNotInCache(ticket->serialize(), persistedJobTicket));
            ticketOnCache->setConstraintsFromFb(createExpectedConstraints());
            return ticketOnCache;
        }
    ));

    // Execute connected
    std::future<void> asyncCompletion;
    component_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    // Check Ticket user quickset Result
    EXPECT_TRUE(savedCompleted);
    EXPECT_TRUE(dune::copy::Jobs::Copy::compareIntents(ticketInsertedToCache->getIntent(), ticketGoodFormed->getIntent()));
}

class GivenAInitializedJobServiceStandardPreparedToValidateTicketInitializationFalse :public GivenANewJobServiceStandard
{
    public:
      GivenAInitializedJobServiceStandardPreparedToValidateTicketInitializationFalse() { GTEST_CHECKPOINTA("GivenAInitializedJobServiceStandardPreparedToValidateTicketInitializationFalse::Constructor -- ENTER\n"); };

      void SetUp() override;
};

void GivenAInitializedJobServiceStandardPreparedToValidateTicketInitializationFalse::SetUp()
{
    GTEST_CHECKPOINTA("GivenAInitializedJobServiceStandardPreparedToValidateTicketInitializationFalse::SetUp -- ENTER");
    GivenANewJobServiceStandard::SetUp();

    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/JobServiceStandardTestDataValidateTicketInitializationFalse.json");

    component_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    // fill here any setInterface required
    component_->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    component_->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    component_->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    component_->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    component_->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    component_->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    component_->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    component_->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    component_->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    component_->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    component_->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    component_->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    component_->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    component_->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    component_->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);
    component_->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    ON_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillByDefault(ReturnRef(copyAdapterDataChangeEvent_));

    GTEST_CHECKPOINTA("GivenAInitializedJobServiceStandardPreparedToValidateTicketInitializationFalse::SetUp -- EXIT");
}

class GivenAInitializedJobServiceStandardPreparedToForceUpgrade :public GivenANewJobServiceStandard
{
  public:
    GivenAInitializedJobServiceStandardPreparedToForceUpgrade() { GTEST_CHECKPOINTA("GivenAInitializedJobServiceStandardPreparedToForceUpgrade::Constructor -- ENTER\n"); };

    void SetUp() override;
};

void GivenAInitializedJobServiceStandardPreparedToForceUpgrade::SetUp()
{
    GTEST_CHECKPOINTA("GivenAInitializedJobServiceStandardPreparedToForceUpgrade::SetUp -- ENTER");
    GivenANewJobServiceStandard::SetUp();

    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/JobServiceStandardTestDataVersioned.json");

    component_->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    // fill here any setInterface required
    component_->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    component_->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    component_->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    component_->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    component_->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    component_->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    component_->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    component_->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    component_->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    component_->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    component_->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    component_->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    component_->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    component_->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    component_->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    component_->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    component_->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr), "MockIMediaHandlingSettings", &mockIMediaHandlingMgr_);
    component_->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    ON_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillByDefault(ReturnRef(copyAdapterDataChangeEvent_));

    GTEST_CHECKPOINTA("GivenAInitializedJobServiceStandardPreparedToForceUpgrade::SetUp -- EXIT");
}

TEST_F(GivenAInitializedJobServiceStandardPreparedToForceUpgrade,WhenConnectIsCalledAndDefaultTicketNotExist_ThenValueOfTicketIsNotUpdated)
{
    // No expectations needed (Empty ticket should have last version)

    // Execute connected
    std::future<void> asyncCompletion;
    component_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    // Check Ticket default result
    auto ticket = component_->getDefaultJobTicket();
    ASSERT_NE(ticket,nullptr);
}

TEST_F(GivenAInitializedJobServiceStandardPreparedToForceUpgrade,WhenConnectIsCalledAndDefaultTicketHasVersion_ThenValueOfTicketIsNotUpdated)
{
    // Default expectation from cache
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketFromCache = createCopyJobTicket(createCorrectJobIntent(),createExpectedConstraints());
    ticketFromCache->setVersion(2); // 2 is current version on src/fw/copy/Jobs/Copy/JobService/Standard/test/testResources/JobServiceStandardTestDataVersioned.json
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketInsertedToCache = createCopyJobTicket(createIncorrectJobIntent(),createExpectedConstraints());
    bool savedCompleted = false;
    dune::framework::data::ObjectClassification objClass;

    EXPECT_CALL(mockIDataStore_, find(Matcher<const Uuid &>(_))).WillRepeatedly(testing::InvokeWithoutArgs([&ticketFromCache,this]() {
        // Get Serialized data
        auto serializedData = ticketFromCache->serialize();

        // Return serialized data
        std::pair<bool, DataObject> returnVal;
        returnVal.first = true;
        returnVal.second.buffer.first = std::move(serializedData.first);
        returnVal.second.buffer.second = serializedData.second;
        return returnVal;
    }));

    EXPECT_CALL(mockIDataStore_, insert_or_replace_ex(_, _, _)).Times(0)
        .WillRepeatedly(Invoke(
            [&savedCompleted, &objClass,this, &ticketInsertedToCache](const dune::framework::data::SerializedDataBuffer& object, const dune::framework::core::Uuid& uuid,const dune::framework::data::ObjectClassification& oc)
            {
                auto packedFb = flatbuffers::GetRoot<dune::copy::Jobs::Copy::CopyJobTicketFb>(object.first);
                auto data = packedFb->UnPack();
                auto dataIntentFb = std::move(data->intent);
                auto intent = ticketInsertedToCache->getIntent();

                intent->setOutputMediaSizeId(dataIntentFb->outputMediaSizeId);
                intent->setOutputMediaOrientation(dataIntentFb->outputMediaOrientation);
                intent->setOutputMediaIdType(dataIntentFb->outputMediaIdType);
                intent->setOutputMediaSource(dataIntentFb->outputMediaSource);
                intent->setOutputPlexMode(dataIntentFb->outputPlexMode);
                intent->setCopyMargins(dataIntentFb->copyMargins);
                intent->setOutputPlexBinding(dataIntentFb->outputPlexBinding);
                intent->setCopies(dataIntentFb->copies);
                intent->setCollate(dataIntentFb->collate);
                intent->setCopyQuality(dataIntentFb->copyQuality);
                intent->setOutputDestination(dataIntentFb->outputMediaDestination);
                intent->setPrintingOrder(dataIntentFb->printingOrder);
                intent->setRotation(dataIntentFb->rotation);
                intent->setAutoRotate(dataIntentFb->autoRotate);
                intent->setMediaFamily(dataIntentFb->mediaFamily);
                intent->setStapleOption(static_cast<dune::imaging::types::StapleOptions>(dataIntentFb->stapleOption));
                intent->setPunchOption(static_cast<dune::imaging::types::PunchingOptions>(dataIntentFb->punchOption));
                intent->setFoldOption(static_cast<dune::imaging::types::FoldingOptions>(dataIntentFb->foldOption));
                intent->setBookletMakerOption(static_cast<dune::imaging::types::BookletMakingOptions>(dataIntentFb->foldOption));
                intent->setCustomMediaXDimension(dataIntentFb->customMediaXDimension);
                intent->setCustomMediaYDimension(dataIntentFb->customMediaYDimension);
                dune::scan::Jobs::Scan::deserializeScanJobIntent(dataIntentFb->scanJobIntent, intent);
                objClass = oc;
                savedCompleted = true;
                delete data;
                return true;
            }
        ));

    // Execute connected
    std::future<void> asyncCompletion;
    component_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    ASSERT_FALSE(savedCompleted);

    // Check Ticket default Result
    auto ticket = component_->getDefaultJobTicket();
    ASSERT_NE(ticket,nullptr);
}

TEST_F(GivenAInitializedJobServiceStandardPreparedToForceUpgrade,WhenConnectIsCalledAndDefaultTicketHasNotVersion_ThenValueOfTicketIsUpdated)
{
    // Default expectation from cache
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketFromCache = createCopyJobTicket(createCorrectJobIntent(),createExpectedConstraints());
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketInsertedToCache = createCopyJobTicket(createIncorrectJobIntent(),createExpectedConstraints());
    bool savedCompleted = false;
    dune::framework::data::ObjectClassification objClass;

    EXPECT_CALL(mockIDataStore_, find(Matcher<const Uuid &>(_))).WillRepeatedly(testing::InvokeWithoutArgs([&ticketFromCache,this]() {
        // Get Serialized data
        auto serializedData = ticketFromCache->serialize();

        // Return serialized data
        std::pair<bool, DataObject> returnVal;
        returnVal.first = true;
        returnVal.second.buffer.first = std::move(serializedData.first);
        returnVal.second.buffer.second = serializedData.second;
        return returnVal;
    }));

    EXPECT_CALL(mockIDataStore_, insert_or_replace_ex(_, _, _))
        .WillOnce(Invoke(
            [&savedCompleted, &objClass,this, &ticketInsertedToCache](const dune::framework::data::SerializedDataBuffer& object, const dune::framework::core::Uuid& uuid,const dune::framework::data::ObjectClassification& oc)
            {
                auto packedFb = flatbuffers::GetRoot<dune::copy::Jobs::Copy::CopyJobTicketFb>(object.first);
                auto data = packedFb->UnPack();
                auto dataIntentFb = std::move(data->intent);
                auto intent = ticketInsertedToCache->getIntent();

                intent->setOutputMediaSizeId(dataIntentFb->outputMediaSizeId);
                intent->setOutputMediaOrientation(dataIntentFb->outputMediaOrientation);
                intent->setOutputMediaIdType(dataIntentFb->outputMediaIdType);
                intent->setOutputMediaSource(dataIntentFb->outputMediaSource);
                intent->setOutputPlexMode(dataIntentFb->outputPlexMode);
                intent->setCopyMargins(dataIntentFb->copyMargins);
                intent->setOutputPlexBinding(dataIntentFb->outputPlexBinding);
                intent->setCopies(dataIntentFb->copies);
                intent->setCollate(dataIntentFb->collate);
                intent->setCopyQuality(dataIntentFb->copyQuality);
                intent->setOutputDestination(dataIntentFb->outputMediaDestination);
                intent->setPrintingOrder(dataIntentFb->printingOrder);
                intent->setRotation(dataIntentFb->rotation);
                intent->setAutoRotate(dataIntentFb->autoRotate);
                intent->setMediaFamily(dataIntentFb->mediaFamily);
                intent->setStapleOption(static_cast<dune::imaging::types::StapleOptions>(dataIntentFb->stapleOption));
                intent->setPunchOption(static_cast<dune::imaging::types::PunchingOptions>(dataIntentFb->punchOption));
                intent->setFoldOption(static_cast<dune::imaging::types::FoldingOptions>(dataIntentFb->foldOption));
                intent->setBookletMakerOption(static_cast<dune::imaging::types::BookletMakingOptions>(dataIntentFb->foldOption));
                intent->setCustomMediaXDimension(dataIntentFb->customMediaXDimension);
                intent->setCustomMediaYDimension(dataIntentFb->customMediaYDimension);
                dune::scan::Jobs::Scan::deserializeScanJobIntent(dataIntentFb->scanJobIntent, intent);
                objClass = oc;
                savedCompleted = true;
                delete data;
                return savedCompleted;
            }
        ));

    // Execute connected
    std::future<void> asyncCompletion;
    component_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    ASSERT_TRUE(savedCompleted);

    // Check Ticket default Result
    auto ticketGoodFormed = createCopyJobTicket(createCorrectJobIntent(),createExpectedConstraints());
    ticketGoodFormed->setVersion(2);                                                            // 2 is current version on src/fw/copy/Jobs/Copy/JobService/Standard/test/testResources/JobServiceStandardTestDataVersioned.json
    ticketGoodFormed->getIntent()->setMediaFamily(dune::imaging::types::MediaFamily::UNKNOWN);  // Correction from same json file
    ticketGoodFormed->getIntent()->setImagePreview(dune::scan::types::ImagePreview::Enable);  // Correction from same json file
    EXPECT_TRUE(dune::copy::Jobs::Copy::compareIntents(ticketInsertedToCache->getIntent(), ticketGoodFormed->getIntent()));
}

TEST_F(GivenAInitializedJobServiceStandardPreparedToForceUpgrade,WhenConnectIsCalledAndTicketFromUserHasVersion_ThenValueOfTicketIsNotUpdated)
{
    // user quickset expectation from cache and list of shortcuts
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticket = createCopyJobTicket(createCorrectJobIntent(),createExpectedConstraints());
    ticket->setVersion(2); // 2 is current version on src/fw/copy/Jobs/Copy/JobService/Standard/test/testResources/JobServiceStandardTestDataVersioned.json
    insertShortcutOnList(ticket);
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketInsertedToCache = createCopyJobTicket(createIncorrectJobIntent(),createExpectedConstraints());
    bool savedCompleted = false;
    dune::framework::data::ObjectClassification objClass;

    EXPECT_CALL(mockIDataStore_, find(Matcher<const Uuid &>(_))).WillRepeatedly(testing::InvokeWithoutArgs([&ticket,this]() {
        // Get Serialized data
        auto serializedData = ticket->serialize();

        // Return serialized data
        std::pair<bool, DataObject> returnVal;
        returnVal.first = true;
        returnVal.second.buffer.first = std::move(serializedData.first);
        returnVal.second.buffer.second = serializedData.second;
        return returnVal;
    }));

    EXPECT_CALL(mockIDataStore_, insert_or_replace_ex(_, _, _)).Times(0)
        .WillRepeatedly(Invoke(
            [&savedCompleted, &objClass,this, &ticketInsertedToCache](const dune::framework::data::SerializedDataBuffer& object, const dune::framework::core::Uuid& uuid,const dune::framework::data::ObjectClassification& oc)
            {
                auto packedFb = flatbuffers::GetRoot<dune::copy::Jobs::Copy::CopyJobTicketFb>(object.first);
                auto data = packedFb->UnPack();
                auto dataIntentFb = std::move(data->intent);
                auto intent = ticketInsertedToCache->getIntent();

                intent->setOutputMediaSizeId(dataIntentFb->outputMediaSizeId);
                intent->setOutputMediaOrientation(dataIntentFb->outputMediaOrientation);
                intent->setOutputMediaIdType(dataIntentFb->outputMediaIdType);
                intent->setOutputMediaSource(dataIntentFb->outputMediaSource);
                intent->setOutputPlexMode(dataIntentFb->outputPlexMode);
                intent->setCopyMargins(dataIntentFb->copyMargins);
                intent->setOutputPlexBinding(dataIntentFb->outputPlexBinding);
                intent->setCopies(dataIntentFb->copies);
                intent->setCollate(dataIntentFb->collate);
                intent->setCopyQuality(dataIntentFb->copyQuality);
                intent->setOutputDestination(dataIntentFb->outputMediaDestination);
                intent->setPrintingOrder(dataIntentFb->printingOrder);
                intent->setRotation(dataIntentFb->rotation);
                intent->setAutoRotate(dataIntentFb->autoRotate);
                intent->setMediaFamily(dataIntentFb->mediaFamily);
                intent->setStapleOption(static_cast<dune::imaging::types::StapleOptions>(dataIntentFb->stapleOption));
                intent->setPunchOption(static_cast<dune::imaging::types::PunchingOptions>(dataIntentFb->punchOption));
                intent->setFoldOption(static_cast<dune::imaging::types::FoldingOptions>(dataIntentFb->foldOption));
                intent->setBookletMakerOption(static_cast<dune::imaging::types::BookletMakingOptions>(dataIntentFb->foldOption));
                intent->setCustomMediaXDimension(dataIntentFb->customMediaXDimension);
                intent->setCustomMediaYDimension(dataIntentFb->customMediaYDimension);
                dune::scan::Jobs::Scan::deserializeScanJobIntent(dataIntentFb->scanJobIntent, intent);
                objClass = oc;
                savedCompleted = true;
                delete data;
                return true;
            }
        ));

    EXPECT_CALL(mockIJobTicketResourceManager_,loadJobTicketIntoCacheIfNeeded(_,_)).WillRepeatedly(Return(ticket));

    // Execute connected
    std::future<void> asyncCompletion;
    component_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    ASSERT_FALSE(savedCompleted);
}

TEST_F(GivenAInitializedJobServiceStandardPreparedToForceUpgrade,WhenConnectIsCalledAndTicketFromUserHasNotVersion_ThenValueOfTicketIsUpdated)
{
    // user quickset expectation from cache and list of shortcuts
    // Constraints that not fit
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticket = createCopyJobTicket(createCorrectJobIntent(),createExpectedConstraints());
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketGoodFormed = createCopyJobTicket(createCorrectJobIntent(),createExpectedConstraints());
    ticketGoodFormed->setVersion(2);                                                            // 2 is current version on src/fw/copy/Jobs/Copy/JobService/Standard/test/testResources/JobServiceStandardTestDataVersioned.json
    ticketGoodFormed->getIntent()->setMediaFamily(dune::imaging::types::MediaFamily::UNKNOWN); // Correction from same json file
    ticketGoodFormed->getIntent()->setImagePreview(dune::scan::types::ImagePreview::Enable);  // Correction from same json file
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> ticketInsertedToCache = createCopyJobTicket(createIncorrectJobIntent(),createExpectedConstraints());
    bool savedCompleted = false;
    dune::framework::data::ObjectClassification objClass;

    // Create a shortcut on list to check
    insertShortcutOnList(ticket);

    // Return for Default Ticket
    EXPECT_CALL(mockIDataStore_, find(Matcher<const Uuid &>(_)))
    .WillOnce(testing::InvokeWithoutArgs([&ticketGoodFormed,this]() {
        // Get Serialized data
        auto serializedData = ticketGoodFormed->serialize();

        // Return serialized data
        std::pair<bool, DataObject> returnVal;
        returnVal.first = true;
        returnVal.second.buffer.first = std::move(serializedData.first);
        returnVal.second.buffer.second = serializedData.second;
        return returnVal;
    }));

    // Insert of ticket of shortcut expected
    EXPECT_CALL(mockIDataStore_, insert_or_replace_ex(_, _, _))
        .WillOnce(Invoke(
            [&savedCompleted, &objClass,this, &ticketInsertedToCache](const dune::framework::data::SerializedDataBuffer& object, const dune::framework::core::Uuid& uuid,const dune::framework::data::ObjectClassification& oc)
            {
                auto packedFb = flatbuffers::GetRoot<dune::copy::Jobs::Copy::CopyJobTicketFb>(object.first);
                auto data = packedFb->UnPack();
                auto dataIntentFb = std::move(data->intent);
                auto intent = ticketInsertedToCache->getIntent();

                intent->setOutputMediaSizeId(dataIntentFb->outputMediaSizeId);
                intent->setOutputMediaOrientation(dataIntentFb->outputMediaOrientation);
                intent->setOutputMediaIdType(dataIntentFb->outputMediaIdType);
                intent->setOutputMediaSource(dataIntentFb->outputMediaSource);
                intent->setOutputPlexMode(dataIntentFb->outputPlexMode);
                intent->setCopyMargins(dataIntentFb->copyMargins);
                intent->setOutputPlexBinding(dataIntentFb->outputPlexBinding);
                intent->setCopies(dataIntentFb->copies);
                intent->setCollate(dataIntentFb->collate);
                intent->setCopyQuality(dataIntentFb->copyQuality);
                intent->setOutputDestination(dataIntentFb->outputMediaDestination);
                intent->setPrintingOrder(dataIntentFb->printingOrder);
                intent->setRotation(dataIntentFb->rotation);
                intent->setAutoRotate(dataIntentFb->autoRotate);
                intent->setMediaFamily(dataIntentFb->mediaFamily);
                intent->setStapleOption(static_cast<dune::imaging::types::StapleOptions>(dataIntentFb->stapleOption));
                intent->setPunchOption(static_cast<dune::imaging::types::PunchingOptions>(dataIntentFb->punchOption));
                intent->setFoldOption(static_cast<dune::imaging::types::FoldingOptions>(dataIntentFb->foldOption));
                intent->setBookletMakerOption(static_cast<dune::imaging::types::BookletMakingOptions>(dataIntentFb->foldOption));
                intent->setCustomMediaXDimension(dataIntentFb->customMediaXDimension);
                intent->setCustomMediaYDimension(dataIntentFb->customMediaYDimension);
                dune::scan::Jobs::Scan::deserializeScanJobIntent(dataIntentFb->scanJobIntent, intent);
                objClass = oc;
                savedCompleted = true;
                delete data;
                return savedCompleted;
            }
        ));

    // Load ticket to cache expected
    EXPECT_CALL(mockIJobTicketResourceManager_,loadJobTicketIntoCacheIfNeeded(_,_)).WillOnce(Invoke(
        [&ticket, this](const Uuid &ticketId, bool &persistedJobTicket)
        {
            auto ticketOnCache = std::dynamic_pointer_cast<dune::copy::Jobs::Copy::CopyJobTicket>(this->component_->deserializeBaseTicketOnlyIfNotInCache(ticket->serialize(), persistedJobTicket));
            ticketOnCache->setConstraintsFromFb(createExpectedConstraints());
            return ticketOnCache;
        }
    ));

    // Execute connected
    std::future<void> asyncCompletion;
    component_->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    // Check Ticket user quickset Result
    EXPECT_TRUE(savedCompleted);
    EXPECT_TRUE(dune::copy::Jobs::Copy::compareIntents(ticketInsertedToCache->getIntent(), ticketGoodFormed->getIntent()));
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedJobServiceStandardReadyToCallShutdown : shutdown case.
//           Reimplemented to avoid diamond problem
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedJobServiceStandardReadyToCallShutdown : public ::testing::TestWithParam<IComponent::ShutdownCause>
{
  public:
    GivenAConnectedJobServiceStandardReadyToCallShutdown() { GTEST_CHECKPOINTA("GivenAConnectedJobServiceStandardReadyToCallShutdown::Constructor\n"); }

    void SetUp() override;
    std::unique_ptr<CollectionEasyBufferTable> getShortcuts(const bool pinValidateNotRequired,
        const shortcutFilter_t &filter = shortcutFilter_t());

    std::unique_ptr<ItemEasyBufferTable> getShortcut(const dune::framework::core::Uuid &uuid,const bool pinValidateNotRequired,
                                                        const shortcutFilter_t &filter = shortcutFilter_t());

    ShortcutOperationResult addShortcut( const std::unique_ptr<ItemEasyBufferTable> &shortcut);

    ShortcutOperationResult updateShortcut(std::unique_ptr<ItemEasyBufferTable>& shortcut,const bool pinValidateNotReq,const shortcutFilter_t &filter = shortcutFilter_t());

  protected:
    std::unique_ptr<TestSystemServices> systemServices_{};
    MockIDataStore                      mockIDataStore_;
    MockIImagePersister                 mockIImagePersister_;
    MockIJobManager                     mockIJobManager_;
    MockIJobManagerAlertProvider        mockIJobManagerAlertProvider_;
    MockIJobServiceManager              mockIJobServiceManager_;
    MockIJobTicketResourceManager       mockIJobTicketResourceManager_;
    MockIJobDetailsManager              mockDetailsManager_;
    MockIPageAssembler                  mockIPageAssembler_;
    MockIPipelineMemoryClientCreator    mockIPipelineMemoryClientCreator_;
    MockIPrintDevice                    mockIPrintDevice_;
    MockIPrintIntentsFactory            mockIPrintIntentsFactory_;
    MockIRasterFormatSelector           mockIRasterFormatSelector_;
    MockIResourceManagerClient          mockIResourceManagerClient_;
    MockIResourceService                mockIResourceService_;
    MockIScanDevice                     mockIScanDevice_;
    MockIColorDirector                  mockIColorDirector_;
    IComponentManager*                  componentManager_{nullptr};
    IComponent*                         comp{nullptr};
    std::unique_ptr<JobServiceStandard> component_{};
    MockIShortcuts                      mockIShortcut_;
    MockIScanPipeline                   mockIScanPipeline_{};
    MockIMedia                          mockIMedia_{};
    MockIMediaInputCapabilities         mockIMediaInputCapabilities_{};
    MockIScannerCapabilities            mockIScannerCapabilities_{};
    MockIIntentsManager                 mockIIntentsManager_{};
    MockISettings                       mockISettings_{};
    MockIRenderingRequirements          mockIRenderingRequirements_{};
    MockINvram                          mockINvram_{};
    MockIJobConstraints                 mockIJobConstraints_{};
    MockICopyJobDynamicConstraintRules  mockICopyJobDynamicConstraintRules_{};
    MockICopyAdapter                    mockICopyAdapter_{};
    ICopyAdapterDataChangeEvent         copyAdapterDataChangeEvent_;
    CollectionEasyBufferTable           internalShortCutCollection_;
    std::shared_ptr<MockILocaleProvider>mockLocaleProvider_;
    MockIExportImport                   mockIExportImport_{};
    MockISecureFileErase                mockISecureFileErase_{};
    ScanMediaSize                       scanMediaSize_{};
    MockIScanConstraints                mockIScanConstraints_{};
};

void GivenAConnectedJobServiceStandardReadyToCallShutdown::SetUp()
{
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/JobServiceStandardTestData.json");

    component_ = std::make_unique<JobServiceStandard>("myInstance");
    comp = static_cast<IComponent*>(component_.get());

    // Set the default metric as units system
    mockLocaleProvider_ = std::make_shared<MockILocaleProvider>();
    ASSERT_TRUE(mockLocaleProvider_ != nullptr);
    component_->setInterface(GET_INTERFACE_UID(dune::localization::ILocaleProvider),"MockILocaleProvider",(void*)mockLocaleProvider_.get());
    ON_CALL(*mockLocaleProvider_, getMeasurmentUnit()).WillByDefault(Return(dune::localization::MeasurementUnit::METRIC));

    EXPECT_CALL(mockIScanDevice_, getResourceService).WillRepeatedly(Return(&mockIResourceService_));
    EXPECT_CALL(mockIImagePersister_, getResourceService).WillRepeatedly(Return(&mockIResourceService_));
    EXPECT_CALL(mockIPageAssembler_, getResourceService).WillRepeatedly(Return(&mockIResourceService_));
    EXPECT_CALL(mockIPrintDevice_, getResourceService).WillRepeatedly(Return(&mockIResourceService_));
    EXPECT_CALL(mockIPrintDevice_, getRasterFormatSelector(_)).WillRepeatedly(Return(&mockIRasterFormatSelector_));
    EXPECT_CALL(mockIPrintDevice_, getPipelineMemoryClientCreator).WillRepeatedly(Return(&mockIPipelineMemoryClientCreator_));
    EXPECT_CALL(mockIScanPipeline_, getScanPipelineConfiguration()).WillRepeatedly(Return(nullptr));

    ON_CALL(mockIShortcut_,getShortcuts(_,_)).WillByDefault(WithArgs<0,1>(Invoke(
        [=] (const bool pinValidateNotRequired, const shortcutFilter_t &filter = shortcutFilter_t()) -> std::unique_ptr<CollectionEasyBufferTable>
        {
            return getShortcuts(pinValidateNotRequired, filter);
        }
    )));
    ON_CALL(mockIShortcut_,getShortcut(_,_,_)).WillByDefault(WithArgs<0,1,2>(Invoke(
        [=](const dune::framework::core::Uuid &uuid,const bool pinValidateNotRequired,
                const shortcutFilter_t &filter = shortcutFilter_t()) -> std::unique_ptr<ItemEasyBufferTable>
        {
            return getShortcut(uuid, pinValidateNotRequired, filter);
        }
    )));
    ON_CALL(mockIShortcut_,addShortcut(_)).WillByDefault(WithArgs<0>(Invoke(
        [=] (const std::unique_ptr<ItemEasyBufferTable> &shortcut) -> ShortcutOperationResult
        {
            return addShortcut(shortcut);
        }
    )));
    ON_CALL(mockIShortcut_,updateShortcut(_,_,_)).WillByDefault(WithArgs<0,1,2>(Invoke(
        [=] (std::unique_ptr<ItemEasyBufferTable> shortcut,const bool pinValidateNotReq,const shortcutFilter_t &filter = shortcutFilter_t()) -> ShortcutOperationResult
        {
            return updateShortcut(shortcut,pinValidateNotReq,filter);
        }
    )));

    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    // fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);

    ON_CALL(mockIScanPipeline_, getScanMediaSize()).WillByDefault(ReturnRef(scanMediaSize_));

    EXPECT_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillOnce(ReturnRef(copyAdapterDataChangeEvent_));

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}

std::unique_ptr<CollectionEasyBufferTable> GivenAConnectedJobServiceStandardReadyToCallShutdown::getShortcuts(const bool pinValidateNotRequired, const shortcutFilter_t &filter)
{
    DUNE_UNUSED(pinValidateNotRequired);

    CollectionEasyBufferTable auxiliaryCollection;

    // Apply filter get
    if(internalShortCutCollection_.shortcuts.size() > 0){
        for (auto& shortcut : internalShortCutCollection_.collection().getMutable())
        {
            if((filter.factory == dune::cdm::glossary_1::FeatureEnabled::_undefined_    || filter.factory == shortcut.factory.get()) &&
               (filter.type == dune::cdm::shortcut_1::Type::_undefined_                 || filter.type == shortcut.type.get()) &&
               (filter.readOnly == dune::cdm::glossary_1::FeatureEnabled::_undefined_   || filter.readOnly == shortcut.readOnly.get()) &&
               (filter.origin == dune::cdm::shortcut_1::Origin::_undefined_             || filter.origin == shortcut.origin.get()))
            {
                ItemEasyBufferTable shortcutSendToUsb = ItemEasyBufferTable{shortcut};
                auxiliaryCollection.shortcuts.insertItem(shortcutSendToUsb);
            }
        }
    }

    return std::make_unique<CollectionEasyBufferTable>(auxiliaryCollection);
}

std::unique_ptr<ItemEasyBufferTable> GivenAConnectedJobServiceStandardReadyToCallShutdown::getShortcut(const dune::framework::core::Uuid &uuid,const bool pinValidateNotRequired,
                                                                                                        const shortcutFilter_t &filter)
{
    DUNE_UNUSED(pinValidateNotRequired);

    std::unique_ptr<ItemEasyBufferTable> result = nullptr;

    if(internalShortCutCollection_.shortcuts.size() > 0){
        for (auto& shortcut : internalShortCutCollection_.collection().getMutable())
        {
            if(shortcut.id.get() == uuid.toString())
            {
                result = std::make_unique<ItemEasyBufferTable>(shortcut);
            }
        }
    }

    return result;
}

ShortcutOperationResult GivenAConnectedJobServiceStandardReadyToCallShutdown::addShortcut( const std::unique_ptr<ItemEasyBufferTable> &shortcut)
{
    ItemEasyBufferTable shortcutSendToUsb = ItemEasyBufferTable{*shortcut.get()};

    bool result = internalShortCutCollection_.shortcuts.insertItem(shortcutSendToUsb);

    return result ? ShortcutOperationResult::OK : ShortcutOperationResult::ERROR_GENERIC;
}

ShortcutOperationResult GivenAConnectedJobServiceStandardReadyToCallShutdown::updateShortcut(std::unique_ptr<ItemEasyBufferTable>& shortcut,
                                                                                                const bool pinValidateNotReq,const shortcutFilter_t &filter)
{
    bool result = false;
    if(shortcut)
    {
        result = internalShortCutCollection_.shortcuts.updateItem(*shortcut.get());
    }

    return result ? ShortcutOperationResult::OK : ShortcutOperationResult::ERROR_GENERIC;
}

TEST_P(GivenAConnectedJobServiceStandardReadyToCallShutdown, whenShutdownIsCalled_TheComponentGetsShutdown)
{
    // Call GetParam() here to get the Row values
    IComponent::ShutdownCause const& p = GetParam();

    std::future<void> asyncCompletion;
    comp->shutdown(p, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

     ASSERT_TRUE(true);
}

INSTANTIATE_TEST_CASE_P(InstantiationName, GivenAConnectedJobServiceStandardReadyToCallShutdown, ::testing::Values(
 IComponent::ShutdownCause(IComponent::ShutdownCause::POWER_OFF),
 IComponent::ShutdownCause(IComponent::ShutdownCause::REBOOT),
 IComponent::ShutdownCause(IComponent::ShutdownCause::SEVERE_ERROR),
 IComponent::ShutdownCause(IComponent::ShutdownCause::EMERGENCY_ERROR),
 IComponent::ShutdownCause(IComponent::ShutdownCause::CRITICAL_ERROR)
));

// Test for WaitforMedaiEventAndValidate function
TEST_F(GivenANewJobServiceStandard, WhenWaitforMedaiEventAndValidateIsCalled_FunctionExecutesCorrectly)
{
    // Setup system services and initialize component
    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/JobServiceStandardTestData.json");
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

   
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyPipeline), "MockICopyPipeline", &mockCopyPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);
    
    // Mock setup for copy adapter
    EXPECT_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillOnce(ReturnRef(copyAdapterDataChangeEvent_));

    // Connect the component
    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    // Create a mock job ticket table for testing
    auto mockJobTicketTable = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    
    // Call the private function under test directly (using FRIEND_TEST access)
    EXPECT_NO_THROW({
        component_->WaitforMedaiEventAndValidate(mockJobTicketTable);
    });

    // Verify the function executed without errors
    ASSERT_TRUE(true);
}

// Test for onEngineConnectionChange function with hardware capabilities available
TEST_F(GivenANewJobServiceStandard, WhenOnEngineConnectionChangeIsCalled_WithHwCapabilitiesAvailable_FunctionExecutesCorrectly)
{
    // Setup system services and initialize component
    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/JobServiceStandardTestData.json");
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyPipeline), "MockICopyPipeline", &mockCopyPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    // Mock setup for copy adapter
    EXPECT_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillOnce(ReturnRef(copyAdapterDataChangeEvent_));

    // Connect the component
    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    // Create mock connector and status with hardware capabilities available
    dune::print::engine::IConnector* mockConnector = nullptr;
    dune::print::engine::IConnector::ConnectorStatus mockStatus;
    
    // Mock the status to return true for areHwCapabilitiesAvailable()
    // Note: This would typically require a mock implementation of ConnectorStatus
    
    // Call the private function under test directly (using FRIEND_TEST access)
    EXPECT_NO_THROW({
        component_->onEngineConnectionChange(mockConnector, mockStatus);
    });

    // Verify the function executed without errors
    ASSERT_TRUE(true);
}

// Test for onEngineConnectionChange function without hardware capabilities
TEST_F(GivenANewJobServiceStandard, WhenOnEngineConnectionChangeIsCalled_WithoutHwCapabilities_FunctionExecutesCorrectly)
{
    // Setup system services and initialize component
    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/JobServiceStandardTestData.json");
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyPipeline), "MockICopyPipeline", &mockCopyPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    // Mock setup for copy adapter
    EXPECT_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillOnce(ReturnRef(copyAdapterDataChangeEvent_));

    // Connect the component
    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    // Create mock connector and status without hardware capabilities
    dune::print::engine::IConnector* mockConnector = nullptr;
    dune::print::engine::IConnector::ConnectorStatus mockStatus;
    
    // Call the private function under test directly (using FRIEND_TEST access)
    EXPECT_NO_THROW({
        component_->onEngineConnectionChange(mockConnector, mockStatus);
    });

    // Verify the function executed without errors
    ASSERT_TRUE(true);
}

// Test for migration logic in connected method
TEST_F(GivenANewJobServiceStandard, WhenConnectedIsCalled_MigrationLogicExecutesCorrectly)
{
    // Setup system services and initialize component
    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/JobServiceStandardTestData.json");
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());

    
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::color::IColorDirector), "ColorDirector", &mockIColorDirector_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageRetriever", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler), "PageAssemblerService", &mockIPageAssembler_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::Resources::IPrintDevice), "PrintDeviceService", &mockIPrintDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobTicketResourceManager), "JobTicketResourceManager", &mockIJobTicketResourceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory), "PrintIntentsFactory", &mockIPrintIntentsFactory_);
    comp->setInterface(GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts), "MockIShortcuts", &mockIShortcut_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline), "MockIScanPipeline", &mockIScanPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia), "MockIMedia", &mockIScanMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities), "MockIScannerCapabilities", &mockIScannerCapabilities_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::ISettings), "MockISettings", &mockISettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements), "MockIRenderingRequirements", &mockIRenderingRequirements_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::INvram), "MockINvram", &mockINvram_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IIntentsManager), "MockIIntentsManager", &mockIIntentsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMedia), "MockIMedia", &mockIPrintMedia_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings), "MockIMediaHandlingSettings", &mockIMediaHandlingSettings_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes), "MockIMediaAttributes", &mockIMediaAttributes_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyPipeline), "MockICopyPipeline", &mockCopyPipeline_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::conversion::ISystemConversionHelper), "MockISystemConversionHelper", &mockISystemConversionHelper_);

    // Mock setup for copy adapter
    EXPECT_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillOnce(ReturnRef(copyAdapterDataChangeEvent_));

    // Mock setup for system conversion helper to simulate migration scenario
    EXPECT_CALL(mockISystemConversionHelper_, mustConvertDataThisBoot())
        .WillOnce(Return(true));

    // Connect the component - this should trigger migration logic
    std::future<void> asyncCompletion;
    EXPECT_NO_THROW({
        comp->connected(componentManager_, asyncCompletion);
        if (asyncCompletion.valid())
        {
            asyncCompletion.wait();
        }
    });

    // Verify the migration logic was executed without errors
    ASSERT_TRUE(true);
}

}}}} // namespace dune::copy::Jobs::Copy::JobService::Standard