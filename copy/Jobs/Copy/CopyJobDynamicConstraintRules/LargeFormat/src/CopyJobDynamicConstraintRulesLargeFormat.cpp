/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesLargeFormat.cpp
 * @date   Tue, 11 Oct 2022 11:20:06 +0200
 * @brief  Component used to manage the Dynamic Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobDynamicConstraintRulesLargeFormat.h"

#include "common_debug.h"
#include "CopyJobDynamicConstraintRulesLargeFormat_TraceAutogen.h"
#include "ErrorManager.h"
#include "CopyJobDynamicConstraintRulesLargeFormatUwAdapter.h"
#include "StringIds.h"
#include "ILocaleProvider.h"
#include "CopyJobDynamicConstraintRulesLargeFormatParserHelper.h"
#include "ParameterizedString.h"
#include "ILocale.h"
#include "ICopyAdapter.h"
#include "Constraints.h"

using DeviceStatus = dune::print::engine::DeviceStatus;
using IInput = dune::print::engine::IMedia::IInput;
using InputSnapshot = dune::print::engine::IMedia::InputSnapshot;
using InputSnapshotPtr = std::shared_ptr<const InputSnapshot>;
using MediaHelper = dune::print::engine::MediaHelper;
using MediaSource = dune::imaging::types::MediaSource;
using Constraints = dune::framework::data::constraints::Constraints;

using DeviceStatus = dune::print::engine::DeviceStatus;
// Factory method

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_Jobs_Copy_CopyJobDynamicConstraintRulesLargeFormat)
{
    dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat *instance = 
        new dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat(instanceName);
    assert(instance != nullptr);
    return static_cast<dune::framework::component::IComponent *>(instance);
}

static constexpr uint8_t CHECK_AND_APPLY_FORCE_SETS_FROM_TABLE_MAX_ITERATIONS { 5u };

namespace dune { namespace copy { namespace Jobs { namespace Copy {

// Constructor and destructor

CopyJobDynamicConstraintRulesLargeFormat::CopyJobDynamicConstraintRulesLargeFormat(const char *instanceName) :
    instanceName_(instanceName),
    interpreterEnvironment_(nullptr),
    uwAdapter_(nullptr)
{
    CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat: constructed", instanceName_);
}

CopyJobDynamicConstraintRulesLargeFormat::~CopyJobDynamicConstraintRulesLargeFormat()
{
    CHECKPOINTA("%s/CopyJobDynamicConstraintRulesLargeFormat: destructed", instanceName_);
    if ( uwAdapter_ != nullptr )
    {
        delete uwAdapter_;
    }
}

// IComponent methods.

dune::framework::component::ComponentFlavorUid CopyJobDynamicConstraintRulesLargeFormat::getComponentFlavorUid() const
{
    return GET_MODULE_UID(CopyJobDynamicConstraintRulesLargeFormat);
}

const char *CopyJobDynamicConstraintRulesLargeFormat::getComponentInstanceName() const
{
    return instanceName_;
}

void CopyJobDynamicConstraintRulesLargeFormat::initialize(WorkingMode mode, const dune::framework::component::SystemServices *services)
{
    DUNE_UNUSED(mode);
    
    if (nullptr == services)
    {
        CHECKPOINTA("%s/CopyJobDynamicConstraintRulesLargeFormat: initialize services_ value is null during initialize",
                    getComponentInstanceName());
        assert_msg(false, "ERROR:: services_ value is null during initialize");
    }
    else
    {
        interpreterEnvironment_ = services->interpreterEnvironment_;
        configuration_ = getConfiguration(services->configurationService_);
        if (nullptr == configuration_)
        {
            CHECKPOINTA("%s/CopyJobDynamicConstraintRulesLargeFormat: initialize configuration_ value is null during initialize",
                        getComponentInstanceName());
            assert_msg(false, "ERROR:: configuration_ value is null during initialize");
        }
    }

    CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat: initialized", instanceName_);
}

void * CopyJobDynamicConstraintRulesLargeFormat::getInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName)
{
    DUNE_UNUSED(portName);
    void *interfacePtr = nullptr;
    if (interfaceUid == GET_INTERFACE_UID(ICopyJobDynamicConstraintRules))
    {
        interfacePtr = static_cast<ICopyJobDynamicConstraintRules *>(this);
    }
    CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat: getInterface %" PRIu32 " from port %s with addr %p", 
        instanceName_, interfaceUid, portName, interfacePtr);
    return interfacePtr;
}

void CopyJobDynamicConstraintRulesLargeFormat::setInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName, void *interfacePtr)
{    
    if (interfaceUid == GET_INTERFACE_UID(dune::localization::ILocaleProvider))
    {
        localization_ = static_cast<dune::localization::ILocaleProvider*>(interfacePtr);
        CHECKPOINTB("%s/CopyJobDynamicConstraintRulesLargeFormat: setInterface ILocaleProvider to port %s with addr %p", 
            instanceName_, portName, interfacePtr);
    }
    else if (interfaceUid == GET_INTERFACE_UID(dune::print::engine::IMedia))
    {
        CHECKPOINTB("%s/CopyJobDynamicConstraintRulesLargeFormat::setInterface IMedia to port %s with addr %p", 
            instanceName_, portName, interfacePtr);
        media_ = static_cast<dune::print::engine::IMedia *>(interfacePtr);
    }
    else if(interfaceUid == GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter))
    {
        CHECKPOINTB("%s/CopyJobDynamicConstraintRulesLargeFormat::setInterface ICopyAdapter to port %s with addr %p", 
            instanceName_, portName, interfacePtr);
        copyAdapter_ = static_cast<dune::copy::cdm::ICopyAdapter *>(interfacePtr);
    }
}

void CopyJobDynamicConstraintRulesLargeFormat::connected(dune::framework::component::IComponentManager *componentManager, std::future<void> &asyncCompletion)
{
    DUNE_UNUSED(componentManager);
    DUNE_UNUSED(asyncCompletion);
    // Initialize the underware adapter.
    if ( interpreterEnvironment_ != nullptr )
    {
        uwAdapter_ = new CopyJobDynamicConstraintRulesLargeFormatUwAdapter(interpreterEnvironment_, instanceName_, this);
    }

    
    // Register current Media inputs
    assert(media_ != nullptr);
    registerMediaInputStatusChangeEvent();

    CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat: connected", instanceName_);
}

void CopyJobDynamicConstraintRulesLargeFormat::shutdown(ShutdownCause cause, std::future<void> &asyncCompletion)
{
    DUNE_UNUSED(cause);
    DUNE_UNUSED(asyncCompletion);

    unregisterMediaInputStatusChangeEvent();

    CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat: shutdown", instanceName_);
}

std::unique_ptr<CopyJobDynamicConstraintRulesLargeFormatConfigT> CopyJobDynamicConstraintRulesLargeFormat::getConfiguration(
    dune::framework::resources::IConfigurationService *configurationService) const
{
    assert(configurationService);
    dune::framework::resources::IConfigurationService::ConfigurationRawData rawConfiguration =
        configurationService->getConfiguration(GET_MODULE_UID(CopyJobDynamicConstraintRulesLargeFormat), getComponentInstanceName());
    if (rawConfiguration.data && (rawConfiguration.size > 0))
    {
        flatbuffers::Verifier verifier(rawConfiguration.data.get(), rawConfiguration.size);
        assert(VerifyCopyJobDynamicConstraintRulesLargeFormatConfigBuffer(verifier));
        return UnPackCopyJobDynamicConstraintRulesLargeFormatConfig(rawConfiguration.data.get());
    }
    else
    {
        CHECKPOINTB("CopyJobDynamicConstraintRulesLargeFormat::getConfiguration Not Raw Configuration obtained");
        return std::unique_ptr<CopyJobDynamicConstraintRulesLargeFormatConfigT>();
    }
}


