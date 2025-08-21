/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobConstraintsExtension.cpp
 * @date   Tue, 05 Jul 2022 08:29:10 +0200
 * @brief  Component used to manage the Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "JobConstraintsExtension.h"

// Declare externals for SWIG-generated initialization functions
extern "C" int Jobconstraintsuw_Init( Tcl_Interp * interp );

namespace dune { namespace copy { namespace Jobs { namespace Copy {


JobConstraintsExtension::JobConstraintsExtension( )
    : InterpreterExtension("JobConstraintsUw")
{
}

JobConstraintsExtension * JobConstraintsExtension::instance()
{
    static JobConstraintsExtension instance;
    return &instance;
}

void JobConstraintsExtension::init(InterpreterExtension::Language language, void * param)
{
    if ( language == InterpreterExtension::LANGUAGE_TCL )
    {
        Jobconstraintsuw_Init(static_cast<Tcl_Interp*>(param));
    }
}

}}}}  // namespace dune::copy::Jobs::Copy

