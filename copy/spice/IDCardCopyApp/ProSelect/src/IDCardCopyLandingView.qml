import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtScxml 5.8
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0

LandingLayout{

    id: idCardCopyLandingView
    objectName: "idCardCopyLandingView"

    titleText.stringId: "StringIds.cIDCardCopyApp"

    property bool copyButtonEnabled: true;
    property int numCopies: value;
    isTumblerRequired:true
    from: 1
    to: 99
    value: _stateMachine.ticketModel && _stateMachine.ticketModel.data.dest && _stateMachine.ticketModel.data.dest.data.print ?
               _stateMachine.ticketModel.data.dest.data.print.data.copies : 0

    onNumCopiesChanged: {
        console.log("Number of copies (OnNumCopies) updated in UI:",numCopies, " value:", value)
        _stateMachine.ticketModel.data.dest.data.print.data.copies = numCopies;
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
            _stateMachine.idCardCopyControllerfunctions.printTicketModel(_stateMachine.ticketModel)
        }
    }

    Connections {
        target: _stateMachine
        function onTicketModelChanged(ticketModel) {
            console.log("Ticket model changed:", ticketModel)
            _stateMachine.idCardCopyControllerfunctions.printTicketModel(_stateMachine.ticketModel)
        }
    }
    Connections {
    target: _stateMachine
        function onJobInProgressChanged() {
                console.log("jobInProgressChanged: " + _stateMachine.jobInProgress);
                console.log("activating copy button " + _stateMachine.jobInProgress);
                if (_stateMachine.jobInProgress)
                {
                    console.log("Copy button enabled")
                    copyButtonEnabled = false;
                }
                else
                {
                    console.log("Copy button disabled")
                    copyButtonEnabled = true;
                }
        }
    }


    actions: QQmlObjectListModel {
        ButtonModel {
            objectName: "IDCardCopyButton"
            enabled: idCardCopyLandingView.copyButtonEnabled

            textObject.stringId: "StringIds.cCopy"
            buttonType: SpiceButton.Type.Primary

            onClicked: {
                console.log("ID Card Copy starts!! Copy based on next ticket model:");
                _stateMachine.submitEvent("ev.start.idcard_copy");
            }

        }

        ButtonModel {
            objectName: "IDCardCopyOptionsButton"
            textObject.stringId: "StringIds.cOptions"
            onClicked: {
                console.log("Options clicked")
                _stateMachine.ticketModel.data.dest.data.print.data.copies = numCopies ;
                _stateMachine.submitEvent("ev.options.clicked")
            }
        }
    }



    StackView.onActivating: {

        console.log("Activating the ID_CARD_COPY_LANDING");
        console.assert( _stateMachine.ticketModel !== null, "ERROR _stateMachine.ticketModel === null" );
        let ticketCopies = (_stateMachine.ticketModel === null ||
                            _stateMachine.ticketModel.data.dest === null  ||
                            _stateMachine.ticketModel.data.dest.print === null ) ? 1 : _stateMachine.ticketModel.data.dest.data.print.data.copies
        console.log("Number of copies updated according to the ticket (onActivating):", ticketCopies)
        idCardCopyLandingView.value = ticketCopies
    }

    Component.onCompleted: {
        console.log("ID Card Copy app is there onCompleted!")
    }
}