std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> CopyJobDynamicConstraintRulesLargeFormat::getDynamicConstraints(
        std::shared_ptr<ICopyJobTicket> jobTicket, std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> staticConstraintsGroup,
        const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable)
{
    CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getDynamicConstraints");

    // Return a nullptr when configuration_ not exist
    // This situation is not normal expected case because all products must to have a properly config file on initialization
    // Return null when ignore boolean is set to true
    if(!configuration_ || ignoreGenerationConstraints_)
    {
        return nullptr;
    }

    // If mapMediaSourcesStatus_ is empty, then check again if the media information is available now
    if (mapMediaSourcesStatus_.empty())
    {
        registerMediaInputStatusChangeEvent();
    }

    // Modify the media source dependant static constraints with the ready media sources, and when job is started.
    // If ticket hasn't job associated, allow select roll options instead of are not loaded
    if (!mapMediaSourcesStatus_.empty() && jobTicket && jobTicket->getState() != dune::job::JobStateType::UNDEFINED)
    {
        CHECKPOINTB("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getDynamicConstraints job defined and media inputs to check dependencies");
        auto outputCanvasMediaIdConstraints = staticConstraintsGroup->getConstraints("pipelineOptions/imageModifications/outputCanvasMediaId");
        modifyValidValuesConstraintMediaSourceStatusDependant(outputCanvasMediaIdConstraints);

        auto scaleToOutputConstraints = staticConstraintsGroup->getConstraints("pipelineOptions/scaling/scaleToOutput");
        auto scaleToSelectionConstraints = staticConstraintsGroup->getConstraints("pipelineOptions/scaling/scaleSelection");
        modifyValidValuesConstraintMediaSourceStatusDependantOutputScale(scaleToOutputConstraints, scaleToSelectionConstraints);
    }
    else
    {
        CHECKPOINTB("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getDynamicConstraints no media inputs to check dependencies");
    }

    modifyConstraintsAffectedByCurrentMeasureUnit(staticConstraintsGroup);

    auto foldingStyleIdConstraints = staticConstraintsGroup->getConstraints("dest/print/foldingStyleId");
    modifyValidValuesConstraintFoldingStyleIdFinisherDependant(foldingStyleIdConstraints, jobTicket, updatedJobTicketTable);

    auto mediaDestinationConstraints = staticConstraintsGroup->getConstraints("dest/print/mediaDestination");
    modifyValidValuesConstraintMediaDestinationDependantCopyMode(mediaDestinationConstraints, jobTicket);

    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> constraintsGroupResult = 
        std::make_shared<dune::framework::data::constraints::ConstraintsGroup>();

    // If there are rules on list and static constrains have elements, start to manage rules
    if(jobTicket != nullptr && !configuration_->listOfRulesBasedOnTicketValues.empty() && !staticConstraintsGroup->getAllConstraints().empty())
    {
        for(auto dynamicRule : configuration_->listOfRulesBasedOnTicketValues)
        {
            CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getDynamicConstraints checking rule for setting: %s",
                dynamicRule->settingName.c_str());
            // Check if ticket have a Rule to apply based on ticket
            std::unordered_map<std::string,std::vector<std::shared_ptr<CopyIntentTableValueT>>> mapSettingsThatCauseConstraint;
            std::shared_ptr<ConstrainedValuesT> constraintValues = getConstraintsToApply(dynamicRule, jobTicket, staticConstraintsGroup, 
                mapSettingsThatCauseConstraint, updatedJobTicketTable);

            // Generate and add constraint on constraint group, and take settings that cause this constraint error to generate error message expected
            auto constraints = staticConstraintsGroup->getConstraints(dynamicRule->settingName);

            // Not add constraints if not exist, they must to come from static
            if(constraints != nullptr && constraintValues != nullptr)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getDynamicConstraints adding constraints for setting: %s",
                    dynamicRule->settingName.c_str());                    
                std::vector<std::shared_ptr<CopyIntentTableValueT>> valuesAffected = 
                    FlatBufferParserToCdmType::getValuesNotAllowed(constraintValues,constraints); 
                std::string constrainedMessage = getConstrainedMessage(dynamicRule->settingName, valuesAffected, mapSettingsThatCauseConstraint);
                auto newConstraints = createConstraintFromRule(constraintValues, dynamicRule->settingName, constraints, constrainedMessage);
                constraintsGroupResult->set(dynamicRule->settingName, newConstraints);
            }
            else
            {
                if(constraints == nullptr)
                {
                    CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getDynamicConstraints warning, setting:"
                        " %s is not on static constraints", dynamicRule->settingName.c_str());
                }
                if(constraintValues == nullptr)
                {
                    CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getDynamicConstraints warning, setting:"
                        " %s not have new values", dynamicRule->settingName.c_str());
                }
            } 
        }
    }

    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getDynamicConstraints -- Exit");

    return constraintsGroupResult;
}

bool CopyJobDynamicConstraintRulesLargeFormat::checkAndApplyForceSets(
    const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>&          updatedJobTicketTable, 
    std::shared_ptr<ICopyJobTicket>                                         ticket, 
    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup>   currentConstraintsGroup,
    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup>   staticConstraintsGroup)
{
    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::checkAndApplyForceSets");
    bool updatedValue = false;
    std::shared_ptr<Constraints> constraintForRule;

    auto iteration = 0;
    for(;iteration < CHECK_AND_APPLY_FORCE_SETS_FROM_TABLE_MAX_ITERATIONS; iteration++)
    {
        // Update dynamic constraint in iteration to ensure that constraints are as expected with ticket un job ticket table
        bool result = false;
        
        if(updatedJobTicketTable != nullptr && !configuration_->listOfDynamicForceSets.empty() && !currentConstraintsGroup->getAllConstraints().empty())
        {
            // We have Dynamic Force Sets to apply.
            // Dynamic Force Sets are like Dynamic Constraints, but they're more like a "hint", not a constraint:
            // when the set condition evaluates as true, it will set the value, but it will let the user change the value.
            for(auto dynamicSet : configuration_->listOfDynamicForceSets)
            {
                CHECKPOINTD_STR("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::checkAndApplyForceSets going to check force set %s",
                    dynamicSet->settingName.c_str());
                constraintForRule = getConstraintsForDynamicForceSets(dynamicSet, updatedJobTicketTable, currentConstraintsGroup);
                if (constraintForRule != nullptr && 
                    CopyTicketCdmHelper::checkIfValueNeedToBeUpdatedOnJobTicketTable(dynamicSet->settingName,updatedJobTicketTable,ticket,constraintForRule)) {
                    CHECKPOINTC_STR("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::checkAndApplyForceSets update value of force set %s",
                        dynamicSet->settingName.c_str());
                
                    // simulate the constraint to force the value
                    result |= CopyTicketCdmHelper::updateValue(dynamicSet->settingName,updatedJobTicketTable,constraintForRule);
                }
            }
        }

        // "For" loop of setting name on list to check specific settings
        // The reason to mainly check only the values on csf file
        // It's because not other values are expected to have problems when a setting is not supported
        // Static constraints never must to have problems on deserialization
        // Dynamic Force Sets already check for constraints
        if(updatedJobTicketTable != nullptr && !configuration_->listOfRulesBasedOnTicketValues.empty() && !currentConstraintsGroup->getAllConstraints().empty())
        {
            for(auto dynamicRule : configuration_->listOfRulesBasedOnTicketValues)
            {
                constraintForRule = currentConstraintsGroup->getConstraints(dynamicRule->settingName);
                CHECKPOINTD_STR("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::checkAndApplyForceSets going to check setting %s",
                    dynamicRule->settingName.c_str());
                if (CopyTicketCdmHelper::checkIfValueNeedToBeUpdatedOnJobTicketTable(dynamicRule->settingName,updatedJobTicketTable,ticket,constraintForRule))
                {
                    CHECKPOINTC_STR("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::checkAndApplyForceSets update value of setting %s",
                        dynamicRule->settingName.c_str());
                    result |= CopyTicketCdmHelper::updateValue(dynamicRule->settingName,updatedJobTicketTable,constraintForRule);
                }
            }
        }

        if (result)
        {
            updatedValue = true;
            auto dynamicConstraintsGroup = getDynamicConstraints(ticket, 
                staticConstraintsGroup ? staticConstraintsGroup : currentConstraintsGroup, 
                updatedJobTicketTable);

            if(dynamicConstraintsGroup)
            {
                auto dynamicConstraints = dynamicConstraintsGroup->getAllConstraints();
                for ( auto &constraint : dynamicConstraints )
                {
                    CHECKPOINTC("CopyJobDynamicConstraintRulesLargeFormat::checkAndApplyForceSets"
                        " - dynamicConstraintsGroup need updated %s", (constraint.first).c_str());
                    currentConstraintsGroup->remove(constraint.first);
                    currentConstraintsGroup->set(constraint.first, constraint.second);
                }
            }
        }
        else
        {
            CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::checkAndApplyForceSets anymore updates");
            break;
        }
    }

    assert_msg(iteration < CHECK_AND_APPLY_FORCE_SETS_FROM_TABLE_MAX_ITERATIONS,
        "CopyJobDynamicConstraintRulesLargeFormat Max number iteration supported was reached. In case if needed, increase number.");

    return updatedValue;
}

std::shared_ptr<Constraints> CopyJobDynamicConstraintRulesLargeFormat::getConstraintsForDynamicForceSets(std::shared_ptr<CopyDynamicRuleT> listOfRules,
    const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable,
    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> currentConstraintsGroup)
{
    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getConstraintsForDynamicForceSets");
    std::shared_ptr<ConstrainedValuesT> result;

    for(auto ticketRule : listOfRules->rules)
    {
        if(evaluateRule(ticketRule, nullptr /* instead of a job ticket we'll use the table */, currentConstraintsGroup, nullptr /* we don't need the reason */, 
            updatedJobTicketTable))
        {
            CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getConstraintsForDynamicForceSets accepted rule");

            // Combine with previous rule
            result = combineRules(result, ticketRule);

            if(ticketRule->rulePolicy == dune::copy::Jobs::Copy::RulePolicy::STOP)
            {
                CHECKPOINTC_STR("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getConstraintsForDynamicForceSets STOP Policy,"
                    " finish rule for setting %s",listOfRules->settingName.c_str());
                break;
            }
        }
    }

    CHECKPOINTD_STR("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getConstraintsForDynamicForceSets %s",
        (result != nullptr)?"there will be constraint to add":"not constraints to be added");

    std::shared_ptr<Constraints> constraints;
    if (result != nullptr) 
    {
        std::shared_ptr<Constraints> baseConstraints = currentConstraintsGroup->getConstraints(listOfRules->settingName); // to make sure we can set that value
        constraints = createConstraintFromRule(result, listOfRules->settingName, baseConstraints);
    }

    return constraints;
}

