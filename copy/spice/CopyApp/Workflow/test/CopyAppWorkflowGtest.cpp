////////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAppWorkflowGTest.cpp
 * @brief  GTest for CopyApp
 * @date   18th Feb, 2020
 * @author Hectorn Sanchez Gonzalez (hector.sanchez-gonzalez@hp.com)
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

#include "common_debug.h"
#include "CopyAppWorkflowGtest_TraceAutogen.h"
#include "SpiceLoc.h"
#include <vector>
#include <QQmlContext>
#include "CopyAppWorkflow.h"
#include "GTestConfigHelper.h"
#include "SpiceWorkflowFixture.h"
#include "SimplePathDirMock.h"
#include "TestSystemServices.h"
#include "IMenuResource.h"
#include "MockHomeScreen.h"
#include "SpiceDataMap.h"
#include "PreviewStandard.h"
#include "CopyAppWorkflowConstants.h"
#include "com_hp_cdm_service_jobManagement_version_1_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_qmlRegistration_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_sharedTypes_jobTicket_models_generated.h"
#include "com_hp_cdm_service_jobTicket_version_1_sharedTypes_jobTicket_qmlRegistration_generated.h"
#include "com_hp_cdm_service_overlay_version_1_sharedTypes_overlay_models_generated.h"
#include "com_hp_cdm_service_overlay_version_1_sharedTypes_overlay_qmlRegistration_generated.h"
#include "com_hp_cdm_service_scan_version_1_models_generated.h"
#include "com_hp_cdm_service_validator_version_1_models_generated.h"
#include "com_hp_cdm_service_validator_version_1_qmlRegistration_generated.h"
#include "com_hp_cdm_service_print_version_2_qmlRegistration_generated.h"
#include "com_hp_cdm_service_print_version_2_models_generated.h"
#include "com_hp_cdm_service_shortcut_version_1_models_generated.h"
#include "com_hp_cdm_service_shortcut_version_1_qmlRegistration_generated.h"
#include "com_hp_cdm_service_shortcut_version_1_sharedTypes_shortcut_models_generated.h"
#include "com_hp_cdm_service_shortcut_version_1_sharedTypes_shortcut_qmlRegistration_generated.h"
#include "com_hp_cdm_domain_glossary_version_1_models_generated.h"

using namespace dune::spice::testing;
using namespace dune::spice::testing::qmltest;
using namespace dune::spice::testing::environment;
using namespace dune::spice::guiCore;
using namespace dune::spice::jobManagement_1;
using namespace dune::spice::jobTicket_1;
using namespace dune::spice::jobTicket_1::jobTicket;
using namespace dune::spice::overlay_1;
using dune::spice::jobManagement_1::JobModel;
using dune::spice::jobManagement_1::JobsModel;
using namespace dune::spice::scan_1;
using namespace dune::spice::validator_1;
using dune::print::spice::PreviewStandard;

using dune::copy::spice::CopyAppWorkflow;
using FeatureEnabled = dune::spice::glossary_1::FeatureEnabled::FeatureEnabled;
using TestSystemServices = dune::framework::component::TestingUtil::TestSystemServices;
using SystemServices = dune::framework::component::SystemServices;
using dune::framework::storage::path::Paths;

using namespace dune::spice::shortcut_1;
using namespace dune::spice::shortcutSharedTypesShortcut_1;
using dune::spice::shortcut_1::ShortcutModel;
using dune::spice::shortcut_1::ShortcutsModel;
using PrintStatusModel =  dune::spice::print_2::StatusModel;


class GivenTestingCopyAppWorkflow : public SpiceWorkflowFixture
{
  public:
    using StatusModel = dune::spice::scan_1::StatusModel;
    GivenTestingCopyAppWorkflow() = default;

    virtual void SetUp()
    {
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

        // CDM mocking
        jobsListing_ =
            mockIResourceStore_->registerFakeResource<JobsModel>(new JobsModel("/cdm/jobManagement/v1/queue"));
        defaultTicket_ = mockIResourceStore_->registerFakeResource<JobTicketModel>(
            new JobTicketModel("/cdm/jobTicket/v1/configuration/defaults/copy"));
        fillJobTicketModel(defaultTicket_, "fake-default-id");
        // register and create jobTicket resources
        createInstanceOfJobTicket(QStringLiteral("fake-9999-0001-id"));
        createInstanceOfJobTicket(QStringLiteral("fake-9999-0001-id"));
        registerJobTicket(QStringLiteral("fake-9999-0000-id"));
        registerJobTicket(QStringLiteral("fake-9999-0001-id"));

        //Create preview component to register preview module into QML
        preview_ = std::make_shared<PreviewStandard>("PreviewStandard");
        preview_->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices *>(systemServices_));
        preview_->setInterface(GET_INTERFACE_UID(dune::spice::guiCore::IGuiApplicationEngine), "", static_cast<void*>(mockIGuiApplicationEngine));
        std::future<void> previewUnusedFuture;
        
        std::function<void()> f = [&]() { preview_->connected(nullptr, previewUnusedFuture); };
        SpiceGuiFixture::executeTask<decltype(f)>(f);

        constraintsModel1_ = mockIResourceStore_->registerFakeResource<ConstraintsModel>(
            new ConstraintsModel(QStringLiteral("/cdm/jobTicket/v1/tickets/%1/constraints").arg("fake-9999-0000-id")));
        constraintsModel2_ = mockIResourceStore_->registerFakeResource<ConstraintsModel>(
            new ConstraintsModel(QStringLiteral("/cdm/jobTicket/v1/tickets/%1/constraints").arg("fake-9999-0001-id")));

        scanStatusModel_ = mockIResourceStore_->registerFakeResource<StatusModel>( 
            new StatusModel( "/cdm/scan/v1/status" ) );
        
        printStatusModel_ = mockIResourceStore_->registerFakeResource<PrintStatusModel>(
            new PrintStatusModel("/cdm/print/v2/status"));
        
