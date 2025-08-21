////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAppProSelectGTest.cpp
 * @brief  GTest for CopyApp
 * @date   18th Feb, 2020
 * @author Hectorn Sanchez Gonzalez (hector.sanchez-gonzalez@hp.com)
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

#include "CopyAppProSelectGtest_TraceAutogen.h"
#include "SpiceLoc.h"
#include "CopyAppProSelect.h"
#include "GTestConfigHelper.h"
#include "IMenuResource.h"
#include "MockHomeScreen.h"
#include "SpiceDataMap.h"
#include "SimplePathDirMock.h"
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
#include "com_hp_cdm_service_validator_version_1_models_generated.h"
#include "com_hp_cdm_service_validator_version_1_qmlRegistration_generated.h"

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
using namespace dune::spice::validator_1;
using dune::spice::shortcut_1::ShortcutModel;
using dune::spice::shortcut_1::ShortcutsModel;
using FeatureEnabled = dune::spice::glossary_1::FeatureEnabled::FeatureEnabled;
using TestSystemServices = dune::framework::component::TestingUtil::TestSystemServices;
using SystemServices = dune::framework::component::SystemServices;
using dune::framework::storage::path::Paths;

using dune::copy::spice::CopyAppProSelect;
using TestSystemServices = dune::framework::component::TestingUtil::TestSystemServices;
using dune::framework::storage::path::Paths;

class GivenTestingCopyAppProSelect : public SpiceProSelectFixture
{
  public:
    using StatusModel = dune::spice::scan_1::StatusModel;

    GivenTestingCopyAppProSelect() = default;
    virtual ~GivenTestingCopyAppProSelect() {}

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

        dune::spice::shortcut_1::CapabilitiesModel* shortcutCapModel =
            new dune::spice::shortcut_1::CapabilitiesModel("/cdm/shortcut/v1/capabilities");
        // Reading supported sizes list
        QVariantListModel* supportedShortcutTypes = shortcutCapModel->getDeviceShortcutsJobTypeSupported();

        // Adding media size to supported sizes list
        supportedShortcutTypes->append(static_cast<std::int16_t>(dune::spice::jobManagement_1::JobType::JobType::copy));
        // Registering fake capabilities model
        mockIResourceStore_->registerFakeResource<dune::spice::shortcut_1::CapabilitiesModel>(shortcutCapModel);
        // dictionary registration
        qmlRegisterUncreatableType<dune::spice::core::ResourceStoreTypes>(
            "spiceGuiCore", 1, 0, "ResourceStoreTypes", "ResourceStoreTypes class can not be created");

        jobTicketModel_ = mockIResourceStore_->setCreateBehaviour<JobTicketModel>(
            new JobTicketModel(), "/cdm/jobTicket/v1/tickets", "/cdm/jobTicket/v1/tickets", "ticketId");

        jobTicketModel2_ = mockIResourceStore_->setCreateBehaviour<JobTicketModel>(
            new JobTicketModel(), "/cdm/jobTicket/v1/tickets", "/cdm/jobTicket/v1/tickets", "ticketId");
        fillJobTicketModel(jobTicketModel_, QStringLiteral("fake-9999-0000-id"));
        fillJobTicketModel(jobTicketModel2_, QStringLiteral("fake-9999-0001-id"));
        jobTicketModel3_ = mockIResourceStore_->registerFakeResource<JobTicketModel>(
            new JobTicketModel("/cdm/jobTicket/v1/tickets/fake-9999-0001-id"));
        fillJobTicketModel(jobTicketModel3_, QStringLiteral("fake-9999-0001-id"));
        jobTicketModel4_ = mockIResourceStore_->registerFakeResource<JobTicketModel>(
            new JobTicketModel("/cdm/jobTicket/v1/tickets/fake-9999-0000-id"));
        fillJobTicketModel(jobTicketModel4_, QStringLiteral("fake-9999-0000-id"));

        jobInfoModel_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
            new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");

        jobInfoModel2_ = mockIResourceStore_->setCreateBehaviour<JobModel>(
            new JobModel(), "/cdm/jobManagement/v1/jobs", "/cdm/jobManagement/v1/jobs", "jobId");

        scanStatus_ = new StatusModel("/cdm/scan/v1/status");
        mockIResourceStore_->registerFakeResource<StatusModel>(scanStatus_);

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

