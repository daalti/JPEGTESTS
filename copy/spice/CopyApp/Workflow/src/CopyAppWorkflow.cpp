///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAppWorkflow.cpp
 * @date   September, 09 2019
 * @brief
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyAppWorkflow.h"
#include "IPathDirectory.h"
#include <QAbstractEventDispatcher>
#include <QGuiApplication>
#include <QQmlContext>
#include <QQmlEngine>

#include "common_debug.h"
#include "CopyAppWorkflow_TraceAutogen.h"
#include "IConfigurationService.h"
#include "IMenuResource.h"
#include "IPathServices.h"
#include "QmlUtils.h"
#include "IResourceStoreFuture.h"
#include "com_hp_cdm_service_jobManagement_version_1_models_generated.h"
EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_spice_CopyAppWorkflow)
{
    dune::copy::spice::CopyAppWorkflow *instance = new dune::copy::spice::CopyAppWorkflow(instanceName);
    assert(instance != nullptr);
    return static_cast<dune::framework::component::IComponent *>(instance);
}

namespace dune { namespace copy { namespace spice {

using namespace dune::framework::component;
using namespace dune::spice::guiCore;
using dune::framework::storage::path::Paths;

CopyAppWorkflow::CopyAppWorkflow(const char *instanceName) : SpiceGuiApplicationCommon(instanceName)
{
    instanceName_ =  instanceName;
    CHECKPOINTC("%s/CopyAppWorkflow: constructed", instanceName);
}

void CopyAppWorkflow::start(QVariantMap initialProperties)
{
    SpiceGuiApplicationCommon::start(initialProperties);
    applicationRunning_ = true;

    auto resourceStore = applicationEngine_->getResourceStore();
    prioritySessionModel_ = resourceStore->createInstance(dune::spice::core::ResourceStoreTypes::Type::JOB_MANAGEMENT_1_PRIORITY_MODE_SESSION);
    auto priorityModeSessionModelData = static_cast<dune::spice::jobManagement_1::PriorityModeSessionModel *>(prioritySessionModel_->getData());
    priorityModeSessionModelData->setApplicationId("cedab422-33b3-4638-b6a1-604e54525215");
    priorityModeSessionModelData->setBehavior(dune::spice::jobManagement_1::priorityModeSession::Behavior::Behavior::blockNonPriorityJobs);

    IResourceStoreFuture *future = resourceStore->create("/cdm/jobManagement/v1/priorityModeSessions", prioritySessionModel_);

    connect(future, &IResourceStoreFuture::resolved, [this, priorityModeSessionModelData](IResourceStoreFuture *future) {
                    CHECKPOINTA("%s/CopyAppWorkflow: Entered into priority mode session!", instanceName_);

                    prioritySessionModel_ = future->get();
                    QString priorityModeSessionModelId = static_cast<dune::spice::jobManagement_1::PriorityModeSessionModel *>(prioritySessionModel_->getData())->getPriorityModeSessionId();

                    // If application is closed but priority mode session is still exists, then destroy the priority mode session.
                    if ( !applicationRunning_)
                    {
                        CHECKPOINTA("%s/CopyAppWorkflow Application is still running, destroying priority mode session!", instanceName_);
                        auto resourceStore = applicationEngine_->getResourceStore();
                        auto future = resourceStore->destroyResource(prioritySessionModel_);

                        connect(future, &IResourceStoreFuture::resolved, [this](IResourceStoreFuture *future) {
                            CHECKPOINTA("%s/CopyAppWorkflow Exited from priority mode session!", instanceName_);
                            prioritySessionModel_->deleteLater();
                            prioritySessionModel_ = nullptr;
                        });
                    }
                    else
                    {
                        if(contentItem_) // If contentItem_ is already created, then set the prioritySessionId property.
                        {
                            contentItem_->setProperty("prioritySessionId", priorityModeSessionModelId);
                        }
                        else{
                            connect(getSpiceQmlIncubator(), &SpiceQmlIncubator::incubationFinished, [=](bool sucess) {
                                CHECKPOINTA("%s/CopyAppWorkflow incubator finished slot called!", instanceName_);
                                if (sucess)
                                {
                                    contentItem_->setProperty("prioritySessionId", priorityModeSessionModelId);
                                }
                            });
                            
                        }
                    }
                    
                    CHECKPOINTA("%s/CopyAppWorkflow PriorityModeSession created successfully!", instanceName_);
    });

    connect(future, &IResourceStoreFuture::rejected, [this](IResourceStoreFuture *future) {
        CHECKPOINTA("%s/CopyAppWorkflow Failed to create priority mode session!", instanceName_);
    });
}

void CopyAppWorkflow::quit()
{
    if(prioritySessionModel_)
    {
        CHECKPOINTC("%s/CopyAppWorkflow Exiting from the priorityMode Session..", instanceName_);
        auto resourceStore = applicationEngine_->getResourceStore();
        auto future = resourceStore->destroyResource(prioritySessionModel_);

        connect(future, &IResourceStoreFuture::resolved, [this](IResourceStoreFuture *future) {
            CHECKPOINTC("%s/CopyAppWorkflow Exited from priority mode session!", instanceName_);
            prioritySessionModel_->deleteLater();
            prioritySessionModel_ = nullptr;
        });

        connect(future, &IResourceStoreFuture::rejected, [this](IResourceStoreFuture *future) {
            CHECKPOINTC("%s/CopyAppWorkflow Failed to exit from priority mode session!", instanceName_);
            prioritySessionModel_->deleteLater();
            prioritySessionModel_ = nullptr;
        });
    }
    SpiceGuiApplicationCommon::quit();
    applicationRunning_ = false; 
}

CopyAppWorkflow::~CopyAppWorkflow()
{
    if (copySettingsResource_)
    {
        copySettingsResource_->deleteLater();
    }

    if (copyModeSettingsResource_)
    {
        copyModeSettingsResource_->deleteLater();
    }
}

void  CopyAppWorkflow::initialize(WorkingMode mode, const dune::framework::component::SystemServices *services)
{
    DUNE_UNUSED(mode);
    services_ = services;
    //SpiceGuiApplicationCommon::initialize(mode, services);

    if (services_->configurationService_ != nullptr)
    {
        config_ = getConfiguration(services_->configurationService_);
    }
    CHECKPOINTC("%s/ CopyAppWorkflow: initialized", instanceName_);

}

void CopyAppWorkflow::connected(IComponentManager *componentManager, std::future<void> &asyncCompletion)
{
    
    // Call the base once there is a job app with rrc to register, until then we avoid the assert
    SpiceGuiApplicationCommon::connected(componentManager, asyncCompletion);
    fillInteractiveSummaryList();
    fillMoreOptionList();
    fillQuicksetIconList();
    copyPreviewInteractiveEnabled_ = config_->copyPreviewInteractiveEnabled;
    isCopyConfigSubscriptionRequired_ = config_->isCopyConfigSubscriptionRequired;
    isCopyPermissionsConfigurable_ = config_->isCopyPermissionsConfigurable;
    pathToResource_ = services_->pathServices_->getPathDirectory()->getPath(Paths::RESOURCE_DIRECTORY).c_str();
    if (pathToResource_.endsWith("/"))
    {
        pathToResource_.remove(pathToResource_.size() - 1, 1);
    }
    pathToResource_ = QString("%1/0x%2/").arg(pathToResource_).arg(getComponentFlavorUid(), 0, 16);
    copySettingsResource_ = IMenuResource::createResourceForCSF(std::move(config_->copySettings));
    copySettingsResource_->setEngine(applicationEngine_->getQQmlEngine());

    copySettingsResource_->moveToThread(nullptr);

    //Check if copy mode setting is defined in the configuration
    if(config_->copyModeSettings)
    {
        copyModeSettingsResource_ = IMenuResource::createResourceForCSF(std::move(config_->copyModeSettings));

        if(nullptr != copyModeSettingsResource_)
        {
            copyModeSettingsResource_->setEngine(applicationEngine_->getQQmlEngine());
            copyModeSettingsResource_->moveToThread(nullptr);
        }
    }

    QSemaphore waitForInit;

    QMetaObject::invokeMethod(QAbstractEventDispatcher::instance(qGuiApp->thread()),
                                [&] {
                                    copySettingsResource_->moveToThread(qGuiApp->thread());

                                    applicationEngine_->getQQmlEngine()->rootContext()->setContextProperty(
                                        "_copySettingsResource", copySettingsResource_);

                                    applicationEngine_->getQQmlEngine()->rootContext()->setContextProperty(
                                        "_copyInteractiveSummaryList", QVariant(interactiveSummaryList_));

                                    applicationEngine_->getQQmlEngine()->rootContext()->setContextProperty(
                                        "_copyQuicksetIconList", quicksetIconList_);
                                    
                                    applicationEngine_->getQQmlEngine()->rootContext()->setContextProperty(
                                        "_copySettingOptionListAvailability", QVariant(moreOptionSettingsList_));

                                    applicationEngine_->getQQmlEngine()->setObjectOwnership(copySettingsResource_,
                                                                                          QQmlEngine::CppOwnership);
                                    
                                    if(nullptr != copyModeSettingsResource_)
                                    {
                                        copyModeSettingsResource_->moveToThread(qGuiApp->thread());
                                        applicationEngine_->getQQmlEngine()->rootContext()->setContextProperty("_copyModeSettingsResource",
                                                                            copyModeSettingsResource_);
                                        applicationEngine_->getQQmlEngine()->setObjectOwnership(copyModeSettingsResource_,
                                                                    QQmlEngine::CppOwnership);
                                    }

                                    applicationEngine_->getQQmlEngine()->rootContext()->setContextProperty(
                                        "_copyPreviewInteractiveEnabled", QVariant(copyPreviewInteractiveEnabled_));

                                    applicationEngine_->getQQmlEngine()->rootContext()->setContextProperty(
                                        "_isCopyConfigSubscriptionRequired", QVariant(isCopyConfigSubscriptionRequired_));    

                                    applicationEngine_->getQQmlEngine()->rootContext()->setContextProperty(
                                        "_isCopyPermissionsConfigurable", QVariant(isCopyPermissionsConfigurable_));
                                    waitForInit.release();
                                },
                                Qt::QueuedConnection);
    waitForInit.acquire();
}

std::unique_ptr<CopyAppWorkflowListT> CopyAppWorkflow::getConfiguration(dune::framework::resources::IConfigurationService *configService) const
{
    assert(configService);
    auto rawConfig = configService->getConfiguration(GET_MODULE_UID(CopyAppWorkflow), instanceName_);
    if (rawConfig.data && (rawConfig.size > 0))
    {
        flatbuffers::Verifier verifier(rawConfig.data.get(), rawConfig.size);
        assert(VerifyCopyAppWorkflowListBuffer(verifier));
        return UnPackCopyAppWorkflowList(rawConfig.data.get());
    }
    return std::unique_ptr<CopyAppWorkflowListT>();

}

void CopyAppWorkflow::fillInteractiveSummaryList()
{
    if(config_->interactive->list.size() > 0)
    {
        auto listOfArray = config_->interactive->list;
        for(unsigned int i = 0; i < listOfArray.size(); i++){
            std::string str = listOfArray[i];
            interactiveSummaryList_.append(QString(str.c_str()));
        }
    }
}



void CopyAppWorkflow::fillMoreOptionList()
{    
    // At current iteration we take the list of setting as the simple mode from a .csf file.    
    // Possible improvement could it be a general feature list with all data relative
    // or a capabilities list loaded from initialization from CDM.
    // With current designed code, Best Option is take data from csf files to specific components.
    if(config_->listOfMoreOptionSettings.size() > 0)
    {
        auto listOfMoreOptionSettings = config_->listOfMoreOptionSettings;
        for(unsigned int i=0; i < listOfMoreOptionSettings.size(); i++){
            std::string str = listOfMoreOptionSettings[i];
            moreOptionSettingsList_.append(QString(str.c_str()));
        }
    }    
}

void CopyAppWorkflow::fillQuicksetIconList()
{
    if (!config_->quicksetList.empty())
    {
        for(unsigned int i=0; i < config_->quicksetList.size(); i++)
        {
            quicksetIconList_.insert(QString(config_->quicksetList[i]->uuid.c_str()),QVariant(config_->quicksetList[i]->icon.c_str()));
        }
    }
    else
    {
        CHECKPOINTB("%s/CopyAppWorkflow::fillQuicksetIconList field configuration_->quicksetList is empty()", getComponentInstanceName());
    }
}

// IComponent methods.
dune::framework::component::ComponentFlavorUid CopyAppWorkflow::getComponentFlavorUid() const
{
    return GET_MODULE_UID(CopyAppWorkflow);
}

}}}  // namespace dune::copy::spice