        printStatusModel_->setPrinterState(dune::spice::print_2::status::PrinterState::PrinterState::idle);
        mockIGuiApplicationEngine->getQQmlEngine()->addImportPath("qrc:/Walkup/imports");
        propertyMap_ = new SpiceDataMap(QString("./testResources/generated/TestSpiceDataMap.bin"));
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty("_propertyMap", propertyMap_);

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
        // creating aut
        aut_ = std::make_shared<CopyAppWorkflow>("CopyApp");
        aut_->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices *>(systemServices_));

        // IComponent initialization
        aut_->setInterface(GET_INTERFACE_UID(dune::spice::guiCore::IGuiApplicationEngine), "",
                           static_cast<void*>(mockIGuiApplicationEngine));

        priorityModeSessionModel_ = mockIResourceStore_->registerFakeResource<PriorityModeSessionModel>(
            new PriorityModeSessionModel("/cdm/jobManagement/v1/priorityModeSessions"));
        
    }

    void startApplication(){
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
        copyAppStack_ = qvariant_cast<QQuickItem*>(stack);
        stateMachine_ = qvariant_cast<QQuickItem*>(application_->property("_stateMachine"));
        stateMachine_->setProperty("toastTimeout", 100);
    }

    void mockShortcuts(){

       
        std::shared_ptr<ShortcutsModel> shortcutListing_;
        ShortcutModel*                  shortcutItem_;


        // cdm/shortcut/v1/shortcuts?type=singleJob&source=scan&destination=print
        // CDM mocking

        auto shortcutListingCustom_ = mockIResourceStore_->registerFakeResource<ShortcutsModel>(
            new ShortcutsModel("/cdm/shortcut/v1/shortcuts?type=singleJob&source=scan&destination=print"));
        
        QObjectListModel* shortcutListCustom = shortcutListingCustom_->getShortcuts();
        shortcutListElementCustomModel_1 = new ShortcutModel();
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
        linkShortcutCustom->setParent(shortcutListElementCustomModel_1->getLinks());

        shortcutListCustom->append(shortcutListElementCustomModel_1);

        // CDM mocking
        shortcutListing_ =
            mockIResourceStore_->registerFakeResource<ShortcutsModel>(new ShortcutsModel("/cdm/shortcut/v1/shortcuts"));

        QObjectListModel* shortcutList = shortcutListing_->getShortcuts();
        shortcutListElementPrivateModel_1 = new ShortcutModel();

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
        linkShortcut1->setParent(shortcutListElementPrivateModel_1->getLinks());
        shortcutList->append(shortcutListElementPrivateModel_1);
        

        shortcutListElementPrivateModel_2 = new ShortcutModel();
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
        linkShortcut2->setParent(shortcutListElementPrivateModel_2->getLinks());
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
        linkShortcut3->setParent(shortcutItem_->getLinks());
        mockHomeScreen_ = new MockApplicationItem();
        mockHomeScreen_->setApplicationName("CopyApp");

}

    void startApplicationFromQuickset()
    {

        shortcutListElementPrivateModel_ = new ShortcutModel();

        shortcutListElementPrivateModel_->setId(QString::fromStdString("cedab422-33b3-4638-b6a1-604e54525215"));
        shortcutListElementPrivateModel_->setTitle(QString::fromStdString("QuickSetCopy1"));
        // shortcutListElementPrivateModel_->setTitleId(QString::fromStdString("StringIds.cQuickSetButton"));
        shortcutListElementPrivateModel_->setPermissionId(
            QString::fromStdString("cedab422-33b3-4638-b6a1-604e54525215"));

        shortcutListElementPrivateModel_->setType(dune::spice::shortcut_1::Type::Type::singleJob);
        shortcutListElementPrivateModel_->setSource(dune::spice::shortcut_1::Source::Source::scan);
        shortcutListElementPrivateModel_->getDestinations()->append(QVariant((int)Destination::Destination::print));
        shortcutListElementPrivateModel_->setAction(dune::spice::shortcut_1::Action::Action::execute);
        shortcutListElementPrivateModel_->setCopyAllowed(FeatureEnabled::true_);

        dune::spice::glossary_1::links::ItemModel* linkShortcut1 = new dune::spice::glossary_1::links::ItemModel();
        linkShortcut1->setRel(QStringLiteral("shortcut"));
        linkShortcut1->setHref(QStringLiteral("/cdm/jobTicket/v1/tickets/113e4567-e89b-12d3-a456-42661417400"));
        shortcutListElementPrivateModel_->getLinks()->append(linkShortcut1);
        linkShortcut1->setParent(shortcutListElementPrivateModel_->getLinks());

        QVariantMap initialValues;
        initialValues.insert("launchFrom", 1);
        initialValues.insert("href", "b8460c9e-43c8-4290-a0f8-8ce450867f09");
        initialValues.insert("selectedShortcutModel", QVariant::fromValue(shortcutListElementPrivateModel_));
        initialValues.insert("appId", "cedab422-33b3-4638-b6a1-604e54525215");


        std::future<void>     completionFuture;
        std::function<void()> f = [&]() { aut_->connected(nullptr, completionFuture); };
        SpiceGuiFixture::executeTask<decltype(f)>(f);

        GTestSignalSpy spy(aut_->getSpiceQmlIncubator(), SIGNAL(incubationFinished(bool)));

        aut_->start(initialValues);

        ASSERT_TRUE(spy.waitForSignal(30000));

        application_ = aut_->getSpiceApplication();
        
        ASSERT_NE(application_, nullptr);
       
       // application_->setProperty("selectedShortcutModel", QVariant::fromValue(shortcutListElementPrivateModel_1));
        stateMachine_ = qvariant_cast<QQuickItem*>(application_->property("_stateMachine"));
        ASSERT_NE(stateMachine_, nullptr);
        stateMachine_->setProperty("isOneTouchQuickSet", true);
        stateMachine_->setProperty("toastTimeout", 100);
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
        jobTicketModels_.push_back(jobTicketModel);
    }

    /**
     * @brief fillJobTicketModel fills jobTicketModel received with all valid and needed info
     *  for jobTicketModel used on copy app
     * @param jobTicketModel ticket model to be fille with valid data and ticketId of JobTicket
     * @param ticketId of JobTicket
     */
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

        WatermarkDetailsModel* watermarkDetailsModel = new WatermarkDetailsModel();
        watermarkDetailsModel->setWatermarkType(dune::spice::overlay_1::watermarkDetails::WatermarkType::WatermarkType::none);
        
        ScanStampLocationModel* scanStampTopLeftModel = new ScanStampLocationModel();
        scanStampTopLeftModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::topLeft);
        ScanStampLocationModel* scanStampTopCenterModel = new ScanStampLocationModel();
        scanStampTopCenterModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::topCenter);
        ScanStampLocationModel* scanStampTopRightModel = new ScanStampLocationModel();
        scanStampTopRightModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::topRight);
        ScanStampLocationModel* scanStampBottomLeftModel = new ScanStampLocationModel();
        scanStampBottomLeftModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::bottomLeft);
        ScanStampLocationModel* scanStampBottomCenterModel = new ScanStampLocationModel();
        scanStampBottomCenterModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::bottomCenter);
        ScanStampLocationModel* scanStampBottomRightModel = new ScanStampLocationModel();
        scanStampBottomRightModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::bottomRight);

        ScalingModel* scalingModel = new ScalingModel();
        scalingModel->setYScalePercent(100);
        scalingModel->setXScalePercent(100);
        scalingModel->setScaleToFitEnabled(FeatureEnabled::true_);
        pipelineOptionsModel->setScaling(scalingModel);
        pipelineOptionsModel->setWatermark(watermarkDetailsModel);
        pipelineOptionsModel->setImageModifications(imageModificationsModel);
        ManualUserOperationsModel* manualUserOperations = new ManualUserOperationsModel();
        manualUserOperations->setImagePreviewConfiguration(manualUserOperations::ImagePreviewConfiguration::ImagePreviewConfiguration::optional);
        pipelineOptionsModel->setManualUserOperations(manualUserOperations);
        pipelineOptionsModel->setStampTopLeft(scanStampTopLeftModel);
        pipelineOptionsModel->setStampTopCenter(scanStampTopCenterModel);
        pipelineOptionsModel->setStampTopRight(scanStampTopRightModel);
        pipelineOptionsModel->setStampBottomLeft(scanStampBottomLeftModel);
        pipelineOptionsModel->setStampBottomCenter(scanStampBottomCenterModel);
        pipelineOptionsModel->setStampBottomRight(scanStampBottomRightModel);
        jobTicketModel->setPipelineOptions(pipelineOptionsModel);

        srcModel->setScan(scanModel);
        dstModel->setPrint(printModel);
        jobTicketModel->setDest(dstModel);
        jobTicketModel->setSrc(srcModel);

    }

    /**
     * @brief fill job info model data
     * 
     * @param jobInfoModel object of jobInfo
     * @param jobId 
     */
    void fillJobInfoModel(std::shared_ptr<JobModel> &jobInfoModel, QString jobId) 
    { 
        jobInfoModel->setJobId(jobId); 
        jobInfoModel->setState(dune::spice::jobManagement_1::State::State::ready);
    }

    /**
     * @brief fill the scan status model for the ADf, GLASS
     * 
     * @param scanStatusModel object scanner status
     */
    void fillAdfFlatbedScanStatusModel(std::shared_ptr<StatusModel>  &scanStatusModel)
    {
        FlatbedModel* flatbedModel = new FlatbedModel();
        AdfModel*     adfModel = new AdfModel();
        adfModel->setState(dune::spice::scan_1::ScanAdfStateType::ScanAdfStateType::ScannerAdfLoaded);
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
        delete propertyMap_;
        delete systemServices_;
        if(application_){
            application_->deleteLater();
        }
        if(stateMachine_){
            stateMachine_->deleteLater();
        }
        if(copyAppStack_){
            copyAppStack_->deleteLater();
        }  
        if(shortcutListElementPrivateModel_) delete shortcutListElementPrivateModel_;
        if(shortcutListElementPrivateModel_1) delete shortcutListElementPrivateModel_1;
        if(shortcutListElementPrivateModel_2) delete shortcutListElementPrivateModel_2;
        if(shortcutListElementCustomModel_1) delete shortcutListElementCustomModel_1;
        if(mockHomeScreen_) mockHomeScreen_->deleteLater();
        devicesupportedShortcutTypes->deleteLater();      
        SpiceWorkflowFixture::TearDown();
        
    }

    std::shared_ptr<StatusModel>                    scanStatusModel_;

  protected:
    QObject*                                        application_ = nullptr;
    QObject*                                        stateMachine_ = nullptr;
    QQuickItem*                                     copyAppStack_ = nullptr;
    SpiceDataMap*                                   propertyMap_ = nullptr;
    TestSystemServices*                             systemServices_ = nullptr;
    std::shared_ptr<CopyAppWorkflow>                aut_;
    std::shared_ptr<PreviewStandard>               preview_;

    std::vector<std::shared_ptr<JobTicketModel>>    jobTicketModels_;
    std::vector<std::shared_ptr<JobModel>>          jobInfoModels_;
    std::shared_ptr<JobModel>                       jobInfoModel1_;
    std::shared_ptr<JobModel>                       jobInfoModel2_;
    std::shared_ptr<JobModel>                       jobInfoModel3_;
    std::shared_ptr<JobModel>                       jobInfoModel4_;

    std::shared_ptr<JobsModel>                      jobsListing_;
    std::shared_ptr<PagesModel>                     pagesModel_;
    std::shared_ptr<JobTicketModel>                 defaultTicket_;   
    std::shared_ptr<ConstraintsModel>               constraintsModel1_;
    std::shared_ptr<ConstraintsModel>               constraintsModel2_;

    std::shared_ptr<PrintStatusModel>               printStatusModel_;


    MockApplicationItem*            mockHomeScreen_ = nullptr;
    ShortcutModel* shortcutListElementPrivateModel_2 = nullptr;
    ShortcutModel* shortcutListElementPrivateModel_1 = nullptr;
    ShortcutModel* shortcutListElementPrivateModel_ = nullptr;
    ShortcutModel* shortcutListElementCustomModel_1 = nullptr;
    bool                                                    scanPreviewSupported{true};
    bool                                                    jobConcurrency{true};
    bool                                                    multiPagePreviewSupported{false};
    QVariantListModel*                              devicesupportedShortcutTypes;
    std::shared_ptr<PriorityModeSessionModel>               priorityModeSessionModel_{nullptr};
};

