////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAppWorkflowGTest.cpp
 * @brief  GTest for IDCardCopyApp
 * @date   18th Feb, 2020
 * @author Shubham Khandelwal
 *
 * (C) Copyright 2019 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "gmock/gmock-matchers.h"
#include "IPathDirectory.h"
#include "MockIGuiApplicationEngine.h"
#include "MockIResourceStore.h"
#include "gmock/gmock.h"
#include "gtest/gtest.h"
#include "SpiceLoc.h"
#include "common_debug.h"

#include "IDCardCopyAppWorkflowGtest_TraceAutogen.h"
#include <vector>
#include <QQmlContext>
#include "IDCardCopyAppWorkflow.h"
#include "GTestConfigHelper.h"
#include "SpiceWorkflowFixture.h"
#include "SimplePathDirMock.h"
#include "TestSystemServices.h"
#include "IMenuResource.h"
#include "MockHomeScreen.h"
#include "SpiceDataMap.h"
#include "com_hp_cdm_service_jobTicket_version_1_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_qmlRegistration_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_sharedTypes_jobTicket_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_sharedTypes_jobTicket_qmlRegistration_generated.h"
#include "com_hp_cdm_service_media_version_1_resource_mediaCapabilities_models_generated.h"
#include "com_hp_cdm_service_media_version_1_resource_mediaCapabilities_qmlRegistration_generated.h"
#include "com_hp_cdm_service_media_version_1_resource_mediaConfiguration_models_generated.h"
#include "com_hp_cdm_service_media_version_1_resource_mediaConfiguration_qmlRegistration_generated.h"
#include "com_hp_cdm_service_scan_version_1_models_generated.h"
#include "com_hp_cdm_service_integrationTest_version_1_models_generated.h"
#include "com_hp_cdm_service_jobManagement_version_1_models_generated.h"
#include "com_hp_cdm_service_validator_version_1_models_generated.h"
#include "com_hp_cdm_service_validator_version_1_qmlRegistration_generated.h"
#include "com_hp_cdm_service_print_version_2_qmlRegistration_generated.h"
#include "com_hp_cdm_service_print_version_2_models_generated.h"

using namespace dune::spice::testing;
using namespace dune::spice::testing::qmltest;
using namespace dune::spice::testing::environment;
using namespace dune::spice::guiCore;
using namespace dune::spice::scan_1;
using namespace dune::spice::media_1;
using namespace dune::spice::jobTicket_1;
using namespace dune::spice::jobTicket_1::jobTicket;
using dune::spice::jobManagement_1::JobModel;
using dune::spice::jobManagement_1::JobsModel;
using namespace dune::spice::jobManagement_1;
using namespace dune::spice::validator_1;

using dune::copy::spice::IDCardCopyAppWorkflow;
using FeatureEnabled = dune::spice::glossary_1::FeatureEnabled::FeatureEnabled;
using TestSystemServices = dune::framework::component::TestingUtil::TestSystemServices;
using SystemServices = dune::framework::component::SystemServices;
using dune::framework::storage::path::Paths;
using PrintStatusModel =  dune::spice::print_2::StatusModel;

class GivenTestingIDCardCopyAppWorkflow : public SpiceWorkflowFixture
{
  public:
    using StatusModel = dune::spice::scan_1::StatusModel;
    GivenTestingIDCardCopyAppWorkflow() = default;