        MockApplicationItem*            mockHomeScreen_ = nullptr;
        std::shared_ptr<ShortcutsModel> shortcutListing_;
        ShortcutModel*                  shortcutItem_;

        std::shared_ptr<ShortcutsModel> shortcutListingCustom_;

        /// cdm/shortcut/v1/shortcuts?type=singleJob&source=scan&destination=print

        // CDM mocking
        shortcutListingCustom_ = mockIResourceStore_->registerFakeResource<ShortcutsModel>(
            new ShortcutsModel("/cdm/shortcut/v1/shortcuts?type=singleJob&source=scan&destination=print"));

        QObjectListModel* shortcutListCustom = shortcutListingCustom_->getShortcuts();
        ShortcutModel*    shortcutListElementCustomModel_1 = new ShortcutModel();
        shortcutListElementCustomModel_1->setId(QString::fromStdString("cedab422-33b3-4638-b6a1-604e54525415"));
        shortcutListElementCustomModel_1->setTitle(QString::fromStdString("QuickSetCopyCustom"));
        shortcutListElementCustomModel_1->setPermissionId(
            QString::fromStdString("cedab422-33b3-4638-b6a1-604e54525415"));

        shortcutListElementCustomModel_1->setType(dune::spice::shortcut_1::Type::Type::singleJob);
        shortcutListElementCustomModel_1->setSource(dune::spice::shortcut_1::Source::Source::scan);
        shortcutListElementCustomModel_1->getDestinations()->append(QVariant((int)Destination::Destination::print));
        shortcutListElementCustomModel_1->setAction(dune::spice::shortcut_1::Action::Action::open);
        shortcutListElementCustomModel_1->setCopyAllowed(FeatureEnabled::true_);

        dune::spice::glossary_1::links::ItemModel* linkShortcutCustom = new dune::spice::glossary_1::links::ItemModel();
        linkShortcutCustom->setRel(QStringLiteral("shortcut"));
        linkShortcutCustom->setHref(
            QStringLiteral("/cdm/application/v1/applications/113e4567-e89b-12d3-a456-42661417700"));
        shortcutListElementCustomModel_1->getLinks()->append(linkShortcutCustom);

        shortcutListCustom->append(shortcutListElementCustomModel_1);

        // CDM mocking
        shortcutListing_ =
            mockIResourceStore_->registerFakeResource<ShortcutsModel>(new ShortcutsModel("/cdm/shortcut/v1/shortcuts"));

        QObjectListModel* shortcutList = shortcutListing_->getShortcuts();
        ShortcutModel*    shortcutListElementPrivateModel_1 = new ShortcutModel();

        shortcutListElementPrivateModel_1->setId(QString::fromStdString("cedab422-33b3-4638-b6a1-604e54525215"));
        shortcutListElementPrivateModel_1->setTitle(QString::fromStdString("QuickSetCopy1"));
        // shortcutListElementPrivateModel_1->setTitleId(QString::fromStdString("StringIds.cQuickSetButton"));
        shortcutListElementPrivateModel_1->setPermissionId(
            QString::fromStdString("cedab422-33b3-4638-b6a1-604e54525215"));

        shortcutListElementPrivateModel_1->setType(dune::spice::shortcut_1::Type::Type::singleJob);
        shortcutListElementPrivateModel_1->setSource(dune::spice::shortcut_1::Source::Source::scan);
        shortcutListElementPrivateModel_1->getDestinations()->append(QVariant((int)Destination::Destination::print));
        shortcutListElementPrivateModel_1->setAction(dune::spice::shortcut_1::Action::Action::open);
        shortcutListElementPrivateModel_1->setCopyAllowed(FeatureEnabled::true_);

        dune::spice::glossary_1::links::ItemModel* linkShortcut1 = new dune::spice::glossary_1::links::ItemModel();
        linkShortcut1->setRel(QStringLiteral("shortcut"));
        linkShortcut1->setHref(QStringLiteral("/cdm/application/v1/applications/113e4567-e89b-12d3-a456-42661417400"));
        shortcutListElementPrivateModel_1->getLinks()->append(linkShortcut1);

        shortcutList->append(shortcutListElementPrivateModel_1);

