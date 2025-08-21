/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAdapterStandardGtestMain.cpp
 * @date   Wed, 27 Jul 2022 19:48:04 -0600
 * @brief  This is a CDM Adapter component defining the Copy Service
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyAdapterStandard.h"

#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include "TestSystemServices.h"
#include "GTestConfigHelper.h"

#include "IResetManager.h"
#include "Fs.h"

#include "MockIMicroServiceFactory.h"
#include "MockIDataStore.h"
#include "MockICopyAdapter.h"
#include "MockILocaleProvider.h"
#include "MockIExportImport.h"
#include "MockIResetManager.h"

using IMicroService         = dune::ws::cdm::framework::IMicroService;
using IResourceDefinition   = dune::ws::cdm::framework::IResourceDefinition;
using IResourceProvider     = dune::ws::cdm::IResourceProvider;
using MockIMicroServiceFactory = dune::ws::cdm::framework::MockIMicroServiceFactory;
using CopyAdapterStandard   = dune::copy::cdm::CopyAdapterStandard;
using TestSystemServices    = dune::framework::component::TestingUtil::TestSystemServices;
using IComponent            = dune::framework::component::IComponent;
using IComponentManager     = dune::framework::component::IComponentManager;
using SystemServices        = dune::framework::component::SystemServices;
using SysTrace              = dune::framework::core::dbg::SysTrace;
using CheckpointLevel       = SysTrace::CheckpointLevel;
using MockIDataStore        = dune::framework::data::MockIDataStore;
using FeatureEnabled        = dune::cdm::glossary_1::FeatureEnabled;
using BackupOperationResult = dune::framework::data::backup::OperationResult;
using OperationDescription = dune::framework::data::backup::IExportImport::OperationDescription;
using FileInfoCollection   = dune::framework::data::backup::IExportImport::FileInfoCollection;
using IdentificationData   = dune::framework::data::backup::IExportImport::IdentificationData;
using path = dune::framework::storage::fs::path; // dune::framework::storage::fs;
using MockICopyAdapter          = dune::copy::cdm::MockICopyAdapter;
using MockILocaleProvider   = dune::localization::MockILocaleProvider;
using MockIExportImport     = dune::framework::data::backup::MockIExportImport;

using GTestConfigHelper     = dune::framework::core::gtest::GTestConfigHelper;

using ::testing::_;
using ::testing::Return;
using ::testing::ByMove;

GTestConfigHelper testConfigOptions_;


int main(int argc, char  *argv[])
{
    // run google tests
    //
    std::cout << "Main:  " << argv[0] << std::endl;

    testConfigOptions_.parse(argc, argv);
    testConfigOptions_.Configure();

    ::testing::FLAGS_gmock_catch_leaked_mocks = true;
    ::testing::FLAGS_gmock_verbose = "error";

    ::testing::InitGoogleTest(&argc, argv);

    return RUN_ALL_TESTS();
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenANewCopyAdapterStandard : public ::testing::Test
//
///////////////////////////////////////////////////////////////////////////////

class GivenANewCopyAdapterStandard : virtual public ::testing::Test
{
  public:

    GivenANewCopyAdapterStandard() : component_(nullptr), systemServices_(nullptr), componentManager_(nullptr) {};

    virtual void SetUp() override;

    virtual void TearDown() override;

  protected:

    dune::copy::cdm::CopyAdapterStandard            * component_;
    TestSystemServices                              * systemServices_;
    dune::framework::component::IComponentManager   * componentManager_;
    std::shared_ptr<MockIMicroServiceFactory>         mockMicroServiceFactory_{std::make_shared<MockIMicroServiceFactory>()};
    std::shared_ptr<MockIDataStore>                   mockIDataStore_{std::make_shared<MockIDataStore>()};
    std::shared_ptr<MockILocaleProvider>              mockILocaleProvider_{std::make_shared<MockILocaleProvider>()};
    std::shared_ptr<MockIExportImport>                mockIExportImport_{std::make_shared<MockIExportImport>()};
};

void GivenANewCopyAdapterStandard::SetUp()
{
    systemServices_ = new TestSystemServices();
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyAdapterStandardConfig.fbs", "./testResources/CopyAdapterStandardTestData.json");

    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyAdapterStandardConfig.fbs", 
                                                "./testResources/CopyAdapterStandardTestData.json");
    component_ = new CopyAdapterStandard("myInstance");
    ASSERT_TRUE(component_ != nullptr);
}

void GivenANewCopyAdapterStandard::TearDown()
{
    delete component_;
    delete systemServices_;
}

TEST_F(GivenANewCopyAdapterStandard, WhenGetComponentFlavorUidIsCalled_ThenComponentFlavorUidIsReturned)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    dune::framework::component::ComponentFlavorUid flavorUid = comp->getComponentFlavorUid();

    EXPECT_EQ(flavorUid, GET_MODULE_UID(CopyAdapterStandard));
}

TEST_F(GivenANewCopyAdapterStandard, WhenSetInterfaceIsCalled_ThenInterfaceIsSet)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->setInterface(GET_INTERFACE_UID(dune::localization::ILocaleProvider), "",
                   (void*)mockILocaleProvider_.get());
    
    ASSERT_TRUE(true);
}