    virtual void SetUp()
    {
        SpiceWorkflowFixture::SetUp();
        SpiceWorkflowFixture::configureS();

        systemServices_ = new TestSystemServices();
        systemServices_->setConfigurationServiceBehaviour("./testResources/InteractiveOrder.fbs", "./testResources/IDCardCopyAppWorkflow.json");
        // mocking the resources folder path
        auto spm = new dune::framework::storage::path::SimplePathServicesMock();
        auto spd = new dune::framework::storage::path::SimplePathDirectory();
        spd->addPath(Paths::RESOURCE_DIRECTORY, SpiceGuiGTestEnvironment::resourceDirectory.toStdString());
        spm->setPathDirectory(spd);
        systemServices_->setPathServices(spm);

        // dictionary registration
        qmlRegisterUncreatableType<dune::spice::core::ResourceStoreTypes>(
            "spiceGuiCore", 1, 0, "ResourceStoreTypes", "ResourceStoreTypes class can not be created");
        
        // CDM mocking
        jobsListing_ =
            mockIResourceStore_->registerFakeResource<JobsModel>(new JobsModel("/cdm/jobManagement/v1/queue"));

        // register and create jobTicket resources
        createInstanceOfJobTicket(QStringLiteral("fake-9999-0000-id"));
        createInstanceOfJobTicket(QStringLiteral("fake-9999-0001-id"));
        createInstanceOfJobTicket(QStringLiteral("fake-9999-0001-id"));
        registerJobTicket(QStringLiteral("fake-9999-0000-id"));
        registerJobTicket(QStringLiteral("fake-9999-0000-id"));
        registerJobTicket(QStringLiteral("fake-9999-0001-id"));

        scanStatusModel_ = mockIResourceStore_->registerFakeResource<StatusModel>( 
            new StatusModel( "/cdm/scan/v1/status" ) );

        // CDM mocking for Media
        MediaConfigurationModel* mediaConfModel = new MediaConfigurationModel("/cdm/media/v1/configuration");

        MediaInputsModel* inputModel = new MediaInputsModel("", mediaConfModel);

        inputModel->setMediaSourceId(dune::spice::glossary_1::MediaSourceId::MediaSourceId::auto_);
        inputModel->setCurrentMediaSize(dune::spice::glossary_1::MediaSize::MediaSize::na_letter_8_dot_5x11in);
        inputModel->setCurrentMediaType(dune::spice::glossary_1::MediaType::MediaType::stationery);

        printStatusModel_ = mockIResourceStore_->registerFakeResource<PrintStatusModel>(
            new PrintStatusModel("/cdm/print/v2/status"));
        
        printStatusModel_->setPrinterState(dune::spice::print_2::status::PrinterState::PrinterState::idle);

        mediaConfModel->getInputs()->append(inputModel);

        mockIResourceStore_->registerFakeResource<MediaConfigurationModel>(mediaConfModel);

        propertyMap_ = new SpiceDataMap(QString("./testResources/generated/TestSpiceDataMap.bin"));
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty("_propertyMap", propertyMap_);
        mockIGuiApplicationEngine->getQQmlEngine()->addImportPath("qrc:/Walkup/imports");
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty(
                                        "_scanPreviewSupported", QVariant(scanPreviewSupported));

        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty(
                                "_jobConcurrencySupported", QVariant(jobConcurrency));
        
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty(
                                         "_scannerStatusModel", scanStatusModel_.get());

        propertyMap_->moveToThread(nullptr);
        // creating aut
        aut_ = std::make_shared<IDCardCopyAppWorkflow>("IDCardCopyApp");
        aut_->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices *>(systemServices_));

