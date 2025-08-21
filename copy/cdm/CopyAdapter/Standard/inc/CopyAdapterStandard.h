/* -*- c++ -*- */

#ifndef DUNE_COPY_CDM_COPY_ADAPTER_STANDARD_H
#define DUNE_COPY_CDM_COPY_ADAPTER_STANDARD_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAdapterStandard.h
 * @date   Wed, 27 Jul 2022 19:48:04 -0600
 * @brief  This is a CDM Adapter component defining the Copy Service
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyConfigurationProvider.h"
#include "IComponent.h"
#include "ICopyAdapter.h"
#include "IMicroServiceFactory.h"
#include "IDataStore.h"
#include "CopyConstraintsProvider.h"

#include "IExportImport.h"
#include "IPathDirectory.h"
#include "IPathServices.h"
#include "CopyAdapterStandardConfig_generated.h"

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_cdm_CopyAdapterStandard);

using dune::framework::core::Uuid;
using dune::framework::data::IDataStore;
using dune::ws::cdm::framework::IMicroService;
using dune::ws::cdm::framework::IMicroServiceFactory;

using APIResult       = dune::framework::core::APIResult;
using featureEnabled      = dune::cdm::glossary_1::FeatureEnabled;
using APIResult           = dune::framework::core::APIResult;
using IExportImport       = dune::framework::data::backup::IExportImport;
using OperationType       = dune::framework::data::backup::OperationType;
using BackupCategory      = dune::framework::data::backup::Category;
using IExportImport        = dune::framework::data::backup::IExportImport;
using ContentId            = dune::framework::data::backup::IExportImport::ContentId;
using IdentificationData   = dune::framework::data::backup::IExportImport::IdentificationData;
using OperationDescription = dune::framework::data::backup::IExportImport::OperationDescription;
using FileInfoCollection   = dune::framework::data::backup::IExportImport::FileInfoCollection;
using FileInfo             = dune::framework::data::backup::IExportImport::FileInfo;
using ExtendedInfo         = dune::framework::data::backup::IExportImport::FileInfo::ExtendedInfo;
using SubscriptionHandler  = dune::framework::data::backup::IExportImport::SubscriptionHandler;
using IParticipant         = dune::framework::data::backup::IExportImport::IParticipant;
using BackupOperationResult = dune::framework::data::backup::OperationResult;
using IPathDirectory       = dune::framework::storage::path::IPathDirectory;
using Category             = dune::framework::data::backup::Category;



namespace dune { namespace localization {
class ILocaleProvider;
}}


namespace dune { namespace copy { namespace cdm {
// Forward declaration.
class CopyAdapterStandardUwAdapter;

/**
 * Implementation of the Standard flavor of the CopyAdapter component.
 */
class CopyAdapterStandard : public dune::framework::component::IComponent, public ICopyAdapter,
                            protected dune::framework::data::backup::IExportImport::IParticipant
{
public:
    /**
     * @name ICopyAdapter methods.
     * @{
     */

    /// @todo redeclare methods from ICopyAdapter here (don't forget the 'override' clause).

    /**
     * @}
     */

    /**
     * @brief CopyAdapterStandard Constructor.
     *
     * @param instanceName the name of the component instance.
     */
    explicit CopyAdapterStandard(const char *instanceName);

    /**
     * Destructor.
     */
    virtual ~CopyAdapterStandard();

    /**
     * @name IComponent methods.
     * @{
     */

    dune::framework::component::ComponentFlavorUid getComponentFlavorUid() const override;
    const char                                    *getComponentInstanceName() const override;
    void  initialize(WorkingMode mode, const dune::framework::component::SystemServices *services) override;
    void *getInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName) override;
    void  setInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName,
                       void *interfacePtr) override;
    void  connected(dune::framework::component::IComponentManager *componentManager,
                    std::future<void>                             &asyncCompletion) override;
    void  shutdown(ShutdownCause cause, std::future<void> &asyncCompletion) override;

    /**
     * @}
     */
    bool getCopyEnabled() override;
    void setCopyEnabled(dune::cdm::glossary_1::FeatureEnabled value) override;

    bool getColorCopyEnabled() override;
    void setColorCopyEnabled(dune::cdm::glossary_1::FeatureEnabled value) override;

    /**
     * @brief Get the Copy Mode
     * 
     * @return The current copy mode
     */
    dune::cdm::copy_1::configuration::CopyMode getCopyMode() override;

    /**
     * @brief Set the Copy Mode
     * 
     * @param value Copy mode type
     */
    void setCopyMode(dune::cdm::copy_1::configuration::CopyMode value) override;

    /**
     * @brief Get the Interrupt Mode object
     * @return featureEnabled current interrupt mode
     */
    dune::cdm::glossary_1::FeatureEnabled getInterruptMode() override;

