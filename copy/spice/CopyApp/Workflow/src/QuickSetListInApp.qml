import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import QtQml.Models 2.15
import "qrc:/SpiceBinding.js" as SpiceBinding

SpiceModalLayout {
    id: root
    objectName: "QSListofApp"
   
    _modal: true
    modalWidth : SpiceModalLayout.SpiceModalWidthType.BIG
    modalStatus : SpiceModalLayout.SpiceModalStatus.INFORMATION
    property bool smallVersion: Global.breakpoint <= Global.BreakPoint.S
    property QQmlObjectListModel quicksetListUnderAppModel: QQmlObjectListModel{}
    property ISpiceModel quickSetsSpecificToApp:null;
    property QQmlObjectListRolesModel quicksetModelList: QQmlObjectListRolesModel{}

    header: SpiceHeaderVar1{
        id:qSListofAppHeader
        objectName: "QSListofAppHeader"
        title:SpiceLocObject{stringId: "StringIds.cQuickSetsAppHeading"}
        buttons: QQmlObjectListModel {
                        ButtonModel 
                        {
                            objectName: "CloseQuicksetList"
                            iconPath: "qrc:/images/Glyph/Close.json"
                            buttonType: SpiceButton.Type.Secondary
                            flat:true
                            onClicked: {
                                _stack.pop()
                            }
                        }

                    }
    }

    content: {
            if(smallVersion){
                console.log("content is handleListDisplay" )
                return handleListDisplay
            }
            else
            {
                console.log("content is handleRadioButtonDisplay" )
                return handleRadioButtonDisplay
            }
    }
    
    
    Component{
        id: handleRadioButtonDisplay
        SpiceGridLayout {
            id: gridLayout
            width: root.modalPaintedWidth
            Layout.alignment: Qt.AlignLeft
            gutterVertical: 3 * Global.rem
            gutterHorizontal: 3 * Global.rem
            leftMargin: 3 * Global.rem
            rightMargin: 3 * Global.rem
            topMargin: 3 * Global.rem
            bottomMargin: 3 * Global.rem
            maxItemsPerRow: Global.breakpoint === Global.BreakPoint.XL ? 5 : 4
            behavior: SpiceGridLayout.Behavior.Fixed
            itemsWidth: (width - leftMargin - rightMargin - ((maxItemsPerRow - 1) * gutterVertical)) / maxItemsPerRow

            items: ObjectModel {
                Repeater {
                    id: repeater
                    model: root.quicksetListUnderAppModel

                    delegate:SpiceRadioButton{
                                id: radioButtons
                                objectName: modelData.objectName === "" ? (modelData.textObject === null ? "" : modelData.textObject.text) : modelData.objectName
                                Layout.alignment: Qt.AlignTop | Qt.AlignHCenter
                                variation: SpiceRadioButton.Type.Variation2
                                buttonGroup: modelData.buttonGroup
                                textObject: modelData.textObject
                                checked: modelData.checked
                                icon: modelData.icon
                                permissionId: modelData.permissionId 
                                pinProtected: modelData.pinProtected                         
                                onClicked: {
                                    modelData.clicked(modelData)
                                }

                                Component.onCompleted:{
                                    SpiceBinding.twoWayBinding(radioButtons,"checked",modelData)
                                }

                                 Component.onDestruction: {
                                    SpiceBinding.destroyTwoWayBinding(radioButtons,"checked",modelData)
                                }
   
                            } 

                    onModelChanged: {
                        console.debug("onModelChanged ")
                    }
                }
            }
        }
    }

    Component{
        id: handleListDisplay

            SpiceListView{
                id: qsList
                width : root.modalPaintedWidth
                height : root.modalPaintedHeight - SpiceHeaderViewConstants.height

                rowList: root.quicksetModelList
            }
    }

    Component.onDestruction: {
        if(_stateMachine.quicksetSelectionUpdate !== undefined && !_stateMachine.quicksetSelectionUpdate) // if there is no selection done, refresh landing page of quickset panel to show the checked item
        {
            _stateMachine.quicksetSelectionUpdate = true
        }
        if(typeof quicksetData != "undefined"  && !quicksetData.quicksetSelectionUpdate)
        {
            quicksetData.quicksetSelectionUpdate = true
        }     
        if(typeof quicksetData != "undefined"  && !quicksetData.backFromQuickSetListInApp)
        {
            quicksetData.backFromQuickSetListInApp = true
        }
    }

}

