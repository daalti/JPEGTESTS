/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobServiceStandard.cpp
 * @date   Wed, 08 May 2019 06:49:55 -0700
 * @brief  JobService specific class to CopyJobs
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////
#include "IJobManager.h"
#include "IJobQueue.h"
#include "JobServiceStandard.h"

#include <cassert>
#include <functional>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

#include "common_debug.h"

#include "JobServiceStandard_TraceAutogen.h"

#include "ConstraintsGroup.h"
#include "CopyJobDetailsProvider.h"
#include "CopyJobPromptController.h"
#include "CopyJobTicket.h"
#include "ErrorManager.h"
#include "FBUtils.h"
#include "IColorDirector.h"
#include "IConfigurationService.h"
#include "ICopyJobTicket.h"
#include "IIntentsManager.h"
#include "IJobManager.h"
#include "ILocale.h"
#include "ILocaleProvider.h"
#include "IMediaHandlingMgr.h"
#include "IMediaHandlingSettings.h"
#include "INvram.h"
#include "IPathServices.h"
#include "IPrintDevice.h"
#include "IPrintIntentsFactory.h"
#include "IRenderingRequirements.h"
#include "IResetManager.h"
#include "IScanDevice.h"
#include "IScannerMedia.h"
#include "ISecureFileErase.h"
#include "ISettings.h"
#include "IShortcuts.h"
#include "ISystemConversionHelper.h"
#include "ITicketAdapter.h"
#include "JobFrameworkBaseTypes.h"
#include "JobFrameworkTypes.h"
#include "JobFrameworkTypes_generated.h"
#include "JobServiceFactoryQuicksetConfig_generated.h"
#include "JobServiceStandardUwAdapter.h"
#include "JobTicketResourceHelper.h"
#include "OperationFailedException.h"
#include "ShortcutsHelper.h"
#include "StringIds.h"
#include "typeMappers.h"
#include "CopyTicketAdapter.h"
#include "IStatus.h"
#include "IPrint.h"
#include "ICapabilitiesFactory.h"
#include "Capabilities.h"


using ResourceServiceId = std::string;
using JobServiceId = dune::job::JobServiceId;
using ItemEasyBufferTable = dune::cdm::shortcut_1::ShortcutTable;
using ShortcutsHelper = dune::admin::shortcuts::ShortcutsHelper;
using dune::copy::Jobs::Copy::CopyJobTicketFbT;
using dune::framework::utils::FBUtils;
using FlatBufferDataObjectAdapterJobTicket = dune::framework::data::FlatBufferDataObjectAdapter<CopyJobTicketFbT>;
using SerializedDataBufferPtr = dune::framework::data::SerializedDataBufferPtr;
using SettingId = dune::print::engine::SettingId;
using ConversionResult = dune::framework::data::conversion::ConversionResult;
using namespace dune::job::cdm;
using IStatus                = dune::scan::scanningsystem::IStatus;
using StatusType             = dune::scan::scanningsystem::StatusType;
using IMediaPath             = dune::scan::scanningsystem::IMediaPath;
using MediaPresenceStatus    = dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus;
using IPrint                 = dune::print::engine::IPrint;
// Factory method

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_Jobs_Copy_JobServiceStandard)
{
    dune::copy::Jobs::Copy::JobServiceStandard *instance = new dune::copy::Jobs::Copy::JobServiceStandard(instanceName);
    assert(instance != nullptr);
    return static_cast<dune::framework::component::IComponent *>(instance);
}

/**
 * @brief Map const encapsulation to have values to force updated on ticket that have not default initial values
 * expected
 */
const std::unordered_map<dune::copy::Jobs::Copy::SettingsEnumForForceValue,
                         std::function<void(std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> jobTicketToBeForced,
                                            std::shared_ptr<dune::copy::Jobs::Copy::CopyJobIntentFbT> defaultValue)>>
    MAP_TO_FORCE_VALUE_FROM_DEFAULT_TICKET{
        {dune::copy::Jobs::Copy::SettingsEnumForForceValue::MEDIA_FAMILY,
         [](std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket>   jobTicketToBeForced,
            std::shared_ptr<dune::copy::Jobs::Copy::CopyJobIntentFbT> defaultValue) -> void {
             jobTicketToBeForced->getIntent()->setMediaFamily(defaultValue->mediaFamily);
         }},
        {dune::copy::Jobs::Copy::SettingsEnumForForceValue::AUTO_ROTATE,
         [](std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket>   jobTicketToBeForced,
            std::shared_ptr<dune::copy::Jobs::Copy::CopyJobIntentFbT> defaultValue) -> void {
             jobTicketToBeForced->getIntent()->setAutoRotate(defaultValue->autoRotate);
         }},
        {dune::copy::Jobs::Copy::SettingsEnumForForceValue::SCALE_TO_OUTPUT,
         [](std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket>   jobTicketToBeForced,
            std::shared_ptr<dune::copy::Jobs::Copy::CopyJobIntentFbT> defaultValue) -> void {
             jobTicketToBeForced->getIntent()->setScaleToOutput(defaultValue->scanJobIntent->scaleToOutput);
         }},
        {dune::copy::Jobs::Copy::SettingsEnumForForceValue::IMAGE_PREVIEW_CONFIGURATION,
         [](std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket>   jobTicketToBeForced,
            std::shared_ptr<dune::copy::Jobs::Copy::CopyJobIntentFbT> defaultValue) -> void {
             jobTicketToBeForced->getIntent()->setImagePreview(defaultValue->scanJobIntent->scanImagePreview);
         }}};

// namespace {

// } // anonymous namespace

namespace dune { namespace copy { namespace Jobs { namespace Copy {

// Constructor and destructor
JobServiceStandard::JobServiceStandard(const char *instanceName)
    : JobServiceFactory(JobServiceId::COPY, GET_MODULE_UID(JobServiceStandard), {JobType::COPY}),
      instanceName_{instanceName}
{
    CHECKPOINTC("%s/JobServiceStandard: constructed", getComponentInstanceName());
}

JobServiceStandard::~JobServiceStandard()
{
    if (uwAdapter_ != nullptr)
    {
        delete uwAdapter_;
    }
}

// IComponent methods.

dune::framework::component::ComponentFlavorUid JobServiceStandard::getComponentFlavorUid() const
{
    return GET_MODULE_UID(JobServiceStandard);
}

const char *JobServiceStandard::getComponentInstanceName() const
{
    return instanceName_;
}

void JobServiceStandard::initialize(WorkingMode mode, const dune::framework::component::SystemServices *services)
{
    DUNE_UNUSED(mode);
    CHECKPOINTC("%s/JobServiceStandard: initialized", getComponentInstanceName());

    if (nullptr == services)
    {
        CHECKPOINTA("%s/JobServiceStandard: initialize services_ value is null during initialize",
                    getComponentInstanceName());
        assert_msg(false, "ERROR:: services_ value is null during initialize");
    }
    else
    {
        setSystemServices(services);

        configuration_ = getConfiguration(services->configurationService_);
        if (nullptr == configuration_)
        {
            CHECKPOINTA("%s/JobServiceStandard: initialize configuration_ value is null during initialize",
                        getComponentInstanceName());
            assert_msg(false, "ERROR:: configuration_ value is null during initialize");
        }

        if (nullptr == services->threadPool_)
        {
            CHECKPOINTA("%s/JobServiceStandard: initialize services->threadPool_ value is null during initialize",
                        getComponentInstanceName());
            assert_msg(false, "ERROR:: services->threadPool_ value is null during initialize");
        }

        dune::framework::storage::path::IPathDirectory *pathDirectory = services->pathServices_->getPathDirectory();
        assert(pathDirectory);

        COPY_JOB_SERVICE_RESOURCE_FILE_DIR =
            pathDirectory->getPath(dune::framework::storage::path::Paths::RESOURCE_DIRECTORY);

        // Append id of component to path.
        std::stringstream stream;
        stream << std::hex << std::setw(6) << std::setfill('0') << getComponentFlavorUid();

        std::string ifaceId("0x");
        ifaceId.append(stream.str());

        COPY_JOB_SERVICE_RESOURCE_FILE_DIR.append(ifaceId).append("/");
    }
}

void *JobServiceStandard::getInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName)
{
    CHECKPOINTC("%s/JobServiceStandard: getInterface %" PRIu32 " from port %s", getComponentInstanceName(),
                interfaceUid, portName);

    DUNE_UNUSED(portName);

    void *interfacePtr = nullptr;
    if (interfaceUid == GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobService))
    {
        interfacePtr = static_cast<dune::copy::Jobs::Copy::ICopyJobService *>(this);
    }
    else if (interfaceUid == GET_INTERFACE_UID(dune::job::IJobTicketResourceHelper))
    {
        interfacePtr = static_cast<dune::job::IJobTicketResourceHelper *>(jobTicketResourceHelper_.get());
    }
    else
    {
        CHECKPOINTA("%s/JobServiceStandard: getInterface 0x%x is not provided by this instance",
                    getComponentInstanceName(), interfaceUid);
    }

