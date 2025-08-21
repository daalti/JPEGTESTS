/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAdapterStandardUwAdapter.cpp
 * @date   Wed, 27 Jul 2022 19:48:04 -0600
 * @brief  This is a CDM Adapter component defining the Copy Service
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyAdapterStandardUwAdapter.h"
#include "CopyAdapterExtension.h"
#include "InterpreterEnvironment.h"

namespace dune { namespace copy { namespace cdm {

CopyAdapterStandardUwAdapter::CopyAdapterStandardUwAdapter(dune::framework::underware::InterpreterEnvironment * interpreterEnvironment,
                                 const char * instanceName, CopyAdapterStandard * adaptee)
    : interpreterEnvironment_(interpreterEnvironment), instanceName_(instanceName), adaptee_(adaptee)
{
    // Register the extension
    interpreterEnvironment_->addExtension(CopyAdapterExtension::instance());

    // Register this instance
    interpreterEnvironment_->addInstance( dune::framework::underware::InterpreterInstance(static_cast<CopyAdapterUw*>(this),
                                                                                          instanceName_,
                                                                                          "dune__copy__cdm__CopyAdapterUw",
                                                                                          "CopyAdapterUw") );
}

CopyAdapterStandardUwAdapter::~CopyAdapterStandardUwAdapter()
{
    interpreterEnvironment_->removeInstance(instanceName_);
}

// @todo implement methods from CopyAdapterUw here.

}}}  // namespace dune::copy::cdm

