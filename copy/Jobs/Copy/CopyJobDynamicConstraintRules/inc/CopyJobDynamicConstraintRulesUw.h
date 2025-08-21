/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_UW_H
#define DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_UW_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesUw.h
 * @date   Mon, 11 Jul 2022 11:20:06 +0200
 * @brief  Component used to manage the Dynamic Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

namespace dune { namespace copy { namespace Jobs { namespace Copy {
/**
 * @brief Interface exported to interpreters, also known as "underware
 * interface".
 */
class CopyJobDynamicConstraintRulesUw
{
public:

    /**
     * Destructor.
     */
    virtual ~CopyJobDynamicConstraintRulesUw() { }

    // @todo add pure virtual methods of the interface here.

    /**
     * @brief Disable/enable dynamic constraint generation
     * @param value true if disable dynamic constraints generation, false if no
     */
    virtual void PUB_disableDynamicConstraints(const bool value) = 0;
};

}}}}  // namespace dune::copy::Jobs::Copy


#endif  // DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_UW_H

