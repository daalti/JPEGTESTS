////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAppWorkflowPageSensorGtest.cpp
 * @brief  GTest for CopyApp
 * @date   11th Nov, 2020
 * @author Hectorn Sanchez Gonzalez (hector.sanchez-gonzalez@hp.com)
 *
 * (C) Copyright 2019 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "gmock/gmock-matchers.h"
#include <QQmlContext>
#include "IPathDirectory.h"
#include "MockIGuiApplicationEngine.h"
#include "MockIResourceStore.h"
#include "gmock/gmock.h"
#include "gtest/gtest.h"

#include "common_debug.h"
#include "CopyAppWorkflowPageSensorGtest_TraceAutogen.h"
#include "WalkupAppGtestUtils.h"
#include "CopyAppWorkflow.h"
#include "SimplePathDirMock.h"
#include "TestSystemServices.h"
#include "SpiceDataMap.h"
#include "PreviewStandard.h"
#include "CopyAppWorkflowConstants.h"
#include "com_hp_cdm_service_jobManagement_version_1_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_sharedTypes_jobTicket_models_generated.h"
#include "com_hp_cdm_service_scan_version_1_models_generated.h"
#include "com_hp_cdm_service_validator_version_1_models_generated.h"
#include "com_hp_cdm_service_validator_version_1_qmlRegistration_generated.h"

using namespace dune::spice::testing;
using namespace dune::spice::testing::qmltest;
using namespace dune::spice::testing::environment;
using namespace dune::spice::guiCore;
using namespace dune::spice::jobManagement_1;
using namespace dune::spice::jobTicket_1;
using namespace dune::spice::jobTicket_1::jobTicket;
using namespace dune::spice::scan_1;
using namespace WalkupAppGtestUtils;
using namespace dune::spice::validator_1;
using dune::print::spice::PreviewStandard;

using dune::copy::spice::CopyAppWorkflow;
using TestSystemServices = dune::framework::component::TestingUtil::TestSystemServices;
using SystemServices = dune::framework::component::SystemServices;
using dune::framework::storage::path::Paths;
using FeatureEnabled = dune::spice::glossary_1::FeatureEnabled::FeatureEnabled;

#define FAKE_JOB_0_ID  "fake-job0-0000-id"
#define FAKE_JOB_1_ID  "fake-job0-0001-id"

class GivenCopyAppConfigured : public SpiceWorkflowFixture
{
  public:
    using StatusModel = dune::spice::scan_1::StatusModel;
    GivenCopyAppConfigured() = default;

    virtual void SetUp()
    {
        SpiceWorkflowFixture::configureXL();
        SpiceWorkflowFixture::SetUp();

        systemServices_ = new TestSystemServices();
        systemServices_->setConfigurationServiceBehaviour("./testResources/CopySummary.fbs", "./testResources/CopyAppWorkflow.json");
        // mocking the resources folder path
        auto spm = new dune::framework::storage::path::SimplePathServicesMock();
        auto spd = new dune::framework::storage::path::SimplePathDirectory();
        spd->addPath(Paths::RESOURCE_DIRECTORY, SpiceGuiGTestEnvironment::resourceDirectory.toStdString());
        spm->setPathDirectory(spd);
        systemServices_->setPathServices(spm);

        // dictionary registration
        qmlRegisterUncreatableType<dune::spice::core::ResourceStoreTypes>(
            "spiceGuiCore", 1, 0, "ResourceStoreTypes", "ResourceStoreTypes class can not be created");

        jobInfoModel_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
            new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");
        jobInfoModel_->setJobId("fake-job0-0000-id"); 
        jobInfoModel_->setState(dune::spice::jobManagement_1::State::State::created);
        scanStatusModel_ = mockIResourceStore_->registerFakeResource<dune::spice::scan_1::StatusModel>(
            new dune::spice::scan_1::StatusModel( "/cdm/scan/v1/status" ) );

        // // CDM mocking
        jobsListing_ =
            mockIResourceStore_->registerFakeResource<JobsModel>(new JobsModel("/cdm/jobManagement/v1/queue"));

        pagesModel_ =
            mockIResourceStore_->registerFakeResource<PagesModel>(new PagesModel("/cdm/jobManagement/v1/jobs/fake-job0-0000-id/pages"));

        //Create preview component to register preview module into QML
        preview_ = std::make_shared<PreviewStandard>("PreviewStandard");
        preview_->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices *>(systemServices_));
        preview_->setInterface(GET_INTERFACE_UID(dune::spice::guiCore::IGuiApplicationEngine), "", static_cast<void*>(mockIGuiApplicationEngine));
        std::future<void> previewUnusedFuture;
        std::function<void()> f = [&]() { preview_->connected(nullptr, previewUnusedFuture); };
        SpiceGuiFixture::executeTask<decltype(f)>(f);

