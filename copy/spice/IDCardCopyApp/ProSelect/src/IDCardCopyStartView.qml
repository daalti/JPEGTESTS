import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtScxml 5.8
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0

MessageLayout {
    id: idCardCopyStartingView
    objectName: "idCardCopyStartingView"

    messageType: MessageLayout.MessageType.SCREEN

    titleText: SpiceLocObject {stringId: "StringIds.cIDCardCopyApp"}

    detailTexts:
    QQmlObjectListModel{
            SpiceLocObject {stringId: "StringIds.cPlaceCardOnGlass"}
    }
    actions: QQmlObjectListModel {

        ButtonModel {
            objectName: "idCardContinueButton"
            textObject: SpiceLocObject { stringId: "StringIds.cContinue"}
            buttonType: SpiceButton.Type.Primary
            onClicked: {
                _stateMachine.submitEvent("ev.idcardcopy.continue")
            }
        }
    }
}
