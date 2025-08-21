import QtQuick 2.15
import spiceuxToastSystem 1.0
import spiceuxComponents 1.0

QtObject {
    id: root

    //Add when needed a button on the toast.
    // current we need just a toast.
    property QtObject buttonModel: ButtonModel{
        objectName: "toastHideButton"
        iconPath: "qrc:/images/Glyph/ChevronUp.json"
        flat: true
        type: SpiceButton.Type.Secondary
        onClicked: {
            console.log("Toast dismissed")
            ToastSystem.toastDismissed();
        }
    }

    property QtObject toastModel: ToastModel{
        imgSource: "qrc:/images/Status/ProgressBarCircleIndeterminateStatic.json"
        objectName: "messageToastModel"
        // all job toasts shall be made busy/job progressing
        toastState: SpiceToast.SpiceToastState.BUSY
        appToStart: "JobQueueApp"
        button1: buttonModel
    }

    function showToast(stringId, timeout = 5000)
    {
        toastModel.msg = ToastSystem.createSpiceLoc({ "stringId": "StringIds.cStringEllipsis", "params": [stringId] })
        toastModel.interval = timeout
        ToastSystem.showMessageObject(toastModel)
    }

    function showToastWithoutEllipsis(stringId, timeout = 5000)
    {
        toastModel.msg = ToastSystem.createSpiceLoc({"stringId": stringId})
        toastModel.interval = timeout
        ToastSystem.showMessageObject(toastModel)
    }
}