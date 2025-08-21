import QtQuick 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxToastSystem 1.0
import "qrc:/QuickSetsUtils.js" as QuickSetsUtils

ButtonListLayout {

    id:quickSetSaveOptionsView
    objectName: "QuickSetSaveOptionsView"
    property string appName : ""

    header: SpiceLocObject {
        stringId: "StringIds.cSaveOptions"
    }

    actions: QQmlObjectListModel{
        ButtonModel{
            objectName: "AsDefault"
            textObject : SpiceLocObject{stringId : "StringIds.cAsDefaults"}
            onClicked: {
                ToastSystem.showMessage(ToastSystem.createSpiceLoc({"stringId": "StringIds.cSaveQuickSetMessage"}), ToastSystem.ToastState.INFORMATION,1000)
                QuickSetsUtils.saveDefaultTicket(appName,_stateMachine,ResourceStoreTypes.JOB_TICKET_1_JOB_TICKET,deleteSaveOnSuccess,failedToSave)
            }
        }

        ButtonModel{
            objectName: "NewQuickSet"
            textObject : SpiceLocObject{stringId : "StringIds.cNewQuickSet"}
            visible : false
            onClicked: {
                _stateMachine.newQuickSetName=""
                _stateMachine.newQuickSetStartInstantly=false
                _stateMachine.submitEvent("ev.newQuickSet.clicked")
            }
        }

        ButtonModel{
            objectName: "UpdateQuickSet"
            textObject : SpiceLocObject{stringId : "StringIds.cUpdateQuickSet"}
            visible : false
            onClicked: {
                //TODO Call update quickSet function
                _stateMachine.submitEvent("ev.back")
            }
        }

    }

    function deleteSaveOnSuccess(){
        _stateMachine.submitEvent("ev.back")
    }
    function failedToSave(){
        console.info("failed to save to default..")
    }
}
