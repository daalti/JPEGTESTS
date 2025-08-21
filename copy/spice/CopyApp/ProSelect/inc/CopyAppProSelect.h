#ifndef DUNE_COPY_SPICE_COPY_APP_PROSELECT_H
#define DUNE_COPY_SPICE_COPY_APP_PROSELECT_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAppProSelect.h
 * @date   September 04, 2019
 * @brief  The ProSelect flavor of the Copy App
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "IComponentManager.h"
#include "SpiceGuiApplicationCommon.h"

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_spice_CopyAppProSelect);

namespace dune { namespace spice { namespace guiCore {
class IMenuResource;
}}}  // namespace dune::spice::guiCore

namespace dune { namespace copy { namespace spice {

using namespace dune::spice::guiCore;

/**
 * The ProSelect flavor of the Copy App
 */
class CopyAppProSelect : public SpiceGuiApplicationCommon
{
  public:
    /**
     * @brief CopyAppProSelect Constructor.
     *
     * @param instanceName the name of the component instance.
     */
    explicit CopyAppProSelect(const char *instanceName);

    /**
     * Destructor.
     */
    virtual ~CopyAppProSelect() override;

    /**
     * @name IComponent methods.
     * @{
     */
    dune::framework::component::ComponentFlavorUid getComponentFlavorUid() const override;
    void connected(dune::framework::component::IComponentManager *componentManager,
                   std::future<void> &                            asyncCompletion) override;  

    private:
    IMenuResource *copySettingsResource_;
    QString        pathToResource_;  
};

}}}  // namespace dune::copy::spice

DEFINE_MODULE_UID(dune::copy::spice::CopyAppProSelect, 0x2eb46b);
DESCRIBE_COMPONENT_FLAVOR_BEGIN(dune::copy::spice::CopyAppProSelect)
PROVIDES_INTERFACE(dune::spice::guiCore::ISpiceGuiApplication)
PROVIDES_INTERFACE(dune::spice::core::ISpiceApplication)
DESCRIBE_COMPONENT_FLAVOR_END(dune::copy::spice::CopyAppProSelect)

#endif  // DUNE_COPY_SPICE_COPY_APP_PROSELECT_H
