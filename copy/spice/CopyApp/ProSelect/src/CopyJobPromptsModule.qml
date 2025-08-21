import QtQuick 2.15
import spiceGuiCore 1.0
import "qrc:/StateDecorator/StateDecorator.js" as StateDecorator
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0

QtObject {

    id: root

    function stateActivated(state, context)
    {
        let decoration;
        let view;
        let detailMessage = _qmlUtils.createCollection(root);

        switch(Number(state.category)){
        case Alert_1_Category.Category.scanManualDuplexSecondSide:
        case Alert_1_Category.Category.scanManualDuplexSecondPage:
            decoration = [
                        {
                            "name": "Response_01",
                            "args": {
                                "textObject.stringId": "StringIds.cContinue",
                                "type": SpiceButton.Type.Primary,
                                "onActivated":  () => {
                                    responseContinue(state)
                                }
                            }
                        },
                        {
                            "name": "Response_02",
                            "args": {
                                "objectName": "CopyCancelButton",
                                "textObject.stringId": "StringIds.cCancel",
                                "onActivated":  () => {
                                    responseCancel(state)
                                }
                            }
                        },
                        {
                            "name": "NoResponse",
                            "args": {
                                "textObject.stringId": "StringIds.cCancel",
                                "visible": false,
                                "onActivated":  () => {
                                    responseCancel(state)
                                }
                            }
                        }
                    ]
            break;

        default:
            console.error("CopyJobPromptsModule category not handled: " + state.category)
        }

        let actions = StateDecorator.createActionsCollection(state,decoration)

        switch(Number(state.category)){
        case Alert_1_Category.Category.scanManualDuplexSecondSide:
            detailMessage.append(_qmlUtils.createSpiceLoc( root ,{"stringId": "StringIds.cFlipIDCard" }));
            view = StateDecorator.pushView(
                        state,
                        "qrc:/layouts/MessageLayout.qml",
                        [
                            {
                                "objectName": state.category,
                                "messageType": MessageLayout.MessageType.DIALOG,
                                "messageDialogType": MessageLayout.MessageDialogType.INFO,
                                "titleText": _qmlUtils.createSpiceLoc( root ,{"stringId": "StringIds.cIDCardCopyApp" }),
                                "detailTexts": detailMessage,
                                "actions": actions
                            }
                        ]
                        )
            break;
            case Alert_1_Category.Category.collationNotHonoured:
            decoration = []
            detailMessage.append(_qmlUtils.createSpiceLoc( root ,{"stringId": "StringIds.cPrintingCollatedPages"}));
            view = StateDecorator.pushView(
                        state,
                        "qrc:/layouts/MessageLayout.qml",
                        [
                            {
                                "objectName": state.category,
                                "messageDialogType": MessageLayout.MessageDialogType.WARNING,
                                "titleText": _qmlUtils.createSpiceLoc( root ,{"stringId": "StringIds.cCollateProblem"}),
                                "detailTexts": detailMessage,
                                "actions": actions,
                                "messageType":MessageLayout.MessageType.DIALOG

                            }
                        ]
                        )
            break;
        case Alert_1_Category.Category.scanManualDuplexSecondPage:
            detailMessage.append(_qmlUtils.createSpiceLoc( root ,{"stringId": "StringIds.cPlaceSecondPage" }));
            view = StateDecorator.pushView(
                        state,
                        "qrc:/layouts/MessageLayout.qml",
                        [
                            {
                                "objectName": state.category,
                                "messageType": MessageLayout.MessageType.DIALOG,
                                "messageDialogType": MessageLayout.MessageDialogType.INFO,
                                "titleText": _qmlUtils.createSpiceLoc( root ,{"stringId": "StringIds.c2SidedCopying" }),
                                "detailTexts": detailMessage,
                                "actions": actions
                            }
                        ]
                        )
            break;

        default:
            console.error("CopyJobPromptsModule category not handled: " + state.category)
        }
    }

    function responseContinue(state) {
        let jobAlertsActionData = _resourceStore.createInstance(ResourceStoreTypes.JOB_MANAGEMENT_1_JOB_MANAGEMENT_ALERTS_ACTION_DATA)
        jobAlertsActionData.data.jobAction = JobManagement_1_JobManagementAlertsAction.JobManagementAlertsAction.Response_01
        StateDecorator.postAlertActionResponse(state, jobAlertsActionData)
    }

    function responseCancel(state) {
        let jobAlertsActionData = _resourceStore.createInstance(ResourceStoreTypes.JOB_MANAGEMENT_1_JOB_MANAGEMENT_ALERTS_ACTION_DATA)
        jobAlertsActionData.data.jobAction = JobManagement_1_JobManagementAlertsAction.JobManagementAlertsAction.Response_02
        StateDecorator.postAlertActionResponse(state, jobAlertsActionData)
    }

    function stateDeactivated(state, context)
    {
    }
}
