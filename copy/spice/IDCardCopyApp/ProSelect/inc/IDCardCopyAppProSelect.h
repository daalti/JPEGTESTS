#ifndef DUNE_COPY_SPICE_IDCARDCOPY_APP_PROSELECT_H
#define DUNE_COPY_SPICE_IDCARDCOPY_APP_PROSELECT_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   IDCardCopyAppProSelect.h
 * @date   April 05, 2021
 * @brief  The ProSelect flavor of the ID Card Copy App
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "IComponentManager.h"
#include "SpiceGuiApplicationCommon.h"

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_spice_IDCardCopyAppProSelect);

namespace dune { namespace spice { namespace guiCore {
class IMenuResource;
}}}  // namespace dune::spice::guiCore

namespace dune { namespace copy { namespace spice {

using namespace dune::spice::guiCore;

/**
 * The ProSelect flavor of the ID Card Copy App
 */
class IDCardCopyAppProSelect : public SpiceGuiApplicationCommon
{
  public:
    /**
     * @brief IDCardCopyAppProSelect Constructor.
     *
     * @param instanceName the name of the component instance.
     */
    explicit IDCardCopyAppProSelect(const char *instanceName);

    /**
     * Destructor.
     */
    virtual ~IDCardCopyAppProSelect() override;

    /**
     * @name IComponent methods.
     * @{
     */
    dune::framework::component::ComponentFlavorUid getComponentFlavorUid() const override;
    void connected(dune::framework::component::IComponentManager *componentManager,
                   std::future<void> &                            asyncCompletion) override;
    
    private:
    IMenuResource *idcopySettingsResource_;
    QString        pathToResource_;
};

}}}  // namespace dune::copy::spice

DEFINE_MODULE_UID(dune::copy::spice::IDCardCopyAppProSelect, 0x344b97);
DESCRIBE_COMPONENT_FLAVOR_BEGIN(dune::copy::spice::IDCardCopyAppProSelect)
PROVIDES_INTERFACE(dune::spice::guiCore::ISpiceGuiApplication)
PROVIDES_INTERFACE(dune::spice::core::ISpiceApplication)
DESCRIBE_COMPONENT_FLAVOR_END(dune::copy::spice::IDCardCopyAppProSelect)

#endif  // DUNE_COPY_SPICE_IDCARDCOPY_APP_PROSELECT_H
