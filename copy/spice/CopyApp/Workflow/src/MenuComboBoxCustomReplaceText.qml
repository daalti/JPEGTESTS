import QtQuick 2.15
import QtQml 2.15
//import QtQuick.Layouts 1.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
//import QtQml.Models 2.15

//import "qrc:/SpiceBinding.js" as SpiceBinding
//import "qrc:/UnitsUtils.js" as UnitsUtils

/*
In this control, MenuComboBox.qml is reimplemented. 
All the logic is kept as it is, in order to not affect the functionality of constraints, etc.
This control only serves the function of replacing the text of an enumerated value, which in 
this component must have another string value. 
In this way, we do not change the operation of the control and we limit ourselves to making an aesthetic change.
USAGE: 
    1. create a derived QML
    2  reimplement initControl(), 
    3. fill mediaMap  mediaMap.set(Number(ENUM VALUE as a number),replacement text)
    4  call to postInitControl()
*/

SettingsComboBoxViewModel
{
    //same as MenuComboBox.qml
    id : root
    property var menuNode
    node: menuNode
    property var pushMenuItem : null

    function baseCreate()
    {
        let comp = Qt.createComponent("qrc:/menu/MenuComboBoxBase.qml")
        if (comp.status !== Component.Ready) {
            console.warn(comp.errorString())
        }
        root.controlModel  =  comp.createObject(root, {"node": root.menuNode, "pushMenuItem": root.pushMenuItem})
    }

    //new features

    //string map for replacement
    property var mediaMap:new Map()

    //signal handlers (when to replace the text)
    property Connections modelObserver: Connections{
        target: root.controlModel?root.controlModel.model:null
        enabled:target!=null
        function onCountChanged()
        {
            Qt.callLater(replaceText) //replace  text on list
        }
    }

    property Connections menuDelegateObserver: Connections{
        target: root.controlModel?root.controlModel:null
        enabled:target!=null

        function onCurrentIndexChanged()
        {
            Qt.callLater(updateSelectedValue) //replace external text
        }

        function onUpdateModel()
        {
            Qt.callLater(replaceText) //replace  text on list
        }
    }


    //Replace the text in the combo box model, if necessary
    function replaceText()
    {

        if( root.controlModel === null )
        {
            return
        }

        for( let i=0 ; i<root.controlModel.model.count ; i++ )
        {
            let item = root.controlModel.model.get(i)
            let enumNameValue= _qmlUtils.getValueFromStringifiedEnum(root.controlModel.enumType , item.value.toString())
            if(mediaMap.has(Number(enumNameValue))) //we have a replacement for this text
            {
                item.textObject.text= mediaMap.get(Number(enumNameValue))
            }
        }
    }

    //Replace the external text of the combo box, if necessary
    function updateSelectedValue()
    {   
        //The Spice Control already sets the external text of the control with the selected value.
        //ONLY in the case that the selected item is the one we want to replace, will the text of the control be changed. 
        //In any other case, it will function normally 
        if( root.controlModel && root.controlModel.menuDelegateProperties )
        {
            let value = Number(root.controlModel.menuDelegateProperties.value)
            if(mediaMap.has(value))
            {
                root.controlModel.selectedValue.text = mediaMap.get(value)
            }
        }
    }

    function updateSelectedValueLater()
    {
        Qt.callLater(updateSelectedValue)
    }

    function postInitControl()
    {
        //build control
        //baseCreate()
        if(root.controlModel)
        {
            updateSelectedValue()
            root.controlModel.menuDelegateProperties.valueChanged.connect(updateSelectedValueLater)
            replaceText()
        }
    }

    //reimplement initControl(), fill mediaMap  mediaMap.set(Number(ENUM VALUE as number),replacement text), call to postInitControl()
    function initControl()
    {
        postInitControl()
    }


    Component.onCompleted:
    {
        Qt.callLater(baseCreate)
        Qt.callLater(initControl)
    }

    Component.onDestruction:
    {
        if(root.controlModel&& root.controlModel.menuDelegateProperties)
        {
            root.controlModel.menuDelegateProperties.valueChanged.disconnect(updateSelectedValueLater)
        }
    }
}