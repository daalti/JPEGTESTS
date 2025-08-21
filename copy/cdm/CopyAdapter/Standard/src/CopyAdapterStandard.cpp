/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAdapterStandard.cpp
 * @date   Wed, 27 Jul 2022 19:48:04 -0600
 * @brief  This is a CDM Adapter component defining the Copy Service
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyAdapterStandard.h"
#include <jansson.h>
#include "nlohmann/json.hpp"
#include "common_debug.h"
#include <fstream>

#include "CopyAdapterStandard_TraceAutogen.h"

#include "CopyAdapterStandardUwAdapter.h"
#include "ErrorManager.h"
#include "IPathDirectory.h"
#include "com.hp.cdm.service.copy.version.1_generated.h"
#include "ILocaleProvider.h"
#include "IResetManager.h"

using dune::framework::data::SerializedDataBuffer;
using FeatureEnabled = dune::cdm::glossary_1::FeatureEnabled;
using dune::localization::ILocaleProvider;

static constexpr const char *_VERSION_ = "1.0";
// Factory method

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_cdm_CopyAdapterStandard)
{
    dune::copy::cdm::CopyAdapterStandard *instance = new dune::copy::cdm::CopyAdapterStandard(instanceName);
    assert(instance != nullptr);
    return static_cast<dune::framework::component::IComponent *>(instance);
}

dune::cdm::copy_1::configuration::CopyMode mapToCdm(dune::copy::cdm::CopyMode value)
{
    // Not many products use this feature, most of them are undefined.
    if(value == dune::copy::cdm::CopyMode::PRINT_AFTER_SCANNING)
    {
        return dune::cdm::copy_1::configuration::CopyMode::printAfterScanning; 
    }
    else if(value == dune::copy::cdm::CopyMode::PRINT_WHILE_SCANNING)
    {
        return dune::cdm::copy_1::configuration::CopyMode::printWhileScanning;
    }
    else
    {
        return dune::cdm::copy_1::configuration::CopyMode::_undefined_;
    }
}

