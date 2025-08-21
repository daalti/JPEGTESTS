import QtQuick 2.15
import QtQml 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import QtQml.Models 2.15
import quickCopyFooter 1.0

SpiceView{
    width : parent.width
    height : parent.width
    anchors.centerIn: parent
    
    sourceComponent: QuickCopyFooter{
        id : quickCopyFooter
    }
}