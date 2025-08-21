/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_STANDARD_UW_ADAPTER_H
#define DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_STANDARD_UW_ADAPTER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesStandardUwAdapter.h
 * @date   Mon, 11 Jul 2022 11:20:06 +0200
 * @brief  Component used to manage the Dynamic Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobDynamicConstraintRulesUw.h"
#include "CopyJobDynamicConstraintRulesStandard.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

/**
 * Underware object adapter between CopyJobDynamicConstraintRulesUw and CopyJobDynamicConstraintRulesStandard.
 */
class CopyJobDynamicConstraintRulesStandardUwAdapter: public CopyJobDynamicConstraintRulesUw
{
public:

    /**
     * Constructor.
     *
     * @param interpreterEnvironment InterpreterEnvironment system service.
     * @param instanceName name of the instance exported to the interpreter.
     * @param adaptee pointer to the CopyJobDynamicConstraintRulesStandard instance.
     */
    CopyJobDynamicConstraintRulesStandardUwAdapter(dune::framework::underware::InterpreterEnvironment * interpreterEnvironment,
                    const char * instanceName, CopyJobDynamicConstraintRulesStandard * adaptee);

    /**
     * Destructor.
     */
    virtual ~CopyJobDynamicConstraintRulesStandardUwAdapter( );

    /**
     * @name CopyJobDynamicConstraintRulesUw methods.
     * @{
     */

    // @todo redeclare methods from CopyJobDynamicConstraintRulesUw here

    /**
     * @}
     */
    
    /**
     * @brief Disable/enable dynamic constraint generation
     * @param value true if disable dynamic constraints generation, false if no
     */
    void PUB_disableDynamicConstraints(const bool value) override;

private:

    dune::framework::underware::InterpreterEnvironment * interpreterEnvironment_;
    const char * instanceName_;
    CopyJobDynamicConstraintRulesStandard * adaptee_; ///< Pointer to the underlying CopyJobDynamicConstraintRulesStandard object.
};

}}}}  // namespace dune::copy::Jobs::Copy


#endif  // DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_STANDARD_UW_ADAPTER_H

