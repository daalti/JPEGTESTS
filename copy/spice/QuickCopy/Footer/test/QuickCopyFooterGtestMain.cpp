/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   QuickCopyFooterGtestMain.cpp
 * @date   Thu, 22 Feb 2024 11:08:39 -0700
 * @brief  Component Holds different Flavours of QuickCopy.
 *
 * (C) Copyright 2024 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "QuickCopyFooter.h"

#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include "gmock/gmock-matchers.h"

#include "TestSystemServices.h"
#include "GTestConfigHelper.h"
#include "SpiceWorkflowFixture.h"
#include "MockIResourceStore.h"
#include "MockIGuiApplicationEngine.h"
#include "environmentGui.h"
#include "IPathDirectory.h"
#include "SimplePathDirMock.h"
#include <QQmlContext>
#include "MockHomeScreen.h"
#include "QmlUtils.h"

#include "com_hp_cdm_service_jobManagement_version_1_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_qmlRegistration_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_sharedTypes_jobTicket_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_sharedTypes_jobTicket_qmlRegistration_generated.h"
#include "com_hp_cdm_service_scan_version_1_models_generated.h"
#include "com_hp_cdm_service_validator_version_1_models_generated.h"
#include "com_hp_cdm_service_validator_version_1_qmlRegistration_generated.h"

#include "com_hp_cdm_domain_glossary_version_1_models_generated.h"
#include "com_hp_cdm_service_scan_version_1_models_generated.h"
#include "com_hp_cdm_service_copy_version_1_models_generated.h"
#include "SpiceLottie.h"

using namespace dune::spice::guiCore;

using QuickCopyFooter              = dune::copy::spice::QuickCopyFooter;
using TestSystemServices    = dune::framework::component::TestingUtil::TestSystemServices;
using IComponent            = dune::framework::component::IComponent;
using IComponentManager     = dune::framework::component::IComponentManager;
using SystemServices        = dune::framework::component::SystemServices;
using SysTrace              = dune::framework::core::dbg::SysTrace;
using CheckpointLevel       = SysTrace::CheckpointLevel;

using GTestConfigHelper     = dune::framework::core::gtest::GTestConfigHelper;
// using namespace dune::framework::storage::path;
using dune::framework::storage::path::Paths;
using dune::spice::jobManagement_1::JobModel;
using dune::spice::jobManagement_1::JobsModel;
using dune::spice::validator_1::ConstraintsModel;
using dune::spice::scan_1::StatusModel;
using dune::spice::jobTicket_1::JobTicketModel;
using dune::spice::scan_1::AdfModel;
using dune::spice::scan_1::FlatbedModel;
using dune::spice::jobTicket_1::ScanModel;
using dune::spice::jobTicket_1::PrintModel;
using dune::spice::jobTicket_1::jobTicket::DestModel;
using dune::spice::jobTicket_1::jobTicket::SrcModel;
using dune::spice::jobTicket_1::ScalingModel;
using dune::spice::jobTicket_1::ImageModificationsModel;
using dune::spice::jobTicket_1::jobTicket::PipelineOptionsModel;
using FeatureEnabled = dune::spice::glossary_1::FeatureEnabled::FeatureEnabled;
using element_type = dune::spice::jobManagement_1::JobModel;


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
    ::testing::AddGlobalTestEnvironment(new SpiceGuiGTestEnvironment());
    SpiceGuiFixture::warningsAsErrorsProgram = false;

    dune::spice::guiCore::QmlUtils::registerResource(SpiceGuiGTestEnvironment::resourceDirectory + "/workflow.rcc");
    qmlRegisterType<dune::spice::lottie::SpiceLottieValue>("spiceux", 1, 0, "SpiceLottieValue");
    dune::spice::guiCore::QmlUtils::setDefaultTestTheme("darkTheme"); 

    return RUN_ALL_TESTS();
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenANewQuickCopyFooter : public ::testing::Test
//
///////////////////////////////////////////////////////////////////////////////

class GivenANewQuickCopyFooter : public SpiceWorkflowFixture
{
  public:
   
