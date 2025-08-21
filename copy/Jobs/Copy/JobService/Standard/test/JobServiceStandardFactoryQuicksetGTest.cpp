#include "gmock/gmock.h"
#include "gtest/gtest.h"

#include "ComponentSystemTypes.h"
#include "GTestConfigHelper.h"
#include "JobServiceStandard.h"
#include "MockIDataStore.h"
#include "MockIImagePersister.h"
#include "MockIJobManager.h"
#include "MockIJobManagerAlertProvider.h"
#include "MockIJobServiceManager.h"
#include "MockIJobDetailsManager.h"
#include "MockIJobTicketResourceManager.h"
#include "MockIPageAssembler.h"
#include "MockIPipelineMemoryClientCreator.h"
#include "MockIPrintDevice.h"
#include "MockIPrintIntentsFactory.h"
#include "MockIRasterFormatSelector.h"
#include "MockIResourceManagerClient.h"
#include "MockIResourceService.h"
#include "MockIScanDevice.h"
#include "MockIShortcuts.h"
#include "MockIScanPipeline.h"
#include "MockIScannerMedia.h"
#include "MockIMedia.h"
#include "MockICapabilities.h"
#include "MockIJobConstraints.h"
#include "MockICopyJobDynamicConstraintRules.h"
#include "MockICopyAdapter.h"
#include "TestSystemServices.h"
#include "MockIScanConstraints.h"
#include "MediaInputCapabilities.h"
#include "MediaHelper.h"
#include "SimplePathDirMock.h"
#include "com.hp.cdm.service.shortcut.version.1.serviceDefinition_autogen.h"
#include "MockILocale.h"
#include "MockILocaleProvider.h"
#include "MockIExportImport.h"
#include "MockISecureFileErase.h"
#include "MediaSize.h"
#include "MediaSizeId_generated.h"
#include "MockIMediaInfo.h"
#include "MockIMediaInfoPageBased.h"
#include "IMediaInfoPageBased.h"

using ComponentFlavorUid                = dune::framework::component::ComponentFlavorUid;
using IComponent                        = dune::framework::component::IComponent;
using IComponentManager                 = dune::framework::component::IComponentManager;
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
using MockIPrintIntentsFactory          = dune::print::engine::MockIPrintIntentsFactory;
using MockIRasterFormatSelector         = dune::imaging::MockIRasterFormatSelector;
using MockIResourceManagerClient        = dune::job::MockIResourceManagerClient;
using MockIResourceService              = dune::job::MockIResourceService;
using MockIScanDevice                   = dune::scan::Resources::MockIScanDevice;
using SystemServices                    = dune::framework::component::SystemServices;
using TestSystemServices                = dune::framework::component::TestingUtil::TestSystemServices;
using MockIShortcuts                    = dune::admin::shortcuts::MockIShortcuts;
using MockIScanPipeline                 = dune::scan::Jobs::Scan::MockIScanPipeline;
using ScanMediaSize                     = dune::scan::Jobs::Scan::ScanMediaSize;
using MockIMedia                        = dune::scan::scanningsystem::MockIMedia;
using MockIPrintMedia                   = dune::print::engine::MockIMedia;
using MockIMediaInputCapabilities       = dune::scan::scanningsystem::MockIMediaInputCapabilities;
using MockIScannerCapabilities          = dune::scan::scanningsystem::MockIScannerCapabilities;
using MockIMediaPath                    = dune::scan::scanningsystem::MockIMediaPath;
using MockIScanConstraints              = dune::scan::MockIScanConstraints;
using IInputList                        = dune::scan::scanningsystem::IMedia::IInputList;   
using MediaInputCapabilities            = dune::scan::scanningsystem::MediaInputCapabilities;
using MediaSource                       = dune::imaging::types::MediaSource;
using MockIMediaIInput                  = dune::print::engine::MockIMediaIInput;
using InputList                         = dune::print::engine::IMedia::InputList;
using MediaHelper                       = dune::print::engine::MediaHelper;
using Permission                        = dune::security::ac::Permission;
using MockIJobConstraints               = dune::copy::Jobs::Copy::MockIJobConstraints;
using MockICopyJobDynamicConstraintRules = dune::copy::Jobs::Copy::MockICopyJobDynamicConstraintRules;
using MockICopyAdapter                  = dune::copy::cdm::MockICopyAdapter;
using MockILocale                       = dune::localization::MockILocale;
using MockILocaleProvider               = dune::localization::MockILocaleProvider;
using ICopyAdapterDataChangeEvent       = dune::framework::core::event::EventSource<dune::copy::cdm::CopyConfigurationEventType>;
using CollectionEasyBufferTable         = dune::cdm::shortcut_1::ShortcutsTable;
using ItemEasyBufferTable               = dune::cdm::shortcut_1::ShortcutTable;
using ShortcutOperationResult           = dune::admin::shortcuts::ShortcutOperationResult;
using shortcutFilter_t                  = dune::admin::shortcuts::shortcutFilter_t;
using MockIExportImport                 = dune::framework::data::backup::MockIExportImport;
using OperationType                     = dune::framework::data::backup::OperationType;
using MockISecureFileErase              = dune::framework::storage::MockISecureFileErase;
using MediaSizeId          = dune::imaging::types::MediaSizeId;
using MockIMediaInfo                    = dune::print::engine::MockIMediaInfo;
using MediaPropertyChangedEvent =  dune::framework::core::event::EventSource<dune::print::engine::pageBased::MediaPropertyChangedEventArgs>;
using MockIMediaInfoExtension   = dune::print::engine::pageBased::MockIMediaInfoExtension;
using MediaPropertyChangedEventArgs = dune::print::engine::pageBased::MediaPropertyChangedEventArgs;

