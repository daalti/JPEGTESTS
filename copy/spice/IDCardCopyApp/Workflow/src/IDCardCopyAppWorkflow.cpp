/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   IDCardCopyAppWorkflow.cpp
 * @date   Tue, 28 Sep 2021 05:12:18 -0600
 * @brief  
 *
 * (C) Copyright 2021 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "IDCardCopyAppWorkflow.h"
#include "IPathDirectory.h"

#include <QAbstractEventDispatcher>
#include <QGuiApplication>
#include <QQmlContext>
#include <QQmlEngine>

#include "common_debug.h"
#include "IDCardCopyAppWorkflow_TraceAutogen.h"

#include "ErrorManager.h"
#include "IConfigurationService.h"
#include "IMenuResource.h"
#include "IPathServices.h"
#include "QmlUtils.h"
#include "SpiceDataMap.h"
// Factory method

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_spice_IDCardCopyAppWorkflow)
{
    dune::copy::spice::IDCardCopyAppWorkflow *instance = new dune::copy::spice::IDCardCopyAppWorkflow(instanceName);
    assert(instance != nullptr);
    return static_cast<dune::framework::component::IComponent *>(instance);
}

using namespace dune::framework::component;
using namespace dune::spice::guiCore;
using dune::framework::storage::path::Paths;

namespace dune { namespace copy { namespace spice {

// Constructor and destructor

IDCardCopyAppWorkflow::IDCardCopyAppWorkflow(const char *instanceName) :
    SpiceGuiApplicationCommon(instanceName)
{
    instanceName_ =  instanceName;
    CHECKPOINTC("%s/IDCardCopyAppWorkflow: constructed", instanceName_);
}

IDCardCopyAppWorkflow::~IDCardCopyAppWorkflow()
{
    if (idcopySettingsResource_)
    {
        idcopySettingsResource_->deleteLater();
    }
}

void  IDCardCopyAppWorkflow::initialize(WorkingMode mode, const dune::framework::component::SystemServices *services)
{
    DUNE_UNUSED(mode);
    services_ = services;
    //SpiceGuiApplicationCommon::initialize(mode, services);

    if (services_->configurationService_ != nullptr)
    {
        config_ = getConfiguration(services_->configurationService_);
    }
    CHECKPOINTC("%s/ IDCardCopyAppWorkflow: initialized", instanceName_);

}

// IComponent methods.

dune::framework::component::ComponentFlavorUid IDCardCopyAppWorkflow::getComponentFlavorUid() const
{
    return GET_MODULE_UID(IDCardCopyAppWorkflow);
}


void IDCardCopyAppWorkflow::connected(dune::framework::component::IComponentManager *componentManager, std::future<void> &asyncCompletion)
{
    auto listOfArray = config_->list;

    for(unsigned int i=0; i < listOfArray.size(); i++){
        std::string str = listOfArray[i];
        interactiveSummaryList_.append(QString(str.c_str()));
    }

    SpiceGuiApplicationCommon::connected(componentManager, asyncCompletion);

    pathToResource_ = services_->pathServices_->getPathDirectory()->getPath(Paths::RESOURCE_DIRECTORY).c_str();
    if (pathToResource_.endsWith("/")) pathToResource_.remove(pathToResource_.size() - 1, 1);
    pathToResource_ = QString("%1/0x%2/").arg(pathToResource_).arg(getComponentFlavorUid(), 0, 16);
    idcopySettingsResource_ = IMenuResource::createResourceForCSF(std::move(config_->settings));
    idcopySettingsResource_->setEngine(applicationEngine_->getQQmlEngine());

    idcopySettingsResource_->moveToThread(nullptr);

    QSemaphore waitForInit;

    QMetaObject::invokeMethod(QAbstractEventDispatcher::instance(qGuiApp->thread()),
                              [&] {
                                  idcopySettingsResource_->moveToThread(qGuiApp->thread());
                                  applicationEngine_->getQQmlEngine()->rootContext()->setContextProperty(
                                      "_idCardCopySettingsResource", idcopySettingsResource_);
                                    
                                  applicationEngine_->getQQmlEngine()->rootContext()->setContextProperty(
                                      "_idCopyinteractiveSummaryList", QVariant(interactiveSummaryList_));

                                  applicationEngine_->getQQmlEngine()->setObjectOwnership(idcopySettingsResource_,
                                                                                          QQmlEngine::CppOwnership);
                                  waitForInit.release();
                              },
                              Qt::QueuedConnection);
    waitForInit.acquire();
}


std::unique_ptr<InteractiveOrderListT> IDCardCopyAppWorkflow::getConfiguration(dune::framework::resources::IConfigurationService *configService) const
{
    assert(configService);
    auto rawConfig = configService->getConfiguration(GET_MODULE_UID(IDCardCopyAppWorkflow), instanceName_);
    if (rawConfig.data && (rawConfig.size > 0))
    {
        flatbuffers::Verifier verifier(rawConfig.data.get(), rawConfig.size);
        assert(VerifyInteractiveOrderListBuffer(verifier));
        return UnPackInteractiveOrderList(rawConfig.data.get());
    }
    return std::unique_ptr<InteractiveOrderListT>();

}


/// @todo implement methods from IIDCardCopyApp here.

}}}  // namespace dune::copy::spice