TEST_F(GivenANewCopyAdapterStandard, WhenGetInterfaceIsCalled_ThenInterfaceIsReturned)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    void * interface = comp->getInterface(GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter), "");

    EXPECT_TRUE(interface != nullptr);
}

TEST_F(GivenANewCopyAdapterStandard, WhenInitializeIsCalled_TheComponentGetsInitialized)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_);

    ASSERT_TRUE(true);
}

TEST_F(GivenANewCopyAdapterStandard, WhenTheConnectSequenceIsCalled_TheComponentGetsConnected)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required
    component_->setInterface(GET_INTERFACE_UID(dune::ws::cdm::framework::IMicroServiceFactory), "",
                             (void*)mockMicroServiceFactory_.get());
    component_->setInterface(GET_INTERFACE_UID(dune::framework::data::backup::IExportImport), "",
                            (void*)mockIExportImport_.get());

    std::shared_ptr<IMicroService> svc =
        std::make_shared<dune::ws::cdm::framework::MicroServiceFactoryTestHelper::FakeService>();
    EXPECT_CALL(*(mockMicroServiceFactory_.get()), createMicroService(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Return(std::weak_ptr<IMicroService>(svc)));

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    ASSERT_TRUE(true);

    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::_undefined_);
    EXPECT_EQ(component_->getColorCopyEnabled(), true);
    EXPECT_EQ(component_->getCopyEnabled(), true);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::_undefined_);
}

TEST_F(GivenANewCopyAdapterStandard, ExportAndImportConfigurationDataTest) {
    
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // Create test data for import
    OperationDescription importExportDescription;
    IdentificationData identificationData;
    std::string testFilePath("./testResources/exportedCopyConfigData.json");
    const std::string contentId = "CopyEnableSettings"; 
    std::string        version = "1.0";
    const std::string  CONTENT_FILE_TAG("CopyEnableSettings");
    const path     CONTENT_FILE_PATH("./testResources/exportedCopyConfigData.json");
    const std::string  CONTENT_FILE_STR(std::string("test file at ") + CONTENT_FILE_PATH.string());
    const ExtendedInfo CONTENT_FILE_EXT = { {"k0","v0"}, {"k1","v1"} };    
      
    
    FileInfoCollection filesToExportImport = {
        { CONTENT_FILE_TAG, testFilePath, false, false, CONTENT_FILE_EXT }
    };
    
    component_->setInterface(GET_INTERFACE_UID(dune::ws::cdm::framework::IMicroServiceFactory), "",
                             (void*)mockMicroServiceFactory_.get());
    component_->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "",
                             (void*)mockIDataStore_.get());

    // Call the exportData function
    BackupOperationResult exportResult = component_->exportData(importExportDescription, contentId, version, filesToExportImport);

    // Perform assertions on the export result
    EXPECT_EQ(exportResult, BackupOperationResult::SUCCESS);
   
    // Call the importData function
    BackupOperationResult importResult = component_->importData(importExportDescription, identificationData, contentId, version, filesToExportImport);

    // Assert the import result
    EXPECT_EQ(importResult, BackupOperationResult::SUCCESS);
}

TEST_F(GivenANewCopyAdapterStandard, ExportConfigurationDataTest) {
    
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // Create test data
    OperationDescription exportDescription;
    std::string testFilePath("./testResources/exportedCopyConfigData.json");
    const std::string contentId = "CopyEnableSettings"; 
    std::string        version = "1.0";
    const std::string  CONTENT_FILE_TAG("CopyEnableSettings");
    const path     CONTENT_FILE_PATH("./testResources/exportedCopyConfigData.json");
    const std::string  CONTENT_FILE_STR(std::string("test file at ") + CONTENT_FILE_PATH.string());
    const ExtendedInfo CONTENT_FILE_EXT = { {"k0","v0"}, {"k1","v1"} };    
      
    
    FileInfoCollection filesToExport = {
        { CONTENT_FILE_TAG, testFilePath, false, false, CONTENT_FILE_EXT }
    };
    
    //If wrong contentId is passed then check for return value
    BackupOperationResult result = component_->exportData(exportDescription, "WrongContentId", version, filesToExport);
    EXPECT_EQ(result, BackupOperationResult::ERROR_UNKNOWN_CONTENTID);
    
    // Call the exportData function
    BackupOperationResult exportResult = component_->exportData(exportDescription, contentId, version, filesToExport);

    // Perform assertions on the export result
    EXPECT_EQ(exportResult, BackupOperationResult::SUCCESS);
}

