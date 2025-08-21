#include "gmock/gmock-matchers.h"
#include "gmock/gmock.h"
#include <QQmlContext>
#include "IPathDirectory.h"
#include "MockIGuiApplicationEngine.h"
#include "MockIResourceStore.h"
#include "gtest/gtest.h"

#include "common_debug.h"
#include "CopyAppWorkflowNonConcurentGtest_TraceAutogen.h"

#include "WalkupAppGtestUtils.h"

#include "CopyAppWorkflow.h"
#include "SimplePathDirMock.h"
#include "TestSystemServices.h"
#include "IMenuResource.h"
#include "SpiceDataMap.h"
#include "PreviewStandard.h"
#include "com_hp_cdm_service_jobManagement_version_1_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_sharedTypes_jobTicket_models_generated.h"
#include "com_hp_cdm_service_scan_version_1_models_generated.h"
#include "com_hp_cdm_service_validator_version_1_models_generated.h"
#include "com_hp_cdm_service_validator_version_1_qmlRegistration_generated.h"
#include "com_hp_cdm_service_print_version_2_qmlRegistration_generated.h"
#include "com_hp_cdm_service_print_version_2_models_generated.h"

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
using PrintStatusModel =  dune::spice::print_2::StatusModel;

#define FAKE_JOB_0_ID  "fake-job0-0000-id"
#define FAKE_JOB_1_ID  "fake-job0-0001-id"

class GivenCopyAppNonConcurrentConfigured : public SpiceWorkflowFixture
{
  public:
    using StatusModel = dune::spice::scan_1::StatusModel;
    GivenCopyAppNonConcurrentConfigured() = default;

    virtual void SetUp()
    {
        SpiceWorkflowFixture::configureS();
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
        
        scanStatusModel_ = mockIResourceStore_->registerFakeResource<dune::spice::scan_1::StatusModel>(
            new dune::spice::scan_1::StatusModel( "/cdm/scan/v1/status" ) );
        
        printStatusModel_ = mockIResourceStore_->registerFakeResource<PrintStatusModel>(
            new PrintStatusModel("/cdm/print/v2/status"));
        
        printStatusModel_->setPrinterState(dune::spice::print_2::status::PrinterState::PrinterState::idle);

        // // CDM mocking
        jobsListing_ =
            mockIResourceStore_->registerFakeResource<JobsModel>(new JobsModel("/cdm/jobManagement/v1/queue"));
        defaultTicket_ = mockIResourceStore_->registerFakeResource<JobTicketModel>(
            new JobTicketModel("/cdm/jobTicket/v1/configuration/defaults/copy"));
        fillDefaultJobTicketModel(defaultTicket_,"fake-default-id");
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
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty(
                                        "_scanPreviewSupported", QVariant(scanPreviewSupported));
                
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty(
                                "_jobConcurrencySupported", QVariant(jobConcurrency));
        
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty(
                                "_multiPagePreviewSupported", QVariant(multiPagePreviewSupported));
        
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty(
                                         "_scannerStatusModel", scanStatusModel_.get());
        devicesupportedShortcutTypes = new QVariantListModel(); 
        devicesupportedShortcutTypes->append(static_cast<std::int16_t>(dune::spice::jobManagement_1::JobType::JobType::copy));
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty(
                                         "_deviceShortcutsJobTypeSupported", devicesupportedShortcutTypes);
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
        stateMachine_->setProperty("previewConfiguration", "enable");
    }