class GivenCopyAppWorkflowIsStartedWithADF : public GivenTestingCopyAppWorkflow
{
  public:
    GivenCopyAppWorkflowIsStartedWithADF() = default;

    void SetUp() override
    {
        GivenTestingCopyAppWorkflow::SetUp();
        fillAdfFlatbedScanStatusModel(scanStatusModel_);
        startApplication();
        //Register jobInfomodels seperately
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
        
    }
};

class GivenCopyAppWorkflowIsStartedWithADFScannerProcessing : public GivenTestingCopyAppWorkflow
{
  public:
    GivenCopyAppWorkflowIsStartedWithADFScannerProcessing() = default;

    void SetUp() override
    {
        GivenTestingCopyAppWorkflow::SetUp();
        fillScanStatusModelProcessing(scanStatusModel_);
        startApplication();
        
        //Register jobInfomodels seperately
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

    }
};


TEST_F(GivenCopyAppWorkflowIsStartedWithADF, WhenTicketModelDefined_ThenLandingScreenShowsCorrectly)
{

    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);
    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);

    //It requiere another synch method with new substates inside LANDING
    WAIT_UNTIL(stateMachine_->property("currentJobState") == 1);
}

TEST_F(GivenCopyAppWorkflowIsStartedWithADF, WhenTicketModelCreatedState_ThenActionButtonIsDisabled)
{

    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);

    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)

    {
        WAIT_UNTIL(stateMachine_->property("isJobInReadyState").toBool() == false);
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);
        QQuickItem* actionButton = querySelector(copyAppStack_, "#mainActionButtonOfDetailPanel");
        EXPECT_EQ(actionButton->property("enabled").toBool(), false);
    }
}
    