        propertyMap_ = new SpiceDataMap(QString("./testResources/generated/TestSpiceDataMap.bin"));
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty("_propertyMap", propertyMap_);
        mockIGuiApplicationEngine->getQQmlEngine()->addImportPath("qrc:/Walkup/imports");
        propertyMap_->moveToThread(nullptr);

        // Filling several models:Ticket with several calls to createInstance
        WalkupAppGtestUtils::createInstanceOfJobTicket(mockIResourceStore_, QStringLiteral(FAKE_JOB_0_ID));
        WalkupAppGtestUtils::createInstanceOfJobTicket(mockIResourceStore_, QStringLiteral(FAKE_JOB_1_ID));

        // Filling several models:Job
        WalkupAppGtestUtils::registerJobTicket(mockIResourceStore_, QStringLiteral(FAKE_JOB_0_ID));
        WalkupAppGtestUtils::registerJobTicket(mockIResourceStore_, QStringLiteral(FAKE_JOB_1_ID));

        constraintsModel_ = mockIResourceStore_->registerFakeResource<ConstraintsModel>(
            new ConstraintsModel(QStringLiteral("/cdm/jobTicket/v1/tickets/%1/constraints").arg(FAKE_JOB_0_ID)));

        //Filling several models:Scan
        WalkupAppGtestUtils::fillDefaultScanStatusModel( MDF, scanStatusModel_);
        dune::spice::scan_1::MdfModel* mdfModel = static_cast< dune::spice::scan_1::MdfModel* >( scanStatusModel_->getMdf() );
        mdfModel->setState(dune::spice::scan_1::ScanMediaPathStateType::ScanMediaPathStateType::notLoaded);//Media unloaded by default


