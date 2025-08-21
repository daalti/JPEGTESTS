///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAppProSelect.cpp
 * @date   September, 09 2019
 * @brief
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyAppProSelect.h"
#include "IPathDirectory.h"

#include <QAbstractEventDispatcher>
#include <QGuiApplication>
#include <QQmlContext>
#include <QQmlEngine>

#include "common_debug.h"

#include "CopyAppProSelect_TraceAutogen.h"

#include "ErrorManager.h"
#include "IConfigurationService.h"
#include "IMenuResource.h"
#include "IPathServices.h"
#include "QmlUtils.h"
#include "SpiceDataMap.h"

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_spice_CopyAppProSelect)
{
    dune::copy::spice::CopyAppProSelect *instance = new dune::copy::spice::CopyAppProSelect(instanceName);
    assert(instance != nullptr);
    return static_cast<dune::framework::component::IComponent *>(instance);
}

namespace dune { namespace copy { namespace spice {

using namespace dune::framework::component;
using namespace dune::spice::guiCore;
using dune::framework::storage::path::Paths;

CopyAppProSelect::CopyAppProSelect(const char *instanceName) : SpiceGuiApplicationCommon(instanceName)
{
    CHECKPOINTC("%s/CopyAppProSelect: constructed", instanceName);
}

CopyAppProSelect::~CopyAppProSelect()
{
    if (copySettingsResource_)
    {
        copySettingsResource_->deleteLater();
    }
}

// IComponent methods.
dune::framework::component::ComponentFlavorUid CopyAppProSelect::getComponentFlavorUid() const
{
    return GET_MODULE_UID(CopyAppProSelect);
}

void CopyAppProSelect::connected(dune::framework::component::IComponentManager *componentManager,
                                 std::future<void> &                            asyncCompletion)
{
    SpiceGuiApplicationCommon::connected(componentManager, asyncCompletion);

    pathToResource_ = services_->pathServices_->getPathDirectory()->getPath(Paths::RESOURCE_DIRECTORY).c_str();
    if (pathToResource_.endsWith("/")) pathToResource_.remove(pathToResource_.size() - 1, 1);
    pathToResource_ = QString("%1/0x%2/").arg(pathToResource_).arg(getComponentFlavorUid(), 0, 16);
    copySettingsResource_->setEngine(applicationEngine_->getQQmlEngine());

    copySettingsResource_->moveToThread(nullptr);

    QSemaphore waitForInit;

    QMetaObject::invokeMethod(QAbstractEventDispatcher::instance(qGuiApp->thread()),
                              [&] {
                                  copySettingsResource_->moveToThread(qGuiApp->thread());
                                  applicationEngine_->getQQmlEngine()->rootContext()->setContextProperty(
                                      "_copySettingsResource", copySettingsResource_);

                                  applicationEngine_->getQQmlEngine()->setObjectOwnership(copySettingsResource_,
                                                                                          QQmlEngine::CppOwnership);
                                  waitForInit.release();
                              },
                              Qt::QueuedConnection);
    waitForInit.acquire();
}
}}}  // namespace dune::copy::spice
