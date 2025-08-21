/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyPipelineExtension.cpp
 * @date   April 1st, 2024
 * @brief
 *
 * (C) Copyright 2024 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyPipelineExtension.h"

// Declare externals for SWIG-generated initialization functions
extern "C" int Copypipelineuw_Init(Tcl_Interp* interp);

// Initialize the singleton instance.
CopyPipelineExtension* CopyPipelineExtension::instance_ = 0;

CopyPipelineExtension::CopyPipelineExtension() : InterpreterExtension("CopyPipelineUwc", "CopyPipelineUw")
{
}

CopyPipelineExtension* CopyPipelineExtension::instance()
{
    if (instance_ == 0)
    {
        instance_ = new CopyPipelineExtension();
    }
    return instance_;
}

void CopyPipelineExtension::init(InterpreterExtension::Language language, void* param)
{
    if (language == InterpreterExtension::LANGUAGE_TCL)
    {
        Copypipelineuw_Init(static_cast<Tcl_Interp*>(param));
    }
}

void* CopyPipelineExtension::getInterpreterInitFunction(InterpreterExtension::Language language)
{
    return 0;
}