        // creating aut
        aut_ = std::make_shared<CopyAppWorkflow>("CopyApp");
        aut_->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices *>(systemServices_));

        // IComponent initialization
        aut_->setInterface(GET_INTERFACE_UID(dune::spice::guiCore::IGuiApplicationEngine), "",
                           static_cast<void*>(mockIGuiApplicationEngine));

    }
    virtual void startApplication()
    {
        std::future<void> completionFuture;
        std::function<void()> f = [&]() { aut_->connected(nullptr, completionFuture); };
        SpiceGuiFixture::executeTask<decltype(f)>(f);
        
        aut_->start();
        GTestSignalSpy spy(aut_->getSpiceQmlIncubator(), SIGNAL(incubationFinished(bool)));
        ASSERT_TRUE(spy.waitForSignal(30000));
        application_ = aut_->getSpiceApplication();
        ASSERT_NE(application_, nullptr);

        QVariant stack = application_->property("applicationStack");
        ASSERT_FALSE(stack.isNull());
        stack_ = qvariant_cast<QQuickItem*>(stack);
        stateMachine_ = qvariant_cast<QQuickItem*>(application_->property("_stateMachine"));
        stateMachine_->setProperty("toastTimeout", 100);
    }

    void fillPagesModel(){
        pageModel = new PageModel();
        pageModel->setPageId(QString("fake-page0-0000-id"));
        pageModel->setPreviewProgress(100);
        ImageDescriptorModel* highResImage = new ImageDescriptorModel();
        highResImage->setWidth(100);
        highResImage->setHeight(100);
        imageLink = new dune::spice::glossary_1::links::ItemModel();
        imageLink->setRel(QStringLiteral("High Res Image"));
        imageLink->setHref(QStringLiteral("./testResources/integrationTest002.jpg"));

        QObjectListModel* links = highResImage->getLinks();
        links->append(imageLink);

        pageModel->setHighResImage(highResImage);
        QObjectListModel* pageList = pagesModel_->getPages();
        pageList->append(pageModel);
    }

    void fillJobQueueModel(){
        JobModel* jobData = new JobModel();

        jobData->setJobId("fake-job0-0000-id");
        jobData->setJobName("copy");
        jobData->setJobType(dune::spice::jobManagement_1::JobType::JobType::copy);
        jobData->setState(dune::spice::jobManagement_1::State::State::processing);

        QObjectListModel* jobListCustom = jobsListing_->getJobList();

        jobListCustom->append(jobData);

        JobModel* jobData1 = new JobModel();

        jobData1->setJobId("");
        jobData1->setJobName("copy");
        jobData1->setJobType(dune::spice::jobManagement_1::JobType::JobType::copy);
        jobData1->setState(dune::spice::jobManagement_1::State::State::processing);

        jobListCustom->append(jobData1);

    }

    virtual void TearDown()
    {
        aut_->quit();
        
        delete systemServices_;
        delete propertyMap_;
        if(application_){
            application_->deleteLater();
        }
        if(stateMachine_){
            stateMachine_->deleteLater();
        }
        if(stack_){
            stack_->deleteLater();
        }
        SpiceWorkflowFixture::TearDown();
    }

  protected:
    QObject                                         *application_  = nullptr;
    QObject                                         *stateMachine_ = nullptr;
    QQuickItem                                      *stack_        = nullptr;
    SpiceDataMap*                                   propertyMap_ = nullptr;

    std::shared_ptr<CopyAppWorkflow> aut_;
    std::shared_ptr<PreviewStandard>               preview_;

    std::vector<std::shared_ptr<JobTicketModel>>        jobTicketModels_;
    std::vector<std::shared_ptr<JobModel>>              jobInfoModels_;
    std::shared_ptr<dune::spice::scan_1::StatusModel>   scanStatusModel_;
    std::shared_ptr<JobModel>                           jobInfoModel_;
    std::shared_ptr<JobTicketModel>                     jobTicketModel_;
    std::shared_ptr<JobsModel>                          jobsListing_;
    std::shared_ptr<ConstraintsModel>                   constraintsModel_;
    std::shared_ptr<PagesModel>                         pagesModel_;
    dune::spice::glossary_1::links::ItemModel*          imageLink{nullptr};
    PageModel*                                          pageModel{nullptr};
    std::shared_ptr<PageModel>                          pageModel_;

    TestSystemServices*                                 systemServices_;
};

//Workaround for race conditions didnt work in iq. We need a robust solution as disconnect lambada function in gtest TearDowns
//TODO ask to view framework for a solution to avoid this race conditions with lambda functions finishing gtests
TEST_F(GivenCopyAppConfigured, DISABLED_WhenViewsIsShownAndRequestTicketsHasNotFinished_thenAllBottonsAreDisabled)
{
    //Check mainWindow is shown
    {
        WAIT_FOR_ITEM(contentItem_, "#copyLandingView");
        ASSERT_TRUE(item);
        auto copyLandingView = qmltest::querySelector(contentItem_, "#copyLandingView");
    }

    //Check mainActionButton
    {
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);
        WalkupAppGtestUtils::compareSpiceButtonProperties(  item, false, false );
    }

    //Check settings button
    {
        WAIT_FOR_ITEM(contentItem_, "#optionsDetailPanelButton");
        ASSERT_TRUE(item);
        WalkupAppGtestUtils::compareSpiceButtonProperties(  item, true, false );
    }

    //Workaround related to WhenWaitAndCompareForLanding_itGeneratesALeak
    QTest::qWait(1);
}

//DISABLED: requiere constrainst and getUrl from controller fake values
TEST_F(GivenCopyAppConfigured, DISABLED_WhenSettingsButtonIsEnabledAndClicked_thenSettingViesIsShown)
{
    //Check mainWindow is shown
    {
        WAIT_FOR_ITEM(contentItem_, "#copyLandingView");
        ASSERT_TRUE(item);
    }

    //Wait for settings button and click
    {
        WAIT_FOR_ITEM(contentItem_, "#optionsDetailPanelButton");
        ASSERT_TRUE(item);

        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);


        WalkupAppGtestUtils::compareSpiceButtonProperties(  item, true, true );

        mouseClick( item, Qt::LeftButton );
    }

    WAIT_COMPARE(stateMachine_->property("activeState"), "SELECT_SETTINGS");

    //Check select settings window is shown
    {
        WAIT_FOR_ITEM(contentItem_, "#copySettingsView");
        ASSERT_TRUE(item);
    }

}


