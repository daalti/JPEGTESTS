#ifndef DUNE_COPY_SPICE_COPY_APP_WORKFLOW_H
#define DUNE_COPY_SPICE_COPY_APP_WORKFLOW_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyAppWorkflow.h
 * @date   September 04, 2019
 * @brief  The Workflow flavor of the Copy App
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "IComponentManager.h"
#include "SpiceGuiApplicationCommon.h"
#include "CopyAppSummary_generated.h"
EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_spice_CopyAppWorkflow);


namespace dune { namespace spice { namespace guiCore {
class IMenuResource;
}}}  // namespace dune::spice::guiCore
namespace dune { namespace copy { namespace spice {

using namespace dune::spice::guiCore;

/**
 * The Workflow flavor of the Copy App
 */
class CopyAppWorkflow : public SpiceGuiApplicationCommon
{
  public:
    /**
     * @brief CopyAppWorkflow Constructor.
     *
     * @param instanceName the name of the component instance.
     */
    explicit CopyAppWorkflow(const char *instanceName);

    /**
     * Destructor.
     */
    virtual ~CopyAppWorkflow() override;

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
    void start(QVariantMap initialProperties = QVariantMap()) override;
    void quit() override;
    
  private:
    IMenuResource *copySettingsResource_{nullptr};
    QString        pathToResource_;  
    ISpiceModel   *prioritySessionModel_{nullptr};
    bool applicationRunning_ {false};

    /**
     * @brief List of option on summary list
     */
    QList<QString> interactiveSummaryList_;

    /**
     * @brief List of setting options on copy widget   
     */
    QList<QString> copyWidgetSummaryList_;

    /**
     * @brief list of scan option settings enable to be displayed
     */
    QList<QString> moreOptionSettingsList_;

    /**
     * @brief list of quicksets settings enable to be displayed <Uuid,image>
     */
    QMap<QString,QVariant> quicksetIconList_;

    /**
     * @brief Variable for control if preview is interactive (zoom)
     */
    bool copyPreviewInteractiveEnabled_{false};
    bool isCopyConfigSubscriptionRequired_{false};
    bool isCopyPermissionsConfigurable_{false};

    const char *                              instanceName_;  ///< The instance name.
    //const dune::framework::component::SystemServices * services_ = nullptr;
    std::unique_ptr<CopyAppWorkflowListT>     config_ = nullptr;
    IMenuResource*                            copyModeSettingsResource_{nullptr};

    std::unique_ptr<CopyAppWorkflowListT> getConfiguration(dune::framework::resources::IConfigurationService *configService) const;
    /**
     * @brief Fill list of summary      
     */
    void fillInteractiveSummaryList();

    /**
     * @brief Fill list of widget     
     */

    /**
     * @brief Main Method to overfill data expected to more option settings application display dependency
     *  Relative to copy settings
     */
    void fillMoreOptionList();

    /**
     * @brief Fill list of quicksetIcon
     */
    void fillQuicksetIconList();
};

}}}  // namespace dune::copy::spice

DEFINE_MODULE_UID(dune::copy::spice::CopyAppWorkflow, 0x49f4c0);
DESCRIBE_COMPONENT_FLAVOR_BEGIN(dune::copy::spice::CopyAppWorkflow)
PROVIDES_INTERFACE(dune::spice::guiCore::ISpiceGuiApplication)
PROVIDES_INTERFACE(dune::spice::core::ISpiceApplication)
DESCRIBE_COMPONENT_FLAVOR_END(dune::copy::spice::CopyAppWorkflow)

#endif  // DUNE_COPY_SPICE_COPY_APP_WORKFLOW_H