TEST_F(GivenANewCopyAdapterStandard, ImportConfigurationDataTest) {
    
    IComponent * comp = static_cast<IComponent*>(component_);

    MockICopyAdapter                            mockCopyAdapter_;
    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // Create test data
    OperationDescription importDescription;
    IdentificationData identificationData;
    std::string testFilePath("./testResources/exportedCopyConfigData.json");
    const std::string contentId = "CopyEnableSettings"; 
    std::string        version = "1.0";
    const std::string  CONTENT_FILE_TAG("CopyEnableSettings");
    const path     CONTENT_FILE_PATH("./testResources/exportedCopyConfigData.json");
    const std::string  CONTENT_FILE_STR(std::string("test file at ") + CONTENT_FILE_PATH.string());
    const ExtendedInfo CONTENT_FILE_EXT = { {"k0","v0"}, {"k1","v1"} };    
      
    
    FileInfoCollection filesToImport = {
        { CONTENT_FILE_TAG, testFilePath, false, false, CONTENT_FILE_EXT }
    };

    component_->setInterface(GET_INTERFACE_UID(dune::ws::cdm::framework::IMicroServiceFactory), "",
                             (void*)mockMicroServiceFactory_.get());
    component_->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "",
                             (void*)mockIDataStore_.get());

    dune::ws::cdm::OperationResponseMetadataT responseMetadata;

    importDescription.operationType = dune::framework::data::backup::OperationType::BACKUP_RESTORE;

    //If wrong contentId is passed then check for return value
    BackupOperationResult result = component_->importData(importDescription, identificationData, "wrongContentId", version, filesToImport);
    EXPECT_EQ(result, BackupOperationResult::ERROR_UNKNOWN_CONTENTID);
    
    // Call the importData function
    BackupOperationResult importResult = component_->importData(importDescription, identificationData, contentId, version, filesToImport);

    // Assert the expected result
    EXPECT_EQ(importResult, BackupOperationResult::SUCCESS);
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyAdapterStandard : Do here tests of public api
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyAdapterStandard :public GivenANewCopyAdapterStandard
{
  public:

    GivenAConnectedCopyAdapterStandard() {};

    virtual void SetUp() override;

    virtual void TearDown() override;
};

void GivenAConnectedCopyAdapterStandard::SetUp()
{
    GivenANewCopyAdapterStandard::SetUp();

    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required
    component_->setInterface(GET_INTERFACE_UID(dune::ws::cdm::framework::IMicroServiceFactory), "",
                             (void*)mockMicroServiceFactory_.get());

    std::shared_ptr<IMicroService> svc =
        std::make_shared<dune::ws::cdm::framework::MicroServiceFactoryTestHelper::FakeService>();
    EXPECT_CALL(*(mockMicroServiceFactory_.get()), createMicroService(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Return(std::weak_ptr<IMicroService>(svc)));

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

}

void GivenAConnectedCopyAdapterStandard::TearDown()
{
    GivenANewCopyAdapterStandard::TearDown();
}

TEST_F(GivenANewCopyAdapterStandard,WheGetCopyEnabledIsCalled_ThenCopyEnabledIsReturned)
{
    EXPECT_EQ(component_->getCopyEnabled(), true);
}

TEST_F(GivenANewCopyAdapterStandard, WhenSetCopyEnabledIsCalled_ThenCopyEnabledIsSet)
{
    component_->setCopyEnabled(FeatureEnabled::false_);
    EXPECT_EQ(component_->getCopyEnabled(), false);
}

TEST_F(GivenANewCopyAdapterStandard, WhenGetColorCopyEnabledIsCalled_ThenColorCopyEnabledIsReturned)
{
    EXPECT_EQ(component_->getColorCopyEnabled(), true);
}

TEST_F(GivenANewCopyAdapterStandard, WhenSetColorCopyEnabledIsCalled_ThenColorCopyEnabledIsSet)
{
    component_->setColorCopyEnabled(FeatureEnabled::false_);
    EXPECT_EQ(component_->getColorCopyEnabled(), false);
}

TEST_F(GivenANewCopyAdapterStandard, WhenGetCopyModeIsCalled_ThenCopyModeIsReturned)
{
    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::_undefined_);
}

TEST_F(GivenANewCopyAdapterStandard, WhenSetCopyModeIsCalled_ThenCopyModeIsSetAndInterruptStillUndefined)
{
    component_->setCopyMode(dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::_undefined_);
}

TEST_F(GivenANewCopyAdapterStandard, WhenGetInterruptModeIsCalled_ThenInterruptModeIsReturned)
{
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::_undefined_);
}

TEST_F(GivenANewCopyAdapterStandard, WhenSetInterruptModeIsCalled_ThenInterruptModeIsSet)
{
    component_->setInterruptMode(FeatureEnabled::false_);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::false_);
}

class GivenResetLevelParametrizedForCopyAdapter
    : virtual public ::testing::Test,
    public ::testing::WithParamInterface<dune::framework::data::resets::ResetLevel>
{
public:
    GivenResetLevelParametrizedForCopyAdapter() {};

    virtual void SetUp() override { resetMocked_ = GetParam(); };

    virtual void TearDown() override {};

    dune::framework::data::resets::ResetLevel resetMocked_{dune::framework::data::resets::ResetLevel::NONE};
};

const std::vector<dune::framework::data::resets::ResetLevel> GivenResetLevelParametrizedForCopyAdapterResetLevels_ = {
    dune::framework::data::resets::ResetLevel::USER_SETTINGS_RESET,
    dune::framework::data::resets::ResetLevel::USER_DATA_RESET,
    dune::framework::data::resets::ResetLevel::FACTORY_DATA_RESET,
    dune::framework::data::resets::ResetLevel::FULL_FACTORY_DATA_RESET
};

///////////////////////////////////////////////////////////////////////////////
//
// class GivenACopyAdapterStandardWithPrintAfterScanningByDefault
//
///////////////////////////////////////////////////////////////////////////////

