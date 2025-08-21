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


SpiceModalLayout
{
    id: root
    objectName: "idCopySettingsView"
    modalWidth : SpiceModalLayout.SpiceModalWidthType.BIG
     content: MenuListListView{
        id: idCardCopySettingsPage
        objectName: "idCardCopySettingsPage"
        node: "idCardCopySettingsPage"
        menuDynamicUrl: _stateMachine.idCardCopyControllerfunctions.getSelfUrl()
        resourceInstance: _idCardCopySettingsResource
        resourceModel: _stateMachine.ticketModelForSettings
        width: root.modalPaintedWidth
        height: root.modalPaintedHeight
        forceToOnePanel : true
        inmodal : true
        
        onCloseButtonClicked:
        {
            _window.postViewEvent(QmlUtils.ViewEventType.Back)
        }         
    }
}