        ShortcutModel* shortcutListElementPrivateModel_2 = new ShortcutModel();
        shortcutListElementPrivateModel_2->setId(QString::fromStdString("cedab422-33b3-4638-b6a1-604e54525216"));
        // shortcutListElementPrivateModel_2->setTitleId(QString::fromStdString("StringIds.cQuickSetsAppHeading"));
        shortcutListElementPrivateModel_2->setPermissionId(
            QString::fromStdString("cedab422-33b3-4638-b6a1-604e54525215"));

        shortcutListElementPrivateModel_2->setTitle(QString::fromStdString("QuickSetCopy2"));
        shortcutListElementPrivateModel_2->setType(dune::spice::shortcut_1::Type::Type::singleJob);
        shortcutListElementPrivateModel_2->setSource(dune::spice::shortcut_1::Source::Source::scan);
        shortcutListElementPrivateModel_2->getDestinations()->append(QVariant((int)Destination::Destination::print));
        shortcutListElementPrivateModel_2->setAction(dune::spice::shortcut_1::Action::Action::open);
        shortcutListElementPrivateModel_2->setCopyAllowed(FeatureEnabled::true_);

        dune::spice::glossary_1::links::ItemModel* linkShortcut2 = new dune::spice::glossary_1::links::ItemModel();
        linkShortcut2->setRel(QStringLiteral("shortcut"));
        linkShortcut2->setHref(QStringLiteral("/cdm/application/v1/applications/113e4567-e89b-12d3-a456-42661417410"));
        shortcutListElementPrivateModel_2->getLinks()->append(linkShortcut2);

        shortcutList->append(shortcutListElementPrivateModel_2);

        shortcutItem_ = mockIResourceStore_
                            ->registerFakeResource<ShortcutModel>(
                                new ShortcutModel("/cdm/shortcut/v1/shortcuts/cedab422-33b3-4638-b6a1-604e54525215"))
                            .get();

        shortcutItem_->setId(QString::fromStdString("cedab422-33b3-4638-b6a1-604e54525215"));

        // shortcutItem_->setTitleId(QString::fromStdString("StringIds.cQuickSetsAppHeading"));
        shortcutItem_->setPermissionId(QString::fromStdString("cedab422-33b3-4638-b6a1-604e54525215"));

        shortcutItem_->setType(dune::spice::shortcut_1::Type::Type::singleJob);
        shortcutItem_->setSource(dune::spice::shortcut_1::Source::Source::scan);
        shortcutItem_->getDestinations()->append(QVariant((int)Destination::Destination::print));
        shortcutItem_->setAction(dune::spice::shortcut_1::Action::Action::open);
        shortcutItem_->setCopyAllowed(FeatureEnabled::true_);

        dune::spice::glossary_1::links::ItemModel* linkShortcut3 = new dune::spice::glossary_1::links::ItemModel();
        linkShortcut3->setRel(QStringLiteral("shortcut"));
        linkShortcut3->setHref(QStringLiteral("/cdm/application/v1/applications/113e4567-e89b-12d3-a456-42661417410"));
        shortcutItem_->getLinks()->append(linkShortcut3);

        mockHomeScreen_ = new MockApplicationItem();
        mockHomeScreen_->setApplicationName("CopyApp");