std::shared_ptr<ConstrainedValuesT> CopyJobDynamicConstraintRulesLargeFormat::getConstraintsToApply(std::shared_ptr<CopyDynamicRuleT> listOfRules,
    std::shared_ptr<ICopyJobTicket> jobTicket,
    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> staticConstraintsGroup, 
    std::unordered_map<std::string,std::vector<std::shared_ptr<CopyIntentTableValueT>>> &mapSettingsThatCauseConstraint,
    const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable)
{
    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getConstraintsToApply");
    std::shared_ptr<ConstrainedValuesT> result;

    for(auto ticketRule : listOfRules->rules)
    {
        if(evaluateRule(ticketRule, jobTicket, staticConstraintsGroup, &mapSettingsThatCauseConstraint, updatedJobTicketTable))
        {
            CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getConstraintsToApply accepted rule");

            // Combine with previous rule
            result = combineRules(result, ticketRule);

            if(ticketRule->rulePolicy == dune::copy::Jobs::Copy::RulePolicy::STOP)
            {
                CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getConstraintsToApply STOP Policy,"
                    " finish rule for setting %s",listOfRules->settingName.c_str());
                break;
            }
        }
    }

    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getConstraintsToApply %s",
        (result != nullptr)?"there will be constraint to add":"not constraints to be added");

    return result;
}

std::shared_ptr<dune::framework::data::constraints::Constraints> CopyJobDynamicConstraintRulesLargeFormat::createConstraintFromRule(
    std::shared_ptr<ConstrainedValuesT> dataOfRule, 
    const std::string &stringName, 
    std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints, 
    const std::string &constrainedMessage)
{
    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::createConstraintFromRule for setting %s",stringName.c_str());

    auto newConstraint = std::make_shared<dune::framework::data::constraints::Constraints>();

    std::string stringIdLocalized = "";
    
    if(dataOfRule->constrainedMessageStringId != "")
    {
        CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::createConstraintFromRule "
            "inserted message for constraints -> %s",dataOfRule->constrainedMessageStringId.c_str());

        // Get string id localized from
        stringIdLocalized = localization_->deviceLocale()->get(
            localization_->deviceLocale()->getStringIdForCsfOnly(dataOfRule->constrainedMessageStringId.c_str()));
    }
    else if(constrainedMessage != "")
    {
        CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::createConstraintFromRule"
            " inserted auto generated constrained message %s",constrainedMessage.c_str());        
        stringIdLocalized = constrainedMessage;
    }
    // Not normal expected, usually must be covered from constrainedMessageStringId or autogenerated with the values from csf
    else
    {
        stringIdLocalized = localization_->deviceLocale()->get(dune::localization::string_id::cThisOptionUnavailable);
    }

    // Define property as disabled
    if(dataOfRule->disabled)
    {
        CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::createConstraintFromRule"
            " disabled rule for setting %s",stringName.c_str());
        newConstraint->add(std::make_unique<dune::framework::data::constraints::Lock>(stringIdLocalized));
    }
    
    // Insert values on new constraint (posible, valid, range, regular Expresion, etc...)
    FlatBufferParserToCdmType::setValuesOnConstraint(dataOfRule->supportedValues,newConstraint,staticConstraints,stringIdLocalized);
    
    return newConstraint;
}

bool CopyJobDynamicConstraintRulesLargeFormat::evaluateRule(std::shared_ptr<CopyTicketRuleT> dataOfRule, 
    std::shared_ptr<ICopyJobTicket> jobTicket, 
    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> staticConstraintsGroup, 
    std::unordered_map<std::string,std::vector<std::shared_ptr<CopyIntentTableValueT>>> *mapSettingsThatCauseConstraint,
    const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable)
{
    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::evaluateRule");

    // AND and NOR logics needs to start with true always
    // NAND and OR needs to start with false
    bool result = (dataOfRule->ifOperation == OperationModeRule::AND || dataOfRule->ifOperation == OperationModeRule::NAND);

    std::unordered_map<std::string,std::vector<std::shared_ptr<CopyIntentTableValueT>>> internalMap;

    if(!dataOfRule->if_.empty())
    { 
        for(auto valuesOfASetting : dataOfRule->if_)
        {
            // Evaluate if ticket has a value
            bool settingIsInCdm = false;
            // It setting on Job Ticket table has a new value that not coincidence, check job ticket should be ignored, this is not here.
            bool isSettingValueOnCurrentTicket = checkIfAnyValueWasUpdatedOnTicket(valuesOfASetting, updatedJobTicketTable, settingIsInCdm)
                || (!settingIsInCdm && checkIfAnyValueExistOnTicket(valuesOfASetting, jobTicket));

            // Evaluate bool result with if Operation, consider break time if any evaluation result on false
            switch(dataOfRule->ifOperation)
            {
                case OperationModeRule::OR:
                case OperationModeRule::NOR:
                    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::evaluateRule OR | NOR logic to apply");
                    result |= isSettingValueOnCurrentTicket;
                    break;
                case OperationModeRule::AND:
                case OperationModeRule::NAND:
                default:
                    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::evaluateRule AND | NAND logic to apply");
                    result &= isSettingValueOnCurrentTicket;
                    break;
            }

            if(isSettingValueOnCurrentTicket && (dataOfRule->ifOperation == OperationModeRule::AND || dataOfRule->ifOperation == OperationModeRule::OR))
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::evaluateRule AND | OR logic - insert withValueIn directly on internal map");

                internalMap.insert(std::make_pair<std::string,std::vector<std::shared_ptr<CopyIntentTableValueT>>>(
                    std::string(valuesOfASetting->settingName),
                    std::vector<std::shared_ptr<CopyIntentTableValueT>>(valuesOfASetting->withValueIn)));
            }
            else if(staticConstraintsGroup != nullptr && !isSettingValueOnCurrentTicket && (dataOfRule->ifOperation == OperationModeRule::NAND || dataOfRule->ifOperation == OperationModeRule::NOR))
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::evaluateRule NAND | NOR logic - insert reverse of withValueIn on internal map");
                std::shared_ptr<ConstrainedValuesT> contraintValidValues = std::make_shared<ConstrainedValuesT>();
                contraintValidValues->supportedValues = valuesOfASetting->withValueIn;

                std::vector<std::shared_ptr<CopyIntentTableValueT>> vectorIntentValuesForMessage = FlatBufferParserToCdmType::getValuesNotAllowed(
                    contraintValidValues,
                    staticConstraintsGroup->getConstraints(valuesOfASetting->settingName));

                internalMap.insert(std::make_pair<std::string,std::vector<std::shared_ptr<CopyIntentTableValueT>>>(
                    std::string(valuesOfASetting->settingName),
                    std::vector<std::shared_ptr<CopyIntentTableValueT>>(vectorIntentValuesForMessage)));
            }

            // With NAND or OR logics, if there is any that is true, I can stop seeing anymore
            // With AND and NOR logic,s if there is any that is false, I can stop too
            if(((dataOfRule->ifOperation == OperationModeRule::NAND || dataOfRule->ifOperation == OperationModeRule::AND ) && !result) ||
                ((dataOfRule->ifOperation == OperationModeRule::OR || dataOfRule->ifOperation == OperationModeRule::NOR) && result) )
            {
                CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::evaluateRule not needed check more values");
                break;
            }
        }

        // In case that we are on a Negative operation, we invert current result
        if(dataOfRule->ifOperation == OperationModeRule::NAND || dataOfRule->ifOperation == OperationModeRule::NOR) 
        {
            result = !result;
        }
    }
    else
    {
        result = false;
        CHECKPOINTB("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::evaluateRule not dataOfRule->if_ to read");
    }

    if (mapSettingsThatCauseConstraint != nullptr) {
        // Add values on map
        if(result && !internalMap.empty())
        {
            for(auto pair : internalMap)
            {
                CHECKPOINTD_STR("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::evaluateRule going to add values on mapSettingsThatCauseConstraint %s",pair.first.c_str());
                auto iterator = mapSettingsThatCauseConstraint->find(pair.first);        
                
                // New value
                if(iterator == mapSettingsThatCauseConstraint->end())
                {
                    CHECKPOINTB_STR("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::evaluateRule insert on mapSettingsThatCauseConstraint setting cause %s",pair.first.c_str());
                    mapSettingsThatCauseConstraint->insert(pair);
                }
                // add values affected on same iterator.
                else
                {
                    for(auto intentValueTables : pair.second)
                    {
                        // Avoid to add repeated values
                        auto vectorIterator = std::find_if(iterator->second.begin(),iterator->second.end(),
                            [&](std::shared_ptr<CopyIntentTableValueT> vectorValue)
                            {
                                CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::evaluateRule Comparing union values");
                                return FlatBufferParserToCdmType::compareUnionValue(vectorValue->unionValue, intentValueTables->unionValue);
                            }
                        );

                        if(vectorIterator == iterator->second.end())
                        {
                            CHECKPOINTD_STR("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::evaluateRule Updating value on mapSettingsThatCauseConstraint for setting %s",pair.first.c_str());
                            iterator->second.push_back(intentValueTables);
                        }
                        else
                        {
                            CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::evaluateRule update exist, not need to add again");
                        }
                    }            
                }
            }
        }
        else
        {
            CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::evaluateRule Not values added to map of cause error");
        }
    }

    CHECKPOINTC_STR("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::evaluateRule result %s",result ? "Accepted" : "Rejected");

    return result;
}

bool CopyJobDynamicConstraintRulesLargeFormat::checkIfAnyValueExistOnTicket(std::shared_ptr<SettingFromTicketT> valuesOfASetting, 
    std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::checkIfAnyValueExistOnTicket");

    bool result = false;
    if(jobTicket)
    {
        // Check that values on withValueIn are all the same type
        // Check that type coincidence between all values in vector.
        auto unionType = valuesOfASetting->withValueIn[0]->unionValue.type;
        for(auto unionValueTable : valuesOfASetting->withValueIn)
        {
            assert_msg(unionType == unionValueTable->unionValue.type,"Type between union not coincidence, report as an error");

            // OR check, when check on specific ticket values, we always will check if any value exist on ticket, that means and OR logic
            result |= CopyTicketCheckerFromFlatBufferEnum::compareValueOnTicket(valuesOfASetting->settingName,unionValueTable->unionValue,jobTicket);
            if(result)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::checkIfAnyValueExistOnTicket any value founded");
                break;
            }
        }
    }

    CHECKPOINTD_STR("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::checkIfAnyValueExistOnTicket any value %s",
        result? "exist": "non exist");

    return result;
}

