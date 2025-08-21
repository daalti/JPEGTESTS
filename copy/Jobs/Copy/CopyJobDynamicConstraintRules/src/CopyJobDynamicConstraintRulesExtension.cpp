/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesExtension.cpp
 * @date   Mon, 11 Jul 2022 11:20:06 +0200
 * @brief  Component used to manage the Dynamic Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobDynamicConstraintRulesExtension.h"

// Declare externals for SWIG-generated initialization functions
extern "C" int Copyjobdynamicconstraintrulesuw_Init( Tcl_Interp * interp );

namespace dune { namespace copy { namespace Jobs { namespace Copy {


CopyJobDynamicConstraintRulesExtension::CopyJobDynamicConstraintRulesExtension( )
    : InterpreterExtension("CopyJobDynamicConstraintRulesUw")
{
}

CopyJobDynamicConstraintRulesExtension * CopyJobDynamicConstraintRulesExtension::instance()
{
    static CopyJobDynamicConstraintRulesExtension instance;
    return &instance;
}

void CopyJobDynamicConstraintRulesExtension::init(InterpreterExtension::Language language, void * param)
{
    if ( language == InterpreterExtension::LANGUAGE_TCL )
    {
        Copyjobdynamicconstraintrulesuw_Init(static_cast<Tcl_Interp*>(param));
    }
}

}}}}  // namespace dune::copy::Jobs::Copy

