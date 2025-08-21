////////////////////////////////////////////////////////////////////////////////
/**
 * @file   IDCardCopyAppProSelectGTest.cpp
 * @brief  GTest for IDCardCopyApp
 * @date   5th Apr, 2021
 * @author Gwangeun Sim (gwangeun.sim@hp.com)
 *
 * (C) Copyright 2019 HP Inc
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "gmock/gmock-matchers.h"
#include <QQmlContext>
#include "IPathDirectory.h"
#include "MenuNodesConverter.h"
#include "MockIGuiApplicationEngine.h"
#include "MockIResourceStore.h"
#include "gmock/gmock.h"
#include "gtest/gtest.h"

#include "IDCardCopyAppProSelectGtest_TraceAutogen.h"

#include "GTestConfigHelper.h"
#include "IDCardCopyAppProSelect.h"
#include "IMenuResource.h"
#include "MockHomeScreen.h"
#include "SpiceDataMap.h"
#include "SpiceProSelectFixture.h"
#include "SimplePathDirMock.h"
#include "TestSystemServices.h"
#include "com.hp.cdm.service.jobTicket.version.1.serviceDefinition_autogen.h"
#include "com_hp_cdm_domain_glossary_version_1_models_generated.h"
#include "com_hp_cdm_service_integrationTest_version_1_models_generated.h"
#include "com_hp_cdm_service_jobManagement_version_1_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_qmlRegistration_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_sharedTypes_jobTicket_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_sharedTypes_jobTicket_qmlRegistration_generated.h"
#include "com_hp_cdm_service_media_version_1_resource_mediaCapabilities_models_generated.h"
#include "com_hp_cdm_service_media_version_1_resource_mediaCapabilities_qmlRegistration_generated.h"
#include "com_hp_cdm_service_media_version_1_resource_mediaConfiguration_models_generated.h"
#include "com_hp_cdm_service_media_version_1_resource_mediaConfiguration_qmlRegistration_generated.h"
#include "com_hp_cdm_service_scan_version_1_models_generated.h"
#include "com_hp_cdm_service_shortcut_version_1_models_generated.h"
#include "com_hp_cdm_service_shortcut_version_1_qmlRegistration_generated.h"
#include "com_hp_cdm_service_shortcut_version_1_sharedTypes_shortcut_models_generated.h"
#include "com_hp_cdm_service_shortcut_version_1_sharedTypes_shortcut_qmlRegistration_generated.h"

using namespace dune::spice::testing;
using namespace dune::spice::testing::qmltest;
using namespace dune::spice::testing::environment;
using namespace dune::spice::guiCore;
using namespace dune::spice::jobTicket_1;
using namespace dune::spice::jobTicket_1::jobTicket;
using namespace dune::spice::jobManagement_1;
using namespace dune::spice::media_1;
using namespace dune::spice::shortcut_1;
using namespace dune::spice::shortcutSharedTypesShortcut_1;
using namespace dune::spice::scan_1;
using dune::spice::shortcut_1::ShortcutModel;
using dune::spice::shortcut_1::ShortcutsModel;
using FeatureEnabled = dune::spice::glossary_1::FeatureEnabled::FeatureEnabled;
using TestSystemServices = dune::framework::component::TestingUtil::TestSystemServices;
using SystemServices = dune::framework::component::SystemServices;
using dune::framework::storage::path::Paths;

using dune::copy::spice::IDCardCopyAppProSelect;

class GivenTestingIDCardCopyAppProSelect : public SpiceProSelectFixture
{
  public:
    GivenTestingIDCardCopyAppProSelect() = default;
    virtual ~GivenTestingIDCardCopyAppProSelect() {}

    virtual void SetUp()
    {
        SpiceProSelectFixture::SetUp();
	    
        systemServices_ = new TestSystemServices();
        // mocking the resources folder path
        auto spm = new dune::framework::storage::path::SimplePathServicesMock();
        auto spd = new dune::framework::storage::path::SimplePathDirectory();
        spd->addPath(Paths::RESOURCE_DIRECTORY, SpiceGuiGTestEnvironment::resourceDirectory.toStdString());
        spm->setPathDirectory(spd);
        systemServices_->setPathServices(spm);        

        // dictionary registration
        qmlRegisterUncreatableType<dune::spice::core::ResourceStoreTypes>(
            "spiceGuiCore", 1, 0, "ResourceStoreTypes", "ResourceStoreTypes class can not be created");

        jobTicketModel_ = mockIResourceStore_->setCreateBehaviour<JobTicketModel>(
            new JobTicketModel(), "/cdm/jobTicket/v1/tickets", "/cdm/jobTicket/v1/tickets", "ticketId");

        jobTicketModel2_ = mockIResourceStore_->setCreateBehaviour<JobTicketModel>(
            new JobTicketModel(), "/cdm/jobTicket/v1/tickets", "/cdm/jobTicket/v1/tickets", "ticketId");
        fillJobTicketModel(jobTicketModel_, QStringLiteral("fake-9999-0000-id"));
        fillJobTicketModel(jobTicketModel2_, QStringLiteral("fake-9999-0001-id"));

        jobInfoModel_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
            new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");

        // CDM mocking for Media
        MediaConfigurationModel* mediaConfModel = new MediaConfigurationModel("/cdm/media/v1/configuration");

        MediaInputsModel* inputModel = new MediaInputsModel("", mediaConfModel);

        inputModel->setMediaSourceId(dune::spice::glossary_1::MediaSourceId::MediaSourceId::auto_);
        inputModel->setCurrentMediaSize(dune::spice::glossary_1::MediaSize::MediaSize::na_letter_8_dot_5x11in);
        inputModel->setCurrentMediaType(dune::spice::glossary_1::MediaType::MediaType::stationery);

        mediaConfModel->getInputs()->append(inputModel);

        mockIResourceStore_->registerFakeResource<MediaConfigurationModel>(mediaConfModel);

        MenuNodeConverter menuNodesConverter;
        auto menuNode = menuNodesConverter.getFlatbufferData("./testResources/MenuNodes.fbs","./testResources/TestMenuNodes.json");
        menuResource_ = IMenuResource::createResourceForCSF(std::move(menuNode));
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty("_menuResource", menuResource_);
        propertyMap_ = new SpiceDataMap(QString("testResources/generated/TestSpiceDataMap.bin"));
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty("_propertyMap", propertyMap_);


        MockApplicationItem* mockHomeScreen_ = nullptr;

        mockHomeScreen_ = new MockApplicationItem();
        mockHomeScreen_->setApplicationName("IDCardCopyApp");

        // creating aut
        aut_ = std::make_shared<IDCardCopyAppProSelect>("IDCardCopyApp");
        aut_->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));
        ASSERT_NE(aut_, nullptr);

        aut_->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices *>(systemServices_));
        // IComponent initialization
        aut_->setInterface(GET_INTERFACE_UID(dune::spice::guiCore::IGuiApplicationEngine), "",
                           static_cast<void*>(mockIGuiApplicationEngine));

        std::future<void>     completionFuture;
        std::function<void()> f = [&]() { aut_->connected(nullptr, completionFuture); };
        SpiceGuiFixture::executeTask<decltype(f)>(f);

        GTestSignalSpy spy(aut_->getSpiceQmlIncubator(), SIGNAL(incubationFinished(bool)));

        aut_->start();

        ASSERT_TRUE(spy.waitForSignal(30000));

        application_ = aut_->getSpiceApplication();
        ASSERT_NE(application_, nullptr);
        application_->setProperty("appId", "c74293eb-04c1-4dff-b469-1c0e99fdbe8b");
        stateMachine_ = qvariant_cast<QQuickItem*>(application_->property("_stateMachine"));
        ASSERT_NE(stateMachine_, nullptr);
        EXPECT_EQ(application_->property("appId").toString(), "c74293eb-04c1-4dff-b469-1c0e99fdbe8b");
    }

    /**
     * @brief fillJobTicketModel fills jobTicketModel received with all valid and needed info
     *  for jobTicketModel used on copy app
     * @param jobTicketModel ticket model to be fille with valid data
     */
    void fillJobTicketModel(std::shared_ptr<JobTicketModel> jobTicketModel, QString rel)
    {
        jobTicketModel->setTicketId(rel);

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
        PipelineOptionsModel* pipelineOptionsModel = new PipelineOptionsModel();
        pipelineOptionsModel->setImageModifications(imageModificationsModel);
        jobTicketModel_->setPipelineOptions(pipelineOptionsModel);

        srcModel->setScan(scanModel);
        dstModel->setPrint(printModel);
        jobTicketModel->setDest(dstModel);
        jobTicketModel->setSrc(srcModel);
    }

    /**
     * @brief fill jobInfo Details
     * 
     * @param jobInfoModel 
     * @param rel 
     */
    void fillJobInfoModel(std::shared_ptr<JobModel> jobInfoModel, QString rel) { jobInfoModel->setJobId(rel); }

    void printPropertyList()
    {
        const QMetaObject* meta = stateMachine_->metaObject();
        int                n = meta->propertyCount();
        for (int i = 0; i < n; ++i)
        {
            GTEST_CHECKPOINTA("dynamic property listing: %s\t", meta->property(i).name());
            QVariant var = stateMachine_->property(meta->property(i).name());
            GTEST_CHECKPOINTA("type %s\n", var.typeName());
        }
    }

    virtual void TearDown()
    {
        aut_->quit();
        delete systemServices_;
        SpiceProSelectFixture::TearDown();

        delete menuResource_;
        delete propertyMap_;
    }

  protected:
    QObject*                                application_ = nullptr;
    QObject*                                stateMachine_ = nullptr;
    std::shared_ptr<IDCardCopyAppProSelect> aut_;

    std::shared_ptr<JobTicketModel>         jobTicketModel_;
    std::shared_ptr<JobTicketModel>         jobTicketModel2_;
    std::shared_ptr<JobModel>               jobInfoModel_;
    std::shared_ptr<JobTicketModel>         jobTicketModel3_;

    JobModel*                               jobInfo_ = nullptr;
    IMenuResource*                          menuResource_ = nullptr;
    SpiceDataMap*                           propertyMap_ = nullptr;
    TestSystemServices*                     systemServices_ = nullptr;
};

