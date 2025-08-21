/* -*- c++ -*- */

#ifndef DUNE_COPY_PIPELINE_UW_ADAPTER_H
#define DUNE_COPY_PIPELINE_UW_ADAPTER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyPipelineUwAdapter.h
 * @date   April 1st, 2024
 * @brief
 *
 * (C) Copyright 2024 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyPipelineUw.h"
#include "InterpreterEnvironment.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

class CopyPipelineStandard;

/**
 * Underware object adapter between CopyPipelineUw and CopyPipelineStandard.
 */
class CopyPipelineUwAdapter : public CopyPipelineUw
{
  public:
    /**
     * Constructor.
     *
     * @param interpreterEnvironment InterpreterEnvironment system service.
     * @param instanceName name of the instance exported to the interpreter.
     * @param adaptee pointer to the CopyPipelineStandard instance.
     */
    CopyPipelineUwAdapter(dune::framework::underware::InterpreterEnvironment* interpreterEnvironment,
                          const char* instanceName, CopyPipelineStandard* adaptee);

    /**
     * Destructor.
     */
    virtual ~CopyPipelineUwAdapter();

    /**
     * @name CopyPipelineUw methods.
     * @{
     */

    void PUB_enableLayoutFilter(bool enable) override final;

    /**
     * @}
     */

  private:
    dune::framework::underware::InterpreterEnvironment* interpreterEnvironment_;
    const std::string                                   instanceName_;
    CopyPipelineStandard* adaptee_;  ///< Pointer to the underlying CopyPipelineStandard object.
};

}}}}  // namespace dune::copy::Jobs::Copy

#endif  // DUNE_COPY_PIPELINE_UW_ADAPTER_H
