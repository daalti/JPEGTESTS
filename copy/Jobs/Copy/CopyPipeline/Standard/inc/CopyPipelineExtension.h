/* -*- c++ -*- */

#ifndef DUNE_COPY_PIPELINE_EXTENSION_UW_H
#define DUNE_COPY_PIPELINE_EXTENSION_UW_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyPipelineExtension.h
 * @date   April 1st, 2024
 * @brief
 *
 * (C) Copyright 2024 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "InterpreterExtension.h"

/**
 * Interpreter registration broker singleton for CopyPipelineUw.
 */
class CopyPipelineExtension : public dune::framework::underware::InterpreterExtension
{
  public:
    /**
     * Get the singleton instance. The instance is created only the first time
     * this class method is called.
     *
     * @return the singleton instance.
     */
    static CopyPipelineExtension* instance();

    /**
     * @name InterpreterExtension methods.
     * @{
     */

    void  init(InterpreterExtension::Language language, void* param);
    void* getInterpreterInitFunction(InterpreterExtension::Language language);

    /**
     * @}
     */

  private:
    /*
     * Hide constructors and destructor.
     */
    CopyPipelineExtension();
    CopyPipelineExtension(const CopyPipelineExtension& ext);

    static CopyPipelineExtension* instance_;  ///< The singleton instance.
};

#endif  // DUNE_COPY_PIPELINE_EXTENSION_UW_H