class GivenNotLoadedMfpCopyApp : public GivenCopyAppConfigured
{
  public:
    GivenNotLoadedMfpCopyApp() = default;

    void SetUp() override
    {
        GivenCopyAppConfigured::SetUp();
        startApplication();
        // Unload media.
        scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Idle);
        dune::spice::scan_1::MdfModel* mdfModel = static_cast< dune::spice::scan_1::MdfModel* >( scanStatusModel_->getMdf() );
        mdfModel->setState(dune::spice::scan_1::ScanMediaPathStateType::ScanMediaPathStateType::notLoaded);
    }
    void startApplication() override
    {
        GivenCopyAppConfigured::startApplication();
    }
};

TEST_F(GivenNotLoadedMfpCopyApp, DISABLED_WhenWaitAndCompareForLanding_itGeneratesALeak)
{
    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS);

    //This wait solves the Leak generated!!
    //Test is so simple and so fast, some lambdas are generated, but gtest finishes very fast and
    //lambda functions are executed once statemachine execute doQuit and while tearDown is executing.
    //Will be asked to viewFramework about how disconnect in tearDown the conecction
    // aut_->connected(nullptr, completionFuture) did in fixture

    //QTest::qWait(1);
}

TEST_F(GivenNotLoadedMfpCopyApp, DISABLED_WhenInitWithoutMediaStateArrive_thenCopyButtonIsEnabled)
{
    //Check mainWindow is shown
    {
        WAIT_FOR_ITEM(contentItem_, "#copyLandingView");
        ASSERT_TRUE(item);
        auto copyLandingView = qmltest::querySelector(contentItem_, "#copyLandingView");
    }


    //Check mainActionButton when NOT_LOADED state arrives
    {
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);
        
        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);

        WalkupAppGtestUtils::compareSpiceButtonProperties(  item, true, true, "cCopy" );
    }

    //Check settings button
    {
        WAIT_FOR_ITEM(contentItem_, "#optionsDetailPanelButton");
        ASSERT_TRUE(item);
        WalkupAppGtestUtils::compareSpiceButtonProperties(  item, true, true );
    }
}
// This test has a Screencapture tests
// https://rndwiki.inc.hpicorp.net/confluence/pages/viewpage.action?spaceKey=Dune&title=Screencapture+tests
SETUP_LAYOUT_TEST(GivenNotLoadedMfpCopyApp)

TEST_P(GivenNotLoadedMfpCopyApp_P, DISABLED_WhenInitWithoutMediaStateArrive_thenEjectButtonIsInvisible)
{
    //Check mainWindow is shown
    {
        WAIT_FOR_ITEM(contentItem_, "#copyLandingView");
        ASSERT_TRUE(item);
        auto copyLandingView = qmltest::querySelector(contentItem_, "#copyLandingView");
    }


    //Check mainActionButton when NOT_LOADED state arrives
    {
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);
        
        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);

        WalkupAppGtestUtils::compareSpiceButtonProperties( item, true, true, "cCopy" );
    }
    
    //Check ejectMainPanelButton when NOT_LOADED state arrives
    {
        WAIT_FOR_ITEM(contentItem_, "#ejectMainPanelButton");
        ASSERT_TRUE(item);

        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);

        WalkupAppGtestUtils::compareSpiceButtonProperties(  item, false, true);
    }
    EXPECT_TRUE(qmltest::validateScreenCapture());
}
TEST_F(GivenNotLoadedMfpCopyApp, DISABLED_WhenInitMediaNotLoaded_thenModalConstraintEnabled)
{
    //Check mainWindow is shown
    {
        WAIT_FOR_ITEM(contentItem_, "#copyLandingView");
        ASSERT_TRUE(item);
        auto copyLandingView = qmltest::querySelector(contentItem_, "#copyLandingView");
    }

    //Check mainActionButton when NOT_LOADED state arrives
    {
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);
        
        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);
        WalkupAppGtestUtils::compareSpiceButtonProperties(  item, true, true, "cCopy");

        WAIT_UNTIL(item->property("constrained").toBool() == true);
        mouseClick( item, Qt::LeftButton );
    }

    //Commenting the below cose as it is causing the gtest to fail intermittenly
    // {
    
    //    WAIT_FOR_ITEM(contentItem_, "#ConstraintMessage");
    //    auto constraintMessage = item;

    //    auto notInsertPage = (constraintMessage->property("message"));
    //    EXPECT_EQ(notInsertPage, "cInsertPageInScanner");
       
    //    auto okButton = qmltest::querySelector(constraintMessage, "#okButton");
    //    ASSERT_TRUE(okButton);

       
    // }

}

