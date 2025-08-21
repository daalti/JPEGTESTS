import QtQml 2.15
import QtQuick 2.15

import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0

SettingsComboBoxViewModel {
    id: root
    objectName: root.menuNode ? (root.menuNode.id + "MenuComboBox") : "MenuComboBox"

    property var menuNode: null
    node: menuNode

    property string foldingStyleIdProperty: "dest/print/foldingStyleId"
    property string mediaDestinationIdProperty: "dest/print/mediaDestination"
    property string finisherConfigurationUrl: "/cdm/media/v1/finisherConfiguration"

    property ISpiceModel jobTicketModel: null;
    property ISpiceModel jobTicketConstraintsModel: null
    property ISpiceModel finisherConfigurationModel: null

    function isFolderStyleConstrained()
    {
        let isFolderConstrained = false;

        let validator = _stateMachine.controller.findValidatorForConstraint(foldingStyleIdProperty);

        if( validator.disabled && validator.disabled.value == Glossary_1_FeatureEnabled.FeatureEnabled.true_ )
        {
            isFolderConstrained = true
            root.controlModel.constrainedMessage = _qmlUtils.createSpiceLoc(root, {"text": validator.disabled.message});
        }

        return isFolderConstrained;
    }

    function isFoldingStyleVisible()
    {
        let result = false
        var mediaDestinationIdList = []

        if (root.finisherConfigurationModel && root.finisherConfigurationModel.data.folders)
        {
            let foldersList = root.finisherConfigurationModel.data.folders

            for(let i = 0; i < foldersList.count; ++i)
            {
                let currentFolder = foldersList.get(i)

                let folderString = folderEnumToString(currentFolder.mediaDestinationId);
                mediaDestinationIdList.push(folderString)
            }

            result = isFoldingStyleEnabled(mediaDestinationIdList)
        }
        else
        {
            console.log("COPY_SETTINGS_FOLDING_STYLE: finisher configuration model is null")
        }

        return result;
    }

    function folderEnumToString( mediaDestinationEnum )
    {
        let value = "";

        switch(Number(mediaDestinationEnum))
        {
            case Glossary_1_MediaDestinationId.MediaDestinationId.folder_dash_1:
                value = "folder-1";
                break;
            case Glossary_1_MediaDestinationId.MediaDestinationId.folder_dash_2:
                value = "folder-2";
                break;
            case Glossary_1_MediaDestinationId.MediaDestinationId.folder_dash_3:
                value = "folder-3";
                break;
            case Glossary_1_MediaDestinationId.MediaDestinationId.folder_dash_4:
                value = "folder-4";
                break;
        }

        return value;
    }

    function isFoldingStyleEnabled(mediaDestinationIdList) 
    {
        let isEnabled = false;
        let validator = _stateMachine.controller.findValidatorForConstraint(mediaDestinationIdProperty);
  
        if(jobTicketConstraintsModel !== null && validator != null && validator.options.count > 0)
        {
            let mediaDestinationOptions = validator.options

            for(var i = 0 ; i < mediaDestinationOptions.count; i++)
            {
                let currentMediaDestination = mediaDestinationOptions.get(i)

                for(var j = 0; j < mediaDestinationIdList.length; j++)
                {
                    if(currentMediaDestination.seValue == mediaDestinationIdList[j])
                    {
                        if(!(currentMediaDestination.disabled in currentMediaDestination) || currentMediaDestination.disabled == Glossary_1_FeatureEnabled.FeatureEnabled.false_)
                        {
                            isEnabled = true;
                        }
                    }
                }
            }
        }
        else
        {
            console.log("COPY_SETTINGS_FOLDING_STYLE: job ticket constraints model is null")
        }

        return isEnabled;
    }

    function generateFoldingStyleNamesFromList(foldingStyleIdList)
    {
        let foldingStyleNames = [...foldingStyleIdList]

        if (root.finisherConfigurationModel && root.finisherConfigurationModel.data.folders)
        {
            for(let i = 0; i < root.finisherConfigurationModel.data.folders.count; ++i)
            {
                let currentFolder = root.finisherConfigurationModel.data.folders.get(i)
                let supportedFoldingStyles = currentFolder.standardFoldingStylesSupported

                for(let j = 0; j < supportedFoldingStyles.count; ++j)
                {
                    let foldingStyleIndex = foldingStyleNames.findIndex(name => name == supportedFoldingStyles.get(j).foldingStyleId)
                    if (foldingStyleIndex !== -1) { foldingStyleNames[foldingStyleIndex] = supportedFoldingStyles.get(j).foldingStyleName }
                }
            }
        }
        else
        {
            console.log("COPY_SETTINGS_FOLDING_STYLE: finisher configuration model is null")
        }

        return foldingStyleNames
    }

    function generateFoldingStyleValues() 
    {
        if (root.jobTicketConstraintsModel)
        {
            let validatorList = jobTicketConstraintsModel.data.validators 
            for(let i = 0; i < validatorList.count; ++i)
            {
                let currentValidator = validatorList.get(i)
                if (currentValidator.propertyPointer === root.foldingStyleIdProperty)
                {
                    let foldingStyleIdList = currentValidator.options.objectList().map(option => option.iValue)
                    let foldingStyleNameList = generateFoldingStyleNamesFromList(foldingStyleIdList)

                    for(let j = 0; j < foldingStyleNameList.length; ++j) 
                    {
                        let comboBoxComp = Qt.createComponent("qrc:/components/models/ComboBoxModel.qml")
                        let foldingStyleItem = comboBoxComp.createObject(root.controlModel.model, {
                                                                                                    "objectName": "foldingStyleComboBox" + foldingStyleIdList[j],
                                                                                                    "textObject.text": foldingStyleNameList[j],
                                                                                                    "value": foldingStyleIdList[j]
                                                                                                  })
                        root.controlModel.model.append(foldingStyleItem)
                    }

                    // Signal when selected value changes.
                    root.controlModel.selected.connect(updateFoldingStyleValueWithNewFoldingStyle)
                    root.controlModel.currentIndex = foldingStyleIdList.findIndex(foldingStyleId => foldingStyleId === root.jobTicketModel.data.dest.print.foldingStyleId);
                    break
                }
            }
        }
        else
        {
            console.log("COPY_SETTINGS_FOLDING_STYLE: job ticket constraints model is null")
        }
    }

    function updateFoldingStyleValueWithNewFoldingStyle(foldingStyleModelIndex)
    {
        if (root.jobTicketModel)
        {
            let newFolderStyleId = root.controlModel.model.get(foldingStyleModelIndex).value
            let currentFolderStyleId = getValueFromModelPath(root.jobTicketModel.data, root.foldingStyleIdProperty)

            if (currentFolderStyleId !== newFolderStyleId)
            {
                setValueFromModelPath(root.jobTicketModel.data, root.foldingStyleIdProperty, newFolderStyleId)
                _resourceStore.modify(root.jobTicketModel)
            }
            else
            {
                console.log("COPY_SETTINGS_FOLDING_STYLE: folding style id already saved")
            }
        }
        else
        {
            console.log("COPY_SETTINGS_FOLDING_STYLE: job ticket model is null")
        }
    }

    //This method provides a flexible and recursive way to access nested property values
    function getValueFromModelPath(jobTicketModelData, propertyPath)
    {
        if (!propertyPath)
        { 
            return jobTicketModelData
        }
        else
        {
            const properties = propertyPath.split('/')
            if (properties.length === 1)
            {
                // If the propertyPath has only one component, return the value of that property in the jobTicketModelData
                return jobTicketModelData[propertyPath]
            }
            else
            {
                // If the propertyPath has more than one component, recursively call this function with the first component removed from the propertyPath
                return getValueFromModelPath(jobTicketModelData[properties.shift()], properties.join('/'))
            }
        }
    }

    // This method provides a flexible and recursive way to set nested property values
    function setValueFromModelPath(jobTicketModelData, propertyPath, newFolderStyleIdValue)
    {
        if (!propertyPath)
        { 
            return
        }
        else
        {
            const properties = propertyPath.split('/')
            if (properties.length === 1)
            {
                // If the propertyPath has only one component, set the newFolderStyleIdValue of that property in the jobTicketModelData
                jobTicketModelData[propertyPath] = newFolderStyleIdValue
                return
            }
            else
            {
                // If the propertyPath has more than one component, recursively call this function with the first component removed from the propertyPath
                return setValueFromModelPath(jobTicketModelData[properties.shift()], properties.join('/'), newFolderStyleIdValue)
            }
        }
    }

    function onModelsRetrieved()
    {
        if(root.jobTicketModel && root.jobTicketConstraintsModel && root.finisherConfigurationModel)
        {
            clearControlModelData()
            generateFoldingStyleValues()
        }
    }

    function clearControlModelData(autoDestroy = true)
    {
        if (root.controlModel)
        {
            root.controlModel.selected.disconnect(updateFoldingStyleValueWithNewFoldingStyle)

            if (autoDestroy)
            {
                for(let i = 0; i < root.controlModel.count; ++i) { root.controlModel.model.get(i).destroy() }
            }

            root.controlModel.model.clear()
        }
    }

    Component.onCompleted:
    {
        jobTicketModel = _stateMachine.ticketModel
        jobTicketConstraintsModel = _stateMachine.constraintModel

        let finisherConfigurationFuture = _resourceStore.get(root.finisherConfigurationUrl)
        finisherConfigurationFuture.resolved.connect((future) => { root.finisherConfigurationModel = future.get(); onModelsRetrieved() })
        finisherConfigurationFuture.rejected.connect((future) => { console.log("COPY_SETTINGS_FOLDING_STYLE: finisher configuration info retrieve failed with error " + future.error) })

        root.controlModel.visible = Qt.binding(function() { return isFoldingStyleVisible() })
        root.controlModel.constrained = Qt.binding(function() { return isFoldingStyleVisible() && isFolderStyleConstrained() })
        root.controlModel.textObject.stringId = Qt.binding(function() { return root.menuNode ? root.menuNode.titleId : StringIds.cDefaultFoldingStyle })
    }

    Component.onDestruction:
    {
        clearControlModelData(false)
    }
}