TEST_F(GivenCopyAppWorkflowIsStartedWithADF, WhenClickOnCopyButtonInDetailPanel_JobStarted)
{

    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);

    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);


    {
        WAIT_COMPARE(stateMachine_->property("currentJobState"), 1)
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);
        mouseClick(item, Qt::LeftButton);
        scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Processing);
        WAIT_UNTIL(stateMachine_->property("isScannerIdle").toBool() == false);
        WAIT_UNTIL(stateMachine_->property("jobInProgress").toBool() == true);

        QQuickItem* actionButton = querySelector(copyAppStack_, "#mainActionButtonOfDetailPanel");
        EXPECT_EQ(actionButton->property("enabled").toBool(), false);

        {
            WAIT_FOR_ITEM(contentItem_, "#SpiceToast");
            ASSERT_TRUE(item);          
        }
        QTest::qWait(100);
    }

    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)
}

TEST_F(GivenCopyAppWorkflowIsStartedWithADFScannerProcessing, WhenScanIsInProcessingState_ActionButtonDisabled)
{

    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);

    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);
    {
        WAIT_COMPARE(stateMachine_->property("currentJobState"), 1)
        WAIT_UNTIL(stateMachine_->property("isJobInReadyState").toBool() == true);
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);
        QQuickItem* actionButton = querySelector(copyAppStack_, "#mainActionButtonOfDetailPanel");
        EXPECT_EQ(actionButton->property("enabled").toBool(), false);
    }
}


TEST_F(GivenCopyAppWorkflowIsStartedWithADFScannerProcessing, WhenScanStateChangeToIdle_ActionButtonEnabled)
{

    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);

    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);
    {
        WAIT_COMPARE(stateMachine_->property("currentJobState"), 1)
        WAIT_UNTIL(stateMachine_->property("isJobInReadyState").toBool() == true);
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);
        QQuickItem* actionButton = querySelector(copyAppStack_, "#mainActionButtonOfDetailPanel");
        EXPECT_EQ(actionButton->property("enabled").toBool(), false);
    }

    //scan status changed, Action button should be enabled now
    scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Idle);
    {
        WAIT_COMPARE(stateMachine_->property("isScannerIdle").toBool(), true)
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);
        QQuickItem* actionButton = querySelector(copyAppStack_, "#mainActionButtonOfDetailPanel");
        WAIT_COMPARE(actionButton->property("enabled").toBool(), true);
    }
}

TEST_F(GivenCopyAppWorkflowIsStartedWithADF, WhenScanStateChangeToPocessing_OptionsAreNotConstrained)
{
    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);

    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)
    
    scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Processing);   
    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);
    {
        QVariant returnedValue;
        auto controller = stateMachine_->property("controller").value<QObject*>();
        ASSERT_NE(controller, nullptr);
        auto ret = QMetaObject::invokeMethod(controller,"isSettingEnabled",
                                            Q_RETURN_ARG(QVariant, returnedValue),Q_ARG(QVariant , QVariant::fromValue(QString("src/scan/colorMode"))));
        ASSERT_EQ(ret, true);
        ASSERT_TRUE(returnedValue.toBool());
    }
}

TEST_F(GivenCopyAppWorkflowIsStartedWithADF, WhenClickOnCopyButtonInPreviewPanel_JobStarted)
{

    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);

    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);

    WAIT_FOR_ITEM(contentItem_, "#_ExpandButton");
    ASSERT_TRUE(item);
    mouseClick(item, Qt::LeftButton);

    {
        WAIT_COMPARE(stateMachine_->property("currentJobState"), "1")
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfMainPanel");
        ASSERT_TRUE(item);
        mouseClick(item, Qt::LeftButton);
        WAIT_UNTIL(stateMachine_->property("isJobInReadyState").toBool() == false);

        scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Processing);
        WAIT_UNTIL(stateMachine_->property("isScannerIdle").toBool() == false);

        {
            WAIT_FOR_ITEM(contentItem_, "#SpiceToast");
            ASSERT_TRUE(item);
            
        }
        QTest::qWait(100);
    }

    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)
}

TEST_F(GivenCopyAppWorkflowIsStartedWithADF, WhenClickOnCopyButtonInPreviewPanel_DummyPreviewComes)
{

    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);

    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);

    WAIT_FOR_ITEM(contentItem_, "#_ExpandButton");
    ASSERT_TRUE(item);
    mouseClick(item, Qt::LeftButton);

    {
        WAIT_COMPARE(stateMachine_->property("currentJobState"), 1)
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfMainPanel");
        ASSERT_TRUE(item);
        mouseClick(item, Qt::LeftButton);
        fillJobQueueModel();
        {
            WAIT_FOR_ITEM(contentItem_, "#SpiceToast");
            ASSERT_TRUE(item);
        }
        {
            // Wait for preview component to be properly set up with dummy pages
            // Check if preview component handler exists and is enabled
            QQuickItem* previewHandler = querySelector(contentItem_, "PreviewComponentHandler");
            if (previewHandler) {
                // Wait for preview component to be enabled and dummy pages to be set
                WAIT_UNTIL_TIMEOUT(previewHandler->property("setPreviewComponent").toBool() == true, 3000);
                // Additional wait to ensure dummy pages are loaded
                QTest::qWait(500);
            }

            // Wait for the state machine to reach the correct state for preview
            WAIT_UNTIL_TIMEOUT(stateMachine_->property("currentJobState").toInt() >= 1, 3000);

            WAIT_FOR_ITEM_TIMEOUT(contentItem_, "#FitPage", 10000);
            ASSERT_TRUE(item);
            
        }
    }
    QTest::qWait(100);
    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)
}

