/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_I_JOB_CONSTRAINTS_H
#define DUNE_COPY_JOBS_COPY_I_JOB_CONSTRAINTS_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   IJobConstraints.h
 * @date   Tue, 05 Jul 2022 08:29:10 +0200
 * @brief  Component used to manage the Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "ComponentSystemTypes.h"

#include "ConstraintsGroup.h"
#include "CopyJobTicket.h"
#include "ITicketAdapter.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {
/**
 * @brief Component used to manage the Copy Job Constraints
 *
 * @todo describe the main responsibilities and interactions of the
 * component(s) realizing this interface.
 */
class ICopyJobTicket;
class IJobConstraints
{
public:

    /**
     * Destructor.
     */
    virtual ~IJobConstraints() { }

    // @todo add pure virtual methods of the interface here.
    /**
     * @brief getConstraints
     * @param jobTicket. CopyJob Ticket associated with the constraints 
     * @param ticketAdapter The ticket adapter (used for it's 'supportsProperty' method) 
     * @return Return the copy and scan constraints grouped
     */
    virtual std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> getConstraints(
        std::shared_ptr<ICopyJobTicket> jobTicket, dune::job::ITicketAdapter& ticketAdapter ) = 0;

    /**
     * @brief getFbConstraintsTableFromConfiguration. It reads the .bin file from the .csf configuration and 
     * returns the constraints Flatbuffer table
     * @return Return the copy and scan constraints in a Flattbuffers table
     */
    virtual std::shared_ptr<CopyJobConstraintsFbT> getFbConstraintsTableFromConfiguration(void) = 0;
};

}}}}  // namespace dune::copy::Jobs::Copy

DEFINE_INTERFACE_UID(dune::copy::Jobs::Copy::IJobConstraints, 0xf7a0c7);

#endif  // DUNE_COPY_JOBS_COPY_I_JOB_CONSTRAINTS_H

