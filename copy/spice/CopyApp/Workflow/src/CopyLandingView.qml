import QtQuick 2.15
import QtQuick.Layouts 1.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxMenu 1.0
import QtQml.Models 2.15
import QtQuick.Controls 2.15


SpiceAppLandingLayout {
    objectName: "copyLandingView"
    id: root
    
    signal copyButtonClicked;
    signal moreSettingsButtonClicked;
    signal startButtonClicked;
    signal doneButtonClicked;
    signal previewButtonClicked;
    signal ejectButtonClicked;
    signal cancelButtonClicked;
    signal stopScanButtonClicked;
    signal saveQuicksetButtonClicked;
    signal refreshPreviewButtonClicked;
    signal discardPageButtonClicked(int pageNumber, string discardPageIdString )
    signal previewReady();


    //Only one action button in only one, it could be "COPY","START","DONE", "NONE"(none hiddes it)
    //Pending future improvements: use enums, constraints or models
    property string mainActionButtonType: "NONE";   //Rules strings and signals
    property bool isVisiblePrePreviewTextAndImage: true;
    property string jobTicketUrl: "";
    property QQmlObjectListModel prePreviewMessageForMdf: QQmlObjectListModel{}

    property bool isMainActionButtonEnabled: false;
    property var actionButtonConstraintMessageId:"StringIds.cUnknown";
    property var mainActionButtonStringIdForPrePreview:"StringIds.cUnknown";
    
    onIsMainActionButtonEnabledChanged: {
        console.log("Status of main action button", root.isMainActionButtonEnabled)
    }

    // Interactive Summary properties
    property ISpiceModel menuResourceModel: null
    property string previewJobId: "";
    property var summaryList: null;
    property var copyResourceInstance: null;

    property bool isDetailPanelVisible: true
    property bool isPreviewPanelVisible: true
    property bool secondaryPanelVisible: isDetailPanelVisible && isPreviewPanelVisible
    secondaryCollapsed: !secondaryPanelVisible 
    secondaryPanel: secondaryPanelVisible ? (templatePriority === SpiceAppLandingLayout.TemplatePriority.DetailPanelTemplate ? (Global.breakpoint > Global.BreakPoint.S ?subLevel2: subLevel1 ) : Global.breakpoint > Global.BreakPoint.S ? subLevel1: subLevel2):null
    templatePriority:  secondaryPanelVisible ? SpiceAppLandingLayout.TemplatePriority.DetailPanelTemplate : Global.breakpoint < Global.BreakPoint.M && isPreviewPanelVisible ? SpiceAppLandingLayout.TemplatePriority.PreviewTemplate : SpiceAppLandingLayout.TemplatePriority.DetailPanelTemplate

    //Properties that defines states of buttons
    property bool isEditSettingsActionEnabled: false;
    property bool isEjectButtonVisible: false;
    property bool isCancelButtonVisible: false;
    property bool isStopScanButtonEnabled: false
    property bool isActionButtonConstrained: false;
    property bool isQuickSetSaveButtonVisible : false;
    property bool isPageAdded: false
    property bool isMultiPagePreviewSupported: false
    property bool isAJobInProgress: false
    property bool saveButtonIsVisibleBeforePreview: false
    property bool showCancelButtonAfterClickingCopy: false
    property bool isImageEditingSupported: false
    property bool isDiscardPagesSupported: false

    // PreviewComponentHandler to handle the preview Components
    property QtObject previewComponentHandler: null
    // Check that all previews are received and state machine is waiting for previews (scanner acquisition has finished, idle)
    property bool isScannerIdleAndPreviewsReceived: previewComponentHandler && !previewComponentHandler.imageAdded && previewComponentHandler.imageLoaded && _stateMachine.areWaitingForPreviews;
    onIsScannerIdleAndPreviewsReceivedChanged: {
        console.debug("onIsScannerIdleAndPreviewsReceivedChanged state: " + root.isScannerIdleAndPreviewsReceived)
        if(root.isScannerIdleAndPreviewsReceived){
            root.previewReady();
        }
    }

    property bool smallVersion: Global.breakpoint <= Global.BreakPoint.S
    property real spiceHeaderViewConstantHeight: SpiceHeaderViewConstants.height
    property real spiceFooterViewConstantHeight: SpiceFooterViewConstants.height
    property int previewConfiguration: 0
    property int inputMediaSourceSelected: 0

    function isMainActionTypeButtonValid( mainButtonType )
    {
        return mainButtonType === "COPY" || 
               mainButtonType === "START" ||
               mainButtonType === "SEND" ||
               mainButtonType === "DONE" ||
               mainButtonType === "PREVIEW" ||
               mainButtonType === "NONE";
    }

    function isMainActionButtonVisible( mainButtonType )
    {
        let isVisible = false;

        if(isMainActionTypeButtonValid(mainButtonType))
        {
            isVisible = ( mainButtonType !== "NONE" );
        }
        else
        {
            isVisible = false;

            console.warn("isMainActionButtonVisible type not valid: " + mainButtonType);
        }

        return isVisible;
    }

    function getMainButtonType( mainButtonType )
    {
        let type = SpiceButton.Type.Secondary;

        if( mainButtonType === "DONE" )
        {
            type = SpiceButton.Type.PrimaryFlow;
        }
        else
        {
            type = SpiceButton.Type.Primary;
        }

        return type;
    }

    function getMainButtonIcon( mainButtonType )
    {
        let icon = "";

        if( mainButtonType === "DONE" )
        {
            icon = "";
        }
        else
        {
            icon = "qrc:/images/Glyph/InstantLaunch.json";
        }

        return icon;
    }

    //It returns cUnknown if button type not valid
    function getStringIdAccordingMainButtonType( mainButtonType)
    {
        let stringId = "StringIds.cUnknown";

        if( isMainActionTypeButtonValid( mainButtonType ) )
        {
            if( mainButtonType === "COPY" )
            {
                stringId = "StringIds.cCopy";
            }
            else if( mainButtonType === "START" )
            {
                stringId = "StringIds.cStart";
            }
            else if( mainButtonType === "PREVIEW")
            {
                stringId = "StringIds.cPreviewLabel";
            }
            else if( mainButtonType === "DONE" )
            {
                stringId = "StringIds.cDoneButton";
            }
        }

        return stringId;
    }

    //It returns false if type is not valid
    function emitMainActionButtonClicked( mainButtonType )
    {
        if( isMainActionTypeButtonValid( mainButtonType ) )
        {
            if( mainButtonType === "COPY" )
            {
                root.copyButtonClicked();
                console.log("emitted mainActionButtonClicked");
            }
            else if( mainButtonType === "START" )
            {
                root.startButtonClicked();
                console.log("emitted startButtonClicked");
            }
            else if( mainButtonType === "PREVIEW")
            {
                root.previewButtonClicked();
            }
            else if( mainButtonType === "DONE" )
            {
                root.doneButtonClicked();
                console.log("emitted doneButtonClicked");
            }
        }
        else
        {
            console.warn("emitMainActionButtonClicked, Button type not controlled: " + mainButtonType );
            isEmitted = false;
        }

        return false;
    }

    function isDiscardPageButtonActive()
    {
        return previewComponentHandler && previewComponentHandler.imageLoaded && root.isDiscardPagesSupported && 
            // If Job is not completed or cancelled
            !(_stateMachine.currentJobState == JobManagement_1_State.State.completed || 
            _stateMachine.currentJobState == JobManagement_1_State.State.cancelProcessing) &&
            // If copy configuration is available we also check that copy mode is compatible with edition.
            ( _stateMachine.copyConfiguration == null || _stateMachine.copyConfiguration.data.copyMode != Copy_1_Configuration_CopyMode.CopyMode.printWhileScanning );
    }
    
    function isEditButtonActive()
    {
        return previewComponentHandler && previewComponentHandler.imageLoaded && root.isImageEditingSupported && 
            // If Job is not completed or cancelled
            !(_stateMachine.currentJobState == JobManagement_1_State.State.completed || 
            _stateMachine.currentJobState == JobManagement_1_State.State.cancelProcessing) &&
            // If copy configuration is available we also check that copy mode is compatible with edition.
            ( _stateMachine.copyConfiguration == null || _stateMachine.copyConfiguration.data.copyMode != Copy_1_Configuration_CopyMode.CopyMode.printWhileScanning );
    }

    function isCopyModeButtonVisible()
    {
        return _stateMachine.isPageSensorflow() && !_stateMachine.inPreviewState && !(_stateMachine.isOneTouchQuickSet ||
        ( _stateMachine.isLaunchedFromWidget && !_stateMachine.isLaunchedFromWidgetOptions));
    }

    headerMain: SpiceHeaderVar2 {
        id: copyHeaderMain
        customText: SpiceLocObject { stringId: "StringIds.cCopyAppHeading" }
    }

    headerDetail: SpiceHeaderVar2 {
        customText: SpiceLocObject { stringId: "StringIds.cCopyAppHeading" }
    }

    //Pre-preview Layout
    mainComponent: previewComponentHandler ? previewComponentHandler.previewComponent : null

    detailComponentModel: MenuInteractiveSummaryList {
            node: "copyInteractiveSummary"
            interctiveSummaryList : root.summaryList
            resourceModel : root.menuResourceModel
            resourceInstance: root.copyResourceInstance
    }

    footerMain: SpiceFooter {
        leftBlockModel: ObjectModel {

            SpiceButton {
                id: refreshPanelButton
                objectName: "refreshPanelButton"
                visible: active
                active: root.previewComponentHandler ?  (root.previewJobId != "") && !root.isMultiPagePreviewSupported : false
                textObject.stringId: root.smallVersion ? "" : "StringIds.cRefresh"
                enabled: root.previewComponentHandler ? root.previewComponentHandler.imageLoaded && root.isMainActionButtonEnabled: false
                icon: "qrc:/images/Glyph/+lang_ar/Refresh.json"
                Layout.alignment: Qt.AlignLeft
                flat:true
                type: SpiceButton.Type.Secondary
                variation: SpiceButton.ButtonVariation.VariationOne
                
                onClicked: {
                    if(!root.previewComponentHandler.refreshPreviewJobInProgress){
                        previewComponentHandler.refreshPreviewButtonClicked()
                        if(root.isQuickSetSaveButtonVisible){
                            root.saveButtonIsVisibleBeforePreview = true
                            root.refreshPreviewButtonClicked()
                        }                 
                        root.previewButtonClicked();
                    }
                }
            } 

            SpiceButton {
                id: ejectButton
                objectName: "ejectMainPanelButton"

                Layout.alignment: Qt.AlignLeft

                type: SpiceButton.Type.Secondary
                variation: SpiceButton.ButtonVariation.VariationOne
                icon: "qrc:/images/Glyph/EjectPaper.json"
                active: root.isEjectButtonVisible
                visible: active
                flat: true

                onClicked: {

                    console.log("eject Button  - Clicked");
                    root.ejectButtonClicked();
                }
            }

            SpiceButton {
                id: copyModeButton
                objectName: "copyModeMainPanelButton"

                Layout.alignment: Qt.AlignLeft

                active: isCopyModeButtonVisible()
                flat: true
                icon: "qrc:/images/Glyph/CopyMode.json"
                textObject: SpiceLocObject { stringId: "StringIds.cSelectCopyMode" }
                type: SpiceButton.Type.Secondary
                variation: SpiceButton.ButtonVariation.VariationOne
                visible: active

                onClicked: {
                    console.log("CopyMode Button  - Clicked");
                    _stack.pushModal("qrc:/CopyApp/CopyModeActionsModal.qml")
                }
            }

            SpiceButton{
                id: switchPreviewLayoutButton
                objectName: "switchPreviewLayoutButton"
                icon: root.previewComponentHandler && root.previewComponentHandler.switchPreviewLayout ? "qrc:/images/Glyph/ThumbnailView.json" : "qrc:/images/Glyph/FitPage.json"
                textObject.stringId: (Global.breakpoint >= Global.BreakPoint.M) ? "StringIds.cView" :  ""
                flat: true
                type: SpiceButton.Type.Secondary
                visible: active
                active: (Global.breakpoint>=Global.BreakPoint.M) && (root.isAJobInProgress || _stateMachine.previewComponentControl) && _enableGridPreview
                onClicked: {
                    root.previewComponentHandler.switchPreviewLayout = !root.previewComponentHandler.switchPreviewLayout;
                }            
            }

            SpiceButton{
                id:editButton
                objectName:"editButton"
                icon: (Global.breakpoint === Global.BreakPoint.XS) ? "qrc:/images/Glyph/Edit.json" : ""
                textObject.stringId: (Global.breakpoint === Global.BreakPoint.XS) ? "" :  "StringIds.cEdit"
                active: isEditButtonActive()
                type: SpiceButton.Type.Secondary
                flat:true
                onClicked: {
                    previewComponentHandler.editButtonClicked()
                }
            }

            SpiceButton{
                id:discardPageCopyButton
                objectName:"discardPageCopyButton"
                textObject.stringId: (Global.breakpoint === Global.BreakPoint.XS) ? "" :  "StringIds.cDiscard"
                active: isDiscardPageButtonActive()
                type: SpiceButton.Type.Secondary
                flat:true


                onClicked: {
                    let pageNumber = previewComponentHandler.focusImage + 1; //First page is page #0
                    let pageModel = previewComponentHandler.getFocusedPageModel();
                    let discardPageIdString = pageModel.pageId ;
                    
                    root.discardPageButtonClicked(pageNumber, discardPageIdString )
                }
            }
        }

        rightBlockModel: ObjectModel {
            SpiceButton {
                Layout.alignment: Qt.AlignRight

                textObject.stringId: (Global.breakpoint === Global.BreakPoint.XS) ? "" : getStringIdAccordingMainButtonType( root.mainActionButtonType )
                type: getMainButtonType( root.mainActionButtonType )
                objectName: "mainActionButtonOfMainPanel"
                variation: SpiceButton.ButtonVariation.VariationOne

                constrained: (_stateMachine.isPageSensorflow() && root.isAJobInProgress) ? root.isActionButtonConstrained || !previewComponentHandler.imageLoaded
                    : root.isActionButtonConstrained
                constrainedMessage:SpiceLocObject{stringId:actionButtonConstraintMessageId}

                enabled: root.isMainActionButtonEnabled;
                visible: active
                active: (root.smallVersion || root.isSecondaryCollapsed) && isMainActionButtonVisible( root.mainActionButtonType )

                icon: getMainButtonIcon( root.mainActionButtonType )

                onClicked: {
                    root.showCancelButtonAfterClickingCopy = true
                    root.emitMainActionButtonClicked( root.mainActionButtonType );
                }
            }

            SpiceButton {
                id: cancelJobButton
                objectName: "cancelButtonPreviewPanel"
                visible: active
                active: root.previewComponentHandler ? (root.smallVersion || root.isSecondaryCollapsed) && root.isCancelButtonVisible && (!root.previewComponentHandler.imageLoaded || root.showCancelButtonAfterClickingCopy) : (root.smallVersion || root.isSecondaryCollapsed) && root.isCancelButtonVisible
                textObject.stringId: (Global.breakpoint === Global.BreakPoint.XS) ? "" : "StringIds.cCancel"
                Layout.alignment: Qt.AlignRight
                type: SpiceButton.Type.Destructive
                icon: Global.breakpoint == Global.BreakPoint.XS ? "qrc:/images/Glyph/Cancel.json" : ""
                variation: SpiceButton.ButtonVariation.VariationOne
                
                onClicked: {
                    console.log("Copy Cancel job  - Clicked");
                    root.cancelButtonClicked();
                    root.showCancelButtonAfterClickingCopy = false
                }
            }

            SpiceButton{
                id: stopScanButton
                objectName: "stopScanButtonPreviewPanel"
                visible: active
                active: (root.smallVersion || root.isSecondaryCollapsed) && root.isStopScanButtonEnabled

                icon: Global.breakpoint == Global.BreakPoint.XS ? "qrc:/images/Glyph/Cancel.json" : ""
                textObject.stringId: (Global.breakpoint === Global.BreakPoint.XS) ? "" : "StringIds.cStopScan"
                type: SpiceButton.Type.Destructive
                variation: SpiceButton.ButtonVariation.VariationOne
                Layout.alignment: Qt.AlignRight
                onClicked: {

                   console.log("stop scan Clicked")
                   root.stopScanButtonClicked();
                }
            }
        }
    }


    footerDetail: SpiceFooter {
        rightBlockModel: ObjectModel {

            SpiceButton {
                Layout.alignment: Qt.AlignRight

                textObject.stringId: (Global.breakpoint === Global.BreakPoint.XS) ? "" : getStringIdAccordingMainButtonType( root.mainActionButtonType )

                type: getMainButtonType( root.mainActionButtonType )
                objectName: "mainActionButtonOfDetailPanel"
                variation: SpiceButton.ButtonVariation.VariationOne

                constrained: (_stateMachine.isPageSensorflow() && root.isAJobInProgress) ? root.isActionButtonConstrained || !previewComponentHandler.imageLoaded
                    : root.isActionButtonConstrained
                constrainedMessage:SpiceLocObject{stringId:actionButtonConstraintMessageId}
                
                enabled: root.isMainActionButtonEnabled
                visible: active
                active: isMainActionButtonVisible( root.mainActionButtonType )

                icon: getMainButtonIcon( root.mainActionButtonType )

                onClicked: {
                    root.showCancelButtonAfterClickingCopy = true
                    root.emitMainActionButtonClicked( root.mainActionButtonType );
                    if(root.mainActionButtonType == "DONE")
                    {
                        root.previewComponentHandler.doneButtonClicked()
                    }
                }
            }

            SpiceButton {
                id: cancelJobButton
                objectName: "cancelButton"
                visible: active
                active: root.previewComponentHandler ? root.isCancelButtonVisible && (!root.previewComponentHandler.imageLoaded || root.showCancelButtonAfterClickingCopy): root.isCancelButtonVisible
                textObject.stringId: (Global.breakpoint === Global.BreakPoint.XS) ? "" :  "StringIds.cCancel"
                Layout.alignment: Qt.AlignRight
                type: SpiceButton.Type.Destructive
                variation: SpiceButton.ButtonVariation.VariationOne
                icon: Global.breakpoint == Global.BreakPoint.XS ? "qrc:/images/Glyph/Cancel.json" : ""
                
                onClicked: {
                    console.log("Copy Cancel job  - Clicked");
                    root.cancelButtonClicked();
                    root.showCancelButtonAfterClickingCopy = false
                }
            }

            SpiceButton{
                id: stopScanButton
                objectName: "stopScanButtonDetailRightBlock"
                visible: active
                active: root.isStopScanButtonEnabled
                icon: Global.breakpoint == Global.BreakPoint.XS ? "qrc:/images/Glyph/Cancel.json" : ""
                textObject.stringId: (Global.breakpoint === Global.BreakPoint.XS) ? "" :  "StringIds.cStopScan"
                type: SpiceButton.Type.Destructive
                variation: SpiceButton.ButtonVariation.VariationOne
                Layout.alignment: Qt.AlignRight
                onClicked: {

                    console.log("stop scan Clicked")
                    root.stopScanButtonClicked();
                }
            }

            SpiceButton {
                id: optionsDetailPanelButton
                objectName: "optionsDetailPanelButton"

                enabled: root.isEditSettingsActionEnabled

                icon: "qrc:/images/Glyph/PrintMode.json"
                Layout.alignment: Qt.AlignRight
                type: SpiceButton.Type.Secondary
                variation: SpiceButton.ButtonVariation.VariationOne
                flat: true
                
                onClicked: {

                    console.log("Copy OPTIONS  - Clicked");
                    root.moreSettingsButtonClicked();
                }
            }            

        }
        leftBlockModel: ObjectModel { 
            SpiceButton {
                id: ejectButton
                objectName: "ejectDetailPanelButton"
                Layout.alignment: Qt.AlignLeft
                type: SpiceButton.Type.Secondary
                variation: SpiceButton.ButtonVariation.VariationOne
                icon: "qrc:/images/Glyph/EjectPaper.json"
                active: root.smallVersion && root.isEjectButtonVisible 
                visible: active
                flat: true

                onClicked: {
                    console.log("eject Button  - Clicked");
                    root.ejectButtonClicked();
                }
            }
            SpiceButton {
                    id: savePanelButton
                    objectName: "savePanelButton"
                    visible: active
                    active: (root.isQuickSetSaveButtonVisible || root.saveButtonIsVisibleBeforePreview)
                    icon: "qrc:/images/Glyph/Save.json"
                    Layout.alignment: Qt.AlignLeft
                    flat:true
                    type: SpiceButton.Type.Secondary
                    variation: SpiceButton.ButtonVariation.VariationOne
                    permissionId: _stateMachine.isCopyPermissionsConfigurable
                        ? "2aafb08e-faf8-42cf-8623-fafc36209105"  // Permission ID for enterprise
                        : "10673dd6-60f9-4b82-badb-3a28d15b4d42"  // Existing permission ID for non enterprise
                    onClicked: {                    
                        root.saveQuicksetButtonClicked();
                        root.saveButtonIsVisibleBeforePreview = false 
                    }
                }
        }  
    }

    Component.onCompleted: {
        if(_scanPreviewSupported){
            root.previewComponentHandler = Qt.createQmlObject('import QtQuick 2.15; import preview 1.0; import spiceGuiCore 1.0;
                PreviewComponentHandler{
                    // PrePreview StringId Configuration
                    prePreviewConfigurable: _stateMachine.isPrePreviewConfigurable
                    // LongplotScan Usecase
                    longPlotScan: false
                    // is screen is small size
                    previewComponentheight: root.smallVersion ? root.staticAvailableheight - root.spiceHeaderViewConstantHeight - root.spiceFooterViewConstantHeight : root.staticAvailableheight - root.spiceFooterViewConstantHeight

                    // PrePreview Componeont , PreviewMultipage
                    setPreviewComponent: root.isAJobInProgress || _stateMachine.previewComponentControl

                    //stringId 
                    actionButtonStringId: root.mainActionButtonStringIdForPrePreview

                    // multipage previe single Preview
                    isMultiPagePreviewSupported: root.isMultiPagePreviewSupported

                    // In multipage Add Page
                    isSecondaryCollapsed: root.isSecondaryCollapsed

                    // Adding Page Laogic
                    previewJobId: root.previewJobId

                    jobTicketUrl: root.jobTicketUrl

                    isVisiblePrePreviewTextAndImage: root.isVisiblePrePreviewTextAndImage;

                    //refresh Preview Warning Icon
                    refreshPreviewWarningIcon: root.isMultiPagePreviewSupported ? false : root.isQuickSetSaveButtonVisible
                    isImageEditingSupported: root.isImageEditingSupported

                    // Override back button behaviour for preview template
                    isZoomPreviewSupported: _copyPreviewInteractiveEnabled
                    inputMediaSourceSelected: root.inputMediaSourceSelected
                    //Job Type for adfLoadedStringID
                    jobType : PreviewComponentHandler.JobType.Copy
                    previewConfiguration : getEnumValueOfPreviewConfiguration()

                    previewComponentHelper.mdfPreviewAvailableMessage: prePreviewMessageForMdf
                    //Selene Preview
                    onPreviewButtonClicked: {
                        console.log("prepare processing the image")
                        root.showCancelButtonAfterClickingCopy = false
                        if(root.isQuickSetSaveButtonVisible){
                            root.saveButtonIsVisibleBeforePreview = true
                            root.refreshPreviewButtonClicked()
                        }
                        root.previewButtonClicked()
                    }

                    onAddPageClicked:{
                        console.log("add page clicked")
                        if(root.isMultiPagePreviewSupported)
                        {
                            let contentTexts = _qmlUtils.createCollection(root)
                            contentTexts.append(_qmlUtils.createSpiceLoc( root ,{ "stringId":"StringIds.cInsertPageInScannerText"}))
                            //shouldModalBeDismissed is included to disappear the constraint modal if the media is loaded at any time
                            if(_stateMachine.isPageSensorflow())
                            {
                                _stack.pushModal("qrc:/Preview/PreviewAddPagePrompt.qml",{"contentTexts":contentTexts, "headerText": _qmlUtils.createSpiceLoc( root ,{ "stringId":"StringIds.cInsertPageInScanner"}), "previewAnimation":_qmlUtils.getWorkflowResourceUrl("InsertPageScanner", "images"), "shouldModalBeDismissed": Qt.binding( function() { return _stateMachine.isScanMediaLoaded } )})
                            }
                            else
                            {
                                root.previewButtonClicked()
                            }
                        }
                    }
                    function getEnumValueOfPreviewConfiguration()
                    {
                        switch(root.previewConfiguration)
                        {
                            case JobTicket_1_ManualUserOperations_ImagePreviewConfiguration.ImagePreviewConfiguration.enable:
                                return PreviewComponentHandler.PreviewConfiguration.Enabled;
                            case JobTicket_1_ManualUserOperations_ImagePreviewConfiguration.ImagePreviewConfiguration.optional:
                                return PreviewComponentHandler.PreviewConfiguration.Optional;
                            default:
                                return PreviewComponentHandler.PreviewConfiguration.Disabled;
                        }
                    }
                }', 
                root,
                "dynamicPreviewComponent") 
        }
    }
}