    GivenANewQuickCopyFooter() : component_(nullptr), systemServices_(nullptr), componentManager_(nullptr) {};

    void SetUp() override{
        SpiceWorkflowFixture::SetUp();
        systemServices_ = new TestSystemServices();
        systemServices_->setConfigurationServiceBehaviour("./testResources/QuickCopyFooterConfig.fbs", "./testResources/QuickCopyFooterTestData.json");

        // mocking the resources folder path
        auto spm = new dune::framework::storage::path::SimplePathServicesMock();
        auto spd = new dune::framework::storage::path::SimplePathDirectory();
        spd->addPath(Paths::RESOURCE_DIRECTORY, SpiceGuiGTestEnvironment::resourceDirectory.toStdString());
        spm->setPathDirectory(spd);
        systemServices_->setPathServices(spm);

        mockHomeScreenViewObject_ = new MockHomeScreenViewObject();
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty("_homeFooterView",mockHomeScreenViewObject_);

        component_ = new QuickCopyFooter("myInstance");
        ASSERT_NE(nullptr, component_);
    }

    void TearDown() override{
        SpiceWorkflowFixture::TearDown();
        delete component_;
        delete systemServices_;
        mockHomeScreenViewObject_->deleteLater();
    }


  protected:

    dune::copy::spice::QuickCopyFooter                          * component_;
    TestSystemServices                              * systemServices_;
    dune::framework::component::IComponentManager   * componentManager_;
    QObject*                                        mockHomeScreenViewObject_ {nullptr};

};



TEST_F(GivenANewQuickCopyFooter, WhenInitializeIsCalled_TheComponentGetsInitialized)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_);

    // Add here the checks about the expected internal status of the component after initialize().
    // Example:
    // - Check that the internal variables are initialized to the right values
    // - Check that the CSF configuration has been correctly read and contains accepted values
    // - ...
}

TEST_F(GivenANewQuickCopyFooter, WhenTheConnectSequenceIsCalled_TheComponentGetsConnected)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));
    comp->setInterface(GET_INTERFACE_UID(dune::spice::guiCore::IGuiApplicationEngine), "", static_cast<void*>(mockIGuiApplicationEngine));
    // fill here any setInterface required

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }
}


///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedQuickCopyFooter : Do here tests of public api
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedQuickCopyFooter :public GivenANewQuickCopyFooter
{
  public:

    GivenAConnectedQuickCopyFooter() {};

    virtual void SetUp() override;

    virtual void TearDown() override;
  protected:
    std::shared_ptr<dune::spice::copy_1::ConfigurationModel> copyConfiguration_{nullptr};
};

void GivenAConnectedQuickCopyFooter::SetUp()
{
    GivenANewQuickCopyFooter::SetUp();

    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    component_->setInterface(GET_INTERFACE_UID(dune::spice::guiCore::IGuiApplicationEngine), "",
                            static_cast<void*>(mockIGuiApplicationEngine));

    // fill here any setInterface required
    copyConfiguration_ = mockIResourceStore_->registerFakeResource<dune::spice::copy_1::ConfigurationModel>( new dune::spice::copy_1::ConfigurationModel("/cdm/copy/v1/configuration"));
    copyConfiguration_->setCopyEnabled(FeatureEnabled::true_);
    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

}

void GivenAConnectedQuickCopyFooter::TearDown()
{
    GivenANewQuickCopyFooter::TearDown();
}

