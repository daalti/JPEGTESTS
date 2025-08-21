/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_JOB_CONSTRAINTS_EXTENSION_H
#define DUNE_COPY_JOBS_COPY_JOB_CONSTRAINTS_EXTENSION_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobConstraintsExtension.h
 * @date   Tue, 05 Jul 2022 08:29:10 +0200
 * @brief  Component used to manage the Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "InterpreterExtension.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

/**
 * Interpreter registration broker singleton for JobConstraintsUw.
 */
class JobConstraintsExtension: public dune::framework::underware::InterpreterExtension
{
public:

    /**
     * Get the singleton instance. The instance is created only the first time
     * this class method is called.
     *
     * @return the singleton instance.
     */
    static JobConstraintsExtension * instance();

    /**
     * @name InterpreterExtension methods.
     * @{
     */

    void init(InterpreterExtension::Language language, void * param);

    /**
     * @}
     */

private:

    /*
     * Hide constructor and destructor.
     */
    JobConstraintsExtension();
    ~JobConstraintsExtension() = default;

    /*
     * remove copy and move constructors and assignments
     */
    JobConstraintsExtension(const JobConstraintsExtension & ext) = delete;
    JobConstraintsExtension & operator=(const JobConstraintsExtension & ext) = delete;
    JobConstraintsExtension(JobConstraintsExtension && ext) = delete;
    JobConstraintsExtension & operator=(JobConstraintsExtension && ext) = delete;
};

}}}}  // namespace dune::copy::Jobs::Copy


#endif  // DUNE_COPY_JOBS_COPY_JOB_CONSTRAINTS_EXTENSION_H

