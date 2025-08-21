import QtQuick 2.15
import QtQml 2.15
import QtQuick.Layouts 1.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxMenu 1.0
import QtQml.Models 2.15

import "qrc:/SpicePropertyValueFromModel.js" as SpicePropertyValueFromModel
import "qrc:/menu/MenuDelegateApplier.js" as DelegateApplier

RadioButtonModel {
    id: root
    property var menuNode:null
    property var pushMenuItem : null
    property int checkedValue_
    property int unCheckedValue_

    readonly property QtObject menuDelegateProperties : MenuDelegateProperties{}

    objectName: menuNode ? menuNode["id"] + "MenuRadioButton" : "MenuRadioButton"

    //menuNode is set by MenuList as it initializes this component
    //Enumeration value(int) from the resource which will set the state to checked and unchecked
    //are noted in variables checkedValue_ and unCheckedValue_. Values are read from property Map
    onMenuNodeChanged: {
        if (menuNode !== null) 
        {
            let dataObj = _templatesData.valueMapFromList("menuRadioButtons", menuNode.id)
            const propDict = (dataObj === null) ? null : dataObj.asMap()
            if(propDict !== null && propDict.hasOwnProperty("infoText"))
            {
                root.infoText.stringId = propDict["infoText"]
            }
            if(propDict !== null && propDict.hasOwnProperty("description"))
            {
                root.description.stringId = propDict["description"]
            }
            if(propDict !== null && propDict.hasOwnProperty("icon"))
            {
                root.icon = propDict["icon"]
            }
            if(propDict !== null && propDict.hasOwnProperty("titleId"))
            {
                _qmlUtils.validateStringId(propDict.titleId)
                root.textObject.stringId=Qt.binding(function(){return propDict.titleId;})
            }
            if(propDict !== null && propDict.hasOwnProperty("ON"))
            {
                checkedValue_=_menuResource.enumForMenuEnumString(propDict.ON)
            }
            if(propDict !== null && propDict.hasOwnProperty("OFF"))
            {
                unCheckedValue_=_menuResource.enumForMenuEnumString(propDict.OFF)
            }
            if(propDict !== null && propDict.hasOwnProperty("valueResource"))
            {
                menuDelegateProperties.valueResource_=propDict.valueResource
            }
            if(propDict !== null && propDict.hasOwnProperty("constraint"))
            {
                menuDelegateProperties.constraint = propDict["constraint"]
            }
            if (!propDict)
            {
                console.log("Couldn't find dictionary for id: ${menuNode.id}")
                console.log(_templatesData.valueMapFromList("menuRadioButtons", 'supplyPolicy'))
                return
            }

            DelegateApplier.createDelegates(menuNode)
        }
    }

    //toggle ISpiceModel field to checkedValue_ or unCheckedValue_ depending on current value
    //trigger a patch
    onClicked: {
        let obj_= _qmlUtils.parseMenuResourceEntry(menuDelegateProperties.valueResource_)
        let propArray = obj_[1]
        let field=propArray.pop()
        let obj=SpicePropertyValueFromModel.findPropertyValueFromModelForPropertyArray(menuDelegateProperties.dataModel, propArray)
        if (obj[field] != checkedValue_)
        {
            obj[field]=checkedValue_
            _resourceStore.modify(menuDelegateProperties.dataModel)
        }
    }

    onVisibleChanged:{
        if (visible && menuDelegateProperties.valueResource_ !== "" ) {
            DelegateApplier.getResource()
        }

    }

    //using value to set checked to not cause a binding loop
    Component.onCompleted: {
        menuDelegateProperties.valueChanged.connect(function() {
            checked = (menuDelegateProperties.value== checkedValue_)
        })
    }

    Component.onDestruction: {
        menuDelegateProperties.valueChanged.disconnect()
    }

}