TEST_F(GivenAConnectedQuickCopyFooter, WhenTheHomescreenGetsReady_QuickCopyFooterComponentIsInitialized)
{
    auto homeScreenView = dune::spice::guiCore::QmlUtils::createObject(mockIGuiApplicationEngine->getQQmlEngine(), (QStringLiteral("file://%1/testResources/MockHomeScreenView.qml").arg(QDir::currentPath())));
    mockHomeScreenViewObject_->setProperty("view",QVariant::fromValue( homeScreenView));

    auto footerRightComonent = homeScreenView->property("homeScreenFooterRightComponent");
    ASSERT_TRUE(footerRightComonent.isNull());
    
    QMetaObject::invokeMethod(homeScreenView, "emitHomescreenViewReady");
    QTest::qWait(10);
    
    footerRightComonent = homeScreenView->property("homeScreenFooterRightComponent");
    ASSERT_FALSE(footerRightComonent.isNull());
    ASSERT_EQ(qvariant_cast<QQmlComponent*>(footerRightComonent)->url().toString(), "qrc:/QuickCopy/QuickCopyFooter.qml");    
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedQuickCopyFooterReadyToCallShutdown : shutdown case.
// Dummy class that inherits from GivenAConnectedQuickCopyFooter in order to reuse code
// and enable parametrized tests. 
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedQuickCopyFooterReadyToCallShutdown : public GivenAConnectedQuickCopyFooter,
                           public ::testing::WithParamInterface<IComponent::ShutdownCause>
{

};


TEST_P(GivenAConnectedQuickCopyFooterReadyToCallShutdown, whenShutdownIsCalled_TheComponentGetsShutdown)
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

    // Add here the checks about the expected internal status of the component after shutdown():
    // Example:
    // - Check that the finalization operations that use the received interfaces have been called (EXPECT_CALL)
    // - Check that all the internal threads have been stopped / destroyed.
    // - Check that the memory allocated by this component has been freed.
    // - ...
}

INSTANTIATE_TEST_CASE_P(InstantiationName, GivenAConnectedQuickCopyFooterReadyToCallShutdown, ::testing::Values(
 IComponent::ShutdownCause(IComponent::ShutdownCause::POWER_OFF),
 IComponent::ShutdownCause(IComponent::ShutdownCause::REBOOT),
 IComponent::ShutdownCause(IComponent::ShutdownCause::SEVERE_ERROR),
 IComponent::ShutdownCause(IComponent::ShutdownCause::EMERGENCY_ERROR),
 IComponent::ShutdownCause(IComponent::ShutdownCause::CRITICAL_ERROR)
));



class GivenAQuickCopyFooterView : public SpiceWorkflowFixture
{
  public:
    virtual void SetUp() override
    {
        SpiceWorkflowFixture::SetUp();
        engine_->addImportPath("qrc:/QuickCopy/imports");
        dune::spice::guiCore::QmlUtils::registerResource(SpiceGuiGTestEnvironment::resourceDirectory + "/0x93070d/QuickCopy.rcc");
        jobsListing_ =
                mockIResourceStore_->registerFakeResource<JobsModel>(new JobsModel("/cdm/jobManagement/v1/queue"));

        // register and create jobTicket resources
        createInstanceOfJobTicket(QStringLiteral("fake-9999-0000-id"));
        registerJobTicket(QStringLiteral("fake-9999-0000-id"));

        scanStatusModel_ = mockIResourceStore_->registerFakeResource<StatusModel>( 
                new StatusModel( "/cdm/scan/v1/status" ) );

        constraintsModel1_ = mockIResourceStore_->registerFakeResource<ConstraintsModel>(
                new ConstraintsModel(QStringLiteral("/cdm/jobTicket/v1/configuration/defaults/copy/constraints")));

        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty(
                                            "_scannerStatusModel", scanStatusModel_.get());
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty(
                                    "_jobConcurrencySupported", QVariant(jobConcurrency));

        fillScanStatusModelFlatbedLoaded(scanStatusModel_);

        jobInfoModel1_ = mockIResourceStore_->registerFakeResource<JobModel>(
                new JobModel("/cdm/jobManagement/v1/jobs/fake-job0-0000-id"));
        jobInfoModel1_->setJobId("fake-job0-0000-id"); 
        jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::created);