        // IComponent initialization
        aut_->setInterface(GET_INTERFACE_UID(dune::spice::guiCore::IGuiApplicationEngine), "",
                           static_cast<void*>(mockIGuiApplicationEngine));

        
    }

    void startApplication()
    {
        std::future<void> completionFuture;
        std::function<void()> f = [&]() { aut_->connected(nullptr, completionFuture); };
        SpiceGuiFixture::executeTask<decltype(f)>(f);
        
        aut_->start();
        GTestSignalSpy spy(aut_->getSpiceQmlIncubator(), SIGNAL(incubationFinished(bool)));
        ASSERT_TRUE(spy.waitForSignal(30000));
        application_ = aut_->getSpiceApplication();
        ASSERT_NE(application_, nullptr);
        application_->setProperty("appId", "c74293eb-04c1-4dff-b469-1c0e99fdbe8b");
        stateMachine_ = qvariant_cast<QQuickItem*>(application_->property("_stateMachine"));
        ASSERT_NE(stateMachine_, nullptr);
        EXPECT_EQ(application_->property("appId").toString(), "c74293eb-04c1-4dff-b469-1c0e99fdbe8b");

        QVariant stack = application_->property("applicationStack");
        ASSERT_FALSE(stack.isNull());
        stack_ = qvariant_cast<QQuickItem*>(stack);
        stateMachine_ = qvariant_cast<QQuickItem*>(application_->property("_stateMachine"));
    }

    /**
     * @brief Create a Instance Of Job Ticket object and set behaviour
     * 
     * @param ticketId of jobticket
     */
    void createInstanceOfJobTicket(QString ticketId)
    {
        std::shared_ptr<JobTicketModel> jobTicketModel;
        jobTicketModel = mockIResourceStore_->setCreateBehaviour<JobTicketModel>(
            new JobTicketModel(), "/cdm/jobTicket/v1/tickets", "/cdm/jobTicket/v1/tickets", "ticketId");
        fillJobTicketModel(jobTicketModel, ticketId);

        jobTicketModels_.push_back(jobTicketModel);
    }

    /**
     * @brief Create a Instance Of Job Model
     * 
     * @param jobId of jobInfoModel
     */

    void createInstanceOfJob(QString jobId)
    {
        std::shared_ptr<JobModel>   jobInfoModel;
        jobInfoModel = mockIResourceStore_->setCreateBehaviour<JobModel>(
            new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");
        fillJobInfoModel(jobInfoModel, jobId);
        jobInfoModels_.push_back(jobInfoModel);
    }

    /**
     * @brief register the fake resource of jobTicketModel
     * 
     * @param ticketId of jobTicket
     */

    void registerJobTicket(QString ticketId)
    {
        std::shared_ptr<JobTicketModel> jobTicketModel;
        jobTicketModel = mockIResourceStore_->registerFakeResource<JobTicketModel>(
            new JobTicketModel(QStringLiteral("/cdm/jobTicket/v1/tickets/%1").arg(ticketId)));
        fillJobTicketModel(jobTicketModel, ticketId);
    }

    /**
     * @brief fillJobTicketModel fills jobTicketModel received with all valid and needed info
     *  for jobTicketModel used on copy app
     * @param jobTicketModel ticket model to be fille with valid data and ticketId of JobTicket
     * @param ticketId of JobTicket
     */
    void fillJobTicketModel(std::shared_ptr<JobTicketModel> jobTicketModel, QString ticketId)
    {
        jobTicketModel->setTicketId(ticketId);

        // check parenting or destruction!!!!
        DestModel* dstModel = new DestModel();
        SrcModel*  srcModel = new SrcModel();

        ScanModel* scanModel = new ScanModel();
        scanModel->setColorMode(dune::spice::jobTicket_1::ColorModes::ColorModes::autoDetect);
        scanModel->setPlexMode(dune::spice::glossary_1::PlexMode::PlexMode::simplex);
        scanModel->setMediaSize(dune::spice::glossary_1::MediaSize::MediaSize::iso_a4_210x297mm);
        scanModel->setMediaSource(dune::spice::glossary_1::ScanMediaSourceId::ScanMediaSourceId::flatbed);
        scanModel->setResolution(dune::spice::jobTicket_1::Resolutions::Resolutions::e300Dpi);
        scanModel->setContentType(dune::spice::jobTicket_1::ContentType::ContentType::text);

        PrintModel* printModel = new PrintModel();
        printModel->setCopies(6);
        printModel->setMediaSource(dune::spice::glossary_1::MediaSourceId::MediaSourceId::tray_dash_3);
        printModel->setPlexMode(dune::spice::glossary_1::PlexMode::PlexMode::simplex);
        printModel->setCollate(dune::spice::jobTicket_1::CollateModes::CollateModes::collated);

        printModel->setMediaType(dune::spice::glossary_1::MediaType::MediaType::custom);
        printModel->setMediaSize(dune::spice::glossary_1::MediaSize::MediaSize::iso_a4_210x297mm);
        printModel->setPrintQuality(dune::spice::glossary_1::PrintQuality::PrintQuality::normal);
        printModel->setDuplexBinding(dune::spice::glossary_1::DuplexBinding::DuplexBinding::twoSidedLongEdge);

        ImageModificationsModel* imageModificationsModel = new ImageModificationsModel();
        imageModificationsModel->setExposure(4);
        imageModificationsModel->setPagesPerSheet(dune::spice::jobTicket_1::PagesPerSheet::PagesPerSheet::oneUp);
        PipelineOptionsModel* pipelineOptionsModel = new PipelineOptionsModel();

        ScalingModel* scalingModel = new ScalingModel();
        scalingModel->setYScalePercent(100);
        scalingModel->setXScalePercent(100);
        scalingModel->setScaleToFitEnabled(FeatureEnabled::true_);
        pipelineOptionsModel->setScaling(scalingModel);

        pipelineOptionsModel->setImageModifications(imageModificationsModel);
        jobTicketModel->setPipelineOptions(pipelineOptionsModel);

        srcModel->setScan(scanModel);
        dstModel->setPrint(printModel);
        jobTicketModel->setDest(dstModel);
        jobTicketModel->setSrc(srcModel);

        auto links = jobTicketModel->getLinks();
        auto link = new dune::spice::glossary_1::links::ItemModel("", jobTicketModel->getData());
        link->setRel("constraints");
        link->setHref(QStringLiteral("/cdm/jobTicket/v1/tickets/%1/constraints").arg(ticketId));
        links->append(link);

        constraintsModel_ = mockIResourceStore_->registerFakeResource<ConstraintsModel>(
            new ConstraintsModel(QStringLiteral("/cdm/jobTicket/v1/tickets/%1/constraints").arg(ticketId)));
    }

    /**
     * @brief fillScanStatusModel fills scanStatus model valid and needed info
     *  for scanStatusModel used on copy app
     * @param scanStatusModel model to be fille with valid data
     */
    void fillScanStatusModel(std::shared_ptr<StatusModel>  &scanStatusModel)
    {
        FlatbedModel* flatbedModel = new FlatbedModel();
        AdfModel*     adfModel = new AdfModel();
        adfModel->setState(dune::spice::scan_1::ScanAdfStateType::ScanAdfStateType::ScannerAdfEmpty);
        scanStatusModel->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Idle);
        scanStatusModel->setAdf(adfModel);
        scanStatusModel->setFlatbed(flatbedModel);
    }

    /**
     * @brief fill the scan status model for the ADf, GLASS
     * 
     * @param scanStatusModel object scanner status
     */
    void fillScanStatusModelProcessing(std::shared_ptr<StatusModel>  &scanStatusModel)
    {
        FlatbedModel* flatbedModel = new FlatbedModel();
        AdfModel*     adfModel = new AdfModel();
        adfModel->setState(dune::spice::scan_1::ScanAdfStateType::ScanAdfStateType::ScannerAdfLoaded);
        scanStatusModel->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Processing);
        scanStatusModel->setAdf(adfModel);
        scanStatusModel->setFlatbed(flatbedModel);
    }

    /**
     * @brief fill job info model data
     * 
     * @param jobInfoModel object of jobInfo
     * @param jobId 
     */
    void fillJobInfoModel(std::shared_ptr<JobModel> jobInfoModel, QString jobId) 
    { 
        jobInfoModel->setJobId(jobId); 
        jobInfoModel->setState(dune::spice::jobManagement_1::State::State::ready);
    }

    /**
     * @brief fill the data in JobQueue 
     * 
     */

    void fillJobQueueModel(){
        JobModel* jobData = new JobModel();

        jobData->setJobId("fake-job0-0000-id");
        jobData->setJobName("CopyJob");
        jobData->setJobType(dune::spice::jobManagement_1::JobType::JobType::copy);
        jobData->setState(dune::spice::jobManagement_1::State::State::processing);

        QObjectListModel* jobListCustom = jobsListing_->getJobList();

        jobListCustom->append(jobData);

    }


    virtual void TearDown()
    {
        aut_->quit();
        delete systemServices_;
        delete propertyMap_;
        SpiceGuiFixture::TearDown();
    }

    std::shared_ptr<StatusModel>                    scanStatusModel_;
  protected:
    QObject*                                        application_ = nullptr;
    QObject*                                        stateMachine_ = nullptr;
    QQuickItem*                                     stack_ = nullptr;
    JobModel*                                       jobInfo_ = nullptr;
    TestSystemServices*                             systemServices_ = nullptr;
    SpiceDataMap*                                   propertyMap_ = nullptr;
    std::shared_ptr<IDCardCopyAppWorkflow>          aut_;
    bool                                            scanPreviewSupported{true};
    bool                                            jobConcurrency{true};

    std::vector<std::shared_ptr<JobTicketModel>>    jobTicketModels_;
    std::vector<std::shared_ptr<JobModel>>          jobInfoModels_;
    std::shared_ptr<JobModel>                       jobInfoModel1_;
    std::shared_ptr<JobModel>                       jobInfoModel2_;
    std::shared_ptr<JobModel>                       jobInfoModel3_;

    std::shared_ptr<JobsModel>                      jobsListing_;
    std::shared_ptr<PrintStatusModel>               printStatusModel_;

    std::shared_ptr<ConstraintsModel>               constraintsModel_;
    std::shared_ptr<dune::spice::jobManagement_1::CapabilitiesModel> jobManagementCapabilities;
};


