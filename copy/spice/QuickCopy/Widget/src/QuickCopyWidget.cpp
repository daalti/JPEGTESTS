/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   QuickCopyWidget.cpp
 * @date   Thu, 22 Feb 2024 11:08:39 -0700
 * @brief  Component Holds different Flavours of QuickCopy.
 *
 * (C) Copyright 2024 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "QuickCopyWidget.h"
#include "common_debug.h"
#include "QuickCopyWidget_TraceAutogen.h"
#include "IConfigurationService.h"
#include "IPathServices.h"
#include <QObject>
#include "QmlUtils.h"
#include "IResourceStoreFuture.h"

// Factory method

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_spice_QuickCopyWidget)
{
    dune::copy::spice::QuickCopyWidget *instance = new dune::copy::spice::QuickCopyWidget(instanceName);
    assert(instance != nullptr);
    return static_cast<dune::framework::component::IComponent *>(instance);
}


namespace dune { namespace copy { namespace spice {

// Constructor and destructor

QuickCopyWidget::QuickCopyWidget(const char *instanceName) :
    instanceName_(instanceName)
{
    CHECKPOINTC("%s/QuickCopyWidget: constructed", instanceName_);
}

QuickCopyWidget::~QuickCopyWidget()
{
    if(copyShortcutModel_) copyShortcutModel_->deleteLater();
}

// IComponent methods.

dune::framework::component::ComponentFlavorUid QuickCopyWidget::getComponentFlavorUid() const
{
    return GET_MODULE_UID(QuickCopyWidget);
}

const char *QuickCopyWidget::getComponentInstanceName() const
{
    return instanceName_;
}

void QuickCopyWidget::initialize(WorkingMode mode, const dune::framework::component::SystemServices *services)
{
    DUNE_UNUSED(mode);
    DUNE_UNUSED(services);
    services_ = services;
    if ( services->configurationService_ != nullptr )
    {
        configuration_ = getConfiguration(services->configurationService_);
    }

    CHECKPOINTC("%s/QuickCopyWidget: initialized", instanceName_);
}

void * QuickCopyWidget::getInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName)
{
    DUNE_UNUSED(portName);
    void *interfacePtr = nullptr;
    if (interfaceUid == GET_INTERFACE_UID(IQuickCopy))
    {
        interfacePtr = static_cast<IQuickCopy *>(this);
    }
    CHECKPOINTC("%s/QuickCopyWidget: getInterface %" PRIu32 " from port %s with addr %p", instanceName_, interfaceUid, portName, interfacePtr);
    return interfacePtr;
}


void QuickCopyWidget::setInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName, void *interfacePtr)
{
     if (interfaceUid == GET_INTERFACE_UID(dune::spice::widget::IWidgetService))
    {
        CHECKPOINTC("%s CopyAppWorkflow: setInterfave widgetService", instanceName_);

        widgetService_ = static_cast<dune::spice::widget::IWidgetService *>(interfacePtr);
    }
    if (interfaceUid == GET_INTERFACE_UID(dune::spice::guiCore::IGuiApplicationEngine))
    {
        applicationEngine_ = static_cast<dune::spice::guiCore::IGuiApplicationEngine *>(interfacePtr);
    }
    CHECKPOINTC("%s/QuickCopyWidget: setInterface %" PRIu32 " to port %s with addr %p", instanceName_, interfaceUid, portName, interfacePtr);
}

void QuickCopyWidget::connected(dune::framework::component::IComponentManager *componentManager, std::future<void> &asyncCompletion)
{
    DUNE_UNUSED(componentManager);
    DUNE_UNUSED(asyncCompletion);
    fillCopyWidgetSummaryList();
    QString rccPath = QStringLiteral("%1/%2/%3.rcc").arg(services_->pathServices_->getPathDirectory()->getPath(dune::framework::storage::path::Paths::RESOURCE_DIRECTORY).c_str()).arg(dune::spice::guiCore::QmlUtils::getFlavorUidInHex(getComponentFlavorUid())).arg("QuickCopy");
    dune::spice::guiCore::QmlUtils::registerResource(rccPath);
    QMetaObject::invokeMethod(QAbstractEventDispatcher::instance(qGuiApp->thread()),
                                [&] {
                                    if(widgetService_)
                                    {
                                        auto resourceStore = applicationEngine_->getResourceStore();

                                        auto onResourceStoreReady = [this,resourceStore]() {
                                            dune::spice::core::IResourceStoreFuture* future = resourceStore->subscribe("/cdm/shortcut/v1/shortcuts/cedab422-33b3-4638-b6a1-604e54525215");
                                            auto connection = QObject::connect(future, &dune::spice::core::IResourceStoreFuture::resolved, [this](dune::spice::core::IResourceStoreFuture *future) {
                                                CHECKPOINTC("%s/ QuickCopyWidget: Subscription to copy shortcut resolved", instanceName_);
                                                copyShortcutModel_ = future->get();
                                                auto shortcutModel = static_cast<dune::spice::shortcut_1::ShortcutModel *>(copyShortcutModel_->getData());
                                                dune::spice::widget::WidgetItem* copyWidget = widgetService_->getWidget("quickcopy");
                                                auto onCopyShortcutStateChanged = [=]() {
                                                    if(copyWidget)
                                                    {
                                                        if(shortcutModel->getState() == dune::spice::shortcut_1::State::State::disabled)
                                                            copyWidget->setVisible(false);
                                                        else
                                                            copyWidget->setVisible(true);
                                                    }
                                                };
                                                    onCopyShortcutStateChanged();
                                                    QObject::connect(shortcutModel, &dune::spice::shortcut_1::ShortcutModel::stateChanged, onCopyShortcutStateChanged);
                                                });

                                                QObject::connect(future, &dune::spice::core::IResourceStoreFuture::rejected, [this](dune::spice::core::IResourceStoreFuture *future) {
                                                    CHECKPOINTC("%s/ QuickCopyWidget: Subscription to copy shortcut rejected",instanceName_);
                                                });
                                        };

                                        auto connection = QObject::connect(resourceStore, &dune::spice::core::IResourceStore::ready, onResourceStoreReady);
                                        if (resourceStore->isReady())
                                        {
                                            QObject::disconnect(connection);
                                            onResourceStoreReady();
                                        }
                                        applicationEngine_->getQQmlEngine()->rootContext()->setContextProperty(
                                        "_quickCopyWidgetSummaryList", QVariant(quickCopyWidgetSummaryList_));
                                    }}); 
    
    CHECKPOINTC("%s/QuickCopyWidget: connected", instanceName_);
}

void QuickCopyWidget::shutdown(ShutdownCause cause, std::future<void> &asyncCompletion)
{
    DUNE_UNUSED(cause);
    DUNE_UNUSED(asyncCompletion);
    CHECKPOINTC("%s/QuickCopyWidget: shutdown", instanceName_);
}

std::unique_ptr<QuickCopyWidgetConfigT> QuickCopyWidget::getConfiguration(dune::framework::resources::IConfigurationService *configurationService) const
{
    assert(configurationService);
    dune::framework::resources::IConfigurationService::ConfigurationRawData rawConfiguration =
        configurationService->getConfiguration(GET_MODULE_UID(QuickCopyWidget), instanceName_);
    if (rawConfiguration.data && (rawConfiguration.size > 0))
    {
        flatbuffers::Verifier verifier(rawConfiguration.data.get(), rawConfiguration.size);
        assert(VerifyQuickCopyWidgetConfigBuffer(verifier));
        return UnPackQuickCopyWidgetConfig(rawConfiguration.data.get());
    }
    else
    {
        return std::unique_ptr<QuickCopyWidgetConfigT>();
    }
}

void QuickCopyWidget::fillCopyWidgetSummaryList()
{
    if(configuration_->listOfWidgetSummary.size() > 0)
    {
        auto listOfWidgetSummary = configuration_->listOfWidgetSummary;
        for(unsigned int i=0; i < listOfWidgetSummary.size(); i++){
            std::string str = listOfWidgetSummary[i];
            quickCopyWidgetSummaryList_.append(QString(str.c_str()));
        }
    }
}

}}}  // namespace dune::copy::spice

