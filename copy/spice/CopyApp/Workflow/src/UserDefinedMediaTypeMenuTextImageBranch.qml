import QtQuick 2.15
import QtQml 2.15
import QtQuick.Layouts 1.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import QtQml.Models 2.15

SettingsTextImageBranchViewModel
{
    id : root
    property var menuNode
    node: menuNode
    property var pushMenuItem : null
    property ISpiceModel mediaPropertyConfigurationModelV2: null;
    property QtObject mediaUtility: MediaUtility{}

    function baseCreate()
    {
        let comp = Qt.createComponent("qrc:/menu/MenuTextImageBranchBase.qml")
        if (comp.status !== Component.Ready) {
            console.warn(comp.errorString())
        }
        root.controlModel  =  comp.createObject(root, {"menuNode": root.menuNode, "pushMenuItem": root.pushMenuItem})
        updateSelectedValue()
        root.controlModel.menuDelegateProperties.valueChanged.connect(updateSelectedValueLater)
    }

    function updateSelectedValueLater()
    {
        Qt.callLater(updateSelectedValue)
    }

    function updateSelectedValue(){
        if(root.controlModel.menuDelegateProperties.type === "dune::spice::glossary_1::MediaType::MediaType")
        {
            let mediaTypeStr = _qmlUtils.convertfbsExtendedCharsetEnumValueToCppEnumValue(root.controlModel.menuDelegateProperties.value.toString())
            if(root.mediaUtility.isUserDefinedMediaType(mediaTypeStr) === true)
            {
                let cdmEndPoint = root.mediaUtility.convertToCDMString(mediaTypeStr.toString())
                let future = _resourceStore.subscribe("/cdm/mediaProperty/v2/mediaConfigs/"+cdmEndPoint, true)
                future.resolved.connect(function(){
                                        root.mediaPropertyConfigurationModelV2 = future.get()
                                        if(root.mediaPropertyConfigurationModelV2.data != null)
                                        {
                                            let usdName = root.mediaPropertyConfigurationModelV2.data.userDefinedName.toString()
                                            root.controlModel.valueText.text = _qmlUtils.createSpiceLoc( root ,{"text":usdName}).text
                                        }
                                        })
            }
            else
            {
                return
            }
        }
        else
        {
            return
        }
    }

    Component.onCompleted:
    {
        Qt.callLater(baseCreate)
    }

    Component.onDestruction:
    {
        if(root.controlModel.menuDelegateProperties)
        {
            root.controlModel.menuDelegateProperties.valueChanged.disconnect(updateSelectedValueLater)
        }
    } 
}
