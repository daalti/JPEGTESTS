/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_LARGE_FORMAT_H
#define DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_LARGE_FORMAT_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesLargeFormat.h
 * @date   Tue, 11 Oct 2022 11:20:06 +0200
 * @brief  Component used to manage the Dynamic Copy Job Constraints
 * @author yago.cordero.carrera@hp.com (Cordero Carrera, Yago)
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "IComponent.h"
#include "ICopyJobDynamicConstraintRules.h"
#include "CopyJobDynamicConstraintRulesLargeFormatConfig_generated.h"
#include "typeMappers.h"
#include "IMedia.h"

#include <unordered_map>

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_Jobs_Copy_CopyJobDynamicConstraintRulesLargeFormat);

namespace dune { namespace localization {
class ILocaleProvider;
}}

namespace dune { namespace copy { namespace cdm {
class ICopyAdapter;
}}}

namespace dune { namespace copy { namespace Jobs { namespace Copy {
// Forward declaration.
class CopyJobDynamicConstraintRulesLargeFormatUwAdapter;

/**
 * Implementation of the LargeFormat flavor of the CopyJobDynamicConstraintRules component.
 */
class CopyJobDynamicConstraintRulesLargeFormat:
    public dune::framework::component::IComponent,
    public ICopyJobDynamicConstraintRules
{
    friend class CopyJobDynamicConstraintRulesLargeFormatUwAdapter;
public:

    /**
     * @name ICopyJobDynamicConstraintRules methods.
     * @{
     */

    /**
     * @brief getDynamicConstraints
     * @param jobTicket. CopyJob Ticket associated with the constraints 
     * @param staticConstraintsGroup static constraints from previous step, if needed take data from here     
     * @return Return the dynamic constraints grouped
     */
    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> getDynamicConstraints(
        std::shared_ptr<ICopyJobTicket> jobTicket, std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> staticConstraintsGroup,
        const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable = nullptr) override;

    /**
     * @brief Method to force change on ticket if needed
     * @param updatedJobTicketTable ticket updated
     * @param ticket current ticket     
     * @param currentConstraintsGroup current constraints to apply force set check
     * @return Return if constraints was applied and need to be updated again
     */
    bool checkAndApplyForceSets(const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable,
        std::shared_ptr<ICopyJobTicket>                                         ticket,
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup>   currentConstraintsGroup,
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup>   staticConstraintsGroup = nullptr) override;

    /**
     * @brief Update existing constraints wth job dynamic constraints
     * @param jobTicket CopyJob Ticket associated with the constraints 
     * @param constraintsGroup constraints grouped to be updated
     */
    void updateWithJobDynamicConstraints(std::shared_ptr<ICopyJobTicket>        jobTicket, 
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup>   constraintsGroup) override;

    /**
     * @}
     */

    /**
     * @brief CopyJobDynamicConstraintRulesLargeFormat Constructor.
     *
     * @param instanceName the name of the component instance.
     */
    explicit CopyJobDynamicConstraintRulesLargeFormat(const char *instanceName);

    /**
     * Destructor.
     */
    virtual ~CopyJobDynamicConstraintRulesLargeFormat();

    /**
     * @name IComponent methods.
     * @{
     */

    dune::framework::component::ComponentFlavorUid getComponentFlavorUid() const override;
    const char * getComponentInstanceName() const override;
    void initialize(WorkingMode mode, const dune::framework::component::SystemServices *services) override;
    void * getInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName) override;
    void setInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName, void *interfacePtr) override;
    void connected(dune::framework::component::IComponentManager *componentManager, std::future<void> &asyncCompletion) override;
    void shutdown(ShutdownCause cause, std::future<void> &asyncCompletion) override;

    /**
     * @}
     */

private:

    /**
     * @brief Get the Constraints To Apply object     
     * @param listOfRules list of rules expected to apply
     * @param jobTicket current ticket
     * @param staticConstraints constraints from static relative to current setting
     * @param mapSettingsThatCauseConstraint map passed by reference to be filled details relative to values that cause a constraint
     * @return std::shared_ptr<ConstrainedValuesT> constraint values result after check rule
     */
    std::shared_ptr<ConstrainedValuesT> getConstraintsToApply(std::shared_ptr<CopyDynamicRuleT> listOfRules,
        std::shared_ptr<ICopyJobTicket> jobTicket, 
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> staticConstraintsGroup, 
        std::unordered_map<std::string,std::vector<std::shared_ptr<CopyIntentTableValueT>>> &mapSettingsThatCauseConstraint,
        const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable = nullptr);

    /**
     * @brief Get the constraints for the dynamic Force Set to apply object
     * @param listOfRules list of rules expected to apply
     * @param updatedJobTicketTable ticket updated
     * @param currentConstraintsGroup current constraints to apply force set check
     * @return std::shared_ptr<Constraints> constraint values result after check rule
     */
    std::shared_ptr<dune::framework::data::constraints::Constraints> getConstraintsForDynamicForceSets(std::shared_ptr<CopyDynamicRuleT> listOfRules, 
        const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, 
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> currentConstraintsGroup);

