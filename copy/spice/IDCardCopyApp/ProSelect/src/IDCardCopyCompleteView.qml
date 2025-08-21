import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtScxml 5.8
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0

SpiceView {
    objectName: "idCardCopyCompleteView"

    sourceComponent: BaseView {
        anchors { left: parent.left; right: parent.right }

        contentComponent: Column {
            width: parent.width

//            SpiceImage {
//                id: idCardCopyCompleteTick
//                objectName: "idCardCopyCompleteTick"
//                source: "qrc:/images/checkmark_s.svg"
//            }

            SpiceText{
                textObject: SpiceLocObject{stringId: "StringIds.cCopyCompleteMessage"}

                type: SpiceText.Type.H5
            }
        }
    }

    Timer{
        id: idCardCopyCompleteTimeout
        objectName: "idCardCopyCompleteTimeout"
        running: false
        interval: 3000
        repeat: false
        onTriggered: {
            console.log("idCardCopyCompleteView timeout: move to init")
            _stateMachine.submitEvent("ev.idcardcopy.restart")
        }
    }

    Component.onCompleted: {
        console.log("idCardCopyCompleteView");
        idCardCopyCompleteTimeout.running = true;
    }
}