class GivenIDCardCopyAppProSelectIsStarted : public GivenTestingIDCardCopyAppProSelect
{
  public:
    GivenIDCardCopyAppProSelectIsStarted() = default;

    void SetUp() override
    {
        GivenTestingIDCardCopyAppProSelect::SetUp();

        fillJobInfoModel(jobInfoModel_, "fake-job0-0000-id");

        jobInfo_ = new JobModel("/cdm/jobManagement/v1/jobs/fake-job0-0000-id");
        mockIResourceStore_->registerFakeResource<JobModel>(jobInfo_);

        {
            WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_LANDING")
            QQuickItem* view = querySelector(contentItem_, "#idCardCopyLandingView");
            ASSERT_TRUE(view);
        }
    }
};

TEST_F(GivenIDCardCopyAppProSelectIsStarted, WhenTicketModelDefined_ThenLandingScreenShowsCorrectly)
{
    {
        WAIT_FOR_ITEM(contentItem_, "SpiceText[text=cIDCardCopyApp]");
        ASSERT_TRUE(item);
    }
}

TEST_F(GivenIDCardCopyAppProSelectIsStarted, WhenClickedOnCopyButton_ThenFirstPromptCome)
{
    {
        WAIT_FOR_ITEM(contentItem_, "#IDCardCopyButton");
        ASSERT_TRUE(item);
        mouseClick(item, Qt::LeftButton);
    }

    WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_STARTING")
    QQuickItem* view = querySelector(contentItem_, "#idCardCopyStartingView");
    ASSERT_TRUE(view);
}