bool CopyJobDynamicConstraintRulesLargeFormat::checkIfAnyValueWasUpdatedOnTicket(std::shared_ptr<SettingFromTicketT> valuesOfASetting, 
    const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm)
{
    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::checkIfAnyValueWasUpdatedOnTicket");

    bool result = false;

    if(updatedJobTicketTable)
    {
        // Check that values on withValueIn are all the same type
        // Check that type coincidence between all values in vector.
        auto unionType = valuesOfASetting->withValueIn[0]->unionValue.type;
        for(auto unionValueTable : valuesOfASetting->withValueIn)
        {
            assert_msg(unionType == unionValueTable->unionValue.type,"Type between union not coincidence, report as an error");

            // OR check, when check on specific ticket values, we always will check if any value exist on ticket, that means and OR logic
            result |= CopyTicketCheckerFromFlatBufferEnum::compareValueOnTicketTable(valuesOfASetting->settingName,unionValueTable->unionValue,
                updatedJobTicketTable, settingIsSetOnCdm);

            if (result) {
                CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::checkIfAnyValueWasUpdatedOnTicket any value founded");
                break;
            }
        }
    }
    else
    {
        CHECKPOINTB("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::checkIfAnyValueWasUpdatedOnTicket Job Ticket Table is null");
    }

    CHECKPOINTD_STR("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::checkIfAnyValueWasUpdatedOnTicket any value %s",result ? 
        "exist": "non exist" );

    return result;
}

std::shared_ptr<ConstrainedValuesT> CopyJobDynamicConstraintRulesLargeFormat::combineRules(std::shared_ptr<ConstrainedValuesT> currentConstraintValues,std::shared_ptr<CopyTicketRuleT> ruleToCombine)
{
    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::combineRules");

    assert_msg(ruleToCombine->then,"Then combination is empty, crash error");
    assert_msg(!ruleToCombine->then->supportedValues.empty(),"Supported values on then is empty, not supported set");

    if(currentConstraintValues)
    {
        // Find constraints that are on two rules
        std::vector<std::shared_ptr<CopyIntentTableValueT>> newSupportedValues;

        for(auto unionValueTable : currentConstraintValues->supportedValues)
        {
            std::vector<std::shared_ptr<CopyIntentTableValueT>>::iterator iteratorConstraintValues = std::find_if(ruleToCombine->then->supportedValues.begin(), ruleToCombine->then->supportedValues.end(), 
                [&](std::shared_ptr<CopyIntentTableValueT> newValue)
                {
                    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::combineRules Comparing union values");
                    return FlatBufferParserToCdmType::compareUnionValue(newValue->unionValue, unionValueTable->unionValue);
                }
            );

            if ( iteratorConstraintValues != ruleToCombine->then->supportedValues.end())
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::combineRules Adding constraint on union value");
                newSupportedValues.push_back(unionValueTable);
            }
        }

        currentConstraintValues->supportedValues = newSupportedValues;        
        assert_msg(!currentConstraintValues->supportedValues.empty(), "Dynamic Constraints always must to result on at least one value, have zero is an error");

        // Maintain message from first. So nothing to merge needed.
        // If current not have message, take from new rule
        if(currentConstraintValues->constrainedMessageStringId == "" && 
            currentConstraintValues->constrainedMessageStringId != ruleToCombine->then->constrainedMessageStringId)
        {
            CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::combineRules set constrained message id %s",ruleToCombine->then->constrainedMessageStringId.c_str());

            currentConstraintValues->constrainedMessageStringId = ruleToCombine->then->constrainedMessageStringId;
        }

        // Prioritize disabled state on true
        currentConstraintValues->disabled |= ruleToCombine->then->disabled;
    }
    else
    {
        CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::combineRules - No previous rules, accept rule directly");

        // Not current constraints set, so new rule is directly selected.
        currentConstraintValues = ruleToCombine->then;
    }

    assert_msg(currentConstraintValues != nullptr,"Constraint is null there must to be an error related on setter");

    return currentConstraintValues;
}

void CopyJobDynamicConstraintRulesLargeFormat::registerMediaInputStatusChangeEvent()
{
    const auto      inputDevicesListTuple = media_->getInputDevices();
    const APIResult inputListOK = std::get<0>(inputDevicesListTuple);
    const auto      inputDevicesList = std::get<1>(inputDevicesListTuple);

    if ((inputListOK == APIResult::OK) && (inputDevicesList.size() > 0))
    {
        CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat::registerMediaInputStatusChangeEvent: input devices size = %d", instanceName_, inputDevicesList.size());

        for (const auto &inputDevice : inputDevicesList)
        {
            InputSnapshotPtr inputSnapshot = MediaHelper::getInputSnapshot(inputDevice);
            auto source = inputDevice->getMediaSource();

            inputStatusChangeSubscriptionId_ = inputDevice->getInputStatusChangeEvent().addSubscription(
                EVENT_MAKE_MEMBER_DELEGATE_WITH_EMITTER(CopyJobDynamicConstraintRulesLargeFormat::onInputStatusChangeEvent, this));
            inputStatusChangeEventIdMap_.insert(std::pair<dune::imaging::types::MediaSource, IInput::InputStatusChangeEvent::SubscriptionId>(source, inputStatusChangeSubscriptionId_));
            CHECKPOINTB("%s/CopyJobDynamicConstraintRulesLargeFormat::registerMediaInputStatusChangeEvent: subscription to InputStatusChangeEvent done eventId = %d", instanceName_, inputStatusChangeSubscriptionId_);

            mapMediaSourcesStatus_.insert(std::pair<dune::imaging::types::MediaSource, bool>(source, false));

            // Force first time
            onInputStatusChangeEvent(inputDevice.get(), inputSnapshot);
        }
    }
    else
    {
        CHECKPOINTA("%s/CopyJobDynamicConstraintRulesLargeFormat::registerMediaInputStatusChangeEvent: ERROR input devices are not available", instanceName_);
    }
}

void CopyJobDynamicConstraintRulesLargeFormat::unregisterMediaInputStatusChangeEvent()
{
    const auto      inputDevicesListTuple = media_->getInputDevices();
    const APIResult inputListOK = std::get<0>(inputDevicesListTuple);
    const auto      inputDevicesList = std::get<1>(inputDevicesListTuple);

    if ((inputListOK == APIResult::OK) && (inputDevicesList.size() > 0))
    {
        for (auto &inputDevice : inputDevicesList)
        {
            auto mediaSource = inputDevice->getMediaSource();
            for (auto it = inputStatusChangeEventIdMap_.begin(); it != inputStatusChangeEventIdMap_.end(); it++)
            {
                if ((it->first) == mediaSource)
                {
                    CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat::unregisterMediaInputStatusChangeEvent: mediaSource = %d", instanceName_, static_cast<int>(mediaSource));
                    inputDevice->getInputStatusChangeEvent().removeSubscription(it->second);
                    inputStatusChangeEventIdMap_.erase(it);
                    break;
                }
            }
        }
        assert(inputStatusChangeEventIdMap_.empty());
        CHECKPOINTB("%s/CopyJobDynamicConstraintRulesLargeFormat::unregisterMediaInputStatusChangeEvent: All the input status change event id subscriptions were removed", instanceName_);
    }
}

void CopyJobDynamicConstraintRulesLargeFormat::onInputStatusChangeEvent(IInput *inputDevice, const InputSnapshotPtr &snapshot)
{
    CHECKPOINTD("%s/CopyJobDynamicConstraintRulesLargeFormat::onInputStatusChangeEvent enter", instanceName_);

    // There are situation when rpc connect not goes well, and notify an snapshot on start or on update, with nullptr
    // So It's needed a protection to avoid do any error related with this
    if(inputDevice && snapshot)
    {
        const auto source = inputDevice->getMediaSource();
        mapMediaSourcesStatus_[source] = (snapshot->hasDeviceStatus(DeviceStatus::READY) || snapshot->hasDeviceStatus(DeviceStatus::STANDBY));

        CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat::onInputStatusChangeEvent: media source = %d is READY || STANDBY = %s", instanceName_, static_cast<int32_t>(source), (mapMediaSourcesStatus_[source] ? "true" : "false"));

        for (auto status : snapshot->getDeviceStatus())
        {
            CHECKPOINTD("%s/CopyJobDynamicConstraintRulesLargeFormat::onInputStatusChangeEvent media source = %d status: %d", instanceName_, source, status);
        }
    }
    else
    {
        CHECKPOINTB("%s/CopyJobDynamicConstraintRulesLargeFormat::onInputStatusChangeEvent Received info with nullptr, discarded any change", instanceName_);
    }
    
    CHECKPOINTD("%s/CopyJobDynamicConstraintRulesLargeFormat::onInputStatusChangeEvent exit", instanceName_);
}

