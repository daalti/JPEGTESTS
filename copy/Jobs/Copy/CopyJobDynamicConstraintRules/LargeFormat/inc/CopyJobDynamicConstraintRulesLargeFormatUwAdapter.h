/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_LARGE_FORMAT_UW_ADAPTER_H
#define DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_LARGE_FORMAT_UW_ADAPTER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesLargeFormatUwAdapter.h
 * @date   Tue, 11 Oct 2022 11:20:06 +0200
 * @brief  Component used to manage the Dynamic Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobDynamicConstraintRulesUw.h"
#include "CopyJobDynamicConstraintRulesLargeFormat.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

/**
 * Underware object adapter between CopyJobDynamicConstraintRulesUw and CopyJobDynamicConstraintRulesLargeFormat.
 */
class CopyJobDynamicConstraintRulesLargeFormatUwAdapter: public CopyJobDynamicConstraintRulesUw
{
public:

    /**
     * Constructor.
     *
     * @param interpreterEnvironment InterpreterEnvironment system service.
     * @param instanceName name of the instance exported to the interpreter.
     * @param adaptee pointer to the CopyJobDynamicConstraintRulesLargeFormat instance.
     */
    CopyJobDynamicConstraintRulesLargeFormatUwAdapter(dune::framework::underware::InterpreterEnvironment * interpreterEnvironment,
                    const char * instanceName, CopyJobDynamicConstraintRulesLargeFormat * adaptee);

    /**
     * Destructor.
     */
    virtual ~CopyJobDynamicConstraintRulesLargeFormatUwAdapter( );

    /**
     * @name CopyJobDynamicConstraintRulesUw methods.
     * @{
     */

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
    CopyJobDynamicConstraintRulesLargeFormat * adaptee_; ///< Pointer to the underlying CopyJobDynamicConstraintRulesLargeFormat object.
};

}}}}  // namespace dune::copy::Jobs::Copy


#endif  // DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_LARGE_FORMAT_UW_ADAPTER_H

