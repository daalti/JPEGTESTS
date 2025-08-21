///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAppLifestyle.cpp
 * @date   Tue, 17 Dec 2019 13:22:31 +0530
 * @brief  Copy Application for Lifestyle Experience
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyAppLifestyle.h"

#include "common_debug.h"

#include "CopyAppLifestyle_TraceAutogen.h"

#include "CopyAppController.h"
EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_spice_CopyAppLifestyle)
{
    dune::copy::spice::CopyAppLifestyle *instance = new dune::copy::spice::CopyAppLifestyle(instanceName);
    assert(instance != nullptr);
    return static_cast<dune::framework::component::IComponent *>(instance);
}

namespace dune { namespace copy { namespace spice {

CopyAppLifestyle::CopyAppLifestyle(const char *instanceName)
    : SpiceApplicationCommon(instanceName), controller_(nullptr)
{
    CHECKPOINTC("%s/CopyAppLifestyle: constructed", instanceName);
}

CopyAppLifestyle::~CopyAppLifestyle()
{
}

dune::framework::component::ComponentFlavorUid CopyAppLifestyle::getComponentFlavorUid() const
{
    return GET_MODULE_UID(CopyAppLifestyle);
}

void CopyAppLifestyle::connected(IComponentManager *componentManager, std::future<void> &asyncCompletion)
{
    SpiceApplicationCommon::connected(componentManager, asyncCompletion);

    controller_ = new CopyAppController(applicationEngine_);
    controller_->moveToThread(qApp->thread());
    controller_->copyInitialize();
}

}}}  // namespace dune::copy::spice
