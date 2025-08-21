/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyPipelineUwAdapter.cpp
 * @date   April 1st, 2024
 * @brief
 *
 * (C) Copyright 2024 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyPipelineUwAdapter.h"

#include "CopyPipelineExtension.h"
#include "CopyPipelineStandard.h"
#include "Interpreter.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

CopyPipelineUwAdapter::CopyPipelineUwAdapter(dune::framework::underware::InterpreterEnvironment *interpreterEnvironment,
                                             const char *instanceName, CopyPipelineStandard *adaptee)
    : interpreterEnvironment_(interpreterEnvironment), instanceName_(instanceName), adaptee_(adaptee)
{
    // Register the extension
    interpreterEnvironment_->addExtension(CopyPipelineExtension::instance());

    // Register this instance
    interpreterEnvironment_->addInstance(
        dune::framework::underware::InterpreterInstance(static_cast<CopyPipelineUw *>(this), instanceName_.c_str(),
                                                        "dune__copy__Jobs__Copy__CopyPipelineUw", "CopyPipelineUw"));
}

CopyPipelineUwAdapter::~CopyPipelineUwAdapter()
{
    interpreterEnvironment_->removeInstance(instanceName_);
}

void CopyPipelineUwAdapter::PUB_enableLayoutFilter(bool enable)
{
    adaptee_->enableLayoutFilter(enable);
}

}}}}  // namespace dune::copy::Jobs::Copy
