import QtQuick 2.15
import QtQuick.Layouts 1.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxMenu 1.0
import QtQml.Models 2.15
import QtQuick.Controls 2.15
import "qrc:/imports/spiceuxToastSystem/SpiceToastUtils.js" as SpiceToastUtils

SpiceAppLandingLayout {
    objectName: "idCopyLandingView"
    id: root
    property bool copyButtonEnabled: false
    property bool isCancelButtonVisible: false
    property bool isEditButtonEnabled: false
    property string animationPath: ""

    property bool smallVersion: Global.breakpoint <= Global.BreakPoint.S
    signal cancelButtonClicked;

    headerMain: SpiceHeaderVar2 {
        customText: SpiceLocObject { stringId: "StringIds.cIDCardCopyApp" }
    }

    headerDetail: SpiceHeaderVar2 {
        customText: SpiceLocObject { stringId: "StringIds.cIDCardCopyApp" }
    }

    mainImage: root.animationPath

    detailComponentModel: MenuInteractiveSummaryList {
        node: "idCopyInteractiveSummary"
        interctiveSummaryList : _stateMachine.summaryList
        resourceModel: _stateMachine.ticketModelForSettings
        resourceInstance: _idCardCopySettingsResource

    }

    property bool secondaryPanelVisible: smallVersion ? _scanPreviewSupported : true
    secondaryPanel: secondaryPanelVisible? (templatePriority === SpiceAppLandingLayout.TemplatePriority.DetailPanelTemplate ? (Global.breakpoint > Global.BreakPoint.S ?subLevel2: subLevel1 ) : Global.breakpoint > Global.BreakPoint.S ? subLevel1: subLevel2):null

    footerMain: SpiceFooter {
        rightBlockModel: ObjectModel {
            
            SpiceButton {
                Layout.alignment: Qt.AlignRight
                textObject.stringId: (Global.breakpoint === Global.BreakPoint.XS) ? "" : "StringIds.cCopy"
                type: SpiceButton.Type.Primary
                objectName: "copyPreviewPanelButton"
                variation: SpiceButton.ButtonVariation.VariationOne
                enabled: root.copyButtonEnabled
                visible: active
                active: root.smallVersion || root.isSecondaryCollapsed
                icon: "qrc:/images/Glyph/InstantLaunch.json"
                 onClicked: {
                     if(_stateMachine.isPrinterIdle)
                    {
                        console.log("Copy clicked")
                        _stateMachine.submitEvent("ev.start.idcard_copy")               
                    }
                    else
                    {
                        console.log("Printer is busy")
                        _stateDecorator.showHighestError()
                    }             
                }                                   
            }

            //the Cancel button will only be visible if there is jobInProgress from Landing Page
            SpiceButton {
                id: cancelButton
                objectName: "cancelButton"
                textObject.stringId: (Global.breakpoint === Global.BreakPoint.XS) ? "" : "StringIds.cCancel"
                visible: active
                active: root.isCancelButtonVisible && (root.smallVersion || root.isSecondaryCollapsed)
                Layout.alignment: Qt.AlignRight
                type: SpiceButton.Type.Destructive
                variation: SpiceButton.ButtonVariation.VariationOne
                icon: Global.breakpoint == Global.BreakPoint.XS ? "qrc:/images/Glyph/Cancel.json" : ""
                
                onClicked: {
                    console.log("Cancel button clicked")
                    root.cancelButtonClicked();
                }
            }
        }
    }

    footerDetail: SpiceFooter {
        rightBlockModel: ObjectModel {
            
            SpiceButton {
                Layout.alignment: Qt.AlignRight
                textObject.stringId: (Global.breakpoint === Global.BreakPoint.XS) ? "" : "StringIds.cCopy"
                type: SpiceButton.Type.Primary
                objectName: "copyDetailPanelButton"
                variation: SpiceButton.ButtonVariation.VariationOne
                icon: "qrc:/images/Glyph/InstantLaunch.json"
                enabled: root.copyButtonEnabled
                 onClicked: {
                    if(_stateMachine.isPrinterIdle)
                    {
                        console.log("Copy clicked")
                        _stateMachine.submitEvent("ev.start.idcard_copy")               
                    }
                    else
                    {
                        console.log("Printer is busy")
                        if(!!_statusCenter && !!_statusCenter.dashboard)
                        {
                            _statusCenter.changeDashboardState("EXPANDED")
                        }
                        else
                        {
                            SpiceToastUtils.launchAppIfPermitted("JobQueueApp", _applicationEngine)
                        }
                    }
                }                                   
            }

            //the Cancel button will only be visible if there is jobInProgress from Landing Page
            SpiceButton {
                id: cancelButton
                objectName: "cancelButtonDetailPanel"
                textObject.stringId: (Global.breakpoint === Global.BreakPoint.XS) ? "" : "StringIds.cCancel"
                active: root.isCancelButtonVisible
                visible: active
                Layout.alignment: Qt.AlignRight
                type: SpiceButton.Type.Destructive
                variation: SpiceButton.ButtonVariation.VariationOne
                icon: Global.breakpoint == Global.BreakPoint.XS ? "qrc:/images/Glyph/Cancel.json" : ""
        
                onClicked: {
                    console.log("Cancel button clicked")
                    root.cancelButtonClicked();
                }
            }

            SpiceButton {
                Layout.alignment: Qt.AlignRight
                type: SpiceButton.Type.Secondary
                variation: SpiceButton.ButtonVariation.VariationOne
                objectName: "optionsDetailPanelButton"
                enabled: root.isEditButtonEnabled
                icon: "qrc:/images/Glyph/PrintMode.json"
                 onClicked: {
                    console.log("ID Copy OPTIONS  - Clicked");
                    _stateMachine.submitEvent("ev.options.clicked")
                                   
                }
            }
            
        }
    }


    Component.onCompleted: {
        console.log("IDCard App Landing Page Loaded")
    }
}