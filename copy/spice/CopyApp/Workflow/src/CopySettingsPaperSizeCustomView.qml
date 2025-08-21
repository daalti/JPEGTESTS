import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import QtQml.Models 2.15
import "qrc:/UnitsUtils.js" as UnitsUtils
import "qrc:/SpiceBinding.js" as SpiceBinding

SpiceModalLayout
{
    id:root
    objectName: "CopySettingsPaperSizeCustomModal"
    modalWidth : SpiceModalLayout.SpiceModalWidthType.FULL
    _modal: true

    /* These properties are needed from menu framework. but not used in this layout. */
    property var pushMenuItem : null
    property var resourceModel : null
    property string titleId:""
    property string enumType : ""
    property string valueResource:""
    property string constraint:""
    property string menuDynamicUrl: ""
    property string node:""
    property QtObject menuResourceInstance: _menuResource

    footer: SpiceFooter {

        anchors.left: parent.left
        anchors.right: parent.right

        rightBlockModel: ObjectModel {
            SpiceButton{
                id: copySettingsPaperSizeCustomViewDoneBtn
                objectName: "copySettingsPaperSizeCustomViewDoneBtn"
                Layout.alignment: Qt.AlignRight
                textObject.stringId: "StringIds.cDoneButton"
                type: SpiceButton.Type.PrimaryFlow

                onClicked: {
                    console.log("clicked Done button in CopySettingsPaperSizeCustomView")
                    _window.postViewEvent(QmlUtils.ViewEventType.Back)
                }
            }
        }
    }

    content : SpiceListView {
        id: copySettingsPaperSizeCustomView
        objectName: "CopySettingsPaperSizeCustomView"
        width: root.modalPaintedWidth
        height: root.modalPaintedHeight - SpiceFooterViewConstants.height -SpiceHeaderViewConstants.height

        property QQmlObjectListModel controlModelList : QQmlObjectListModel {}
        property QtObject spinModel : SpinBoxModel {}

        property ISpiceModel ticketModel: null;
        // Check on unit to indicate if current machine must to indicate data for client on inches or in mm
        property QtObject measurementConfigModel: null

        // Cdm related field
        property QtObject xSpinBoxValidator: null
        property QtObject ySpinBoxValidator: null

        property bool isMetricInInches: (measurementConfigModel && measurementConfigModel.data && measurementConfigModel.data.displayUnitOfMeasure == System_1_UnitsOfMeasurement.UnitsOfMeasurement.imperial)

        property bool settingDependenciesArePrepared: measurementConfigModel && measurementConfigModel.data && xSpinBoxValidator && ySpinBoxValidator && ticketModel
        property bool isSelectedUnitInInches: _stateMachine.metricUnitSelected == "" ? isMetricInInches : _stateMachine.metricUnitSelected == "imperial" ? true : false

        readonly property int expectedDecimalsInInches: 2
        readonly property int expectedDecimalsInMm: 0
        readonly property int expectedDecimalsInDpi: 0

        Component {
            id : copySettingsPaperSizeCustomComboBox
            SettingsComboBoxViewModel {
                id : copySettingsPaperSizeCustomComboBoxView

                controlModel : ComboBoxListModel {
                    id : copySettingsPaperSizeCustomComboBoxList
                    textObject : SpiceLocObject {
                        stringId : "StringIds.cUnitofMeasurement"
                    }
                    model : QQmlObjectListModel {
                        ComboBoxModel {
                            objectName : "comboListMillimeter"
                            textObject : SpiceLocObject {
                                stringId : "StringIds.cUnitofMillimeter"
                            }
                            value : 0
                        }
                        ComboBoxModel {
                            objectName : "comboListInches"
                            textObject : SpiceLocObject {
                                stringId : "StringIds.cUnitOfMeasureInches"
                            }
                            value : 1
                        }
                    }
                }

                Component.onCompleted: {
                    copySettingsPaperSizeCustomComboBoxView.controlModel.currentIndex = isSelectedUnitInInches ? 1 : 0

                    controlModel.selected.connect(function (val) {
                        console.log("controlModel val is: " + val )
                        if(val == 1 && _stateMachine.metricUnitSelected != "imperial")
                        {
                            console.log("selection imperial")
                            copySettingsPaperSizeCustomView.rowList.removeAt(1, copySettingsPaperSizeCustomView.rowList.count - 1)
                            //isMetricInInches = val
                            _stateMachine.metricUnitSelected = "imperial"
                            copySettingsPaperSizeCustomView.controlModelList.clear()

                        }
                        else if(val == 0 && _stateMachine.metricUnitSelected != "metric")
                        {
                            console.log("selection metric")
                            copySettingsPaperSizeCustomView.rowList.removeAt(1, copySettingsPaperSizeCustomView.rowList.count - 1)
                            _stateMachine.metricUnitSelected = "metric"
                            copySettingsPaperSizeCustomView.controlModelList.clear()
                        }
                    })
                }
            }
        }

        Component {
            id: copySettingsPaperSizeCustomImageModel
            ListViewModel{
                id: imageCustom
                objectName: "imageCustom"
                clickable: false
                blocks: QQmlObjectListModel {
                    RowBlockInfoModel {
                        imageTextModel: ImageTextModel{
                            images: [getTrayImage()]
                            imagesOrientation: Qt.AlignLeft
                            imagesAlignMiddle: false
                        }
                    }
                }
            } //ListViewModel
        }

        Component {
            id : sliderModelComponent
            SpinBoxModel {}
        }

        Component {
            id : spinBoxViewModel

            SettingsSpinBoxViewModel {
                id : root
                controlModel : SpinBoxModel {}
                visible : controlModel.visible
                clickable : false
                description.text : controlModel.description !== null ? controlModel.description.text : ""
                property var imagePath : ""
                property string infoText : ""
                blocks : QQmlObjectListModel {
                    RowBlockComponentModel {
                        fillWidth : true
                        alignment : Qt.AlignLeft
                        componentList : ObjectModel {
                            SpiceTextImage  {
                                Layout.fillWidth: true
                                imagesOrientation: Qt.AlignLeft
                                imagesAlignMiddle: false
                                images : [imagePath]
                                contentsTexts: QQmlObjectListModel{
                                    SpiceLocObject{
                                        stringId : infoText
                                    }
                                }
                            }
                        }
                    }
                    RowBlockComponentModel {
                        id : comonentBlock
                        fillWidth : true
                        alignment : Qt.AlignRight
                        componentList : ObjectModel {
                            SpiceSpinBox {
                                id : menuSpiceSpinBox
                                objectName : controlModel.objectName === "" ? (controlModel.textObject === null ? "" : controlModel.textObject.text) : controlModel.objectName
                                value : controlModel.value
                                from : controlModel.from
                                to : controlModel.to
                                decimals : controlModel.decimals
                                stepSize : controlModel.stepSize
                                spinboxText: SpiceLocObject {
                                    stringId : isSelectedUnitInInches ? "StringIds.cPaperRangeDeciTo" : "StringIds.cRangeDeciFloatZero"; params:[controlModel.from, controlModel.to, _qmlUtils.createSpiceLoc(root,{"stringId": isSelectedUnitInInches ? "StringIds.cInches" : "StringIds.cUnitOfMeasureMillimeters"})]
                                }
                                Component.onCompleted : {
                                    SpiceBinding.twoWayBinding(menuSpiceSpinBox, "value", controlModel)
                                }
                                Component.onDestruction : {
                                    SpiceBinding.destroyTwoWayBinding(menuSpiceSpinBox, "value", controlModel)
                                }
                            }
                        }
                    }
                }
            }
        }

        //1
        Component.onCompleted: {
            console.log("Component.onCompleted")
            rowList.append(copySettingsPaperSizeCustomComboBox.createObject(rowList, {
                "visible": true
            }));
            Qt.callLater(connectAllCdmNeeds)
        }

        //2
        // Method to take the external cdm needs for work with current qml component
        function connectAllCdmNeeds()
        {
            // Connect to configuration on start to take unit current metrics
            ticketModel = _stateMachine.ticketModel
            xSpinBoxValidator = _stateMachine.controller.findValidatorForConstraint("dest/print/customMediaXFeedDimension");
            ySpinBoxValidator = _stateMachine.controller.findValidatorForConstraint("dest/print/customMediaYFeedDimension");

            let measurementConfigResponse = _resourceStore.subscribe("/cdm/system/v1/configuration");
            measurementConfigResponse.resolved.connect((future) => {
                console.log("copySettingsPaperSizeCustomView connect response subscribe to configuration" )
                measurementConfigModel = future.get();
            });

            measurementConfigResponse.rejected.connect((future) => {
                console.warn("copySettingsPaperSizeCustomView connect subscribe to check units fail")
            });
        }

        onXSpinBoxValidatorChanged: {
            if(xSpinBoxValidator == null)
            {
                xSpinBoxValidator = _stateMachine.controller.findValidatorForConstraint("dest/print/customMediaXFeedDimension");
            }
        }

        onYSpinBoxValidatorChanged: {
            if(ySpinBoxValidator == null)
            {
                ySpinBoxValidator = _stateMachine.controller.findValidatorForConstraint("dest/print/customMediaYFeedDimension");
            }
        }

        //3
        onSettingDependenciesArePreparedChanged: {
            if(settingDependenciesArePrepared){
                connectSpinBox()
            }
        }

        onIsSelectedUnitInInchesChanged: {
            if(settingDependenciesArePrepared)
            {
                connectSpinBox()
            }  
        }

        function connectSpinBox(){
            let xFrom = getValueOnMetricExpected(xSpinBoxValidator.minDouble.value)
            let xTo = getValueOnMetricExpected(xSpinBoxValidator.maxDouble.value)
            let xStep = getStepValueOnMetricExpected(xSpinBoxValidator.stepDouble.value)
            let xValue =  getValueOnMetricExpected(ticketModel.data.dest.print.customMediaXFeedDimension)
            let xSpinBox = addSliderButton("xDimexsionSpinBox", "StringIds.cXDimension", "qrc:/images/Glyph/Xaxis.json", xFrom, xTo, xStep, xValue)
            xSpinBox.onValueChanged.connect(() => {
                console.log("xSpinBox.onValueChanged")
                tryUpdateXValueOnCdm(xSpinBox.value)
            })

            let yFrom = getValueOnMetricExpected(ySpinBoxValidator.minDouble.value)
            let yTo = getValueOnMetricExpected(ySpinBoxValidator.maxDouble.value)
            let yStep = getStepValueOnMetricExpected(ySpinBoxValidator.stepDouble.value)
            let yValue = getValueOnMetricExpected(ticketModel.data.dest.print.customMediaYFeedDimension)
            let ySpinBox = addSliderButton("yDimexsionSpinBox", "StringIds.cYDimension", "qrc:/images/Glyph/Yaxis.json", yFrom, yTo, yStep, yValue)
            ySpinBox.onValueChanged.connect(() => {
                console.log("ySpinBox.onValueChanged")
                tryUpdateYValueOnCdm(ySpinBox.value)
            })

            rowList.append(copySettingsPaperSizeCustomImageModel.createObject(rowList, {
                "visible": true
            }));
        }

        function addSliderButton(objName, buttonStrId, imagePath, lower, upper, step, defVal) {
            let decimals = (isSelectedUnitInInches) ? expectedDecimalsInInches : expectedDecimalsInMm
            copySettingsPaperSizeCustomView.spinModel = sliderModelComponent.createObject(copySettingsPaperSizeCustomView.controlModelList, {
                "objectName": objName,
                "decimals": decimals,
                "from": lower,
                "to": upper,
                "stepSize": step,
                "value": defVal
            });
            copySettingsPaperSizeCustomView.controlModelList.append(copySettingsPaperSizeCustomView.spinModel)

            rowList.append(spinBoxViewModel.createObject(rowList, {
                "controlModel": copySettingsPaperSizeCustomView.controlModelList.get(copySettingsPaperSizeCustomView.controlModelList.size() - 1),
                "imagePath" : imagePath,
                "infoText": buttonStrId
            }));
            return copySettingsPaperSizeCustomView.spinModel
        }

        // Method to try to update current x value from spin box, to cdm
        function tryUpdateXValueOnCdm(value)
        {
            let valueInDpiFixed = isSelectedUnitInInches ? UnitsUtils.inchToDpi(value) : UnitsUtils.mmToDpi(value)
            console.debug("copySettingsPaperSizeCustomView tryUpdateYValueOnCdm new value: " + valueInDpiFixed)
            ticketModel.data.dest.print.customMediaXFeedDimension = fixedValue(valueInDpiFixed, expectedDecimalsInDpi)
            _resourceStore.modify(ticketModel)
        }

        // Method to try to update current y value from spin box, to cdm
        function tryUpdateYValueOnCdm(value)
        {
            let valueInDpiFixed = isSelectedUnitInInches ? UnitsUtils.inchToDpi(value) : UnitsUtils.mmToDpi(value)
            console.debug("copySettingsPaperSizeCustomView tryUpdateYValueOnCdm new value: " + valueInDpiFixed)
            ticketModel.data.dest.print.customMediaYFeedDimension = fixedValue(valueInDpiFixed, expectedDecimalsInDpi)
            _resourceStore.modify(ticketModel)
        }

        function fixedValue(value, expectedDecimals)
        {
            return Number.parseFloat(value.toFixed(expectedDecimals))
        }

        function getValueOnMetricExpected(objectValue)
        {
            if (settingDependenciesArePrepared && objectValue)
            {
                let returnVal = 0
                if(isSelectedUnitInInches)
                {
                    returnVal = UnitsUtils.dpiToInch(objectValue)
                    return fixedValue(returnVal, expectedDecimalsInInches)
                }
                else // metric is on milimetters
                {
                    returnVal = UnitsUtils.dpiToMm(objectValue)
                    return fixedValue(returnVal, expectedDecimalsInMm)
                }
            }
            else
            {
                console.log("settingDependenciesArePrepared is false or objectValue is null")
                return 0
            }
        }

        function getStepValueOnMetricExpected(objectValue)
        {
            let returnVal = objectValue
            if (settingDependenciesArePrepared && objectValue)
            {
                if(isSelectedUnitInInches)
                {
                    returnVal = objectValue/100
                }
            }
            return returnVal
        }
        
        function getTrayImage(){

            let path = ""
            if(ticketModel)
            {
                if(ticketModel.data.dest.print.mediaSource == Glossary_1_MediaSourceId.MediaSourceId.tray_dash_1)
                {
                    console.debug("get Customt1")
                    path = _qmlUtils.getWorkflowResourceUrl("Customt1", "animations")
                }
                else
                {
                    console.debug("get CustomCass")
                    path = _qmlUtils.getWorkflowResourceUrl("CustomCass", "animations")
                }
            }
            
            return path
        }
    }
}