void CopyJobDynamicConstraintRulesLargeFormat::modifyValidValuesConstraintMediaSourceStatusDependant(std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints)
{
    if(staticConstraints != nullptr)
    {
        std::vector<dune::cdm::glossary_1::MediaSourceId> validValues = std::vector<dune::cdm::glossary_1::MediaSourceId>();
        std::vector<dune::cdm::glossary_1::MediaSourceId> possibleValues = std::vector<dune::cdm::glossary_1::MediaSourceId>();

        for(auto constraint : staticConstraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM)
            {
                auto previousValidValues = static_cast<dune::framework::data::constraints::ValidValuesEnum<dune::cdm::glossary_1::MediaSourceId>*>
                    (constraint)->getValidValues();

                // Always insert automatic if product support it
                auto iteratorAutoValidValue = std::find(previousValidValues.begin(), previousValidValues.end(), dune::cdm::glossary_1::MediaSourceId::auto_);
                if (iteratorAutoValidValue != previousValidValues.end())
                {
                    CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat::modifyValidValuesConstraintMediaSourceStatusDependant"
                        " inserting auto media source value", instanceName_);
                    validValues.push_back(dune::cdm::glossary_1::MediaSourceId::auto_);
                }

                // Check If media (roll, tray, or similar) is on media source list  
                for (auto mediaSource : mapMediaSourcesStatus_)
                {
                    dune::cdm::glossary_1::MediaSourceId mediaSourceCdmValue = dune::job::cdm::mapToCdm(mediaSource.first);
                    bool mediaSourceReady = mediaSource.second;
                    auto iteratorPreviousValidValues = std::find(previousValidValues.begin(), previousValidValues.end(), mediaSourceCdmValue);

                    // Not add accepted valid value, if static constraints not accept them as they expected.
                    if (iteratorPreviousValidValues != previousValidValues.end() && mediaSourceReady)
                    {
                        CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat::modifyValidValuesConstraintMediaSourceStatusDependant"
                            " mediaSource %d added as valid value", instanceName_, mediaSourceCdmValue);
                        validValues.push_back(mediaSourceCdmValue);
                    }
                }
            }
            else if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::POSSIBLE_VALUE_ENUM)
            {
                possibleValues = static_cast<dune::framework::data::constraints::PossibleValuesEnum<dune::cdm::glossary_1::MediaSourceId>*>
                    (constraint)->getPossibleValues();
            }
        }

        // Refreshing values in current static constraints
        staticConstraints->removeAll();
        auto enumValidValuesConstraint =    std::make_unique<dune::framework::data::constraints::ValidValuesEnum<dune::cdm::glossary_1::MediaSourceId>>
            (validValues,   dune::localization::string_id::cSingleRollOutOfPaper);
        auto enumPossibleValuesConstraint = std::make_unique<dune::framework::data::constraints::PossibleValuesEnum<dune::cdm::glossary_1::MediaSourceId>>
            (possibleValues,
            &dune::cdm::glossary_1::MediaSourceId::valueToString,
            dune::localization::string_id::cSingleRollOutOfPaper);
        staticConstraints->add(std::move(enumValidValuesConstraint));
        staticConstraints->add(std::move(enumPossibleValuesConstraint));
    }
    else
    {
        CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat::modifyValidValuesConstraintMediaSourceStatusDependant staticConstraints is null!", 
            instanceName_);
    }
}

void CopyJobDynamicConstraintRulesLargeFormat::modifyValidValuesConstraintFoldingStyleIdFinisherDependant(
    std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints,
    std::shared_ptr<ICopyJobTicket> jobTicket,
    const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable )
{
    CHECKPOINTC("CopyJobStaticConstraintRules::getFoldingStylesConstraints Enter");
    // Valid Values on an Enum

    if( nullptr != staticConstraints )
    {
        // New values vector.
        std::vector<short> validValues = std::vector<short>();
        std::vector<short> possibleValues = std::vector<short>(); // Add this line
        std::vector<std::string> stylesNames = std::vector<std::string>();

        // Call IMedia to get the list of devices dynamically for finishers
        const auto outputFinisherDevicesListTuple = media_->getFinisherDevices(dune::print::engine::DeviceOrder::DONT_CARE);
        const auto outputFinisherDevicesList = std::get<1>(outputFinisherDevicesListTuple);
        const APIResult outputFinisherListOK = std::get<0>(outputFinisherDevicesListTuple);

        auto hwFolderConnected {false};

        // Then add values from the finisher.
        if((outputFinisherDevicesList.size() > 0) && (outputFinisherListOK == APIResult::OK))
        {
            for(auto it : outputFinisherDevicesList)
            {
                auto lffolder = it->getLargeFormatFolder();
                if(lffolder != nullptr)
                {
                    // Get the lfp folder snapshot tuple which includes the snapshot pointer
                    auto snapTuple = lffolder->getSnapShot();
                    auto lfpFolderStatusVector_ = getStatusFromDevice(snapTuple);
                    
                    
                    auto foldingStyleVec = lffolder->getProperties().getFoldingStyles();

                    // Check if the folder is connected by checking if the status vector doesnt contain NOT_INSTALLED and
                    // the amount of folding styles is non zero.
                    hwFolderConnected = std::find(lfpFolderStatusVector_.begin(), lfpFolderStatusVector_.end(), DeviceStatus::NOT_INSTALLED) == lfpFolderStatusVector_.end() &&
                        foldingStyleVec.size() > 0;
                    if(hwFolderConnected){
                        for (const auto foldingStyle : foldingStyleVec)
                        {
                            stylesNames.push_back(foldingStyle.getName());

                            if (std::find(validValues.begin(), validValues.end(), (short)foldingStyle.getId()) == validValues.end())
                            {
                                CHECKPOINTB("CopyJobStaticConstraintRules::getFoldingStylesConstraints adding new valid values --> %hd ", (short)foldingStyle.getId());
                                validValues.push_back((short)foldingStyle.getId());
                            }

                            if (std::find(possibleValues.begin(), possibleValues.end(), (short)foldingStyle.getId()) == possibleValues.end())
                            {
                                CHECKPOINTB("CopyJobStaticConstraintRules::getFoldingStylesConstraints adding new possible values --> %hd ", (short)foldingStyle.getId());
                                possibleValues.push_back((short)foldingStyle.getId());
                            } 
                        }
                    }
                }
            }
        }

        if( !hwFolderConnected )
        {
            // Iterate each constraint in the constraints of this group to get the constraint we want.
            for( auto constraint : staticConstraints->getConstraints())
            {
                if( constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_SHORT)
                {
                    // Get the current valid values.
                    const std::vector<short> previousValidValues = static_cast<dune::framework::data::constraints::ValidValuesShort*>(constraint)->getValidValues();

                    // Add them to new vector.
                    for( auto value : previousValidValues)
                    {
                        validValues.push_back(value);
                    }
                }
                else if( constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::POSSIBLE_VALUE_SHORT)
                {
                    // Get the current possible values.
                    std::vector<short> previousPossibleValues = static_cast<dune::framework::data::constraints::PossibleValuesShort*>(constraint)->getPossibleValues();

                    // Add them to new vector.
                    for( auto value : previousPossibleValues)
                    {
                        possibleValues.push_back(value);
                    }
                }
            }
        }

        // Don't forget to remove previous constraints.
        staticConstraints->removeAll();

        std::string constrainedMessage = "";
        
        // Add lock constraint here if the media destination is not output.
        // This isn't in the .csf because there isn't a list of supported values we can write there.
        dune::imaging::types::MediaDestinationId currentOutputDestination = jobTicket->getIntent()->getOutputDestination();
        // Check if the job ticket table has a destination
        if (updatedJobTicketTable && updatedJobTicketTable->dest.get() && updatedJobTicketTable->dest.get()->print.get() )
        {
            // Get the media destination from the updated job ticket table.
            auto printTable = updatedJobTicketTable->dest.get()->print.get();
            auto isPatch = dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH;
            if (printTable->mediaDestination.isSet(isPatch))
            {
                currentOutputDestination = dune::job::cdm::mapFromCdm(printTable->mediaDestination.get());
            }
        }

        if( currentOutputDestination != dune::imaging::types::MediaDestinationId::FOLDER  &&
            currentOutputDestination != dune::imaging::types::MediaDestinationId::FOLDER2 &&
            currentOutputDestination != dune::imaging::types::MediaDestinationId::FOLDER3 &&
            currentOutputDestination != dune::imaging::types::MediaDestinationId::FOLDER4 )
        {
            // We also build the constraint message. This is a constraint checking a list of short values.
            // But we do not want to show numbers to the user, but the names of the folding styles instead.
            // We get them from the folder device and replicate the constraint message.
            constrainedMessage = localization_->deviceLocale()->get(dune::localization::string_id::cSettingsConfiguringIncompatible) + "\n\n";
            constrainedMessage += getStringIdForCdmSetting("dest/print/foldingStyleId") + "\n";

            for( std::string& name : stylesNames )
            {
                // Bullet point + value
                dune::localization::ParameterizedString parameterizedValueAffectedNameString(
                    dune::localization::string_id::cStringBullet,
                    name);

                constrainedMessage += localization_->deviceLocale()->format(&parameterizedValueAffectedNameString) + "\n";
            }

            constrainedMessage += "\n" + localization_->deviceLocale()->get(dune::localization::string_id::cIncompatibleSettings) + ":\n\n";
            constrainedMessage += getStringIdForCdmSetting("dest/print/mediaDestination") + "\n";

            // Bullet point + value
            dune::localization::ParameterizedString parameterizedValueAffectedNameString(
                dune::localization::string_id::cStringBullet,
                localization_->deviceLocale()->get(dune::localization::string_id::cStacker));

                constrainedMessage += localization_->deviceLocale()->format(&parameterizedValueAffectedNameString);

            staticConstraints->add(std::make_unique<dune::framework::data::constraints::Lock>(constrainedMessage));
        }

        // Add Possible/Valid values to Constraint
        std::string stringIdLocalized = constrainedMessage != "" ? constrainedMessage : 
            localization_->deviceLocale()->get(dune::localization::string_id::cUndefined);
        auto enumValidValuesConstraint = std::make_unique<dune::framework::data::constraints::ValidValuesShort>(validValues, stringIdLocalized);
        auto enumPossibleValuesConstraint = std::make_unique<dune::framework::data::constraints::PossibleValuesShort>(possibleValues, stringIdLocalized);
        
        staticConstraints->add(std::move(enumValidValuesConstraint));
        staticConstraints->add(std::move(enumPossibleValuesConstraint));
    }
    CHECKPOINTC("CopyJobStaticConstraintRules::getFoldingStylesConstraints Exit");
}