class GivenTestingIDCardCopyAppWorkflowFlatbedLoaded : public GivenTestingIDCardCopyAppWorkflow
{
  public:
    GivenTestingIDCardCopyAppWorkflowFlatbedLoaded() = default;

    void SetUp() override
    {
        GivenTestingIDCardCopyAppWorkflow::SetUp();
        fillScanStatusModel(scanStatusModel_);
        startApplication();

        //Setting the animationPath to other image, as product specific image is not accessible
        stateMachine_->setProperty("animationPath", "qrc:/images/Glyph/IDCardCopy.json");

        

        //Register jobInfomodels seperately
        jobInfoModel1_ = mockIResourceStore_->registerFakeResource<JobModel>(
            new JobModel("/cdm/jobManagement/v1/jobs/fake-job0-0000-id"));
        jobInfoModel1_->setJobId("fake-job0-0000-id"); 
        jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::created);
        jobInfoModel2_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
            new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");
        jobInfoModel2_->setJobId("fake-job0-0000-id"); 
        jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::created);
        jobInfoModel3_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
            new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");
        
        jobManagementCapabilities = mockIResourceStore_->registerFakeResource<dune::spice::jobManagement_1::CapabilitiesModel>( 
            new dune::spice::jobManagement_1::CapabilitiesModel( "/cdm/jobManagement/v1/capabilities" ) );
 
        jobManagementCapabilities->setJobConcurrencySupported(FeatureEnabled::true_,dune::spice::core::ISpiceModel::PropertyState::CACHE);
    }
};

