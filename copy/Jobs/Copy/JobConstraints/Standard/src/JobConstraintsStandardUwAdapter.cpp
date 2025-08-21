/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobConstraintsStandardUwAdapter.cpp
 * @date   Tue, 05 Jul 2022 08:29:10 +0200
 * @brief  Component used to manage the Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "JobConstraintsStandardUwAdapter.h"
#include "InterpreterEnvironment.h"
#include "JobConstraintsExtension.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

JobConstraintsStandardUwAdapter::JobConstraintsStandardUwAdapter(dune::framework::underware::InterpreterEnvironment * interpreterEnvironment,
                                 const char * instanceName, JobConstraintsStandard * adaptee)
    : interpreterEnvironment_(interpreterEnvironment), instanceName_(instanceName), adaptee_(adaptee)
{
    // Register the extension
    interpreterEnvironment_->addExtension(JobConstraintsExtension::instance());

    // Register this instance
    interpreterEnvironment_->addInstance( dune::framework::underware::InterpreterInstance(static_cast<JobConstraintsUw*>(this),
                                                                                          instanceName_,
                                                                                          "dune__copy__Jobs__Copy__JobConstraintsUw",
                                                                                          "JobConstraintsUw") );
}

JobConstraintsStandardUwAdapter::~JobConstraintsStandardUwAdapter()
{
    interpreterEnvironment_->removeInstance(instanceName_);
}

// @todo implement methods from JobConstraintsUw here.

}}}}  // namespace dune::copy::Jobs::Copy