        // creating aut
        aut_ = std::make_shared<CopyAppProSelect>("CopyApp");
        aut_->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));
        ASSERT_NE(aut_, nullptr);
        aut_->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices *>(systemServices_));

        // IComponent initialization
        aut_->setInterface(GET_INTERFACE_UID(dune::spice::guiCore::IGuiApplicationEngine), "",
                           static_cast<void*>(mockIGuiApplicationEngine));
    }

    void startApplication()
    {
        std::future<void>     completionFuture;
        std::function<void()> f = [&]() { aut_->connected(nullptr, completionFuture); };
        SpiceGuiFixture::executeTask<decltype(f)>(f);

        GTestSignalSpy spy(aut_->getSpiceQmlIncubator(), SIGNAL(incubationFinished(bool)));

        aut_->start();

        ASSERT_TRUE(spy.waitForSignal(30000));

        application_ = aut_->getSpiceApplication();
        ASSERT_NE(application_, nullptr);
        application_->setProperty("appId", "cedab422-33b3-4638-b6a1-604e54525215");
        stateMachine_ = qvariant_cast<QQuickItem*>(application_->property("_stateMachine"));
        ASSERT_NE(stateMachine_, nullptr);
        EXPECT_EQ(application_->property("appId").toString(), "cedab422-33b3-4638-b6a1-604e54525215");
    }

    void startApplicationFromQuickset()
    {
        std::future<void>     completionFuture;
        std::function<void()> f = [&]() { aut_->connected(nullptr, completionFuture); };
        SpiceGuiFixture::executeTask<decltype(f)>(f);

        GTestSignalSpy spy(aut_->getSpiceQmlIncubator(), SIGNAL(incubationFinished(bool)));

        aut_->start();

        ASSERT_TRUE(spy.waitForSignal(30000));

        application_ = aut_->getSpiceApplication();
        application_->setProperty("launchFrom", 1);
        ASSERT_NE(application_, nullptr);
        application_->setProperty("appId", "cedab422-33b3-4638-b6a1-604e54525215");

        ShortcutModel* shortcutListElementPrivateModel_1 = new ShortcutModel();

        shortcutListElementPrivateModel_1->setId(QString::fromStdString("cedab422-33b3-4638-b6a1-604e54525215"));
        shortcutListElementPrivateModel_1->setTitle(QString::fromStdString("QuickSetCopy1"));
        // shortcutListElementPrivateModel_1->setTitleId(QString::fromStdString("StringIds.cQuickSetButton"));
        shortcutListElementPrivateModel_1->setPermissionId(
            QString::fromStdString("cedab422-33b3-4638-b6a1-604e54525215"));

        shortcutListElementPrivateModel_1->setType(dune::spice::shortcut_1::Type::Type::singleJob);
        shortcutListElementPrivateModel_1->setSource(dune::spice::shortcut_1::Source::Source::scan);
        shortcutListElementPrivateModel_1->getDestinations()->append(QVariant((int)Destination::Destination::print));
        shortcutListElementPrivateModel_1->setAction(dune::spice::shortcut_1::Action::Action::execute);
        shortcutListElementPrivateModel_1->setCopyAllowed(FeatureEnabled::true_);

        dune::spice::glossary_1::links::ItemModel* linkShortcut1 = new dune::spice::glossary_1::links::ItemModel();
        linkShortcut1->setRel(QStringLiteral("shortcut"));
        linkShortcut1->setHref(QStringLiteral("/cdm/jobTicket/v1/tickets/113e4567-e89b-12d3-a456-42661417400"));
        shortcutListElementPrivateModel_1->getLinks()->append(linkShortcut1);

        application_->setProperty("selectedShortcutModel", QVariant::fromValue(shortcutListElementPrivateModel_1));

        stateMachine_ = qvariant_cast<QQuickItem*>(application_->property("_stateMachine"));
        stateMachine_->setProperty("isOneTouchQuickSet", true);
        ASSERT_NE(stateMachine_, nullptr);
        EXPECT_EQ(application_->property("appId").toString(), "cedab422-33b3-4638-b6a1-604e54525215");
    }

    /**
     * @brief fillJobTicketModel fills jobTicketModel received with all valid and needed info
     *  for jobTicketModel used on copy app
     * @param jobTicketModel ticket model to be fille with valid data
     */
    void fillJobTicketModel(std::shared_ptr<JobTicketModel> jobTicketModel, QString rel)
    {
        jobTicketModel->setTicketId(rel);

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
        link->setHref(QStringLiteral("/cdm/jobTicket/v1/tickets/%1/constraints").arg(rel));
        links->append(link);

        constraintsModel_ = mockIResourceStore_->registerFakeResource<ConstraintsModel>(
            new ConstraintsModel(QStringLiteral("/cdm/jobTicket/v1/tickets/%1/constraints").arg(rel)));
    }

    void fillJobInfoModel(std::shared_ptr<JobModel> jobInfoModel, QString rel) 
    { 
        jobInfoModel->setJobId(rel); 
        jobInfoModel->setState(dune::spice::jobManagement_1::State::State::ready);
    }

    /**
     *
     */
    void fillScanStatusModel(StatusModel* scanStatusModel)
    {
        FlatbedModel* flatbedModel = new FlatbedModel();
        AdfModel*     adfModel = new AdfModel();
        adfModel->setState(dune::spice::scan_1::ScanAdfStateType::ScanAdfStateType::ScannerAdfLoaded);
        scanStatusModel->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Idle);
        scanStatusModel->setAdf(adfModel);
        scanStatusModel->setFlatbed(flatbedModel);
    }

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
    QObject*                          application_ = nullptr;
    QObject*                          stateMachine_ = nullptr;
    std::shared_ptr<CopyAppProSelect> aut_;

    std::shared_ptr<JobTicketModel> jobTicketModel_;
    std::shared_ptr<JobTicketModel> jobTicketModel2_;
    std::shared_ptr<JobModel>       jobInfoModel_;
    std::shared_ptr<JobModel>       jobInfoModel2_;
    std::shared_ptr<JobTicketModel> jobTicketModel3_;
    std::shared_ptr<JobTicketModel> jobTicketModel4_;
    std::shared_ptr<ConstraintsModel> constraintsModel_;

    JobModel*  jobInfo_ = nullptr;
    StatusModel*   scanStatus_ = nullptr;
    IMenuResource* menuResource_ = nullptr;
    SpiceDataMap*  propertyMap_ = nullptr;
    TestSystemServices* systemServices_ = nullptr;
};