class GivenLoadedMfpCopyApp : public GivenCopyAppConfigured
{
  public:
    GivenLoadedMfpCopyApp() = default;

    void SetUp() override
    {
        GivenCopyAppConfigured::SetUp();
        startApplication();
        //Media loaded
        dune::spice::scan_1::MdfModel* mdfModel = static_cast< dune::spice::scan_1::MdfModel* >( scanStatusModel_->getMdf() );
        mdfModel->setEjectable(dune::spice::glossary_1::FeatureEnabled::FeatureEnabled::true_);
        mdfModel->setState(dune::spice::scan_1::ScanMediaPathStateType::ScanMediaPathStateType::loaded);  
        scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Idle);
    }
    void startApplication() override
    {
        GivenCopyAppConfigured::startApplication();
    }
};


TEST_F(GivenLoadedMfpCopyApp, DISABLED_WhenInitWithMediaStateArrive_thenStartButtonIsEnabled)
{
    //Check mainWindow is shown
    {
        WAIT_FOR_ITEM(contentItem_, "#copyLandingView");
        ASSERT_TRUE(item);
        auto copyLandingView = qmltest::querySelector(contentItem_, "#copyLandingView");
    }

    //Check mainActionButton when NOT_LOADED state arrives
    {
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);

        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);

        WalkupAppGtestUtils::compareSpiceButtonProperties( item, true, true, "cStart" );

        ASSERT_FALSE(item->property("constrained").toBool());
    }

    //Check settings button
    {
        WAIT_FOR_ITEM(contentItem_, "#optionsDetailPanelButton");
        ASSERT_TRUE(item);
        WalkupAppGtestUtils::compareSpiceButtonProperties(  item, true, true );
    }
}

TEST_F(GivenLoadedMfpCopyApp, DISABLED_WhenInitWithMediaStateArriveAndThenEjectMedia_thenEjectButtonIsInvisible)
{
    //Check mainWindow is shown
    {
        WAIT_FOR_ITEM(contentItem_, "#copyLandingView");
        ASSERT_TRUE(item);
        auto copyLandingView = qmltest::querySelector(contentItem_, "#copyLandingView");
    }

    //Check mainActionButton when NOT_LOADED state arrives
    {
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);

        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);

        WalkupAppGtestUtils::compareSpiceButtonProperties( item, true, true, "cStart" );
    }

    //Check ejectMainPanelButton when NOT_LOADED state arrives
    {
        WAIT_FOR_ITEM(contentItem_, "#ejectMainPanelButton");
        ASSERT_TRUE(item);

        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);

        WalkupAppGtestUtils::compareSpiceButtonProperties( item, true, true);
    }

    //If suddenly media change to notEjectable eject button must dissapear
    dune::spice::scan_1::MdfModel* mdfModel = static_cast< dune::spice::scan_1::MdfModel* >( scanStatusModel_->getMdf() );
    mdfModel->setEjectable(dune::spice::glossary_1::FeatureEnabled::FeatureEnabled::false_);
    {
        WAIT_FOR_ITEM(contentItem_, "#ejectMainPanelButton");
        ASSERT_TRUE(item);

        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("visible").toBool() == false); //WAIT because can exist some race condition hidding the button

        WalkupAppGtestUtils::compareSpiceButtonProperties( item, false, true);
    }
}

class GivenInitialStateMachineCopyApp : public GivenCopyAppConfigured
{
  public:
    GivenInitialStateMachineCopyApp() = default;

    void SetUp() override
    {
        GivenCopyAppConfigured::SetUp();
        startApplication();
        //Media loaded
        dune::spice::scan_1::MdfModel* mdfModel = static_cast< dune::spice::scan_1::MdfModel* >( scanStatusModel_->getMdf() );
        mdfModel->setEjectable(dune::spice::glossary_1::FeatureEnabled::FeatureEnabled::true_);
        mdfModel->setState(dune::spice::scan_1::ScanMediaPathStateType::ScanMediaPathStateType::loaded);
        scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Idle);
    }
     void startApplication() override
    {
        GivenCopyAppConfigured::startApplication();
    }
};

