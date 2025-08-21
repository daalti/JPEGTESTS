import QtQuick 2.15
import QtQml 2.15
import QtQuick.Layouts 1.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import QtQml.Models 2.15
/*
In this control, MenuComboBox.qml is reimplemented. 
All the logic is kept as it is, in order to not affect the functionality of constraints, etc.
This control only serves the function of replacing the text of an enumerated value, which in 
this component must have another StringId value. 
In this way, we do not change the operation of the control and we limit ourselves to making an aesthetic change.

MediaProfile_1_MediaFamily.MediaFamily.unknown is translated as "StringIds.cUnknown," but in the copy component, it has been used as "cAny". 

*/

SettingsComboBoxViewModel
{
    id : root
    property var menuNode
    node: menuNode
    property var pushMenuItem : null

    //replacement properties
    property var replaceEnumValue: MediaProfile_1_MediaFamily.MediaFamily.unknown //target value
    property string replaceEnumValueString: "StringIds.cAny" //replacement StringId
    property SpiceLocObject anyTextObject: SpiceLocObject{
        stringId: replaceEnumValueString
    }

    //signal handlers
    property Connections modelObserver: Connections{
        target: root.controlModel?root.controlModel.model:null
        enabled:target!=null
        function onCountChanged()
        {
            Qt.callLater(replaceText)
        }
    }

    property Connections menuDelegateObserver: Connections{
        target: root.controlModel?root.controlModel:null
        enabled:target!=null

        function onCurrentIndexChanged()
        {
            Qt.callLater(updateSelectedValue)
        }

        function onUpdateModel()
        {
            Qt.callLater(replaceText)
        }
    }

    //Replace the text in the combo box model, if necessary
    function replaceText()
    {
        if( root.controlModel === null )
        {
            return
        }

        let replacementValue =_menuResource.enumStringFromValue(root.controlModel.enumType,root.replaceEnumValue)

        for( let i=0 ; i<root.controlModel.model.count ; i++ )
        {
            let item = root.controlModel.model.get(i)
            /*
            stringId getter is numeric int getStringId() (we need "StringIds.cUnknown" integer value );
            stringId setter is qvariant (qstring or int) setStringId(QVariant stringId);
            */

            if(item.value == replacementValue){
                console.log("replace combobox text "+ item.textObject.stringId + " -> " + root.replaceEnumValueString)
                item.textObject.stringId = root.replaceEnumValueString
                break
            }
        }
    }

    //Replace the external text of the combo box, if necessary
    function updateSelectedValue()
    {   
        //The Spice Control already sets the external text of the control with the selected value.
        //ONLY in the case that the selected item is the one we want to replace, will the text of the control be changed. 
        //In any other case, it will function normally 
        if( root.controlModel === null ){
            return
        } 
        if(root.controlModel.menuDelegateProperties === null){
            return
        }

        if(root.controlModel.menuDelegateProperties.value == root.replaceEnumValue){
           root.controlModel.selectedValue.text = anyTextObject.text 
        }
    }

    function updateSelectedValueLater()
    {
        Qt.callLater(updateSelectedValue)
    }

    //same as MenuComboBox.qml
    function baseCreate()
    {
        let comp = Qt.createComponent("qrc:/menu/MenuComboBoxBase.qml")
        if (comp.status !== Component.Ready) {
            console.warn(comp.errorString())
        }
        root.controlModel  =  comp.createObject(root, {"node": root.menuNode, "pushMenuItem": root.pushMenuItem})
        //update control external string
        updateSelectedValue()
        root.controlModel.menuDelegateProperties.valueChanged.connect(updateSelectedValueLater)
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