namespace dune { namespace copy { namespace cdm {

// Constructor and destructor

CopyAdapterStandard::CopyAdapterStandard(const char *instanceName)
    : instanceName_(instanceName), interpreterEnvironment_(nullptr), uwAdapter_(nullptr)
{
    CHECKPOINTC("%s/CopyAdapterStandard: constructed", instanceName_);
}

CopyAdapterStandard::~CopyAdapterStandard()
{
    if (uwAdapter_ != nullptr)
    {
        delete uwAdapter_;
    }
}

// IComponent methods.

dune::framework::component::ComponentFlavorUid CopyAdapterStandard::getComponentFlavorUid() const
{
    return GET_MODULE_UID(CopyAdapterStandard);
}

const char *CopyAdapterStandard::getComponentInstanceName() const
{
    return instanceName_;
}

void CopyAdapterStandard::initialize(WorkingMode mode, const dune::framework::component::SystemServices *services)
{
    DUNE_UNUSED(mode);

    systemServices_ = services;
    interpreterEnvironment_ = services->interpreterEnvironment_;

    if ( services->configurationService_ != nullptr )
    {
        configuration_ = getConfiguration(services->configurationService_);
    }

    if(nullptr != services->pathServices_)
    {
        pathDirectory_ = services->pathServices_->getPathDirectory();
    }

    CHECKPOINTC("%s/CopyAdapterStandard: initialized", instanceName_);
}

void *CopyAdapterStandard::getInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName)
{
    DUNE_UNUSED(portName);
    void *interfacePtr = nullptr;
    if (interfaceUid == GET_INTERFACE_UID(ICopyAdapter))
    {
        interfacePtr = static_cast<ICopyAdapter *>(this);
    }
    CHECKPOINTC("%s/CopyAdapterStandard: getInterface %" PRIu32 " from port %s with addr %p", instanceName_,
                interfaceUid, portName, interfacePtr);
    return interfacePtr;
}

void CopyAdapterStandard::setInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName,
                                       void *interfacePtr)
{
    DUNE_UNUSED(interfacePtr);
    CHECKPOINTC("%s/CopyAdapterStandard: setInterface %" PRIu32 " to port %s with addr %p", instanceName_, interfaceUid,
                portName, interfacePtr);
    if (interfacePtr != nullptr)
    {
        if (interfaceUid == GET_INTERFACE_UID(IMicroServiceFactory))
        {
            CHECKPOINTC("%s/CopyAdapterStandard: setInterface IMicroServiceFactory to port %s with addr %p",
                        instanceName_, portName, interfacePtr);
            microServiceFactory_ = static_cast<IMicroServiceFactory *>(interfacePtr);
        }

        if (interfaceUid == GET_INTERFACE_UID(IDataStore))
        {
            CHECKPOINTC("%s/CopyAdapterStandard: setInterface IDataStore to port %s with addr %p",
                        instanceName_, portName, interfacePtr);
            dataStore_ = static_cast<IDataStore *>(interfacePtr);
        }

        if (interfaceUid == GET_INTERFACE_UID(ILocaleProvider))
        {
            CHECKPOINTC("%s/CopyAdapterStandard: setInterface ILocaleProvider to port %s with addr %p", instanceName_,
                            portName, interfacePtr);
            localeProvider_ = static_cast<ILocaleProvider *>(interfacePtr);
        }
        
        if(interfaceUid == GET_INTERFACE_UID(dune::framework::data::backup::IExportImport))
        {
            exportImportManager_ = static_cast <dune::framework::data::backup::IExportImport *>(interfacePtr);        
            CHECKPOINTA("%s/CopyAdapterStandard: setInterface IExportImport to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
    }
}

std::unique_ptr<CopyAdapterStandardConfigT> CopyAdapterStandard::getConfiguration(
    dune::framework::resources::IConfigurationService *configurationService) const
{
    CHECKPOINTC("CopyAdapterStandard:getConfiguration - Entry");

    assert(configurationService != nullptr);
    dune::framework::resources::IConfigurationService::ConfigurationRawData rawConfiguration =
        configurationService->getConfiguration(GET_MODULE_UID(dune::copy::cdm::CopyAdapterStandard), "CopyAdapter");

    if (rawConfiguration.data && (rawConfiguration.size > 0))
    {
        CHECKPOINTC("CopyAdapterStandard:getConfiguration rawConfiguration has data");
        flatbuffers::Verifier verifier(rawConfiguration.data.get(), rawConfiguration.size);
        assert(VerifyCopyAdapterStandardConfigBuffer(verifier));
        return UnPackCopyAdapterStandardConfig(rawConfiguration.data.get());
    }
    else
    {
        CHECKPOINTA("CopyAdapterStandard:getConfiguration: failed to configure <data=%p>, <size=%u>",
                    rawConfiguration.data.get(), rawConfiguration.size);
        return std::unique_ptr<CopyAdapterStandardConfigT>();
    }
}

void CopyAdapterStandard::connected(dune::framework::component::IComponentManager *componentManager,
                                    std::future<void>                             &asyncCompletion)
{
    DUNE_UNUSED(componentManager);
    DUNE_UNUSED(asyncCompletion);

    // Initialize the underware adapter.
    if (interpreterEnvironment_ != nullptr)
    {
        uwAdapter_ = new CopyAdapterStandardUwAdapter(interpreterEnvironment_, instanceName_, this);
    }

    CHECKPOINTC("%s/CopyAdapterStandard: connected", instanceName_);

    assert_msg(microServiceFactory_ != nullptr, "MicroServiceFactory not connected in graph");
    if (microServiceFactory_)
    {
        // Register the Copy MicroService
        copySvc_ = microServiceFactory_->createMicroService(dune::cdm::copy_1::Definition());
        if (copySvc_.expired())
        {
            CHECKPOINTA("CopyAdapterStandard::connected: unable to createMicroService");
            assert(0);
        }
        else
        {
            auto svc = copySvc_.lock();
            if (svc)
            {
                // Register the Configuration provider: /cdm/copy/v1/configuration
                copyConfigurationProvider_ = std::make_shared<CopyConfigurationProvider>(this);
                dune::cdm::copy_1::configuration::Definition tempConfigurationDef;
                IMicroService::RegistrationResult            result =
                    svc->registerResourceProvider(tempConfigurationDef, copyConfigurationProvider_);
                if (result != IMicroService::RegistrationResult::SUCCESS)
                {
                    CHECKPOINTA("CopyAdapterStandard::connected: unable to registerResourceProvider %d",
                                static_cast<uint32_t>(result));
                    assert(0);
                }

                //Crete and registrer copy configuration constraints provider
                copyConfigurationConstraintsProvider_ = std::make_shared<CopyConfigurationConstraintsProvider>(this, localeProvider_, configuration_->constraintsStringIds);
                dune::cdm::copy_1::configurationConstraints::Definition tempScanConstraintsDef;
                result = svc->registerResourceProvider(tempScanConstraintsDef, copyConfigurationConstraintsProvider_);
                if (result != IMicroService::RegistrationResult::SUCCESS)
                {
                    CHECKPOINTA("CopyAdapterStandard::connected: unable to registerResourceProvider for  scan configuration constraints result = %d", static_cast<uint32_t>(result));
                    assert(0);
                }
            }

            if(exportImportManager_ != nullptr)
            {
                subscriptionHandlerBackupRestore_ = exportImportManager_->subscribeParticipant(OperationType::BACKUP_RESTORE,
                                                                                    BackupCategory::CopySettings,
                                                                                    contentId_,
                                                                                    static_cast<IExportImport::IParticipant*>(this));
                
                subscriptionHandlerExportImport_ = exportImportManager_->subscribeParticipant(  OperationType::EXPORT_IMPORT,
                                                                                    BackupCategory::CopySettings,
                                                                                    contentId_,
                                                                                    static_cast<IExportImport::IParticipant*>(this));
            }
        }
    }
    else
    {
        CHECKPOINTA("CopyAdapterStandard::connected: microServiceFactory_ is nullptr");
        assert(0);
    }

    if (dataStore_ && !readCopyConfigurationFromDataStore())
    {
        CHECKPOINTA("CopyAdapterStandard:connected: no data found in DataStore");
    }

    checkIfResetDataIsNeeded();
}

void CopyAdapterStandard::shutdown(ShutdownCause cause, std::future<void> &asyncCompletion)
{
    DUNE_UNUSED(cause);
    DUNE_UNUSED(asyncCompletion);
    CHECKPOINTC("%s/CopyAdapterStandard: shutdown", instanceName_);
}

/// @todo implement methods from ICopyAdapter here.

bool CopyAdapterStandard::getCopyEnabled()
{
    CHECKPOINTC("CopyAdapterStandard::getCopyEnabled value : %d", (int)orgConfigurations_->copyEnabled);
    switch (orgConfigurations_->copyEnabled)
    {
        case FeatureEnabled::true_:
            return true;
        case FeatureEnabled::false_:
            return false;
        case FeatureEnabled::_undefined_:
        default:
            // default value is true
            return true;
    }
}

void CopyAdapterStandard::setCopyEnabled(FeatureEnabled value)
{
    CHECKPOINTB("CopyAdapterStandard::setCopyEnabled value : %d", (int)value);

    orgConfigurations_->copyEnabled = value;
    writeCopyConfigurationToDataStore();
    copyAdapterDataChangeEventSource_.fireSync(CopyConfigurationEventType::COPY_ENABLE_STATE_CHANGE);
}

bool CopyAdapterStandard::getColorCopyEnabled()
{
    CHECKPOINTC("CopyAdapterStandard::getColorCopyEnabled value : %d", (int)orgConfigurations_->colorCopyEnabled);
    switch (orgConfigurations_->colorCopyEnabled)
    {
        case FeatureEnabled::true_:
            return true;
        case FeatureEnabled::false_:
            return false;
        case FeatureEnabled::_undefined_:
        default:
            // default value is true
            return true;
    }
}

void CopyAdapterStandard::setColorCopyEnabled(FeatureEnabled value)
{
    CHECKPOINTB("CopyAdapterStandard::setColorCopyEnabled value : %d", (int)value);

    orgConfigurations_->colorCopyEnabled = value;
    writeCopyConfigurationToDataStore();
    copyAdapterDataChangeEventSource_.fireSync(CopyConfigurationEventType::COLOR_COPY_ENABLE_STATE_CHANGE);
}

dune::cdm::copy_1::configuration::CopyMode CopyAdapterStandard::getCopyMode()
{
    CHECKPOINTC("CopyAdapterStandard::getCopyMode value : %d", (int)orgConfigurations_->copyMode);
    return orgConfigurations_->copyMode;
}

void CopyAdapterStandard::setCopyMode(dune::cdm::copy_1::configuration::CopyMode value)
{
    CHECKPOINTB("CopyAdapterStandard::setCopyMode value : %d", (int)value);
    if(orgConfigurations_->copyMode != value && value != dune::cdm::copy_1::configuration::CopyMode::_undefined_)
    {
        orgConfigurations_->copyMode = value;
        writeCopyConfigurationToDataStore();
        copyAdapterDataChangeEventSource_.fireSync(CopyConfigurationEventType::COPY_MODE);

        if(orgConfigurations_->allowInterrupt != FeatureEnabled::_undefined_)
        {
            if(orgConfigurations_->copyMode == dune::cdm::copy_1::configuration::CopyMode::printAfterScanning)
            {
                CHECKPOINTC("CopyAdapterStandard::setCopyMode: printAfterScanning -> forcing interrupt to false");
                setInterruptMode(FeatureEnabled::false_);
            }
            else if(orgConfigurations_->copyMode == dune::cdm::copy_1::configuration::CopyMode::printWhileScanning)
            {
                CHECKPOINTC("CopyAdapterStandard::setCopyMode: printWhileScanning -> forcing interrupt to true");
                setInterruptMode(FeatureEnabled::true_);
            }
        }
    }
}

FeatureEnabled CopyAdapterStandard::getInterruptMode()
{
    CHECKPOINTC("CopyAdapterStandard::getInterruptMode value : %d", (int)orgConfigurations_->allowInterrupt);
    return orgConfigurations_->allowInterrupt;
}

void CopyAdapterStandard::setInterruptMode(FeatureEnabled value)
{
    CHECKPOINTB("CopyAdapterStandard::setInterruptMode value : %d", (int)value);

    orgConfigurations_->allowInterrupt = value;
    writeCopyConfigurationToDataStore();
    copyAdapterDataChangeEventSource_.fireSync(CopyConfigurationEventType::COPY_INTERRUPT_MODE);
}

bool CopyAdapterStandard::writeCopyConfigurationToDataStore()
{
    CHECKPOINTC("CopyAdapterStandard::writeCopyConfigurationToDataStore");

    if (dataStore_ == nullptr)
    {
        CHECKPOINTA("CopyAdapterStandard::writeCopyConfigurationToDataStore: Exit[dataStore_ is NULL]");
        return false;
    }

    flatbuffers::FlatBufferBuilder dataFbb;
    dataFbb.Finish(CreateConfiguration(dataFbb, orgConfigurations_.get()));
    SerializedDataBuffer saveData(dataFbb.GetBufferPointer(), dataFbb.GetSize());

    bool result = dataStore_->insert_or_replace(saveData, copyConfigurationUuid_, dataClassification_);

    CHECKPOINTB("CopyAdapterStandard::writeCopyConfigurationToDataStore: Exit - result: %d", result);
    return result;
}

bool CopyAdapterStandard::readCopyConfigurationFromDataStore()
{
    CHECKPOINTC("CopyAdapterStandard::readCopyConfigurationFromDataStore");
    bool result{false};

    if (dataStore_ == nullptr)
    {
        CHECKPOINTA("CopyAdapterStandard::readCopyConfigurationFromDataStore: Exit[dataStore_ is NULL]");
        return result;
    }

    auto found = dataStore_->find(copyConfigurationUuid_);
    if (found.first)
    {
        auto readConfiguration = std::make_shared<dune::cdm::copy_1::ConfigurationT>();
        flatbuffers::Verifier verifierGen(found.second.buffer.first.get(), found.second.buffer.second);
        auto readData = flatbuffers::GetRoot<dune::cdm::copy_1::Configuration>(found.second.buffer.first.get());
        if (readData && readData->Verify(verifierGen))
        {
            readData->UnPackTo(readConfiguration.get());
            orgConfigurations_->copyEnabled      = readConfiguration->copyEnabled;
            orgConfigurations_->colorCopyEnabled = readConfiguration->colorCopyEnabled;
            orgConfigurations_->copyMode         = readConfiguration->copyMode;
            orgConfigurations_->allowInterrupt   = readConfiguration->allowInterrupt;
            result = true;

            CHECKPOINTB("CopyAdapterStandard::readCopyConfigurationFromDataStor: result %d", found.first);
        }
        else
        {
            CHECKPOINTA("CopyAdapterStandard::readCopyConfigurationFromDataStor: Error[Persisted config failed verification]");
        }
    }
    else
    {
        CHECKPOINTA("CopyAdapterStandard::readCopyConfigurationFromDataStore: Error[Not matched uuid]");
    }

    // default value
    if (orgConfigurations_->copyEnabled == FeatureEnabled::_undefined_)
    {
        CHECKPOINTA("CopyAdapterStandard::readCopyConfigurationFromDataStore: Set Default Value for copyEnabled");
        orgConfigurations_->copyEnabled = FeatureEnabled::true_;
    }
    if (orgConfigurations_->colorCopyEnabled == FeatureEnabled::_undefined_)
    {
        CHECKPOINTA("CopyAdapterStandard::readCopyConfigurationFromDataStore: Set Default Value for colorCopyEnabled");
        orgConfigurations_->colorCopyEnabled = FeatureEnabled::true_;
    }
    if (orgConfigurations_->copyMode == dune::cdm::copy_1::configuration::CopyMode::_undefined_)
    {
        CHECKPOINTA("CopyAdapterStandard::readCopyConfigurationFromDataStore: Set Default Value for copyMode");
        orgConfigurations_->copyMode = mapToCdm(configuration_->defaultCopyMode);
    }
    if (orgConfigurations_->allowInterrupt == FeatureEnabled::_undefined_ && configuration_->allowInterrupt)
    {
        CHECKPOINTA("CopyAdapterStandard::readCopyConfigurationFromDataStore: Set Default Value based in copy mode for interrupt mode");
        orgConfigurations_->allowInterrupt = (orgConfigurations_->copyMode == dune::cdm::copy_1::configuration::CopyMode::printWhileScanning)
            ? FeatureEnabled::true_ : FeatureEnabled::false_;
    }


    CHECKPOINTB("CopyAdapterStandard::readCopyConfigurationFromDataStore: Exit - result: %d", result);
    return result;
}

ICopyAdapterDataChangeEvent& CopyAdapterStandard::getCopyAdapterDataChangeEvent()
{
    return copyAdapterDataChangeEventSource_;
}


BackupOperationResult CopyAdapterStandard::exportData(const OperationDescription& exportDescription,
                                                     const ContentId& contentId,
                                                     std::string& version,
                                                     FileInfoCollection& filesToExport)
{
    CHECKPOINTC("CopyAdapterStandard::exportData: Entry");

    // This is the version of the data that we are exporting
    version = _VERSION_;

    if (contentId != "CopyEnableSettings")
    {
        CHECKPOINTA_STR("CopyAdapterStandard::exportData: ERROR: Invalid content id: %s", contentId.c_str());
        return BackupOperationResult::ERROR_UNKNOWN_CONTENTID;
    }

    if (contentId == contentId_)
    {
        // Read the configuration
        auto readConfiguration = std::make_shared<dune::cdm::copy_1::ConfigurationT>();
        readConfiguration->copyEnabled = orgConfigurations_->copyEnabled;
        readConfiguration->colorCopyEnabled = orgConfigurations_->colorCopyEnabled;
        readConfiguration->copyMode = orgConfigurations_->copyMode;

        // Convert the configuration to JSON
        std::string jsonData = convertConfigurationToJson(readConfiguration);

        // Create a temporary file path
        std::string filePath = pathDirectory_->createTempFile();

        // Write the JSON data to the file
        writeJsonToFile(jsonData, filePath);
        // Add the file to the list of files to export
        IExportImport::FileInfo fileInfo;
        fileInfo.tag = contentId;
        fileInfo.path = filePath;
        fileInfo.encrypt = false; // as it does not contain secrets
        fileInfo.disposable = true;
        filesToExport.push_back(fileInfo);

        CHECKPOINTB("CopyAdapterStandard::exportData: Exit - result: %d", BackupOperationResult::SUCCESS);
        return BackupOperationResult::SUCCESS;
    }

    CHECKPOINTA("CopyAdapterStandard::exportData: Error[Not matched contentId]");
    return BackupOperationResult::ERROR_UNKNOWN_CONTENTID;
}

std::string CopyAdapterStandard::convertConfigurationToJson(const std::shared_ptr<dune::cdm::copy_1::ConfigurationT>& configuration)
{
    // Convert the configuration to JSON using your preferred JSON library
    nlohmann::json jsonConfig;
    jsonConfig["copyEnabled"] = configuration->copyEnabled;
    jsonConfig["colorCopyEnabled"] = configuration->colorCopyEnabled;
    jsonConfig["copyMode"] = configuration->copyMode;

    return jsonConfig.dump();
}

void CopyAdapterStandard::writeJsonToFile(const std::string& jsonData, const std::string& filePath)
{
    // Write the JSON data to the file
    std::ofstream file(filePath, std::ios::out | std::ios::binary);
    if (file.is_open())
    {
        file << jsonData;
        file.close();
    }
    else
    {
        CHECKPOINTA("CopyAdapterStandard::writeJsonToFile: Error[Failed to open file]");
    }
}
  
BackupOperationResult CopyAdapterStandard::importData(const OperationDescription& importDescription,
                            const IdentificationData& identificationData,
                            const ContentId& contentId,
                            const std::string& version,
                            const FileInfoCollection& filesToImport)
{
    CHECKPOINTC("CopyAdapterStandard::importData: Entry");
    BackupOperationResult result = BackupOperationResult::ERROR;

    if (contentId == contentId_)
    {
        if (version == _VERSION_)
        {
            for (const FileInfo& fileInfo : filesToImport)
            {
                if (fileInfo.tag == contentId)
                {
                    CHECKPOINTA("CopyAdapterStandard::importData: -- Sucess");
                    // Read the JSON data from the file
                    std::string jsonData = readJsonFromFile(fileInfo.path);

                    // Convert the JSON data to configuration
                    std::shared_ptr<dune::cdm::copy_1::ConfigurationT> configuration = convertJsonToConfiguration(jsonData);

                    setCopyEnabled(configuration->copyEnabled);
                    setColorCopyEnabled(configuration->colorCopyEnabled);
                    setCopyMode(configuration->copyMode);

                    result = BackupOperationResult::SUCCESS;
                    break;
                }
                else 
                {
                    CHECKPOINTA("CopyAdapterStandard::importData: Error[Not matched tag]");
                }
            }

            if (result == BackupOperationResult::SUCCESS)
                return BackupOperationResult::SUCCESS;
        }
    }

    CHECKPOINTA("CopyAdapterStandard::importData: Error[Not matched contentId or version]");
    return BackupOperationResult::ERROR_UNKNOWN_CONTENTID;
}

void CopyAdapterStandard::checkIfResetDataIsNeeded()
{
    if(systemServices_ && systemServices_->resetManager_)
    {
        dune::framework::data::resets::ResetLevel resetLevel = systemServices_->resetManager_->getCurrentLevel();

        CHECKPOINTA("CopyAdapterStandard::connected resetLevel = %d", static_cast<int>(resetLevel));

        if ((resetLevel == dune::framework::data::resets::ResetLevel::USER_SETTINGS_RESET) ||
            (resetLevel == dune::framework::data::resets::ResetLevel::USER_DATA_RESET) ||
            (resetLevel == dune::framework::data::resets::ResetLevel::FACTORY_DATA_RESET) ||
            (resetLevel == dune::framework::data::resets::ResetLevel::FULL_FACTORY_DATA_RESET))
        {
            // Only reset when value was defined. Undefined values not need to be reset.
            if (orgConfigurations_->copyMode != dune::cdm::copy_1::configuration::CopyMode::_undefined_)
            {
                CHECKPOINTA("CopyAdapterStandard::connected resetLevel: Set Default Value for copyMode");
                orgConfigurations_->copyMode = mapToCdm(configuration_->defaultCopyMode);
            }
            if (orgConfigurations_->allowInterrupt != FeatureEnabled::_undefined_ && configuration_->allowInterrupt)
            {
                CHECKPOINTA("CopyAdapterStandard::readCopyConfigurationFromDataStore: Set Default Value based in copy mode for interrupt mode");
                orgConfigurations_->allowInterrupt = (orgConfigurations_->copyMode == dune::cdm::copy_1::configuration::CopyMode::printWhileScanning)
                    ? FeatureEnabled::true_ : FeatureEnabled::false_;
            }

            // Force write to data store to ensure that last data after read and check reset is ok
            writeCopyConfigurationToDataStore();
        }
    }
}

std::string CopyAdapterStandard::readJsonFromFile(const std::string& filePath)
{
    // Read the JSON data from the file
    std::ifstream file(filePath,std::ios::in | std::ios::binary);
    std::string jsonData;

    if (file.is_open())
    {
        std::stringstream buffer;
        buffer << file.rdbuf();
        jsonData = buffer.str();
        file.close();
    }
    else
    {
        CHECKPOINTA("CopyAdapterStandard::readJsonFromFile: Error[Failed to open file]");
    }

    return jsonData;
}

std::shared_ptr<dune::cdm::copy_1::ConfigurationT> CopyAdapterStandard::convertJsonToConfiguration(const std::string& jsonData)
{
    nlohmann::json jsonConfig = nlohmann::json::parse(jsonData);

    std::shared_ptr<dune::cdm::copy_1::ConfigurationT> configuration = std::make_shared<dune::cdm::copy_1::ConfigurationT>();
    configuration->copyEnabled = jsonConfig["copyEnabled"];
    configuration->colorCopyEnabled = jsonConfig["colorCopyEnabled"];
    configuration->copyMode = jsonConfig["copyMode"];
    return configuration;
}


}}}  // namespace dune::copy::cdm
