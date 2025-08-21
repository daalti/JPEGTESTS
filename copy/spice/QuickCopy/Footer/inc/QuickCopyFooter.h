/* -*- c++ -*- */

#ifndef DUNE_COPY_SPICE_QUICK_COPY_FOOTER_H
#define DUNE_COPY_SPICE_QUICK_COPY_FOOTER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   QuickCopyFooter.h
 * @date   Thu, 22 Feb 2024 11:08:39 -0700
 * @brief  Component Holds different Flavours of QuickCopy.
 *
 * (C) Copyright 2024 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "IComponent.h"
#include "IQuickCopy.h"
#include "QuickCopyFooterConfig_generated.h"
#include "IGuiApplicationEngine.h"
#include "IConfigurationService.h"
EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_spice_QuickCopyFooter);

namespace dune { namespace copy { namespace spice {

/**
 * Implementation of the Footer flavor of the QuickCopy component.
 */
class QuickCopyFooter:
    public dune::framework::component::IComponent,
    public IQuickCopy
{
public:

    /**
     * @name IQuickCopy methods.
     * @{
     */

    /// @todo redeclare methods from IQuickCopy here (don't forget the 'override' clause).

    /**
     * @}
     */

    /**
     * @brief QuickCopyFooter Constructor.
     *
     * @param instanceName the name of the component instance.
     */
    explicit QuickCopyFooter(const char *instanceName);

    /**
     * Destructor.
     */
    virtual ~QuickCopyFooter();

    /**
     * @name IComponent methods.
     * @{
     */

    dune::framework::component::ComponentFlavorUid getComponentFlavorUid() const override;
    const char * getComponentInstanceName() const override;
    void initialize(WorkingMode mode, const dune::framework::component::SystemServices *services) override;
    void * getInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName) override;
    void setInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName, void *interfacePtr) override;
    void connected(dune::framework::component::IComponentManager *componentManager, std::future<void> &asyncCompletion) override;
    void shutdown(ShutdownCause cause, std::future<void> &asyncCompletion) override;

    /**
     * @}
     */

protected:

    /**
     * @brief Loads the configuration for this component instance
     *
     * @param configurationService the pointer to the system's configuration service
     * @return the configuration values to be used by this instance, according to the system's product and proto
     *         versions or nullptr if the configuration is not available for this instance.
     */
    std::unique_ptr<QuickCopyFooterConfigT> getConfiguration(dune::framework::resources::IConfigurationService *configurationService) const;
    dune::spice::guiCore::IGuiApplicationEngine *applicationEngine_{nullptr};
    const dune::framework::component::SystemServices *services_ = nullptr;
private:

    const char *instanceName_; ///< The instance name.
    std::unique_ptr<QuickCopyFooterConfigT> configuration_; ///< The instance's constants configuration
    QObject* quickCopyComponentHandler_{nullptr};
};

}}}  // namespace dune::copy::spice

DEFINE_MODULE_UID(dune::copy::spice::QuickCopyFooter, 0x93070d);

DESCRIBE_COMPONENT_FLAVOR_BEGIN(dune::copy::spice::QuickCopyFooter)
    PROVIDES_INTERFACE(dune::copy::spice::IQuickCopy)
DESCRIBE_COMPONENT_FLAVOR_END(dune::copy::spice::QuickCopyFooter)


#endif  // DUNE_COPY_SPICE_QUICK_COPY_FOOTER_H