    void fillDefaultJobTicketModel(std::shared_ptr<JobTicketModel> &jobTicketModel, QString ticketId){
        defaultTicket_->setTicketId(ticketId);
        PipelineOptionsModel* pipelineOptionsModel = new PipelineOptionsModel();
        ManualUserOperationsModel* manualUserOperations = new ManualUserOperationsModel();
        manualUserOperations->setImagePreviewConfiguration(manualUserOperations::ImagePreviewConfiguration::ImagePreviewConfiguration::optional);
        pipelineOptionsModel->setManualUserOperations(manualUserOperations);
        defaultTicket_->setPipelineOptions(pipelineOptionsModel);
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
        EXPECT_CALL(*mockIResourceStore_, destroyResource(_, _))
            .WillOnce(testing::Invoke([&](dune::spice::core::ISpiceModel* spiceModel, QVariantMap queryParameters = QVariantMap())
            {
                auto future = new NiceMock<MockIResourceStoreFuture>();
    
                future->setParent(QCoreApplication::instance());
    
                QTimer::singleShot(0, [=]() {
                    future->resolved(future);
                    future->deleteLater();
                });

                return future;
        }));

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

        if(imageLink){
            delete imageLink;
        }
        if(pageModel){
            delete pageModel;
        }
        devicesupportedShortcutTypes->deleteLater();
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
    std::shared_ptr<JobModel>                           jobInfoModel1_;
    std::shared_ptr<JobModel>                           jobInfoModel2_;
    std::shared_ptr<JobModel>                           jobInfoModel3_;
    std::shared_ptr<JobModel>                           jobInfoModel4_;
    std::shared_ptr<dune::spice::scan_1::StatusModel>   scanStatusModel_;
    std::shared_ptr<JobTicketModel>                     jobTicketModel_;
    std::shared_ptr<JobsModel>                          jobsListing_;
    std::shared_ptr<ConstraintsModel>                   constraintsModel_;
    std::shared_ptr<PagesModel>                         pagesModel_;
    dune::spice::glossary_1::links::ItemModel*          imageLink{nullptr};
    PageModel*                                          pageModel{nullptr};
    std::shared_ptr<PageModel>                          pageModel_;
    std::shared_ptr<PrintStatusModel>                   printStatusModel_;
    std::shared_ptr<JobTicketModel>                     defaultTicket_;
    TestSystemServices*                                 systemServices_;
    bool                                                    scanPreviewSupported{true};
    bool                                                    jobConcurrency{false};
    bool                                                    multiPagePreviewSupported{false};
    QVariantListModel*                                  devicesupportedShortcutTypes;
    std::shared_ptr<PriorityModeSessionModel>               priorityModeSessionModel_{nullptr};
};

class GivenCopyAppNonConcurrentMfpNotLoaded : public GivenCopyAppNonConcurrentConfigured
{
    public:
        GivenCopyAppNonConcurrentMfpNotLoaded() = default;

        void SetUp() override
        {
            GivenCopyAppNonConcurrentConfigured::SetUp();
            startApplication();
            jobInfoModel1_ = mockIResourceStore_->registerFakeResource<JobModel>(
            new JobModel("/cdm/jobManagement/v1/jobs/fake-job0-0000-id"));
            jobInfoModel1_->setJobId("fake-job0-0001-id"); 
            jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::created);
            jobInfoModel2_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
                new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");
            jobInfoModel2_->setJobId("fake-job0-0000-id"); 
            jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::created);


            jobInfoModel3_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
                new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");
            jobInfoModel3_->setJobId("fake-job0-0000-id"); 
            jobInfoModel3_->setState(dune::spice::jobManagement_1::State::State::created);
            jobInfoModel4_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
                new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");
            jobInfoModel4_->setJobId("fake-job0-0000-id"); 
            jobInfoModel4_->setState(dune::spice::jobManagement_1::State::State::created);
            scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Idle);
            dune::spice::scan_1::MdfModel* mdfModel = static_cast< dune::spice::scan_1::MdfModel* >( scanStatusModel_->getMdf() );
            mdfModel->setState(dune::spice::scan_1::ScanMediaPathStateType::ScanMediaPathStateType::notLoaded);
            priorityModeSessionModel_ = mockIResourceStore_->registerFakeResource<PriorityModeSessionModel>(
                new PriorityModeSessionModel("/cdm/jobManagement/v1/priorityModeSessions"));
        }
        void startApplication() override
        {
            GivenCopyAppNonConcurrentConfigured::startApplication();
        }
};

TEST_F(GivenCopyAppNonConcurrentMfpNotLoaded, WhenInitMediaNotLoaded_CopyButtonAndOptionsButtonEnabled)
{
    //Check mainWindow is shown
    {
        WAIT_FOR_ITEM(contentItem_, "#copyLandingView");
        ASSERT_TRUE(item);
        //Check Small screen doesnot show prepreview animation
    }

    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)

     WAIT_COMPARE(stateMachine_->property("isEditSettingsActionEnabled"), true)

    //Check mainActionButton when NOT_LOADED state arrives
    {
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);
        jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
        jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);
        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);

        WalkupAppGtestUtils::compareSpiceButtonProperties(  item, true, true, "cCopy" );
    }

    //Check settings button
    {
        WAIT_FOR_ITEM(contentItem_, "#optionsDetailPanelButton");
        ASSERT_TRUE(item);
        WAIT_UNTIL(item->property("enabled").toBool() == true);
        WalkupAppGtestUtils::compareSpiceButtonProperties(  item, true, true );
    }
}

