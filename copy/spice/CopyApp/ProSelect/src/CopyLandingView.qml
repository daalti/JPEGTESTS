import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtScxml 5.8
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import "qrc:/QuickSetsUtils.js" as QuickSetsUtils

LandingLayout{

    id: copyLandingView
    objectName: "copyLandingView"

    titleText.stringId: "StringIds.cCopyAppHeading"

    property int numCopies: value;
    property bool copyButtonEnabled: true;
    isTumblerRequired:true
    from: 1
    to: 99
    value: _stateMachine.ticketModel && _stateMachine.ticketModel.data.dest && _stateMachine.ticketModel.data.dest.data.print ?
               _stateMachine.ticketModel.data.dest.data.print.data.copies : 0
    
    onNumCopiesChanged: {
        console.log("Number of copies (OnNumCopies) updated in UI:",numCopies, " value:", value)
        if (_stateMachine.ticketModel.data.dest.data.print.data.copies != numCopies){
            _stateMachine.ticketModel.data.dest.data.print.data.copies = numCopies;
            _stateMachine.copyControllerfunctions.updateJobTicket()
        }
    }

    onCopyButtonEnabledChanged: {
        console.log("Copy button onCopyButtonEnabledChanged " + copyButtonEnabled)
    }

    Connections {
        target: _stateMachine.ticketModel && _stateMachine.ticketModel.data.dest && _stateMachine.ticketModel.data.dest.data.print ?
                    _stateMachine.ticketModel.data.dest.data.print.data :
                    null
        function onCopiesChanged(numcopies) {
            console.log("Number of copies updated according to the ticket:",numcopies)
            value = numcopies }
    }

    Connections {
        target: _stateMachine.ticketModel
        function onDataChanged(ticketData) {
            console.log("Ticket data changed:", ticketData)
            _stateMachine.copyControllerfunctions.printTicketModel(_stateMachine.ticketModel)
        }
    }

    Connections {
        target: _stateMachine
        function onTicketModelChanged(ticketModel) {
            console.log("Ticket model changed:", ticketModel)
            _stateMachine.copyControllerfunctions.printTicketModel(_stateMachine.ticketModel)
        }
    }


    actions: QQmlObjectListModel {
        ButtonModel {
            objectName: "CopyButton"
            
            textObject.stringId: "StringIds.cCopy"
            buttonType: SpiceButton.Type.Primary

            onClicked: {
                console.log("Copy clicked");
                _stateMachine.submitEvent("ev.start.clicked")
            }

        }

        NameValueModel{
            objectName: "CopyQuickSetSelected"
            nameText: SpiceLocObject { stringId: "StringIds.cDefaultsAndQuickSets" }
            valueButton: ButtonModel{
                objectName: "QuickSetSelectedButton"
                textObject: _stateMachine.quickSetSelected

                onClicked: {
                    _stateMachine.submitEvent("ev.listQuickSets.clicked")
                }
            }
            permissionId:_stateMachine.quickSetPermissionIdSelected

        }

        ButtonModel {
            objectName: "CopyOptionsButton"
            textObject.stringId: "StringIds.cOptions"
            onClicked: {
                console.log("Options clicked")
                _stateMachine.ticketModel.data.dest.data.print.data.copies = numCopies ;
                removeSaveButtonFromLayout()
                _stateMachine.submitEvent("ev.settings.clicked")
            }
        }
    }

    Component {
        id: actionSaveModelComponent
        ButtonModel {
            buttonType:SpiceButton.Type.Secondary
            onClicked: {
                _stateMachine.submitEvent("ev.quickSetSaveOption.clicked")
            }
        }
    }

    function removeSaveButtonFromLayout(){

        for (var i=actions.count - 1; i >= 0; --i)
        {
            if (actions.get(i).objectName == "DefaultSaveButton"){
                actions.removeAt(i);
                _stateMachine.isTicketModelChanged=false
            }
        }

    }

    function addSaveButtonToLayout(){

        for (var i=actions.count - 1; i >= 0; --i)
        {
            if (actions.get(i).objectName == "CopyQuickSetSelected"){
                if(actions.get(i+1).objectName != "DefaultSaveButton"){
                    let action = actionSaveModelComponent.createObject(null,
                                                                       {
                                                                           "objectName":"DefaultSaveButton",
                                                                           "textObject.stringId":"StringIds.cSave",
                                                                       })
                    actions.insert(i+1,action)
                }
            }
        }

    }

    StackView.onActivating: {
        if(_stateMachine.isTicketIdSubscribeReady && !_stateMachine.isOneTouchQuickSet){

            _stateMachine.copyControllerfunctions.updateScannerMediaSource();
            _stateMachine.copyControllerfunctions.clearJobInfo();
            
            _stateMachine.copyControllerfunctions.subscribeForDataChange(_stateMachine.copyControllerfunctions.connectEachDataChange)
            _stateMachine.copyControllerfunctions.createJob(_stateMachine.ticketModel.data.ticketId)
        }
        console.log(_stateMachine.isOneTouchQuickSet)
            

        console.log("Activating the COPY_LANDING");
        console.assert( _stateMachine.ticketModel !== null, "ERROR _stateMachine.ticketModel === null" );
        let ticketCopies = (_stateMachine.ticketModel === null ||
                            _stateMachine.ticketModel.data.dest === null  ||
                            _stateMachine.ticketModel.data.dest.print === null ) ? 1 : _stateMachine.ticketModel.data.dest.data.print.data.copies
        console.log("Number of copies updated according to the ticket (onActivating):", ticketCopies)
        copyLandingView.value = ticketCopies
        if(!_stateMachine.isTicketModelChanged){
            removeSaveButtonFromLayout()
        }
        else if(_stateMachine.isTicketModelChanged){
            //_stateMachine.copyControllerfunctions.updateJobTicket();
            addSaveButtonToLayout()
        }
    }

    Component.onCompleted: {
        console.log("Copy app is there onCompleted!")
        if(_stateMachine.quickSetVisibility == false){
            for (var i=actions.count - 1; i >= 0; --i)
            {
                if (actions.get(i).objectName == "CopyQuickSetSelected"){
                    actions.removeAt(i);
                }
            }
        }
    }


}
