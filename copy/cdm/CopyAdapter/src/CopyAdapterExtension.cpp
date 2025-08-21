/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAdapterExtension.cpp
 * @date   Wed, 27 Jul 2022 19:48:04 -0600
 * @brief  This is a CDM Adapter component defining the Copy Service
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyAdapterExtension.h"

// Declare externals for SWIG-generated initialization functions
extern "C" int Copyadapteruw_Init( Tcl_Interp * interp );

namespace dune { namespace copy { namespace cdm {


CopyAdapterExtension::CopyAdapterExtension( )
    : InterpreterExtension("CopyAdapterUw")
{
}

CopyAdapterExtension * CopyAdapterExtension::instance()
{
    static CopyAdapterExtension instance;
    return &instance;
}

void CopyAdapterExtension::init(InterpreterExtension::Language language, void * param)
{
    if ( language == InterpreterExtension::LANGUAGE_TCL )
    {
        Copyadapteruw_Init(static_cast<Tcl_Interp*>(param));
    }
}

}}}  // namespace dune::copy::cdm

