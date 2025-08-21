import QtQml 2.15
import spiceux 1.0
import spiceGuiCore 1.0

QtObject{
    id: root
    property  ISpiceModel copyConfiguration: null

    function createQuickCopyComponent()
    {
        let quickCopyComponent = Qt.createComponent("qrc:/QuickCopy/QuickCopyFooter.qml")
        console.assert(quickCopyComponent.status === Component.Ready, quickCopyComponent.errorString())
        return quickCopyComponent
    }

    function subscribeToCopyConfigurationAndUpdateQuickCopyFooter()
    {
        let response = _resourceStore.subscribe("/cdm/copy/v1/configuration");

        response.resolved.connect((future) => {
            console.log("Copyconfiguration subscribe resolved");
            copyConfiguration = future.get()
            handleCopyEnabledChanged()
            copyConfiguration.data.copyEnabledChanged.connect(handleCopyEnabledChanged)
        });

        response.rejected.connect((future) => {
            console.warn("Copyconfiguration subscribe rejected: " + future.error)
        });
    }

    function handleCopyEnabledChanged()
    {
        console.log("CopyEnabledchanged to ->",copyConfiguration.data.copyEnabled )
        if( copyConfiguration.data.copyEnabled != Glossary_1_FeatureEnabled.FeatureEnabled.true_
            && _homeFooterView !== null && _homeFooterView.view !== null)
        {
            _homeFooterView.view.homeScreenFooterRightComponent = null
        }
        else if( _homeFooterView !== null && _homeFooterView.view !== null){
            _homeFooterView.view.homeScreenFooterRightComponent = createQuickCopyComponent()
        }
    }

    Component.onCompleted:{
        Global.homeScreenViewReady.connect(subscribeToCopyConfigurationAndUpdateQuickCopyFooter)
    }

    Component.onDestruction:{
        if(copyConfiguration)
        {
            root.copyConfiguration.data.copyEnabledChanged.disconnect(handleCopyEnabledChanged)
        }
        Global.homeScreenViewReady.disconnect(subscribeToCopyConfigurationAndUpdateQuickCopyFooter)
    }
}