import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtScxml 5.8
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0

SpiceKeyboard {
    objectName: "enterQuickSetName"
    onTextSet: function(text) {
        _stateMachine.newQuickSetName = text
        _stateMachine.submitEvent("ev.saveNewQuickSet.selected")
    }
}