TEST_F(GivenTestingIDCardCopyAppWorkflowFlatbedLoaded, WhenTicketModelDefined_ThenLandingScreenShowsCorrectly)
{

    WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_LANDING")
    QQuickItem* view = querySelector(stack_, "#idCopyLandingView");
    ASSERT_TRUE(view);

    WAIT_COMPARE(stateMachine_->property("jobState"), 5)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);

    {
        WAIT_COMPARE(stateMachine_->property("jobState"), 1)
    }
}

TEST_F(GivenTestingIDCardCopyAppWorkflowFlatbedLoaded,  whenCopyLandingViewLaunched_checkHeaderString)
{
    WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_LANDING")
    QQuickItem* view = querySelector(stack_, "#idCopyLandingView");
    ASSERT_TRUE(view);
    WAIT_FOR_ITEM(contentItem_, "#SpiceHeaderVar2");
    ASSERT_TRUE(item);
    auto *spiceText = item->property("customText").value<SpiceLoc *>();
    EXPECT_EQ(spiceText->getText().toStdString(), "cIDCardCopyApp");
}

TEST_F(GivenTestingIDCardCopyAppWorkflowFlatbedLoaded, WhenClickOnCopyButtonInDetailPanel_JobStarted)
{
    {
        WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_LANDING")
        QQuickItem* view = querySelector(stack_, "#idCopyLandingView");
        ASSERT_TRUE(view);
    }

    WAIT_COMPARE(stateMachine_->property("jobState"), 5)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);
    {
        WAIT_COMPARE(stateMachine_->property("jobState"), 1)
    }
    WAIT_UNTIL(stateMachine_->property("isScannerIdle").toBool() == true);
    WAIT_FOR_ITEM(contentItem_, "#copyDetailPanelButton");
    ASSERT_TRUE(item);
    mouseClick(item, Qt::LeftButton);
    {
        WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_STARTING")
        QQuickItem* view = querySelector(stack_, "#idCardCopyStartView");
        ASSERT_TRUE(view);

        QTest::qWait(100);
        auto *image = qmltest::querySelector(view, " #alertStatusImage");
        ASSERT_NE(image, nullptr);
        QString expectedIconPath = QString("qrc:/images/Graphics/IDCardCopyFrontGraph.json");
        ASSERT_EQ(expectedIconPath, image->property("images").toStringList().at(0));
    }
   

    {
        // WAIT_COMPARE(stateMachine_->property("jobState"), "ready")
        WAIT_FOR_ITEM(contentItem_, "#idCopyContinueButton");
        ASSERT_TRUE(item);
        mouseClick(item, Qt::LeftButton);
        QVariant                        var = stateMachine_->property("ticketModel");
        dune::spice::core::ISpiceModel* ticketSpiceModel = var.value<dune::spice::core::ISpiceModel*>();
        JobTicketModel*                 jobTicketModel = static_cast<JobTicketModel*>(ticketSpiceModel->getData());
        SrcModel*                       srcModel = static_cast<SrcModel*>(jobTicketModel->getSrc()->getData());
        ScanModel*                      scanModel = static_cast<ScanModel*>(srcModel->getScan()->getData());
        DestModel*                      destModel = static_cast<DestModel*>(jobTicketModel->getDest()->getData());
        PrintModel*                     printModel = static_cast<PrintModel*>(destModel->getPrint()->getData());

        GTEST_CHECKPOINTA("JOB RUNNING!\n");

        GTEST_CHECKPOINTA("ticketId %s\n", jobTicketModel->getTicketId().toStdString().c_str());
        GTEST_CHECKPOINTA("copies %d\n", (int)printModel->getCopies());
        GTEST_CHECKPOINTA("media source %d\n", (int)scanModel->getMediaSource());
        GTEST_CHECKPOINTA("media color %d\n", (int)scanModel->getColorMode());
        {
            WAIT_FOR_ITEM(contentItem_, "#SpiceToast");
            ASSERT_TRUE(item);
            QMetaObject::invokeMethod(item, "dismissed");
        }
    }
}

