import QtQuick 2.15
import QtQml 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxMenu 1.0
import QtQml.Models 2.15
import "qrc:/UnitsUtils.js" as UnitsUtils


MenuRadioIconBranch
{
    id: copySettingsPaperSizeCustomRadioIconBranch
    objectName: "CopySettingsPaperSizeCustom"
    property ISpiceModel ticketModel: null;
    property bool customChecked: false
    property QtObject measurementConfigModel: null
    property bool isMetricInInches: (measurementConfigModel && measurementConfigModel.data && measurementConfigModel.data.displayUnitOfMeasure == System_1_UnitsOfMeasurement.UnitsOfMeasurement.imperial)
    property bool isSettingPrepared: measurementConfigModel && measurementConfigModel.data && ticketModel
    property bool isSelectedUnitInInches: _stateMachine.metricUnitSelected == "" ? isMetricInInches : _stateMachine.metricUnitSelected == "imperial" ? true : false

    readonly property int expectedDecimalsInInches: 2
    readonly property int expectedDecimalsInMm: 0

    function clickAction() {
        console.log("copySettingsPaperSizeCustomRadioIconBranch on clicked")
        if (ticketModel.data.dest.print.mediaSize != Glossary_1_MediaSize.MediaSize.custom)
        {
            ticketModel.data.dest.print.mediaSize = Glossary_1_MediaSize.MediaSize.custom
            _resourceStore.modify(ticketModel)
            copySettingsPaperSizeCustomRadioIconBranch.controlModel.checked = true // Force true check value
        }
    }

    function generateSettingText(){

        let customMediaXFeedDimension = getValueOnMetricExpected(ticketModel.data.dest.print.customMediaXFeedDimension)
        let customMediaYFeedDimension = getValueOnMetricExpected(ticketModel.data.dest.print.customMediaYFeedDimension)
        let returnVal = _qmlUtils.createSpiceLoc( copySettingsPaperSizeCustomRadioIconBranch  , 
                                    {"stringId": isSelectedUnitInInches ? "StringIds.cPaperRange" : "StringIds.cDimensionFloatZero",
                                     "params": [customMediaXFeedDimension,
                                                customMediaYFeedDimension,
                                                _qmlUtils.createSpiceLoc(root , {"stringId": isSelectedUnitInInches ? "StringIds.cInches" : "StringIds.cUnitOfMeasureMillimeters"})
                                    ]})

        return returnVal
    }

    function getValueOnMetricExpected(objectValue)
    {
        let returnVal = 0
        if(isSelectedUnitInInches)
        {
            returnVal = UnitsUtils.dpiToInch(objectValue).toFixed(expectedDecimalsInInches)
        }
        else // metric is on milimetters
        {
            returnVal = UnitsUtils.dpiToMm(objectValue).toFixed(expectedDecimalsInMm)
        }
        return Number.parseFloat(returnVal)
    }

    function generateTextCustomValues(){
        if(isSettingPrepared)
        {
            // Concatenated message:
            // Loc. Ex. Result -> (210.00x297.00 mm) / (8.50x11.00 in)
            copySettingsPaperSizeCustomRadioIconBranch.controlModel.infoText = generateSettingText()
            console.log("copySettingsPaperSizeCustomRadioIconBranch generate custom width and length text: ",copySettingsPaperSizeCustomRadioIconBranch.controlModel.infoText.text)   
        }
        else
        {
            console.log("copySettingsPaperSizeCustomRadioIconBranch setting is not prepared to show text values")
        }

    }

    function checkRadioButtonState()
    {
        customChecked = ticketModel.data.dest.print.mediaSize == Glossary_1_MediaSize.MediaSize.custom
        console.log("CopySettingsPaperSizeCustom check current state of radio button check: ", customChecked? "true": "false")
        copySettingsPaperSizeCustomRadioIconBranch.controlModel.checked = customChecked
    }

    function connectValue(){
        console.log("connectValue")
        ticketModel = _stateMachine.ticketModel
        copySettingsPaperSizeCustomRadioIconBranch.controlModel.icon = "qrc:/images/Glyph/ChevronRight.json" 
        copySettingsPaperSizeCustomRadioIconBranch.controlModel.checkable = false
        copySettingsPaperSizeCustomRadioIconBranch.controlModel.clicked.connect(clickAction)
        generateTextCustomValues()
        checkRadioButtonState()
        ticketModel.data.dest.print.mediaSizeChanged.connect(checkRadioButtonState)
        ticketModel.data.dest.print.customMediaXFeedDimensionChanged.connect(generateTextCustomValues)
        ticketModel.data.dest.print.customMediaYFeedDimensionChanged.connect(generateTextCustomValues)
        _stateMachine.metricUnitSelectedChanged.connect(generateTextCustomValues)
        
    }

    Component.onCompleted: {
        console.log("Component.onCompleted")
        // Called later to load menu containers previously and then connect to cdm and option expected
        let measurementConfigResponse = _resourceStore.subscribe("/cdm/system/v1/configuration");
        measurementConfigResponse.resolved.connect((future) => {
            console.log("CopySettingsPaperSizeCustomRadioIconBranch connect response subscribe to configuraton" )
            measurementConfigModel = future.get();

            if(measurementConfigModel.data.displayUnitOfMeasure == System_1_UnitsOfMeasurement.UnitsOfMeasurement.imperial && _stateMachine.metricUnitSelected == "")
            {
                console.log("CopySettingsPaperSizeCustomRadioIconBranch connect response subscribe to configuraton is imperial, set metricUnitSelected to imperial")
                _stateMachine.metricUnitSelected = "imperial"
            }
            else if (measurementConfigModel.data.displayUnitOfMeasure == System_1_UnitsOfMeasurement.UnitsOfMeasurement.metric && _stateMachine.metricUnitSelected == "")
            {
                console.log("CopySettingsPaperSizeCustomRadioIconBranch connect response subscribe to configuraton is metric, set metricUnitSelected to metric")
                _stateMachine.metricUnitSelected = "metric"
            }

            // Force regenerate
            generateTextCustomValues();
        });

        measurementConfigResponse.rejected.connect((future) => {
            console.warn("CopySettingsPaperSizeCustomRadioIconBranch connect subscribe to check units fail")
        });

        Qt.callLater(connectValue)
    }
    Component.onDestruction: {
        console.log("copy setting print mediasize and custom x,y disconnect")
        copySettingsPaperSizeCustomRadioIconBranch.controlModel.clicked.disconnect(clickAction)

        ticketModel.data.dest.print.mediaSizeChanged.disconnect(checkRadioButtonState)
        ticketModel.data.dest.print.customMediaXFeedDimensionChanged.disconnect(generateTextCustomValues)
        ticketModel.data.dest.print.customMediaYFeedDimensionChanged.disconnect(generateTextCustomValues)
        _stateMachine.metricUnitSelectedChanged.disconnect(generateTextCustomValues)
    }
}