class GivenACopyAdapterStandardWithPrintAfterScanningByDefault :public GivenANewCopyAdapterStandard
{
  public:

    GivenACopyAdapterStandardWithPrintAfterScanningByDefault() {};

    virtual void SetUp() override;

    virtual void TearDown() override;

    dune::framework::core::Uuid copyConfigurationUuid{Uuid("24eb349c-11ec-11ed-861d-0242ac120002")};
};

void GivenACopyAdapterStandardWithPrintAfterScanningByDefault::SetUp()
{
    GivenANewCopyAdapterStandard::SetUp();

    IComponent * comp = static_cast<IComponent*>(component_);

    //Set print after scanning as default copy mode
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyAdapterStandardConfig.fbs", "./testResources/PrintAfterScanningTestData.json");

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required
    component_->setInterface(GET_INTERFACE_UID(dune::ws::cdm::framework::IMicroServiceFactory), "",
                             (void*)mockMicroServiceFactory_.get());
    component_->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "",
                             (void*)mockIDataStore_.get());
}

void GivenACopyAdapterStandardWithPrintAfterScanningByDefault::TearDown()
{
    GivenANewCopyAdapterStandard::TearDown();
}

TEST_F(GivenACopyAdapterStandardWithPrintAfterScanningByDefault, WhenTheConnectSequenceIsCalled_ThenCopyConfigurationSettingsHaveDefaultValues)
{
    ON_CALL(*mockIDataStore_, find(copyConfigurationUuid)).WillByDefault(Return(ByMove(std::pair<bool, dune::framework::data::DataObject>(
            false, dune::framework::data::DataObject({{nullptr, 0x200}, {0,0,0,0}, dune::framework::core::Uuid()})))));

    std::shared_ptr<IMicroService> svc =
    std::make_shared<dune::ws::cdm::framework::MicroServiceFactoryTestHelper::FakeService>();
    EXPECT_CALL(*(mockMicroServiceFactory_.get()), createMicroService(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Return(std::weak_ptr<IMicroService>(svc)));

    std::future<void> asyncCompletion;
    static_cast<IComponent*>(component_)->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    //Check default values
    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    EXPECT_EQ(component_->getColorCopyEnabled(), true);
    EXPECT_EQ(component_->getCopyEnabled(), true);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::_undefined_);
}

class GivenACopyAdapterStandardWithPrintAfterScanningByDefaultAndResetLevelParametrized :
    public GivenACopyAdapterStandardWithPrintAfterScanningByDefault,
    public GivenResetLevelParametrizedForCopyAdapter
{
public:
    GivenACopyAdapterStandardWithPrintAfterScanningByDefaultAndResetLevelParametrized(){};
    virtual void SetUp() override;
    virtual void TearDown() override;
};

void GivenACopyAdapterStandardWithPrintAfterScanningByDefaultAndResetLevelParametrized::SetUp()
{
    GivenACopyAdapterStandardWithPrintAfterScanningByDefault::SetUp();
    GivenResetLevelParametrizedForCopyAdapter::SetUp();

    ON_CALL(*mockIDataStore_, find(copyConfigurationUuid)).WillByDefault(Return(ByMove(std::pair<bool, dune::framework::data::DataObject>(
            false, dune::framework::data::DataObject({{nullptr, 0x200}, {0,0,0,0}, dune::framework::core::Uuid()})))));

    std::shared_ptr<IMicroService> svc =
    std::make_shared<dune::ws::cdm::framework::MicroServiceFactoryTestHelper::FakeService>();
    EXPECT_CALL(*(mockMicroServiceFactory_.get()), createMicroService(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Return(std::weak_ptr<IMicroService>(svc)));

    std::future<void> asyncCompletion;
    static_cast<IComponent*>(component_)->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    //Check default values
    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    EXPECT_EQ(component_->getColorCopyEnabled(), true);
    EXPECT_EQ(component_->getCopyEnabled(), true);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::_undefined_); 

    // Force update internal values with non default values
    component_->setCopyMode(dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    ASSERT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    ASSERT_EQ(component_->getInterruptMode(), FeatureEnabled::_undefined_);

    ON_CALL(*(systemServices_->getMockIResetManager()),getCurrentLevel()).WillByDefault(testing::Return(resetMocked_));
}

void GivenACopyAdapterStandardWithPrintAfterScanningByDefaultAndResetLevelParametrized::TearDown()
{
    GivenACopyAdapterStandardWithPrintAfterScanningByDefault::TearDown(); 
};

TEST_P(GivenACopyAdapterStandardWithPrintAfterScanningByDefaultAndResetLevelParametrized, WhenCheckResetIsCalled_ThenValuesResetToExpected)
{
    EXPECT_CALL(*mockIDataStore_, insert_or_replace_ex(_,_,_)).Times(1).WillRepeatedly(testing::Return(true));
    component_->checkIfResetDataIsNeeded();

    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    EXPECT_EQ(component_->getColorCopyEnabled(), true);
    EXPECT_EQ(component_->getCopyEnabled(), true);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::_undefined_);
}