TEST_F(GivenIDCardCopyAppProSelectIsStarted, WhenLandingState_ThenSelectCopyStateIsReachedAndScanSourceIsSelected)
{
    printPropertyList();

    QVariant                        var = stateMachine_->property("ticketModel");
    dune::spice::core::ISpiceModel* ticketSpiceModel = var.value<dune::spice::core::ISpiceModel*>();
    JobTicketModel*                 jobTicketModel = static_cast<JobTicketModel*>(ticketSpiceModel->getData());
    SrcModel*                       srcModel = static_cast<SrcModel*>(jobTicketModel->getSrc()->getData());
    ScanModel*                      scanModel = static_cast<ScanModel*>(srcModel->getScan()->getData());
    DestModel*                      destModel = static_cast<DestModel*>(jobTicketModel->getDest()->getData());
    PrintModel*                     printModel = static_cast<PrintModel*>(destModel->getPrint()->getData());

    GTEST_CHECKPOINTA("ticketId %s\n", jobTicketModel->getTicketId().toStdString().c_str());
    GTEST_CHECKPOINTA("copies %d\n", (int)printModel->getCopies());
    GTEST_CHECKPOINTA("media source %d\n", (int)scanModel->getMediaSource());
    GTEST_CHECKPOINTA("media color %d\n", (int)scanModel->getColorMode());

    // check pre-condition: Flatbed is set as a default source
    ASSERT_TRUE(scanModel->getMediaSource() ==
                dune::spice::glossary_1::ScanMediaSourceId::ScanMediaSourceId::flatbed);

    {
        WAIT_FOR_ITEM(contentItem_, "#IDCardCopyButton");
        ASSERT_TRUE(item);
        mouseClick(item, Qt::LeftButton);
    }

    WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_STARTING")
    QQuickItem* view = querySelector(contentItem_, "#idCardCopyStartingView");
    ASSERT_TRUE(view);
    {
        WAIT_FOR_ITEM(contentItem_, "#idCardContinueButton");
        ASSERT_TRUE(item);
        mouseClick(item, Qt::LeftButton);
    }
    
    WAIT_COMPARE(stateMachine_->property("activeState"), "ID_CARD_COPY_LANDING")
    WAIT_FOR_ITEM(contentItem_, "#IDCardCopyButton");
    ASSERT_TRUE(item);
    WAIT_UNTIL(item->property("enabled").toBool() == false);

    GTEST_CHECKPOINTA("JOB RUNNING!\n");

    GTEST_CHECKPOINTA("ticketId %s\n", jobTicketModel->getTicketId().toStdString().c_str());
    GTEST_CHECKPOINTA("copies %d\n", (int)printModel->getCopies());
    GTEST_CHECKPOINTA("media source %d\n", (int)scanModel->getMediaSource());
    GTEST_CHECKPOINTA("media color %d\n", (int)scanModel->getColorMode());

    jobInfoModel_->setState(dune::spice::jobManagement_1::State::State::completed);

    WAIT_UNTIL(item->property("enabled").toBool() == true);
}


TEST_F(GivenIDCardCopyAppProSelectIsStarted, WhenTicketModelDefined_ThenLandingScreenShowsNoCorrectly)
{
    {
        WAIT_FOR_ITEM(contentItem_, "SpiceTumbler[value=6]");
        ASSERT_TRUE(item);
    }
}