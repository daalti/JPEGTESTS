/* -*- c++ -*- */

#ifndef DUNE_COPY_CDM_COPY_ADAPTER_UW_H
#define DUNE_COPY_CDM_COPY_ADAPTER_UW_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAdapterUw.h
 * @date   Wed, 27 Jul 2022 19:48:04 -0600
 * @brief  This is a CDM Adapter component defining the Copy Service
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

namespace dune { namespace copy { namespace cdm {
/**
 * @brief Interface exported to interpreters, also known as "underware
 * interface".
 */
class CopyAdapterUw
{
public:

    /**
     * Destructor.
     */
    virtual ~CopyAdapterUw() { }

    // @todo add pure virtual methods of the interface here.
};

}}}  // namespace dune::copy::cdm


#endif  // DUNE_COPY_CDM_COPY_ADAPTER_UW_H