TEST_F(GivenCopyAppNonConcurrentMfpNotLoaded,WhenInitMediaNotLoaded_MainActionButtonConstrained_thenInsertingPagemainactionbuttonisNotConstrained)
{
     {
        WAIT_FOR_ITEM(contentItem_, "#copyLandingView");
        ASSERT_TRUE(item);
    }

    //Check mainActionButton when NOT_LOADED state arrives
    {
        WAIT_UNTIL(stateMachine_->property("isJobSubscribed") == true);
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);
        jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
        jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);
        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);
        WalkupAppGtestUtils::compareSpiceButtonProperties(  item, true, true, "cCopy");

        WAIT_UNTIL(item->property("constrained").toBool() == true);
    }
    dune::spice::scan_1::MdfModel* mdfModel = static_cast< dune::spice::scan_1::MdfModel* >( scanStatusModel_->getMdf() );
    mdfModel->setState(dune::spice::scan_1::ScanMediaPathStateType::ScanMediaPathStateType::loaded);
    {
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);
        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);
        WalkupAppGtestUtils::compareSpiceButtonProperties(  item, true, true, "cCopy");

        WAIT_UNTIL(item->property("constrained").toBool() == false);
    }
}

class GivenCopyAppNonConcurrentMfpLoaded : public GivenCopyAppNonConcurrentConfigured
{
    public:
        GivenCopyAppNonConcurrentMfpLoaded() = default;

        void SetUp() override
        {
            GivenCopyAppNonConcurrentConfigured::SetUp();
            startApplication();
            jobInfoModel1_ = mockIResourceStore_->registerFakeResource<JobModel>(
            new JobModel("/cdm/jobManagement/v1/jobs/fake-job0-0000-id"));
            jobInfoModel1_->setJobId("fake-job0-0001-id"); 
            jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::created);
            jobInfoModel2_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
                new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");
            jobInfoModel2_->setJobId("fake-job0-0000-id"); 
            jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::created);


            jobInfoModel3_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
                new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");
            jobInfoModel3_->setJobId("fake-job0-0000-id"); 
            jobInfoModel3_->setState(dune::spice::jobManagement_1::State::State::created);
            jobInfoModel4_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
                new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");
            jobInfoModel4_->setJobId("fake-job0-0000-id"); 
            jobInfoModel4_->setState(dune::spice::jobManagement_1::State::State::created);
            // Unload media.
            scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Idle);
            dune::spice::scan_1::MdfModel* mdfModel = static_cast< dune::spice::scan_1::MdfModel* >( scanStatusModel_->getMdf() );
            mdfModel->setState(dune::spice::scan_1::ScanMediaPathStateType::ScanMediaPathStateType::loaded);
        }
        void startApplication() override
        {
            GivenCopyAppNonConcurrentConfigured::startApplication();
        }
};

TEST_F(GivenCopyAppNonConcurrentMfpLoaded,WhenInitMediaLoaded_MainActionButtonisNotConstrained)
{
     {
        WAIT_FOR_ITEM(contentItem_, "#copyLandingView");
        ASSERT_TRUE(item);
    }

    //Check mainActionButton when LOADED state arrives
    {
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);
        WAIT_UNTIL(stateMachine_->property("isJobSubscribed") == true);
        jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
        jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);
        //Sync action because WAIT_FOR substates without view does not work
        WAIT_UNTIL(item->property("enabled").toBool() == true);
        WalkupAppGtestUtils::compareSpiceButtonProperties(  item, true, true, "cCopy");

        WAIT_UNTIL(item->property("constrained").toBool() == false);
    }
}

TEST_F(GivenCopyAppNonConcurrentMfpLoaded,WhenInitMediaLoaded_ClickOnCopyButtonStartsCopy)
{
    {
        WAIT_FOR_ITEM(contentItem_, "#copyLandingView");
        ASSERT_TRUE(item);
    }
    WAIT_UNTIL(stateMachine_->property("isJobSubscribed") == true);
    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);
    
    WAIT_COMPARE(stateMachine_->property("currentJobState"), 1)
    WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
    ASSERT_TRUE(item);
    mouseClick( item, Qt::LeftButton );
    scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Processing);
    
    WAIT_UNTIL(stateMachine_->property("isScannerIdle").toBool() == false);
    WAIT_UNTIL(stateMachine_->property("jobInProgress").toBool() == true);

    QQuickItem* actionButton = querySelector(contentItem_, "#mainActionButtonOfDetailPanel");
    EXPECT_EQ(actionButton->property("enabled").toBool(), false);
    
}