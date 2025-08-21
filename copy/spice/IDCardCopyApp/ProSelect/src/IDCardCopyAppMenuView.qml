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

MenuList {
    id: idCardSettingsMenu
    node: "idcopySettingsPage"
    menuDynamicUrl: _stateMachine.idCardCopyControllerfunctions.getSelfUrl()
    menuResourceInstance: _idcopySettingsResource
}