// Disabled due to detected race conditions (e.g. see 1s wait in line 481)
TEST_F(GivenInitialStateMachineCopyApp, DISABLED_WhenWeRunFullCopyStateMachine_thenFinalStateIsProcessingAndAction)
{
    //Check mainWindow is shown
    {
        WAIT_FOR_ITEM(contentItem_, "#copyLandingView");
        ASSERT_TRUE(item);
        // MDF type of scanner with M to XL show prepreview animation
        auto copyLandingView = qmltest::querySelector(contentItem_, "#copyLandingView");
    }

    //Check mainActionButton when MEDIA LOADED state arrives
    {
        CHECKPOINTA("### CHECKING MEDIA_LOADED ###");
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);

        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);

        WalkupAppGtestUtils::compareSpiceButtonProperties( item, true, true, "cStart" );

        mouseClick( item, Qt::LeftButton );
    }

    // CLONE_TICKET
    // self.isEditSettingsActionEnabled = false;
    // self.mainActionButtonType = "NONE";
    // self.isMainActionButtonEnabled = false;
    // self.isEjectActionAllowedByStMachine = false;
    // self.currentJobState = -1

    // CLONE_TICKET (wait synchronization for current state)
    CHECKPOINTA("### CHECKING CLONE_TICKET ###");
    WAIT_UNTIL(stateMachine_->property("currentJobState") == -1);

    // Automatic transition CLONE_TICKET -> INIT_JOB
    
    // INIT_JOB
    // self.isEditSettingsActionEnabled = false;
    // self.mainActionButtonType = "NONE";
    // self.isMainActionButtonEnabled = false;
    // self.isEjectActionAllowedByStMachine = false;

    // Transition INIT_JOB -> INIT_SCANNING
    CHECKPOINTA("### CHECKING INIT_JOB ###");
    stateMachine_->setProperty("currentJobState", 1);

    // INIT_SCANNING
    // self.isEditSettingsActionEnabled = false;
    // self.mainActionButtonType = "NONE";
    // self.isMainActionButtonEnabled = false;
    // self.isEjectActionAllowedByStMachine = false;

    // Transition INIT_SCANNING -> ACQUIRING
    CHECKPOINTA("### CHECKING INIT_SCANNING ###");
    QTest::qWait(1000); // Inevitable wait, it seems the Gtest is faster than the state machine and we have to slow down to sync
    scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Processing);

    // ACQUIRING
    // self.isEditSettingsActionEnabled = true;
    // self.mainActionButtonType = "NONE";
    // self.isMainActionButtonEnabled = false;
    // self.isEjectActionAllowedByStMachine = false;

    // Check settings button appears
    {
        CHECKPOINTA("### CHECKING ACQUIRING ###");
        WAIT_FOR_ITEM(contentItem_, "#optionsDetailPanelButton");
        ASSERT_TRUE(item);

        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);
    }

    // Check main button does not appear
    {
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);

        WAIT_UNTIL(item->property("enabled").toBool() == false);

        //Sync action because WAIT_FOR substates without view does not work
        WalkupAppGtestUtils::compareSpiceButtonProperties( item, false, false);
    }
    
    // Transition ACQUIRING -> PROCESSING_AND_ACTION
    scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Idle);
    
    // PROCESSING_AND_ACTION
    // self.isEditSettingsActionEnabled = true;
    // self.mainActionButtonType = self.isTicketMultipage() ? "DONE" : "NONE";
    // self.isMainActionButtonEnabled = self.isTicketMultipage();
    // self.isEjectActionAllowedByStMachine = true;
    
    // Check settings button appears
    {
        CHECKPOINTA("### CHECKING PROCESSING_AND_ACTION 1 ###");
        WAIT_FOR_ITEM(contentItem_, "#optionsDetailPanelButton");
        ASSERT_TRUE(item);

        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);
    }

    // Click done and wait for quit event
    {
        CHECKPOINTA("### CHECKING PROCESSING_AND_ACTION 2 ###");
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);

        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);

        WalkupAppGtestUtils::compareSpiceButtonProperties( item, true, true, "cDoneButton" );
    }
}

class GivenLaunchCopyAppFromwidget : public GivenCopyAppConfigured
{
  public:
    GivenLaunchCopyAppFromwidget() = default;

