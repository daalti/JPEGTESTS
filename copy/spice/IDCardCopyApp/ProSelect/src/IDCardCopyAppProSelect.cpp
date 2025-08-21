///////////////////////////////////////////////////////////////////////////////
/**
 * @file   IDCardCopyAppProSelect.cpp
 * @date   April, 05 2021
 * @brief
 *
 * (C) Copyright 2021 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "IDCardCopyAppProSelect.h"
#include "IPathDirectory.h"

#include <QAbstractEventDispatcher>
#include <QGuiApplication>
#include <QQmlContext>
#include <QQmlEngine>

#include "common_debug.h"

#include "IDCardCopyAppProSelect_TraceAutogen.h"

#include "ErrorManager.h"
#include "IConfigurationService.h"
#include "IMenuResource.h"
#include "IPathServices.h"
#include "QmlUtils.h"
#include "SpiceDataMap.h"

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_spice_IDCardCopyAppProSelect)
{
    dune::copy::spice::IDCardCopyAppProSelect *instance = new dune::copy::spice::IDCardCopyAppProSelect(instanceName);
    assert(instance != nullptr);
    return static_cast<dune::framework::component::IComponent *>(instance);
}

using namespace dune::framework::component;
using namespace dune::spice::guiCore;
using dune::framework::storage::path::Paths;

namespace dune { namespace copy { namespace spice {

IDCardCopyAppProSelect::IDCardCopyAppProSelect(const char *instanceName) : SpiceGuiApplicationCommon(instanceName)
{
    CHECKPOINTC("%s/IDCardCopyAppProSelect: constructed", instanceName);
}

IDCardCopyAppProSelect::~IDCardCopyAppProSelect()
{
    if (idcopySettingsResource_)
    {
        idcopySettingsResource_->deleteLater();
    }
}

// IComponent methods.
dune::framework::component::ComponentFlavorUid IDCardCopyAppProSelect::getComponentFlavorUid() const
{
    return GET_MODULE_UID(IDCardCopyAppProSelect);
}


void IDCardCopyAppProSelect::connected(dune::framework::component::IComponentManager *componentManager,
                                 std::future<void> &                            asyncCompletion)
{
    SpiceGuiApplicationCommon::connected(componentManager, asyncCompletion);

    pathToResource_ = services_->pathServices_->getPathDirectory()->getPath(Paths::RESOURCE_DIRECTORY).c_str();
    if (pathToResource_.endsWith("/")) pathToResource_.remove(pathToResource_.size() - 1, 1);
    pathToResource_ = QString("%1/0x%2/").arg(pathToResource_).arg(getComponentFlavorUid(), 0, 16);
    idcopySettingsResource_->moveToThread(nullptr);

    QSemaphore waitForInit;

    QMetaObject::invokeMethod(QAbstractEventDispatcher::instance(qGuiApp->thread()),
                              [&] {
                                  idcopySettingsResource_->moveToThread(qGuiApp->thread());
                                  applicationEngine_->getQQmlEngine()->rootContext()->setContextProperty(
                                      "_idcopySettingsResource", idcopySettingsResource_);

                                  applicationEngine_->getQQmlEngine()->setObjectOwnership(idcopySettingsResource_,
                                                                                          QQmlEngine::CppOwnership);
                                  waitForInit.release();
                              },
                              Qt::QueuedConnection);
    waitForInit.acquire();
}

}}}  // namespace dune::copy::spice