INSTANTIATE_TEST_CASE_P(, GivenACopyAdapterStandardWithPrintAfterScanningByDefaultAndResetLevelParametrized,
    ::testing::ValuesIn(GivenResetLevelParametrizedForCopyAdapterResetLevels_));

///////////////////////////////////////////////////////////////////////////////
//
// class GivenACopyAdapterStandardWithPrintWhileScanningByDefault
//
///////////////////////////////////////////////////////////////////////////////

class GivenACopyAdapterStandardWithPrintWhileScanningByDefault :public GivenANewCopyAdapterStandard
{
  public:

    GivenACopyAdapterStandardWithPrintWhileScanningByDefault() {};

    virtual void SetUp() override;

    virtual void TearDown() override;

    dune::framework::core::Uuid copyConfigurationUuid{Uuid("24eb349c-11ec-11ed-861d-0242ac120002")};
};

void GivenACopyAdapterStandardWithPrintWhileScanningByDefault::SetUp()
{
    GivenANewCopyAdapterStandard::SetUp();

    IComponent * comp = static_cast<IComponent*>(component_);

    //Set print after scanning as default copy mode
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyAdapterStandardConfig.fbs", "./testResources/PrintWhileScanningTestData.json");

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required
    component_->setInterface(GET_INTERFACE_UID(dune::ws::cdm::framework::IMicroServiceFactory), "",
                             (void*)mockMicroServiceFactory_.get());
    component_->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "",
                             (void*)mockIDataStore_.get());
}

void GivenACopyAdapterStandardWithPrintWhileScanningByDefault::TearDown()
{
    GivenANewCopyAdapterStandard::TearDown();
}

TEST_F(GivenACopyAdapterStandardWithPrintWhileScanningByDefault, WhenTheConnectSequenceIsCalled_ThenCopyConfigurationSettingsHaveDefaultValues)
{
    ON_CALL(*mockIDataStore_, find(copyConfigurationUuid)).WillByDefault(Return(ByMove(std::pair<bool, dune::framework::data::DataObject>(
            false, dune::framework::data::DataObject({{nullptr, 0x200}, {0,0,0,0}, dune::framework::core::Uuid()})))));

    std::shared_ptr<IMicroService> svc =
    std::make_shared<dune::ws::cdm::framework::MicroServiceFactoryTestHelper::FakeService>();
    EXPECT_CALL(*(mockMicroServiceFactory_.get()), createMicroService(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Return(std::weak_ptr<IMicroService>(svc)));

    std::future<void> asyncCompletion;
    static_cast<IComponent*>(component_)->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    //Check default values
    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    EXPECT_EQ(component_->getColorCopyEnabled(), true);
    EXPECT_EQ(component_->getCopyEnabled(), true);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::_undefined_);
}

class GivenACopyAdapterStandardWithPrintWhileScanningByDefaultAndResetLevelParametrized :
    public GivenACopyAdapterStandardWithPrintWhileScanningByDefault,
    public GivenResetLevelParametrizedForCopyAdapter
{
public:
    GivenACopyAdapterStandardWithPrintWhileScanningByDefaultAndResetLevelParametrized(){};
    virtual void SetUp() override;
    virtual void TearDown() override;
};

void GivenACopyAdapterStandardWithPrintWhileScanningByDefaultAndResetLevelParametrized::SetUp()
{
    GivenACopyAdapterStandardWithPrintWhileScanningByDefault::SetUp();
    GivenResetLevelParametrizedForCopyAdapter::SetUp();

    ON_CALL(*mockIDataStore_, find(copyConfigurationUuid)).WillByDefault(Return(ByMove(std::pair<bool, dune::framework::data::DataObject>(
            false, dune::framework::data::DataObject({{nullptr, 0x200}, {0,0,0,0}, dune::framework::core::Uuid()})))));

    std::shared_ptr<IMicroService> svc =
    std::make_shared<dune::ws::cdm::framework::MicroServiceFactoryTestHelper::FakeService>();
    EXPECT_CALL(*(mockMicroServiceFactory_.get()), createMicroService(testing::_))
        .Times(1)
        .WillRepeatedly(testing::Return(std::weak_ptr<IMicroService>(svc)));

    std::future<void> asyncCompletion;
    static_cast<IComponent*>(component_)->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

    //Check default values
    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    EXPECT_EQ(component_->getColorCopyEnabled(), true);
    EXPECT_EQ(component_->getCopyEnabled(), true);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::_undefined_);    

    // Force update internal values with non default values
    component_->setCopyMode(dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    ASSERT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    ASSERT_EQ(component_->getInterruptMode(), FeatureEnabled::_undefined_);

    ON_CALL(*(systemServices_->getMockIResetManager()),getCurrentLevel()).WillByDefault(testing::Return(resetMocked_));
}

void GivenACopyAdapterStandardWithPrintWhileScanningByDefaultAndResetLevelParametrized::TearDown()
{
    GivenACopyAdapterStandardWithPrintWhileScanningByDefault::TearDown(); 
};

TEST_P(GivenACopyAdapterStandardWithPrintWhileScanningByDefaultAndResetLevelParametrized, WhenCheckResetIsCalled_ThenValuesResetToExpected)
{
    EXPECT_CALL(*mockIDataStore_, insert_or_replace_ex(_,_,_)).Times(1).WillRepeatedly(testing::Return(true));
    component_->checkIfResetDataIsNeeded();

    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    EXPECT_EQ(component_->getColorCopyEnabled(), true);
    EXPECT_EQ(component_->getCopyEnabled(), true);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::_undefined_);
}

