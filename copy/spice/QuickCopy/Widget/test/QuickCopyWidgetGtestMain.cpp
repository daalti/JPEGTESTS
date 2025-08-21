/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   QuickCopyWidgetGtestMain.cpp
 * @date   Thu, 22 Feb 2024 11:08:39 -0700
 * @brief  Component Holds different Flavours of QuickCopy.
 *
 * (C) Copyright 2024 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "QuickCopyWidget.h"

#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include "IPathDirectory.h"
#include "SimplePathDirMock.h"
#include "TestSystemServices.h"
#include "GTestConfigHelper.h"
#include "IWidgetService.h"
#include "MockIWidgetService.h"
#include "MockIResourceStore.h"
#include "SpiceGuiFixture.h"
#include "SpiceWorkflowFixture.h"
#include "QmlUtils.h"

#include "com_hp_cdm_service_shortcut_version_1_models_generated.h"
#include "com_hp_cdm_service_shortcut_version_1_qmlRegistration_generated.h"
#include "com_hp_cdm_service_shortcut_version_1_sharedTypes_shortcut_models_generated.h"
using QuickCopyWidget              = dune::copy::spice::QuickCopyWidget;
using TestSystemServices    = dune::framework::component::TestingUtil::TestSystemServices;
using IComponent            = dune::framework::component::IComponent;
using IComponentManager     = dune::framework::component::IComponentManager;
using SystemServices        = dune::framework::component::SystemServices;
using SysTrace              = dune::framework::core::dbg::SysTrace;
using CheckpointLevel       = SysTrace::CheckpointLevel;
using FeatureEnabled        = dune::spice::glossary_1::FeatureEnabled::FeatureEnabled;
using GTestConfigHelper     = dune::framework::core::gtest::GTestConfigHelper;
using Paths                 = dune::framework::storage::path::Paths;

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
    return RUN_ALL_TESTS();
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenANewQuickCopyWidget : public ::testing::Test
//
///////////////////////////////////////////////////////////////////////////////

class GivenANewQuickCopyWidget : public SpiceWorkflowFixture
{
  public:

    GivenANewQuickCopyWidget() : component_(nullptr), systemServices_(nullptr), componentManager_(nullptr) {};

    virtual void SetUp() override;

    virtual void TearDown() override;
    void mockWidgetService();

    void mockCopyShortcut();

  protected:

    dune::copy::spice::QuickCopyWidget                          * component_{nullptr};
    TestSystemServices                              * systemServices_{nullptr};
    dune::framework::component::IComponentManager   * componentManager_{nullptr};
    dune::spice::widget::MockIWidgetService*                widgetService_{nullptr};
    dune::spice::widget::WidgetItem*                        widgetItem{nullptr};
    std::shared_ptr<dune::spice::shortcut_1::ShortcutModel>                  CopyShortcutModel;
    const QString copyShortcutUrl{"/cdm/shortcut/v1/shortcuts/cedab422-33b3-4638-b6a1-604e54525215"};
};

void GivenANewQuickCopyWidget::SetUp()
{
    SpiceWorkflowFixture::SetUp();
    systemServices_ = new TestSystemServices();
    systemServices_->setConfigurationServiceBehaviour("./testResources/QuickCopyWidgetConfig.fbs", "./testResources/QuickCopyWidgetTestData.json");
    
    auto spm = new dune::framework::storage::path::SimplePathServicesMock();
    auto spd = new dune::framework::storage::path::SimplePathDirectory();
    spd->addPath(dune::framework::storage::path::Paths::RESOURCE_DIRECTORY, SpiceGuiGTestEnvironment::resourceDirectory.toStdString());
    spm->setPathDirectory(spd);
    systemServices_->setPathServices(spm);

    component_ = new QuickCopyWidget("myInstance");
    ASSERT_NE(nullptr, component_);
}

void GivenANewQuickCopyWidget::TearDown()
{
    qmltest::wait(30);
    delete component_;
    delete systemServices_;
    if(widgetService_){
            widgetService_->deleteLater();
    }
    SpiceWorkflowFixture::TearDown();
}
void GivenANewQuickCopyWidget::mockWidgetService()
{
    widgetService_ = new NiceMock<dune::spice::widget::MockIWidgetService>();
    QObjectListModel * widgets = new QObjectListModel(widgetService_);        
    widgetItem = new dune::spice::widget::WidgetItem(widgets);
    widgetItem->setId("quickCopy");
    widgetItem->setVisible(true);
    widgetItem->setPosition(0);
    widgets->append(widgetItem);
    ON_CALL(*widgetService_, getWidget(_)).WillByDefault(Return(widgetItem));
}

void GivenANewQuickCopyWidget::mockCopyShortcut()
{
    CopyShortcutModel = mockIResourceStore_->registerFakeResource<dune::spice::shortcut_1::ShortcutModel>(new dune::spice::shortcut_1::ShortcutModel(copyShortcutUrl));
    CopyShortcutModel->setId(QString::fromStdString("cedab422-33b3-4638-b6a1-604e54525415"));
    CopyShortcutModel->setPermissionId(QString::fromStdString("cedab422-33b3-4638-b6a1-604e54525415"));
    CopyShortcutModel->setType(dune::spice::shortcut_1::Type::Type::nativeApp);
    CopyShortcutModel->setSource(dune::spice::shortcut_1::Source::Source::scan);
    CopyShortcutModel->getDestinations()->append(QVariant((int)dune::spice::shortcut_1::Destination::Destination::print));
    CopyShortcutModel->setAction(dune::spice::shortcut_1::Action::Action::open);
    CopyShortcutModel->setCopyAllowed(FeatureEnabled::true_);
}