TEST_F(GivenTestingIDCardCopyAppWorkflowFlatbedLoaded, WhenClickOnCopyButtonInDetailPanel_JobStartedCancelButtonApear)
{
    {
        WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_LANDING")
        QQuickItem* view = querySelector(stack_, "#idCopyLandingView");
        ASSERT_TRUE(view);
    }

    WAIT_COMPARE(stateMachine_->property("jobState"), 5)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);

    {
        WAIT_COMPARE(stateMachine_->property("jobState"), 1)
    }
    
    WAIT_FOR_ITEM(contentItem_, "#copyDetailPanelButton");
    ASSERT_TRUE(item);
    mouseClick(item, Qt::LeftButton);
    {
        WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_STARTING")
        QQuickItem* view = querySelector(stack_, "#idCardCopyStartView");
        ASSERT_TRUE(view);
    }
   

    {
        WAIT_FOR_ITEM(contentItem_, "#idCopyContinueButton");
        ASSERT_TRUE(item);
        mouseClick(item, Qt::LeftButton);

        {
            WAIT_FOR_ITEM(contentItem_, "#SpiceToast");
            ASSERT_TRUE(item);
            QMetaObject::invokeMethod(item, "dismissed");
        }
    }

    fillJobQueueModel();
    {
        WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_LANDING")
        QQuickItem* view = querySelector(stack_, "#idCopyLandingView");
        ASSERT_TRUE(view);

        WAIT_FOR_ITEM(contentItem_, "#cancelButtonDetailPanel");
        ASSERT_TRUE(item);
        QQuickItem* cancelButton = querySelector(stack_, "#cancelButtonDetailPanel");
        ASSERT_EQ(cancelButton->property("visible").toBool(), true);
    }
}