    /**
     * @brief Set the Interrupt Mode object     
     * @param value cdm boolean to change mode
     */
    void setInterruptMode(dune::cdm::glossary_1::FeatureEnabled value) override;   

	/**
	 * @brief Get the Copy Adapter Data Change Event object
	 * @return ICopyAdapterDataChangeEvent& event to subscribe to changes in settings in adapter
	 */
    ICopyAdapterDataChangeEvent& getCopyAdapterDataChangeEvent() override;

    BackupOperationResult exportData(const OperationDescription & exportDescription,
                               const ContentId            & contentId,
                               std::string                & version,
                               FileInfoCollection         & filesToExport);
    
    BackupOperationResult importData(const OperationDescription& importDescription,
                               const IdentificationData& identificationData,
                               const ContentId& contentId,
                               const std::string& version,
                               const FileInfoCollection& filesToImport);

    /**
     * @brief Method to check if reset is needed
     */
    void checkIfResetDataIsNeeded();
    
  private:
  
    /**
     * @brief Write to data store
     * @return bool
     */
    bool writeCopyConfigurationToDataStore(void);
    /**
     * @brief Read from dataStore
     * @return bool 
     */
    bool readCopyConfigurationFromDataStore(void);

    /**
     * @brief Loads the configuration for this component instance
     *
     * @param configurationService the pointer to the system's configuration service
     * @return the configuration values to be used by this instance, according to the system's product and proto
     *         versions or nullptr if the configuration is not available for this instance.
     */
    std::unique_ptr<CopyAdapterStandardConfigT> getConfiguration(
        dune::framework::resources::IConfigurationService* configurationService) const;

    IMicroServiceFactory                      			*microServiceFactory_{nullptr};  ///< MicroService registration interface
    IDataStore                                			*dataStore_{nullptr};
    std::weak_ptr<IMicroService>               			copySvc_;  ///< MicroService handler obtained from factory
    std::shared_ptr<CopyConfigurationProvider> 			copyConfigurationProvider_;
    std::string convertConfigurationToJson(const std::shared_ptr<dune::cdm::copy_1::ConfigurationT>& configuration);
    void writeJsonToFile(const std::string& jsonData, const std::string& filePath);

    std::shared_ptr<dune::cdm::copy_1::ConfigurationT> convertJsonToConfiguration(const std::string& jsonData);
    std::string readJsonFromFile(const std::string& filePath);

    const char *instanceName_;  ///< The instance name.

    dune::framework::underware::InterpreterEnvironment 	*interpreterEnvironment_;  ///< The environment where underwares are to be registered
    dune::copy::cdm::CopyAdapterStandardUwAdapter 		*uwAdapter_;  ///< The underware object adapter.

    std::shared_ptr<dune::cdm::copy_1::ConfigurationT>  orgConfigurations_{std::make_shared<dune::cdm::copy_1::ConfigurationT>()};
    dune::framework::data::ObjectClassification         dataClassification_{1, 0x3f5445, 1, 0};
    dune::framework::core::Uuid                         copyConfigurationUuid_{Uuid("24eb349c-11ec-11ed-861d-0242ac120002")};
    std::unique_ptr<CopyAdapterStandardConfigT>         configuration_; // The instance's constants configuration
    IExportImport*                                      exportImportManager_{nullptr};
    std::unique_ptr<SubscriptionHandler>                subscriptionHandlerBackupRestore_{nullptr};
    std::unique_ptr<SubscriptionHandler>                subscriptionHandlerExportImport_{nullptr};
    const std::string                                   contentId_ = "CopyEnableSettings";
    dune::framework::storage::path::IPathDirectory*     pathDirectory_{nullptr};

    dune::framework::core::event::EventSource<CopyConfigurationEventType> copyAdapterDataChangeEventSource_;
    std::shared_ptr<CopyConfigurationConstraintsProvider> copyConfigurationConstraintsProvider_{nullptr};
    dune::localization::ILocaleProvider *localeProvider_{nullptr};
    const dune::framework::component::SystemServices* systemServices_{nullptr};

};

}}}  // namespace dune::copy::cdm

DEFINE_MODULE_UID(dune::copy::cdm::CopyAdapterStandard, 0x3f5445);

DESCRIBE_COMPONENT_FLAVOR_BEGIN(dune::copy::cdm::CopyAdapterStandard)
PROVIDES_INTERFACE(dune::copy::cdm::ICopyAdapter)
REQUIRES_INTERFACE(dune::ws::cdm::framework::IMicroServiceFactory)
REQUIRES_INTERFACE(dune::localization::ILocaleProvider)
REQUIRES_INTERFACE(dune::framework::data::backup::IExportImport)
DESCRIBE_COMPONENT_FLAVOR_END(dune::copy::cdm::CopyAdapterStandard)

#endif  // DUNE_COPY_CDM_COPY_ADAPTER_STANDARD_H
