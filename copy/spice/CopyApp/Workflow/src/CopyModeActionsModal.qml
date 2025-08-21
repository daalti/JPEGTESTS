import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtScxml 5.8
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxMenu 1.0

import QtQml.Models 2.15

SpiceModalLayout
{
    id: root
    modalWidth : SpiceModalLayout.SpiceModalWidthType.BIG
     content: MenuListListView{
        id: copyModeSettingsPage
        node: "copyModeSettingsPage"
        resourceInstance: _copyModeSettingsResource
        width: root.modalPaintedWidth
        height: root.modalPaintedHeight
        forceToOnePanel : true
        inmodal : true

        onCloseButtonClicked:
        {
            _stack.pop();
        }
    }
}