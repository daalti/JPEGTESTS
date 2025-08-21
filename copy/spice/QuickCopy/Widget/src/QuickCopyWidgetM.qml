import QtQuick 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import QtQuick.Layouts 1.15
import QtQml.Models 2.15
import spiceuxToastSystem 1.0
import security 1.0
import inactivityTimeout 1.0

Item {
    id: copyQuickWidget
    property QQmlObjectListModel widgetProperty: QQmlObjectListModel{}
    property int numberOfCopiesMin: 1
    property int numberOfCopiesMax: 999
    property int numberOfCopies: 1
    signal copyClicked(int numberOfCopies);
    signal settingClicked(int numberOfCopies);
    property bool copyButtonEnabled: true
    property QQmlObjectListModel widgetInfoText:QQmlObjectListModel{}
    property SpiceLocObject copyConstrainedMessage:SpiceLocObject{
        stringId: "StringIds.cInsertPageInScanner"
    }
    onCopyButtonEnabledChanged: {
        console.log("Copy Button Enabled changed", copyButtonEnabled)
    }

    property bool copybuttonConstrained:false
    width: parent.width
    height: parent.height
    Item {
        anchors.top: copyQuickWidget.top
        id: topContainer
        width: copyQuickWidget.width
        height: Global.BreakPoint.M === Global.breakpoint ? copyQuickWidget.height * 0.68 : Global.BreakPoint.L === Global.breakpoint ? copyQuickWidget.height * 0.68 : copyQuickWidget.height * 0.65

        SpiceGridLayout {
            id: topGrid
            width: topContainer.width-(2*leftMargin)
            height: topContainer.height
            maxItemsPerRow: 1
            topMargin:0.5 * Global.rem
            leftMargin:4*Global.rem
            rightMargin:4*Global.rem
            bottomMargin:0.5 * Global.rem
            gutterHorizontal:0.5 * Global.rem
            gutterVertical: 0.5 * Global.rem
            behavior: SpiceGridLayout.Behavior.Fixed

            itemsWidth: topContainer.width -(2*leftMargin)

            items: ObjectModel {
                    SpiceTextImage {
                        Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                        titlesSmallTexts: QQmlObjectListModel { SpiceLocObject { stringId: "StringIds.cCopy" } }
                    }

                    SpiceTextImage {
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        height: Global.BreakPoint.M === Global.breakpoint ? topGrid.height * 0.2 : Global.BreakPoint.L === Global.breakpoint ? topGrid.height * 0.2 : topGrid.height * 0.25
                        variation: SpiceTextImage.Variation.ImageContainer
                        images: ["qrc:/images/placeholder/image_60x70.png"]
                    }
                    SpiceTextImage {
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        contentsSmallTexts: QQmlObjectListModel { SpiceLocObject { stringId: "StringIds.cDefault" } }
                    }
                        
                    SpiceGridLayout {
                        width: topGrid.itemsWidth
                        height: topGrid.height * 0.25
                        maxItemsPerRow: 1
                        itemsWidth: topGrid.itemsWidth
                        gutterHorizontal:0.1*Global.rem
                        leftMargin: 0.5 * Global.rem
                        behavior: SpiceGridLayout.Behavior.Fixed
                        items:ObjectModel{
                            SpiceDivider {
                                Layout.fillWidth: true
                                type: SpiceDivider.Type.DV2H
                                lineWidth: topGrid.width
                                opacity:0.1
                                padding: SpiceSpacerViewConstants.sp2_height
                            }
                            Repeater{
                                model: copyQuickWidget.widgetProperty ? copyQuickWidget.widgetProperty.size():0
                                delegate:Item{
                                    
                                    id:innerContainer
                                    Layout.fillWidth:true
                                    Layout.minimumHeight: 2*Global.rem
                                    Layout.maximumHeight: 10*Global.rem
                                    SpiceTextImage{
                                        anchors.top:innerContainer.top
                                        anchors.left:innerContainer.left
                                        height:innerContainer.height-dividerid.height
                                        width:innerContainer.width*0.4
                                        onlyTextAlign: Text.AlignLeft
                                        clarificationsTexts:QQmlObjectListModel{   SpiceLocObject{ stringId:copyQuickWidget.widgetInfoText.get(modelData).stringId}}
                                    }
                                    SpiceTextImage{
                                        anchors.top:innerContainer.top
                                        anchors.right: innerContainer.right
                                        height:innerContainer.height-dividerid.height
                                        width:innerContainer.width*0.6
                                        onlyTextAlign: Text.AlignRight
                                        clarificationsTexts: QQmlObjectListModel{ SpiceLocObject{ stringId:copyQuickWidget.widgetProperty.get(modelData).stringId}}
                                    }
                                    SpiceDivider {
                                        id:dividerid
                                        anchors.bottom:innerContainer.bottom
                                        anchors.left:innerContainer.left
                                        Layout.fillWidth: true
                                        type: SpiceDivider.Type.DV2H
                                        lineWidth: topGrid.width
                                        opacity:0.1
                                        padding: SpiceSpacerViewConstants.sp2_height
                                    }
                                }
                            }
                        }
                    }
            }
        }
    }

    Item {
        id: bottomContainer
        anchors.top: topContainer.bottom
        width: parent.width
        height: parent.height * 0.20

        SpiceGridLayout {
            width: bottomContainer.width

            height: bottomContainer.height
            maxItemsPerRow: 1
            topMargin:0.5 * Global.rem
            gutterHorizontal:0.5 * Global.rem
            gutterVertical: 0.5 * Global.rem
            itemsWidth: topContainer.width - 3* Global.rem
            behavior: SpiceGridLayout.Behavior.Fixed
           
            items: ObjectModel {
                    Item {
                        Layout.fillWidth:true
                        height:spinboxid.height
                        Layout.alignment: Qt.AlignHCenter
                        SpiceSpinBox {
                            id:spinboxid
                            anchors.centerIn:parent
                            objectName: "copyWidgetSpinBox"
                            value: copyQuickWidget.numberOfCopies
                            from: copyQuickWidget.numberOfCopiesMin
                            to: copyQuickWidget.numberOfCopiesMax
                            enabled:copyWidgetStartButton._permitted
                            onValueChanged: {
                                copyQuickWidget.numberOfCopies = value
                            }
                        }
                    }
                    RowLayout {
                        Layout.alignment: Qt.AlignCenter
                        SpiceButton {
                            id: optionsDetailPanelButton
                            objectName: "copyWidgetSettingsButton"
                            icon: "qrc:/images/Glyph/PrintMode.json"
                            Layout.alignment: Qt.AlignLeft
                            type: SpiceButton.Type.Secondary
                            enabled:copyWidgetStartButton._permitted
                            variation: SpiceButton.ButtonVariation.VariationOne
                            onClicked: {
                                copyQuickWidget.settingClicked(numberOfCopies)
                                spinboxid.value = 1
                            }
                        }
                        SpiceButton {
                            id:copyWidgetStartButton
                            width: 15*Global.rem
                            Layout.alignment: Qt.AlignRight
                            textObject: SpiceLocObject { stringId: "StringIds.cCopy"}
                            type: SpiceButton.Type.Primary
                            objectName: "copyWidgetStartButton"
                            variation: SpiceButton.ButtonVariation.VariationOne
                            enabled: copyQuickWidget.copyButtonEnabled
                            permissionId:"ef92c290-8fa5-4403-85bc-f6becc86b787" 
                            onClicked: {
                                console.log("Copy Clicked !!")
                                if(copyQuickWidget.copybuttonConstrained)
                                {
                                    _stack.pushModal("qrc:/components/SpiceConstraintMessage.qml",{"message": copyQuickWidget.copyConstrainedMessage.text})
                                }
                                else
                                {
                                    copyQuickWidget.copyClicked(numberOfCopies)
                                }
                            }    
                        }     
                    }
            }
        Component.onCompleted: {
            console.log("quick copy widget completed")
            _inactivityTimer.fired.connect(resetNumberOfCopies)
        }

        Component.onDestruction: {
            _inactivityTimer.fired.disconnect(resetNumberOfCopies)
        }

        function resetNumberOfCopies()
        {
            console.log("quick copy widget resetNumberOfCopies")
            spinboxid.value = 1
        }
    }
}
}