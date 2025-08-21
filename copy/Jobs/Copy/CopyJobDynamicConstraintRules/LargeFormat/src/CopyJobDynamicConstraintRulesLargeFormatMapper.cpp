/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesLargeFormatMapper.cpp
 * @date   Tue, 11 Oct 2022 11:20:06 +0200
 * @brief  Namespace with maps between types and main method executions
 * @author yago.cordero.carrera@hp.com (Cordero Carrera, Yago)
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobDynamicConstraintRulesLargeFormatMapper.h"
#include "common_debug.h"
#include "CopyJobDynamicConstraintRulesLargeFormatMapper_TraceAutogen.h"

#include <utility>

namespace dune { namespace copy { namespace Jobs { namespace Copy {

void CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointDebug(const char* message)
{
    CHECKPOINTD_STR("%s", message);
}

void CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo(const char* message)
{
    CHECKPOINTC_STR("%s", message);
}

void CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointWarning(const char* message)
{
    CHECKPOINTB_STR("%s", message);
}

}}}}  // namespace dune::copy::Jobs::Copy
