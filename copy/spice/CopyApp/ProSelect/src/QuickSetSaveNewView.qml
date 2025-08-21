import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtScxml 5.8
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxToastSystem 1.0
import "qrc:/QuickSetsUtils.js" as QuickSetsUtils

BaseView {
    id: quickSetSaveNewView
    objectName: "QuickSetSaveNewView"

    contentComponent: Column {

        SpiceTextImage {
            id: headerText
            objectName: "Header"
            textObject: SpiceLocObject{stringId: "StringIds.cSaveQuickSetTitle"}
            type: SpiceTextImage.Type.TitleImage
            active: textObject !== null
        }

        SpiceSpacer {
            type: SpiceSpacer.Type.SP3
        }

        SpiceNameValue {
            id: nameValueOfNewQuickSet
            objectName: "NameValueOfNewQuickSet"
            width: parent.width
            model:NameValueModel {
                objectName: "NameOfNewQuickSet"
                valueText: SpiceLocObject{stringId: "StringIds.cName"}
                valueButton: ButtonModel {
                    objectName: "NewQuickSetNameButton"
                    textObject.text: _stateMachine.newQuickSetName
                    onClicked: {
                        _stateMachine.submitEvent("ev.enterQuickSetName.selected")
                    }
                }
            }
        }

        SpiceSpacer {
            type: SpiceSpacer.Type.SP3
            anchors.horizontalCenter: parent.horizontalCenter
        }


        SpiceCheckBox{
            id: startInstantlyOption
            objectName: "StartInstantlyOption"
            width: parent.width
            textObject:SpiceLocObject{stringId: "StringIds.cStartInstantly"}
            checked: false
            onCheckedChanged: {
                if (checked)
                {
                    _stateMachine.newQuickSetStartInstantly = true
                }
                else
                {
                    _stateMachine.newQuickSetStartInstantly = false
                }
            }
        }

        SpiceSpacer {
            type: SpiceSpacer.Type.SP2
        }

        SpiceButton{
            id: saveNewQuickSetButton
            objectName: "SaveNewQuickSetButton"
            anchors.horizontalCenter: parent.horizontalCenter
            textObject: SpiceLocObject{stringId:"StringIds.cSave"}
            type: SpiceButton.Type.Primary
            onClicked: {
                console.log("SaveNewQuickSetButton clicked")
                //TODO Save QuickSet to be called
                ToastSystem.showMessage(ToastSystem.createSpiceLoc({"stringId": "StringIds.cSaveQuickSetMessage"}), ToastSystem.ToastState.INFORMATION,1000)
                _stateMachine.submitEvent("ev.back")
            }
        }

    }
}
