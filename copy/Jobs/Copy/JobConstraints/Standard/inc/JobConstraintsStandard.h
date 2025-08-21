/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_JOB_CONSTRAINTS_STANDARD_H
#define DUNE_COPY_JOBS_COPY_JOB_CONSTRAINTS_STANDARD_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobConstraintsStandard.h
 * @date   Tue, 05 Jul 2022 08:29:10 +0200
 * @brief  Component used to manage the Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "IComponent.h"
#include "IJobConstraints.h"
#include "JobConstraintsStandardConfig_generated.h"
#include "ICopyJobDynamicConstraintRules.h"
#include "IScanConstraints.h"

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_Jobs_Copy_JobConstraintsStandard);

namespace dune { namespace copy { namespace Jobs { namespace Copy {

using namespace dune::framework::data::constraints;
using namespace dune::cdm::jobTicket_1;

// Forward declaration.
class JobConstraintsStandardUwAdapter;

/**
 * Implementation of the Standard flavor of the JobConstraints component.
 */
class JobConstraintsStandard:
    public dune::framework::component::IComponent,
    public IJobConstraints
{
public:

    /**
     * @name IJobConstraints methods.
     * @{
     */

    /// @todo redeclare methods from IJobConstraints here (don't forget the 'override' clause).
    /**
     * @brief getConstraints
     * @param jobTicket. CopyJob Ticket associated with the constraints 
     * @param ticketAdapter. ticketAdapter used for it's 'supportsProperty' method. 
     * @return Return the copy and scan constraints grouped
     */
    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> getConstraints(
        std::shared_ptr<ICopyJobTicket> jobTicket, dune::job::ITicketAdapter& ticketAdapter ) override;

    /**
     * @brief getFbConstraintsTableFromConfiguration. It reads the .bin file from the .csf configuration and 
     * returns the constraints Flatbuffer table
     * @return Return the copy and scan constraints in a Flattbuffers table
     */
    std::shared_ptr<CopyJobConstraintsFbT> getFbConstraintsTableFromConfiguration(void) override;

    /**
     * @}
     */

    /**
     * @brief JobConstraintsStandard Constructor.
     *
     * @param instanceName the name of the component instance.
     */
    explicit JobConstraintsStandard(const char *instanceName);

    /**
     * Destructor.
     */
    virtual ~JobConstraintsStandard();

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
    /**
     * @brief Loads the configuration for this component instance
     *
     * @param configurationService the pointer to the system's configuration service
     * @return the configuration values to be used by this instance, according to the system's product and proto
     *         versions or nullptr if the configuration is not available for this instance.
     */
    std::unique_ptr<JobConstraintsStandardConfigT> getConfiguration(dune::framework::resources::IConfigurationService *configurationService) const;
    
private:

    const char                                          *instanceName_; ///< The instance name.
    std::unique_ptr<JobConstraintsStandardConfigT>       configuration_{nullptr};  ///< The instance's constants configuration    
    std::shared_ptr<CopyJobConstraintsFbT> constraints_{nullptr};
    dune::framework::underware::InterpreterEnvironment * interpreterEnvironment_; ///< The environment where underwares are to be registered
    dune::copy::Jobs::Copy::JobConstraintsStandardUwAdapter *uwAdapter_; ///< The underware object adapter.
    dune::scan::IScanConstraints                        *scanConstraints_{ nullptr }; ///< interface to obtain the Scan constraints.

    /**
     * This function should be deleted after moving the contained logic into the scan job constraints rules.
     * The logic which disables some properties should be moved into various
     * 'getXXXConstraints(jobTicket) functions in the scan job constraint rules.
     * 
     * @brief Checks the current ticket for incompatible configurations. If found, it changes the constraints accordingly.
     * @param constraintsGroup Group of constraints to be modified.
     */
    void checkIncompatibleTicketConfigurations(std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> constraintsGroup, 
        std::shared_ptr<ICopyJobTicket> jobTicket);

    void updateScanConstraints(std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> scanConstraintsGroup, std::shared_ptr<ICopyJobTicket> jobTicket);    

    dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules * copyJobDynamicConstraintRules_;

};

}}}}  // namespace dune::copy::Jobs::Copy

DEFINE_MODULE_UID(dune::copy::Jobs::Copy::JobConstraintsStandard, 0x36f65a);

DESCRIBE_COMPONENT_FLAVOR_BEGIN(dune::copy::Jobs::Copy::JobConstraintsStandard)
    PROVIDES_INTERFACE(dune::copy::Jobs::Copy::IJobConstraints)
    REQUIRES_INTERFACE(dune::scan::IScanConstraints)
DESCRIBE_COMPONENT_FLAVOR_END(dune::copy::Jobs::Copy::JobConstraintsStandard)


#endif  // DUNE_COPY_JOBS_COPY_JOB_CONSTRAINTS_STANDARD_H