using ::testing::ReturnRef;
using testing::_;
using testing::Return;
using testing::Invoke;
using ::testing::SetArgPointee;
using ::testing::WithArgs;
using ::testing::ByMove;

#define RESOURCE_PATH "./testResources/"

/**
 * Test Relative to Factory QuickSet
 */
///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedJobServiceStandardShortcutListEmpty
//
///////////////////////////////////////////////////////////////////////////////

typedef std::tuple< std::string,                                    // Config json with names of json
                    std::vector<std::string>                        // Vector with expected id loaded on shortcut list
                    > GetQuickSetEncapsulation;

class GivenAConnectedJobServiceStandardShortcutListEmpty : public ::testing::Test
{
public:
    GivenAConnectedJobServiceStandardShortcutListEmpty() { GTEST_CHECKPOINTA("GivenAConnectedJobServiceStandardShortcutListEmpty::Constructor -- ENTER\n"); };

    void SetUp() override;

    void SetUpJsonFactoryQuickSets(std::string jsonName);

    // Fake Methods for IMockShortcut
    /**
     * @brief getShortcuts
     * @return Return all shortcuts registered in the system
     * query can be done to return based on type, source destination
     * if any one of them is not given , all shortcuts of that category would be returned
     */
    std::unique_ptr<CollectionEasyBufferTable> getShortcuts(const bool pinValidateNotRequired,
        const shortcutFilter_t &filter = shortcutFilter_t());

    /**
     * @brief getShortcut
     * @param uuid
     * @return return a short based on the UUID
     */
    std::unique_ptr<ItemEasyBufferTable> getShortcut(const dune::framework::core::Uuid &uuid,const bool pinValidateNotRequired,
                                                        const shortcutFilter_t &filter = shortcutFilter_t());

    /**
     * @brief addShortcut
     * @param shortcut
     * @return Add a new shortcut. Based on the Origin it will be persitent or not
     * Origin == Device  will be persitent , other would need to call this function on every boot
     */
    ShortcutOperationResult addShortcut( const std::unique_ptr<ItemEasyBufferTable> &shortcut);

    /**
     * @brief removeShortcut
     * @param shortcut
     * @return Removes a shortcut, Our a persitent shortcut it will be erased from the store also
     */
    ShortcutOperationResult removeShortcut(const Uuid &shortcutId,const bool pinValidateNotReq,const shortcutFilter_t &filter = shortcutFilter_t());

    /**
     * @brief updateShortcut
     * @param shortcut
     * @return updates a shortcut
     */
    ShortcutOperationResult updateShortcut(std::unique_ptr<ItemEasyBufferTable>& shortcut,const bool pinValidateNotReq,const shortcutFilter_t &filter = shortcutFilter_t());

