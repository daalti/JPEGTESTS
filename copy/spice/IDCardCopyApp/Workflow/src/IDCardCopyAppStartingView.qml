import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQml.Models 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0

AlertModel {
    id: idCardCopyStartView
    objectName: "idCardCopyStartView"
    closeIconSupported: false
    modalType: AlertModel.ModalType.LAYOUT1
    modalSizeRequired : AlertModel.ModalSize.BIG
    // QML doesn't take enum values with lower cases, hardcoding the value
    //alertSeverity: Alert_1_Alert_Severity.Severity.information
    alertSeverity:0

    property QtObject alertModel: QtObject {
        property string icon: "qrc:/images/Status/Informative.json"
        property SpiceLocObject message: SpiceLocObject{ stringId:  "StringIds.cIDCardFront"}
        property SpiceLocObject messageDetails: SpiceLocObject{}
        property QQmlObjectListModel messagesDetails: QQmlObjectListModel{
                                                        SpiceLocObject { stringId: "StringIds.cPlaceCardOnGlass"}
                                                    }
        property QQmlObjectListModel detailsIcon: QQmlObjectListModel{
                                                    ImageModel {
                                                        image: "qrc:/images/Graphics/IDCardCopyFrontGraph.json"
                                                    }
                                                }
        property QQmlObjectListModel actions: QQmlObjectListModel {
                                                ButtonModel {
                                                    buttonType: SpiceButton.Type.PrimaryFlow
                                                    objectName: "idCopyContinueButton"
                                                    textObject: SpiceLocObject { stringId: "StringIds.cContinue"}
                                                    variation: SpiceButton.ButtonVariation.VariationOne
                                                    onClicked: {
                                                        console.log("Continue clicked")
                                                        _stateMachine.submitEvent("ev.idcardcopy.continue")               
                                                    } 
                                                }
                                                ButtonModel {
                                                    buttonType: SpiceButton.Type.Secondary
                                                    textObject: SpiceLocObject { stringId: "StringIds.cCancel"}
                                                    variation: SpiceButton.ButtonVariation.VariationOne
                                                    objectName: "idCopyCancelButton"
                                                    onClicked: {
                                                        console.log("Cancel  - Clicked");
                                                        _stateMachine.submitEvent("ev.back")
                                                                        
                                                    }
                                                }
                                            }
    }

    alertViewModel: alertModel

}