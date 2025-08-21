/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_JOB_SERVICE_STANDARD_H
#define DUNE_COPY_JOBS_COPY_JOB_SERVICE_STANDARD_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobServiceStandard.h
 * @date   Wed, 08 May 2019 06:49:55 -0700
 * @brief  JobService specific class to CopyJobs
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "gtest/gtest_prod.h"

#include "IComponent.h"
#include "ICopyJobService.h"
#include "ICopyPipeline.h"
#include "IExportImport.h"
#include "IJobDetailsManager.h"
#include "IJobManagerAlertProvider.h"
#include "IMediaInfoPageBased.h"
#include "IScanConstraints.h"
#include "ISystemConversionHelper.h"
#include "ICopyTicketConverter.h"
#include "JobFrameworkTypes.h"
#include "JobServiceStandardConfig_generated.h"
#include "JobTicketResourceHelper.h"
#include "SettingsTypes.h"
#include "IConnector.h"
#include "IColorAccessControl.h"
#include "IScanPipeline.h"
// #include "SystemConversionHelperJoltToDune.h"

#include <tuple>
#include <mutex>
#include <condition_variable>
#include <memory>

#include "com.hp.cdm.service.shortcut.version.1.sharedTypes.shortcut_generated.h"

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_Jobs_Copy_JobServiceStandard);

// Forward declarations
namespace dune { namespace imaging {
class IPipelineMemoryClientCreator;
}}  // namespace dune::imaging

namespace dune { namespace print { namespace engine {
class IPrintIntentsFactory;
class ISettings;
class IPrint;
class ICapabilitiesFactory;
}}}  // namespace dune::print::engine

namespace dune { namespace job {
class IIntentsManager;
}}  // namespace dune::job

namespace dune { namespace print { namespace engine { namespace helpers {
class IPrintIntentsFactory;
}}}}  // namespace dune::print::engine::helpers

namespace dune { namespace localization {
class ILocaleProvider;
}}  // namespace dune::localization

namespace dune { namespace admin { namespace shortcuts {
struct FactoryShortuctDefT;
}}}  // namespace dune::admin::shortcuts

namespace dune { namespace scan { namespace scanningsystem {
class IStatus;
}}}  // namespace dune::scan::scanningsystem

