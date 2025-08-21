/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobServiceExtension.cpp
 * @date   Wed, 08 May 2019 11:36:41 -0700
 * @brief  JobService specific class to CopyJobs
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "JobServiceExtension.h"

// Declare externals for SWIG-generated initialization functions
extern "C" int Copyjobserviceuw_Init( Tcl_Interp * interp );

namespace dune { namespace copy { namespace Jobs { namespace Copy {

// Initialize the singleton instance.
JobServiceExtension * JobServiceExtension::instance_ = 0;

JobServiceExtension::JobServiceExtension( )
: InterpreterExtension( "CopyJobServiceUwc", "CopyJobServiceUw" )
{
}

JobServiceExtension * JobServiceExtension::instance( )
{
    if ( instance_ == 0 )
    {
        instance_ = new JobServiceExtension();
    }
    return instance_;
}

void JobServiceExtension::init( InterpreterExtension::Language language, void * param )
{
    Copyjobserviceuw_Init( static_cast<Tcl_Interp*>(param) );
}

}}}}  // namespace dune::copy::Jobs::Copy 