        jobInfoModel2_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
                new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");
        jobInfoModel2_->setJobId("fake-job0-0000-id"); 
        jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::created);
    
        layout1_ = pushViewLocal("testResources/QuickCopyFooterTestView.qml", QDir::currentPath());
    }
    virtual void TearDown() override
    {
        SpiceWorkflowFixture::TearDown();
    }

    void createInstanceOfJobTicket(QString ticketId)
    {
        jobTicketModel1_ = mockIResourceStore_->setCreateBehaviour<JobTicketModel>(
            new JobTicketModel(), "/cdm/jobTicket/v1/tickets", "/cdm/jobTicket/v1/tickets", "ticketId");
        fillJobTicketModel(jobTicketModel1_, ticketId);
    }

    void registerJobTicket(QString ticketId)
    {
        jobTicketModel2_  = mockIResourceStore_->registerFakeResource<JobTicketModel>(
            new JobTicketModel(QStringLiteral("/cdm/jobTicket/v1/tickets/%1").arg(ticketId)));
        fillJobTicketModel(jobTicketModel2_, ticketId);
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
     * @brief fill the scan status model for the ADf, GLASS
     * 
     * @param scanStatusModel object scanner status
     */
    void fillScanStatusModelFlatbedLoaded(std::shared_ptr<StatusModel>  &scanStatusModel)
    {
        
        FlatbedModel* flatbedModel = new FlatbedModel();
        AdfModel*     adfModel = new AdfModel();
        adfModel->setState(dune::spice::scan_1::ScanAdfStateType::ScanAdfStateType::ScannerAdfEmpty);
        flatbedModel->setState(dune::spice::scan_1::ScanMediaPathStateType::ScanMediaPathStateType::loaded);
        scanStatusModel->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Idle);
        scanStatusModel->setAdf(adfModel);
        scanStatusModel->setFlatbed(flatbedModel);
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

    virtual void fillJobTicketModel(std::shared_ptr<JobTicketModel> &jobTicketModel, QString ticketId)
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

    }

    protected:
        std::shared_ptr<JobTicketModel>                 jobTicketModel1_;
        std::shared_ptr<JobTicketModel>                 jobTicketModel2_;
        std::shared_ptr<JobModel>                       jobInfoModel1_;
        std::shared_ptr<JobModel>                       jobInfoModel2_;
        std::shared_ptr<JobsModel>                      jobsListing_;
        std::shared_ptr<StatusModel>                    scanStatusModel_;
        std::shared_ptr<ConstraintsModel>               constraintsModel1_;
        bool                                            jobConcurrency{true};
        QQuickItem*                                     layout1_{nullptr};
};

TEST_F(GivenAQuickCopyFooterView, whenClickedOnQuickCopyButton_JobHasAutoStarted)
{
    WAIT_FOR_ITEM(layout1_, "#copyQuickFooter");
    auto buttonView = qmltest::querySelector(layout1_, "#QuickCopyButton");
    qmltest::mouseClick(buttonView, Qt::LeftButton);
    QTest::qWait(5);
    EXPECT_TRUE(jobInfoModel2_->getAutoStart() == FeatureEnabled::true_);
    layout1_->deleteLater();
}

TEST_F(GivenAQuickCopyFooterView, whenScanIsInProcessingState_ActionButtonDisabled)
{
    fillScanStatusModelProcessing(scanStatusModel_);
    WAIT_FOR_ITEM(layout1_, "#copyQuickFooter");
    auto buttonView = qmltest::querySelector(layout1_, "#QuickCopyButton");
    EXPECT_TRUE(buttonView->isEnabled() == false);
    layout1_->deleteLater();
}

TEST_F(GivenAQuickCopyFooterView, WhenClickedOnQuickCopyButton_VerifyNumberOfCopies)
{
    WAIT_FOR_ITEM(layout1_, "#copyQuickFooter");
    auto quickCopySpinBox = qmltest::querySelector(layout1_, "#quickCopySpinBox");
    quickCopySpinBox->setProperty("value", 10);
    auto buttonView = qmltest::querySelector(layout1_, "#QuickCopyButton");
    qmltest::mouseClick(buttonView, Qt::LeftButton);
    QTest::qWait(5);
    DestModel*      destModel = static_cast<DestModel*>(jobTicketModel1_->getDest()->getData());
    PrintModel*     printModel = static_cast<PrintModel*>(destModel->getPrint()->getData());
    EXPECT_TRUE(printModel->getCopies() == 10);
    layout1_->deleteLater();
}