TEST_F(GivenTestingIDCardCopyAppWorkflowFlatbedLoaded, WhenClickOnCopyButtonInPreviewPanel_JobStarted)
{
    WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_LANDING")
    QQuickItem* view = querySelector(stack_, "#idCopyLandingView");
    ASSERT_TRUE(view);

    WAIT_COMPARE(stateMachine_->property("jobState"), 5)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);

    WAIT_FOR_ITEM(contentItem_, "#_ExpandButton");
    ASSERT_TRUE(item);
    mouseClick(item, Qt::LeftButton);

    {
        WAIT_COMPARE(stateMachine_->property("jobState"), 1)
    }

    {
        WAIT_FOR_ITEM(contentItem_, "#copyPreviewPanelButton");
        ASSERT_TRUE(item);
        mouseClick(item, Qt::LeftButton);
    }
    
    {
        WAIT_FOR_ITEM(contentItem_, "#idCopyContinueButton");
        ASSERT_TRUE(item);
        mouseClick(item, Qt::LeftButton);
        QVariant                        var = stateMachine_->property("ticketModel");
        dune::spice::core::ISpiceModel* ticketSpiceModel = var.value<dune::spice::core::ISpiceModel*>();
        JobTicketModel*                 jobTicketModel = static_cast<JobTicketModel*>(ticketSpiceModel->getData());
        SrcModel*                       srcModel = static_cast<SrcModel*>(jobTicketModel->getSrc()->getData());
        ScanModel*                      scanModel = static_cast<ScanModel*>(srcModel->getScan()->getData());
        DestModel*                      destModel = static_cast<DestModel*>(jobTicketModel->getDest()->getData());
        PrintModel*                     printModel = static_cast<PrintModel*>(destModel->getPrint()->getData());
        GTEST_CHECKPOINTA("JOB RUNNING!\n");

        GTEST_CHECKPOINTA("ticketId %s\n", jobTicketModel->getTicketId().toStdString().c_str());
        GTEST_CHECKPOINTA("copies %d\n", (int)printModel->getCopies());
        GTEST_CHECKPOINTA("media source %d\n", (int)scanModel->getMediaSource());
        GTEST_CHECKPOINTA("media color %d\n", (int)scanModel->getColorMode());
        {
            WAIT_FOR_ITEM(contentItem_, "#SpiceToast");
            ASSERT_TRUE(item);
            QMetaObject::invokeMethod(item, "dismissed");
        }
    }
}



class GivenTestingIDCardCopyAppWorkflowScannerProcessing : public GivenTestingIDCardCopyAppWorkflow
{
  public:
    GivenTestingIDCardCopyAppWorkflowScannerProcessing() = default;

    void SetUp() override
    {
        GivenTestingIDCardCopyAppWorkflow::SetUp();
        fillScanStatusModelProcessing(scanStatusModel_);
        startApplication();

        

        //Register jobInfomodels seperately
        jobInfoModel1_ = mockIResourceStore_->registerFakeResource<JobModel>(
            new JobModel("/cdm/jobManagement/v1/jobs/fake-job0-0000-id"));
        jobInfoModel1_->setJobId("fake-job0-0000-id"); 
        jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::created);
        jobInfoModel2_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
            new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");
        jobInfoModel2_->setJobId("fake-job0-0000-id"); 
        jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::created);
        jobInfoModel3_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
            new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");
        
        jobManagementCapabilities = mockIResourceStore_->registerFakeResource<dune::spice::jobManagement_1::CapabilitiesModel>( 
            new dune::spice::jobManagement_1::CapabilitiesModel( "/cdm/jobManagement/v1/capabilities" ) );
 
        jobManagementCapabilities->setJobConcurrencySupported(FeatureEnabled::true_,dune::spice::core::ISpiceModel::PropertyState::CACHE);
    }
};


TEST_F(GivenTestingIDCardCopyAppWorkflowScannerProcessing, WhenScanIsInProcessingState_ActionButtonDisabled)
{

    WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_LANDING")
    QQuickItem* view = querySelector(stack_, "#idCopyLandingView");
    ASSERT_TRUE(view);

    WAIT_COMPARE(stateMachine_->property("jobState"), 5)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);
    {
        WAIT_COMPARE(stateMachine_->property("jobState"), 1)
        WAIT_UNTIL(stateMachine_->property("isJobInReadyState").toBool() == true);
        WAIT_FOR_ITEM(contentItem_, "#copyDetailPanelButton");
        ASSERT_TRUE(item);
        QQuickItem* actionButton = querySelector(stack_, "#copyDetailPanelButton");
        EXPECT_EQ(actionButton->property("enabled").toBool(), false);
    }
}