/* Functions which consolidate the calls to IMedia and gather all IMedia information for finishings. Call to IMedia needs to go thru
 * proxy and hence is expensive call.
 */
template<class DeviceTuple>
std::vector<DeviceStatus> CopyJobDynamicConstraintRulesLargeFormat::getStatusFromDevice( DeviceTuple& tuple ) const
{
    std::vector<DeviceStatus> statVec;
    if(std::get<0>(tuple) == APIResult::OK)
    {
        auto snapShaPtr = std::get<1>( tuple );
        statVec = snapShaPtr->getDeviceStatus();
    }
    else
    {
        CHECKPOINTA("CopyJobDynamicConstraintRulesLargeFormat: getStatusFromDevice:: failed to get snapTuple");
    }
    return statVec;
}

void CopyJobDynamicConstraintRulesLargeFormat::modifyValidValuesConstraintMediaSourceStatusDependantOutputScale(
    std::shared_ptr<dune::framework::data::constraints::Constraints> staticScaleToOutputConstraints,
    std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraintsScaleSelection)
{
    bool mediaSourceAvailable = false;
    if(staticScaleToOutputConstraints != nullptr)
    {
        auto validValues         = std::vector<dune::cdm::glossary_1::MediaSourceId>();
        auto possibleValues      = std::vector<dune::cdm::glossary_1::MediaSourceId>();
        auto previousValidValues = std::vector<dune::cdm::glossary_1::MediaSourceId>();

        for(auto constraint : staticScaleToOutputConstraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM)
            {
                previousValidValues = 
                    static_cast<dune::framework::data::constraints::ValidValuesEnum<dune::cdm::glossary_1::MediaSourceId>*>(constraint)->getValidValues();

                // Check If media (roll, tray, or similar) is on media source list  
                for (auto mediaSource : mapMediaSourcesStatus_)
                {
                    dune::cdm::glossary_1::MediaSourceId mediaSourceCdmValue = dune::job::cdm::mapToCdm(mediaSource.first);
                    bool mediaSourceReady = mediaSource.second;

                    auto iteratorPreviousValidValues = std::find(previousValidValues.begin(), previousValidValues.end(), mediaSourceCdmValue);

                    // Not add accepted valid value, if static constraints not accept them as they expected.
                    if (iteratorPreviousValidValues != previousValidValues.end() && mediaSourceReady)
                    {
                        mediaSourceAvailable = true;
                        CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat::"
                            "modifyValidValuesConstraintMediaSourceStatusDependantOutputScale mediaSource %d added as valid value", 
                            instanceName_, mediaSourceCdmValue);
                        validValues.push_back(mediaSourceCdmValue);
                    }
                }
            }            
            else if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::POSSIBLE_VALUE_ENUM)
            {
                possibleValues = static_cast<dune::framework::data::constraints::PossibleValuesEnum<dune::cdm::glossary_1::MediaSourceId>*>
                    (constraint)->getPossibleValues();
            }
        }

        // Refreshing values in current static constraints
        // In case of all source are not loaded, set previous valid values, Scale Selection will be the affected
        if(mediaSourceAvailable)
        {
            staticScaleToOutputConstraints->removeAll();
            auto enumValidValuesConstraint =    std::make_unique<dune::framework::data::constraints::ValidValuesEnum<dune::cdm::glossary_1::MediaSourceId>>
                ( validValues, dune::localization::string_id::cSingleRollOutOfPaper);
            auto enumPossibleValuesConstraint = std::make_unique<dune::framework::data::constraints::PossibleValuesEnum<dune::cdm::glossary_1::MediaSourceId>>
                (possibleValues,
                &dune::cdm::glossary_1::MediaSourceId::valueToString,
                dune::localization::string_id::cSingleRollOutOfPaper);
            staticScaleToOutputConstraints->add(std::move(enumValidValuesConstraint));
            staticScaleToOutputConstraints->add(std::move(enumPossibleValuesConstraint));
        }
        else
        {
            CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat::"
                "modifyValidValuesConstraintMediaSourceStatusDependantOutputScale mediaSourceAvailable not loaded!", instanceName_);

            auto scaleSelectionValidValues = std::vector<dune::cdm::jobTicket_1::scaling::ScaleSelection> ();
            auto scaleSelectionPossibleValues = std::vector<dune::cdm::jobTicket_1::scaling::ScaleSelection> ();

            if(staticConstraintsScaleSelection != nullptr)
            {
                for(auto constraint : staticConstraintsScaleSelection->getConstraints())
                {
                    if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM)
                    {
                        auto previousValidValues = 
                            static_cast<dune::framework::data::constraints::ValidValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>*>
                            (constraint)->getValidValues();
                        // Check If media (roll, tray, or similar) is on media source list  
                        for (auto &scaleSelection : previousValidValues)
                        {
                            // Not add accepted valid value, if static constraints not accept them as they expected.
                            if (scaleSelection != dune::cdm::jobTicket_1::scaling::ScaleSelection::scaleToOutput)
                            {
                                CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat::"
                                    "modifyValidValuesConstraintMediaSourceStatusDependantOutputScale scaleSelection %d added as valid value", 
                                    instanceName_, scaleSelection);
                                scaleSelectionValidValues.push_back(scaleSelection);
                            }
                        }
                    }
                    else if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::POSSIBLE_VALUE_ENUM)
                    {
                        scaleSelectionPossibleValues = static_cast<dune::framework::data::constraints::PossibleValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>*>
                            (constraint)->getPossibleValues();
                    }
                }

                // Refreshing values in current static constraints
                staticConstraintsScaleSelection->removeAll();
                auto enumValidValuesScaleSelectionConstraint =    std::make_unique<dune::framework::data::constraints::ValidValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>>
                    (scaleSelectionValidValues,   dune::localization::string_id::cOutOfPaperAllSourcesNoParameter);
                auto enumPossibleValuesScaleSelectionConstraint = std::make_unique<dune::framework::data::constraints::PossibleValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>>
                    (scaleSelectionPossibleValues,
                    &dune::cdm::jobTicket_1::scaling::ScaleSelection::valueToString,
                    dune::localization::string_id::cOutOfPaperAllSourcesNoParameter);
                    staticConstraintsScaleSelection->add(std::move(enumValidValuesScaleSelectionConstraint));
                    staticConstraintsScaleSelection->add(std::move(enumPossibleValuesScaleSelectionConstraint));
            }
            else
            {
                CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat::modifyValidValuesConstraintMediaSourceStatusDependantOutputScale"
                    " staticConstraintsScaleSelection is empty!", instanceName_);
            }
        }
    }
    else
    {
        CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat::modifyValidValuesConstraintMediaSourceStatusDependantOutputScale" 
            " staticConstraints is null!", instanceName_);
    }
}

