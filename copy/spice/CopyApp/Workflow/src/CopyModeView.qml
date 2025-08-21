import QtQuick 2.15
import QtQml 2.15
import QtQuick.Layouts 1.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import QtQml.Models 2.15


SettingsTextImageBranchViewModel
{
    id : root
    objectName: "copyModeSettingsTextImage"
    property string node
    property var pushMenuItem : null
    property var resourceModel : null
    property string menuDynamicUrl: ""
    property var menuResourceInstance : _menuResource
    property var menuNode

    property var map_: new Map()
    property var copyConfigModel: null

    controlModel : TextImageBranchModel
    {
        infoText : SpiceLocObject{ stringId: "StringIds.cSelectCopyMode" }
        onClicked:{
            root.pushMenuItem("qrc:/menu/MenuList.qml", {node: menuNode.id, title: menuNode.titleId, "menuResourceInstance": resourceInstance, "menuDynamicUrl" : menuDynamicUrl})
        }
    }

    function updateData(){
        map_.set(Copy_1_Configuration_CopyMode.CopyMode.printAfterScanning, _qmlUtils.createSpiceLoc(root ,{"stringId": "StringIds.cCopySendManually"}).text);
        map_.set(Copy_1_Configuration_CopyMode.CopyMode.printWhileScanning, _qmlUtils.createSpiceLoc(root ,{"stringId": "StringIds.cCopySendAutomatically"}).text);
    }

    function getSecondaryText()
    {
        if(root.copyConfigModel && root.copyConfigModel.data.copyMode)
        {
            let copyModeAction = root.copyConfigModel.data.copyMode;
            if(map_.has(copyModeAction))
            {
                controlModel.secondInfoText.text = map_.get(copyModeAction);
            }
        }
        else
        {
            // Assume its default.
            controlModel.secondInfoText.text = map_.get(Copy_1_Configuration_CopyMode.CopyMode.printAfterScanning);
        }
    }

    function onCopyConfigModelSubscribed(future)
    {
        root.copyConfigModel = future.get();
        root.copyConfigModel.data.copyModeChanged.connect(getSecondaryText);
    }

    Component.onCompleted:
    {
        updateData();

        let response = _resourceStore.get("/cdm/copy/v1/configuration");

        response.resolved.connect((future) => 
        {
            console.log("GET copy/v1/configuration resolved: " + future.data)
            let copyConfig = future.get();
            let copyModeAction = copyConfig.data.copyMode;

            if(map_.has(copyModeAction))
            {
                controlModel.secondInfoText.text = map_.get(copyModeAction);
            }
        })

        response.rejected.connect((future) => {
            console.log("copy/v1/configuration rejected error: " + future.error)
        })

        let eventFuture_sub = _resourceStore.subscribe("/cdm/copy/v1/configuration");

        eventFuture_sub.resolved.connect(onCopyConfigModelSubscribed);

        eventFuture_sub.rejected.connect((future) => {
            console.log("eventFuture_sub future.rejected.connect: " + future.error)
        })
    }

    Component.onDestruction:
    {
        _resourceStore.unsubscribe(root.copyConfigModel);
    }
}