    /**
     * @brief Main Execution of current test     
     */
    void executeConnectedAction();

    /**
     * @brief List of quicksets expected on ShortcutCollection
     * Can be a vector of 0 or more
     * @param quickSetsExpected json value to take directly from it the fb expected and perform comparison
     */
    void checkQuicksetList(std::vector<std::string> quickSetsExpected = std::vector<std::string>());

    /**
     * @brief Search for a unique quickset on list     
     * @param quickSetsExpected name of quickset expected
     */
    void checkQuicksetList(std::string quickSetsExpected);

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
    MockIScanDevice                     mockIScanDevice_;
    MockIJobDetailsManager              mockDetailsManager_;
    IComponentManager*                  componentManager_{nullptr};
    IComponent*                         comp{nullptr};
    std::unique_ptr<JobServiceStandard> component_{};
    MockIShortcuts                      mockIShortcut_{};
    MockIScanPipeline                   mockIScanPipeline_{};
    ScanMediaSize                       scanMediaSize_{};
    MockIMedia                          mockIScanMedia_{};
    MockIMediaInputCapabilities         mockIMediaInputCapabilities_{};
    MockIScannerCapabilities            mockIScannerCapabilities_{};
    std::shared_ptr<MockIMediaPath>     pMockIMediaPath_;
    IInputList                          mockIScanInputList_;
    MediaInputCapabilities              mediaICap;
    MockIPrintMedia                     mockIPrintMedia_{};
    InputList                           printList_;
    std::shared_ptr<MockIMediaIInput>   pMockIMediaIInput_;
    MockIJobConstraints                 mockIJobConstraints_{};
    MockICopyJobDynamicConstraintRules  mockICopyJobDynamicConstraintRules_{};  
    MockICopyAdapter                    mockICopyAdapter_{};
    ICopyAdapterDataChangeEvent         copyAdapterDataChangeEvent_;
    std::shared_ptr<MockILocale>        mockILocale_{};
    MockILocaleProvider                 mockILocaleProvider_{};
    dune::localization::StringId_Type   localizationId{0};
    MockIExportImport                   mockIExportImport_{};
    MockISecureFileErase                mockISecureFileErase_{};
    MockIMediaInfo                      mockIMediaInfo_{};
    MockIMediaInfoExtension             mockIMediaInfoPageBased_;    
    MediaPropertyChangedEvent           mediaPropertyChangedEvent_;
    MockIScanConstraints                mockIScanConstraints_;

    // Internal Variables
    CollectionEasyBufferTable internalShortCutCollection_;
    std::string jsonToRead_;
    std::vector<std::string> listOfQuickSetVector_;    
};