void CopyJobDynamicConstraintRulesLargeFormat::modifyValidValuesConstraintMediaDestinationDependantCopyMode(
    std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints,
    std::shared_ptr<ICopyJobTicket> jobTicket)
{
    if(!staticConstraints)
    {
        CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat::modifyValidValuesConstraintMediaDestinationDependantCopyMode staticConstraints is null!", instanceName_);
        return;
    }
        
    //Chekc if folder option is available
    bool folderAvailable = false;
    for(auto constraint : staticConstraints->getConstraints())
    {
        if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::POSSIBLE_VALUE_ENUM)
        {
            std::vector<dune::cdm::glossary_1::MediaDestinationId> possibleValues = static_cast<dune::framework::data::constraints::PossibleValuesEnum<dune::cdm::glossary_1::MediaDestinationId>*>(constraint)->getPossibleValues();
            for(auto mediaDestination : possibleValues)
            {
                if(mediaDestination == dune::cdm::glossary_1::MediaDestinationId::folder_dash_1  || mediaDestination == dune::cdm::glossary_1::MediaDestinationId::folder_dash_2 ||
                   mediaDestination == dune::cdm::glossary_1::MediaDestinationId::folder_dash_3 || mediaDestination == dune::cdm::glossary_1::MediaDestinationId::folder_dash_4)
                {
                    folderAvailable = true;
                    break;
                }
            }
        }
    }

    // In case the folder is available and we are in direct copy mode, we need to remove folder as a valid value.
    // But only when ticket is associated to a created job, to allow set folder in Default ticket and User Quicksets in creation or edition.
    if(folderAvailable && 
        copyAdapter_->getCopyMode() == dune::cdm::copy_1::configuration::CopyMode::printWhileScanning &&
        jobTicket && jobTicket->getState() != dune::job::JobStateType::UNDEFINED)
    {
        CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat::modifyValidValuesConstraintMediaDestinationDependantCopyMode Direct copy mode and folder available, remove folder from valid values", instanceName_);
        // New values vector.
        auto validValues    = std::vector<dune::cdm::glossary_1::MediaDestinationId>();
        auto possibleValues = std::vector<dune::cdm::glossary_1::MediaDestinationId>();
        for(auto constraint : staticConstraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM)
            {
                const std::vector<dune::cdm::glossary_1::MediaDestinationId> previousValidValues = 
                    static_cast<dune::framework::data::constraints::ValidValuesEnum<dune::cdm::glossary_1::MediaDestinationId>*>(constraint)->getValidValues();
                for(auto value : previousValidValues)
                {
                    if(value != dune::cdm::glossary_1::MediaDestinationId::folder_dash_1 && value != dune::cdm::glossary_1::MediaDestinationId::folder_dash_2 &&
                       value != dune::cdm::glossary_1::MediaDestinationId::folder_dash_3 && value != dune::cdm::glossary_1::MediaDestinationId::folder_dash_4)
                    {
                        CHECKPOINTC("%s/CopyJobDynamicConstraintRulesLargeFormat::modifyValidValuesConstraintMediaDestinationDependantCopyMode"
                            " mediaDestination %d added as valid value", instanceName_, value);
                        validValues.push_back(value);
                    }
                }
            }
            else if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::POSSIBLE_VALUE_ENUM)
            {
                possibleValues = static_cast<dune::framework::data::constraints::PossibleValuesEnum<dune::cdm::glossary_1::MediaDestinationId>*>
                    (constraint)->getPossibleValues();
            }
        }

        //Create constrained message
        std::string constrainedMessage = localization_->deviceLocale()->get(dune::localization::string_id::cSettingsConfiguringIncompatible) + "\n\n";
        constrainedMessage += getStringIdForCdmSetting("dest/print/mediaDestination") + "\n";

        // Bullet point + value
        dune::localization::ParameterizedString parameterizedValueAffectedNameString(
            dune::localization::string_id::cStringBullet,
            getStringIdForCdmValueSetting("dest/print/mediaDestination", "folder"));
        
        constrainedMessage +=  localization_->deviceLocale()->format(&parameterizedValueAffectedNameString);

        constrainedMessage += "\n\n" + localization_->deviceLocale()->get(dune::localization::string_id::cIncompatibleSettings) + ":\n\n";
        constrainedMessage += localization_->deviceLocale()->get(dune::localization::string_id::cCopyMode) + "\n";
         
        // Bullet point + value
        dune::localization::ParameterizedString parameterizedValueIncompatibleNameString(
            dune::localization::string_id::cStringBullet,
            localization_->deviceLocale()->get(dune::localization::string_id::cCopySendAutomatically));
        constrainedMessage += localization_->deviceLocale()->format(&parameterizedValueIncompatibleNameString);

        // Don't forget to remove previous constraints.
        staticConstraints->removeAll();
        staticConstraints->add(std::make_unique<dune::framework::data::constraints::Lock>(constrainedMessage));
        //Remove previous constraints and add new ones
        auto enumValidValuesConstraint = std::make_unique<dune::framework::data::constraints::ValidValuesEnum<dune::cdm::glossary_1::MediaDestinationId>>
            (validValues, constrainedMessage);
        staticConstraints->add(std::move(enumValidValuesConstraint));
        auto enumPossibleValuesConstraint = std::make_unique<dune::framework::data::constraints::PossibleValuesEnum<dune::cdm::glossary_1::MediaDestinationId>>
            (possibleValues,
            &dune::cdm::glossary_1::MediaDestinationId::valueToString, 
            constrainedMessage);
        staticConstraints->add(std::move(enumPossibleValuesConstraint));
    }
}

void CopyJobDynamicConstraintRulesLargeFormat::updateWithJobDynamicConstraints(std::shared_ptr<ICopyJobTicket> jobTicket, 
                                                                               std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> constraintsGroup)
{
    CHECKPOINTD("CopyJobDynamicConstraintRulesLargeFormat::updateWithJobDynamicConstraints Enter, job state %d",(int)jobTicket->getState());

    //Lock some settings between pages -> Processing state
    if(jobTicket->getState() == dune::job::JobStateType::PROCESSING)
    {
        for(const auto &blockedSetting : configuration_->blockedSettingsBetweenPages)
        {
            CHECKPOINTC("CopyJobDynamicConstraintRulesLargeFormat::updateWithJobDynamicConstraints blocked setting: %s", blockedSetting.c_str());

            std::shared_ptr<dune::framework::data::constraints::Constraints> constraints = constraintsGroup->getConstraints(blockedSetting);

            if(constraints != nullptr)
            {
                CHECKPOINTC("CopyJobDynamicConstraintRulesLargeFormat::updateWithJobDynamicConstraints creation of lock sentence");

                // Remove any constraints related with LOCK.
                constraints->remove(
                    [](const dune::framework::data::constraints::IConstraint& constraint)
                    { 
                        return constraint.getConstraintType() == dune::framework::data::constraints::ConstraintType::LOCK; 
                    }
                );

                // Get string id localized
                std::string settingName = getStringIdForCdmSetting(blockedSetting);
                
                // Generate and set message id
                dune::localization::ParameterizedString parameterizedString(dune::localization::string_id::cMessageNotAllowModifySettings, 
                    settingName); 
                std::string message = localization_->deviceLocale()->format(&parameterizedString);
                constraints->add(std::make_unique<dune::framework::data::constraints::Lock>(message));
            }
        }
    } 
    CHECKPOINTD("CopyJobDynamicConstraintRulesLargeFormat::updateWithJobDynamicConstraints Exit");
}

std::string CopyJobDynamicConstraintRulesLargeFormat::getStringIdForCdmSetting(const std::string &cdmSettingPath)
{
    // Try to find string id on map
    std::vector<std::string> vectorStringFromCsf;
    if(!configuration_->vectorMapStringIdForSettings.empty())
    {
        std::vector<std::shared_ptr<CopyIntentStringIdMapT>>::iterator iterator = std::find_if(configuration_->vectorMapStringIdForSettings.begin(), configuration_->vectorMapStringIdForSettings.end(), 
            [&](std::shared_ptr<CopyIntentStringIdMapT> keyValue)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getStringIdForCdmSetting find if setting %s, checking setting %s on string map with string id %s",
                    cdmSettingPath.c_str(),keyValue->settingName.c_str(),((keyValue->vectorStringId).back()).c_str());
                return (keyValue->settingName == cdmSettingPath);
            }
        );

        if ( iterator != configuration_->vectorMapStringIdForSettings.end())
        {
            vectorStringFromCsf = (*iterator)->vectorStringId;
            CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getStringIdForCdmSetting setting %s founded stringName %s", cdmSettingPath.c_str(),(vectorStringFromCsf.back()).c_str());
        }
        else
        {
            CHECKPOINTB("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getStringIdForCdmSetting setting %s without string id", cdmSettingPath.c_str());
        }
    }
    // Get String id localized, if string id was founded, generated with device locale, get id from csf method
    std::string settingName = "";
    if(vectorStringFromCsf.empty())
    {
        settingName = localization_->deviceLocale()->get(dune::localization::string_id::cThisOptionUnavailable);
    }
    else 
    {
        settingName = localization_->deviceLocale()->get(localization_->deviceLocale()->getStringIdForCsfOnly( (*vectorStringFromCsf.begin()).c_str() ));
        for(auto it = vectorStringFromCsf.begin() + 1; it != vectorStringFromCsf.end(); ++it)
        {
            dune::localization::ParameterizedString parameterizedSettingNameString(dune::localization::string_id::cMultilevelSettingSeparator, settingName, 
                    localization_->deviceLocale()->get(localization_->deviceLocale()->getStringIdForCsfOnly((*it).c_str())));
            settingName = localization_->deviceLocale()->format(&parameterizedSettingNameString);
        }
    }

    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getStringIdForCdmSetting setting id localized %s", settingName.c_str());
    return settingName;
}

std::string CopyJobDynamicConstraintRulesLargeFormat::getStringIdForCdmValueSetting(const std::string &cdmSettingPath, const std::string &valueAsString)
{
    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getStringIdForCdmValueSetting enter");
    // Try to find string id on map
    std::string stringFromCsf;
    if(!configuration_->vectorMapStringIdForSettings.empty())
    {
        std::vector<std::shared_ptr<CopyIntentStringIdMapT>>::iterator iterator = std::find_if(configuration_->vectorMapStringIdForSettings.begin(), configuration_->vectorMapStringIdForSettings.end(), 
            [&](std::shared_ptr<CopyIntentStringIdMapT> keyValue)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getStringIdForCdmValueSetting find if setting %s, checking setting %s on string map with string id %s",
                    cdmSettingPath.c_str(),keyValue->settingName.c_str(),((keyValue->vectorStringId).back()).c_str());
                return (keyValue->settingName == cdmSettingPath);
            }
        );
        
        if ( iterator != configuration_->vectorMapStringIdForSettings.end())
        {
            CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getStringIdForCdmValueSetting setting %s founded", cdmSettingPath.c_str());
            std::vector<std::shared_ptr<CopyIntentStringIdValueMapT>> vectorMap = (*iterator)->stringIdsForValuesOfSetting;
            std::vector<std::shared_ptr<CopyIntentStringIdValueMapT>>::iterator iteratorVectorMap = std::find_if(vectorMap.begin(), vectorMap.end(), 
                [&](std::shared_ptr<CopyIntentStringIdValueMapT> keyValue)
                {
                    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getStringIdForCdmValueSetting find if valueAsString %s, checking setting value %s on string map with string id %s",
                        valueAsString.c_str(),keyValue->settingNameValue.c_str(),keyValue->stringId.c_str());
                    return (keyValue->settingNameValue == valueAsString);
                }
            );

            // Take value from map if setting value exist
            if(iteratorVectorMap != vectorMap.end())
            {
                stringFromCsf = (*iteratorVectorMap)->stringId;
                CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getStringIdForCdmValueSetting setting value %s string id from csf %s", valueAsString.c_str(),stringFromCsf.c_str());
            }
            else
            {
                CHECKPOINTB("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getStringIdForCdmValueSetting setting value %s without string id", valueAsString.c_str());
            }
        }
        else
        {
            CHECKPOINTB("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getStringIdForCdmValueSetting setting %s without string id", cdmSettingPath.c_str());
        }
    }

    // Get String id localized, if string id was founded, generated with device locale, get id from csf method
    std::string settingValueName = (stringFromCsf != "") 
        ? localization_->deviceLocale()->get(localization_->deviceLocale()->getStringIdForCsfOnly( stringFromCsf.c_str() ))
        : localization_->deviceLocale()->get(dune::localization::string_id::cThisOptionUnavailable);

    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::getStringIdForCdmValueSetting setting id localized %s", settingValueName.c_str());
    return settingValueName;
}