TEST_F(GivenCopyAppWorkflowIsStartedWithADF, WhenCopyButtonIsClicked_SaveButtonIsNotVisible)
{

    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);
    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)
    QQuickItem* saveButton = querySelector(copyLandingView, "#savePanelButton");
    ASSERT_TRUE(saveButton);
    ASSERT_FALSE(saveButton->isVisible());
}

TEST_F(GivenCopyAppWorkflowIsStartedWithADF, WhenClickOnCopyButtonInDetailPanel_JobStartedCancelButtonAppear)
{

    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);

    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)
    
    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);
    
    scanStatusModel_->setScannerState(dune::spice::scan_1::ScannerStatusType::ScannerStatusType::Idle);
    {
        WAIT_COMPARE(stateMachine_->property("currentJobState"), 1)
        WAIT_UNTIL(stateMachine_->property("isJobInReadyState").toBool() == true);
        WAIT_FOR_ITEM(contentItem_, "#mainActionButtonOfDetailPanel");
        ASSERT_TRUE(item);
        mouseClick(item, Qt::LeftButton);

        WAIT_UNTIL(stateMachine_->property("isJobInReadyState").toBool() == false);
        {
            WAIT_FOR_ITEM(contentItem_, "#SpiceToast");
            ASSERT_TRUE(item);
            
        }
        fillJobQueueModel();
        {
            WAIT_FOR_ITEM(contentItem_, "#cancelButton");
            ASSERT_TRUE(item);

            QQuickItem* cancelButton = querySelector(contentItem_, "#cancelButton");
            ASSERT_EQ(cancelButton->property("visible").toBool(), true);

        }
        QTest::qWait(100);
    }

    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)
}


class GivenCopyAppWorkflowIsStartedWithADFWithQuickSet : public GivenTestingCopyAppWorkflow
{
  public:
    GivenCopyAppWorkflowIsStartedWithADFWithQuickSet() = default;

    void SetUp() override
    {
        GivenTestingCopyAppWorkflow::SetUp();
        mockShortcuts();
        fillAdfFlatbedScanStatusModel(scanStatusModel_);
        startApplication();
        
        //Register jobInfomodels seperately
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

    }
};

// Disabling the gtest as it causing memory leak in jupiter
TEST_F(GivenCopyAppWorkflowIsStartedWithADFWithQuickSet, DISABLED_WhenAppEnteredQuicksetRadioButtonAreSeenOnQSPanel)
{
    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);
    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)
    QQuickItem* qsScroll = querySelector(copyAppStack_, "#qsScroll");
    ASSERT_TRUE(qsScroll);

    QQuickItem* defaultInView = querySelector(qsScroll, "#Default");
    ASSERT_TRUE(defaultInView);

    EXPECT_EQ(defaultInView->property("checked").toBool(), true);
    EXPECT_EQ(defaultInView->property("enabled").toBool(), true);
    {
        WAIT_FOR_ITEM(contentItem_, "#cedab422-33b3-4638-b6a1-604e54525415");
        ASSERT_TRUE(item);

        mouseClick(item, Qt::LeftButton);
    }

    QTest::qWait(100);
    QQuickItem* quickSetCopyCustom = querySelector(copyAppStack_, "#cedab422-33b3-4638-b6a1-604e54525415");
    ASSERT_TRUE(quickSetCopyCustom);
    EXPECT_EQ(quickSetCopyCustom->property("checked").toBool(), true);


    {
        WAIT_FOR_ITEM(contentItem_, "#ViewAll");
        ASSERT_TRUE(item);

        mouseClick(item, Qt::LeftButton);
    }

    QQuickItem* qSListofApp = querySelector(contentItem_, "#QSListofApp");
    ASSERT_TRUE(qSListofApp);

    auto image = querySelector(contentItem_, "#ContentItem SpiceImage");
    ASSERT_TRUE(image);
    mouseClick(image, Qt::LeftButton);

    {
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);
    }

}

class GivenCopyAppWorkflowIsStartedWithADFWithQuickSetXL : public GivenCopyAppWorkflowIsStartedWithADFWithQuickSet
{
  public:
    GivenCopyAppWorkflowIsStartedWithADFWithQuickSetXL() = default;

    void SetUp() override
    {
        SpiceWorkflowFixture::configureXL();
        GivenCopyAppWorkflowIsStartedWithADFWithQuickSet::SetUp();
    }
};

TEST_F(GivenCopyAppWorkflowIsStartedWithADFWithQuickSetXL, WhenAppEnteredQuicksetRadioButtonAreSeenOnQSPanelThenDefaultIconIsSet)
{
    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);
    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)

    {
        WAIT_FOR_ITEM(copyAppStack_, "#qsScroll");
        ASSERT_TRUE(item);
    }

    QQuickItem* qsScroll = querySelector(copyAppStack_, "#qsScroll");
    ASSERT_TRUE(qsScroll);

    {
        WAIT_FOR_ITEM(contentItem_, "#cedab422-33b3-4638-b6a1-604e54525415");
        ASSERT_TRUE(item);
    }

    QQuickItem* quickSetCopyCustom = querySelector(copyAppStack_, "#cedab422-33b3-4638-b6a1-604e54525415");
    ASSERT_TRUE(quickSetCopyCustom);
    EXPECT_EQ(quickSetCopyCustom->property("icon").toString(), "qrc:/images/Graphics/UserCreatedQuickset.json");
}
class GivenCopyAppWorkflowIsStartedWithADFWithQuickSetSpecificIconXL : public GivenCopyAppWorkflowIsStartedWithADFWithQuickSetXL
{
  public:
    GivenCopyAppWorkflowIsStartedWithADFWithQuickSetSpecificIconXL() = default;

    void SetUp() override
    {
        SpiceWorkflowFixture::configureXL();
        GivenCopyAppWorkflowIsStartedWithADFWithQuickSetXL::SetUp();

        QMap<QString, QVariant> mapIcon ;
        mapIcon["cedab422-33b3-4638-b6a1-604e54525415"] = QVariant("qrc:/images/Graphics/ColorModeMixedColor.json");
        QVariant mapIconVarinat (mapIcon);
        mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty("_copyQuicksetIconList", mapIconVarinat);
    }
};