void GivenAConnectedJobServiceStandardShortcutListEmpty::SetUp()
{
    GTEST_CHECKPOINTA("GivenAConnectedJobServiceStandardShortcutListEmpty::SetUp -- ENTER\n");
    systemServices_ = std::make_unique<TestSystemServices>();
    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/JobServiceStandardTestData.json");
    
    component_ = std::make_unique<JobServiceStandard>(instanceName_);
    component_->setIfResourcePathNeedComponentId(false);
    comp = static_cast<IComponent*>(component_.get());
    ASSERT_TRUE(component_ != nullptr);    
    
    //Scan list
    pMockIMediaPath_ = std::make_shared<MockIMediaPath>();
    ASSERT_TRUE(pMockIMediaPath_ != nullptr);
    mockIScanInputList_.push_back(pMockIMediaPath_);
    
    //Print list
    pMockIMediaIInput_ = std::make_shared<MockIMediaIInput>();
    ASSERT_TRUE(pMockIMediaIInput_ != nullptr);
    printList_.push_back(pMockIMediaIInput_);
    
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
    
    //printMedia
    EXPECT_CALL(mockIPrintMedia_, getInputDevices).WillRepeatedly(Return(tupleInputList));
    EXPECT_CALL((*pMockIMediaIInput_), getMediaSupportedSizes).WillRepeatedly(Return(tupleMediaOrientedSizes));
    // Create all on-call expects with mock shortcut, and perform method to call non-static methods.
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
    ON_CALL(mockIShortcut_,removeShortcut(_,_,_)).WillByDefault(WithArgs<0,1,2>(Invoke(
        [=] (const Uuid &shortcutId,const bool pinValidateNotReq,const shortcutFilter_t &filter = shortcutFilter_t()) -> ShortcutOperationResult
        {
            return removeShortcut(shortcutId,pinValidateNotReq,filter);
        }
    )));
    ON_CALL(mockIShortcut_,updateShortcut(_,_,_)).WillByDefault(WithArgs<0,1,2>(Invoke(
        [=] (std::unique_ptr<ItemEasyBufferTable> shortcut,const bool pinValidateNotReq,const shortcutFilter_t &filter = shortcutFilter_t()) -> ShortcutOperationResult
        {
            return updateShortcut(shortcut,pinValidateNotReq,filter);
        }
    )));

    // fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "MockIDataStore", &mockIDataStore_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobServiceManager), "", &mockIJobServiceManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobManager), "", &mockIJobManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider), "", &mockIJobManagerAlertProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceManagerClient), "", &mockIResourceManagerClient_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::Resources::IScanDevice), "ScanDeviceService", &mockIScanDevice_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "MarkingFilter", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister), "ImagePersister", &mockIImagePersister_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "ImageProcessor", &mockIResourceService_);
    comp->setInterface(GET_INTERFACE_UID(dune::job::IResourceService), "LayoutFilter", &mockIResourceService_);
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
    comp->setInterface(GET_INTERFACE_UID(dune::job::IJobDetailsManager), "MockIJobDetailsManager",&mockDetailsManager_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints), "", &mockIJobConstraints_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules), "", &mockICopyJobDynamicConstraintRules_);
    comp->setInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "MockICopyAdapter", &mockICopyAdapter_);
    comp->setInterface(GET_INTERFACE_UID(dune::localization::ILocaleProvider),"MockILocaleProvider",&mockILocaleProvider_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "MockIExportImport",  &mockIExportImport_);
    comp->setInterface(GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase), "MockISecureFileErase",  &mockISecureFileErase_);
    comp->setInterface(GET_INTERFACE_UID(dune::print::engine::IMediaInfo), "MockIMediaInfo", &mockIMediaInfo_);
    comp->setInterface(GET_INTERFACE_UID(dune::scan::IScanConstraints), "MockScanConstraints",  &mockIScanConstraints_);

    mockILocale_ = std::make_shared<MockILocale>();

    ON_CALL(*mockILocale_, getStringIdForCsfOnly(_))
        .WillByDefault(Return(localizationId));

    ON_CALL(mockILocaleProvider_,deviceLocale())
        .WillByDefault(Return(mockILocale_));


    ON_CALL(mockIMediaInfo_, getPageBasedExtension()).WillByDefault(Return(&mockIMediaInfoPageBased_));
    ON_CALL(mockIMediaInfoPageBased_, getMediaPropertyChangedEvent()).WillByDefault(ReturnRef(mediaPropertyChangedEvent_));
    EXPECT_CALL(mockICopyAdapter_, getCopyAdapterDataChangeEvent())
        .WillOnce(ReturnRef(copyAdapterDataChangeEvent_));
    ON_CALL(mockIExportImport_, subscribeParticipant(OperationType::BACKUP_RESTORE,_,_,_,_))
        .WillByDefault(Return(ByMove(std::move(nullptr))));
    ON_CALL(mockIExportImport_, subscribeParticipant(OperationType::EXPORT_IMPORT,_,_,_,_))
        .WillByDefault(Return(ByMove(std::move(nullptr))));
    
    ON_CALL(mockIScanPipeline_, getScanMediaSize()).WillByDefault(ReturnRef(scanMediaSize_));


    GTEST_CHECKPOINTA("GivenAConnectedJobServiceStandard::SetUp -- EXIT");
}

