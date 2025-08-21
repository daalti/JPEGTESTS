import QtQuick 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxToastSystem 1.0
import "qrc:/QuickSetsUtils.js" as QuickSetsUtils
AlertModel {
    id: root
    objectName: "ConfirmMessage"
    property string appName : ""
    closeIconSupported: false
    modalType: AlertModel.ModalType.LAYOUT1
    modalSizeRequired: AlertModel.ModalSize.SMALL
    signal closeQuicksetConfirmMessage();
    alertSeverity:{
                    return Alert_1_Alert_Severity.Severity.information
                }
    alertViewModel : QtObject {
        property SpiceLocObject messageDetails: SpiceLocObject{ stringId:  "StringIds.cCurrentToNewDefaults"}
        property QQmlObjectListModel actions: QQmlObjectListModel {
                                                ButtonModel {
                                                    buttonType: SpiceButton.Type.PrimaryFlow
                                                    objectName: "messageSave"
                                                    textObject: SpiceLocObject { stringId: "StringIds.cSave"}
                                                    variation: SpiceButton.ButtonVariation.VariationOne
                                                    onClicked: {
                                                        QuickSetsUtils.saveDefaultTicket(appName,_stateMachine,ResourceStoreTypes.JOB_TICKET_1_JOB_TICKET,deleteSaveOnSuccess,failedToSave)  
                                                    } 
                                                }

                                                ButtonModel {
                                                    objectName: "messageCancel"
                                                    textObject: SpiceLocObject { stringId: "StringIds.cCancel"}
                                                    variation: SpiceButton.ButtonVariation.VariationOne
                                                    onClicked: {
                                                         applicationStack.pop()        
                                                    } 
                                                }
                                            }
    }


    function deleteSaveOnSuccess(){
        console.info("save as default..")
        applicationStack.pop() 
        root.closeQuicksetConfirmMessage()
        ToastSystem.createToast("StringIds.cDefaultSettingsSaved",null,SpiceToast.SpiceToastState.INFORMATION,"",3000, "")
    }
    function failedToSave(){
        console.info("failed to save to default..")
         applicationStack.pop()
         root.closeQuicksetConfirmMessage()
        ToastSystem.createToast("StringIds.cSettingsFailed",null,SpiceToast.SpiceToastState.INFORMATION,"",3000, "")
             
    }

}
