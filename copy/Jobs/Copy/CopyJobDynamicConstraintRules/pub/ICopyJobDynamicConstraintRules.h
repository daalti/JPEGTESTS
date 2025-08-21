/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_I_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_H
#define DUNE_COPY_JOBS_COPY_I_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   ICopyJobDynamicConstraintRules.h
 * @date   Thu, 07 Jul 2022 08:23:03 +0200
 * @brief  Component used to manage the Dynamic Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "ComponentSystemTypes.h"
#include "ConstraintsGroup.h"
#include "com.hp.cdm.service.jobTicket.version.1.easybuffers_autogen.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

class ICopyJobTicket;
/**
 * @brief Component used to manage the Dynamic Copy Job Constraints
 *
 * @todo describe the main responsibilities and interactions of the
 * component(s) realizing this interface.
 */
class ICopyJobDynamicConstraintRules
{
public:

    /**
     * Destructor.
     */
    virtual ~ICopyJobDynamicConstraintRules() { }

    // @todo add pure virtual methods of the interface here.
    /**
     * @brief getDynamicConstraints
     * @param jobTicket. CopyJob Ticket associated with the constraints 
     * @param staticConstraintsGroup static constraints from previous step, if needed take data from here
     * @return Return the dynamic constraints grouped
     */
    virtual std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> getDynamicConstraints(
        std::shared_ptr<ICopyJobTicket> jobTicket, std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> staticConstraintsGroup,
        const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable = nullptr) = 0;

    /**
     * @brief Method to force change on ticket if needed
     * @param updatedJobTicketTable ticket updated
     * @param ticket current ticket     
     * @param currentConstraintsGroup current constraints to apply force set check
     * @return Return if constraints was applied and need to be updated again
     */
    virtual bool checkAndApplyForceSets(const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, 
        std::shared_ptr<ICopyJobTicket> ticket, 
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> currentConstraintsGroup,
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> staticConstraintsGroup = nullptr) = 0;

    /**
     * @brief Update existing constraints wth job dynamic constraints
     * @param jobTicket CopyJob Ticket associated with the constraints 
     * @param constraintsGroup constraints grouped to be updated
     */
    virtual void updateWithJobDynamicConstraints(std::shared_ptr<ICopyJobTicket> jobTicket, std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> constraintsGroup) = 0;
    
};

}}}}  // namespace dune::copy::Jobs::Copy

DEFINE_INTERFACE_UID(dune::copy::Jobs::Copy::ICopyJobDynamicConstraintRules, 0x2314f6);

#endif  // DUNE_COPY_JOBS_COPY_I_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_H