    return interfacePtr;
}

void JobServiceStandard::setInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName,
                                      void *interfacePtr)
{
    if (interfacePtr != nullptr)
    {
        if (interfaceUid == GET_INTERFACE_UID(dune::job::IJobServiceManager))
        {
            dune::job::IJobServiceManager *jobServiceManagerPtr =
                static_cast<dune::job::IJobServiceManager *>(interfacePtr);
            setJobServiceManager(jobServiceManagerPtr);
            CHECKPOINTC("%s/JobServiceStandard: setInterface IJobServiceManager to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyPipeline))
        {
            copyPipeline_ = static_cast<dune::copy::Jobs::Copy::ICopyPipeline *>(interfacePtr);
            CHECKPOINTC("%s/JobServiceStandard: setInterface ICopyPipeline to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::job::IJobManager))
        {
            dune::job::IJobManager *jobManagerPtr = static_cast<dune::job::IJobManager *>(interfacePtr);
            setJobManager(jobManagerPtr);
            CHECKPOINTC("%s/JobServiceStandard: setInterface IJobManager to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::job::IResourceManagerClient))
        {
            auto *resourceManagerClient = static_cast<dune::job::IResourceManagerClient *>(interfacePtr);
            setResourceManager(resourceManagerClient);
            servicePackage_.resourceManager = resourceManagerClient;
            CHECKPOINTC("%s/JobServiceStandard: setInterface IResourceManagerClient to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::job::IJobQueue))
        {
            auto jobQueuePtr = static_cast<dune::job::IJobQueue *>(interfacePtr);
            servicePackage_.jobQueue = jobQueuePtr;
            CHECKPOINTC("%s/JobServiceStandard: setInterface IJobQueue to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::imaging::IColorAccessControl ))
        {
            CHECKPOINTB("JobServiceStandard::setInterface: Received IColorAccessControl interface");
            colorAccessControl_ = static_cast<dune::imaging::IColorAccessControl  *>(interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::job::IJobDetailsManager))
        {
            jobDetailsManager_ = static_cast<dune::job::IJobDetailsManager *>(interfacePtr);
            CHECKPOINTC("%s/JobServiceStandard: setInterface IJobDetailsManager to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::job::cdm::IJobManagerAlertProvider))
        {
            jobManagerAlertProvider_ = static_cast<dune::job::cdm::IJobManagerAlertProvider *>(interfacePtr);
            assert(jobManagerAlertProvider_);
            CHECKPOINTC("%s/JobServiceStandard: setInterface IJobManagerAlertProvider to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::job::IJobTicketResourceManager))
        {
            auto *jobTicketResourceManager = static_cast<dune::job::IJobTicketResourceManager *>(interfacePtr);
            setJobTicketResourceManager(jobTicketResourceManager);
            CHECKPOINTC("%s/JobServiceStandard: setInterface IJobTicketResourceManager to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::print::engine::IPrintIntentsFactory))
        {
            auto *printIntentsFactoryPtr = static_cast<dune::print::engine::IPrintIntentsFactory *>(interfacePtr);
            servicePackage_.printIntentsFactory = printIntentsFactoryPtr;
            CHECKPOINTC("%s/JobServiceStandard: setInterface IPrintIntentsFactory to port %s with addr %p",
                        instanceName_, portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::print::engine::IPrint))
        {
            auto *printEnginePtr = static_cast<dune::print::engine::IPrint *>(interfacePtr);
            servicePackage_.printEngine = printEnginePtr;
            CHECKPOINTC("%s/JobServiceStandard: setInterface IPrint to port %s with addr %p",
                instanceName_, portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::print::engine::ICapabilitiesFactory))
        {
            servicePackage_.engineCapabilitiesFactory = static_cast<dune::print::engine::ICapabilitiesFactory *>(interfacePtr);
            CHECKPOINTC("%s/JobServiceStandard: setInterface ICapabilitiesFactory to port %s with addr %p",
                        instanceName_, portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::scan::Resources::IScanDevice))
        {
            assert(servicePackage_.scanDeviceService == nullptr);
            servicePackage_.scanDeviceService = static_cast<dune::scan::Resources::IScanDevice *>(interfacePtr);
            static_cast<dune::scan::Resources::IScanDevice *>(interfacePtr)->getResourceService();
            CHECKPOINTC("%s/JobServiceStandard: setInterface IScanDevice to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::imaging::color::IColorDirector))
        {
            servicePackage_.colorDirector = static_cast<dune::imaging::color::IColorDirector *>(interfacePtr);
            CHECKPOINTC("%s/JobServiceStandard: setInterface IColorDirector to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints))
        {
            jobConstraintsHelper_ = static_cast<dune::copy::Jobs::Copy::IJobConstraints *>(interfacePtr);
            assert(jobConstraintsHelper_);
            CHECKPOINTC("%s/JobServiceStandard: setInterface IJobConstraints to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules))
        {
            copyDynamicConstraintsHelper_ =
                static_cast<dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules *>(interfacePtr);
            assert(copyDynamicConstraintsHelper_);
            CHECKPOINTC("%s/JobServiceStandard: setInterface ICopyJobDynamicConstraintRules to port %s with addr %p",
                        instanceName_, portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::job::IResourceService))
        {
            auto *resourceServicePtr = static_cast<dune::job::IResourceService *>(interfacePtr);

            if (strcmp(portName, "MarkingFilter") == 0)
            {
                assert(servicePackage_.markingFilterService == nullptr);
                servicePackage_.markingFilterService =
                    dynamic_cast<dune::imaging::Resources::IMarkingFilter *>(resourceServicePtr);
                CHECKPOINTC(
                    "%s/JobServiceStandard: setInterface MarkingFilter IResourceService to port %s with addr %p",
                    instanceName_, portName, interfacePtr);
            }
            else if (strcmp(portName, "ImageRetriever") == 0)
            {
                assert(servicePackage_.imageRetrieverService == nullptr);
                servicePackage_.imageRetrieverService = resourceServicePtr;
                CHECKPOINTC(
                    "%s/JobServiceStandard: setInterface ImageRetriver IResourceService to port %s with addr %p",
                    instanceName_, portName, interfacePtr);
            }
            else if (strcmp(portName, "ImageProcessor") == 0)
            {
                assert(servicePackage_.imageProcessor == nullptr);
                servicePackage_.imageProcessor =
                    dynamic_cast<dune::imaging::Resources::IImageProcessor *>(resourceServicePtr);
                CHECKPOINTC("%s/JobServiceStandard: setInterface IImageProcessor to port %s with addr %p",
                            instanceName_, portName, interfacePtr);
            }
            else if (strcmp(portName, "LayoutFilter") == 0)
            {
                assert(servicePackage_.layoutFilterService == nullptr);
                servicePackage_.layoutFilterService =
                    dynamic_cast<dune::imaging::Resources::ILayoutFilter *>(resourceServicePtr);
                CHECKPOINTC("%s/JobServiceStandard: setInterface ILayoutFilter to port %s with addr %p", instanceName_,
                            portName, interfacePtr);
            }
            else if (strcmp(portName, "RtpFilterService") == 0)
            {
                assert(servicePackage_.rtpFilterService == nullptr);
                servicePackage_.rtpFilterService = resourceServicePtr;
                CHECKPOINTC(
                    "%s/JobServiceStandard: setInterface RtpFilterService IResourceService to port %s with addr %p",
                    instanceName_, portName, interfacePtr);
            }
            else
            {
                CHECKPOINTC("%s/JobServiceStandard: setInterface portName is not implemented, port %s with addr %p",
                            instanceName_, portName, interfacePtr);
            }
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::imaging::Resources::IImagePersister))
        {
            assert(servicePackage_.imagePersister == nullptr);
            servicePackage_.imagePersister = static_cast<dune::imaging::Resources::IImagePersister *>(interfacePtr);
            CHECKPOINTC("%s/JobServiceStandard: setInterface IImagePersister to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::imaging::Resources::IPageAssembler))
        {
            assert(servicePackage_.pageAssembler == nullptr);
            servicePackage_.pageAssembler = static_cast<dune::imaging::Resources::IPageAssembler *>(interfacePtr);
            CHECKPOINTC("%s/JobServiceStandard: setInterface IPageAssembler to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::framework::data::IDataStore))
        {
            auto dataStore = static_cast<dune::framework::data::IDataStore *>(interfacePtr);
            setDataStore(dataStore);
            CHECKPOINTC("%s/JobServiceStandard: setInterface IDataStore to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::print::Resources::IPrintDevice))
        {
            assert(servicePackage_.printDevice == nullptr);
            servicePackage_.printDevice = static_cast<dune::print::Resources::IPrintDevice *>(interfacePtr);
            CHECKPOINTA("%s/JobServiceStandard: Copy pipeline using print device memory client",
                        getComponentInstanceName());
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::print::engine::IMedia))
        {
            CHECKPOINTA("%s/JobServiceStandard: setInterface IMedia interfaceUid %" PRIu32 " to port %s with addr %p",
                        getComponentInstanceName(), interfaceUid, portName, interfacePtr);
            servicePackage_.mediaInterface = static_cast<dune::print::engine::IMedia *>(interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingSettings))
        {
            CHECKPOINTC("%s/JobServiceStandard: setInterface IMediaHandlingSettings interfaceUid %" PRIu32
                        " to port %s with addr %p",
                        getComponentInstanceName(), interfaceUid, portName, interfacePtr);
            servicePackage_.mediaHandlingSettings =
                static_cast<dune::print::mediaHandlingAssets::IMediaHandlingSettings *>(interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::print::mediaHandlingAssets::IMediaHandlingMgr))
        {
            CHECKPOINTC("%s/JobServiceStandard: setInterface IMediaHandlingSettings interfaceUid %" PRIu32
                        " to port %s with addr %p",
                        getComponentInstanceName(), interfaceUid, portName, interfacePtr);
            servicePackage_.mediaHandlingMgr =
                static_cast<dune::print::mediaHandlingAssets::IMediaHandlingMgr *>(interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::print::engine::IMediaInfo))
        {
            CHECKPOINTC("%s/JobServiceStandard: setInterface IMediaInfo interfaceUid %" PRIu32
                        " to port %s with addr %p",
                        getComponentInstanceName(), interfaceUid, portName, interfacePtr);
            servicePackage_.mediaInfo = static_cast<dune::print::engine::IMediaInfo *>(interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::admin::shortcuts::IShortcuts))
        {
            auto shortcut = static_cast<dune::admin::shortcuts::IShortcuts *>(interfacePtr);
            setIShortcuts(shortcut);
            CHECKPOINTC("%s/JobServiceStandard: setInterface IShortcuts to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::scan::Jobs::Scan::IScanPipeline))
        {
            auto scanPipeline = static_cast<dune::scan::Jobs::Scan::IScanPipeline *>(interfacePtr);
            scanPipeline_ = scanPipeline;
            CHECKPOINTC("%s/JobServiceStandard: setInterface IScanPipeline to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::scan::scanningsystem::IMedia))
        {
            CHECKPOINTA("%s/JobServiceStandard: setInterface scanningsystem::IMedia interfaceUid %" PRIu32
                        " to port %s with addr %p",
                        getComponentInstanceName(), interfaceUid, portName, interfacePtr);
            scanMedia_ = static_cast<dune::scan::scanningsystem::IMedia *>(interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::scan::scanningsystem::IScannerCapabilities))
        {
            CHECKPOINTA("%s/JobServiceStandard: setInterface scanningsystem::IScannerCapabilities interfaceUid %" PRIu32
                        " to port %s with addr %p",
                        getComponentInstanceName(), interfaceUid, portName, interfacePtr);
            scanCapabilities_ = static_cast<dune::scan::scanningsystem::IScannerCapabilities *>(interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::print::engine::helpers::IRenderingRequirements))
        {
            servicePackage_.renderingRequirements =
                static_cast<dune::print::engine::helpers::IRenderingRequirements *>(interfacePtr);
            CHECKPOINTB("%s/JobServiceStandard: setInterface IRenderingRequirements to port %s with addr %p",
                        instanceName_, portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::imaging::asset::IMediaAttributes))
        {
            servicePackage_.mediaAttributes = static_cast<dune::imaging::asset::IMediaAttributes *>(interfacePtr);
            CHECKPOINTB("%s/JobServiceStandard: setInterface IMediaAttributes to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::framework::storage::INvram))
        {
            Nvram_ = static_cast<dune::framework::storage::INvram *>(interfacePtr);
            CHECKPOINTB("JobServiceStandard: setInterface INvram");
        }
        else if (interfaceUid == GET_INTERFACE_UID(ILocaleProvider))
        {
            localization_ = static_cast<ILocaleProvider *>(interfacePtr);
            CHECKPOINTB("%s/JobServiceStandard: setInterface ILocaleProvider to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::print::engine::ISettings))
        {
            interfaceISettings_ = static_cast<dune::print::engine::ISettings *>(interfacePtr);
            CHECKPOINTC("%s/JobServiceStandard: setInterface ISettings to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter))
        {
            copyAdapter_ = static_cast<dune::copy::cdm::ICopyAdapter *>(interfacePtr);
            CHECKPOINTB("%s/JobServiceStandard: setInterface ICopyAdapter to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::job::IIntentsManager))
        {
            intentsManager_ = static_cast<dune::job::IIntentsManager *>(interfacePtr);
            CHECKPOINTB("%s/JobServiceStandard: setInterface IIntentsManager to port %s with addr %p", instanceName_,
                        portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::framework::data::backup::IExportImport))
        {
            CHECKPOINTA("%s/JobServiceStandard: setInterface IExportImport interfaceUid %" PRIu32
                        " to port %s with addr %p",
                        getComponentInstanceName(), interfaceUid, portName, interfacePtr);
            exportImportManager_ = static_cast<dune::framework::data::backup::IExportImport *>(interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::framework::storage::ISecureFileErase))
        {
            auto *fileErase = static_cast<dune::framework::storage::ISecureFileErase *>(interfacePtr);
            setFileErase(fileErase);
            CHECKPOINTC("%s/JobServiceStandard: setInterface ISecureFileErase to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }        
        else if (interfaceUid == GET_INTERFACE_UID(dune::admin::deviceinfo::IDeviceInfo))
        {
            auto *deviceInfoPtr = static_cast<dune::admin::deviceinfo::IDeviceInfo *>(interfacePtr);
            servicePackage_.deviceInfo = deviceInfoPtr;
            CHECKPOINTB("%s/JobServiceStandard: setInterface IDeviceInfo to port %s with addr %p",
                        instanceName_, portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::io::net::core::INetworkManager))
        {
            auto *networkManagerPtr = static_cast<dune::io::net::core::INetworkManager *>(interfacePtr);
            servicePackage_.networkManager = networkManagerPtr;
            CHECKPOINTB("%s/JobServiceStandard: setInterface INetworkManager to port %s with addr %p",
                        instanceName_, portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(ISystemConversionHelper))
        {
            systemConversionHelper_ = static_cast<ISystemConversionHelper *>(interfacePtr);
            CHECKPOINTC("%s/JobServiceStandard: setInterface ISystemConversionHelper to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else if( interfaceUid == GET_INTERFACE_UID(ICopyTicketConverter))
        {
            copyTicketConverter_ = static_cast<ICopyTicketConverter *>(interfacePtr);
            CHECKPOINTC("%s/JobServiceStandard: setInterface ICopyTicketConverter to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else if(interfaceUid == GET_INTERFACE_UID(dune::print::engine::IConnector))
        {
            itsIConnector_ = static_cast<dune::print::engine::IConnector *>(interfacePtr);
            CHECKPOINTC("%s/JobServiceStandard: setInterface IConnector to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::scan::scanningsystem::IStatus))
        {
            CHECKPOINTA("%s/JobServiceStandard: setInterface scanningsystem::IStatus interfaceUid %" PRIu32
                        " to port %s with addr %p",
                        getComponentInstanceName(), interfaceUid, portName, interfacePtr);
            scannerStatus_ = static_cast<dune::scan::scanningsystem::IStatus *>(interfacePtr);
        }  
        else
        {
            CHECKPOINTA("%s/JobServiceStandard: setInterface not handled for interfaceUid %" PRIu32
                        " to port %s with addr %p",
                        getComponentInstanceName(), interfaceUid, portName, interfacePtr);
        }
    }
    else
    {
        CHECKPOINTA("%s/JobServiceStandard: setInterface 0x%" PRIx32 " to port %s with addr %p",
                    getComponentInstanceName(), interfaceUid, portName, interfacePtr);
    }
}

void JobServiceStandard::connected(dune::framework::component::IComponentManager *componentManager,
                                   std::future<void>                             &asyncCompletion)
{
    DUNE_UNUSED(componentManager);
    DUNE_UNUSED(asyncCompletion);

    // Initialize the underware adapter.
    uwAdapter_ =
        new JobServiceStandardUwAdapter(getSystemServices()->interpreterEnvironment_, getComponentInstanceName(), this);

    assert(getSystemServices() != nullptr);
    assert(getDataStore() != nullptr);
    assert(getJobServiceManager() != nullptr);
    assert(getJobManager() != nullptr);
    assert(getJobTicketResourceManager() != nullptr);
    assert(getResourceManager() != nullptr);
    assert(getFileErase() != nullptr);

    // Assert for the minimum viable resources services, all other resource services could be optional based on product
    // These optional resource services should be checked for availability in the pipeline builder
    assert(servicePackage_.scanDeviceService != nullptr);
    assert(servicePackage_.printDevice != nullptr);

    if (jobDetailsManager_ != nullptr)
    {
        jobDetailsManager_->registerProvider(
            dune::job::JobType::COPY,
            std::make_shared<CopyJobDetailsProvider>(this, getJobTicketResourceManager(), interfaceISettings_,
                                                     scanPipeline_, getSystemServices()->dateTime_));
    }
    else
    {
        CHECKPOINTA("%s/JobServiceStandard: JobDetailsManager is empty!", instanceName_);
    }

    jobTicketResourceHelper_ = std::make_shared<JobTicketResourceHelper>(this);
    jobTicketResourceHelper_->registerHelper(getJobTicketResourceManager());

    // Set the JobConstraints Helper of the ResourceHelper to create a Ticket Adapter with it
    assert(jobConstraintsHelper_ != nullptr);
    jobTicketResourceHelper_->setCopyJobConstraintsHelper(jobConstraintsHelper_);
    // Set the DynamicConstraints Helper of the ResourceHelper to create a Ticket Adapter with it
    assert(copyDynamicConstraintsHelper_ != nullptr);
    jobTicketResourceHelper_->setCopyDynamicConstraintsHelper(copyDynamicConstraintsHelper_);

    if (configuration_ != nullptr)
    {
        jobTicketResourceHelper_->staticConstrainsAreCached_ = configuration_->staticConstrainsAreCached;
        jobTicketResourceHelper_->validateTicketOnSerialization_ = configuration_->validateTicketsOnInitialization;
    }

    // Set the CopyAdapter(CopyConfiguration) of the ResourceHelper to create a Ticket Adapter with it
    assert(copyAdapter_ != nullptr);
    jobTicketResourceHelper_->setCopyConfigurationHelper(copyAdapter_);

    assert(localization_ != nullptr);
    jobTicketResourceHelper_->setLocaleProvider(localization_);

    assert(configuration_ != nullptr);
    if (configuration_ != nullptr)
    {
        /**
         * Read from conf file to find out if product has shared paper path.
         * When scan and print share the same paper path, copy job doesn't support
         * scan and print simultaneously. This configuration is used to make sure
         * copy job pipeline starts from the right Stage.
         *
         */
        hasSharedPaperPath_ = configuration_->hasSharedPaperPath;

        /**
         * Read from conf file to find out preprint configuration mode.
         * Copy job pipeline will configure in a different way by this value.
         */
        prePrintConfiguration_ = configuration_->prePrintConfiguration;

        /**
         * Read from conf file to find out if this product uses basic copy pipeline.
         * Copy job pipeline will configure in a different way by this value.
         */
        copyBasicPipeline_ = configuration_->copyBasicPipeline;

        multiPageSupportedFromFlatbed_ = configuration_->multiPageSupportedFromFlatbed;
        /**
         * Read from conf file to get max length values
         * These values will be used in pipeline to ensure scan Y-Extents are within allowed maximum
         */
        if (configuration_->scanPipelineCfg != nullptr)
        {
            maxLengthConfig_.scanMaxCm = configuration_->scanPipelineCfg->maxSupportedSizes->scanMaxCm;
            maxLengthConfig_.jpegMaxLines = configuration_->scanPipelineCfg->maxSupportedSizes->jpegMaxLines;
            maxLengthConfig_.tiffMaxMb = configuration_->scanPipelineCfg->maxSupportedSizes->tiffMaxMb;
            maxLengthConfig_.pdfMaxCm = configuration_->scanPipelineCfg->maxSupportedSizes->pdfMaxCm;
            maxLengthConfig_.pdfaMaxCm = configuration_->scanPipelineCfg->maxSupportedSizes->pdfaMaxCm;
            maxLengthConfig_.longPlotMaxCm = configuration_->scanPipelineCfg->maxSupportedSizes->longPlotMaxCm;
        }

        thresholdOverride_ = configuration_->thresholdOverride;
        renderIntent_ = configuration_->renderIntent;

        if (configuration_->validateTicketsOnInitialization)
        {
            validateCurrentTickets();
        }
    }
    else
    {
        CHECKPOINTA("ERROR: JobServiceStandard: INVALID CONFIGURATION! Copy not properly setup!");
    }

    assert(getIShortcuts() != nullptr);
    if (getIShortcuts() != nullptr)
    {
        if (configuration_ == nullptr || configuration_->quickSetSupported == true)
        {
            getIShortcuts()->registerJobService(dune::cdm::shortcut_1::Source::scan,
                                                dune::cdm::shortcut_1::Destination::print,
                                                dune::cdm::shortcut_1::JobType::copy, this);
        }

        // TODO: check if it is prestine boot.
        registerShortcuts();
        registerJobServiceState();
    }
    else
    {
        CHECKPOINTA("ERROR: JobServiceStandard: INVALID SHORTCUTS INTERFACE! Not able to register factory shortcuts!");
    }

    if (exportImportManager_ != nullptr)
    {
        subscriptionHandlerExportImport_ =
            exportImportManager_->subscribeParticipant(OperationType::EXPORT_IMPORT, Category::CopySettings, contentId_,
                                                       static_cast<IExportImport::IParticipant *>(this));
        subscriptionHandlerBackupRestore_ =
            exportImportManager_->subscribeParticipant(OperationType::BACKUP_RESTORE, Category::CopySettings,
                                                       contentId_, static_cast<IExportImport::IParticipant *>(this));
    }

    baseConnected();
    if(scanPipeline_ && prePrintConfiguration_ == dune::copy::Jobs::Copy::ProductType::HOME_PRO && !hasSharedPaperPath_)
    {
        scanMediaSizeSubscriptionId_ =  scanPipeline_->getScanMediaSize().getScanMediaSizeEvent().addSubscription(
            EVENT_MAKE_MEMBER_DELEGATE(JobServiceStandard::handleScanMediaSizeEvent, this));
    }
    if (servicePackage_.mediaInfo != nullptr)
    {
        CHECKPOINTB("%s/servicePackage_ is not null", getComponentInstanceName());
        mediaInfoExt_ = servicePackage_.mediaInfo->getPageBasedExtension();
    }
    if (mediaInfoExt_ != nullptr)
    {
        mediaInfoExt_->getMediaPropertyChangedEvent().addSubscription(
            EVENT_MAKE_MEMBER_DELEGATE(JobServiceStandard::onMediaPropertyChangedEvent, this));
        CHECKPOINTB("%s/JobServiceStandard: MediaPropertyChangedEvent subscription added", getComponentInstanceName());
    }
    // Check if we need to convert data this boot
    if (systemConversionHelper_ != nullptr) {

        auto migrateData = systemConversionHelper_->mustConvertDataThisBoot();
        CHECKPOINTB("CopyJobServiceStandard::connected: migrateData %d", migrateData);
        if (migrateData)
        {
            auto migrationResult = checkAndPerformMigration();
            CHECKPOINTB("CopyJobServiceStandard::connected: migrationResult = %d", migrationResult.first);
            if (migrationResult.first == ConversionResult::SUCCESS)
            {
                asyncCompletion = getSystemServices()->threadPool_->submitTask(
                    &JobServiceStandard::WaitforMedaiEventAndValidate, this, migrationResult.second);
            }
        }
    }
    if(servicePackage_.engineCapabilitiesFactory != nullptr)
    {
        std::shared_ptr<dune::print::engine::Capabilities> capabilities = servicePackage_.engineCapabilitiesFactory->getCapabilities();        
        auto result = capabilities->getEngineAttributeValue(dune::print::engine::EngineAttributeFieldType::PRE_RUN_SUPPORTED, isPreRunSupported_);
        CHECKPOINTB("%s/JobServiceStandard: isPreRunSupported_: %d", getComponentInstanceName(), isPreRunSupported_);
    }
    if(isPreRunSupported_ && scannerStatus_ != nullptr)
    {
        scannerStatus_->getStatusChangeEvent().addSubscription(EVENT_MAKE_MEMBER_DELEGATE(JobServiceStandard::onScannerStatusChangedEvent, this));
        CHECKPOINTB("%s/JobServiceStandard: StatusChangeEvent subscription added", getComponentInstanceName());
    }
    if(isPreRunSupported_ && scanMedia_ != nullptr)
    {
        auto inputList = scanMedia_->getInputs();
        CHECKPOINTB("%s/JobServiceStandard: Number of inputs in scannerMediaInterface: %d", getComponentInstanceName(), (uint)inputList.size());
        for(auto inputdev : inputList)
        {
            std::string id = inputdev->getId();
            if (id == "ADF")
            {
                inputdev->getMediaPresenceStatusChangeEvent().addSubscription(EVENT_MAKE_MEMBER_DELEGATE_WITH_EMITTER(JobServiceStandard::onScannerMediaPresenceChange, this));
            }
        }
        CHECKPOINTB("%s/JobServiceStandard: MediaPresenceStatusChangeEvent subscription added", getComponentInstanceName());
    }

    CHECKPOINTC("%s/JobServiceStandard: connected", getComponentInstanceName());
}



void JobServiceStandard::WaitforMedaiEventAndValidate(std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> jobTicketToBeSaved)
{
    CHECKPOINTB("%s/JobServiceStandard::WaitforMedaiEventAndValidate: Entry", getComponentInstanceName());
    
    if (itsIConnector_ != nullptr)
    {
        std::unique_lock<std::mutex> lock(hwCapabilitiesMutex_);
        
        // Check if hardware capabilities are already available under lock protection
        dune::print::engine::IConnector::ConnectorStatus currentStatus;
        itsIConnector_->getConnectorStatus(currentStatus);
        
        if (currentStatus.areHwCapabilitiesAvailable())
        {
            CHECKPOINTB("%s/JobServiceStandard::WaitforMedaiEventAndValidate: Hardware capabilities already available", getComponentInstanceName());
            lock.unlock(); // Release lock before calling saveDefaultJobTicket
            if (jobTicketToBeSaved != nullptr)
            {
                saveDefaultJobTicket(jobTicketToBeSaved, TicketUpdationMode::internal);
            }
        }
        else
        {
            CHECKPOINTB("%s/JobServiceStandard::WaitforMedaiEventAndValidate: Waiting for hardware capabilities", getComponentInstanceName());
            
            // Subscribe to connector status events to wait for hardware capabilities
            connectorStatusEventHandler_ = itsIConnector_->getConnectorStatusEvent().addSubscriptionEx(
                EVENT_MAKE_MEMBER_DELEGATE_WITH_EMITTER(JobServiceStandard::onEngineConnectionChange, this));
            
            // Wait for the condition variable to be notified when capabilities are available
            hwCapabilitiesCondition_.wait(lock, [this]() {
                if (itsIConnector_ != nullptr)
                {
                    dune::print::engine::IConnector::ConnectorStatus status;
                    itsIConnector_->getConnectorStatus(status);
                    return status.areHwCapabilitiesAvailable();
                }
                return false;
            });
            
            lock.unlock(); // Release lock before calling saveDefaultJobTicket
            CHECKPOINTB("%s/JobServiceStandard::WaitforMedaiEventAndValidate: Hardware capabilities now available, validating ticket", getComponentInstanceName());
            if (jobTicketToBeSaved != nullptr)
            {
                CHECKPOINTA("%s/JobServiceStandard::WaitforMedaiEventAndValidate: Saving job ticket after capabilities are available", getComponentInstanceName());
                saveDefaultJobTicket(jobTicketToBeSaved, TicketUpdationMode::internal);
            }
        }
    }
    
    CHECKPOINTB("%s/JobServiceStandard::WaitforMedaiEventAndValidate: Exit", getComponentInstanceName());
}

void JobServiceStandard::onEngineConnectionChange( dune::print::engine::IConnector * connector, const  dune::print::engine::IConnector::ConnectorStatus & status)
{
    CHECKPOINTB("%s/JobServiceStandard::onEngineConnectionChange: Entry", getComponentInstanceName());
    
    if (status.areHwCapabilitiesAvailable())
    {
        CHECKPOINTB("%s/JobServiceStandard::onEngineConnectionChange: Hardware capabilities are now available", getComponentInstanceName());
        
        // Notify the waiting thread that hardware capabilities are available
        {
            std::lock_guard<std::mutex> lock(hwCapabilitiesMutex_);
            hwCapabilitiesCondition_.notify_all();
        }
        
        // Unsubscribe from further events as we no longer need them
        // if (connectorStatusEventHandler_ != nullptr)
        // {
        //     connectorStatusEventHandler_->unsubscribe();
        //     connectorStatusEventHandler_ = nullptr;
        // }
    }
    
    CHECKPOINTB("%s/JobServiceStandard::onEngineConnectionChange: Exit", getComponentInstanceName());
} 

void JobServiceStandard::onScannerMediaPresenceChange(IMediaPath* source, MediaPresenceStatus newState)
{    
    if (isPreRunSupported_ && servicePackage_.printEngine != nullptr && newState == MediaPresenceStatus::LOADED)
    {
        CHECKPOINTB("JobServiceStandard::onScannerMediaPresenceChange: MediaPresenceStatus::LOADED");
        servicePackage_.printEngine->earlyWarmUp();
    }
}

void JobServiceStandard::onScannerStatusChangedEvent(IStatus* scannerStatusInterface)
{
    if (isPreRunSupported_ && servicePackage_.printEngine != nullptr)
    {
        StatusType statusType = StatusType::NotUpdated;
        bool active = 0;
        uint32_t code = 0;
        std::string codeString = "";

        scannerStatusInterface->getScannerStatus(statusType, active, code, codeString);
        if(StatusType::FlatCoverOpen == statusType && active)
        {
            CHECKPOINTB("JobServiceStandard::onScannerStatusChangedEvent: StatusType:FlatCoverOpen Active(%d)", active);
            servicePackage_.printEngine->earlyWarmUp();
        }
    }
}

void JobServiceStandard::onMediaPropertyChangedEvent(const MediaPropertyChangedEventArgs &eventArgs)
{
    CHECKPOINTB("%s/JobServiceStandard::onMediaPropertyChangedEvent: Entry", getComponentInstanceName());
    if (eventArgs.getMediaPropertyId() == dune::print::engine::pageBased::MediaPropertyId::VisibilityMode)
    {
        CHECKPOINTB("JobServiceStandard::Visibility mode changed for MediaType %d",
                    static_cast<int>(eventArgs.getMediaId().getType()));
        bool      mediaTypeVisibleEnabled = false;
        APIResult result = eventArgs.getMediaPropertyValue().getValue<bool>(mediaTypeVisibleEnabled);
        if (mediaTypeVisibleEnabled == true || result != APIResult::OK)
        {
            CHECKPOINTB(
                "JobServiceStandard(COPY)::onMediaPropertyChangedEvent: Visibility mode enabled for MediaType %d "
                "Exiting handler",
                static_cast<int>(eventArgs.getMediaId().getType()));
            return;
        }
        auto currentMediaType = eventArgs.getMediaId().getType();
        auto ticketSave = getDefaultJobTicket();
        auto MediaIdType = ticketSave->getIntent()->getOutputMediaIdType();
        CHECKPOINTB("JobServiceStandard:: Current Selected MediaType is %d", static_cast<int>(MediaIdType));
        if (MediaIdType == currentMediaType)
        {
            CHECKPOINTB(
                "JobServiceStandard::onMediaPropertyChangedEvent: Received MediaIdType is same as current media type "
                "hence resetting to Media type to PLAIN");
            ticketSave->getIntent()->setOutputMediaIdType(MediaIdType::STATIONERY);
            bool retval = saveDefaultJobTicket(ticketSave, TicketUpdationMode::internal);
            CHECKPOINTB(
                "JobServiceStandard::onMediaPropertyChangedEvent: Default Job Ticket saved with new media type with "
                "Returnvalue = %d",
                retval);
        }
        else
        {
            CHECKPOINTB(
                "JobServiceStandard::onMediaPropertyChangedEvent: Received MediaIdType is different from current media "
                "type hence no action");
        }

        // update quicksets
        dune::admin::shortcuts::shortcutFilter_t filter;
        filter.src = dune::cdm::shortcut_1::Source::scan;
        filter.dest = dune::cdm::shortcut_1::Destination::print;
        filter.origin = dune::cdm::shortcut_1::Origin::device;
        filter.type = dune::cdm::shortcut_1::Type::singleJob;
        filter.factory = dune::cdm::glossary_1::FeatureEnabled::false_;
        auto shortcutsData = getIShortcuts()->getShortcuts(true, filter);  // with pinValidateNotReq

        if (shortcutsData != nullptr)
        {
            CHECKPOINTC(
                "JobServiceStandard::onMediaPropertyChangedEvent: Number of Shortcuts to check if need to be updated = "
                "%d.",
                static_cast<int>(shortcutsData->collection().size()));

            for (auto &shortcut : shortcutsData->collection().getMutable())
            {
                for (auto link : shortcut.links.getMutable())
                {
                    // Trim current ticket removing /cdm/jobTicket/v1/tickets/ reference
                    auto        ticketReference = link.href.getMutable();
                    std::size_t positionDivider = ticketReference.find_last_of("/\\");
                    auto        ticketId = ticketReference.substr(positionDivider + 1);
                    CHECKPOINTC("JobServiceStandard::onMediaPropertyChangedEvent: id to validate: %s",
                                ticketId.c_str());

                    // Load ticket to cache if needed
                    bool persistentTicket;
                    auto jobTicket =
                        getJobTicketResourceManager()->loadJobTicketIntoCacheIfNeeded(ticketId, persistentTicket);
                    if (jobTicket == nullptr)
                    {
                        CHECKPOINTB(
                            "JobServiceStandard::onMediaPropertyChangedEvent: job ticket %s not found in cache and "
                            "fail to add it cache",
                            ticketId.c_str());
                        continue;
                    }

                    auto ticket = std::dynamic_pointer_cast<dune::copy::Jobs::Copy::ICopyJobTicket>(jobTicket);

                    // First check if ticket need to do any forced change
                    auto quicksetOutputMediaIdType = ticket->getIntent()->getOutputMediaIdType();
                    if (quicksetOutputMediaIdType == currentMediaType)
                    {
                        CHECKPOINTC(
                            "JobServiceStandard::onMediaPropertyChangedEvent ticket %s need to be updated, set new "
                            "media type",
                            ticketId.c_str());
                        ticket->getIntent()->setOutputMediaIdType(ticketSave->getIntent()->getOutputMediaIdType());
                        persistJobTicketFromCache(ticketId);
                    }
                    else
                    {
                        CHECKPOINTD(
                            "JobServiceStandard::onMediaPropertyChangedEvent ticket %s not updated as currentMediatype "
                            "is not same as changedMediatype",
                            ticketId.c_str());
                    }
                }
            }
        }
    }
    CHECKPOINTB("%s/JobServiceStandard::onMediaPropertyChangedEvent: Exit", getComponentInstanceName());
}

void JobServiceStandard::shutdown(ShutdownCause cause, std::future<void> &asyncCompletion)
{
    DUNE_UNUSED(cause);
    DUNE_UNUSED(asyncCompletion);
    CHECKPOINTC("%s/JobServiceStandard: shutdown", getComponentInstanceName());
    if (subscriptionHandlerExportImport_ != nullptr)
    {
        // Removes the subscription of Export and Import
        subscriptionHandlerExportImport_.reset();
    }
    if (subscriptionHandlerBackupRestore_ != nullptr)
    {
        // Removes the subscription of Backup and Restore
        subscriptionHandlerBackupRestore_.reset();
    }
}

std::unique_ptr<JobServiceStandardConfigT> JobServiceStandard::getConfiguration(
    dune::framework::resources::IConfigurationService *configurationService) const
{
    CHECKPOINTC("%s/JobServiceStandard::getConfiguration:", getComponentInstanceName());

    assert(configurationService);
    dune::framework::resources::IConfigurationService::ConfigurationRawData rawConfiguration =
        configurationService->getConfiguration(GET_MODULE_UID(JobServiceStandard), getComponentInstanceName());
    if (rawConfiguration.data && (rawConfiguration.size > 0))
    {
        flatbuffers::Verifier verifier(rawConfiguration.data.get(), rawConfiguration.size);
        assert(VerifyJobServiceStandardConfigBuffer(verifier));
        return UnPackJobServiceStandardConfig(rawConfiguration.data.get());
    }
    else
    {
        return std::unique_ptr<JobServiceStandardConfigT>();
    }
}

std::shared_ptr<std::map<std::string, std::string>> JobServiceStandard::getJobServiceStringIds() const
{
    if (configuration_ != nullptr)
    {
        CHECKPOINTC("JobServiceStandard::getJobServiceStringIds stringIds configuration found");
        std::vector<std::shared_ptr<CopyStringIdMapT>> copyStringIds = std::move(configuration_->stringIds);
        auto stringIdsMap = std::make_shared<std::map<std::string, std::string>>();
        for (auto const &stringIds : copyStringIds)
        {
            stringIdsMap->emplace(stringIds->type, stringIds->stringId);
        }
        return stringIdsMap;
    }
    CHECKPOINTC("JobServiceStandard::getJobServiceStringIds stringIds configuration not found");
    return nullptr;
}

std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> JobServiceStandard::getFactoryDefaultJobTicket(JobType jobType)
{
    CHECKPOINTC("%s/JobServiceStandard::getFactoryDefaultJobTicket(JobType jobType) - Enter",
                getComponentInstanceName());
    DUNE_UNUSED(jobType);
    // Update when take job type will be implemented from factory defaults.
    auto                              ticket = createEmptyJobTicket();
    dune::imaging::types::MediaSizeId mediaSize = scanPipeline_->getDefaultMediaSize();
    if (mediaSize != dune::imaging::types::MediaSizeId::UNDEFINED)
    {
        CHECKPOINTC("%s/JobServiceStandard::getFactoryDefaultJobTicket() set Cold ResetMediaSize",
                    getComponentInstanceName());
        // set the Cold reset Media Size when creating a job ticket from Scartch
        ticket->getIntent()->setOutputMediaSizeId(mediaSize);
        ticket->getIntent()->setInputMediaSizeId(mediaSize);
    }
    else
    {
        CHECKPOINTA("%s/JobServiceStandard::getFactoryDefaultJobTicket() mediaSize is UNDEFINED",
                    getComponentInstanceName());
    }

    if (localization_)
    {
        CHECKPOINTC("%s/JobServiceStandard::getFactoryDefaultJobTicket() set width and height to letter as default",
                    getComponentInstanceName());
        /*  set width and height of letter as default.
                wdith  : 8.5(inch)  -> 85000(inch*10000)
                height : 11(inch)   -> 110000(inch*10000)
         */
        double defaultWidth = 85000.0;
        double defaultHeight = 110000.0;

        if (localization_->getMeasurmentUnit() == dune::localization::MeasurementUnit::METRIC)
        {
            CHECKPOINTC("%s/JobServiceStandard::getFactoryDefaultJobTicket() set width and height to a4",
                        getComponentInstanceName());
            /* set width and height to a4 .
               wdith  : 210(mm) -> 8.2677(inch)  -> 82677(inch*10000)
               height : 297(mm) -> 11.6929(inch) -> 116929(inch*10000)
             */
            defaultWidth = 82677.0;
            defaultHeight = 116929.0;
        }
        ticket->getIntent()->setCustomMediaXDimension(defaultWidth);
        ticket->getIntent()->setCustomMediaYDimension(defaultHeight);
    }
    else
    {
        CHECKPOINTA(
            "%s/JobServiceStandard::getFactoryDefaultJobTicket() localization_ is null. set custom x,y value to letter",
            getComponentInstanceName());
        ticket->getIntent()->setCustomMediaXDimension((double)85000.0);
        ticket->getIntent()->setCustomMediaYDimension((double)110000.0);
    }

    CHECKPOINTC("%s/JobServiceStandard::getFactoryDefaultJobTicket(JobType jobType) - Exit",
                getComponentInstanceName());

    return ticket;
}

std::map<JobType, dune::security::ac::Permission> JobServiceStandard::getJobCreationPermissions()
{
    CHECKPOINTC("%s/JobServiceStandard::getJobCreationPermissions - Enter", getComponentInstanceName());
    std::map<JobType, Permission> copyJobCreationPermissionMap;
    copyJobCreationPermissionMap[JobType::COPY] = Permission::CP_COPY_APP;

    CHECKPOINTC("%s/JobServiceStandard::getJobCreationPermissions - Exit", getComponentInstanceName());
    return copyJobCreationPermissionMap;
};

std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> JobServiceStandard::createJobTicketUsingFlatbuffer(
    std::shared_ptr<CopyJobIntentFbT> intentFb)
{
    CHECKPOINTC("%s/JobServiceStandard::createJobTicketUsingFlatbuffer - Enter", getComponentInstanceName());
    auto ticket = std::make_shared<dune::copy::Jobs::Copy::CopyJobTicket>(getSystemServices()->threadPool_);
    ticket->setApplicationName(applicationNameForCopy);
    ticket->setMediaInterface(servicePackage_.mediaInterface);
    ticket->setColorAccessControlInterface(colorAccessControl_);
    ticket->setMediaInfoInterface(servicePackage_.mediaInfo);
    ticket->setScanMediaInterface(scanMedia_);
    ticket->setScanCapabilitiesInterface(scanCapabilities_);
    ticket->setNvramInterface(Nvram_);
    ticket->setLocalizationInterface(localization_);
    ticket->setPrePrintConfiguration((Product)prePrintConfiguration_);

    // Update intent with flatbuffer data.
    if (intentFb)
    {
        ticket->setIntent(intentFb);
        /* In case of dest/print/mediaDestination, the default value is set to STANDARDBIN.
        But, depending on whether HW is installed or not, the default value may change.(to AUTO) */
        ticket->validateMediaOutputDestination();
    }

    // Take the constraints from the component asociated to it and load it to the ticket
    std::shared_ptr<CopyJobConstraintsFbT> constraints =
        jobConstraintsHelper_->getFbConstraintsTableFromConfiguration();
    if (constraints != nullptr)
    {
        ticket->setConstraintsFromFb(constraints);
    }
    if (configuration_)
    {
        auto isMediaTypeVisibilityTogglingSupported = configuration_->isMediaTypeVisibilityTogglingSupported;
        CHECKPOINTB(
            "CopyJobServiceStandard::createJobTicketUsingFlatbuffer() assigning isMediaTypeVisibilityTogglingSupported "
            "%d to ticket",
            isMediaTypeVisibilityTogglingSupported);
        ticket->setisMediaTypeVisibilityTogglingSupported(isMediaTypeVisibilityTogglingSupported);
    }

    // New tickets need to have the version expected.
    // Tickets taken from persistance could have oldest version of this value that will be need to be evaluate if needs
    // update on connected method
    if (configuration_ && configuration_->currentTicketVersion > 0)
    {
        CHECKPOINTC("CopyJobServiceStandard::createJobTicketUsingFlatbuffer() assigning version %u to ticket",
                    configuration_->currentTicketVersion);
        ticket->setVersion(configuration_->currentTicketVersion);
    }

    CHECKPOINTC("%s/JobServiceStandard::createJobTicketUsingFlatbuffer - Exit", getComponentInstanceName());
    return ticket;
}

void JobServiceStandard::handleScanMediaSizeEvent(dune::imaging::types::MediaSizeId mediaSizeId)
{
    CHECKPOINTA("%s/JobServiceStandard::handleScanMediaSizeEvent - Enter", getComponentInstanceName());

    // Update the job ticket with the new media size
    setDefaultJobTicketMediaSizeAndType(
        mediaSizeId, dune::imaging::types::MediaIdType::STATIONERY);

    CHECKPOINTC("%s/JobServiceStandard::handleScanMediaSizeEvent - Exit", getComponentInstanceName());
}

bool JobServiceStandard::setDefaultJobTicketMediaSizeAndType(const dune::imaging::types::MediaSizeId size,
                                                             const dune::imaging::types::MediaIdType type)
{
    bool retval = false;
    CHECKPOINTA(
        "%s/JobServiceStandard::setDefaultJobTicketMediaSizeAndType {dune::job::JobType:COPY} Default Ticket - "
        "{MediaIdType:%d} {MediaSizeId:%d} -Enter",
        getComponentInstanceName(), type, size);
    auto ticketSave = getDefaultJobTicket();
    if (ticketSave)
    {
        if (ticketSave->getIntent()->getOutputMediaSizeId() == dune::imaging::types::MediaSizeId::LETTER ||
            ticketSave->getIntent()->getOutputMediaSizeId() == dune::imaging::types::MediaSizeId::A4)
        {
            ticketSave->getIntent()->setOutputMediaSizeId(size);
            ticketSave->getIntent()->setOutputMediaIdType(type);
        }
        if (ticketSave->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::LETTER ||
            ticketSave->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::A4)
        {
            ticketSave->getIntent()->setInputMediaSizeId(size);
        }
        retval = saveDefaultJobTicket(ticketSave, TicketUpdationMode::internal);
        // CHECKPOINTA("JobServiceStandard::setDefaultJobTicketMediaSizeAndType {dune::job::JobType:%d} Default Ticket
        // Successfully Updated.", jobType);
    }
    else
    {
        // CHECKPOINTA("WARNING: Failed to update JobType::FOLDER_PRINT DefaultJobTicket: MediaSize, MediaType",
        // jobType);
    }
    CHECKPOINTC("%s/JobServiceStandard::setDefaultJobTicketMediaSizeAndType : EXIT - returning {Bool:%d}",
                getComponentInstanceName(), retval);

    return retval;
}

std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> JobServiceStandard::createEmptyJobTicket()
{
    CHECKPOINTC("%s/JobServiceStandard::createEmptyJobTicket() - Enter", getComponentInstanceName());

    std::shared_ptr<CopyJobIntentFbT> defaultValuesFb{nullptr};

    // Create ticket with default values if they are available
    if (configuration_ && configuration_->jobIntentConfiguration &&
        configuration_->jobIntentConfiguration->defaultValues)
    {
        defaultValuesFb = configuration_->jobIntentConfiguration->defaultValues;
    }
    CHECKPOINTC("%s/JobServiceStandard::createEmptyJobTicket() - Exit", getComponentInstanceName());

    return createJobTicketUsingFlatbuffer(defaultValuesFb);
}

std::shared_ptr<dune::job::IPipelineBuilder> JobServiceStandard::createPipelineBuilder(
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> jobTicket)
{
    CHECKPOINTA("%s/JobServiceStandard: createPipelineBuilder - Enter", getComponentInstanceName());

    // set intent Manager in services
    servicePackage_.intentsManager = intentsManager_;

    jobTicket->setPrePrintConfiguration((Product)prePrintConfiguration_);
    jobTicket->setMaxLengthConfig(maxLengthConfig_);
    jobTicket->setIntentsManager(intentsManager_);

    // Apply configuration to pageIntent fields
    auto &pageIntent = jobTicket->getPageIntent();
    pageIntent.renderIntent = renderIntent_;
    auto pipelineBuilder = copyPipeline_->createPipelineBuilder(
        jobTicket, (Product)prePrintConfiguration_, servicePackage_, scanPipeline_, copyBasicPipeline_,
        hasSharedPaperPath_, maxLengthConfig_, getSystemServices()->dateTime_, multiPageSupportedFromFlatbed_);

    CHECKPOINTA("%s/JobServiceStandard: createPipelineBuilder - Exit", getComponentInstanceName());
    return pipelineBuilder;
}

std::shared_ptr<dune::job::IPromptController> JobServiceStandard::createPromptController(
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> jobTicket)
{
    CHECKPOINTA("%s/JobServiceStandard: createPromptController - Enter", getComponentInstanceName());
    assert(jobTicket != nullptr);
    auto promptController = std::make_shared<CopyJobPromptController>(
        jobTicket, jobManagerAlertProvider_, (Product)prePrintConfiguration_, multiPageSupportedFromFlatbed_);

    CHECKPOINTA("%s/JobServiceStandard: createPromptController - Exit", getComponentInstanceName());
    return promptController;
}

void JobServiceStandard::registerShortcuts()
{
    CHECKPOINTC("%s/JobServiceStandard::registerShortcuts Enter", getComponentInstanceName());

    dune::admin::shortcuts::ShortcutOperationResult result;
    auto shortcutToAdd = std::make_unique<dune::cdm::shortcut_1::ShortcutTable>(
        "cedab422-33b3-4638-b6a1-604e54525215", "", dune::cdm::shortcut_1::Type::nativeApp,
        dune::cdm::shortcut_1::Action::open);
    shortcutToAdd->readOnly.set(dune::cdm::glossary_1::FeatureEnabled::false_);
    shortcutToAdd->origin.set(dune::cdm::shortcut_1::Origin::externalService);
    shortcutToAdd->factory.set(dune::cdm::glossary_1::FeatureEnabled::true_);
    shortcutToAdd->copyAllowed.set(dune::cdm::glossary_1::FeatureEnabled::false_);
    shortcutToAdd->source.set(dune::cdm::shortcut_1::Source::scan);
    std::vector<dune::cdm::shortcut_1::DestinationEnum> destinations{dune::cdm::shortcut_1::Destination::print};
    shortcutToAdd->destinations = destinations;
    dune::cdm::shortcut_1::LocalIdTable titleId;

    bool copyEnabled = false;
    shortcutToAdd->state.set(dune::cdm::shortcut_1::State::ready);
    if (copyAdapter_ != nullptr)
    {
        copyEnabled = copyAdapter_->getCopyEnabled();
    }
    if (copyEnabled == false)
    {
        shortcutToAdd->state.set(dune::cdm::shortcut_1::State::disabled);
    }

    // IF IDCARDCopy is supported the Copy App name will be document copy
    if (configuration_->isSupportedIdCardCopy)
    {
        titleId.idValue.set(static_cast<unsigned int>(dune::localization::string_id::cDocumentCopyApp.value()));
    }
    else
    {
        titleId.idValue.set(static_cast<unsigned int>(dune::localization::string_id::cCopyAppHeading.value()));
    }

    shortcutToAdd->titleId.set(titleId);
    shortcutToAdd->description.set("CopyApp Shortcut");
    shortcutToAdd->permissionId.set("ef92c290-8fa5-4403-85bc-f6becc86b787");

    std::vector<dune::cdm::glossary_1::links::ItemTable> links;
    dune::cdm::glossary_1::links::ItemTable              link("shortcut");
    link.href = "/CopyApp";
    links.push_back(link);
    shortcutToAdd->links.set(links);

    result = getIShortcuts()->addShortcut(std::move(shortcutToAdd));
    if (result != dune::admin::shortcuts::ShortcutOperationResult::OK &&
        result != dune::admin::shortcuts::ShortcutOperationResult::ERROR_ID_ALREADY_EXIST)
    {
        CHECKPOINTB("%s/JobServiceStandard::registerShortcuts failed to add CopyApp shortcut",
                    getComponentInstanceName());
    }

    if (configuration_->isSupportedIdCardCopy)
    {
        auto shortcutCardCopy = std::make_unique<dune::cdm::shortcut_1::ShortcutTable>(
            "c74293eb-04c1-4dff-b469-1c0e99fdbe8b", "", dune::cdm::shortcut_1::Type::nativeApp,
            dune::cdm::shortcut_1::Action::open);
        shortcutCardCopy->readOnly.set(dune::cdm::glossary_1::FeatureEnabled::false_);
        shortcutCardCopy->origin.set(dune::cdm::shortcut_1::Origin::externalService);
        shortcutCardCopy->factory.set(dune::cdm::glossary_1::FeatureEnabled::true_);
        shortcutCardCopy->copyAllowed.set(dune::cdm::glossary_1::FeatureEnabled::false_);
        shortcutCardCopy->source.set(dune::cdm::shortcut_1::Source::scan);
        std::vector<dune::cdm::shortcut_1::DestinationEnum> destinationsCardCopy{
            dune::cdm::shortcut_1::Destination::print};
        shortcutCardCopy->destinations = destinationsCardCopy;
        dune::cdm::shortcut_1::LocalIdTable titleIdCardCopy;
        titleIdCardCopy.idValue.set(static_cast<unsigned int>(dune::localization::string_id::cIDCardCopyApp.value()));
        shortcutCardCopy->titleId.set(titleIdCardCopy);
        shortcutCardCopy->description.set("IDCardCopyApp Shortcut");
        shortcutCardCopy->permissionId.set("ef92c290-8fa5-4403-85bc-f6becc86b787");

        shortcutCardCopy->state.set(dune::cdm::shortcut_1::State::ready);
        if (copyEnabled == false)
        {
            shortcutCardCopy->state.set(dune::cdm::shortcut_1::State::disabled);
        }
        std::vector<dune::cdm::glossary_1::links::ItemTable> linksCardCopy;
        dune::cdm::glossary_1::links::ItemTable              linkCardCopy("shortcut");
        linkCardCopy.href = "/IDCardCopyApp";
        linksCardCopy.push_back(linkCardCopy);
        shortcutCardCopy->links.set(linksCardCopy);

        result = getIShortcuts()->addShortcut(std::move(shortcutCardCopy));
        if (result != dune::admin::shortcuts::ShortcutOperationResult::OK &&
            result != dune::admin::shortcuts::ShortcutOperationResult::ERROR_ID_ALREADY_EXIST)
        {
            CHECKPOINTB("%s/JobServiceStandard::registerShortcuts failed to add IDCardCopyApp shortcut",
                        getComponentInstanceName());
        }
    }

    // Add factory quicksets if needed
    if (!configuration_->copyQuicksets.empty())
    {
        CHECKPOINTD("%s/JobServiceStandard::registerShortcuts Checking quicksets list on copy with size %d",
                    getComponentInstanceName(), configuration_->copyQuicksets.size());

        for (auto quicksetData : configuration_->copyQuicksets)
        {
            addFactoryShortcut(quicksetData);
        }
    }
    else
    {
        CHECKPOINTB("%s/JobServiceStandard::registerShortcuts field configuration_->copyQuicksets is empty()",
                    getComponentInstanceName());
    }

    CHECKPOINTC("%s/JobServiceStandard::registerShortcuts Exit", getComponentInstanceName());
}

// We add shortcuts reading the data included in a CopyQuicksetDataT fb table.
void JobServiceStandard::addFactoryShortcut(
    const std::shared_ptr<dune::admin::shortcuts::FactoryShortuctDefT> quicksetData)
{
    CHECKPOINTC("%s/JobServiceStandard::addFactoryShortcut Enter", getComponentInstanceName());

    auto factoryQuickset =
        loadFactoryQuicksetFromJson(quicksetData->fileName, "JobServiceFactoryQuicksetConfig.fbs", "CopyQuicksetFb");

    std::string                         translatedTitle;
    dune::cdm::shortcut_1::LocalIdTable titleLocalizationTable;

    std::tie(translatedTitle, titleLocalizationTable) = localizeQuicksetTitleFromStringId(quicksetData->titleStringID);

    auto shortcutToAdd = std::make_unique<dune::cdm::shortcut_1::ShortcutTable>(
        quicksetData->uuid.c_str(), translatedTitle,
        ShortcutsHelper::convertType(factoryQuickset->metadata->shortcutType),
        ShortcutsHelper::convertAction(factoryQuickset->metadata->action));

    shortcutToAdd->titleId.set(titleLocalizationTable);
    shortcutToAdd->readOnly.set(dune::job::cdm::mapToCdmFeatureEnabled(factoryQuickset->metadata->isReadOnly));
    shortcutToAdd->factory.set(dune::job::cdm::mapToCdmFeatureEnabled(factoryQuickset->metadata->isFactory));
    shortcutToAdd->copyAllowed.set(dune::job::cdm::mapToCdmFeatureEnabled(factoryQuickset->metadata->isCopyAllowed));
    shortcutToAdd->origin.set(ShortcutsHelper::convertOrigin(factoryQuickset->metadata->origin));
    shortcutToAdd->source.set(ShortcutsHelper::convertSource(factoryQuickset->metadata->source));

    auto destinations = std::vector<dune::cdm::shortcut_1::DestinationEnum>();
    ShortcutsHelper::convertDestinations(destinations, factoryQuickset->metadata->destinations);
    shortcutToAdd->destinations = destinations;

    // Create a ticket with quickset intent values.
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> qsTicket =
        createJobTicketUsingFlatbuffer(factoryQuickset->ticketSettings);

    bool ticketAlreadyInCache{false};
    addTicketToCache(qsTicket, ticketAlreadyInCache);
    assert(!ticketAlreadyInCache);  // a fresh new cloned ticket cannot exist in the cache.

    // Link the ticket
    std::vector<dune::cdm::glossary_1::links::ItemTable> links;
    dune::cdm::glossary_1::links::ItemTable              link("shortcut");

    std::string shortcutHref = "/cdm/jobTicket/v1/tickets/";
    shortcutHref.append(qsTicket->getTicketId().toString());
    link.href = shortcutHref;

    links.push_back(link);
    shortcutToAdd->links.set(links);

    // When added to the shortcuts the ticket is persisted.
    auto result = getIShortcuts()->addShortcut(std::move(shortcutToAdd));

    if (result != dune::admin::shortcuts::ShortcutOperationResult::OK &&
        result != dune::admin::shortcuts::ShortcutOperationResult::ERROR_ID_ALREADY_EXIST)
    {
        CHECKPOINTB("%s/JobServiceStandard::registerShortcuts failed to add Factory shortcut %s",
                    getComponentInstanceName(), translatedTitle.c_str());
    }

    CHECKPOINTC("%s/JobServiceStandard::addFactoryShortcut Exit", getComponentInstanceName());
}

void JobServiceStandard::resetShortcuts(dune::framework::data::resets::ResetLevel resetLevel)
{
    CHECKPOINTD("%s/JobServiceStandard::resetUserShortcuts - ENTER", getComponentInstanceName());

    // setup the filter to get job service specific shortcuts.
    CHECKPOINTD("JobServiceStandard::resetUserShortcuts: requested reset level = %d.", static_cast<int>(resetLevel));
    dune::admin::shortcuts::shortcutFilter_t filter;
    filter.src = dune::cdm::shortcut_1::Source::scan;
    filter.dest = dune::cdm::shortcut_1::Destination::print;
    filter.origin = dune::cdm::shortcut_1::Origin::device;
    filter.type = dune::cdm::shortcut_1::Type::singleJob;
    if (resetLevel == dune::framework::data::resets::ResetLevel::USER_DATA_RESET)
    {
        // If the reset level is user data, then we should not be requesting factory shortcuts.
        // and if the reset level is factory data, then we must reset both user and factory shortcuts.
        filter.factory = dune::cdm::glossary_1::FeatureEnabled::false_;
    }

    auto shortcutsData = getIShortcuts()->getShortcuts(true, filter);  // with pinValidateNotReq

    if (shortcutsData != nullptr)
    {
        CHECKPOINTB("JobServiceStandard::resetUserShortcuts Number of Shortcuts to reset = %d.",
                    static_cast<int>(shortcutsData->collection().size()));

        for (auto &shortcut : shortcutsData->collection().getMutable())
        {
            getIShortcuts()->removeShortcut(shortcut.id.get(), true);  // with pinValidateNotReq
        }
    }
    CHECKPOINTD("%s/JobServiceStandard::resetUserShortcuts - EXIT", getComponentInstanceName());
}

void JobServiceStandard::registerJobServiceState()
{
    CHECKPOINTD("%s/JobServiceStandard::registerJobServiceState - ENTER", instanceName_);

    copyEventSubscriptionId = copyAdapter_->getCopyAdapterDataChangeEvent().addSubscription(
        EVENT_MAKE_MEMBER_DELEGATE(JobServiceStandard::handleCopyAdapterDataChangeEvent, this));

    onCopyEnableStateChange();  // To update shortcut state while boot up
    CHECKPOINTD("%s/JobServiceStandard::registerJobServiceState - EXIT", instanceName_);
}

void JobServiceStandard::handleCopyAdapterDataChangeEvent(dune::copy::cdm::CopyConfigurationEventType event)
{
    CHECKPOINTD("%s/JobServiceStandard::handleCopyAdapterDataChangeEvent - ENTER", instanceName_);

    if (dune::copy::cdm::CopyConfigurationEventType::COPY_ENABLE_STATE_CHANGE == event)
    {
        onCopyEnableStateChange();
    }

    CHECKPOINTD("%s/JobServiceStandard::handleCopyAdapterDataChangeEvent - EXIT", instanceName_);
}

void JobServiceStandard::onCopyEnableStateChange()
{
    CHECKPOINTC("%s/JobServiceStandard::onCopyEnableStateChange - ENTER", getComponentInstanceName());

    dune::admin::shortcuts::shortcutFilter_t filter = dune::admin::shortcuts::shortcutFilter_t();
    filter.src = dune::cdm::shortcut_1::Source::scan;
    filter.dest = dune::cdm::shortcut_1::Destination::print;
    filter.origin = dune::cdm::shortcut_1::Origin::externalService;
    filter.type = dune::cdm::shortcut_1::Type::nativeApp;

    if (copyAdapter_->getCopyEnabled())
    {
        changeState(dune::job::JobServiceStateType::AVAILABLE, JobType::COPY);
        updateShortcut(filter, dune::cdm::shortcut_1::State::ready);
    }
    else
    {
        changeState(dune::job::JobServiceStateType::UNAVAILABLE, JobType::COPY);
        updateShortcut(filter, dune::cdm::shortcut_1::State::disabled);
    }
    CHECKPOINTC("%s/JobServiceStandard::onCopyEnableStateChange - EXIT", getComponentInstanceName());
}

void JobServiceStandard::updateShortcut(dune::admin::shortcuts::shortcutFilter_t &filter,
                                        const dune::cdm::shortcut_1::State       &state)
{
    CHECKPOINTD("%s/JobServiceStandard::updateShortcut Enter", instanceName_);

    if (nullptr != getIShortcuts())
    {
        dune::admin::shortcuts::ShortcutOperationResult result;

        auto shortcuts = getIShortcuts()->getShortcuts(true, filter);

        for (auto &shortcut : shortcuts->collection().getMutable())
        {
            if (shortcut.state.get() != state)
            {
                CHECKPOINTA("%s/JobServiceStandard::updateShortcut change shortcut state", instanceName_);
                auto shortcutToUpdate = std::make_unique<ItemEasyBufferTable>(shortcut);
                shortcutToUpdate->beginMergePatch();
                shortcutToUpdate->state.set(state);
                result = getIShortcuts()->updateShortcut(std::move(shortcutToUpdate), true, filter);

                if (result != dune::admin::shortcuts::ShortcutOperationResult::OK)
                {
                    CHECKPOINTA("%s/JobServiceStandard::updateShortcut failed to update shortcut", instanceName_);
                }
            }
        }
    }
    else
    {
        CHECKPOINTA("%s/JobServiceStandard::updateShortcut getIShortcuts() is null", instanceName_);
    }

    CHECKPOINTD("%s/JobServiceStandard::updateShortcut Exit", instanceName_);
}

bool JobServiceStandard::isPrintService()
{
    return configuration_->isPrintService;
}

std::string JobServiceStandard::getResourcePath()
{
    CHECKPOINTC("%s/JobServiceStandard::getResourcePath - ENTER", getComponentInstanceName());

    // Get resources directory.
    std::string resourcePath;

    dune::framework::storage::path::IPathDirectory *pathDirectory =
        getSystemServices()->pathServices_->getPathDirectory();
    assert(pathDirectory);

    resourcePath = pathDirectory->getPath(dune::framework::storage::path::Paths::RESOURCE_DIRECTORY);

    // Append id of component to path.
    if (resourcePathWithComponentId_)
    {
        std::stringstream stream;
        stream << std::hex << getComponentFlavorUid();

        std::string ifaceId("0x");
        ifaceId.append(stream.str());

        resourcePath.append(ifaceId).append("/");
    }

    CHECKPOINTC("%s/JobServiceStandard::getResourcePath RESOURCE_DIRECTORY path: %s - EXIT", getComponentInstanceName(),
                resourcePath.c_str());

    return resourcePath;
}

std::shared_ptr<CopyQuicksetFbT> JobServiceStandard::loadFactoryQuicksetFromJson(std::string quicksetFileName,
                                                                                 std::string schemaFilename,
                                                                                 std::string fbsRoot)
{
    auto resourcesPath = getResourcePath();

    // Load json file into a string
    std::string jsonFile;
    std::string jsonFileName{resourcesPath + quicksetFileName};
    bool        jsonLoadingResult = flatbuffers::LoadFile(jsonFileName.c_str(), false, &jsonFile);
    assert(jsonLoadingResult);

    // Deserialize using Flatbuffer utils.
    dune::framework::utils::FBUtils<CopyQuicksetFbT, CopyQuicksetFb> fbUtils;
    std::string                                                      schemaPath{resourcesPath + schemaFilename};
    const char *incDirectories[] = {".", resourcesPath.c_str(), nullptr};
    auto        factoryQuickset = fbUtils.deserializeToFBT(jsonFile, schemaPath, fbsRoot, incDirectories);
    assert(factoryQuickset);

    return factoryQuickset;
}

std::tuple<std::string, dune::cdm::shortcut_1::LocalIdTable> JobServiceStandard::localizeQuicksetTitleFromStringId(
    std::string titleStringIdCsf)
{
    dune::cdm::shortcut_1::LocalIdTable localIdTable;
    localIdTable.idString.set(titleStringIdCsf);

    auto deviceLocale = localization_->deviceLocale();

    auto titleStringId = deviceLocale->getStringIdForCsfOnly(titleStringIdCsf.c_str());
    localIdTable.idValue.set(titleStringId);

    auto translatedTitle = deviceLocale->get(titleStringId);

    return std::make_tuple(translatedTitle, localIdTable);
}

void JobServiceStandard::validateCurrentTickets()
{
    CHECKPOINTA("CopyJobServiceStandard::validateCurrentTickets start");

    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> defaultJobTicket = getDefaultJobTicket();
    assert(defaultJobTicket);
    if (!defaultJobTicket)
    {
        CHECKPOINTA("CopyJobServiceStandard::validateCurrentTickets default job ticket null");
        return;
    }

    std::shared_ptr<CopyJobIntentFbT> defaultValuesFb{nullptr};

    // Create ticket with default values if they are available
    if (configuration_ && configuration_->jobIntentConfiguration &&
        configuration_->jobIntentConfiguration->defaultValues)
    {
        CHECKPOINTA("CopyJobServiceStandard::validateCurrentTickets obtain default value");
        defaultValuesFb = configuration_->jobIntentConfiguration->defaultValues;
    }

    // Do validation and if true, save ticket.
    // Validation can't be done if default from FB not exist.
    if (defaultValuesFb)
    {
        bool updateTicket = false;

        // First check if ticket need to do any forced change
        if (configuration_ && configuration_->currentTicketVersion > 0 &&
            defaultJobTicket->getVersion() < configuration_->currentTicketVersion &&
            !configuration_->ticketUpgradeFunctionality.empty())
        {
            CHECKPOINTB(
                "CopyJobServiceStandard::validateCurrentTickets ticket has an old version %u than current on job "
                "service %u",
                defaultJobTicket->getVersion(), configuration_->currentTicketVersion);
            // Force update current default ticket certain values indicated on csf configurable
            for (auto upgradeStep : configuration_->ticketUpgradeFunctionality)
            {
                if (upgradeStep->version > defaultJobTicket->getVersion() &&
                    !upgradeStep->listOfSettingsToBeForced.empty())
                {
                    for (auto upgradeStepSettingEnum : upgradeStep->listOfSettingsToBeForced)
                    {
                        // Execute map function: map->executeFunction(ticket, defaultTicket)
                        auto pair = MAP_TO_FORCE_VALUE_FROM_DEFAULT_TICKET.find(upgradeStepSettingEnum);
                        assert_msg(pair != MAP_TO_FORCE_VALUE_FROM_DEFAULT_TICKET.end(),
                                   "CopyJobServiceStandard::validateCurrentTickets unsupported setting enum %d on "
                                   "MAP_TO_FORCE_VALUE_FROM_DEFAULT_TICKET",
                                   static_cast<int>(upgradeStepSettingEnum));
                        if (pair != MAP_TO_FORCE_VALUE_FROM_DEFAULT_TICKET.end())
                        {
                            CHECKPOINTD(
                                "CopyJobServiceStandard::validateCurrentTickets ticket changed value for enum on Fbs "
                                "%d",
                                static_cast<int>(upgradeStepSettingEnum));
                            pair->second(defaultJobTicket, defaultValuesFb);
                            updateTicket = true;
                        }
                    }

                    defaultJobTicket->setVersion(upgradeStep->version);
                    CHECKPOINTC("CopyJobServiceStandard::validateCurrentTickets ticket upgraded to version %u",
                                defaultJobTicket->getVersion());
                }
            }
        }
        // ValidateTicket and update if updateTicket is true
        dune::copy::Jobs::Copy::validateTicket(defaultJobTicket, defaultValuesFb, updateTicket);   
        if (updateTicket)
        {
            CHECKPOINTC(
                "CopyJobServiceStandard::validateCurrentTickets ticket need to be updated, save default job ticket");
            saveDefaultJobTicket(defaultJobTicket, TicketUpdationMode::internal);
        }
        else
        {
            CHECKPOINTD("CopyJobServiceStandard::validateCurrentTickets ticket default is ok, not updated");
        }
    }
    else
    {
        CHECKPOINTB(
            "CopyJobServiceStandard::validateCurrentTickets default values or constraints are not valid, so validate "
            "can't be do");
    }

    // Get and updated User Quicksets
    dune::admin::shortcuts::shortcutFilter_t filter;
    filter.src = dune::cdm::shortcut_1::Source::scan;
    filter.dest = dune::cdm::shortcut_1::Destination::print;
    filter.origin = dune::cdm::shortcut_1::Origin::device;
    filter.type = dune::cdm::shortcut_1::Type::singleJob;
    filter.factory = dune::cdm::glossary_1::FeatureEnabled::false_;
    auto shortcutsData = getIShortcuts()->getShortcuts(true, filter);  // with pinValidateNotReq

    if (shortcutsData != nullptr)
    {
        CHECKPOINTC(
            "CopyJobServiceStandard::validateCurrentTickets Number of Shortcuts to check if need to be updated = %d.",
            static_cast<int>(shortcutsData->collection().size()));

        for (auto &shortcut : shortcutsData->collection().getMutable())
        {
            for (auto link : shortcut.links.getMutable())
            {
                // Trim current ticket removing /cdm/jobTicket/v1/tickets/ reference
                auto        ticketReference = link.href.getMutable();
                std::size_t positionDivider = ticketReference.find_last_of("/\\");
                auto        ticketId = ticketReference.substr(positionDivider + 1);
                CHECKPOINTC("CopyJobServiceStandard::validateCurrentTickets id to validate: %s", ticketId.c_str());

                // Load ticket to cache if needed
                bool persistentTicket;
                auto jobTicket =
                    getJobTicketResourceManager()->loadJobTicketIntoCacheIfNeeded(ticketId, persistentTicket);
                if (jobTicket == nullptr)
                {
                    CHECKPOINTB(
                        "CopyJobServiceStandard::validateCurrentTickets() job ticket %s not found in cache and fail to "
                        "add it cache",
                        ticketId.c_str());
                    continue;
                }

                bool userTicketUpdated = false;
                auto ticket = std::dynamic_pointer_cast<dune::copy::Jobs::Copy::ICopyJobTicket>(jobTicket);

                // First check if ticket need to do any forced change
                if (configuration_ && configuration_->currentTicketVersion > 0 &&
                    ticket->getVersion() < configuration_->currentTicketVersion &&
                    !configuration_->ticketUpgradeFunctionality.empty())
                {
                    CHECKPOINTB(
                        "CopyJobServiceStandard::validateCurrentTickets ticket from user quicksets has an old version "
                        "%u than current on job service %u",
                        ticket->getVersion(), configuration_->currentTicketVersion);
                    // Force update current default ticket certain values indicated on csf configurable
                    for (auto upgradeStep : configuration_->ticketUpgradeFunctionality)
                    {
                        if (upgradeStep->version > ticket->getVersion() &&
                            !upgradeStep->listOfSettingsToBeForced.empty())
                        {
                            for (auto upgradeStepSettingEnum : upgradeStep->listOfSettingsToBeForced)
                            {
                                // Execute map function: map->executeFunction(ticket, defaultTicket)
                                auto pair = MAP_TO_FORCE_VALUE_FROM_DEFAULT_TICKET.find(upgradeStepSettingEnum);
                                assert_msg(pair != MAP_TO_FORCE_VALUE_FROM_DEFAULT_TICKET.end(),
                                           "CopyJobServiceStandard::validateCurrentTickets unsupported setting enum %d "
                                           "on MAP_TO_FORCE_VALUE_FROM_DEFAULT_TICKET",
                                           static_cast<int>(upgradeStepSettingEnum));
                                if (pair != MAP_TO_FORCE_VALUE_FROM_DEFAULT_TICKET.end())
                                {
                                    CHECKPOINTD(
                                        "CopyJobServiceStandard::validateCurrentTickets ticket changed value for enum "
                                        "on Fbs %d",
                                        static_cast<int>(upgradeStepSettingEnum));
                                    pair->second(ticket, defaultValuesFb);
                                    userTicketUpdated = true;
                                }
                            }

                            ticket->setVersion(upgradeStep->version);
                            CHECKPOINTC("CopyJobServiceStandard::validateCurrentTickets ticket upgraded to version %u",
                                        ticket->getVersion());
                        }
                    }
                }

                dune::copy::Jobs::Copy::validateTicket(ticket, defaultValuesFb, userTicketUpdated);
                if (userTicketUpdated)
                {
                    CHECKPOINTC(
                        "CopyJobServiceStandard::validateCurrentTickets ticket %s need to be updated, save new ticket "
                        "changed on persistence",
                        ticketId.c_str());
                    persistJobTicketFromCache(ticketId);
                }
                else
                {
                    CHECKPOINTD("CopyJobServiceStandard::validateCurrentTickets ticket %s is ok, not updated",
                                ticketId.c_str());
                }
            }
        }
    }
}

OperationResult JobServiceStandard::exportData(const OperationDescription &exportDescription,
                                               const ContentId &contentId, std::string &version,
                                               FileInfoCollection &filesToExport)
{
    CHECKPOINTC("%s/JobServiceStandard COPY: exportData - ENTER", getComponentInstanceName());

    assert(std::find(std::cbegin(exportDescription.categories), std::cend(exportDescription.categories),
                     Category::CopySettings) != std::cend(exportDescription.categories));

    dune::framework::data::backup::OperationResult  operationResult = OperationResult::ERROR;
    dune::framework::storage::path::IPathDirectory *pathDirectory =
        getSystemServices()->pathServices_->getPathDirectory();

    if (contentId != contentId_)
    {
        CHECKPOINTA("CopyJobServiceStandard::exportData: Unknown content Id: %s", contentId.c_str());
        operationResult = OperationResult::ERROR_UNKNOWN_CONTENTID;
    }
    else
    {
        IExportImport::FileInfo fileInfo;
        fileInfo.tag = contentId;
        fileInfo.path = pathDirectory->createTempFile();  // pathDirectory is the IPathDirectory system service
        fileInfo.encrypt = false;
        fileInfo.disposable =
            true;  // the file can be deleted after ExportImportManager copies it into the export package.

        std::ofstream exportFile(fileInfo.path, std::ios::out | std::ios::binary | std::ios::trunc);

        // open the file to write setup and operation configs and it's content
        if (exportFile.is_open())
        {
            std::string serializedJson = serializeDefaultTicketToJson(dune::job::JobType::COPY);
            CHECKPOINTB("CopyJobServiceStandard::exportData: Did we get the json data? %d",
                        static_cast<int>(!serializedJson.empty()));
            if (!serializedJson.empty())
            {
                exportFile.write(serializedJson.c_str(), serializedJson.size());
                exportFile.flush();

                filesToExport.push_back(fileInfo);
                operationResult = OperationResult::SUCCESS;
            }
        }
        else
        {
            CHECKPOINTA("CopyJobServiceStandard::exportData: Failed to open file for writing: %s",
                        fileInfo.path.c_str());
            operationResult = OperationResult::ERROR;
        }
    }
    version = BACKUP_RESTORE_VERSION;

    CHECKPOINTC("%s/JobServiceStandard COPY: exportData - EXIT", getComponentInstanceName());

    return operationResult;
}

OperationResult JobServiceStandard::importData(const OperationDescription &importDescription,
                                               const IdentificationData &identificationData, const ContentId &contentId,
                                               const std::string &version, const FileInfoCollection &filesToImport)
{
    CHECKPOINTC("%s/JobServiceStandard COPY: importData - ENTRY", getComponentInstanceName());

    dune::framework::data::backup::OperationResult result(dune::framework::data::backup::OperationResult::ERROR);

    if (contentId == contentId_)
    {
        if (version == _VERSION_)
        {
            for (const FileInfo &fileInfo : filesToImport)
            {
                if (fileInfo.tag == contentId)
                {
                    auto defaultTicket = getDefaultJobTicket();
                    result = defaultTicket->readSettingsFromFile(fileInfo.path);
                    saveDefaultJobTicket(defaultTicket, TicketUpdationMode::internal);
                }
            }
        }
        else if (version == BACKUP_RESTORE_VERSION)
        {
            for (const FileInfo &fileInfo : filesToImport)
            {
                if (fileInfo.tag == contentId)
                {
                    std::ifstream importFile(fileInfo.path.c_str(), std::ios::in | std::ios::binary | std::ios::ate);
                    if (importFile.is_open())
                    {
                        std::streampos posEnd = importFile.tellg();
                        importFile.seekg(0, std::ios::beg);

                        std::string jsonData(std::istreambuf_iterator<char>(importFile), {});
                        if (importFile.good() && !jsonData.empty())
                        {
                            CHECKPOINTD("CopyJobServiceStandard::importData: Deserializing ticket");
                            bool deserializationResult =
                                deserializeJsonAndUpdateDefaultTicket(jsonData, dune::job::JobType::COPY);
                            if (deserializationResult)
                            {
                                result = OperationResult::SUCCESS;
                            }
                        }
                        else
                        {
                            CHECKPOINTA("CopyJobServiceStandard::importData: Error reading ticket from backup file");
                            result = OperationResult::ERROR_FILE_OPERATION;
                        }

                        importFile.close();
                    }
                    else
                    {
                        CHECKPOINTA_STR("CopyJobServiceStandard::importData: Failed to open file %s",
                                        fileInfo.path.c_str());
                        result = OperationResult::ERROR_FILE_OPERATION;
                    }
                }
            }
        }
        else
        {
            result = OperationResult::ERROR_VERSION_MISMATCH;
        }
    }
    else
    {
        result = OperationResult::ERROR_UNKNOWN_CONTENTID;
    }
    CHECKPOINTC("%s/JobServiceStandard COPY: importData - EXIT", getComponentInstanceName());
    return result;
}

void JobServiceStandard::getSerializationData(std::string &fbsPath, std::string &resourcesDirectoryPath,
                                              std::string &fbsRoot)
{
    fbsPath = COPY_JOB_SERVICE_RESOURCE_FILE_DIR + "CopyJobTicket.fbs";
    resourcesDirectoryPath = COPY_JOB_SERVICE_RESOURCE_FILE_DIR;
    fbsRoot = "CopyJobTicketFb";

    CHECKPOINTC("CopyJobServiceStandard::getSerializationData: fbsPath - %s, resourcesDirectoryPath - %s, fbsRoot - %s",
                fbsPath.c_str(), resourcesDirectoryPath.c_str(), fbsRoot.c_str());
}

bool JobServiceStandard::serializeTicketToJson(const std::string &ticketId, std::string &jsonData,
                                               std::string &dataToBeEncrypted)
{
    CHECKPOINTB("%s/JobServiceStandard::serializeTicketToJson: ENTER", getComponentInstanceName());
    dune::framework::utils::FBUtils<CopyJobTicketFbT, CopyJobTicketFb> fbUtils;
    bool                                                               result = false;
    dune::framework::core::Uuid                                        uuid = dune::framework::core::Uuid(ticketId);
    std::shared_ptr<ICopyJobTicket>                                    copyJobTicket = getTicketFromCache(uuid);

    if (copyJobTicket == nullptr)
    {
        // If ticket is not in cache, get it from Data Store
        CHECKPOINTB(
            "CopyJobServiceStandard::serializeTicketToJson: Error getting ticket from cache. Get from Data Store");
        try
        {
            copyJobTicket = getTicketFromDataStore(uuid);
        }
        catch (dune::framework::core::OperationFailedException &ex)
        {
            DUNE_UNUSED(ex);
            CHECKPOINTA("CopyJobServiceStandard::serializeTicketToJson: Error getting ticket from Data Store.");
            jsonData = "";
            dataToBeEncrypted = "";
            return result;
        }
    }

    if (copyJobTicket)
    {
        SerializedDataBufferPtr serializedTicket = copyJobTicket->serialize();
        dune::framework::data::FlatBufferDataObjectAdapter<CopyJobTicketFbT> fbAdapter{};
        CopyJobTicketFbT                                                     ticketFbT{};
        bool deserialized = fbAdapter.deserialize(serializedTicket, ticketFbT);

        fbUtils.setFBT(std::make_shared<dune::copy::Jobs::Copy::CopyJobTicketFbT>(ticketFbT));

        std::string fbsPath, fbsRoot, resourcesDirectoryPath;
        getSerializationData(fbsPath, resourcesDirectoryPath, fbsRoot);

        // Copy is not having any Pin for quickset, so no need to get pin from ticket and set empty string.
        dataToBeEncrypted = "";

        if (fbsPath.empty() || resourcesDirectoryPath.empty() || fbsRoot.empty())
        {
            CHECKPOINTA(
                "CopyJobServiceStandard::serializeTicketToJson: fbsPath, resourcesDirectoryPath or fbsRoot is empty.");
            jsonData = "";
            result = false;
        }
        else
        {
            CHECKPOINTA(
                "CopyJobServiceStandard::serializeTicketToJson: fbsPath - %s, resourcesDirectoryPath - %s, fbsRoot - "
                "%s",
                fbsPath.c_str(), resourcesDirectoryPath.c_str(), fbsRoot.c_str());
            const char *incDirectories[] = {resourcesDirectoryPath.c_str(), nullptr};
            jsonData = fbUtils.serializeToJson(fbsPath, fbsRoot, incDirectories, true);
            if (!jsonData.empty())
            {
                CHECKPOINTA("CopyJobServiceStandard::serializeTicketToJson: jsonData %s", jsonData.c_str());
                result = true;
            }
        }
    }
    else
    {
        CHECKPOINTA("CopyJobServiceStandard::serializeTicketToJson: Error getting ticket from cache.");
        result = false;
    }

    CHECKPOINTB("%s/JobServiceStandard::serializeTicketToJson: EXIT result - %d", getComponentInstanceName(), result);

    return result;
}

bool JobServiceStandard::deserializeJsonAndUpdateTicket(const std::string &jsonData)
{
    CHECKPOINTB("%s/JobServiceStandard::deserializeJsonAndUpdateTicket: ENTER", getComponentInstanceName());

    if (jsonData.empty())
    {
        CHECKPOINTA("CopyJobServiceStandard::deserializeJsonAndUpdateTicket: jsonData is empty");
        return false;
    }

    bool                                                               result = false;
    dune::framework::utils::FBUtils<CopyJobTicketFbT, CopyJobTicketFb> fbUtils;
    std::string                                                        fbsPath, fbsRoot, resourcesDirectoryPath;
    getSerializationData(fbsPath, resourcesDirectoryPath, fbsRoot);

    if (fbsPath.empty() || resourcesDirectoryPath.empty() || fbsRoot.empty())
    {
        CHECKPOINTA(
            "CopyJobServiceStandard::deserializeJsonAndUpdateTicket: fbsPath, resourcesDirectoryPath, or fbsRoot is "
            "empty");
        return false;
    }

    const char *incDirectories[] = {resourcesDirectoryPath.c_str(), nullptr};
    std::shared_ptr<dune::copy::Jobs::Copy::CopyJobTicketFbT> ticketFlatBuffer =
        fbUtils.deserializeToFBT(jsonData, fbsPath, fbsRoot, incDirectories);

    if (ticketFlatBuffer != nullptr)
    {
        dune::framework::data::FlatBufferDataObjectAdapter<CopyJobTicketFbT> fbAdapter{};
        dune::framework::data::SerializedDataBufferPtr                       serializedData{};
        fbAdapter.serialize(serializedData, *ticketFlatBuffer);

        std::shared_ptr<ICopyJobTicket> emptycopyJobTicket = createEmptyJobTicket();
        result = emptycopyJobTicket->deserialize(serializedData);

        if (!result)
        {
            CHECKPOINTA("CopyJobServiceStandard::deserializeJsonAndUpdateTicket: Error deserializing configuration.");
            return result;
        }

        std::shared_ptr<ICopyJobTicket> existingCopyJobTicket = getTicketFromCache(emptycopyJobTicket->getTicketId());
        if (existingCopyJobTicket)
        {
            CHECKPOINTA(
                "CopyJobServiceStandard::deserializeJsonAndUpdateTicket: Ticket already exists in cache, updating it.");
            result = existingCopyJobTicket->deserialize(serializedData);
        }
        else
        {
            CHECKPOINTA(
                "CopyJobServiceStandard::deserializeJsonAndUpdateTicket: Ticket does not exist in cache, saving it.");
            bool ticketAlreadyInCache = false;
            addTicketToCache(emptycopyJobTicket, ticketAlreadyInCache);
            persistJobTicketFromCache(emptycopyJobTicket->getTicketId().toString());
            result = true;
        }
        CHECKPOINTA("CopyJobServiceStandard::deserializeJsonAndUpdateTicket: saveDefaultJobTicket result - %d", result);
    }
    else
    {
        JobServiceFactoryLogger::checkpointDebug(
            "JobServiceFactory::deserializeJsonAndUpdateDefaultTicket: Error deserializing configuration.");
    }

    CHECKPOINTB("%s/JobServiceStandard::deserializeJsonAndUpdateTicket: EXIT", getComponentInstanceName());
    return result;
}

bool JobServiceStandard::validateAndSaveDefaultJobTicket(
    const dune::framework::data::SerializedDataBufferPtr &serializedData)
{
    CHECKPOINTC("CopyJobServiceStandard::validateAndSaveDefaultJobTicket -Entry");
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> emptyJobTicket = createEmptyJobTicket();

    bool result = emptyJobTicket->deserialize(serializedData);

    dune::job::Configuration configuration{JobSourceDestinationType::SCAN, JobSourceDestinationType::PRINT,
                                           JobType::COPY, "copy", nullptr};
    dune::job::JobTicketType jobTicketType = JobTicketType::DEFAULT;

    auto defaultCopyJobTicket = getDefaultJobTicket();

    auto jobType = emptyJobTicket->getType();
    if (result && (jobType == dune::job::JobType::COPY))
    {
        std::shared_ptr<ITicketAdapter>                                       adapter{nullptr};
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> constraintsGroup{nullptr};
        if (jobTicketResourceHelper_ != nullptr)
        {
            adapter = jobTicketResourceHelper_->createTicketAdapter(configuration, jobTicketType);
        }

        if (adapter != nullptr)
        {
            constraintsGroup = adapter->getConstraints();
        }
        if (constraintsGroup != nullptr)
        {
            {
                auto c = constraintsGroup->getConstraints("dest/print/colorMode");
                auto colormode = dune::job::cdm::mapToCdm(emptyJobTicket->getIntent()->getColorMode());
                if (c != nullptr && !c->tryValidate(&colormode))
                {
                    CHECKPOINTA(
                        "CopyJobServiceStandard::validateAndSaveDefaultJobTicket -- validation error: colorMode");
                    emptyJobTicket->getIntent()->setColorMode(defaultCopyJobTicket->getIntent()->getColorMode());
                    result = false;
                }
            }
            {
                auto c = constraintsGroup->getConstraints("dest/print/plexMode");
                auto plexMode = dune::job::cdm::mapToCdm(emptyJobTicket->getIntent()->getOutputPlexMode());
                if (c != nullptr && !c->tryValidate(&plexMode))
                {
                    CHECKPOINTA(
                        "CopyJobServiceStandard::validateAndSaveDefaultJobTicket -- validation error: plexMode");
                    emptyJobTicket->getIntent()->setOutputPlexMode(
                        defaultCopyJobTicket->getIntent()->getOutputPlexMode());
                    result = false;
                }
            }
            {
                auto c = constraintsGroup->getConstraints("src/scan/mediaSize");
                auto inputMediaSize = dune::job::cdm::mapToCdm(emptyJobTicket->getIntent()->getInputMediaSizeId());
                if (c != nullptr && !c->tryValidate(&inputMediaSize))
                {
                    CHECKPOINTA(
                        "CopyJobServiceStandard::validateAndSaveDefaultJobTicket -- validation error: inputMediaSize");
                    emptyJobTicket->getIntent()->setInputMediaSizeId(
                        defaultCopyJobTicket->getIntent()->getInputMediaSizeId());
                    result = false;
                }
            }
            {
                auto c = constraintsGroup->getConstraints("dest/print/mediaSource");
                auto mediaSource = dune::job::cdm::mapToCdm(emptyJobTicket->getIntent()->getOutputMediaSource());
                if (c != nullptr && !c->tryValidate(&mediaSource))
                {
                    CHECKPOINTA(
                        "CopyJobServiceStandard::::validateAndSaveDefaultJobTicket -- validation error: mediaSource");
                    emptyJobTicket->getIntent()->setOutputMediaSource(
                        defaultCopyJobTicket->getIntent()->getOutputMediaSource());
                    result = false;
                }
            }
        }
        else
        {
            CHECKPOINTA("CopyJobServiceStandard::::validateAndSaveDefaultJobTicket constraintsGroup is null");
        }
        result = saveDefaultJobTicket(emptyJobTicket, TicketUpdationMode::internal);
    }
    return result;
}

std::pair<ConversionResult, std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>> JobServiceStandard::checkAndPerformMigration()
{
    CHECKPOINTA("%s/CopyJobServiceStandard::checkAndPerformMigration - ENTER", instanceName_);

    std::pair<ConversionResult, std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>> result{ConversionResult::ERROR, std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>()};
    auto contextPair = systemConversionHelper_->getConversionContext("CopyDefaultTicket");

    if (contextPair.first != dune::framework::core::APIResult::OK || !contextPair.second) {
        CHECKPOINTA("CopyJobServiceStandard::checkAndPerformMigration Failed to create conversion context");
        return result;
    }

    auto files = contextPair.second->getFilesToConvert();
    
    if (files.empty())
    {
        CHECKPOINTA("StoredJobManagerStandard::checkAndPerformMigration: No files to convert");
        systemConversionHelper_->setConversionResult(result.first, contextPair.second);
        return result;
    }

    auto file = files.front();
    CHECKPOINTA_STR("CopyJobServiceStandard::checkAndPerformMigration Data migration  filename %s",
                    file.fileName_.c_str());
    
    result.second = std::make_shared<dune::cdm::jobTicket_1::JobTicketTable>();
    result.first = copyTicketConverter_->convert(file, result.second);
    
    systemConversionHelper_->setConversionResult(result.first, contextPair.second);

    CHECKPOINTA("%s/CopyJobServiceStandard::checkAndPerformMigration - EXIT", instanceName_);
    return result;
}

bool JobServiceStandard::saveDefaultJobTicket(std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> jobTicket,
                                                TicketUpdationMode mode)
{
    return dune::job::JobServiceFactory<dune::copy::Jobs::Copy::ICopyJobTicket>::saveDefaultJobTicket(jobTicket, mode);
}

bool JobServiceStandard::saveDefaultJobTicket(std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> jobTicketTable,
                                                TicketUpdationMode mode)
{
    CHECKPOINTA("%s/JobServiceStandard::saveDefaultJobTicket - ENTER", getComponentInstanceName());
    bool result = false;

    if(jobTicketTable == nullptr)
    {
        CHECKPOINTA("CopyJobServiceStandard::saveDefaultJobTicket: jobTicketTable is null");
        return result;
    }
    
    dune::job::Configuration configuration{JobSourceDestinationType::SCAN, JobSourceDestinationType::PRINT,
        JobType::COPY, "copy", nullptr};
    dune::job::JobTicketType jobTicketType = JobTicketType::DEFAULT;

    auto adapter = jobTicketResourceHelper_->createTicketAdapter(configuration, jobTicketType);
    bool isTicketModified = false;
    auto copyAdapter = std::dynamic_pointer_cast<dune::copy::Jobs::Copy::CopyTicketAdapter>(adapter);
    
    auto defaultJobTicket = getDefaultJobTicket();
    copyAdapter->deserializeFromTableWithRules(jobTicketTable, isTicketModified, true, defaultJobTicket->getIntent());
    result = adapter->saveDefaultJobTicket(mode);

    if(!result)
    {
        CHECKPOINTA("CopyJobServiceStandard::saveDefaultJobTicket: Failed to save converted ticket");
    }
    CHECKPOINTA("%s/JobServiceStandard::saveDefaultJobTicket - EXIT", getComponentInstanceName());
    return result;
}
// Test Fixtures added for Gtests

OperationResult JobServiceStandard::testImport(const OperationDescription &operationDescription,
                                               const IdentificationData &identificationData, const ContentId &contentId,
                                               const std::string &version, const FileInfoCollection &filesToImport)
{
    return importData(operationDescription, identificationData, contentId, version, filesToImport);
}

OperationResult JobServiceStandard::testExport(const OperationDescription &exportDescription,
                                               const ContentId &contentId, std::string &version,
                                               FileInfoCollection &filesToExport)
{
    return exportData(exportDescription, contentId, version, filesToExport);
}

std::shared_ptr<std::map<std::string, std::string>> JobServiceStandard::testgetJobServiceStringIds()
{
    return getJobServiceStringIds();
}

std::string JobServiceStandard::getDefaultJobName(dune::job::JobType jobType) const
{
    std::string defaultJobName = "";
    std::shared_ptr<std::map<std::string, std::string>> stringIds = getJobServiceStringIds();
    if (jobType == dune::job::JobType::COPY)
    {
        if (stringIds && stringIds->find("COPY") != stringIds->end())
        {
            defaultJobName = (*stringIds)["COPY"];
        }
    }
    return defaultJobName;
}

}}}}  // namespace dune::copy::Jobs::Copy