    /**
     * @brief Create a Constraint From Rule object
     * @param dataOfRule data of an accepted rule to be inserted onto a constraint
     * @param stringName name of constraint to create
     * @param staticConstraints constraints from static relative to current setting
     * @param constrainedMessage message to set dynamically on constraint.
     * @return std::shared_ptr<dune::framework::data::constraints::Constraints> constraint result for setting
     */
    std::shared_ptr<dune::framework::data::constraints::Constraints> createConstraintFromRule(std::shared_ptr<ConstrainedValuesT> dataOfRule,
        const std::string &stringName, 
        std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints, 
        const std::string &constrainedMessage="");

    /**
     * @brief Evaluate current rule if it's satisfaied and get the reason message
     * @param dataOfRule rule data from fbs
     * @param jobTicket current ticket
     * @param staticConstraintsGroup constraints from static relative to current setting
     * @param mapSettingsThatCauseConstraint map passed by reference to be filled details relative to values that cause a constraint
     * @param updatedJobTicketTable ticket updated
     * @return true if rule is satisfied
     * @return false if no
     * 
     * If you specify `updatedJobTicketTable` the values will be considered only if they changed.
     */
    bool evaluateRule(std::shared_ptr<CopyTicketRuleT> dataOfRule, std::shared_ptr<ICopyJobTicket> jobTicket,
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> staticConstraintsGroup,
        std::unordered_map<std::string,std::vector<std::shared_ptr<CopyIntentTableValueT>>> *mapSettingsThatCauseConstraint = nullptr,
        const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable = std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>(nullptr));

    /**
     * @brief Method to check if any value from setting flatbuffer is on current ticket     
     * @param valuesOfASetting fbs type that contains a possibility of values that must to be checked on ticket
     * @param jobTicket current job ticket
     * @return true if any value from valuesOfSetting is on current job ticket
     * @return false if no
     */
    bool checkIfAnyValueExistOnTicket(std::shared_ptr<SettingFromTicketT> valuesOfASetting, std::shared_ptr<ICopyJobTicket> jobTicket);
    
    /**
     * @brief Method to check if any value from setting flatbuffer is on current ticket, and has changed from the last time
     * @param valuesOfASetting fbs type that contains a possibility of values that must to be checked on ticket
     * @param updatedJobTicketTable ticket updated
     * @return true if any value from valuesOfSetting is on current job ticket
     * @return false if no
     */
    bool checkIfAnyValueWasUpdatedOnTicket(std::shared_ptr<SettingFromTicketT> valuesOfASetting, 
        const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable,
        bool& settingIsSetOnCdm);

    /**
     * @brief Method to combine two rules
     * @param currentConstraintValues current constraint values from previous rules
     * @param ruleToCombine new rule to combine with current constraints
     * 
     * If currentConstraintValues is nullptr, means that not rules what checked previously
     * So ruleToCombineValues will be inserted completely
     * 
     * If currentConstraintValues exist and have values, this method will merge values from current with ruleToCombine
     * Only values that are on two objects, will be conserved on merge action
     */
    std::shared_ptr<ConstrainedValuesT> combineRules(std::shared_ptr<ConstrainedValuesT> currentConstraintValues,
        std::shared_ptr<CopyTicketRuleT> ruleToCombine);

    /**
     * @brief Subscribe to InputStatusChangeEvent notifications for each available input device
     * This event is fired whenever an input device status changes.
     */
    void registerMediaInputStatusChangeEvent();

    /**
     * @brief Unsubscribe to InputStatusChangeEvent notifications for each available input device
     */
    void unregisterMediaInputStatusChangeEvent();

    /**
     * @brief Handle the InputStatusChangeEvent notifications. Update the mapMediaSourcesStatus_ with the
     * input status of the input device snapshot. It is used to modify the media source dependant constraints
     * 
     * @param inputDevice pointer to IInput updated
     * @param snapshot Input snapshot pointer
     */
    void onInputStatusChangeEvent(dune::print::engine::IMedia::IInput *inputDevice, const dune::print::engine::IMedia::InputSnapshotPtr &snapshot);

    /**
     * @brief Modify the valid values of the current setting constraints which are dependant of the input 
     * device status. If an input device is not READY or STANDBY, then it cannot be a valid value for the current 
     * setting constraints
     * 
     * @param staticConstraints constraints from static relative to current setting
     */
    void modifyValidValuesConstraintMediaSourceStatusDependant(std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints);

    /**
     * @brief Modify the valid values of the current setting constraints which are dependant of the finisher 
     * device.
     * 
     * @param staticConstraints constraints from static relative to current setting
     * @param jobTicket current job ticket
     * @param updatedJobTicketTable job ticket table
     */
    void modifyValidValuesConstraintFoldingStyleIdFinisherDependant(std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints,
        std::shared_ptr<ICopyJobTicket> jobTicket,
        const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable);
    
    /* template function to handle different Finisher Device */
    template<class DeviceTuple>
    std::vector<dune::print::engine::DeviceStatus> getStatusFromDevice(DeviceTuple& tuple) const;