TEST_F(GivenCopyAppWorkflowIsStartedWithADFWithQuickSetSpecificIconXL, WhenAppEnteredQuicksetRadioButtonAreSeenOnQSPanelThenSpecificIconIsSet)
{
    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);
    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true) // Wait for the copyApp to load completely else leads to leaks
    
    {
        WAIT_FOR_ITEM(copyAppStack_, "#qsScroll");
        ASSERT_TRUE(item);
    }

    QQuickItem* qsScroll = querySelector(copyAppStack_, "#qsScroll");
    ASSERT_TRUE(qsScroll);

    {
        WAIT_FOR_ITEM(contentItem_, "#cedab422-33b3-4638-b6a1-604e54525415");
        ASSERT_TRUE(item);
    }

    QQuickItem* quickSetCopyCustom = querySelector(copyAppStack_, "#cedab422-33b3-4638-b6a1-604e54525415");
    ASSERT_TRUE(quickSetCopyCustom);
    EXPECT_EQ(quickSetCopyCustom->property("icon").toString(), "qrc:/images/Graphics/ColorModeMixedColor.json");
}

class GivenCopyAppWorkflowIsStartedWithADFWithQuickSetOneTouch : public GivenTestingCopyAppWorkflow
{
  public:
    GivenCopyAppWorkflowIsStartedWithADFWithQuickSetOneTouch() = default;

    void SetUp() override
    {
        
        GivenTestingCopyAppWorkflow::SetUp();
        mockShortcuts();
        fillAdfFlatbedScanStatusModel(scanStatusModel_);
        startApplicationFromQuickset();
        
        //Register jobInfomodels seperately
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
        
    }
};


// Disabling the gtest as it causing memory leak in jupiter
TEST_F(GivenCopyAppWorkflowIsStartedWithADFWithQuickSetOneTouch, DISABLED_WhenJobStarted_FromQuickset)
{
    // Wait till job starts and toast show
        QTest::qWait(500);
        {
            WAIT_FOR_ITEM(contentItem_, "#SpiceToast");
            ASSERT_TRUE(item);
            QTest::qWait(100);
        }
}

class GivenCopyAppWorkflowIsStartedWithFlatbed : public GivenTestingCopyAppWorkflow
{
  public:
    GivenCopyAppWorkflowIsStartedWithFlatbed() = default;

    void fillPagesModel(){
        pageModel = new PageModel();
        pageModel->setPageId(QString("fake-page0-0000-id"));
        pageModel->setPreviewProgress(100);

        QObjectListModel*  pageList = pagesModel_->getPages();
        pageList->append(pageModel);

        pageModel_ = mockIResourceStore_->registerFakeResource<PageModel>(new PageModel("/cdm/jobManagement/v1/jobs/fake-job0-0000-id/pages/fake-page0-0000-id"));
        pageModel_->setPageId(QString("fake-page0-0000-id"));
        pageModel_->setPreviewProgress(100);
        ImageDescriptorModel*  highResImage = new ImageDescriptorModel();
        highResImage->setWidth(100);
        highResImage->setHeight(100);
        imageLink = new dune::spice::glossary_1::links::ItemModel();
        imageLink->setRel(QStringLiteral("High Res Image"));
        imageLink->setHref(QStringLiteral("./testResources/integrationTest002.jpg"));

        QObjectListModel* links = highResImage->getLinks();
        links->append(imageLink);

        pageModel_->setHighResImage(highResImage);
    }

    void SetUp() override
    {
        GivenTestingCopyAppWorkflow::SetUp();
        fillScanStatusModelFlatbedLoaded(scanStatusModel_);
        startApplication();
        
        //Register jobInfomodels seperately
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

        pagesModel_ =
            mockIResourceStore_->registerFakeResource<PagesModel>(new PagesModel("/cdm/jobManagement/v1/jobs/fake-job0-0000-id/pages"));
        fillPagesModel();
    }

    void TearDown() override
    {
        if(imageLink){
            delete imageLink;
        }
        if(pageModel){
            delete pageModel;
        }
        GivenTestingCopyAppWorkflow::TearDown();
    }
  protected:
    dune::spice::glossary_1::links::ItemModel*          imageLink{nullptr};
    PageModel*                                          pageModel{nullptr};
    std::shared_ptr<PageModel>                  pageModel_;
};

TEST_F(GivenCopyAppWorkflowIsStartedWithFlatbed, DISABLED_WhenFlatbedIsLoaded_PreviewButtonAvailableWhenClicked_RefreshButtonAvailableWithoutText)
{

    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);

    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);

    WAIT_FOR_ITEM(contentItem_, "#_ExpandButton");
    ASSERT_TRUE(item);
    mouseClick(item, Qt::LeftButton);

    {
        WAIT_COMPARE(stateMachine_->property("jobState"), "ready")
        WAIT_FOR_ITEM(contentItem_, "#previewButton");
        ASSERT_TRUE(item);
        mouseClick(item, Qt::LeftButton);
        fillJobQueueModel();
         {
            WAIT_COMPARE(stateMachine_->property("isJobInReadyState"), false)
            WAIT_FOR_ITEM(contentItem_, "#FitPage");
            ASSERT_TRUE(item);
        }
    }
    {
    WAIT_FOR_ITEM(contentItem_, "#refreshPanelButton");
    ASSERT_TRUE(item);
    auto spiceIcon = item->property("icon").toString();
    EXPECT_EQ(spiceIcon, "qrc:/images/Glyph/+lang_ar/Refresh.json");
    auto *spiceText = item->property("textObject").value<SpiceLoc *>();
    EXPECT_EQ(spiceText->getText().toStdString(), "");
    }
}

class GivenCopyAppWorkflowIsStartedWithFlatbedConfigureSizeM : public GivenCopyAppWorkflowIsStartedWithFlatbed{
    void SetUp() override
    {
        SpiceWorkflowFixture::configureM();
        GivenCopyAppWorkflowIsStartedWithFlatbed::SetUp();
    }

    void TearDown() override
    {
        GivenCopyAppWorkflowIsStartedWithFlatbed::TearDown();
    }
};