SETUP_LAYOUT_TEST(GivenAQuickCopyFooterView)
TEST_P(GivenAQuickCopyFooterView_P, homeScreenFooterView)
{
    WAIT_FOR_ITEM(layout1_, "#copyQuickFooter");
    ASSERT_TRUE(item);
    {
        WAIT_FOR_ITEM(layout1_, "#QuickCopyButton #ButtonControl #ContentItem #ButtonControlIcon")
        ASSERT_TRUE(item);
    }
    EXPECT_TRUE(qmltest::validateScreenCapture());
    layout1_->deleteLater();
}

class GivenAQuickCopyComponentHandler : public SpiceWorkflowFixture
{
    virtual void SetUp() override
    {
        SpiceWorkflowFixture::SetUp();
        engine_->addImportPath("qrc:/QuickCopy/imports");
        dune::spice::guiCore::QmlUtils::registerResource(SpiceGuiGTestEnvironment::resourceDirectory + "/0x93070d/QuickCopy.rcc");

        copyConfiguration_ = mockIResourceStore_->registerFakeResource<dune::spice::copy_1::ConfigurationModel>( new dune::spice::copy_1::ConfigurationModel("/cdm/copy/v1/configuration"));
        copyConfiguration_->setCopyEnabled(FeatureEnabled::true_);
        mockHomeScreenViewObject_ = new MockHomeScreenViewObject();
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty("_homeFooterView",mockHomeScreenViewObject_);
        
        auto homeScreenView = dune::spice::guiCore::QmlUtils::createObject(mockIGuiApplicationEngine->getQQmlEngine(), (QStringLiteral("file://%1/testResources/MockHomeScreenView.qml").arg(QDir::currentPath())));
        mockHomeScreenViewObject_->setProperty("view",QVariant::fromValue( homeScreenView));
        quickCopyComponentHandler_ = dune::spice::guiCore::QmlUtils::createObject(mockIGuiApplicationEngine->getQQmlEngine(), "qrc:/QuickCopy/QuickCopyComponentHandler.qml");
    }
    virtual void TearDown() override
    {
        if(quickCopyComponentHandler_) quickCopyComponentHandler_->deleteLater();
        if(mockHomeScreenViewObject_) mockHomeScreenViewObject_->deleteLater();
        SpiceWorkflowFixture::TearDown();
    }

    protected:
    QObject *quickCopyComponentHandler_{nullptr};
    QObject* mockHomeScreenViewObject_ {nullptr};
    std::shared_ptr<dune::spice::copy_1::ConfigurationModel> copyConfiguration_{nullptr};
};

TEST_F(GivenAQuickCopyComponentHandler, whenCopyEnabledStateChangeHomeScreenQuickCopyFooterIsChanged)
{
    auto homeScreenView = qvariant_cast<QQuickItem*>(mockHomeScreenViewObject_->property("view"));
    QMetaObject::invokeMethod(homeScreenView, "emitHomescreenViewReady");
    WAIT_UNTIL( qvariant_cast<QQmlComponent*>(homeScreenView->property("homeScreenFooterRightComponent")) != nullptr);
    auto footerRightComonent = homeScreenView->property("homeScreenFooterRightComponent");
    ASSERT_FALSE(footerRightComonent.isNull());
    ASSERT_EQ(qvariant_cast<QQmlComponent*>(footerRightComonent)->url().toString(), "qrc:/QuickCopy/QuickCopyFooter.qml");

    QTest::qWait(10);
    copyConfiguration_->setCopyEnabled(FeatureEnabled::false_);
    footerRightComonent = homeScreenView->property("homeScreenFooterRightComponent");
    ASSERT_TRUE(footerRightComonent.isNull());

    copyConfiguration_->setCopyEnabled(FeatureEnabled::true_);
    footerRightComonent = homeScreenView->property("homeScreenFooterRightComponent");
    ASSERT_FALSE(footerRightComonent.isNull());
    ASSERT_EQ(qvariant_cast<QQmlComponent*>(footerRightComonent)->url().toString(), "qrc:/QuickCopy/QuickCopyFooter.qml");
}