void GivenAConnectedJobServiceStandardShortcutListEmpty::SetUpJsonFactoryQuickSets(std::string jsonName)
{
    systemServices_->setConfigurationServiceBehaviour("./testResources/JobServiceStandardConfig.fbs", "./testResources/" + jsonName);
    
    // mocking the resources folder path
    auto spm = new dune::framework::storage::path::SimplePathServicesMock();
    auto spd = new dune::framework::storage::path::SimplePathDirectory();
    spd->addPath(dune::framework::storage::path::Paths::RESOURCE_DIRECTORY, "./testResources/");
    spm->setPathDirectory(spd);
    systemServices_->setPathServices(spm);

    // initialize component
    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_.get());
}

std::unique_ptr<CollectionEasyBufferTable> GivenAConnectedJobServiceStandardShortcutListEmpty::getShortcuts(const bool pinValidateNotRequired, const shortcutFilter_t &filter)
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
                ItemEasyBufferTable shortcutCopy = ItemEasyBufferTable{shortcut};
                auxiliaryCollection.shortcuts.insertItem(shortcutCopy);
            }
        }
    }

    return std::make_unique<CollectionEasyBufferTable>(auxiliaryCollection);
}

std::unique_ptr<ItemEasyBufferTable> GivenAConnectedJobServiceStandardShortcutListEmpty::getShortcut(const dune::framework::core::Uuid &uuid,const bool pinValidateNotRequired,
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

ShortcutOperationResult GivenAConnectedJobServiceStandardShortcutListEmpty::addShortcut( const std::unique_ptr<ItemEasyBufferTable> &shortcut)
{
    ItemEasyBufferTable shortcutCopy = ItemEasyBufferTable{*shortcut.get()};

    bool result = internalShortCutCollection_.shortcuts.insertItem(shortcutCopy);

    return result ? ShortcutOperationResult::OK : ShortcutOperationResult::ERROR_GENERIC;
}

ShortcutOperationResult GivenAConnectedJobServiceStandardShortcutListEmpty::removeShortcut(const Uuid &shortcutId,const bool pinValidateNotReq,const shortcutFilter_t &filter)
{
    auto shortcut = getShortcut(shortcutId,pinValidateNotReq,filter);
    bool result = false;
    if(shortcut)
    {
        result = internalShortCutCollection_.shortcuts.removeItem(*shortcut.get());
    }

    return result ? ShortcutOperationResult::OK : ShortcutOperationResult::ERROR_GENERIC;
}

ShortcutOperationResult GivenAConnectedJobServiceStandardShortcutListEmpty::updateShortcut(std::unique_ptr<ItemEasyBufferTable>& shortcut,
                                                                                                const bool pinValidateNotReq,const shortcutFilter_t &filter)
{
    bool result = false;
    if(shortcut)
    {
        result = internalShortCutCollection_.shortcuts.updateItem(*shortcut.get());
    }

    return result ? ShortcutOperationResult::OK : ShortcutOperationResult::ERROR_GENERIC;
}

void GivenAConnectedJobServiceStandardShortcutListEmpty::executeConnectedAction()
{
    // Execution part. Connect call finish with register action
    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);

    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }    
}

void GivenAConnectedJobServiceStandardShortcutListEmpty::checkQuicksetList(std::vector<std::string> quickSetsExpected)
{
    // Apply Filter to get only factory quicksets
    shortcutFilter_t filter = shortcutFilter_t{};
    filter.factory = dune::cdm::glossary_1::FeatureEnabled::true_;
    filter.type =  dune::cdm::shortcut_1::Type::singleJob;    
    auto shortcutCollection = getShortcuts(false,filter);

    // Check that queue has the same size
    ASSERT_EQ(shortcutCollection->shortcuts.size(), quickSetsExpected.size());

    // counter to check if quicksets coincidence with id properly
    int countAcceptedQuickset = 0;

    if(shortcutCollection->shortcuts.size() > 0 && quickSetsExpected.size() > 0 && shortcutCollection->shortcuts.size() == quickSetsExpected.size())
    {
        for (auto& shortcut : shortcutCollection->collection().getMutable())
        {       
            for(auto quickSetId : quickSetsExpected)
            {
                GTEST_CHECKPOINTC("Checking next ids: shortcut id: %s, quickset id %s\n", shortcut.id.get().c_str(), quickSetId.c_str());
                // Compare id to check if was added
                if (shortcut.id.get() == quickSetId.c_str() )
                {
                    countAcceptedQuickset++;
                }
            }
        }
    }

    // Check that accepted quickset on comparison, are all counted expected
    EXPECT_EQ(quickSetsExpected.size(),countAcceptedQuickset);
}