TEST_F(GivenCopyAppWorkflowIsStartedWithFlatbedConfigureSizeM, WhenFlatbedIsLoaded_PreviewButtonAvailableWhenClicked_RefreshButtonAvailableWithText)
{

    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);

    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);

    WAIT_FOR_ITEM(contentItem_, "#_ExpandButton");
    ASSERT_TRUE(item);
    mouseClick(item, Qt::LeftButton);

    {
        WAIT_COMPARE(stateMachine_->property("currentJobState"), 1)
        WAIT_FOR_ITEM(contentItem_, "#previewButton");
        ASSERT_TRUE(item);
        mouseClick(item, Qt::LeftButton);
        fillJobQueueModel();
    }
    {
    WAIT_FOR_ITEM(contentItem_, "#refreshPanelButton");
    ASSERT_TRUE(item);
    auto spiceIcon = item->property("icon").toString();
    EXPECT_EQ(spiceIcon, "qrc:/images/Glyph/+lang_ar/Refresh.json");
    auto *spiceText = item->property("textObject").value<SpiceLoc *>();
    EXPECT_EQ(spiceText->getText().toStdString(), "cRefresh");
    }
}


class GivenCopyAppWorkflowIsStartedWithFlatbedPreviewButtonNotVisible : public GivenTestingCopyAppWorkflow
{
  public:
    GivenCopyAppWorkflowIsStartedWithFlatbedPreviewButtonNotVisible() = default;

        /**
     * @brief fillJobTicketModel fills jobTicketModel received with all valid and needed info
     *  for jobTicketModel used on copy app
     * @param jobTicketModel ticket model to be fille with valid data and ticketId of JobTicket
     * @param ticketId of JobTicket
     */
    void fillJobTicketModel(std::shared_ptr<JobTicketModel> &jobTicketModel, QString ticketId) override
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
        imageModificationsModel->setPagesPerSheet(dune::spice::jobTicket_1::PagesPerSheet::PagesPerSheet::twoUp);
        PipelineOptionsModel* pipelineOptionsModel = new PipelineOptionsModel();

        WatermarkDetailsModel* watermarkDetailsModel = new WatermarkDetailsModel();
        watermarkDetailsModel->setWatermarkType(dune::spice::overlay_1::watermarkDetails::WatermarkType::WatermarkType::textWatermark);

        ScanStampLocationModel* scanStampTopLeftModel = new ScanStampLocationModel();
        scanStampTopLeftModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::topLeft);
        ScanStampLocationModel* scanStampTopCenterModel = new ScanStampLocationModel();
        scanStampTopCenterModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::topCenter);
        ScanStampLocationModel* scanStampTopRightModel = new ScanStampLocationModel();
        scanStampTopRightModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::topRight);
        ScanStampLocationModel* scanStampBottomLeftModel = new ScanStampLocationModel();
        scanStampBottomLeftModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::bottomLeft);
        ScanStampLocationModel* scanStampBottomCenterModel = new ScanStampLocationModel();
        scanStampBottomCenterModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::bottomCenter);
        ScanStampLocationModel* scanStampBottomRightModel = new ScanStampLocationModel();
        scanStampBottomRightModel->setLocationId(dune::spice::overlay_1::StampLocation::StampLocation::bottomRight);

        ScalingModel* scalingModel = new ScalingModel();
        scalingModel->setYScalePercent(100);
        scalingModel->setXScalePercent(100);
        scalingModel->setScaleToFitEnabled(FeatureEnabled::true_);
        pipelineOptionsModel->setScaling(scalingModel);
        pipelineOptionsModel->setWatermark(watermarkDetailsModel);
        pipelineOptionsModel->setImageModifications(imageModificationsModel);
        pipelineOptionsModel->setStampTopLeft(scanStampTopLeftModel);
        pipelineOptionsModel->setStampTopCenter(scanStampTopCenterModel);
        pipelineOptionsModel->setStampTopRight(scanStampTopRightModel);
        pipelineOptionsModel->setStampBottomLeft(scanStampBottomLeftModel);
        pipelineOptionsModel->setStampBottomCenter(scanStampBottomCenterModel);
        pipelineOptionsModel->setStampBottomRight(scanStampBottomRightModel);
        jobTicketModel->setPipelineOptions(pipelineOptionsModel);

        srcModel->setScan(scanModel);
        dstModel->setPrint(printModel);
        jobTicketModel->setDest(dstModel);
        jobTicketModel->setSrc(srcModel);

    }

    void SetUp() override
    {
        GivenTestingCopyAppWorkflow::SetUp();
        fillScanStatusModelFlatbedLoaded(scanStatusModel_);
        startApplication();
        
        //Register jobInfomodels seperately
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
    }

    void TearDown() override
    {
        GivenTestingCopyAppWorkflow::TearDown();
    }
};

TEST_F(GivenCopyAppWorkflowIsStartedWithFlatbedPreviewButtonNotVisible, DISABLED_WhenFlatbedIsLoadedPagesPerSheetSelected2_PreviewButtonAvailable)
{

    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);


    WAIT_COMPARE(stateMachine_->property("isJobSubscribed"), true)

    jobInfoModel1_->setState(dune::spice::jobManagement_1::State::State::ready);
    jobInfoModel2_->setState(dune::spice::jobManagement_1::State::State::ready);

    WAIT_FOR_ITEM(contentItem_, "#_ExpandButton");
    ASSERT_TRUE(item);
    mouseClick(item, Qt::LeftButton);

    {
        WAIT_COMPARE(stateMachine_->property("jobState"), "ready")
        QQuickItem* previewButton = querySelector(contentItem_, "#previewButton");
        ASSERT_EQ(previewButton->property("visible").toBool(), true);
    }
}

class GivenCopyAppWorkflowIsConnected : public GivenTestingCopyAppWorkflow
{
  public:
    GivenCopyAppWorkflowIsConnected() = default;

    void SetUp() override
    {
        GivenTestingCopyAppWorkflow::SetUp();
    }
    void TearDown() override
    {
        delete propertyMap_;
        delete systemServices_;
        SpiceWorkflowFixture::TearDown();
    }
};

