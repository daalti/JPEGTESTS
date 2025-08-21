/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesLargeFormatUwAdapter.cpp
 * @date   Tue, 11 Oct 2022 11:20:06 +0200
 * @brief  Component used to manage the Dynamic Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobDynamicConstraintRulesLargeFormatUwAdapter.h"
#include "CopyJobDynamicConstraintRulesExtension.h"
#include "InterpreterEnvironment.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

CopyJobDynamicConstraintRulesLargeFormatUwAdapter::CopyJobDynamicConstraintRulesLargeFormatUwAdapter(dune::framework::underware::InterpreterEnvironment * interpreterEnvironment,
                                 const char * instanceName, CopyJobDynamicConstraintRulesLargeFormat * adaptee)
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

CopyJobDynamicConstraintRulesLargeFormatUwAdapter::~CopyJobDynamicConstraintRulesLargeFormatUwAdapter()
{
    interpreterEnvironment_->removeInstance(instanceName_);
}

void CopyJobDynamicConstraintRulesLargeFormatUwAdapter::PUB_disableDynamicConstraints(const bool value)
{
    adaptee_->setValueIgnoreGenerationConstraints(value);
}

}}}}  // namespace dune::copy::Jobs::Copy

