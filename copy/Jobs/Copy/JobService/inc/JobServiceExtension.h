/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_JOB_SERVICE_EXTENSION_H
#define DUNE_COPY_JOBS_COPY_JOB_SERVICE_EXTENSION_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobServiceExtension.h
 * @date   Wed, 08 May 2019 11:36:41 -0700
 * @brief  JobService specific class to CopyJobs
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "InterpreterExtension.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

/**
 * Interpreter registration broker singleton for CopyJobServiceUw.
 */
class JobServiceExtension: public dune::framework::underware::InterpreterExtension
{
public:

    /**
     * Get the singleton instance. The instance is created only the first time
     * this class method is called.
     *
     * @return the singleton instance.
     */
    static JobServiceExtension * instance( );

    /**
     * @name InterpreterExtension methods.
     * @{
     */

    void init( InterpreterExtension::Language language, void * param );

    /**
     * @}
     */

private:

    /*
     * Hide constructors.
     */
    JobServiceExtension( );
    JobServiceExtension( const JobServiceExtension & ext );

    static JobServiceExtension * instance_; ///< The singleton instance.
};

}}}}  // namespace dune::copy::Jobs::Copy


#endif  // DUNE_COPY_JOBS_COPY_JOB_SERVICE_EXTENSION_H

