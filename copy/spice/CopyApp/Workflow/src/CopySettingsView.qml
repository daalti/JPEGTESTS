import QtQuick 2.15
import QtQuick.Layouts 1.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxMenu 1.0



SpiceModalLayout
{
    id: root
    objectName: "copySettingsView"
    modalWidth : SpiceModalLayout.SpiceModalWidthType.BIG

    property bool emitPostViewEvents: true
    content: MenuListListView{
        id: settingsMenu
        objectName: "copySettingsPage_"
        node: "copySettingsPage_"
        menuDynamicUrl: _stateMachine.controller.getSelfUrl()
        resourceModel: _stateMachine.ticketModel
        resourceInstance: _copySettingsResource
        width: root.modalPaintedWidth
        height: root.modalPaintedHeight
        forceToOnePanel : true
        inmodal : true

        onCloseButtonClicked:
        {
            //If this view doesnt execute QmlUtils.ViewEventType.Back then it pops itself
            _stack.pop();
        }        
    }

}