TEST_F(GivenCopyAppWorkflowIsConnected, WhenCopyAppIsConnected_ThenCopyModeIsSetInQmlEngine)
{
    std::future<void> completionFuture;
    std::function<void()> f = [&]() { aut_->connected(nullptr, completionFuture); };
    SpiceGuiFixture::executeTask<decltype(f)>(f);

    auto menuResourceCopyMode = qvariant_cast<IMenuResource*>(mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->contextProperty("_copyModeSettingsResource"));
    auto copyModeNode = qobject_cast<IMenu *>(menuResourceCopyMode->getNodeById(QString("copyModeSettingsPage")));

    ASSERT_TRUE(copyModeNode);
    ASSERT_EQ(copyModeNode->getId(), "copyModeSettingsPage");
    ASSERT_EQ(copyModeNode->getPriority(), (unsigned int)1);
    ASSERT_EQ(copyModeNode->getMenuType(), IMenu::MenuType::CONTROLPANEL);
}


class GivenCopyAppWorkflowIsPriorityModeStarted : public GivenTestingCopyAppWorkflow
{
  public:
    GivenCopyAppWorkflowIsPriorityModeStarted() = default;

    void SetUp() override
    {
        GivenTestingCopyAppWorkflow::SetUp();
    }
    void TearDown() override
    {
        delete propertyMap_;
        delete systemServices_;
        if(application_){
            application_->deleteLater();
        }
        if(stateMachine_){
            stateMachine_->deleteLater();
        }
        if(copyAppStack_){
            copyAppStack_->deleteLater();
        }      
        if(shortcutListElementPrivateModel_) delete shortcutListElementPrivateModel_;
        if(shortcutListElementPrivateModel_1) delete shortcutListElementPrivateModel_1;
        if(shortcutListElementPrivateModel_2) delete shortcutListElementPrivateModel_2;
        if(shortcutListElementCustomModel_1) delete shortcutListElementCustomModel_1;
        if(mockHomeScreen_) mockHomeScreen_->deleteLater();
        devicesupportedShortcutTypes->deleteLater();      
        SpiceWorkflowFixture::TearDown();
    }
    
};

TEST_F(GivenCopyAppWorkflowIsPriorityModeStarted, WhenCopyAppIsStarted_CreatePriorityModeSession_ThenDestroyPriorityModeSession)
{
    dune::spice::jobManagement_1::PriorityModeSessionModel* prioritySessionModel = nullptr;
    
    EXPECT_CALL(*mockIResourceStore_, createInstance(A<dune::spice::core::ResourceStoreTypes::Type>(), A<QString>()))
        .WillRepeatedly(Return(prioritySessionModel = new dune::spice::jobManagement_1::PriorityModeSessionModel()));
    EXPECT_CALL(*mockIResourceStore_, create(_, _, _, _)).WillRepeatedly(testing::Invoke([](QString url, dune::spice::core::ISpiceModel* spiceModel, bool getConstraint = false, QVariantMap queryParameters = QVariantMap())
        {
            auto future = new NiceMock<MockIResourceStoreFuture>();
 
            ON_CALL(*future, get()).WillByDefault(Return(spiceModel));
 
            future->setParent(QCoreApplication::instance());
 
            QTimer::singleShot(0, [=]() {
                future->resolved(future);
                future->deleteLater();
            });
 
            return future;
        }));

    EXPECT_CALL(*mockIResourceStore_, create(QString("/cdm/jobManagement/v1/priorityModeSessions"), _, _, _))
        .WillOnce(testing::Invoke([](QString url, dune::spice::core::ISpiceModel* spiceModel, bool getConstraint = false, QVariantMap queryParameters = QVariantMap())
        {
            auto future = new NiceMock<MockIResourceStoreFuture>();
 
            ON_CALL(*future, get()).WillByDefault(Return(spiceModel));
 
            future->setParent(QCoreApplication::instance());
 
            QTimer::singleShot(0, [=]() {
                future->resolved(future);
                future->deleteLater();
            });
 
            return future;
        }));
    
    startApplication();

    EXPECT_CALL(*mockIResourceStore_, destroyResource(prioritySessionModel,_))
        .WillOnce(testing::Invoke([](dune::spice::core::ISpiceModel* spiceModel, QVariantMap queryParameters = QVariantMap())
        {
            auto future = new NiceMock<MockIResourceStoreFuture>();
 
            future->setParent(QCoreApplication::instance());
 
            QTimer::singleShot(0, [=]() {
                future->resolved(future);
                future->deleteLater();
            });

            EXPECT_TRUE(spiceModel);

            return future;
            
        }));

    aut_->quit();

}

class GivenAConnectedCopyAppWorkflow: public GivenTestingCopyAppWorkflow
{
  public:
    GivenAConnectedCopyAppWorkflow() = default;

    void SetUp() override
    {
        SpiceWorkflowFixture::configureS();
        GivenTestingCopyAppWorkflow::SetUp();
    }

    void TearDown() override
    {
        GivenTestingCopyAppWorkflow::TearDown();
    }
};

TEST_F(GivenAConnectedCopyAppWorkflow, WhenCopyAppIsStartedWithUnSupportedPreview_ThenSecondaryScreenIsNotVisible)
{
    mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty(
                                        "_scanPreviewSupported", false);
    startApplication();
    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);

    WAIT_COMPARE(copyLandingView->property("mainPanel").isNull(), false);
    //Verifying that Secondary panel doesnot exist
    WAIT_COMPARE(copyLandingView->property("secondaryPanel").isNull(), true);

    QQuickItem* previewButton = querySelector(contentItem_, "#_ExpandButton");
    ASSERT_FALSE(previewButton);
}

TEST_F(GivenAConnectedCopyAppWorkflow, WhenCopyAppIsStartedWithSupportedPreview_ThenSecondaryScreenIsVisible)
{
    mockIGuiApplicationEngine->getQQmlEngine()->rootContext()->setContextProperty(
                                        "_scanPreviewSupported", true);
    startApplication();
    WAIT_COMPARE(stateMachine_->property("activeState"), CopyAppState::GET_CONFIGURATIONS)
    QQuickItem* copyLandingView = querySelector(copyAppStack_, "#copyLandingView");
    ASSERT_TRUE(copyLandingView);

    //Verifying that both the panels exist
    WAIT_COMPARE(copyLandingView->property("mainPanel").isNull(), false);
    WAIT_COMPARE(copyLandingView->property("secondaryPanel").isNull(), false);

    WAIT_FOR_ITEM(contentItem_, "#_ExpandButton");
    ASSERT_TRUE(item);
    mouseClick(item, Qt::LeftButton);
    {
        WAIT_FOR_ITEM(contentItem_, "#prePreview");
    }
}