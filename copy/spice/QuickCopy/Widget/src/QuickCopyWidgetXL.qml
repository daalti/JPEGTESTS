import QtQuick 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import QtQuick.Layouts 1.15
import QtQml.Models 2.15
import spiceuxToastSystem 1.0
import "qrc:/SpiceBinding.js" as SpiceBinding
import security 1.0
import inactivityTimeout 1.0

Rectangle {
    id: copyQuickWidget
    objectName:"copyQuickWidget"

    property QQmlObjectListModel widgetProperty: QQmlObjectListModel{}

    property int numberOfCopiesMin: 1
    property int numberOfCopiesMax: 999
    property int numberOfCopies: 1

    signal copyClicked(int numberOfCopies);
    signal settingClicked(int numberOfCopies);

    property bool copyButtonEnabled: true

    property bool isAnaSignInRequired: !AnaService.isPermitted(PermissionIds.cp_copy_app)
    
    property QQmlObjectListModel widgetInfoText:QQmlObjectListModel{}

    onCopyButtonEnabledChanged: {
        console.log("Copy Button Enabled changed", copyButtonEnabled)
    }

    property bool copybuttonConstrained:false

    color: ColorConstants.box2B
    border.color: ColorConstants.colorStroke2
    radius: SpiceCornerRadiusConstants.cr3


    width: parent.width
    height: parent.height

    anchors.margins: 1.5*Global.rem

    SpiceGridLayout {
        id: topContainer
        maxItemsPerRow: 1
        width: copyQuickWidget.width
        height:5.5*Global.rem
        anchors.top: copyQuickWidget.top
        anchors.horizontalCenter: parent.horizontalCenter
        topMargin:SpiceSpacerViewConstants.sp5_height
        leftMargin:SpiceSpacerViewConstants.sp5_height
        rightMargin:SpiceSpacerViewConstants.sp5_height
        bottomMargin:SpiceSpacerViewConstants.sp5_height
        behavior: SpiceGridLayout.Behavior.Fixed
        itemsWidth: topContainer.width -leftMargin - rightMargin
        items: ObjectModel {
            SpiceTextImage {
                id: widgetTitle
                Layout.preferredWidth: topContainer.itemsWidth
                titlesSmallTexts: QQmlObjectListModel { SpiceLocObject { stringId: "StringIds.cCopy" } }
                imagesAlignMiddle: true
            }
        }
    }

    SpiceGridLayout {
        id: contentArea
        anchors.top: topContainer.bottom
        anchors.bottom: bottomContainer.top
        anchors.left: copyQuickWidget.left
        width: copyQuickWidget.width
        positioning: SpiceGridLayout.Positioning.CenteredAuto
        behavior: SpiceGridLayout.Behavior.Fixed
        topMargin:0 * Global.rem
        leftMargin:0
        rightMargin:0
        bottomMargin:SpiceSpacerViewConstants.sp5_height
        gutterHorizontal:0
        gutterVertical:0
        maxItemsPerRow: 1
        itemsWidth: contentArea.width
        items: ObjectModel {

            SpiceTextImage {
                id: cellOne
                height: 8.5* Global.rem
                width: 22* Global.rem
                variation: SpiceTextImage.Variation.ImageContainer
                images: ["qrc:/images/Graphics/Copy.json"]
                Layout.alignment: Qt.AlignHCenter
            }

            SpiceSpacer {
                id: cellTwo
                width: 22* Global.rem
                height:1*Global.rem
                type: SpiceSpacer.Type.SP4
            }

            SpiceTextImage {
                id: cellThree
                objectName:"copyWidgetQuicksetName"
                onlyTextAlign: Text.AlignHCenter
                width: 22* Global.rem
                height: 3.23 * Global.rem
                contentsSmallTexts: QQmlObjectListModel { SpiceLocObject { stringId: "StringIds.cDefault" } }
                Layout.alignment: Qt.AlignCenter
                Layout.preferredWidth: contentArea.itemsWidth
            }

            SpiceSpacer {
                id: cellFour
                width: 22* Global.rem
                height: 1.5 * Global.rem
                type: SpiceSpacer.Type.SP5
            }

            SpiceGridLayout {
                id: cellFive
                width: 22* Global.rem
                height: 12.5*Global.rem
                maxItemsPerRow: 1
                itemsWidth: contentArea.width - leftMargin - rightMargin
                gutterHorizontal:1
                gutterVertical: 0
                leftMargin:2.58 * Global.rem
                rightMargin:2.58 * Global.rem
                topMargin:0
                bottomMargin:0
                Layout.alignment: Qt.AlignCenter
                behavior: SpiceGridLayout.Behavior.Fixed

                items:ObjectModel{

                    SpiceDivider {
                                id:dividerid
                                padding:0
                                color:ColorConstants.neutral030
                                type: SpiceDivider.Type.DV2H
                                height:2
                            }
                    
                    Repeater{
                        model: copyQuickWidget.widgetProperty ? copyQuickWidget.widgetProperty.size():0
                        delegate:Item{
                            id:innerContainer
                            height:2.64*Global.rem
                            SpiceTextImage{
                                anchors.top:innerContainer.top
                                anchors.left:innerContainer.left
                                width:innerContainer.width*0.5
                                onlyTextAlign: Text.AlignLeft
                                clarificationsTexts:QQmlObjectListModel{   SpiceLocObject{ stringId:copyQuickWidget.widgetInfoText.get(modelData).stringId}}
                            }
                            SpiceTextImage{
                                anchors.top:innerContainer.top
                                anchors.right: innerContainer.right
                                width:innerContainer.width*0.5
                                onlyTextAlign: Text.AlignRight
                                clarificationsTexts: QQmlObjectListModel{ SpiceLocObject{ stringId:copyQuickWidget.widgetProperty.get(modelData).stringId}}
                            }
                            SpiceDivider {
                                id:dividerid
                                padding:0
                                anchors.bottom:innerContainer.bottom
                                anchors.left:innerContainer.left
                                anchors.right:innerContainer.right
                                color:ColorConstants.neutral030
                                type: SpiceDivider.Type.DV2H
                                height:2
                            }
                            
                        }
                    }
                }
                
            }

            SpiceSpacer {
                id: cellSix
                height:1.5*Global.rem
                width:22*Global.rem
                type: SpiceSpacer.Type.SP5
            }

            Item {
                id: cellSeven
                objectName: "copyWidgetSpinBoxContainer"
                height:6.8*Global.rem
                width:22*Global.rem
                Layout.alignment: Qt.AlignCenter
                Layout.maximumWidth: contentArea.width - (SpiceSpacerViewConstants.sp5_height*2)
                SpiceSpinBox {
                    id:spinboxid
                    anchors.centerIn:parent
                    objectName: "copyWidgetSpinBox"
                    value: copyQuickWidget.numberOfCopies
                    from: copyQuickWidget.numberOfCopiesMin
                    to: copyQuickWidget.numberOfCopiesMax
                    enabled:copyWidgetStartButton._permitted

                    Component.onCompleted: {
                                SpiceBinding.twoWayBinding(spinboxid, "value", copyQuickWidget,"numberOfCopies");
                    }

                    Component.onDestruction: {
                                SpiceBinding.destroyTwoWayBinding(spinboxid, "value", copyQuickWidget,"numberOfCopies");
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

    SpiceGridLayout {
        id: anaSignInContentArea
        anchors.top: topContainer.bottom
        anchors.bottom: anaSignInBottomContainer.top
        anchors.left: copyQuickWidget.left
        width: copyQuickWidget.width
        anchors.centerIn: copyQuickWidget
        topMargin:0
        leftMargin:0
        rightMargin:0
        bottomMargin:SpiceSpacerViewConstants.sp5_height
        gutterHorizontal: 0
        gutterVertical: 0
        maxItemsPerRow: 1
        positioning: SpiceGridLayout.Positioning.CenteredAuto
        behavior: SpiceGridLayout.Behavior.Fixed
        itemsWidth: copyQuickWidget.width
        items: ObjectModel {
            SpiceTextImage {
                id: anaSignInCellOne
                height: 8.5* Global.rem
                Layout.alignment: Qt.AlignHCenter
                variation: SpiceTextImage.Variation.ImageContainer
                images: ["qrc:/images/Graphics/LockCircle.json"]
            }
            SpiceSpacer {
                id: anaSignInCellTwo
                type: SpiceSpacer.Type.SP4
            }
            SpiceTextImage {
                id: anaSignInCellThree
                Layout.alignment: Qt.AlignHCenter
                onlyTextAlign: Text.AlignHCenter
                width: contentArea.width
                variation: SpiceTextImage.Variation.TextImage
                contentsSmallTexts: QQmlObjectListModel { SpiceLocObject { stringId: "StringIds.cSignInToUseFeature" } }
            }
        }
    }

    SpiceCard{
        id:bottomContainer 
        expandable: false
        selectable: false
        clickable: true
        height: 7 * Global.rem
        width: copyQuickWidget.width
        anchors.bottom: copyQuickWidget.bottom
        backgroundColor: ColorConstants.box2B
        cardType: SpiceCard.SpiceCardType.DEFAULT
        content: SpiceGridLayout {
            id: bottomContainerArea
            width: copyQuickWidget.width
            topMargin:SpiceSpacerViewConstants.sp5_height
            leftMargin:0
            rightMargin:0
            bottomMargin:0
            gutterHorizontal: 0
            gutterVertical: 0
            maxItemsPerRow: 3
            positioning: SpiceGridLayout.Positioning.CenteredAuto
            behavior: SpiceGridLayout.Behavior.Fixed
            Layout.alignment: Qt.AlignVCenter
            items: ObjectModel {
                    SpiceButton {
                            id: optionsDetailPanelButton
                            objectName: "copyWidgetSettingsButton"
                            Layout.alignment: Qt.AlignVCenter
                            textObject: SpiceLocObject {stringId: "StringIds.cOptions"}
                            type: SpiceButton.Type.Secondary
                            variation: SpiceButton.ButtonVariation.VariationOne
                            onClicked: {
                                copyQuickWidget.settingClicked(numberOfCopies)
                                copyQuickWidget.numberOfCopies = 1;//Reset number of copies to 1 for next use
                            }
                        }

                        SpiceSpacer {
                            type: SpiceSpacer.Type.SP4
                        }
                    
                        SpiceButton {
                            id:copyWidgetStartButton
                            objectName: "copyWidgetStartButton"
                            Layout.alignment: Qt.AlignVCenter
                            textObject: SpiceLocObject { stringId: "StringIds.cCopy"}
                            icon: "qrc:/images/Glyph/InstantLaunch.json";
                            enabled: copyQuickWidget.copyButtonEnabled
                            type: SpiceButton.Type.Primary
                            variation: SpiceButton.ButtonVariation.VariationOne
                            onClicked: {
                                console.log("Copy Clicked !!")
                                copyQuickWidget.copyClicked(numberOfCopies)
                                copyQuickWidget.numberOfCopies = 1;//Reset number of copies to 1 for next use
                            }
                        }
            }
        }        
    }


    SpiceDivider {
        id: anaSignInBottomContainerDivider
        anchors.bottom: anaSignInBottomContainer.top
        padding: 0
        color: ColorConstants.colorForeground
        type: SpiceDivider.Type.DV2H
        opacity: _selector.highContrastEnabled ? 1 : 0.14
        width: root.width
        height: 2
    }     

    SpiceCard{
        id: anaSignInBottomContainer
        expandable: false
        selectable: false
        clickable: true
        height: 7 * Global.rem
        width: copyQuickWidget.width
        anchors.bottom: copyQuickWidget.bottom
        backgroundColor: ColorConstants.box2B
        cardType: SpiceCard.SpiceCardType.DEFAULT
        content: SpiceGridLayout {
            id: anaSignInBottomContainerArea
            width: copyQuickWidget.width
            topMargin:SpiceSpacerViewConstants.sp5_height
            leftMargin:0
            rightMargin:0
            bottomMargin:0
            gutterHorizontal: 0
            gutterVertical: 0
            maxItemsPerRow: 1
            positioning: SpiceGridLayout.Positioning.CenteredAuto
            behavior: SpiceGridLayout.Behavior.Fixed
            Layout.alignment: Qt.AlignVCenter
            items: ObjectModel {
                    SpiceButton {
                    id:widgetSignInButton
                    objectName: "widgetSignInButton"
                    textObject: SpiceLocObject{stringId: "StringIds.cSignIn"}
                    type: SpiceButton.Type.PrimaryFlow
                    Layout.alignment: Qt.AlignCenter
                    variation: SpiceButton.ButtonVariation.VariationOne
                    onClicked: {
                        console.log("onSignInButtonClicked")
                        SecuritySingleton.securityModuleLoader.execute(PermissionIds.cp_copy_app, function(){
                            copyQuickWidget.isAnaSignInRequired = false
                        })
                }
                }
            }
        }        
    }

    states: [
        State {
            when: !copyQuickWidget.isAnaSignInRequired
            name: "STATE_ANA_SIGNED_IN"

            PropertyChanges { target: contentArea; visible: true }
            PropertyChanges { target: anaSignInContentArea; visible: false }
            PropertyChanges { target: bottomContainer; visible: true }
            PropertyChanges { target: anaSignInBottomContainer; visible: false }
        },
        State {
            when: copyQuickWidget.isAnaSignInRequired
            name: "STATE_ANA_NOT_SIGNED_IN"

            PropertyChanges { target: contentArea; visible: false }
            PropertyChanges { target: anaSignInContentArea; visible: true }
            PropertyChanges { target: bottomContainer; visible: false }
            PropertyChanges { target: anaSignInBottomContainer; visible: true }
        }
    ]

    function createContentText(textToDisplay){
        let contentsTexts = _qmlUtils.createCollection(copyQuickWidget)
        contentsTexts.append(textToDisplay);
        return contentsTexts

    }


    Component.onCompleted: {
        if (SecuritySingleton.securityModuleLoader !== null) {
            Qt.callLater(securityModuleLoaded)
        }
        else {
            SecuritySingleton.securityModuleLoaderChanged.connect(securityModuleLoaded)
        }
    }

    Component.onDestruction: {
        SecuritySingleton.securityModuleLoaderChanged.disconnect(securityModuleLoaded)
    }

    function securityModuleLoaded()
    {
        if (SecuritySingleton.securityModuleLoader === null) return
        copyQuickWidget.isAnaSignInRequired = !SecuritySingleton.securityModuleLoader.isPermitted(PermissionIds.cp_copy_app)
        SecuritySingleton.securityModuleLoader.securityContext.connect(()=>{
                                                                            if(copyQuickWidget){
                                                                                copyQuickWidget.isAnaSignInRequired = !SecuritySingleton.securityModuleLoader.isPermitted(PermissionIds.cp_copy_app)
                                                                            }
                                                                       })
    }
}