std::string CopyJobDynamicConstraintRulesLargeFormat::getConstrainedMessage(const std::string &settingName, 
    std::vector<std::shared_ptr<CopyIntentTableValueT>> valuesAffected, 
    std::unordered_map<std::string,std::vector<std::shared_ptr<CopyIntentTableValueT>>> mapSettingsThatCauseConstraint)
{
    CHECKPOINTD("CopyJobDynamicConstraintRulesLargeFormat::getConstrainedMessage enter");
    
    dune::localization::ParameterizedString parameterizedIncompatibleSettingString(dune::localization::string_id::cStringColon,
                dune::localization::string_id::cIncompatibleSettings);

    // Complete message generation
    std::string messageResult = localizeValuesOfSettingAffected(settingName,valuesAffected) // Setting affected
        + "\n\n"                                                                            // Next line and single separation between selected option and not compatible option.
        + localization_->deviceLocale()->format(&parameterizedIncompatibleSettingString)    // Incompatible setting header
        + "\n"
        + localizeSettingsRowThatAffectToConstraint(mapSettingsThatCauseConstraint);        // Incompatible settings

    CHECKPOINTD("CopyJobDynamicConstraintRulesLargeFormat::getConstrainedMessage exit");

    return messageResult;
}

std::string CopyJobDynamicConstraintRulesLargeFormat::localizeValuesOfSettingAffected(const std::string &settingName, std::vector<std::shared_ptr<CopyIntentTableValueT>> valuesAffected)
{
    CHECKPOINTD("CopyJobDynamicConstraintRulesLargeFormat::localizeValuesOfSettingAffected enter");
    std::string valuesAffectedLocalized = "";

    // Not set values if there is not vector
    if(!valuesAffected.empty())
    {
        for(auto intentValue : valuesAffected)
        {
            bool wasLocalized = false;
            std::string valueAffected = FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValue,wasLocalized,localization_);
            std::string valueAffectedLocalized = "";
            if(wasLocalized)
            {
                valueAffectedLocalized = valueAffected;
            }
            else
            {
                // Bullet point + value
                dune::localization::ParameterizedString parameterizedValueAffectedNameString(
                    dune::localization::string_id::cStringBullet,
                    getStringIdForCdmValueSetting(settingName,valueAffected));

                valueAffectedLocalized = localization_->deviceLocale()->format(&parameterizedValueAffectedNameString);
            }

            // First time set directly the value affected
            if(valuesAffectedLocalized == "")
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::localizeValuesOfSettingAffected first value");
                valuesAffectedLocalized = valueAffectedLocalized;
            }
            else
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::localizeValuesOfSettingAffected next value, concat strings");
                // Generate new parametrized message
                // Bullet point + value \n Bullet point + value etc... replicated
                valuesAffectedLocalized = valuesAffectedLocalized + "\n" + valueAffectedLocalized;
            }
        }
    }

    CHECKPOINTD("CopyJobDynamicConstraintRulesLargeFormat::localizeValuesOfSettingAffected exit");

    std::string result = localization_->deviceLocale()->get(dune::localization::string_id::cSettingsConfiguringIncompatible)
        + "\n\n"
        + getStringIdForCdmSetting(settingName)
        + "\n"
        + valuesAffectedLocalized;

    return result;
}

std::string CopyJobDynamicConstraintRulesLargeFormat::localizeSettingsRowThatAffectToConstraint(std::unordered_map<std::string,std::vector<std::shared_ptr<CopyIntentTableValueT>>> mapSettingsThatCauseConstraint)
{
    CHECKPOINTD("CopyJobDynamicConstraintRulesLargeFormat::localizeSettingsRowThatAffectToConstraint enter");

    std::string settingsCombinedMessageLocalized = "";
    if(!mapSettingsThatCauseConstraint.empty())
    {
        for(auto keyValues : mapSettingsThatCauseConstraint)
        {
            std::string valuesSettingLocalized = "";
            for(auto intentValue : keyValues.second)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::localizeSettingsRowThatAffectToConstraint checking intent value");
                // Localize value of setting
                bool wasLocalized = false;
                std::string valueAffected = FlatBufferParserToCdmType::parseCopyIntentTableValueToString(intentValue,wasLocalized,localization_);
                std::string valueAffectedLocalized = "";
                if(wasLocalized)
                {
                    valueAffectedLocalized = valueAffected;
                }
                else
                {
                    dune::localization::ParameterizedString parameterizedValueAffectedNameString(dune::localization::string_id::cStringBullet,
                            getStringIdForCdmValueSetting(keyValues.first,valueAffected));
                    valueAffectedLocalized = localization_->deviceLocale()->format(&parameterizedValueAffectedNameString);
                }
                
                //First value on list
                if(valuesSettingLocalized == "")
                {
                    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::localizeSettingsRowThatAffectToConstraint checking intent value - first value");
                    valuesSettingLocalized = valueAffectedLocalized;
                }
                // Next iterations
                else
                {
                    CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::localizeSettingsRowThatAffectToConstraint checking intent value - next value iteration");
                    // Bullet point + value \n Bullet point + value etc... replicated
                    valuesSettingLocalized = valuesSettingLocalized + "\n" + valueAffectedLocalized;
                }
            }
            // <setting>:
            // - value
            // - value
            // etc...
            std::string settingRowLocalized = "\n"
                + getStringIdForCdmSetting(keyValues.first)
                + "\n"
                + valuesSettingLocalized;
            
            // First setting, set directly
            if(settingsCombinedMessageLocalized == "")
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::localizeSettingsRowThatAffectToConstraint first string");
                settingsCombinedMessageLocalized = settingRowLocalized;
            }
            // Next iterations, concatenate settings
            else
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesLargeFormat::localizeSettingsRowThatAffectToConstraint next string localized to concatenate");
                settingsCombinedMessageLocalized = settingsCombinedMessageLocalized + "\n" + settingRowLocalized;
            }
        }       
    }
    
    CHECKPOINTD("CopyJobDynamicConstraintRulesLargeFormat::localizeSettingsRowThatAffectToConstraint exit");
    return settingsCombinedMessageLocalized;
}

void CopyJobDynamicConstraintRulesLargeFormat::modifyConstraintsAffectedByCurrentMeasureUnit(std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> staticConstraints)
{
    CHECKPOINTD("CopyJobDynamicConstraintRulesLargeFormat::modifyConstraintsAffectedByCurrentMeasureUnit enter");

    if(configuration_ && !configuration_->listOfSettingsAffectedByMeasurementUnit.empty() && 
       staticConstraints && !staticConstraints->getAllConstraints().empty())
    {
        for(auto& settingAffected : configuration_->listOfSettingsAffectedByMeasurementUnit)
        {
            auto originalConstraint = staticConstraints->getConstraints(settingAffected->settingName);
            if(originalConstraint != nullptr)
            {
                CHECKPOINTD("CopyJobDynamicConstraintRulesLargeFormat::modifyConstraintsAffectedByCurrentMeasureUnit checking constraint unit value");

                std::shared_ptr<ConstrainedValuesT> constraintValues = std::make_shared<ConstrainedValuesT>();

                if(localization_ && localization_->getMeasurmentUnit() == dune::localization::MeasurementUnit::METRIC)
                {
                    CHECKPOINTC("CopyJobDynamicConstraintRulesLargeFormat::modifyConstraintsAffectedByCurrentMeasureUnit checking constraint unit value mm");

                    constraintValues->supportedValues = settingAffected->supportedValuesForMetric;
                }
                else // By default if there is not measurement unit accessible, set inches size
                {
                    CHECKPOINTC("CopyJobDynamicConstraintRulesLargeFormat::modifyConstraintsAffectedByCurrentMeasureUnit checking constraint unit value inches");
                    constraintValues->supportedValues = settingAffected->supportedValuesForUS;
                }
                
                auto newConstraints = createConstraintFromRule(constraintValues,settingAffected->settingName,originalConstraint);
                staticConstraints->set(settingAffected->settingName, newConstraints);
            }
        }
    }

    CHECKPOINTD("CopyJobDynamicConstraintRulesLargeFormat::modifyConstraintsAffectedByCurrentMeasureUnit exit");
}

void CopyJobDynamicConstraintRulesLargeFormat::setValueIgnoreGenerationConstraints(const bool value)
{
    ignoreGenerationConstraints_ = value;
}

}}}}  // namespace dune::copy::Jobs::Copy
