/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   QuickCopyFooter.cpp
 * @date   Thu, 22 Feb 2024 11:08:39 -0700
 * @brief  Component Holds different Flavours of QuickCopy.
 *
 * (C) Copyright 2024 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "QuickCopyFooter.h"

#include "common_debug.h"
#include "QuickCopyFooter_TraceAutogen.h"
#include "ErrorManager.h"
#include "QmlUtils.h"
#include "IPathServices.h"
// Factory method

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_spice_QuickCopyFooter)
{
    dune::copy::spice::QuickCopyFooter *instance = new dune::copy::spice::QuickCopyFooter(instanceName);
    assert(instance != nullptr);
    return static_cast<dune::framework::component::IComponent *>(instance);
}


namespace dune { namespace copy { namespace spice {

// Constructor and destructor

QuickCopyFooter::QuickCopyFooter(const char *instanceName) :
    instanceName_(instanceName)
{
    CHECKPOINTC("%s/QuickCopyFooter: constructed", instanceName_);
}

QuickCopyFooter::~QuickCopyFooter()
{
    if(quickCopyComponentHandler_) 
        quickCopyComponentHandler_->deleteLater();
}

// IComponent methods.

dune::framework::component::ComponentFlavorUid QuickCopyFooter::getComponentFlavorUid() const
{
    return GET_MODULE_UID(QuickCopyFooter);
}

const char *QuickCopyFooter::getComponentInstanceName() const
{
    return instanceName_;
}

void QuickCopyFooter::initialize(WorkingMode mode, const dune::framework::component::SystemServices *services)
{
    DUNE_UNUSED(mode);

    if ( services->configurationService_ != nullptr )
    {
        configuration_ = getConfiguration(services->configurationService_);
    }
    services_ = services;
    CHECKPOINTC("%s/QuickCopyFooter: initialized", instanceName_);
}

void * QuickCopyFooter::getInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName)
{
    DUNE_UNUSED(portName);
    void *interfacePtr = nullptr;
    if (interfaceUid == GET_INTERFACE_UID(IQuickCopy))
    {
        interfacePtr = static_cast<IQuickCopy *>(this);
    }
    CHECKPOINTC("%s/QuickCopyFooter: getInterface %" PRIu32 " from port %s with addr %p", instanceName_, interfaceUid, portName, interfacePtr);
    return interfacePtr;
}

void QuickCopyFooter::setInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName, void *interfacePtr)
{
    DUNE_UNUSED(interfacePtr);
    CHECKPOINTC("%s/QuickCopyFooter: setInterface %" PRIu32 " to port %s with addr %p", instanceName_, interfaceUid, portName, interfacePtr);
    if (interfaceUid == GET_INTERFACE_UID(dune::spice::guiCore::IGuiApplicationEngine))
    {
        applicationEngine_ = static_cast<dune::spice::guiCore::IGuiApplicationEngine *>(interfacePtr);
    }
}

void QuickCopyFooter::connected(dune::framework::component::IComponentManager *componentManager, std::future<void> &asyncCompletion)
{
    DUNE_UNUSED(componentManager);
    DUNE_UNUSED(asyncCompletion);
    #if (!defined(NDEBUG)) && (!defined(SPICE_FORCE_QRC_COMPILATION) || SPICE_FORCE_QRC_COMPILATION == 0)
    QString rccPath = QStringLiteral("%1/%2/%3.rcc").arg(services_->pathServices_->getPathDirectory()->getPath(dune::framework::storage::path::Paths::RESOURCE_DIRECTORY).c_str()).arg(dune::spice::guiCore::QmlUtils::getFlavorUidInHex(getComponentFlavorUid())).arg("QuickCopy");
    dune::spice::guiCore::QmlUtils::registerResource(rccPath);   
    #endif

    QMetaObject::invokeMethod(QAbstractEventDispatcher::instance(qGuiApp->thread()), [&] {
        quickCopyComponentHandler_ = dune::spice::guiCore::QmlUtils::createObject(applicationEngine_->getQQmlEngine(), "qrc:/QuickCopy/QuickCopyComponentHandler.qml");
    });
    CHECKPOINTC("%s/QuickCopyFooter: connected", instanceName_);
}

void QuickCopyFooter::shutdown(ShutdownCause cause, std::future<void> &asyncCompletion)
{
    DUNE_UNUSED(cause);
    DUNE_UNUSED(asyncCompletion);
    CHECKPOINTC("%s/QuickCopyFooter: shutdown", instanceName_);
}

std::unique_ptr<QuickCopyFooterConfigT> QuickCopyFooter::getConfiguration(dune::framework::resources::IConfigurationService *configurationService) const
{
    assert(configurationService);
    dune::framework::resources::IConfigurationService::ConfigurationRawData rawConfiguration =
        configurationService->getConfiguration(GET_MODULE_UID(QuickCopyFooter), instanceName_);
    if (rawConfiguration.data && (rawConfiguration.size > 0))
    {
        flatbuffers::Verifier verifier(rawConfiguration.data.get(), rawConfiguration.size);
        assert(VerifyQuickCopyFooterConfigBuffer(verifier));
        return UnPackQuickCopyFooterConfig(rawConfiguration.data.get());
    }
    else
    {
        return std::unique_ptr<QuickCopyFooterConfigT>();
    }
}
/// @todo implement methods from IQuickCopy here.

}}}  // namespace dune::copy::spice

