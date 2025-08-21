#ifndef DUNE_COPY_SPICE_COPY_APP_LIFESTYLE_H
#define DUNE_COPY_SPICE_COPY_APP_LIFESTYLE_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAppLifestyle.h
 * @date   Tue, 17 Dec 2019 13:22:31 +0530
 * @brief  Copy Application for Lifestyle Experience
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyAppController.h"
#include "HardKeyEvent.h"
#include "SpiceApplicationCommon.h"

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_spice_CopyAppLifestyle);

namespace dune { namespace copy { namespace spice {

using namespace dune::spice::core;
/**
 * The Lifestyle flavor of the Copy App
 */
class CopyAppLifestyle : public SpiceApplicationCommon
{
  public:
    /* @brief CopyAppLifestyle Constructor.
     *
     * @param instanceName the name of the component instance.
     */
    explicit CopyAppLifestyle(const char *instanceName);

    /**
     * Destructor.
     */
    virtual ~CopyAppLifestyle();

    dune::framework::component::ComponentFlavorUid getComponentFlavorUid() const override;
    void connected(IComponentManager *componentManager, std::future<void> &asyncCompletion) override;

  private:
    CopyAppController *controller_;
};

}}}  // namespace dune::copy::spice

DEFINE_MODULE_UID(dune::copy::spice::CopyAppLifestyle, 0x083d68);
DESCRIBE_COMPONENT_FLAVOR_BEGIN(dune::copy::spice::CopyAppLifestyle)
PROVIDES_INTERFACE(dune::spice::core::ISpiceApplication)
DESCRIBE_COMPONENT_FLAVOR_END(dune::copy::spice::CopyAppLifestyle)

#endif  // DUNE_COPY_SPICE_COPY_APP_LIFESTYLE_H
