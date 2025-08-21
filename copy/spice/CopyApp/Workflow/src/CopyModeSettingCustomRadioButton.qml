import QtQuick 2.15
import QtQml 2.15
import QtQuick.Layouts 1.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import QtQml.Models 2.15

//Custom radio button created in order to be able to update copy ticket model when modifying copy mode setting
//with that, media destination constraints will be updated (folder should not be available if direct copy is selected)

SettingsRadioButtonViewModel
{
    id : root

    property string node
    property var pushMenuItem : null
    property var resourceModel : null
    property string menuDynamicUrl: ""
    property var menuResourceInstance : _menuResource
    property var menuNode

    function updateTicket()
    {
        if(!!_stateMachine && !!_stateMachine.ticketModel)
        {
            _resourceStore.modify(_stateMachine.ticketModel)
        }
    }

    function baseCreate()
    {
        let comp = Qt.createComponent("qrc:/CopyApp/CopyModeSettingCustomRadioButtonBase.qml")
        if (comp.status !== Component.Ready) {
            console.warn(comp.errorString())
        }
        root.controlModel = comp.createObject(root, {"menuNode": root.menuNode, "pushMenuItem": root.pushMenuItem})
        root.controlModel.clicked.connect(updateTicket)
    }

    Component.onCompleted:
    {
        Qt.callLater(baseCreate)
    }    

    Component.onDestruction: 
    {
        root.controlModel.clicked.disconnect(updateTicket)
    }
}