void GivenAConnectedJobServiceStandardShortcutListEmpty::checkQuicksetList(std::string quickSetsExpected)
{
    std::vector<std::string> list{quickSetsExpected};
    checkQuicksetList(list);
}

class GivenAConnectedJobServiceStandardShortcutListEmptyParametrized : public GivenAConnectedJobServiceStandardShortcutListEmpty,
    public ::testing::WithParamInterface<GetQuickSetEncapsulation>

{
public:
    GivenAConnectedJobServiceStandardShortcutListEmptyParametrized() { GTEST_CHECKPOINTA("GivenAConnectedJobServiceStandardShortcutListEmptyParametrized::Constructor -- ENTER\n"); };

    void SetUp() override
    {
        GivenAConnectedJobServiceStandardShortcutListEmpty::SetUp();

        // Get param values
        jsonToRead_ = std::get<0>(GetParam());
        listOfQuickSetVector_ = std::get<1>(GetParam());
    }
};

TEST_P(GivenAConnectedJobServiceStandardShortcutListEmptyParametrized,WhenConnectedIsCalledWithAParametrizedConfigDefined_ThenQuicksetListIsAsExpected)
{
    // When no factory QuickSets on config
    SetUpJsonFactoryQuickSets(jsonToRead_);

    // Execute connect
    executeConnectedAction();

    // Then no quickset added on list
    checkQuicksetList(listOfQuickSetVector_);
}

INSTANTIATE_TEST_CASE_P(
    , GivenAConnectedJobServiceStandardShortcutListEmptyParametrized,
    ::testing::Values( 
//                                                Config json with names of json                                        Vector with expected id loaded on shortcut list        
                        GetQuickSetEncapsulation{ "JobServiceStandardTestData.json" ,                                   std::vector<std::string>{} },
                        GetQuickSetEncapsulation{ "JobServiceStandardTestDataOneFactoryExistent.json" ,                 std::vector<std::string>{"61b72f38-1945-11ed-bf29-87d40f139a32"} },
                        // GetQuickSetEncapsulation{ "JobServiceStandardTestDataOneFactoryNonExistent.json" ,              std::vector<std::string>{} },        // Death Test - Not Supported 
                        // GetQuickSetEncapsulation{ "JobServiceStandardTestDataOneFactoryExistentMalformed.json",         std::vector<std::string>{} },        // Death Test - Not Supported 
                        GetQuickSetEncapsulation{ "JobServiceStandardTestDataTwoFactoryExistent.json",                  std::vector<std::string>{"61b72f38-1945-11ed-bf29-87d40f139a32","34cc69d4-194f-11ed-89dc-4be3ffadc2eb"} },
                        // GetQuickSetEncapsulation{ "JobServiceStandardTestDataOneFactoryExistentOtherNotExistent.json",  std::vector<std::string>{"61b72f38-1945-11ed-bf29-87d40f139a32"} }, // Death Test - Not Supported 
                        GetQuickSetEncapsulation{ "JobServiceStandardTestDataTwoFactoryExistentWithSameName.json",      std::vector<std::string>{"61b72f38-1945-11ed-bf29-87d40f139a32"} }
                    ));

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedJobServiceStandardShortcutListWithUserQuickSet
//
///////////////////////////////////////////////////////////////////////////////
class GivenAConnectedJobServiceStandardShortcutListWithUserQuickSet : public GivenAConnectedJobServiceStandardShortcutListEmpty,
    public ::testing::WithParamInterface<GetQuickSetEncapsulation>
{
  public:
    GivenAConnectedJobServiceStandardShortcutListWithUserQuickSet() { GTEST_CHECKPOINTA("GivenAConnectedJobServiceStandardShortcutListWithUserQuickSet::Constructor -- ENTER\n"); };

    void SetUp() override;
};

