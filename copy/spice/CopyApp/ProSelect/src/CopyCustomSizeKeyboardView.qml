import QtQuick 2.15
import QtQuick.Layouts 1.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import spiceuxToastSystem 1.0

SpiceKeyboard {
    id: copyCustomSizeKeyboard
    objectName: "copyCustomSizeKeyboardView"
    type: SpiceKeyboard.Type.FullNumeric
    property ISpiceModel ticketModel: null;

    property int minValue: 0
    property int maxValue: 0
    property int xScaleMin: 0
    property int xScaleMax: 0
    property int yScaleMin: 0
    property int yScaleMax: 0
    supportPopOnClose: true

    function setMinMaxValue()
    {
        let validatorForXScale = _stateMachine.copyControllerfunctions.findValidatorForConstraint("pipelineOptions/scaling/xScalePercent");
        if(validatorForXScale != null)
        {
            xScaleMin = validatorForXScale.data.min.data.value;
            xScaleMax = validatorForXScale.data.max.data.value;
        }
        else
        {
            console.error("validatorForXScale is null.")
            xScaleMin = 25;
            xScaleMax = 400;
        }


        let validatorForYScale = _stateMachine.copyControllerfunctions.findValidatorForConstraint("pipelineOptions/scaling/yScalePercent");

        if(validatorForYScale != null)
        {
            yScaleMin = validatorForYScale.data.min.data.value;
            yScaleMax = validatorForYScale.data.max.data.value;
        }
        else
        {
            console.error("validatorForYScale is null.")
            yScaleMin = 25;
            yScaleMax = 400;
        }

        minValue = xScaleMin <= yScaleMin ? xScaleMin : yScaleMin;
        maxValue = xScaleMax >= yScaleMax ? xScaleMax : yScaleMax;

        console.debug("minValue is " + minValue);
        console.debug("maxValue is " + maxValue);

    }

    onTextSet: function(text) {
        let resizeVal = parseInt(text);

        console.debug("text is " + resizeVal)

        setMinMaxValue();

        if (resizeVal < minValue)
        {
            resizeVal = minValue
        }
        else if (resizeVal > maxValue)
        {
            resizeVal = maxValue
        }


        if(resizeVal >= minValue && resizeVal <= maxValue)
        {
            ticketModel.data.pipelineOptions.scaling.scaleToFitEnabled = Glossary_1_FeatureEnabled.FeatureEnabled.false_
            ticketModel.data.pipelineOptions.scaling.xScalePercent = resizeVal
            ticketModel.data.pipelineOptions.scaling.yScalePercent = resizeVal
            _resourceStore.modify(ticketModel)
            _stack.pop()
        }
        
    }

}
