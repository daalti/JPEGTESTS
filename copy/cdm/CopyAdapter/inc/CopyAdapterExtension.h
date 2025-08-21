/* -*- c++ -*- */

#ifndef DUNE_COPY_CDM_COPY_ADAPTER_EXTENSION_H
#define DUNE_COPY_CDM_COPY_ADAPTER_EXTENSION_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAdapterExtension.h
 * @date   Wed, 27 Jul 2022 19:48:04 -0600
 * @brief  This is a CDM Adapter component defining the Copy Service
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "InterpreterExtension.h"

namespace dune { namespace copy { namespace cdm {

/**
 * Interpreter registration broker singleton for CopyAdapterUw.
 */
class CopyAdapterExtension: public dune::framework::underware::InterpreterExtension
{
public:

    /**
     * Get the singleton instance. The instance is created only the first time
     * this class method is called.
     *
     * @return the singleton instance.
     */
    static CopyAdapterExtension * instance();

    /**
     * @name InterpreterExtension methods.
     * @{
     */

    void init(InterpreterExtension::Language language, void * param);

    /**
     * @}
     */

private:

    /*
     * Hide constructor and destructor.
     */
    CopyAdapterExtension();
    ~CopyAdapterExtension() = default;

    /*
     * remove copy and move constructors and assignments
     */
    CopyAdapterExtension(const CopyAdapterExtension & ext) = delete;
    CopyAdapterExtension & operator=(const CopyAdapterExtension & ext) = delete;
    CopyAdapterExtension(CopyAdapterExtension && ext) = delete;
    CopyAdapterExtension & operator=(CopyAdapterExtension && ext) = delete;
};

}}}  // namespace dune::copy::cdm


#endif  // DUNE_COPY_CDM_COPY_ADAPTER_EXTENSION_H

