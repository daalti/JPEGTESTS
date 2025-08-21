/* -*- c++ -*- */

#ifndef DUNE_COPY_CDM_COPY_ADAPTER_STANDARD_UW_ADAPTER_H
#define DUNE_COPY_CDM_COPY_ADAPTER_STANDARD_UW_ADAPTER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAdapterStandardUwAdapter.h
 * @date   Wed, 27 Jul 2022 19:48:04 -0600
 * @brief  This is a CDM Adapter component defining the Copy Service
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyAdapterUw.h"
#include "CopyAdapterStandard.h"

namespace dune { namespace copy { namespace cdm {

/**
 * Underware object adapter between CopyAdapterUw and CopyAdapterStandard.
 */
class CopyAdapterStandardUwAdapter: public CopyAdapterUw
{
public:

    /**
     * Constructor.
     *
     * @param interpreterEnvironment InterpreterEnvironment system service.
     * @param instanceName name of the instance exported to the interpreter.
     * @param adaptee pointer to the CopyAdapterStandard instance.
     */
    CopyAdapterStandardUwAdapter(dune::framework::underware::InterpreterEnvironment * interpreterEnvironment,
                    const char * instanceName, CopyAdapterStandard * adaptee);

    /**
     * Destructor.
     */
    virtual ~CopyAdapterStandardUwAdapter( );

    /**
     * @name CopyAdapterUw methods.
     * @{
     */

    // @todo redeclare methods from CopyAdapterUw here

    /**
     * @}
     */

private:

    dune::framework::underware::InterpreterEnvironment * interpreterEnvironment_;
    const char * instanceName_;
    CopyAdapterStandard * adaptee_; ///< Pointer to the underlying CopyAdapterStandard object.
};

}}}  // namespace dune::copy::cdm


#endif  // DUNE_COPY_CDM_COPY_ADAPTER_STANDARD_UW_ADAPTER_H