INSTANTIATE_TEST_CASE_P(, GivenACopyAdapterStandardWithPrintWhileScanningByDefaultAndResetLevelParametrized,
    ::testing::ValuesIn(GivenResetLevelParametrizedForCopyAdapterResetLevels_));

///////////////////////////////////////////////////////////////////////////////
//
// class GivenACopyAdapterStandardWithInterruptSupported
//
///////////////////////////////////////////////////////////////////////////////

class GivenACopyAdapterStandardWithInterruptSupported :public GivenANewCopyAdapterStandard
{
  public:

    GivenACopyAdapterStandardWithInterruptSupported() {};

    virtual void SetUp() override;

    virtual void TearDown() override;

    dune::framework::core::Uuid copyConfigurationUuid{Uuid("24eb349c-11ec-11ed-861d-0242ac120002")};
};

void GivenACopyAdapterStandardWithInterruptSupported::SetUp()
{
    GivenANewCopyAdapterStandard::SetUp();

    std::shared_ptr<IMicroService> svc =
        std::make_shared<dune::ws::cdm::framework::MicroServiceFactoryTestHelper::FakeService>();

    ON_CALL(*mockIDataStore_, find(copyConfigurationUuid)).WillByDefault(Return(ByMove(std::pair<bool, dune::framework::data::DataObject>(
            false, dune::framework::data::DataObject({{nullptr, 0x200}, {0,0,0,0}, dune::framework::core::Uuid()})))));    

    ON_CALL(*(mockMicroServiceFactory_.get()), createMicroService(testing::_))        
        .WillByDefault(testing::Return(std::weak_ptr<IMicroService>(svc)));

    IComponent * comp = static_cast<IComponent*>(component_);

    //Set print after scanning as default copy mode
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyAdapterStandardConfig.fbs", "./testResources/AllowInterruptTestData.json");

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required
    component_->setInterface(GET_INTERFACE_UID(dune::ws::cdm::framework::IMicroServiceFactory), "",
                             (void*)mockMicroServiceFactory_.get());
    component_->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "",
                             (void*)mockIDataStore_.get());

    std::future<void> asyncCompletion;
    static_cast<IComponent*>(component_)->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }                             
}

void GivenACopyAdapterStandardWithInterruptSupported::TearDown()
{
    GivenANewCopyAdapterStandard::TearDown();
}

TEST_F(GivenACopyAdapterStandardWithInterruptSupported, WhenGetInterruptModeIsCalled_ThenInterruptModeIsReturned)
{
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::false_);
}

TEST_F(GivenACopyAdapterStandardWithInterruptSupported, WhenSetInterruptModeIsCalled_ThenInterruptModeIsSet)
{
    component_->setInterruptMode(FeatureEnabled::true_);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::true_);
}

TEST_F(GivenACopyAdapterStandardWithInterruptSupported, WhenSetCopyModeIsCalledAsPrintAfterScanning_ThenCopyModeIsSetAndInterruptIsFalse)
{
    component_->setCopyMode(dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::false_);
}

TEST_F(GivenACopyAdapterStandardWithInterruptSupported, WhenSetCopyModeIsCalledAsPrintWhileScanning_ThenCopyModeIsSetAndInterruptIsTrue)
{
    component_->setCopyMode(dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::true_);
}

class GivenACopyAdapterStandardWithInterruptSupportedAndResetLevelParametrized :
    public GivenACopyAdapterStandardWithInterruptSupported,
    public GivenResetLevelParametrizedForCopyAdapter
{
public:
    GivenACopyAdapterStandardWithInterruptSupportedAndResetLevelParametrized(){};
    virtual void SetUp() override;

    virtual void TearDown() override;
};

void GivenACopyAdapterStandardWithInterruptSupportedAndResetLevelParametrized::SetUp()
{
    GivenACopyAdapterStandardWithInterruptSupported::SetUp();
    GivenResetLevelParametrizedForCopyAdapter::SetUp();

    // Force update internal values with non default values
    component_->setCopyMode(dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    ASSERT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    ASSERT_EQ(component_->getInterruptMode(), FeatureEnabled::true_);

    ON_CALL(*(systemServices_->getMockIResetManager()),getCurrentLevel()).WillByDefault(testing::Return(resetMocked_));
}

void GivenACopyAdapterStandardWithInterruptSupportedAndResetLevelParametrized::TearDown()
{
    GivenACopyAdapterStandardWithInterruptSupported::TearDown(); 
};

TEST_P(GivenACopyAdapterStandardWithInterruptSupportedAndResetLevelParametrized, WhenCheckResetIsCalled_ThenValuesResetToExpected)
{
    EXPECT_CALL(*mockIDataStore_, insert_or_replace_ex(_,_,_)).Times(1).WillRepeatedly(testing::Return(true));
    component_->checkIfResetDataIsNeeded();

    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::_undefined_);
    EXPECT_EQ(component_->getColorCopyEnabled(), true);
    EXPECT_EQ(component_->getCopyEnabled(), true);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::false_);
}