TEST_F(GivenANewQuickCopyWidget, WhenInitializeIsCalled_TheComponentGetsInitialized)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, systemServices_);

    ASSERT_TRUE(true);

}

TEST_F(GivenANewQuickCopyWidget, WhenTheConnectSequenceIsCalled_TheComponentGetsConnected)
{
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));

    // fill here any setInterface required
    comp->setInterface(GET_INTERFACE_UID(dune::spice::guiCore::IGuiApplicationEngine), "",
                           static_cast<void*>(mockIGuiApplicationEngine));
    comp->setInterface(GET_INTERFACE_UID(dune::spice::widget::IWidgetService), "", widgetService_);
    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

}

TEST_F(GivenANewQuickCopyWidget ,WhenCopyAppIsConnectedShortcutsIsSubscribed){
    mockWidgetService();
    mockCopyShortcut();
    IComponent * comp = static_cast<IComponent*>(component_);
    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));
    comp->setInterface(GET_INTERFACE_UID(dune::spice::guiCore::IGuiApplicationEngine), "",
                           static_cast<void*>(mockIGuiApplicationEngine));
    comp->setInterface(GET_INTERFACE_UID(dune::spice::widget::IWidgetService), "", widgetService_);

    EXPECT_CALL(*mockIResourceStore_, subscribe(copyShortcutUrl, A<bool>(), A<QVariantMap>()));
    std::future<void> completionFuture;
    comp->connected(nullptr, completionFuture);

    WAIT_COMPARE(widgetItem->isVisible(),true);
}

TEST_F(GivenANewQuickCopyWidget, WhenCopyAppIsConnectedEnablingDisablingCopyAppAppliesToWidget)
{
    mockWidgetService();
    mockCopyShortcut();
    IComponent * comp = static_cast<IComponent*>(component_);
    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));
    comp->setInterface(GET_INTERFACE_UID(dune::spice::guiCore::IGuiApplicationEngine), "",
                           static_cast<void*>(mockIGuiApplicationEngine));
    comp->setInterface(GET_INTERFACE_UID(dune::spice::widget::IWidgetService), "", widgetService_);

    EXPECT_CALL(*mockIResourceStore_, subscribe(copyShortcutUrl, A<bool>(), A<QVariantMap>()));
    std::future<void> completionFuture;
    std::function<void()> f = [&]() { comp->connected(nullptr, completionFuture); };
    SpiceGuiFixture::executeTask<decltype(f)>(f);

    ASSERT_EQ(widgetItem->isVisible(),true);
    CopyShortcutModel->setState(dune::spice::shortcut_1::State::State::disabled);
    WAIT_COMPARE(widgetItem->isVisible(),false);
}

///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedQuickCopyWidget : Do here tests of public api
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedQuickCopyWidget :public GivenANewQuickCopyWidget
{
  public:

    GivenAConnectedQuickCopyWidget() {};

    virtual void SetUp() override;

    virtual void TearDown() override;
    
};

void GivenAConnectedQuickCopyWidget::SetUp()
{
    GivenANewQuickCopyWidget::SetUp();
    mockWidgetService();
    mockCopyShortcut();
    IComponent * comp = static_cast<IComponent*>(component_);

    comp->initialize(IComponent::WorkingMode::NORMAL, static_cast<SystemServices*>(systemServices_));
    comp->setInterface(GET_INTERFACE_UID(dune::spice::guiCore::IGuiApplicationEngine), "",
                           static_cast<void*>(mockIGuiApplicationEngine));
    comp->setInterface(GET_INTERFACE_UID(dune::spice::widget::IWidgetService), "", widgetService_);
    // fill here any setInterface required

    std::future<void> asyncCompletion;
    comp->connected(componentManager_, asyncCompletion);
    if (asyncCompletion.valid())
    {
        asyncCompletion.wait();
    }

}

void GivenAConnectedQuickCopyWidget::TearDown()
{
    GivenANewQuickCopyWidget::TearDown(); 
}



///////////////////////////////////////////////////////////////////////////////
//
// class GivenAConnectedQuickCopyWidgetReadyToCallShutdown : shutdown case.
// Dummy class that inherits from GivenAConnectedQuickCopyWidget in order to reuse code
// and enable parametrized tests. 
//
///////////////////////////////////////////////////////////////////////////////

class GivenAConnectedQuickCopyWidgetReadyToCallShutdown : public GivenAConnectedQuickCopyWidget,
                           public ::testing::WithParamInterface<IComponent::ShutdownCause>
{

};


TEST_P(GivenAConnectedQuickCopyWidgetReadyToCallShutdown, whenShutdownIsCalled_TheComponentGetsShutdown)
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

}

INSTANTIATE_TEST_CASE_P(InstantiationName, GivenAConnectedQuickCopyWidgetReadyToCallShutdown, ::testing::Values(
 IComponent::ShutdownCause(IComponent::ShutdownCause::POWER_OFF),
 IComponent::ShutdownCause(IComponent::ShutdownCause::REBOOT),
 IComponent::ShutdownCause(IComponent::ShutdownCause::SEVERE_ERROR),
 IComponent::ShutdownCause(IComponent::ShutdownCause::EMERGENCY_ERROR),
 IComponent::ShutdownCause(IComponent::ShutdownCause::CRITICAL_ERROR)
));