TEST_F(GivenTestingIDCardCopyAppWorkflowScannerProcessing, WhenScanStateChangeToIdle_ActionButtonEnabled)
{

    WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_LANDING")
    QQuickItem* view = querySelector(stack_, "#idCopyLandingView");
    ASSERT_TRUE(view);

    WAIT_COMPARE(stateMachine_->property("jobState"), 5)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);
    {
        WAIT_COMPARE(stateMachine_->property("jobState"), 1)
        WAIT_UNTIL(stateMachine_->property("isJobInReadyState").toBool() == true);
        WAIT_FOR_ITEM(contentItem_, "#copyDetailPanelButton");
        ASSERT_TRUE(item);
        QQuickItem* actionButton = querySelector(stack_, "#copyDetailPanelButton");
        EXPECT_EQ(actionButton->property("enabled").toBool(), false);
    }

    //scan status changed, Action button should be enabled now
    scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Idle);
    {
        WAIT_COMPARE(stateMachine_->property("isScannerIdle").toBool(), true)
        WAIT_FOR_ITEM(contentItem_, "#copyDetailPanelButton");
        ASSERT_TRUE(item);
        QQuickItem* actionButton = querySelector(stack_, "#copyDetailPanelButton");
        EXPECT_EQ(actionButton->property("enabled").toBool(), true);
    }
}

class GivenTestingIDCardCopyAppWorkflowFlatbedLoadedNonConcurrent : public GivenTestingIDCardCopyAppWorkflow
{
  public:
    GivenTestingIDCardCopyAppWorkflowFlatbedLoadedNonConcurrent() = default;

    void SetUp() override
    {
        jobConcurrency = false;
        GivenTestingIDCardCopyAppWorkflow::SetUp();

        fillScanStatusModel(scanStatusModel_);

        //Register jobInfomodels seperately
        jobInfoModel1_ = mockIResourceStore_->registerFakeResource<JobModel>(
            new JobModel("/cdm/jobManagement/v1/jobs/fake-job0-0000-id"));
        jobInfoModel1_->setJobId("fake-job0-0000-id"); 
        jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::created);
        jobInfoModel2_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
            new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");
        jobInfoModel2_->setJobId("fake-job0-0000-id"); 
        jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::created);
        jobInfoModel3_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
            new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");
        
        jobManagementCapabilities = mockIResourceStore_->registerFakeResource<dune::spice::jobManagement_1::CapabilitiesModel>( 
            new dune::spice::jobManagement_1::CapabilitiesModel( "/cdm/jobManagement/v1/capabilities" ) );
 
        jobManagementCapabilities->setJobConcurrencySupported(FeatureEnabled::false_,dune::spice::core::ISpiceModel::PropertyState::CACHE);

        startApplication();

        //Setting the animationPath to other image, as product specific image is not accessible
        stateMachine_->setProperty("animationPath", "qrc:/images/Glyph/IDCardCopy.json");
    }
};

TEST_F(GivenTestingIDCardCopyAppWorkflowFlatbedLoadedNonConcurrent, WhenClickOnCopyButtonInDetailPanel_JobStartedNoToastAppear)
{
    {
        WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_LANDING")
        QQuickItem* view = querySelector(stack_, "#idCopyLandingView");
        ASSERT_TRUE(view);
    }

    WAIT_COMPARE(stateMachine_->property("jobState"), 5)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);

    {
        WAIT_COMPARE(stateMachine_->property("jobState"), 1)
    }
    
    WAIT_FOR_ITEM(contentItem_, "#copyDetailPanelButton");
    ASSERT_TRUE(item);
    mouseClick(item, Qt::LeftButton);
    {
        WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_STARTING")
        QQuickItem* view = querySelector(stack_, "#idCardCopyStartView");
        ASSERT_TRUE(view);
    }
   

    {
        WAIT_FOR_ITEM(contentItem_, "#idCopyContinueButton");
        ASSERT_TRUE(item);
        mouseClick(item, Qt::LeftButton);

        {
            WAIT_COMPARE(stateMachine_->property("isConcurrent"), false)
        }
    }
}