INSTANTIATE_TEST_CASE_P(, GivenACopyAdapterStandardWithInterruptSupportedAndResetLevelParametrized,
    ::testing::ValuesIn(GivenResetLevelParametrizedForCopyAdapterResetLevels_));

///////////////////////////////////////////////////////////////////////////////
//
// class GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupported
//
///////////////////////////////////////////////////////////////////////////////

class GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupported :public GivenANewCopyAdapterStandard
{
  public:

    GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupported() {};

    virtual void SetUp() override;

    virtual void TearDown() override;

    dune::framework::core::Uuid copyConfigurationUuid{Uuid("24eb349c-11ec-11ed-861d-0242ac120002")};
};

void GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupported::SetUp()
{
    GivenANewCopyAdapterStandard::SetUp();

    std::shared_ptr<IMicroService> svc =
        std::make_shared<dune::ws::cdm::framework::MicroServiceFactoryTestHelper::FakeService>();

    ON_CALL(*mockIDataStore_, find(copyConfigurationUuid)).WillByDefault(Return(ByMove(std::pair<bool, dune::framework::data::DataObject>(
            false, dune::framework::data::DataObject({{nullptr, 0x200}, {0,0,0,0}, dune::framework::core::Uuid()})))));    

    ON_CALL(*(mockMicroServiceFactory_.get()), createMicroService(testing::_))        
        .WillByDefault(testing::Return(std::weak_ptr<IMicroService>(svc)));

    IComponent * comp = static_cast<IComponent*>(component_);

    //Set print after scanning as default copy mode
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyAdapterStandardConfig.fbs", "./testResources/PrintAfterScanAllowInterruptTestData.json");

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required
    component_->setInterface(GET_INTERFACE_UID(dune::ws::cdm::framework::IMicroServiceFactory), "",
                             (void*)mockMicroServiceFactory_.get());
    component_->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "",
                             (void*)mockIDataStore_.get());

    std::future<void> asyncCompletion;
    static_cast<IComponent*>(component_)->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }                             
}

void GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupported::TearDown()
{
    GivenANewCopyAdapterStandard::TearDown();
}

TEST_F(GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupported, WhenGetInterruptModeIsCalled_ThenInterruptModeIsReturned)
{
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::false_);
}

TEST_F(GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupported, WhenSetInterruptModeIsCalled_ThenInterruptModeIsSet)
{
    component_->setInterruptMode(FeatureEnabled::true_);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::true_);
}

TEST_F(GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupported, WhenSetCopyModeIsCalledAsPrintAfterScanning_ThenCopyModeIsSetAndInterruptIsFalse)
{
    component_->setCopyMode(dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::false_);
}

TEST_F(GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupported, WhenSetCopyModeIsCalledAsPrintWhileScanning_ThenCopyModeIsSetAndInterruptIsTrue)
{
    component_->setCopyMode(dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::true_);
}

class GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupportedAndResetLevelParametrized :
    public GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupported,
    public GivenResetLevelParametrizedForCopyAdapter
{
public:
    GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupportedAndResetLevelParametrized(){};
    virtual void SetUp() override;

    virtual void TearDown() override;
};

void GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupportedAndResetLevelParametrized::SetUp()
{
    GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupported::SetUp();
    GivenResetLevelParametrizedForCopyAdapter::SetUp();

    // Force update internal values with non default values
    component_->setCopyMode(dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    ASSERT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    ASSERT_EQ(component_->getInterruptMode(), FeatureEnabled::true_);

    ON_CALL(*(systemServices_->getMockIResetManager()),getCurrentLevel()).WillByDefault(testing::Return(resetMocked_));
}

void GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupportedAndResetLevelParametrized::TearDown()
{
    GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupported::TearDown(); 
};

TEST_P(GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupportedAndResetLevelParametrized, WhenCheckResetIsCalled_ThenValuesResetToExpected)
{
    EXPECT_CALL(*mockIDataStore_, insert_or_replace_ex(_,_,_)).Times(1).WillRepeatedly(testing::Return(true));
    component_->checkIfResetDataIsNeeded();

    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    EXPECT_EQ(component_->getColorCopyEnabled(), true);
    EXPECT_EQ(component_->getCopyEnabled(), true);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::false_);
}

INSTANTIATE_TEST_CASE_P(, GivenACopyAdapterStandardWithInterruptWithCopyModePrintAfterScanningSupportedAndResetLevelParametrized,
    ::testing::ValuesIn(GivenResetLevelParametrizedForCopyAdapterResetLevels_));

///////////////////////////////////////////////////////////////////////////////
//
// class GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupported
//
///////////////////////////////////////////////////////////////////////////////

class GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupported :public GivenANewCopyAdapterStandard
{
  public:

    GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupported() {};

    virtual void SetUp() override;

    virtual void TearDown() override;

    dune::framework::core::Uuid copyConfigurationUuid{Uuid("24eb349c-11ec-11ed-861d-0242ac120002")};
};

void GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupported::SetUp()
{
    GivenANewCopyAdapterStandard::SetUp();

    std::shared_ptr<IMicroService> svc =
        std::make_shared<dune::ws::cdm::framework::MicroServiceFactoryTestHelper::FakeService>();

    ON_CALL(*mockIDataStore_, find(copyConfigurationUuid)).WillByDefault(Return(ByMove(std::pair<bool, dune::framework::data::DataObject>(
            false, dune::framework::data::DataObject({{nullptr, 0x200}, {0,0,0,0}, dune::framework::core::Uuid()})))));    

    ON_CALL(*(mockMicroServiceFactory_.get()), createMicroService(testing::_))        
        .WillByDefault(testing::Return(std::weak_ptr<IMicroService>(svc)));

    IComponent * comp = static_cast<IComponent*>(component_);

    //Set print after scanning as default copy mode
    systemServices_->setConfigurationServiceBehaviour("./testResources/CopyAdapterStandardConfig.fbs", "./testResources/PrintWhileScanAllowInterruptTestData.json");

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required
    component_->setInterface(GET_INTERFACE_UID(dune::ws::cdm::framework::IMicroServiceFactory), "",
                             (void*)mockMicroServiceFactory_.get());
    component_->setInterface(GET_INTERFACE_UID(dune::framework::data::IDataStore), "",
                             (void*)mockIDataStore_.get());

    std::future<void> asyncCompletion;
    static_cast<IComponent*>(component_)->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }                             
}

void GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupported::TearDown()
{
    GivenANewCopyAdapterStandard::TearDown();
}

TEST_F(GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupported, WhenGetInterruptModeIsCalled_ThenInterruptModeIsReturned)
{
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::true_);
}

TEST_F(GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupported, WhenSetInterruptModeIsCalled_ThenInterruptModeIsSet)
{
    component_->setInterruptMode(FeatureEnabled::false_);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::false_);
}

TEST_F(GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupported, WhenSetCopyModeIsCalledAsPrintAfterScanning_ThenCopyModeIsSetAndInterruptIsFalse)
{
    component_->setCopyMode(dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::false_);
}

TEST_F(GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupported, WhenSetCopyModeIsCalledAsPrintWhileScanning_ThenCopyModeIsSetAndInterruptIsTrue)
{
    component_->setCopyMode(dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::true_);
}

class GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupportedAndResetLevelParametrized :
    public GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupported,
    public GivenResetLevelParametrizedForCopyAdapter
{
public:
    GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupportedAndResetLevelParametrized(){};
    virtual void SetUp() override;

    virtual void TearDown() override;
};

void GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupportedAndResetLevelParametrized::SetUp()
{
    GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupported::SetUp();
    GivenResetLevelParametrizedForCopyAdapter::SetUp();

    // Force update internal values with non default values
    component_->setCopyMode(dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    ASSERT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printAfterScanning);
    ASSERT_EQ(component_->getInterruptMode(), FeatureEnabled::false_);

    ON_CALL(*(systemServices_->getMockIResetManager()),getCurrentLevel()).WillByDefault(testing::Return(resetMocked_));
}

void GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupportedAndResetLevelParametrized::TearDown()
{
    GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupported::TearDown(); 
};

TEST_P(GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupportedAndResetLevelParametrized, WhenCheckResetIsCalled_ThenValuesResetToExpected)
{
    EXPECT_CALL(*mockIDataStore_, insert_or_replace_ex(_,_,_)).Times(1).WillRepeatedly(testing::Return(true));
    component_->checkIfResetDataIsNeeded();

    EXPECT_EQ(component_->getCopyMode(), dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
    EXPECT_EQ(component_->getColorCopyEnabled(), true);
    EXPECT_EQ(component_->getCopyEnabled(), true);
    EXPECT_EQ(component_->getInterruptMode(), FeatureEnabled::true_);
}

INSTANTIATE_TEST_CASE_P(, GivenACopyAdapterStandardWithInterruptWithCopyModePrintWhileScanningSupportedAndResetLevelParametrized,
    ::testing::ValuesIn(GivenResetLevelParametrizedForCopyAdapterResetLevels_));

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedCopyAdapterStandardReadyToCallShutdown : shutdown case.
// Dummy class that inherits from GivenAConnectedCopyAdapterStandard in order to reuse code
// and enable parametrized tests. 
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedCopyAdapterStandardReadyToCallShutdown : public GivenAConnectedCopyAdapterStandard,
                           public ::testing::WithParamInterface<IComponent::ShutdownCause>
{};

TEST_P(GivenAConnectedCopyAdapterStandardReadyToCallShutdown, whenShutdownIsCalled_TheComponentGetsShutdown)
{
    IComponent * comp = static_cast<IComponent*>(component_);

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

INSTANTIATE_TEST_CASE_P(InstantiationName, GivenAConnectedCopyAdapterStandardReadyToCallShutdown, ::testing::Values(
 IComponent::ShutdownCause(IComponent::ShutdownCause::POWER_OFF),
 IComponent::ShutdownCause(IComponent::ShutdownCause::REBOOT),
 IComponent::ShutdownCause(IComponent::ShutdownCause::SEVERE_ERROR),
 IComponent::ShutdownCause(IComponent::ShutdownCause::EMERGENCY_ERROR),
 IComponent::ShutdownCause(IComponent::ShutdownCause::CRITICAL_ERROR)
));