    /**
     * @brief Modify the valid values of the outputscale constraints which are dependant of the input 
     * device status. If an input device is not READY or STANDBY, then it cannot be a valid value for the current 
     * setting constraints
     * 
     */
    void modifyValidValuesConstraintMediaSourceStatusDependantOutputScale(std::shared_ptr<dune::framework::data::constraints::Constraints> staticScaleToOutputConstraints, 
        std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraintsScaleSelection);

    /**
     * @brief Modify the valid values of the media destination setting constraints which are dependant of the Copy mode setting.
     * If direct copy mode (printWhileScanning) is selected, the folder cannot be a valid value for media destination
     * 
     * @param staticConstraints constraints from static relative to current setting
     */
    void modifyValidValuesConstraintMediaDestinationDependantCopyMode(std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints,
        std::shared_ptr<ICopyJobTicket> jobTicket);

    /**
     * @brief Get the String Id localized for Cdm Setting object, mapping string id with csf list
     * @param cdmSettingPath cdm path of the setting to check
     * @return std::string string localized
     */
    std::string getStringIdForCdmSetting(const std::string &cdmSettingPath);

    /**
     * @brief Method to take string id for a enum value as string id     
     * @param cdmSettingPath path of setting like cdm url
     * @param valueAsString value as a string
     * @return std::string result
     */
    std::string getStringIdForCdmValueSetting(const std::string &cdmSettingPath,const std::string &valueAsString);

    /**
     * @brief Method to obtain the dynamic constrained message for setting
     * @param settingName name of the setting affected
     * @param valuesAffected values that are affected by setting
     * @param mapSettingsThatCauseConstraint map of values that cause the constraint
     * @return std::string message constrained localized result
     */
    std::string getConstrainedMessage(const std::string &settingName, std::vector<std::shared_ptr<CopyIntentTableValueT>> valuesAffected, std::unordered_map<std::string,std::vector<std::shared_ptr<CopyIntentTableValueT>>> mapSettingsThatCauseConstraint);

    /**
     * @brief Method to localize settings value of the setting that is currently constrained     
     * @param settingName name of the setting affected
     * @param valuesAffected vector of values on copy intent value format
     * @return std::string result
     */
    std::string localizeValuesOfSettingAffected(const std::string &settingName, std::vector<std::shared_ptr<CopyIntentTableValueT>> valuesAffected);

    /**
     * @brief Method to localize all settings that cause that another setting is constrained     
     * @param mapSettingsThatCauseConstraint map with setting and values on copy intent value format
     * @return std::string result
     */
    std::string localizeSettingsRowThatAffectToConstraint(std::unordered_map<std::string,std::vector<std::shared_ptr<CopyIntentTableValueT>>> mapSettingsThatCauseConstraint);

    /**
     * @brief Method to check list from configuration of constraints that are affected by the current unit value     
     * @param staticConstraints original constraints to be modified
     */
    void modifyConstraintsAffectedByCurrentMeasureUnit(std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> staticConstraints);

    /**
     * @brief Loads the configuration for this component instance
     *
     * @param configurationService the pointer to the system's configuration service
     * @return the configuration values to be used by this instance, according to the system's product and proto
     *         versions or nullptr if the configuration is not available for this instance.
     */
    std::unique_ptr<CopyJobDynamicConstraintRulesLargeFormatConfigT> getConfiguration(dune::framework::resources::IConfigurationService *configurationService) const;

    /**
     * @brief Set the Value Ignore Generation Constraints object
     * @param value bool
     */
    void setValueIgnoreGenerationConstraints(const bool value);

    const char *instanceName_; ///< The instance name.
    dune::framework::underware::InterpreterEnvironment * interpreterEnvironment_; ///< The environment where underwares are to be registered
    dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormatUwAdapter *uwAdapter_; ///< The underware object adapter.
    std::unique_ptr<CopyJobDynamicConstraintRulesLargeFormatConfigT>       configuration_{nullptr};  ///< The instance's constants configuration    
    dune::localization::ILocaleProvider         *localization_  {nullptr};
    dune::print::engine::IMedia                 *media_         {nullptr};
    dune::copy::cdm::ICopyAdapter               *copyAdapter_   {nullptr};
    std::map<dune::imaging::types::MediaSource, bool> mapMediaSourcesStatus_;
    dune::print::engine::IMedia::IInput::InputStatusChangeEvent::SubscriptionId inputStatusChangeSubscriptionId_;
    std::map<dune::imaging::types::MediaSource, dune::print::engine::IMedia::IInput::InputStatusChangeEvent::SubscriptionId> inputStatusChangeEventIdMap_;
    bool ignoreGenerationConstraints_{false};
};

}}}}  // namespace dune::copy::Jobs::Copy

DEFINE_MODULE_UID(dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat, 0xc3799d);

DESCRIBE_COMPONENT_FLAVOR_BEGIN(dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat)
    PROVIDES_INTERFACE(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules)
    REQUIRES_INTERFACE(dune::localization::ILocaleProvider)
    REQUIRES_INTERFACE(dune::print::engine::IMedia)
    REQUIRES_INTERFACE(dune::copy::cdm::ICopyAdapter)
DESCRIBE_COMPONENT_FLAVOR_END(dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat)


#endif  // DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_LARGE_FORMAT_H