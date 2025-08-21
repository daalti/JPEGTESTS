/* -*- c++ -*- */

#ifndef DUNE_COPY_PIPELINE_UW_H
#define DUNE_COPY_PIPELINE_UW_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyPipelineUw.h
 * @date   April 1st, 2024
 * @brief
 *
 * (C) Copyright 2024 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "dune_types.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

/**
 * @brief Interface exported to interpreters, also known as "underware
 * interface".
 */
class CopyPipelineUw
{
  public:
    /**
     * Destructor.
     */
    virtual ~CopyPipelineUw() {}

    /**
     * @brief Enable and use LayoutFilter instead of MarkingFilter
     *
     * @param enable true to enable LayoutFilter, false to disable it
     */
    virtual void PUB_enableLayoutFilter(bool enable) = 0;
};

}}}}  // namespace dune::copy::Jobs::Copy

#endif  // DUNE_COPY_PIPELINE_UW_H