void GivenAConnectedJobServiceStandardShortcutListWithUserQuickSet::SetUp()
{
    GivenAConnectedJobServiceStandardShortcutListEmpty::SetUp();

    // Create and add custom user quickset
    dune::framework::core::Uuid uuid("c93bc831-99a8-454c-b508-236fc3a2a08d");
    std::string                       id        = uuid.toString(false);
    std::string                       title     = "hello";
    dune::cdm::shortcut_1::TypeEnum   type      = dune::cdm::shortcut_1::Type::singleJob;
    dune::cdm::shortcut_1::ActionEnum action    = dune::cdm::shortcut_1::ActionEnum::Values::open;
    auto                              shortcut  = std::make_unique<dune::cdm::shortcut_1::ShortcutTable>(id, title, type, action);
    shortcut->source                            = dune::cdm::shortcut_1::Source::scan;
    shortcut->destinations                      = {{dune::cdm::shortcut_1::Destination::print}};
    addShortcut(shortcut);   

    // Get param values
    jsonToRead_ = std::get<0>(GetParam());
    listOfQuickSetVector_ = std::get<1>(GetParam());
}

TEST_P(GivenAConnectedJobServiceStandardShortcutListWithUserQuickSet,WhenConnectedIsCalledWithAParametrizedConfigDefined_ThenQuicksetListIsAsExpected)
{
    // When no factory QuickSets on config
    SetUpJsonFactoryQuickSets(jsonToRead_);

    // Execute connect
    executeConnectedAction();

    // Then no quickset added on list
    checkQuicksetList(listOfQuickSetVector_);
}

INSTANTIATE_TEST_CASE_P(
    , GivenAConnectedJobServiceStandardShortcutListWithUserQuickSet,
    ::testing::Values( 
//                                                Config json with names of json                                        Vector with expected id loaded on shortcut list        
                        GetQuickSetEncapsulation{ "JobServiceStandardTestData.json" ,                                   std::vector<std::string>{} },
                        GetQuickSetEncapsulation{ "JobServiceStandardTestDataOneFactoryExistent.json" ,                 std::vector<std::string>{"61b72f38-1945-11ed-bf29-87d40f139a32"} },
                        // GetQuickSetEncapsulation{ "JobServiceStandardTestDataOneFactoryNonExistent.json" ,              std::vector<std::string>{} },    // Death Test - Not Supported 
                        // GetQuickSetEncapsulation{ "JobServiceStandardTestDataOneFactoryExistentMalformed.json",         std::vector<std::string>{} },    // Death Test - Not Supported
                        GetQuickSetEncapsulation{ "JobServiceStandardTestDataTwoFactoryExistent.json",                  std::vector<std::string>{"61b72f38-1945-11ed-bf29-87d40f139a32","34cc69d4-194f-11ed-89dc-4be3ffadc2eb"} },
                        // GetQuickSetEncapsulation{ "JobServiceStandardTestDataOneFactoryExistentOtherNotExistent.json",  std::vector<std::string>{"61b72f38-1945-11ed-bf29-87d40f139a32"} }, // Death Test - Not Supported 
                        GetQuickSetEncapsulation{ "JobServiceStandardTestDataTwoFactoryExistentWithSameName.json",      std::vector<std::string>{"61b72f38-1945-11ed-bf29-87d40f139a32"} }
                    ));

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedJobServiceStandardShortcutListWithFactoryQuickSet
//
///////////////////////////////////////////////////////////////////////////////
class GivenAConnectedJobServiceStandardShortcutListWithFactoryQuickSet : public GivenAConnectedJobServiceStandardShortcutListEmpty,
    public ::testing::WithParamInterface<GetQuickSetEncapsulation>
{
  public:
    GivenAConnectedJobServiceStandardShortcutListWithFactoryQuickSet() { GTEST_CHECKPOINTA("GivenAConnectedJobServiceStandardShortcutListEmpty::Constructor -- ENTER\n"); };

    void SetUp() override;
};

