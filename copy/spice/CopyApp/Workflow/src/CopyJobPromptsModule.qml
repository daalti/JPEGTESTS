import QtQuick 2.15
import spiceGuiCore 1.0
import QtQuick.Layouts 1.15
import QtQml.Models 2.15
import "qrc:/StateDecorator/StateDecorator.js" as StateDecorator
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0

QtObject {

    id: root


    function decorateAlert(state, alert)
    {
        let decoration;
        let collection ;
        switch(Number(state.category)){
        case Alert_1_Category.Category.scanManualDuplexSecondSide:
            alert.detailsIcon = _qmlUtils.createCollection(alert)
            alert.detailsIcon.append(_qmlUtils.createImageModel("qrc:/images/Graphics/IDCardCopyBackGraph.json" , alert))
            collection = _qmlUtils.createCollection(alert)
            collection.insert(0, _qmlUtils.createSpiceLoc( alert ,{"stringId": _propertyMap.cStringIDForEnum("CopyJobPrompts","cFlipIDCardDone")}))
            alert.messagesDetails = collection
            alert.message = _qmlUtils.createSpiceLoc( alert ,{"stringId": _propertyMap.cStringIDForEnum("CopyJobPrompts","cIDCardBack")})
            alert.icon = "qrc:/images/Status/Informative.json"
            decoration = [
                        {
                            "name": "Response_01",
                            "args": {
                                "textObject.stringId": "StringIds.cDoneButton",
                                "buttonType": SpiceButton.Type.PrimaryFlow,
                                "variation": SpiceButton.ButtonVariation.VariationOne,
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
                                "buttonType": SpiceButton.Type.Secondary,
                                "variation": SpiceButton.ButtonVariation.VariationOne,
                                "onActivated":  () => {
                                    responseCancel(state)
                                }
                            }
                        },
                        {
                            "name": "Response_03",
                            "args": {
                                "textObject.stringId": "StringIds.cCancel",
                                "visible": false,
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

        case Alert_1_Category.Category.scanManualDuplexSecondPage:
            alert.detailsIcon = _qmlUtils.createCollection(alert)
            alert.detailsIcon.append(_qmlUtils.createImageModel("qrc:/images/Glyph/2SidedCopy.json" , alert))
            collection = _qmlUtils.createCollection(alert)
            collection.insert(0, _qmlUtils.createSpiceLoc( alert ,{"stringId": "StringIds.cPlaceScannerContinue" }))
            alert.messagesDetails = collection
            alert.message = _qmlUtils.createSpiceLoc( alert ,{"stringId": "StringIds.c2SidedCopy" })
            decoration = [
                        {
                            "name": "Response_01",
                            "args": {
                                "textObject.stringId": "StringIds.cContinue",
                                "buttonType": SpiceButton.Type.PrimaryFlow,
                                "variation": SpiceButton.ButtonVariation.VariationOne,
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
                                "buttonType": SpiceButton.Type.Secondary,
                                "variation": SpiceButton.ButtonVariation.VariationOne,
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
        case Alert_1_Category.Category.morePagesDetectedForCollate:
            collection = _qmlUtils.createCollection(alert)
            //Need to combine 2 strings for description
            collection.insert(0, _qmlUtils.createSpiceLoc( alert ,{"stringId": "StringIds.cPagesDetectedFeeder" }))
            collection.append(_qmlUtils.createSpiceLoc( alert ,{"stringId": "StringIds.cCollatePages" }))
            collection.append(_qmlUtils.createSpiceLoc( alert ,{"stringId": "StringIds.cUnsupportedSizePromptCancel" }))
            alert.messagesDetails = collection
            alert.message = _qmlUtils.createSpiceLoc( alert ,{"stringId": "StringIds.cPagesDetected" })
            decoration = [
                        {
                            "name": "Response_01",
                            "args": {
                                "objectName": "CopyContinueButton",
                                "textObject.stringId": "StringIds.cContinue",
                                "buttonType": SpiceButton.Type.PrimaryFlow,
                                "variation": SpiceButton.ButtonVariation.VariationOne,
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
                                "buttonType": SpiceButton.Type.Secondary,
                                "variation": SpiceButton.ButtonVariation.VariationOne,
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
         case Alert_1_Category.Category.mdfEjectPage:
            collection = _qmlUtils.createCollection(alert)
            collection.insert(0, _qmlUtils.createSpiceLoc( alert ,{"stringId": _propertyMap.valueMap("copyPrompt").asMap()["releasePage"] }))
            alert.messagesDetails = collection
            decoration = [
                       {
                            "name": "NoResponse",
                            "args": {
                                "objectName": "CopyReleasePagebtn",
                                "textObject.stringId": _propertyMap.valueMap("paperEject").asMap()["eject"],
                                "buttonType": SpiceButton.Type.PrimaryFlow,
                                "onActivated":  () => {
                                    noResponse(state)
                                }
                            }
                        }
                    ]
            break;
        default:
            console.error("CopyJobPromptsModule category not handled: " + state.category)
        }

        alert.actions = StateDecorator.createActionsCollection(state,decoration)

    }
    function stateActivated(state, context)
    {       
        let view;
        switch(Number(state.category)){

        case Alert_1_Category.Category.scanManualDuplexSecondSide:
            view = StateDecorator.pushView(
                        state,
                        "qrc:/templates/models/AlertModel.qml",
                        [
                            {
                                "objectName": state.category,
                                "alertViewModel": context.alert,
                                "closeIconSupported": false,
                                "modalType": AlertModel.ModalType.LAYOUT1,
                                "modalSizeRequired" : AlertModel.ModalSize.BIG,
                                "alertSeverity":Alert_1_Alert_Severity.Severity.information
                            }
                        ]
                        )
            break;

        case Alert_1_Category.Category.scanManualDuplexSecondPage:
            view = StateDecorator.pushView(
                        state,
                        "qrc:/templates/models/AlertModel.qml",
                        [
                            {
                                "objectName": state.category,
                                "alertViewModel": context.alert,
                                "closeIconSupported": false,
                                "modalType": AlertModel.ModalType.LAYOUT1,
                                "alertSeverity":Alert_1_Alert_Severity.Severity.information
                            }
                        ]
                        )
            break;
        case Alert_1_Category.Category.morePagesDetectedForCollate:
            view = StateDecorator.pushView(
                        state,
                        "qrc:/templates/models/AlertModel.qml",
                        [
                            {
                                "objectName": state.category,
                                "alertViewModel": context.alert,
                                "closeIconSupported": false,
                                "modalType": AlertModel.ModalType.LAYOUT1,
                                "alertSeverity":Alert_1_Alert_Severity.Severity.warning
                            }
                        ]
                        )
            break;
       case Alert_1_Category.Category.mdfEjectPage:
                        view = StateDecorator.pushView(
                        state,
                        "qrc:/templates/models/AlertModel.qml",
                        [
                            {
                               "objectName": state.category,
                                "alertViewModel": context.alert,
                                "closeIconSupported": false,
                                "modalType": AlertModel.ModalType.LAYOUT1,
                                "alertSeverity":Alert_1_Alert_Severity.Severity.information
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
    function noResponse(state) {
       let jobAlertsActionData = _resourceStore.createInstance(ResourceStoreTypes.JOB_MANAGEMENT_1_JOB_MANAGEMENT_ALERTS_ACTION_DATA)
        jobAlertsActionData.data.jobAction = JobManagement_1_JobManagementAlertsAction.JobManagementAlertsAction.NoResponse
        StateDecorator.postAlertActionResponse(state, jobAlertsActionData)
    }
    function stateDeactivated(state, context)
    {
    }
}