class GivenCopyAppProSelectIsStarted : public GivenTestingCopyAppProSelect
{
  public:
    GivenCopyAppProSelectIsStarted() = default;

    void SetUp() override
    {
        GivenTestingCopyAppProSelect::SetUp();
        startApplication();

        fillJobTicketModel(jobTicketModel_, QStringLiteral("fake-9999-0000-id"));
        fillJobTicketModel(jobTicketModel2_, QStringLiteral("fake-9999-0001-id"));
        jobInfoModel_->setJobId(QStringLiteral("fake-job0-0000-id")); 
        //fillJobInfoModel(jobInfoModel_, "fake-job0-0000-id");
        jobInfoModel_->setState(dune::spice::jobManagement_1::State::State::created);
        fillJobInfoModel(jobInfoModel2_, "fake-job0-0000-id");
        

        jobInfo_ = new JobModel("/cdm/jobManagement/v1/jobs/fake-job0-0000-id");
        mockIResourceStore_->registerFakeResource<JobModel>(jobInfo_);

        fillScanStatusModel(scanStatus_);

        WAIT_COMPARE(stateMachine_->property("activeState"), "COPY_LANDING")
        QQuickItem* view = querySelector(contentItem_, "#copyLandingView");
        ASSERT_TRUE(view);
    }
};

TEST_F(GivenCopyAppProSelectIsStarted, WhenClicked_HandleQuickSetListSelectButton)
{
    QQuickItem* QuickSetoption = querySelector(contentItem_, "#CopyQuickSetSelected");
    if (QuickSetoption != nullptr)
    {
        if (QuickSetoption->property("visible").toBool())
        {
            QQuickItem* saveOption = querySelector(contentItem_, "#DefaultSaveButton");
            if (saveOption != nullptr)
            {
                ASSERT_EQ(saveOption->property("visible").toBool(), false);
            }
            WAIT_FOR_ITEM(contentItem_, "SpiceButton[objectName=QuickSetSelectedButton]");
            ASSERT_TRUE(item);
            mouseClick(item, Qt::LeftButton);

            WAIT_UNTIL(qmltest::querySelector(contentItem_, "#QuickSetListView") != nullptr);

            SpiceLoc* loc = new SpiceLoc();
            loc->setText("cDefault");
            auto* button = qmltest::querySelector(contentItem_, "#QuickSetListView SpiceRadioButton", 0);
            ASSERT_NE(button, nullptr);
            auto textObjectVariant = button->property("textObject");
            auto textObject = qvariant_cast<SpiceLoc*>(textObjectVariant);
            ASSERT_NE(textObject, nullptr);
            EXPECT_EQ(textObject->getText(), loc->getText());
            EXPECT_EQ(button->property("checked").toBool(), true);
        }
    }
}

TEST_F(GivenCopyAppProSelectIsStarted, WhenTicketModelDefined_ThenLandingScreenShowsCorrectly)
{
    {
        WAIT_FOR_ITEM(contentItem_, "SpiceText[text=cCopyAppHeading]");
        ASSERT_TRUE(item);
    }
}

TEST_F(GivenCopyAppProSelectIsStarted, WhenTicketModelDefined_ThenLandingScreenShowsNocCorrectly)
{
    {
        WAIT_FOR_ITEM(contentItem_, "SpiceTumbler[value=6]");
        ASSERT_TRUE(item);
    }
}

