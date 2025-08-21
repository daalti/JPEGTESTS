import QtQuick 2.15
import spiceGuiCore 1.0
import spiceux 1.0
import spiceuxComponents 1.0
import spiceuxLayouts 1.0
import spiceuxTemplates 1.0
import QtQuick.Layouts 1.15
import QtQml.Models 2.15

Rectangle {

    id: root
    objectName: "CopyQuickWidget"
    property QtObject copyController: QuickCopyController {};
    property ISpiceModel defaultSettings: null;
    
    property var widgetSummary: _quickCopyWidgetSummaryList;
    property bool multiWidget: false  // Added property declaration
    
    property bool widgetSize: Global.breakpoint > Global.BreakPoint.S ? true : false 
    property bool previewRequired: copyController.inputMediaSource=="mdf" ?true :false //Preview required will be updated once we get the end point for this
    color: ColorConstants.box2B
    border.color: ColorConstants.colorStroke2
    radius: SpiceCornerRadiusConstants.cr3
    //This onWidgetSizeChanged is used to reload widget sizein runtime using CTRL+SHIFT+(S|L|M)
    onWidgetSizeChanged: {
        if (Global.breakpoint === Global.BreakPoint.XL){
            copyWidgetLoader.sourceComponent = Qt.createComponent("qrc:/QuickCopy/QuickCopyWidgetXL.qml")
        }
        else if (Global.breakpoint > Global.BreakPoint.S){
            copyWidgetLoader.sourceComponent = Qt.createComponent("qrc:/QuickCopy/QuickCopyWidgetM.qml")
        }
        else{
            copyWidgetLoader.sourceComponent = Qt.createComponent("qrc:/QuickCopy/QuickCopyWidgetS.qml")
        }
        console.log("Rectangle width",root.width)
        console.log("Rectangle height",root.height)
        console.log("Rectangle Parent width",parent.width)
        console.log("Rectangle Parent height",parent.width)
    }

    width: multiWidget ? Global.BreakPoint.S === Global.breakpoint ? 34.75*Global.rem : Global.BreakPoint.XS === Global.breakpoint ? 23.16*Global.rem : 18*Global.rem : Global.BreakPoint.S === Global.breakpoint ? 38*Global.rem : Global.BreakPoint.XS === Global.breakpoint ? 24.6*Global.rem : 40*Global.rem//18
    height: Global.BreakPoint.S === Global.breakpoint ? 6*Global.rem : Global.BreakPoint.XS === Global.breakpoint ? 6*Global.rem : Global.BreakPoint.M === Global.breakpoint ? 33.79*Global.rem :Global.BreakPoint.L === Global.breakpoint ? 32.82*Global.rem : 43*Global.rem
 
    
    Loader {
        anchors.top: root.top
        width: root.width
        height: root.height
        id: copyWidgetLoader

        onLoaded: {
            copyWidgetLoader.item.widgetProperty = Qt.binding(function(){return root.copyController.widgetProperty})
            copyWidgetLoader.item.widgetInfoText = Qt.binding(function(){return root.copyController.widgetInfoText})
            copyWidgetLoader.item.numberOfCopiesMax = Qt.binding(function(){return root.copyController.numberOfCopiesMax})
            copyWidgetLoader.item.numberOfCopiesMin = Qt.binding(function(){return root.copyController.numberOfCopiesMin})
            copyWidgetLoader.item.copyButtonEnabled = Qt.binding(function(){return root.copyController.copyEnabled})
            copyWidgetLoader.item.copyClicked.connect(function(val)
            {
                console.log("Copy Widget, Copy Button Clicked, ncopies:" + val);
                if(previewRequired && widgetSize)
                {
                    copyController.startApplication(val,true)
                }
                else{
                    copyController.numCopies = val
                    copyController.startCopy()
                }

            });
            copyWidgetLoader.item.settingClicked.connect(function(val){
                console.log("Copy Widget, Options Button Clicked, ncopies:" + val);
                copyController.startApplication(val, false)
            })
            copyWidgetLoader.item.copybuttonConstrained = Qt.binding(function(){return (copyController.inputMediaSource=="mdf" ? !root.copyController.isScanMediaLoaded : false)})
        }
    }

    Component.onCompleted: {
        console.log(" onCompleted called")
        console.log("Copy widget summary", widgetSummary)
        
        if (Global.breakpoint === Global.BreakPoint.XL){
            root.parent.backgroundColor = ColorConstants.box2B
            copyWidgetLoader.sourceComponent = Qt.createComponent("qrc:/QuickCopy/QuickCopyWidgetXL.qml")
            
            if(copyWidgetLoader.item.numberOfCopies != null){
                root.parent.clicked.connect(function(){
                    if (copyWidgetLoader.item.isAnaSignInRequired == false)
                    {
                        console.log("Copy Widget, Widget are Clicked, ncopies:", copyWidgetLoader.item.numberOfCopies);
                        copyController.startApplication(copyWidgetLoader.item.numberOfCopies,false)
                    }

                });
            }
        }
        else if (Global.breakpoint > Global.BreakPoint.S){
            root.parent.backgroundColor = ColorConstants.neutral018
            copyWidgetLoader.sourceComponent = Qt.createComponent("qrc:/QuickCopy/QuickCopyWidgetM.qml")
        }
        else{
            root.parent.backgroundColor = ColorConstants.neutral024
            copyWidgetLoader.sourceComponent = Qt.createComponent("qrc:/QuickCopy/QuickCopyWidgetS.qml")
            copyController.subscribeToPrinterStatus()
        }
        copyController.subscribeScannerStatus()
        let component = Qt.createComponent("qrc:/QuickCopy/AsyncOperationWrapper.qml")
        let future = component.createObject(root, {"asyncOperation":()=> _resourceStore.get("/cdm/jobTicket/v1/configuration/defaults/copy")})

        future.resolved.connect((future) => {
            console.log("Defaults Request Success");
            root.defaultSettings = future.get()
            copyController.setPropertiesOfWidget(root.defaultSettings, widgetSummary);
            copyWidgetLoader.sourceComponent = undefined;
            if (Global.breakpoint === Global.BreakPoint.XL) {
                copyWidgetLoader.sourceComponent = Qt.createComponent("qrc:/QuickCopy/QuickCopyWidgetXL.qml");
            } else if (Global.breakpoint > Global.BreakPoint.S) {
                copyWidgetLoader.sourceComponent = Qt.createComponent("qrc:/QuickCopy/QuickCopyWidgetM.qml");
            } else {
                copyWidgetLoader.sourceComponent = Qt.createComponent("qrc:/QuickCopy/QuickCopyWidgetS.qml");
            }
        });

        future.rejected.connect((future) => {
            console.assert(false, "ERROR request copy defaults Fail error", future.error);
        });
    }
    
    Component.onDestruction: {
        copyController.unsubscribeScannerStatus()
        copyController.unsubscribeToPrinterStatus()
    }

}
