import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import QtQml.Models 2.15

SpiceListView {
    id:root
    objectName: "copy_bookletView"
    header: SpiceLocObject {stringId: "StringIds.cBooklet"}

    property ISpiceModel ticketModel: null;
    property ISpiceModel constraintModel: null;

    // Properties used by pattern
    property QtObject menuResourceInstance: _menuResource
    property var pushMenuItem : null
    property var resourceModel : null
    property string valueResource:""
    property string constraint:""
    property string menuDynamicUrl: ""
    property string titleId:""
    property string enumType : ""
    property string node:""

    ButtonGroup {
        id: foldAndStitchGroup
    }

    Component {
        id: radioButtonModelComponents
        RadioButtonModel {}
    }

    Component {
        id: radioButtonListViewModels
        SettingsRadioButtonViewModel{}        
    }

    Component {
        id: checkboxModelComponent
        CheckboxModel {}
    }

    Component {
        id: checkboxListViewModels
        SettingsCheckBoxViewModel{}
    }

    Component {
        id : sliderModelComponent
        SpinBoxModel {}
    }

    Component {
        id : spinBoxViewModel
        SettingsSpinBoxViewModel {}
    }

    Component {
        id: controlModelTitleText
        TitleTextModel{}
    }

    Component {
        id: titleTextViewModel
        ListViewModel{
            id: bookletImage
            objectName: "bookletImage"
            clickable: false
            isSubordinate: true
            blocks: QQmlObjectListModel {
                RowBlockComponentModel {
                    fillWidth : true
                    alignment : Qt.AlignLeft
                    componentList : ObjectModel {
                        SpiceTextImage  {
                            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                            variation: SpiceTextImage.Variation.ImageContainer
                            images : getFirstBookletImage()
                            size: 10 * Global.rem
                        }
                        SpiceSpacer{
                            type: Global.breakpoint <= Global.BreakPoint.S ? SpiceSpacer.Type.SP4 : SpiceSpacer.Type.SP5
                        }
                        SpiceTextImage  {
                            Layout.alignment: Qt.AlignLeft
                            variation: SpiceTextImage.Variation.ImageContainer
                            images : getSecondBookletImage()
                            size: 4 * Global.rem
                        }
                        SpiceSpacer{
                            type: Global.breakpoint <= Global.BreakPoint.S ? SpiceSpacer.Type.SP4 : SpiceSpacer.Type.SP5
                        }
                        SpiceTextImage  {
                            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                            variation: SpiceTextImage.Variation.ImageContainer
                            images : getThirdBookletImage()
                            size: 10 * Global.rem
                        }
                    }
                }
            }
        }
    }

    onNodeChanged: {
        if(node != ""){
            enumType = "dune::spice::jobTicket_1::Booklet::Booklet"
            let bookletFormatConstraint = _stateMachine.controller.findValidatorForConstraint("pipelineOptions/imageModifications/bookletFormat");
            let imageborderConstraint = _stateMachine.controller.findValidatorForConstraint("pipelineOptions/imageModifications/imageBorder");

            let FoldAndStitchConstraint = _stateMachine.controller.findValidatorForConstraint("dest/print/bookletMakerOption");

            if(bookletFormatConstraint){
                let stringId = _propertyMap.cStringIDForEnum(enumType, "bookletFormat")
                addCheckBoxMenuforBookletFormat("bookletFormat", stringId, ticketModel.data.pipelineOptions.imageModifications.bookletFormat, JobTicket_1_BookletFormat.BookletFormat.leftEdge, "qrc:/images/Glyph/BookletFormat.json")
                stringId = _propertyMap.cStringIDForEnum(enumType, "bordersOnEachPage")
                addSubordinateCheckBox("bordersOnEachPage", stringId, "qrc:/images/Glyph/BookletBorders.json")
            }

            if(FoldAndStitchConstraint && (FoldAndStitchConstraint.options.count > 1 ||
                (FoldAndStitchConstraint.disabled && FoldAndStitchConstraint.disabled.value == Glossary_1_FeatureEnabled.FeatureEnabled.true_)))
            {
                let stringId = _propertyMap.cStringIDForString("CopyBookletMakerOption", "saddleStitch")
                let checked = ticketModel.data.dest.print.sheetsPerFoldSet.deviceSetsFoldAndStitchSheetsEnabled
                addCheckBoxMenuforFoldAndStitch("foldAndStitch", stringId, ticketModel.data.dest.print.bookletMakerOption, JobTicket_1_BookletMakerOptions.BookletMakerOptions.saddleStitch, "qrc:/images/Glyph/FoldAndStitch.json")
                if(FoldAndStitchConstraint.options.count > 1 )
                {
                    addRadioButton("Automatic", "StringIds.cAutomatic", ticketModel.data.dest.print.sheetsPerFoldSet.deviceSetsFoldAndStitchSheetsEnabled, Glossary_1_FeatureEnabled.FeatureEnabled.true_)
                    addRadioButton("Custom", "StringIds.cCustom", ticketModel.data.dest.print.sheetsPerFoldSet.deviceSetsFoldAndStitchSheetsEnabled, Glossary_1_FeatureEnabled.FeatureEnabled.false_)
                    addSliderButton("sheetsFoldedTogether", "StringIds.cMaximumSheetsPerSet")
                }
            }
            addTextImage()
            console.debug("Booklet Component Start")
        }
    }

    function getFirstBookletImage(){
        let bookletFormat = ticketModel.data.pipelineOptions.imageModifications.bookletFormat == JobTicket_1_BookletFormat.BookletFormat.leftEdge? true : false;
        let foldAndStitch = ticketModel.data.dest.print.bookletMakerOption == JobTicket_1_BookletMakerOptions.BookletMakerOptions.saddleStitch? true : false;
        let imgs = [];

        if(bookletFormat)
        {
            imgs.push("qrc:/images/Graphics/PagesPerSheetOneUpBig.json");
        }
        else if(foldAndStitch)
        {
            imgs.push("qrc:/images/Graphics/BookletFormatBig.json");
        }
        else
        {
            imgs.push("qrc:/images/Graphics/PagesPerSheetOneUpBig.json");
        }

        return imgs;
    }

    function getSecondBookletImage(){
        let imgs = [];
        if(ticketModel.data.pipelineOptions.imageModifications.bookletFormat == JobTicket_1_BookletFormat.BookletFormat.leftEdge
            || ticketModel.data.dest.print.bookletMakerOption == JobTicket_1_BookletMakerOptions.BookletMakerOptions.saddleStitch){
            imgs.push("qrc:/images/Glyph/ArrowRight.json");
        }
        else{
            imgs.push("");
        }
        return imgs;
    }

    function getThirdBookletImage(){
        let bookletFormat = ticketModel.data.pipelineOptions.imageModifications.bookletFormat == JobTicket_1_BookletFormat.BookletFormat.leftEdge? true : false;
        let imageBorder = ticketModel.data.pipelineOptions.imageModifications.imageBorder == JobTicket_1_ImageBorder.ImageBorder.defaultLineBorder? true : false;
        let foldAndStitch = ticketModel.data.dest.print.bookletMakerOption == JobTicket_1_BookletMakerOptions.BookletMakerOptions.saddleStitch? true : false;

        let imgs = [];

        if(foldAndStitch)
        {
            if(false == bookletFormat)
            {
                imgs.push("qrc:/images/Graphics/BookletBordersStitchBig.json");
            }
            else{
                if(imageBorder)
                {
                    imgs.push("qrc:/images/Graphics/BookletBordersStitchBig.json");
                }
                else{ //To be Modified
                    imgs.push("qrc:/images/Graphics/BookletBordersStitchBig.json");
                }
            }
        }
        else if(bookletFormat)
        {
            if(imageBorder)
            {
                imgs.push("qrc:/images/Graphics/BookletBordersBig.json");
            }
            else{
                imgs.push("qrc:/images/Graphics/BookletFormatBig.json");
            }
        }
        else{
            imgs.push("");
        }    
        return imgs;
    }
    
    function addTextImage()
    {
        rowList.append(titleTextViewModel.createObject(rowList,
                                                        {
                                                            "visible": true
                                                        }));
    }
    
    function addCheckBoxMenuforBookletFormat(objName, buttonStrId, enum1, value1, icon)
    {   
        let validator = _stateMachine.controller.findValidatorForConstraint("pipelineOptions/imageModifications/bookletFormat")
        let isConstrained = false
        let message = _qmlUtils.createSpiceLoc(root ,{"stringId": "StringIds.cThisOptionUnavailable"})

        for (let index =0 ; index < validator.options.count ;index++ )
        {
            let value = validator.options.get(index).seValue
            if(objName === "bookletFormat" && value === "leftEdge")
            {
                if(validator.options.get(index).disabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_)
                {
                   isConstrained = true
                   message = _qmlUtils.createSpiceLoc( root ,{"text":validator.options.get(index).message})
                   break
                }
            }
        }
        let isPagesPerSheetConstrained = ticketModel.data.pipelineOptions.imageModifications.pagesPerSheet == JobTicket_1_PagesPerSheet.PagesPerSheet.fourUp ? true : false
        let ispagesFlipUpConstrained = ticketModel.data.src.scan.pagesFlipUpEnabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_ ? true : false
        let isCollateConstrained = ticketModel.data.dest.print.collate == JobTicket_1_CollateModes.CollateModes.uncollated ? true : false
        if(objName === "bookletFormat" && (isPagesPerSheetConstrained || ispagesFlipUpConstrained || isCollateConstrained))
        {
            isConstrained = true
            if(isCollateConstrained)
            {
                message = _qmlUtils.createSpiceLoc(root ,{"stringId": "StringIds.cBookletConstraintCollateDisabled"})
            }
        }
        let checkboxModel = checkboxModelComponent.createObject(rowList,
                                                    {
                                                        "objectName": objName,
                                                        "textObject": _qmlUtils.createSpiceLoc( root , {"stringId": buttonStrId }),
                                                        "checked": enum1 == value1 ? true : false,
                                                        "constrained": isConstrained,
                                                        "constrainedMessage": message,
                                                        "icon": icon
                                                    });
        
        checkboxModel.onCheckedChanged.connect(function(){
            if(checkboxModel.checked)
            {
                setCheckedValue(objName, value1)
            }
            else
            {
                setUnCheckedValue(objName, value1)
            }
            _resourceStore.modify(ticketModel)
        });

        rowList.append(checkboxListViewModels.createObject(rowList,
                                                        {
                                                            "objectName" : "CheckBoxOptions" + objName,
                                                            "controlModel": checkboxModel,
                                                            "lined": false
                                                        }));
    }

    function addCheckBoxMenuforFoldAndStitch(objName, buttonStrId, enum1, value1, icon)
    {   
        let validator = _stateMachine.controller.findValidatorForConstraint("dest/print/bookletMakerOption")
        let isConstrained = (validator.disabled) && (validator.disabled.value == Glossary_1_FeatureEnabled.FeatureEnabled.true_ ? true : false)
        let message = _qmlUtils.createSpiceLoc(root ,{"stringId": "StringIds.cThisOptionUnavailable"})

        if(isConstrained)
        {
            message = validator.disabled.message
        }
        else{
            for (let index =0 ; index < validator.options.count ;index++ )
            {
                if(validator.options.get(index).seValue === "saddleStitch")
                {
                    if(validator.options.get(index).disabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_)
                    {
                        isConstrained = true
                        message = validator.options.get(index).message
                        break
                    }
                }
            }
        }

        let checkboxModel = checkboxModelComponent.createObject(rowList,
                                                    {
                                                        "objectName": objName,
                                                        "textObject": _qmlUtils.createSpiceLoc( root , {"stringId": buttonStrId }),
                                                        "checked": ticketModel.data.dest.print.bookletMakerOption == JobTicket_1_BookletMakerOptions.BookletMakerOptions.saddleStitch ? true : false,
                                                        "constrained": isConstrained,
                                                        "constrainedMessage": _qmlUtils.createSpiceLoc( root ,{"text":message}),
                                                        "icon": icon
                                                    });
        
        checkboxModel.clicked.connect(function(val)
        {
            if(ticketModel.data.dest.print.bookletMakerOption == JobTicket_1_BookletMakerOptions.BookletMakerOptions.saddleStitch)
            {
                ticketModel.data.dest.print.bookletMakerOption = JobTicket_1_BookletMakerOptions.BookletMakerOptions.none
            }
            else
            {
                ticketModel.data.dest.print.bookletMakerOption = JobTicket_1_BookletMakerOptions.BookletMakerOptions.saddleStitch
            }
            _resourceStore.modify(ticketModel)
        });

        rowList.append(checkboxListViewModels.createObject(rowList,
                                                        {
                                                            "objectName" : "CheckBoxOptions" + objName,
                                                            "controlModel": checkboxModel,
                                                            "lined": false
                                                        }));
    }

    function addSubordinateCheckBox(objName, buttonStrId, icon)
    {
        let subcheckboxModel = checkboxModelComponent.createObject(rowList,
                                                    {
                                                        "objectName" : objName,
                                                        "textObject": _qmlUtils.createSpiceLoc( root , {"stringId": buttonStrId }),
                                                        "checked": ticketModel.data.pipelineOptions.imageModifications.imageBorder == JobTicket_1_ImageBorder.ImageBorder.defaultLineBorder ? true : false,
                                                        "constrainedMessage" : _qmlUtils.createSpiceLoc(root ,{"stringId": "StringIds.cBookletConstraintMessage1"}),
                                                        "icon": icon
                                                    });
        subcheckboxModel.constrained = Qt.binding(function(){return ticketModel.data.pipelineOptions.imageModifications.bookletFormat == JobTicket_1_BookletFormat.BookletFormat.off ? true : false})
        subcheckboxModel.onCheckedChanged.connect(function(){
            if(subcheckboxModel.checked)
            {
                ticketModel.data.pipelineOptions.imageModifications.imageBorder = JobTicket_1_ImageBorder.ImageBorder.defaultLineBorder
            }
            else
            {
                ticketModel.data.pipelineOptions.imageModifications.imageBorder = JobTicket_1_ImageBorder.ImageBorder.noBorder
            }
            _resourceStore.modify(ticketModel)
        });

        subcheckboxModel.onConstrainedChanged.connect(function(){
            if(subcheckboxModel.constrained)
            {
                subcheckboxModel.checked = false
            }
        });

        rowList.append(checkboxListViewModels.createObject(rowList,
                                                        {
                                                            "objectName" : "CheckBoxOptions" + objName,
                                                            "controlModel": subcheckboxModel,
                                                            "isSubordinate": true,
                                                            "lined": false
                                                        }));
    }

    function addRadioButton(objName, buttonStrId, enumVal1, enumVal2)
    {
        let message = "";
        let radioButtonModel = radioButtonModelComponents.createObject(rowList,
                                                   {
                                                        "objectName": objName,
                                                        "textObject": _qmlUtils.createSpiceLoc( root ,{"stringId": buttonStrId }),
                                                        "checked": enumVal1 == enumVal2,
                                                        "clickable" : false,
                                                        "constrainedMessage" : _qmlUtils.createSpiceLoc(root ,{"stringId": "StringIds.cBookletConstraintMessage2"}),
                                                        "buttonGroup": foldAndStitchGroup
                                                   });
        radioButtonModel.constrained = Qt.binding(function(){return  ticketModel.data.dest.print.bookletMakerOption == JobTicket_1_BookletMakerOptions.BookletMakerOptions.saddleStitch? false : true})
        radioButtonModel.clicked.connect(function()
        {   
            if(objName =="Automatic")
            {
                ticketModel.data.dest.print.sheetsPerFoldSet.deviceSetsFoldAndStitchSheetsEnabled = Glossary_1_FeatureEnabled.FeatureEnabled.true_
            }
            else
            {
                ticketModel.data.dest.print.sheetsPerFoldSet.deviceSetsFoldAndStitchSheetsEnabled = Glossary_1_FeatureEnabled.FeatureEnabled.false_
            }
            _resourceStore.modify(ticketModel)
            console.log("Modify ticketModel")
        })
  
        rowList.append(radioButtonListViewModels.createObject(rowList,
                                                    {
                                                        "controlModel": radioButtonModel,
                                                        "objectName" :  "ComboBoxOptions" + objName,
                                                        "isSubordinate": true,
                                                        "lined": false
                                                    }));
    }

    function addSliderButton(objName, buttonStrId){

        let validatorFoldAndStitchSheets = _stateMachine.controller.findValidatorForConstraint("dest/print/sheetsPerFoldSet/foldAndStitchSheets");

        let spinModel   =  sliderModelComponent.createObject(rowList,
                                                   {
                                                        "objectName": objName,
                                                        "textObject": _qmlUtils.createSpiceLoc( root , {"stringId": buttonStrId }),
                                                        //"checked":  _menuResource.enumStringFromValue("dune::spice::jobTicket_1::scaling::ScaleSelection::ScaleSelection", ticketModel.data.pipelineOptions.scaling.scaleSelection) == objName ? true : false,
                                                        "clickable" : true,
                                                        "from": validatorFoldAndStitchSheets.data.min.data.value,
                                                        "to": validatorFoldAndStitchSheets.data.max.data.value,
                                                        "stepSize": validatorFoldAndStitchSheets.data.step.data.value,
                                                        "value":  ticketModel.data.dest.print.sheetsPerFoldSet.foldAndStitchSheets,
                                                        "enabled": _stateMachine.controller.isSettingEnabled("dest/print/sheetsPerFoldSet/foldAndStitchSheets"),
                                                        "constrainedMessage" : _qmlUtils.createSpiceLoc(root ,{"stringId": "StringIds.cBookletConstraintMessage3"}),
                                                        "spinboxText": _qmlUtils.createSpiceLoc( root , {"stringId": "StringIds.cMaxFoldText"})
                                                   })
        spinModel.constrained = Qt.binding(function(){
            console.log("TicketModel: " + ticketModel);
            if( ticketModel != null && ticketModel.data != null)
            {
                console.log("deviceSetsFoldAndStitchSheetsEnabled value: " + ticketModel.data.dest.print.sheetsPerFoldSet.deviceSetsFoldAndStitchSheetsEnabled);
                return ticketModel.data.dest.print.sheetsPerFoldSet.deviceSetsFoldAndStitchSheetsEnabled == Glossary_1_FeatureEnabled.FeatureEnabled.true_ ? true : false
            }
            else{
                console.warn("TicketModel or ticketModel.data is null in addSliderButton");
                return false;
            }
        })
        spinModel.onValueChanged.connect(function(val)
        {
            ticketModel.data.dest.print.sheetsPerFoldSet.foldAndStitchSheets = spinModel.value
            _resourceStore.modify(ticketModel)
            console.log("Modify ticketModel")
        })

        rowList.append(spinBoxViewModel.createObject(rowList,   
                                                    {
                                                        "controlModel": spinModel ,
                                                        "objectName" : objName + "Row",
                                                        "isSubordinate": true,
                                                        "lined": false
                                                    }))
     }

    function setCheckedValue(objName, value){
        if (objName == "bookletFormat"){
            ticketModel.data.pipelineOptions.imageModifications.bookletFormat = JobTicket_1_BookletFormat.BookletFormat.leftEdge
            ticketModel.data.pipelineOptions.scaling.xScalePercent = 62.4489795918836739
            ticketModel.data.pipelineOptions.scaling.yScalePercent = 62.4489795918836739
            ticketModel.data.pipelineOptions.imageModifications.pagesPerSheet = JobTicket_1_PagesPerSheet.PagesPerSheet.twoUp
            ticketModel.data.dest.print.plexMode = Glossary_1_PlexMode.PlexMode.duplex
            ticketModel.data.dest.print.duplexBinding = Glossary_1_DuplexBinding.DuplexBinding.twoSidedShortEdge
        }
        else if (objName == "foldAndStitch"){
            ticketModel.data.pipelineOptions.imageModifications.numberUpPresentationDirection = JobTicket_1_NumberUpPresentationDirection.NumberUpPresentationDirection.toBottomToRight
        }
    }

    function setUnCheckedValue(objName, value){
        if (objName == "bookletFormat"){
            ticketModel.data.pipelineOptions.imageModifications.bookletFormat = JobTicket_1_BookletFormat.BookletFormat.off
            ticketModel.data.pipelineOptions.scaling.xScalePercent = 100
            ticketModel.data.pipelineOptions.scaling.yScalePercent = 100
            ticketModel.data.pipelineOptions.imageModifications.pagesPerSheet = JobTicket_1_PagesPerSheet.PagesPerSheet.oneUp
            ticketModel.data.pipelineOptions.imageModifications.imageBorder = JobTicket_1_ImageBorder.ImageBorder.noBorder
            ticketModel.data.dest.print.plexMode = Glossary_1_PlexMode.PlexMode.simplex
            ticketModel.data.dest.print.duplexBinding = Glossary_1_DuplexBinding.DuplexBinding.oneSided
        }
        else if (objName == "foldAndStitch"){
            ticketModel.data.pipelineOptions.imageModifications.numberUpPresentationDirection = JobTicket_1_NumberUpPresentationDirection.NumberUpPresentationDirection.toBottomToLeft
        }
    }

    function setFoldAndStitch(value){
        if (value == "landscape"){
            ticketModel.data.src.scan.contentOrientation = Glossary_1_ContentOrientation.ContentOrientation.landscape
        }
        else if (value == "portrait"){
            ticketModel.data.src.scan.contentOrientation = Glossary_1_ContentOrientation.ContentOrientation.portrait
        }
    }

    footer: SpiceFooter {
        anchors {left: parent.left; right: parent.right;}
        rightBlockModel: QQmlViewListModel {
            SpiceButton {
                id: doneButton
                objectName: "doneButton"
                type: SpiceButton.Type.PrimaryFlow
                Layout.alignment: Qt.AlignRight
                textObject: SpiceLocObject {
                    stringId: "StringIds.cDoneButton"
                }
                onClicked: {
                    _window.postViewEvent(QmlUtils.ViewEventType.Back)
                }
            }
        }
    }

    Component.onCompleted: {
        ticketModel = _stateMachine.ticketModel
        console.log(" copy setting booklet view disconnect")
    }
}