TEST_F(GivenCopyAppProSelectIsStarted, WhenLandingState_ThenSelectCopyStateIsReachedAndScanSourceIsSelected)
{
    printPropertyList();
    {
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
        ASSERT_TRUE(scanModel->getMediaSource() == dune::spice::glossary_1::ScanMediaSourceId::ScanMediaSourceId::adf);

    }
    // evaluate business logic: adf is set as the media source due to the ADF being loaded
    
    {
        WAIT_COMPARE(stateMachine_->property("jobState"), "initializeProcessing")
        stateMachine_->setProperty("jobState", QStringLiteral("ready"));
        WAIT_FOR_ITEM(contentItem_, "#CopyButton");
        ASSERT_TRUE(item);
        mouseClick(item, Qt::LeftButton);
        QVariant                        var = stateMachine_->property("ticketModel");
        dune::spice::core::ISpiceModel* ticketSpiceModel = var.value<dune::spice::core::ISpiceModel*>();
        JobTicketModel*                 jobTicketModel = static_cast<JobTicketModel*>(ticketSpiceModel->getData());
        SrcModel*                       srcModel = static_cast<SrcModel*>(jobTicketModel->getSrc()->getData());
        ScanModel*                      scanModel = static_cast<ScanModel*>(srcModel->getScan()->getData());
        DestModel*                      destModel = static_cast<DestModel*>(jobTicketModel->getDest()->getData());
        PrintModel*                     printModel = static_cast<PrintModel*>(destModel->getPrint()->getData());

        WAIT_UNTIL(stateMachine_->property("jobInProgress").toBool() == true);
        GTEST_CHECKPOINTA("JOB RUNNING!\n");

        GTEST_CHECKPOINTA("ticketId %s\n", jobTicketModel->getTicketId().toStdString().c_str());
        GTEST_CHECKPOINTA("copies %d\n", (int)printModel->getCopies());
        GTEST_CHECKPOINTA("media source %d\n", (int)scanModel->getMediaSource());
        GTEST_CHECKPOINTA("media color %d\n", (int)scanModel->getColorMode());


        jobInfoModel_->setState(dune::spice::jobManagement_1::State::State::completed);
    }
}

/*
============================================================================================
    Layout test
    Any behavior tests are not allowed here.
============================================================================================
*/

SETUP_LAYOUT_TEST(GivenCopyAppProSelectIsStarted)

TEST_P(GivenCopyAppProSelectIsStarted_P, DISABLED_WhenTicketModelDefined_ThenLandingScreenShowsCorrectlyScreenCapture)
{
    // Disabled as this test is failing because of minor view changes intermittantly.
    WAIT_FOR_ITEM(contentItem_, "SpiceText[text=cCopyAppHeading]");
    EXPECT_TRUE(qmltest::validateScreenCapture());
}

/*
============================================================================================
    End of layout test
============================================================================================
*/



class GivenCopyAppProSelectIsStartedFromQuickset : public GivenTestingCopyAppProSelect
{
  public:
    GivenCopyAppProSelectIsStartedFromQuickset() = default;

    void SetUp() override
    {
        GivenTestingCopyAppProSelect::SetUp();
        startApplicationFromQuickset();
        
        fillJobTicketModel(jobTicketModel_, QStringLiteral("fake-9999-0000-id"));
        fillJobTicketModel(jobTicketModel2_, QStringLiteral("fake-9999-0001-id"));
        fillJobInfoModel(jobInfoModel_, "fake-job0-0000-id");

        jobInfo_ = new JobModel("/cdm/jobManagement/v1/jobs/fake-job0-0000-id");
        mockIResourceStore_->registerFakeResource<JobModel>(jobInfo_);

        fillScanStatusModel(scanStatus_);
    }
};

TEST_F(GivenCopyAppProSelectIsStartedFromQuickset, WhenJobStarted_FromQuickset)
{
    // Wait till job starts and toast show
    WAIT_UNTIL(stateMachine_->property("jobInProgress").toBool() == true);
    QQuickItem* view = querySelector(contentItem_, "#SpiceToast");
    ASSERT_TRUE(view);
}

// TODO: Make tuple that will open and check all settings values and screens.
// Make it when app were more stable and settings defined.
// Define a tuple testing with list of [objectName of button, stateMachine state]