namespace dune { namespace copy { namespace Jobs { namespace Copy {

using dune::job::SegmentType;
using IExportImport = dune::framework::data::backup::IExportImport;
using IParticipant = dune::framework::data::backup::IExportImport::IParticipant;
using OperationResult = dune::framework::data::backup::OperationResult;
using IdentificationData = dune::framework::data::backup::IExportImport::IdentificationData;
using OperationDescription = dune::framework::data::backup::IExportImport::OperationDescription;
using ContentId = dune::framework::data::backup::IExportImport::ContentId;
using FileInfoCollection = dune::framework::data::backup::IExportImport::FileInfoCollection;
using FileInfo = dune::framework::data::backup::IExportImport::FileInfo;
using Category = dune::framework::data::backup::Category;
using OperationType = dune::framework::data::backup::OperationType;
using SubscriptionHandler = dune::framework::data::backup::IExportImport::SubscriptionHandler;
using MediaPropertyChangedEventArgs = dune::print::engine::pageBased::MediaPropertyChangedEventArgs;
using ISystemConversionHelper = dune::framework::data::conversion::ISystemConversionHelper;
using ICopyTicketConverter = dune::copy::Jobs::Copy::ICopyTicketConverter;

// Forward declarations
class JobServiceStandardUwAdapter;
struct CopyQuicksetFbT;

/**
 * Implementation of the Standard flavor of the JobService component.
 */
class JobServiceStandard : public dune::framework::component::IComponent,
                           public dune::job::JobServiceFactory<dune::copy::Jobs::Copy::ICopyJobTicket>,
                           protected dune::framework::data::backup::IExportImport::IParticipant
{
  public:
    friend class JobServiceStandardUwAdapter;
    /**
     * @name IJobService methods.
     * @{
     */
    /**
     * @brief getJobConstraintsHelper. Function to get the component to
     * generate the constraints.
     *
     * @return pointer to the component instance to manage constraints.
     */
    inline dune::copy::Jobs::Copy::IJobConstraints *getJobConstraintsHelper(void) const
    {
        return jobConstraintsHelper_;
    }

    virtual std::shared_ptr<dune::job::IPipelineBuilder> createPipelineBuilder(
        std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> jobTicket) override;

    virtual std::shared_ptr<dune::job::IPromptController> createPromptController(
        std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> jobTicket) override;

    virtual bool isPrintService() override;

    virtual std::map<dune::job::JobType, dune::security::ac::Permission> getJobCreationPermissions() override;

    /**
     * @}
     */

    /**
     * @brief JobServiceStandard Constructor.
     *
     * @param instanceName the name of the component instance.
     */
    explicit JobServiceStandard(const char *instanceName);

    /**
     * Destructor.
     */
    virtual ~JobServiceStandard();

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

    /**
     * @brief Loads the configuration for this component instance
     *
     * @param configurationService the pointer to the system's configuration service
     * @return the configuration values to be used by this instance, according to the system's product and proto
     *         versions or nullptr if the configuration is not available for this instance.
     */
    std::unique_ptr<JobServiceStandardConfigT> getConfiguration(
        dune::framework::resources::IConfigurationService *configurationService) const;

    /**
     * @brief Set the If Resource Path Need Component Id object
     * Mostly used on testing
     * @param value boolean
     */
    void setIfResourcePathNeedComponentId(bool value) { resourcePathWithComponentId_ = value; };

    void getSerializationData(std::string &fbsPath, std::string &resourcesDirectoryPath, std::string &fbsRoot) override;

    OperationResult testImport(const OperationDescription &operationDescription,
                               const IdentificationData &identificationData, const ContentId &contentId,
                               const std::string &version, const FileInfoCollection &filesToImport);

    OperationResult testExport(const OperationDescription &exportDescription, const ContentId &contentId,
                               std::string &version, FileInfoCollection &filesToExport);

    std::shared_ptr<std::map<std::string, std::string>> testgetJobServiceStringIds();

    std::string getDefaultJobName(dune::job::JobType jobType) const override;

    bool serializeTicketToJson(const std::string &ticketId, std::string &jsonData,
                               std::string &dataToBeEncrypted) override;
    bool deserializeJsonAndUpdateTicket(const std::string &jsonData) override;
    bool validateAndSaveDefaultJobTicket(const dune::framework::data::SerializedDataBufferPtr &serializedData) override;
    void onMediaPropertyChangedEvent(const MediaPropertyChangedEventArgs &eventArgs);
    void onScannerStatusChangedEvent(dune::scan::scanningsystem::IStatus* scannerStatusInterface);
    void onScannerMediaPresenceChange(dune::scan::scanningsystem::IMediaPath* source, dune::scan::scanningsystem::IMediaPath::MediaPresenceStatus newState);


    bool saveDefaultJobTicket(std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> jobTicket,
                              dune::job::TicketUpdationMode                           updationMode) override;
    bool saveDefaultJobTicket(std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> jobTicket,
                              dune::job::TicketUpdationMode                           updationMode);

  protected:
    virtual dune::framework::core::Uuid getDefaultJobTicketUuid() const override
    {
        return dune::framework::core::Uuid{"557c10b7-e752-45a3-80c0-7e604f7af170"};
    }
    virtual dune::framework::core::Uuid getDefaultJobTicketUuid(dune::job::JobType jobType) const override
    {
        switch (jobType)
        {
            case dune::job::JobType::COPY:
                return getDefaultJobTicketUuid();
            default:
                throw dune::framework::core::ArgumentException("Unsupported Job Type!");
                break;
        }
    }
    virtual std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> createEmptyJobTicket() override;
    virtual std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> getFactoryDefaultJobTicket(
        dune::job::JobType jobType) override;
    virtual void resetShortcuts(dune::framework::data::resets::ResetLevel resetLevel) override;
    std::shared_ptr<std::map<std::string, std::string>> getJobServiceStringIds() const override;
    void validateAndForceUpdateJobTicket(std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> jobTicket);

    std::pair<dune::framework::data::conversion::ConversionResult, 
        std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>> checkAndPerformMigration();

    /**
     * @name IParticipant methods.
     * @{
     */

    OperationResult exportData(const OperationDescription &exportDescription, const ContentId &contentId,
                               std::string &version, FileInfoCollection &filesToExport);

    OperationResult importData(const OperationDescription &importDescription,
                               const IdentificationData &identificationData, const ContentId &contentId,
                               const std::string &version, const FileInfoCollection &filesToImport);

    inline void setResourceFilePath(const std::string &path) { COPY_JOB_SERVICE_RESOURCE_FILE_DIR = path; }
    FRIEND_TEST(GivenAConnectedJobServiceStandard,
                WhenDefaultTicketIsToBeSerialisedToJsonForSupportedJob_ThenReturnSerializedJsonData);
    FRIEND_TEST(GivenAConnectedJobServiceStandard, WhenImportExportDataIsCalled_OperationResultSuccess);
    FRIEND_TEST(GivenANewJobServiceStandard, WhenWaitforMedaiEventAndValidateIsCalled_FunctionExecutesCorrectly);
    FRIEND_TEST(GivenANewJobServiceStandard, WhenOnEngineConnectionChangeIsCalled_WithHwCapabilitiesAvailable_FunctionExecutesCorrectly);
    FRIEND_TEST(GivenANewJobServiceStandard, WhenOnEngineConnectionChangeIsCalled_WithoutHwCapabilities_FunctionExecutesCorrectly);
    FRIEND_TEST(GivenANewJobServiceStandard, WhenConnectedIsCalled_MigrationLogicExecutesCorrectly);
    /**
     * @}
     */

  private:
    const char                                *instanceName_{nullptr};   ///< The instance name.
    std::unique_ptr<JobServiceStandardConfigT> configuration_{nullptr};  ///< The instance's constants configuration
    ServicesPackage servicePackage_{};  ///< service package container for resource manager and other resource services.
    JobServiceStandardUwAdapter              *uwAdapter_{nullptr};                ///< The Underware object adapter
    std::shared_ptr<JobTicketResourceHelper>  jobTicketResourceHelper_{nullptr};  ///< The job ticket resource helper
    dune::job::cdm::IJobManagerAlertProvider *jobManagerAlertProvider_{nullptr};
    dune::scan::Jobs::Scan::IScanPipeline    *scanPipeline_{nullptr};
    dune::scan::scanningsystem::IMedia       *scanMedia_{nullptr};          ///< interface of media from scanningsystem.
    dune::job::IJobDetailsManager            *jobDetailsManager_{nullptr};  ///< JobDetailsManager.

    dune::scan::scanningsystem::IScannerCapabilities *scanCapabilities_{
        nullptr};                                                             ///< interface of scannerCapabilities.
    dune::scan::scanningsystem::IStatus     *scannerStatus_{ nullptr };
    dune::copy::Jobs::Copy::IJobConstraints *jobConstraintsHelper_{nullptr};  ///< interface to obtain the constraints.
    dune::scan::IScanConstraints *scanConstraintsHelper_{nullptr};  ///< interface to obtain the scan constraints.
    dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules *copyDynamicConstraintsHelper_{
        nullptr};  // interface to obtain the dynamic constraints.

    dune::framework::storage::INvram        *Nvram_{nullptr};
    dune::localization::ILocaleProvider     *localization_{nullptr};
    dune::print::engine::ISettings          *interfaceISettings_{nullptr};  ///< interface to the ISettings subsystem
    dune::copy::cdm::ICopyAdapter           *copyAdapter_{nullptr};         ///< ICopyAdapter interface
    dune::job::IIntentsManager              *intentsManager_{nullptr};      ///< IIntentsManager interface
    uint32_t                                 copyEventSubscriptionId{0};
    bool                                     resourcePathWithComponentId_{true};
    bool                                     isPreRunSupported_{false};
    dune::copy::Jobs::Copy::ICopyPipeline   *copyPipeline_{nullptr};
    IExportImport                           *exportImportManager_{nullptr};
    const std::string                        contentId_ = "CopyTicketSettings";
    std::unique_ptr<SubscriptionHandler>     subscriptionHandlerExportImport_ = nullptr;
    std::unique_ptr<SubscriptionHandler>     subscriptionHandlerBackupRestore_ = nullptr;
    std::string                              COPY_JOB_SERVICE_RESOURCE_FILE_DIR;
    std::string                              BACKUP_RESTORE_VERSION = "2.0";
    ISystemConversionHelper                 *systemConversionHelper_{nullptr};
    ICopyTicketConverter                    *copyTicketConverter_{nullptr};
    dune::print::engine::IConnector         *itsIConnector_{nullptr};
    dune::imaging::IColorAccessControl      *colorAccessControl_{nullptr};  ///< Color access control interface
    

    
    std::mutex                               hwCapabilitiesMutex_;
    std::condition_variable                  hwCapabilitiesCondition_;
    dune::print::engine::IConnector::ConnectorStatusEvent::SubscriptionHandler connectorStatusEventHandler_;
    dune::scan::Jobs::Scan::ScanMediaSizeEvent::SubscriptionId                 scanMediaSizeSubscriptionId_;

    /**
     * @name Configuration data members
     * @{
     */

    bool                                hasSharedPaperPath_{false};
    dune::copy::Jobs::Copy::ProductType prePrintConfiguration_{
        dune::copy::Jobs::Copy::ProductType::HOME_PRO};  ///< Print configuration value for copy pipeline
    bool                                                 copyBasicPipeline_{false};
    MaxLengthConfig                                      maxLengthConfig_{};
    int                                                  thresholdOverride_{0};
    dune::imaging::types::RenderIntent                   renderIntent_{dune::imaging::types::RenderIntent::AUTO};
    bool                                                 multiPageSupportedFromFlatbed_{false};
    dune::print::engine::pageBased::IMediaInfoExtension *mediaInfoExt_{nullptr};
    /**
     * @}
     */

    void registerShortcuts();
    void addFactoryShortcut(const std::shared_ptr<dune::admin::shortcuts::FactoryShortuctDefT> quicksetData);
    void registerJobServiceState();
    void handleCopyAdapterDataChangeEvent(dune::copy::cdm::CopyConfigurationEventType event);
    void onCopyEnableStateChange();
    void updateShortcut(dune::admin::shortcuts::shortcutFilter_t &filter, const dune::cdm::shortcut_1::State &state);

    void handleScanMediaSizeEvent(dune::imaging::types::MediaSizeId mediaSizeId);
    bool setDefaultJobTicketMediaSizeAndType(const dune::imaging::types::MediaSizeId size,
                                             const dune::imaging::types::MediaIdType type);

    std::string getResourcePath();

    /**
     * @brief Given a string id using csf format ("StringIds.cXXXXXX"), extract:
     * 1. The string translation to the current configured language
     * 2. The localIdTable containing the stringId as string (idString) and as an integer (idValue).
     * @param titleStringIdCsf String id using csf format
     * @return std::tuple<std::string, dune::cdm::shortcut_1::LocalIdTable> Touple with the translated string Id and the
     * localIdtable
     */
    std::tuple<std::string, dune::cdm::shortcut_1::LocalIdTable> localizeQuicksetTitleFromStringId(
        std::string titleStringIdCsf);

    std::shared_ptr<CopyQuicksetFbT>                        loadFactoryQuicksetFromJson(std::string quicksetFileName,
                                                                                        std::string schemaFilename, std::string fbsRoot);
    std::shared_ptr<dune::copy::Jobs::Copy::ICopyJobTicket> createJobTicketUsingFlatbuffer(
        std::shared_ptr<CopyJobIntentFbT> intentFb);
    void onEngineConnectionChange( dune::print::engine::IConnector * connector, const  dune::print::engine::IConnector::ConnectorStatus & status);
    void WaitforMedaiEventAndValidate( std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable> jobTicketToBeSaved);

    /**
     * @brief Method to validate current tickets related with job service
     */
    void validateCurrentTickets();
};

}}}}  // namespace dune::copy::Jobs::Copy