    void SetUp() override
    {
        GivenCopyAppConfigured::SetUp();
        //Media loaded
        fillPagesModel();
        dune::spice::scan_1::MdfModel* mdfModel = static_cast< dune::spice::scan_1::MdfModel* >( scanStatusModel_->getMdf() );
        mdfModel->setEjectable(dune::spice::glossary_1::FeatureEnabled::FeatureEnabled::true_);
        mdfModel->setState(dune::spice::scan_1::ScanMediaPathStateType::ScanMediaPathStateType::loaded);
        scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Idle);  
    }
    void TearDown()
    {
        if(imageLink){
            delete imageLink;
        }
        if(pageModel){
            delete pageModel;
        }
        GivenCopyAppConfigured::TearDown();
    }
    void startApplication(bool isAutoStartJobFromWidget, int numberOfCopiesFromWidget)
    {
        std::future<void> completionFuture;
        std::function<void()> f = [&]() { aut_->connected(nullptr, completionFuture); };
        SpiceGuiFixture::executeTask<decltype(f)>(f);
        QVariantMap initialValues;
        initialValues.insert("launchFrom", 2);
        initialValues.insert("isAutoStartJobFromWidget", isAutoStartJobFromWidget);
        initialValues.insert("numberOfCopiesFromWidget", numberOfCopiesFromWidget);
        GTestSignalSpy spy(aut_->getSpiceQmlIncubator(), SIGNAL(incubationFinished(bool)));
        aut_->start(initialValues);

        ASSERT_TRUE(spy.waitForSignal(30000));
        application_ = aut_->getSpiceApplication();
        ASSERT_NE(application_, nullptr);

        QVariant stack = application_->property("applicationStack");
        ASSERT_FALSE(stack.isNull());
        stack_ = qvariant_cast<QQuickItem*>(stack);
        stateMachine_ = qvariant_cast<QQuickItem*>(application_->property("_stateMachine"));
        stateMachine_->setProperty("toastTimeout", 100);
    }

};

TEST_F(GivenLaunchCopyAppFromwidget, DISABLED_LaunchCopyAppFromWidgetInitMediaLoaded)
{
    startApplication(true, 2);
    // Check mainWindow is shown and DetailPanel is hidden
    {
        WAIT_FOR_ITEM(contentItem_, "#copyLandingView");
        ASSERT_TRUE(item);
        ASSERT_TRUE(item->property("secondaryPanel").isNull());
        auto copyLandingView = qmltest::querySelector(contentItem_, "#copyLandingView");
    }
    
    // CLONE_TICKET
    // self.isEditSettingsActionEnabled = false;
    // self.mainActionButtonType = "NONE";
    // self.isMainActionButtonEnabled = false;
    // self.isEjectActionAllowedByStMachine = false;
    // self.currentJobState = -1

    // CLONE_TICKET (wait synchronization for current state)
    CHECKPOINTA("### CHECKING CLONE_TICKET ###");
    WAIT_UNTIL(stateMachine_->property("currentJobState") == -1);

    // Automatic transition CLONE_TICKET -> INIT_JOB
    
    // INIT_JOB
    // self.isEditSettingsActionEnabled = false;
    // self.mainActionButtonType = "NONE";
    // self.isMainActionButtonEnabled = false;
    // self.isEjectActionAllowedByStMachine = false;

    // Transition INIT_JOB -> INIT_SCANNING
    CHECKPOINTA("### CHECKING INIT_JOB ###");;
    QTest::qWait(1000);// Inevitable wait, it seems the Gtest is faster than the state machine and we have to slow down to sync
    jobInfoModel_->setState(dune::spice::jobManagement_1::State::State::ready);

    // INIT_SCANNING
    // self.isEditSettingsActionEnabled = false;
    // self.mainActionButtonType = "NONE";
    // self.isMainActionButtonEnabled = false;
    // self.isEjectActionAllowedByStMachine = false;

    // Transition INIT_SCANNING -> ACQUIRING
    CHECKPOINTA("### CHECKING INIT_SCANNING ###");
    QTest::qWait(1000); // Inevitable wait, it seems the Gtest is faster than the state machine and we have to slow down to sync
    scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Processing);

    // ACQUIRING
    // self.isEditSettingsActionEnabled = true;
    // self.mainActionButtonType = "NONE";
    // self.isMainActionButtonEnabled = false;
    // self.isEjectActionAllowedByStMachine = false;

    // Check main button does not appear
    {   
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfMainPanel");
        ASSERT_TRUE(item);

        WAIT_UNTIL(item->property("enabled").toBool() == false);
    }
    
    // Transition ACQUIRING -> WAITING_PREVIEW
    scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Idle);//Will fix this gtest in another story
    
    // Transition WAITING_PREVIEW -> PROCESSING_AND_ACTION
    // PROCESSING_AND_ACTION
    // self.isEditSettingsActionEnabled = true;
    // self.mainActionButtonType = self.isTicketMultipage() ? "DONE" : "NONE";
    // self.isMainActionButtonEnabled = self.isTicketMultipage();
    // self.isEjectActionAllowedByStMachine = true;

    
    {
        CHECKPOINTA("### CHECKING PROCESSING_AND_ACTION 2 ###");
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfMainPanel");
        ASSERT_TRUE(item);
        WAIT_UNTIL(item->property("enabled").toBool() == true);

        WalkupAppGtestUtils::compareSpiceButtonProperties( item, true, true, "cDoneButton" );
    }

}


