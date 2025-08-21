/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesStandardUwAdapter.cpp
 * @date   Mon, 11 Jul 2022 11:20:06 +0200
 * @brief  Component used to manage the Dynamic Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobDynamicConstraintRulesStandardUwAdapter.h"
#include "CopyJobDynamicConstraintRulesExtension.h"
#include "Interpreter.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

CopyJobDynamicConstraintRulesStandardUwAdapter::CopyJobDynamicConstraintRulesStandardUwAdapter(dune::framework::underware::InterpreterEnvironment * interpreterEnvironment,
                                 const char * instanceName, CopyJobDynamicConstraintRulesStandard * adaptee)
    : interpreterEnvironment_(interpreterEnvironment), instanceName_(instanceName), adaptee_(adaptee)
{
    // Register the extension
    interpreterEnvironment_->addExtension(CopyJobDynamicConstraintRulesExtension::instance());

    // Register this instance
    interpreterEnvironment_->addInstance( dune::framework::underware::InterpreterInstance(static_cast<CopyJobDynamicConstraintRulesUw*>(this),
                                                                                          instanceName_,
                                                                                          "dune__copy__Jobs__Copy__CopyJobDynamicConstraintRulesUw",
                                                                                          "CopyJobDynamicConstraintRulesUw") );
}

CopyJobDynamicConstraintRulesStandardUwAdapter::~CopyJobDynamicConstraintRulesStandardUwAdapter()
{
    interpreterEnvironment_->removeInstance(instanceName_);
}

void CopyJobDynamicConstraintRulesStandardUwAdapter::PUB_disableDynamicConstraints(const bool value)
{
    DUNE_UNUSED(value);
    // Not implemented yet
}

// @todo implement methods from CopyJobDynamicConstraintRulesUw here.

}}}}  // namespace dune::copy::Jobs::Copy