void GivenAConnectedJobServiceStandardShortcutListWithFactoryQuickSet::SetUp()
{
    GivenAConnectedJobServiceStandardShortcutListEmpty::SetUp();

    // Create an add custom factory quickset
    dune::framework::core::Uuid uuid("61b72f38-1945-11ed-bf29-87d40f139a32");
    std::string                       id        = uuid.toString(false);
    std::string                       title     = "hello";
    dune::cdm::shortcut_1::TypeEnum   type      = dune::cdm::shortcut_1::Type::singleJob;
    dune::cdm::shortcut_1::ActionEnum action    = dune::cdm::shortcut_1::ActionEnum::Values::open;
    auto                              shortcut  = std::make_unique<dune::cdm::shortcut_1::ShortcutTable>(id, title, type, action);
    shortcut->source                            = dune::cdm::shortcut_1::Source::scan;
    shortcut->destinations                      = {{dune::cdm::shortcut_1::Destination::print}};
    shortcut->factory                           = dune::cdm::glossary_1::FeatureEnabled::true_;
    shortcut->readOnly                          = dune::cdm::glossary_1::FeatureEnabled::true_;
    shortcut->copyAllowed                       = dune::cdm::glossary_1::FeatureEnabled::true_;
    shortcut->origin                            = dune::cdm::shortcut_1::Origin::device;
    addShortcut(shortcut);  

    // Get param values
    jsonToRead_ = std::get<0>(GetParam());
    listOfQuickSetVector_ = std::get<1>(GetParam()); 
}

TEST_P(GivenAConnectedJobServiceStandardShortcutListWithFactoryQuickSet,WhenConnectedIsCalledWithAParametrizedConfigDefined_ThenQuicksetListIsAsExpected)
{
    // When no factory QuickSets on config
    SetUpJsonFactoryQuickSets(jsonToRead_);

    // Execute connect
    executeConnectedAction();

    // Then no quickset added on list
    checkQuicksetList(listOfQuickSetVector_);
}

INSTANTIATE_TEST_CASE_P(
    , GivenAConnectedJobServiceStandardShortcutListWithFactoryQuickSet,
    ::testing::Values( 
//                                                Config json with names of json                                        Vector with expected id loaded on shortcut list        
                        // GetQuickSetEncapsulation{ "JobServiceStandardTestData.json" ,                                   std::vector<std::string>{} },                                                // Unsupported for the moment remove of older quicksets
                        GetQuickSetEncapsulation{ "JobServiceStandardTestDataOneFactoryExistent.json" ,                 std::vector<std::string>{"61b72f38-1945-11ed-bf29-87d40f139a32"} },
                        // GetQuickSetEncapsulation{ "JobServiceStandardTestDataOneFactoryExistentMalformed.json",         std::vector<std::string>{} },                                                // Unsupported for the moment remove of older quicksets
                        // GetQuickSetEncapsulation{ "JobServiceStandardTestDataOneFactorySecondExistent.json" ,                 std::vector<std::string>{"34cc69d4-194f-11ed-89dc-4be3ffadc2eb"} },    // Unsupported for the moment remove of older quicksets
                        // GetQuickSetEncapsulation{ "JobServiceStandardTestDataOneFactoryNonExistent.json" ,              std::vector<std::string>{} },                                                // Unsupported for the moment remove of older quicksets
                        GetQuickSetEncapsulation{ "JobServiceStandardTestDataTwoFactoryExistent.json",                  std::vector<std::string>{"61b72f38-1945-11ed-bf29-87d40f139a32","34cc69d4-194f-11ed-89dc-4be3ffadc2eb"} },
                        // GetQuickSetEncapsulation{ "JobServiceStandardTestDataOneFactoryExistentOtherNotExistent.json",  std::vector<std::string>{"61b72f38-1945-11ed-bf29-87d40f139a32"} },
                        // GetQuickSetEncapsulation{ "JobServiceStandardTestDataOneFactorySecondExistentOtherNotExistent.json",  std::vector<std::string>{"34cc69d4-194f-11ed-89dc-4be3ffadc2eb"} },    // Unsupported for the moment remove of older quicksets
                        GetQuickSetEncapsulation{ "JobServiceStandardTestDataTwoFactoryExistentWithSameName.json",      std::vector<std::string>{"61b72f38-1945-11ed-bf29-87d40f139a32"} }
                        // GetQuickSetEncapsulation{ "JobServiceStandardTestDataTwoFactorySecondExistentWithSameName.json",      std::vector<std::string>{"34cc69d4-194f-11ed-89dc-4be3ffadc2eb"} }     // Unsupported for the moment remove of older quicksets
                    ));

