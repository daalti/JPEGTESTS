import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0

SpiceModalLayout
{
    id: root
    objectName: "QuickSetSaveTicketChanged"
    enum ModificationOptions{
        UNDEFINED,
        AS_DEFAULT,
        NEW_QUICKSET,
        UPDATE_QUICKSET        
    }

    _modal: true
    modalWidth : SpiceModalLayout.SpiceModalWidthType.BIG
    modalStatus : SpiceModalLayout.SpiceModalStatus.INFORMATION
    property int selectedOption : QuickSetSaveTicketChanged.ModificationOptions.AS_DEFAULT

    header: SpiceHeaderVar1{
        id:saveoptionHeader
        objectName: "saveoptionHeader"
        title:SpiceLocObject{stringId: "StringIds.cSaveOptions"}
    }
      
    footer: SpiceFooter {
        id:saveoptionFooter
        objectName : "saveoptionFooter"
        width: parent.width
        rightBlockModel: QQmlViewListModel {
            SpiceButton{
                Layout.alignment: Qt.AlignRight
                textObject.stringId: "StringIds.cSave"
                objectName: "saveoptionOK"
                type: SpiceButton.Type.PrimaryFlow

                onClicked: {
                    // _stateMachine.submitEvent("ev.quicksetConfirmSave");
                   let confirmMessage= applicationStack.pushModal("qrc:/CopyApp/QuickSetConfirmMessage.qml",{"appName":"CopyApp"})
                   confirmMessage.closeQuicksetConfirmMessage.connect(function(){
                       applicationStack.pop()
                   })
                   confirmMessage.Component.onDestruction.connect(function(){
                        confirmMessage.closeQuicksetConfirmMessage.disconnect(function(){
                       applicationStack.pop()
                   })
                   })
                }
            }
            SpiceButton{
                Layout.alignment: Qt.AlignRight
                textObject.stringId: "StringIds.cCancel"
                objectName: "saveoptionCancel"
                type: SpiceButton.Type.Secondary

                onClicked: {
                    applicationStack.pop()
                }
            }
            
        }
    }   
    content: 
        SpiceListListLayout {
            
            id : saveOptions
            objectName : "SaveOptionsForQS"
            width : root.modalPaintedWidth
            height : root.modalPaintedHeight - SpiceFooterViewConstants.height - SpiceHeaderViewConstants.height
            rowList1 : QQmlObjectListRolesModel{
                        SettingsRadioButtonViewModel
                        {
                            id : asDefaults
                            controlModel : RadioButtonModel
                            {
                                textObject:SpiceLocObject { stringId: "StringIds.cAsDefaults" }
                                objectName: "AsDefaults"
                                checked: root.selectedOption == QuickSetSaveTicketChanged.ModificationOptions.AS_DEFAULT
                                onClicked: {
                                    root.selectedOption = QuickSetSaveTicketChanged.ModificationOptions.AS_DEFAULT
                                    console.log("As default is selected")
                                }
                            }
                        }

                        SettingsRadioButtonViewModel
                        {
                            id : newQuickSet
                            controlModel : RadioButtonModel
                            {
                                textObject: SpiceLocObject { stringId: "StringIds.cNewQuickSet" }
                                objectName: "NewQuickSet"
                                visible:false
                                checked: false
                                onClicked: {
                                    console.log("new QuickSet is selected")
                                }
                            }
                        }
                        SettingsRadioButtonViewModel
                        {
                            id : updateQuickSet
                            controlModel : RadioButtonModel
                            {
                                textObject: SpiceLocObject { stringId: "StringIds.cUpdateQuickSet" }
                                objectName: "UpdateQuickSet"
                                visible:false
                                checked: false
                                onClicked: {
                                    console.log("updateQuickSet is selected")
                                }
                            }
                        }                        
            }

        }
    
}
