/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_STANDARD_H
#define DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_STANDARD_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesStandard.h
 * @date   Mon, 11 Jul 2022 11:20:06 +0200
 * @brief  Component used to manage the Dynamic Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "IComponent.h"
#include "ICopyJobDynamicConstraintRules.h"
#include "ICopyAdapter.h"
#include "CopyJobConstraintRules.h"
#include "StringIds.h"
#include "IMediaConstraints.h"
#include "IScanConstraints.h"
#include "IColorAccessControl.h"

#include "CopyJobDynamicConstraintRulesStandardConfig_generated.h"

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_Jobs_Copy_CopyJobDynamicConstraintRulesStandard);

namespace dune { namespace copy { namespace Jobs { namespace Copy {
// Forward declaration.
class CopyJobDynamicConstraintRulesStandardUwAdapter;
using IColorAccessControl = dune::imaging::IColorAccessControl;
using ColorAccess = dune::imaging::ColorAccess;
/**
 * Implementation of the Standard flavor of the CopyJobDynamicConstraintRules component.
 */
class CopyJobDynamicConstraintRulesStandard:
    public dune::framework::component::IComponent,
    public ICopyJobDynamicConstraintRules,
    public CopyJobConstraintRules
{
public:

    /**
     * @name ICopyJobDynamicConstraintRules methods.
     * @{
     */

    /// @todo redeclare methods from ICopyJobDynamicConstraintRules here (don't forget the 'override' clause).
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
    bool checkAndApplyForceSets(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, 
        std::shared_ptr<ICopyJobTicket> ticket, 
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> currentConstraintsGroup,
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup>   staticConstraintsGroup = nullptr) override;

    /**
     * @brief Update existing constraints wth job dynamic constraints
     * @param jobTicket CopyJob Ticket associated with the constraints 
     * @param constraintsGroup constraints grouped to be updated
     */
    void updateWithJobDynamicConstraints(std::shared_ptr<ICopyJobTicket> jobTicket, 
                                         std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> constraintsGroup) override;

    /**
     * @}
     */

    /**
     * @brief CopyJobDynamicConstraintRulesStandard Constructor.
     *
     * @param instanceName the name of the component instance.
     */
    explicit CopyJobDynamicConstraintRulesStandard(const char *instanceName);

    /**
     * Destructor.
     */
    virtual ~CopyJobDynamicConstraintRulesStandard();

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
     * overridden to check 'copyAdapter_->getColorCopyEnabled()'.
     */
    bool hasColorPermission(std::shared_ptr<ICopyJobTicket> jobTicket) override;
    bool isColorRestricted(std::shared_ptr<ICopyJobTicket> jobTicket) override;

private:

    /**
     * @brief Method to check if a constraint is supported to be modified by dynamic component     
     * @param cdmPathName path of the cdm to be checked
     * @param staticConstraintsGroup constraints from static
     * @return true if exist
     * @return false if no
     */
    bool checkIfConstraintIsSupported(std::string cdmPathName, std::shared_ptr<ICopyJobTicket> jobTicket);

    std::unique_ptr<dune::copy::Jobs::copy::CopyJobDynamicConstraintRulesStandardConfigT> getConfiguration(dune::framework::resources::IConfigurationService *configurationService) const;

    const char *instanceName_; ///< The instance name.
    dune::framework::underware::InterpreterEnvironment * interpreterEnvironment_; ///< The environment where underwares are to be registered
    dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesStandardUwAdapter *uwAdapter_; ///< The underware object adapter.
    dune::copy::cdm::ICopyAdapter* copyAdapter_{nullptr};
    dune::print::engine::constraints::IMediaConstraints* mediaConstraints_{nullptr};
    dune::scan::IScanConstraints* scanConstraintsHelper_{nullptr};
    std::unique_ptr<dune::copy::Jobs::copy::CopyJobDynamicConstraintRulesStandardConfigT>       configuration_{nullptr};  ///< The instance's constants configuration    
    IColorAccessControl *colorAccessControlInst_{nullptr};

    // TODO:
    // we can remove this wart (constraintsStringIds_) once we move the scanJobConstraintsRules into a component.
    std::vector<dune::localization::StringId> constraintsStringIds_ = {
            string_id::cScanningScanGlass
    };
};

}}}}  // namespace dune::copy::Jobs::Copy

DEFINE_MODULE_UID(dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesStandard, 0xe76f80);

DESCRIBE_COMPONENT_FLAVOR_BEGIN(dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesStandard)
    PROVIDES_INTERFACE(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules)
    REQUIRES_INTERFACE(dune::imaging::ColorAccessControl::IColorAccessControl)
DESCRIBE_COMPONENT_FLAVOR_END(dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesStandard)


#endif  // DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_STANDARD_H