class GivenLoadedMfpCopyAppForPreview : public GivenCopyAppConfigured
{
  public:
    GivenLoadedMfpCopyAppForPreview() = default;

    void SetUp() override
    {
        GivenCopyAppConfigured::SetUp();       
        fillPagesModel();
        startApplication();
        //Media loaded
        dune::spice::scan_1::MdfModel* mdfModel = static_cast< dune::spice::scan_1::MdfModel* >( scanStatusModel_->getMdf() );
        mdfModel->setEjectable(dune::spice::glossary_1::FeatureEnabled::FeatureEnabled::true_);
        mdfModel->setState(dune::spice::scan_1::ScanMediaPathStateType::ScanMediaPathStateType::loaded);   
        scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Idle);
    }
    void startApplication() override
    {
        GivenCopyAppConfigured::startApplication();
    }

    void TearDown() override
    {
        if(imageLink){
            delete imageLink;
        }
        if(pageModel){
            delete pageModel;
        }
        GivenCopyAppConfigured::TearDown();
    }
};

TEST_F(GivenLoadedMfpCopyAppForPreview, DISABLED_LaunchCopyAppInitMediaLoadedAndCheckPreview)
{
    //Check mainWindow is shown
    {
        WAIT_FOR_ITEM(contentItem_, "#copyLandingView");
        ASSERT_TRUE(item);
        auto copyLandingView = qmltest::querySelector(contentItem_, "#copyLandingView");
    }

    CHECKPOINTA("### CHECKING INIT_JOB ###");;
    QTest::qWait(1000);// Inevitable wait, it seems the Gtest is faster than the state machine and we have to slow down to sync
    jobInfoModel_->setState(dune::spice::jobManagement_1::State::State::ready);

    //Check mainActionButton when MEDIA LOADED state arrives
    {
        CHECKPOINTA("### CHECKING MEDIA_LOADED ###");
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);

        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);

        WalkupAppGtestUtils::compareSpiceButtonProperties( item, true, true, "cStart" );

        mouseClick( item, Qt::LeftButton );
    }

    CHECKPOINTA("### CHECKING INIT_JOB ###");;
    QTest::qWait(100);// Inevitable wait, it seems the Gtest is faster than the state machine and we have to slow down to sync
    jobInfoModel_->setState(dune::spice::jobManagement_1::State::State::ready);
    fillJobQueueModel();
    {
            WAIT_FOR_ITEM(contentItem_, "#FitPage");
            ASSERT_TRUE(item);
            QTest::qWait(1000);
    }
    {
        WAIT_FOR_ITEM(contentItem_, "#addPageButton");
        ASSERT_TRUE(item);
        mouseClick( item, Qt::LeftButton );
        QTest::qWait(1000);
    }
    {
        CHECKPOINTA("### checking previewpageprompt ###");
        WAIT_FOR_ITEM(contentItem_, "#previewAddPagePrompt");
        ASSERT_TRUE(item);
        CHECKPOINTA("### CHECKING addpagebutton ###");
        auto okButton = qmltest::querySelector(item, "#addPageOkButton");
        ASSERT_TRUE(okButton);
        mouseClick( okButton, Qt::LeftButton );
    }
}
