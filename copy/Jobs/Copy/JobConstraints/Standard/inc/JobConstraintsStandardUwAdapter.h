/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_JOB_CONSTRAINTS_STANDARD_UW_ADAPTER_H
#define DUNE_COPY_JOBS_COPY_JOB_CONSTRAINTS_STANDARD_UW_ADAPTER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobConstraintsStandardUwAdapter.h
 * @date   Tue, 05 Jul 2022 08:29:10 +0200
 * @brief  Component used to manage the Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "JobConstraintsUw.h"
#include "JobConstraintsStandard.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

/**
 * Underware object adapter between JobConstraintsUw and JobConstraintsStandard.
 */
class JobConstraintsStandardUwAdapter: public JobConstraintsUw
{
public:

    /**
     * Constructor.
     *
     * @param interpreterEnvironment InterpreterEnvironment system service.
     * @param instanceName name of the instance exported to the interpreter.
     * @param adaptee pointer to the JobConstraintsStandard instance.
     */
    JobConstraintsStandardUwAdapter(dune::framework::underware::InterpreterEnvironment * interpreterEnvironment,
                    const char * instanceName, JobConstraintsStandard * adaptee);

    /**
     * Destructor.
     */
    virtual ~JobConstraintsStandardUwAdapter( );

    /**
     * @name JobConstraintsUw methods.
     * @{
     */

    // @todo redeclare methods from JobConstraintsUw here

    /**
     * @}
     */

private:

    dune::framework::underware::InterpreterEnvironment * interpreterEnvironment_;
    const char * instanceName_;
    JobConstraintsStandard * adaptee_; ///< Pointer to the underlying JobConstraintsStandard object.
};

}}}}  // namespace dune::copy::Jobs::Copy


#endif  // DUNE_COPY_JOBS_COPY_JOB_CONSTRAINTS_STANDARD_UW_ADAPTER_H

