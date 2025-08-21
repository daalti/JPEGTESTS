/* -*- c++ -*- */

#ifndef DUNE_COPY_SPICE_I_QUICK_COPY_H
#define DUNE_COPY_SPICE_I_QUICK_COPY_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   IQuickCopy.h
 * @date   Thu, 22 Feb 2024 11:08:38 -0700
 * @brief  Component Holds different Flavours of QuickCopy.
 *
 * (C) Copyright 2024 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "ComponentSystemTypes.h"

namespace dune { namespace copy { namespace spice {
/**
 * @brief Component Holds different Flavours of QuickCopy.
 *
 * @todo describe the main responsibilities and interactions of the
 * component(s) realizing this interface.
 */
class IQuickCopy
{
public:

    /**
     * Destructor.
     */
    virtual ~IQuickCopy() { }

    // @todo add pure virtual methods of the interface here.
};

}}}  // namespace dune::copy::spice

DEFINE_INTERFACE_UID(dune::copy::spice::IQuickCopy, 0xb4017a);

#endif  // DUNE_COPY_SPICE_I_QUICK_COPY_H

