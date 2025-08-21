/* -*- c++ -*- */

#ifndef DUNE_COPY_SPICE_I_D_CARD_COPY_APP_WORKFLOW_H
#define DUNE_COPY_SPICE_I_D_CARD_COPY_APP_WORKFLOW_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   IDCardCopyAppWorkflow.h
 * @date   Tue, 28 Sep 2021 05:12:18 -0600
 * @brief  The WorkFlow Flavour of IDCardCopy App
 *
 * (C) Copyright 2021 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "IComponentManager.h"
#include "SpiceGuiApplicationCommon.h"
#include "InteractiveOrder_generated.h"

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_spice_IDCardCopyAppWorkflow);

namespace dune { namespace spice { namespace guiCore {
class IMenuResource;
}}}  // namespace dune::spice::guiCore

namespace dune { namespace copy { namespace spice {

using namespace dune::spice::guiCore;

/**
 * The Workflow flavor of the IDCardCopy App
 */
class IDCardCopyAppWorkflow : public SpiceGuiApplicationCommon
{
  public:
    /**
     * @brief IDCardCopyAppWorkflow Constructor.
     *
     * @param instanceName the name of the component instance.
     */
    explicit IDCardCopyAppWorkflow(const char *instanceName);

    /**
     * Destructor.
     */
    virtual ~IDCardCopyAppWorkflow() override;

    /**
     * @name IComponent methods.
     * @{
     */
    dune::framework::component::ComponentFlavorUid getComponentFlavorUid() const override;
    
    /**
     * @}
     */
    void initialize(WorkingMode mode, const dune::framework::component::SystemServices *services) override;
    void connected(IComponentManager *componentManager, std::future<void> &asyncCompletion) override;

    private:
    IMenuResource *idcopySettingsResource_{nullptr};
    QString        pathToResource_;


    QList<QString> interactiveSummaryList_;

    const char *                                       instanceName_;  ///< The instance name.
    std::unique_ptr<InteractiveOrderListT>     config_ = nullptr;
    std::unique_ptr<InteractiveOrderListT> getConfiguration(dune::framework::resources::IConfigurationService *configService) const;
};

}}}  // namespace dune::copy::spice

DEFINE_MODULE_UID(dune::copy::spice::IDCardCopyAppWorkflow, 0x2649f5);
DESCRIBE_COMPONENT_FLAVOR_BEGIN(dune::copy::spice::IDCardCopyAppWorkflow)
PROVIDES_INTERFACE(dune::spice::guiCore::ISpiceGuiApplication)
PROVIDES_INTERFACE(dune::spice::core::ISpiceApplication)
DESCRIBE_COMPONENT_FLAVOR_END(dune::copy::spice::IDCardCopyAppWorkflow)


#endif  // DUNE_COPY_SPICE_I_D_CARD_COPY_APP_WORKFLOW_H