DEFINE_MODULE_UID(dune::copy::Jobs::Copy::JobServiceStandard, 0x6a979c);

DESCRIBE_COMPONENT_FLAVOR_BEGIN(dune::copy::Jobs::Copy::JobServiceStandard)
PROVIDES_INTERFACE(dune::copy::Jobs::Copy::ICopyJobService)
PROVIDES_INTERFACE(dune::job::IJobTicketResourceHelper)
REQUIRES_INTERFACE(dune::job::IJobServiceManager)
REQUIRES_INTERFACE(dune::job::IJobManager)
REQUIRES_INTERFACE(dune::job::IJobTicketResourceManager)
REQUIRES_INTERFACE(dune::job::IResourceService)
REQUIRES_INTERFACE(dune::print::Resources::IPrintDevice)
REQUIRES_INTERFACE(dune::job::IJobDetailsManager)
REQUIRES_INTERFACE(dune::job::IResourceManagerClient)
REQUIRES_INTERFACE(dune::job::cdm::IJobManagerAlertProvider)
REQUIRES_INTERFACE(dune::imaging::Resources::IImagePersister)
REQUIRES_INTERFACE(dune::framework::data::IDataStore)
REQUIRES_INTERFACE(dune::print::engine::IPrintIntentsFactory)
REQUIRES_INTERFACE(dune::admin::shortcuts::IShortcuts)
REQUIRES_INTERFACE(dune::print::engine::helpers::IRenderingRequirements)
REQUIRES_INTERFACE(dune::copy::cdm::ICopyAdapter)
REQUIRES_INTERFACE(dune::scan::Resources::IScanDevice)
REQUIRES_INTERFACE(dune::copy::Jobs::Copy::IJobConstraints)
REQUIRES_INTERFACE(dune::scan::IScanConstraints)
REQUIRES_INTERFACE(dune::copy::Jobs::Copy::ICopyPipeline)
REQUIRES_INTERFACE(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules)
REQUIRES_INTERFACE(dune::imaging::asset::IMediaAttributes)
REQUIRES_INTERFACE(dune::job::IIntentsManager)
REQUIRES_INTERFACE(dune::framework::data::backup::IExportImport)
DESCRIBE_COMPONENT_FLAVOR_END(dune::copy::Jobs::Copy::JobServiceStandard)

#endif  // DUNE_COPY_JOBS_COPY_JOB_SERVICE_STANDARD_H