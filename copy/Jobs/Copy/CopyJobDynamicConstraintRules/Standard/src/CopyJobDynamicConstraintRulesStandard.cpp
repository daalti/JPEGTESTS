/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesStandard.cpp
 * @date   Mon, 11 Jul 2022 11:20:06 +0200
 * @brief  Component used to manage the Dynamic Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobDynamicConstraintRulesStandard.h"

#include "common_debug.h"
#include "CopyJobDynamicConstraintRulesStandard_TraceAutogen.h"
#include "ErrorManager.h"
#include "StringIds.h"
#include "CopyJobDynamicConstraintRulesStandardUwAdapter.h"
#include "ForceSets.h"
#include "typeMappers.h"

using ColorModes = dune::cdm::jobTicket_1::ColorModes;

// Factory method

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_Jobs_Copy_CopyJobDynamicConstraintRulesStandard)
{
    dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesStandard *instance = new dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesStandard(instanceName);
    assert(instance != nullptr);
    return static_cast<dune::framework::component::IComponent *>(instance);
}


namespace dune { namespace copy { namespace Jobs { namespace Copy {

// Constructor and destructor

CopyJobDynamicConstraintRulesStandard::CopyJobDynamicConstraintRulesStandard(const char *instanceName) :
    instanceName_(instanceName),
    interpreterEnvironment_(nullptr),
    uwAdapter_(nullptr)
{
    CHECKPOINTC("%s/CopyJobDynamicConstraintRulesStandard: constructed", instanceName_);
}

CopyJobDynamicConstraintRulesStandard::~CopyJobDynamicConstraintRulesStandard()
{
    if ( uwAdapter_ != nullptr )
    {
        delete uwAdapter_;
    }
}

// IComponent methods.

dune::framework::component::ComponentFlavorUid CopyJobDynamicConstraintRulesStandard::getComponentFlavorUid() const
{
    return GET_MODULE_UID(CopyJobDynamicConstraintRulesStandard);
}

const char *CopyJobDynamicConstraintRulesStandard::getComponentInstanceName() const
{
    return instanceName_;
}

void CopyJobDynamicConstraintRulesStandard::initialize(WorkingMode mode, const dune::framework::component::SystemServices *services)
{
    DUNE_UNUSED(mode);
    if(services == nullptr)
    {
        CHECKPOINTA("%s/CopyJobDynamicConstraintRulesStandard: initialize services_ value is null during initialize",
            getComponentInstanceName());
        assert_msg(false, "ERROR:: services_ value is null during initialize");
    }
    else
    {
        interpreterEnvironment_ = services->interpreterEnvironment_;
        configuration_ = getConfiguration(services->configurationService_);
        if (nullptr == configuration_)
        {
            CHECKPOINTA("%s/CopyJobDynamicConstraintRulesStandard: initialize configuration_ value is null during initialize",
                        getComponentInstanceName());
            assert_msg(false, "ERROR:: configuration_ value is null during initialize");
        }
    }
    CHECKPOINTC("%s/CopyJobDynamicConstraintRulesStandard: initialized", instanceName_);
}

void * CopyJobDynamicConstraintRulesStandard::getInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName)
{
    DUNE_UNUSED(portName);
    void *interfacePtr = nullptr;
    if (interfaceUid == GET_INTERFACE_UID(ICopyJobDynamicConstraintRules))
    {
        interfacePtr = static_cast<ICopyJobDynamicConstraintRules *>(this);
    }
    CHECKPOINTC("%s/CopyJobDynamicConstraintRulesStandard: getInterface %" PRIu32 " from port %s with addr %p", instanceName_, interfaceUid, portName, interfacePtr);
    return interfacePtr;
}

void CopyJobDynamicConstraintRulesStandard::setInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName, void *interfacePtr)
{
    if (interfacePtr != nullptr)
    {
        if (interfaceUid == GET_INTERFACE_UID(dune::copy::cdm::ICopyAdapter))
        {
            copyAdapter_ = static_cast<dune::copy::cdm::ICopyAdapter *>(interfacePtr);
            CHECKPOINTC("%s/CopyJobDynamicConstraintRulesStandard: setInterface ICopyAdapter to port %s with addr %p", instanceName_, portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::print::engine::constraints::IMediaConstraints))
        {
            mediaConstraints_ = static_cast<dune::print::engine::constraints::IMediaConstraints *>(interfacePtr);
            CHECKPOINTC("%s/CopyJobDynamicConstraintRulesStandard: setInterface IMediaConstraints to port %s with addr %p", instanceName_, portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(dune::scan::IScanConstraints))
        {
            scanConstraintsHelper_ = static_cast<dune::scan::IScanConstraints *>(interfacePtr);
            assert(scanConstraintsHelper_);
            
            CHECKPOINTA("%s/CopyJobDynamicConstraintRulesStandard: setInterface IScanConstraints to port %s with addr %p", instanceName_, portName, interfacePtr);
        }
        else if (interfaceUid == GET_INTERFACE_UID(IColorAccessControl))
        {
            CHECKPOINTB("CopyJobDynamicConstraintRulesStandard::setInterface: Received IColorAccessControl interface");
            colorAccessControlInst_ = static_cast<IColorAccessControl *>(interfacePtr);
        }

    }
}

void CopyJobDynamicConstraintRulesStandard::connected(dune::framework::component::IComponentManager *componentManager, std::future<void> &asyncCompletion)
{
    DUNE_UNUSED(componentManager);
    DUNE_UNUSED(asyncCompletion);
    
    // Initialize the underware adapter.
    if ( interpreterEnvironment_ != nullptr )
    {
        uwAdapter_ = new CopyJobDynamicConstraintRulesStandardUwAdapter(interpreterEnvironment_, instanceName_, this);
    }

    CHECKPOINTC("%s/CopyJobDynamicConstraintRulesStandard: connected", instanceName_);
}

void CopyJobDynamicConstraintRulesStandard::shutdown(ShutdownCause cause, std::future<void> &asyncCompletion)
{
    DUNE_UNUSED(cause);
    DUNE_UNUSED(asyncCompletion);   
    CHECKPOINTC("%s/CopyJobDynamicConstraintRulesStandard: shutdown", instanceName_);
}

std::unique_ptr<dune::copy::Jobs::copy::CopyJobDynamicConstraintRulesStandardConfigT> CopyJobDynamicConstraintRulesStandard::getConfiguration(dune::framework::resources::IConfigurationService *configurationService) const
{
    CHECKPOINTC("%s/CopyJobDynamicConstraintRulesStandard::getConfiguration:", getComponentInstanceName());

    assert(configurationService);
    dune::framework::resources::IConfigurationService::ConfigurationRawData rawConfiguration =
        configurationService->getConfiguration(GET_MODULE_UID(CopyJobDynamicConstraintRulesStandard), getComponentInstanceName());
    if (rawConfiguration.data && (rawConfiguration.size > 0))
    {
        flatbuffers::Verifier verifier(rawConfiguration.data.get(), rawConfiguration.size);
        assert(dune::copy::Jobs::copy::VerifyCopyJobDynamicConstraintRulesStandardConfigBuffer(verifier));
        return dune::copy::Jobs::copy::UnPackCopyJobDynamicConstraintRulesStandardConfig(rawConfiguration.data.get());
    }
    else
    {
        return std::unique_ptr<dune::copy::Jobs::copy::CopyJobDynamicConstraintRulesStandardConfigT>();
    }
}


bool CopyJobDynamicConstraintRulesStandard::checkAndApplyForceSets(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, 
    std::shared_ptr<ICopyJobTicket> ticket, 
    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> currentConstraintsGroup,
    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> staticConstraintsGroup)
{
    DUNE_UNUSED(staticConstraintsGroup);
    ForceSets::checkAndApplyForceSets( updatedJobTicketTable, ticket, currentConstraintsGroup, scanConstraintsHelper_);
    // Standard flavour always will return false, to avoid regenerate of constraints as are not expected
    return false;
}


/// @todo implement methods from ICopyJobDynamicConstraintRules here.
std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> CopyJobDynamicConstraintRulesStandard::getDynamicConstraints(
        std::shared_ptr<ICopyJobTicket> jobTicket, std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> staticConstraintsGroup,
        const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable)
{
    CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesStandard::getDynamicConstraints");
    DUNE_UNUSED(updatedJobTicketTable);

    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> constraintsGroup  = 
        std::make_shared<dune::framework::data::constraints::ConstraintsGroup>();


    if(checkIfConstraintIsSupported("dest/print/colorMode",jobTicket))
    {
        auto c = getPrintColorModeConstraints(jobTicket);
        constraintsGroup->set("dest/print/colorMode",c);
    }
    
    if(checkIfConstraintIsSupported("dest/print/mediaSource",jobTicket))
    {
        auto c = getMediaSourceConstraints(jobTicket);
        constraintsGroup->set("dest/print/mediaSource",c);
    }
    
    if(checkIfConstraintIsSupported("dest/print/mediaDestination",jobTicket))
    {
        auto c = getOutputPrintMediaConstraints(jobTicket);
        constraintsGroup->set("dest/print/mediaDestination",c);
    }
    
    if(checkIfConstraintIsSupported("dest/print/mediaSize",jobTicket))
    {
        auto c = getMediaSizeIdConstraints(jobTicket);
        constraintsGroup->set("dest/print/mediaSize",c);
    }
    
    if(checkIfConstraintIsSupported("dest/print/mediaType",jobTicket))
    {
        auto c = getMediaIdTypeConstraints(jobTicket);
        constraintsGroup->set("dest/print/mediaType",c);
    }
    
    if(checkIfConstraintIsSupported("dest/print/plexMode",jobTicket))
    {
        auto c = getPlexModeConstraints(jobTicket);
        constraintsGroup->set("dest/print/plexMode",c);
    }

    if(checkIfConstraintIsSupported("pipelineOptions/imageModifications/pagesPerSheet",jobTicket))
    {
        auto c = getPagesPerSheetConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/imageModifications/pagesPerSheet",c);
    }

    // currently we're using 'src/scan/colorMode' instead of 'dest/print/colorMode', we may change that later.
    if(checkIfConstraintIsSupported("src/scan/colorMode",jobTicket))
    {
        auto c = getPrintColorModeConstraints(jobTicket);
        constraintsGroup->set("src/scan/colorMode",c);
    }

    if(checkIfConstraintIsSupported("src/scan/mediaSize",jobTicket))
    {
        // change constratins for mixed size
        auto scanMediaSizeConstraints = staticConstraintsGroup->getConstraints("src/scan/mediaSize");
        auto c = getInputMediaSizeIdConstraints(jobTicket, scanMediaSizeConstraints);
        constraintsGroup->set("src/scan/mediaSize",c);
    }

    if(checkIfConstraintIsSupported("src/scan/scanCaptureMode",jobTicket))
    {
        auto c = getScanCaptureModeConstraints(jobTicket);
        constraintsGroup->set("src/scan/scanCaptureMode",c);
    }

    if(checkIfConstraintIsSupported("pipelineOptions/watermark/watermarkType",jobTicket))
    {
        auto c = getWatermarkTypeConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/watermark/watermarkType",c);
    }

    if(checkIfConstraintIsSupported("pipelineOptions/watermark/watermarkId",jobTicket))
    {
        auto c = getWatermarkIdConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/watermark/watermarkId",c);
    }

    if(checkIfConstraintIsSupported("pipelineOptions/watermark/textFont",jobTicket))
    {
        auto c = getWatermarkTextFontConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/watermark/textFont",c);
    }

    if(checkIfConstraintIsSupported("pipelineOptions/watermark/textSize",jobTicket))
    {
        auto c = getWatermarkTextSizeConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/watermark/textSize",c);
    }

    if(checkIfConstraintIsSupported("pipelineOptions/watermark/textColor",jobTicket))
    {
        auto c = getWatermarkTextColorConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/watermark/textColor",c);
    }

    if(checkIfConstraintIsSupported("pipelineOptions/watermark/onlyFirstPage",jobTicket))
    {
        auto c = getWatermarkOnlyFirstPageConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/watermark/onlyFirstPage",c);
    }

    if(checkIfConstraintIsSupported("pipelineOptions/watermark/rotate45",jobTicket))
    {
        auto c = getWatermarkRotate45Constraints(jobTicket);
        constraintsGroup->set("pipelineOptions/watermark/rotate45",c);
    }

    if(checkIfConstraintIsSupported("pipelineOptions/watermark/backgroundColor",jobTicket))
    {
        auto c = getWatermarkBackgroundColorConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/watermark/backgroundColor",c);
    }

    if(checkIfConstraintIsSupported("pipelineOptions/watermark/backgroundPattern",jobTicket))
    {
        auto c = getWatermarkBackgroundPatternConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/watermark/backgroundPattern",c);
    }

    if(checkIfConstraintIsSupported("pipelineOptions/watermark/darkness",jobTicket))
    {
        auto c = getWatermarkDarknessConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/watermark/darkness",c);
    }

    if(checkIfConstraintIsSupported("pipelineOptions/scaling/scaleSelection",jobTicket))
    {
        auto c = getScaleSelectionConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/scaling/scaleSelection",c);
    }

    if(checkIfConstraintIsSupported("stampLocation",jobTicket))
    {
        auto c = getStampLocationConstraints(dune::cdm::overlay_1::StampLocation::topLeft, jobTicket);
        constraintsGroup->set("pipelineOptions/stampTopLeft/locationId", c);
        c = getStampLocationConstraints(dune::cdm::overlay_1::StampLocation::topCenter, jobTicket);
        constraintsGroup->set("pipelineOptions/stampTopCenter/locationId", c);
        c = getStampLocationConstraints(dune::cdm::overlay_1::StampLocation::topRight, jobTicket);
        constraintsGroup->set("pipelineOptions/stampTopRight/locationId", c);
        c = getStampLocationConstraints(dune::cdm::overlay_1::StampLocation::bottomLeft, jobTicket);
        constraintsGroup->set("pipelineOptions/stampBottomLeft/locationId", c);
        c = getStampLocationConstraints(dune::cdm::overlay_1::StampLocation::bottomCenter, jobTicket);
        constraintsGroup->set("pipelineOptions/stampBottomCenter/locationId", c);
        c = getStampLocationConstraints(dune::cdm::overlay_1::StampLocation::bottomRight, jobTicket);
        constraintsGroup->set("pipelineOptions/stampBottomRight/locationId", c);
    }

    if(checkIfConstraintIsSupported("stampPolicy",jobTicket))
    {
        auto c = getStampPolicyConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/stampTopLeft/policy", c);
        constraintsGroup->set("pipelineOptions/stampTopCenter/policy", c);
        constraintsGroup->set("pipelineOptions/stampTopRight/policy", c);
        constraintsGroup->set("pipelineOptions/stampBottomLeft/policy", c);
        constraintsGroup->set("pipelineOptions/stampBottomCenter/policy", c);
        constraintsGroup->set("pipelineOptions/stampBottomRight/policy", c);
    }

    if(checkIfConstraintIsSupported("stampType",jobTicket))
    {
        auto c = getStampTypeConstraints(dune::cdm::overlay_1::StampLocation::topLeft, jobTicket, jobTicket->getIntent()->getStampTopLeft().stampPolicy);
        constraintsGroup->set("pipelineOptions/stampTopLeft/stampContent/stampId", c);
        c = getStampTypeConstraints(dune::cdm::overlay_1::StampLocation::topCenter, jobTicket, jobTicket->getIntent()->getStampTopCenter().stampPolicy);
        constraintsGroup->set("pipelineOptions/stampTopCenter/stampContent/stampId", c);
        c = getStampTypeConstraints(dune::cdm::overlay_1::StampLocation::topRight, jobTicket, jobTicket->getIntent()->getStampTopRight().stampPolicy);
        constraintsGroup->set("pipelineOptions/stampTopRight/stampContent/stampId", c);
        c = getStampTypeConstraints(dune::cdm::overlay_1::StampLocation::bottomLeft, jobTicket, jobTicket->getIntent()->getStampBottomLeft().stampPolicy);
        constraintsGroup->set("pipelineOptions/stampBottomLeft/stampContent/stampId", c);
        c = getStampTypeConstraints(dune::cdm::overlay_1::StampLocation::bottomCenter, jobTicket, jobTicket->getIntent()->getStampBottomCenter().stampPolicy);
        constraintsGroup->set("pipelineOptions/stampBottomCenter/stampContent/stampId", c);
        c = getStampTypeConstraints(dune::cdm::overlay_1::StampLocation::bottomRight, jobTicket, jobTicket->getIntent()->getStampBottomRight().stampPolicy);
        constraintsGroup->set("pipelineOptions/stampBottomRight/stampContent/stampId", c);
    }

    if(checkIfConstraintIsSupported("stampTextColor",jobTicket))
    {
        auto c = getStampTextColorConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/stampTopLeft/textColor", c);
        constraintsGroup->set("pipelineOptions/stampTopCenter/textColor", c);
        constraintsGroup->set("pipelineOptions/stampTopRight/textColor", c);
        constraintsGroup->set("pipelineOptions/stampBottomLeft/textColor", c);
        constraintsGroup->set("pipelineOptions/stampBottomCenter/textColor", c);
        constraintsGroup->set("pipelineOptions/stampBottomRight/textColor", c);
    }

    if(checkIfConstraintIsSupported("stampTextFont",jobTicket))
    {
        auto c = getStampTextFontConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/stampTopLeft/textFont", c);
        constraintsGroup->set("pipelineOptions/stampTopCenter/textFont", c);
        constraintsGroup->set("pipelineOptions/stampTopRight/textFont", c);
        constraintsGroup->set("pipelineOptions/stampBottomLeft/textFont", c);
        constraintsGroup->set("pipelineOptions/stampBottomCenter/textFont", c);
        constraintsGroup->set("pipelineOptions/stampBottomRight/textFont", c);
    }

    if(checkIfConstraintIsSupported("stampTextSize",jobTicket))
    {
        auto c = getStampTextSizeConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/stampTopLeft/textSize", c);
        constraintsGroup->set("pipelineOptions/stampTopCenter/textSize", c);
        constraintsGroup->set("pipelineOptions/stampTopRight/textSize", c);
        constraintsGroup->set("pipelineOptions/stampBottomLeft/textSize", c);
        constraintsGroup->set("pipelineOptions/stampBottomCenter/textSize", c);
        constraintsGroup->set("pipelineOptions/stampBottomRight/textSize", c);
    }

    if(checkIfConstraintIsSupported("stampPageNumberingStyle",jobTicket))
    {
        auto c = getStampPageNumberingStyleConstraints(jobTicket);
        constraintsGroup->set("pipelineOptions/stampTopLeft/pageNumberingStyle", c);
        constraintsGroup->set("pipelineOptions/stampTopCenter/pageNumberingStyle", c);
        constraintsGroup->set("pipelineOptions/stampTopRight/pageNumberingStyle", c);
        constraintsGroup->set("pipelineOptions/stampBottomLeft/pageNumberingStyle", c);
        constraintsGroup->set("pipelineOptions/stampBottomCenter/pageNumberingStyle", c);
        constraintsGroup->set("pipelineOptions/stampBottomRight/pageNumberingStyle", c);
    }

    if(checkIfConstraintIsSupported("dest/print/customMediaXFeedDimension",jobTicket))
    {
        if(mediaConstraints_ != nullptr)
        {
            CHECKPOINTB("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesStandard::getDynamicConstraints : go getCustomMediaXFeedDimension()");
            auto c = getCustomMediaXFeedDimension(mediaConstraints_);
            constraintsGroup->set("dest/print/customMediaXFeedDimension",c);
        }
    }

    if(checkIfConstraintIsSupported("dest/print/customMediaYFeedDimension",jobTicket))
    {
        if(mediaConstraints_ != nullptr)
        {
            CHECKPOINTB("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesStandard::getDynamicConstraints : go getCustomMediaYFeedDimension()");
            auto c = getCustomMediaYFeedDimension(mediaConstraints_);
            constraintsGroup->set("dest/print/customMediaYFeedDimension",c);
        }
    }

    if(checkIfConstraintIsSupported("src/scan/contentOrientation",jobTicket))
    {
        updateScanContentOrientationConstraints(staticConstraintsGroup, jobTicket);   
    }
    // "src/scan/colorMode" constraints can be changed by "copy/v1/configuration/colorCopyEnabled" value.
    CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobDynamicConstraintRulesStandard::getDynamicConstraints : getColorCopyEnabled() %d", copyAdapter_->getColorCopyEnabled());
    return constraintsGroup;
}

void CopyJobDynamicConstraintRulesStandard::updateWithJobDynamicConstraints(std::shared_ptr<ICopyJobTicket> jobTicket, 
                                                                            std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> constraintsGroup)
{
    if (!jobTicket || !constraintsGroup) {
        CHECKPOINTA("CopyJobDynamicConstraintRulesStandard::updateWithJobDynamicConstraints Error: Null jobTicket or constraintsGroup");
        return;
    }

    CHECKPOINTA("CopyJobDynamicConstraintRulesStandard::updateWithJobDynamicConstraints Enter, job state %d",(int)jobTicket->getState());
    // Add the Blocked settings between pages from Job Service
    std::vector<std::string> blockedSettingsBetweenPages;
    for(const auto &blockedSetting : configuration_->blockedSettingsBetweenPages)
    {
        CHECKPOINTC("CopyJobDynamicConstraintRulesStandard::updateWithJobDynamicConstraints blocked setting: %s", blockedSetting.c_str());
        blockedSettingsBetweenPages.push_back(blockedSetting);
    }
    std::vector<std::pair<std::string, std::string>> vectorMapStringIdForSettings;
    for(const auto &stringMap : configuration_->vectorMapStringIdForSettings)
    {
        for(const auto &stringId : stringMap->vectorStringId)
        {
            vectorMapStringIdForSettings.push_back(std::make_pair(stringMap->settingName, stringId));
        } 
    }
    if(scanConstraintsHelper_)
    {
        scanConstraintsHelper_->updateWithJobDynamicConstraints(jobTicket, constraintsGroup, blockedSettingsBetweenPages, vectorMapStringIdForSettings);
    }
    CHECKPOINTA("CopyJobDynamicConstraintRulesStandard::updateWithJobDynamicConstraints Exit");
}

bool CopyJobDynamicConstraintRulesStandard::hasColorPermission(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    bool hasPermission =  CopyJobConstraintRules::hasColorPermission(jobTicket);
    if( hasPermission &&  copyAdapter_ != nullptr)
    {
        hasPermission =  copyAdapter_->getColorCopyEnabled();
    }
    CHECKPOINTB("CopyJobDynamicConstraintRulesStandard::hasColorPermission: %d", (int)hasPermission);
    return hasPermission;
}

bool CopyJobDynamicConstraintRulesStandard::isColorRestricted(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    ColorAccess colorAccess = ColorAccess::ENABLED; // Default to enabled, if no access control is available.
    bool colorRestricted = false; // Default to not restricted.
    if (colorAccessControlInst_ != nullptr)
    {
        CHECKPOINTB("CopyJobDynamicConstraintRulesStandard::isColorRestricted: checking color access control");
        ColorAccess colorAccess = colorAccessControlInst_->getColorAccess();
        switch (colorAccess)
        {
            case ColorAccess::ENABLED:
                CHECKPOINTB("CopyJobDynamicConstraintRulesStandard::isColorRestricted: color access is ENABLED");
                colorRestricted=false; // Not restricted, color access is enabled.
                break;
            case ColorAccess::DISABLED:
                CHECKPOINTB("CopyJobDynamicConstraintRulesStandard::isColorRestricted: color access is DISABLED");
                colorRestricted=true; // Restricted, color access is disabled.
                break;
            default:
                CHECKPOINTA("CopyJobDynamicConstraintRulesStandard::isColorRestricted: color access is UNKNOWN");
                break;
        }

    }
    else
    {
        CHECKPOINTA("CopyJobDynamicConstraintRulesStandard::isColorRestricted: color access control not available");
        return false; // No color access control, so not restricted.
    }
    jobTicket->setRestrictColorPrint(colorRestricted); // Update the copy ticket with the color restriction status.
    return colorRestricted;   
}


// This method has a different signiture than the LargeFormat component. It is more in-line with the standard flavor approach.
bool CopyJobDynamicConstraintRulesStandard::checkIfConstraintIsSupported(std::string cdmPathName,std::shared_ptr<ICopyJobTicket> jobTicket)
{
     bool retVal = true;

    if(jobTicket->getConstraints())
    {
        // dest.print properties
        if(cdmPathName == "dest/print/printMargins" && jobTicket->getConstraints()->getCopyMargins().size() ==0 )
            retVal = false;
        else if(cdmPathName == "dest/print/plexMode" && jobTicket->getConstraints()->getPlexMode().size() ==0 )
            retVal = false;
        else if(cdmPathName == "dest/print/duplexBinding" && jobTicket->getConstraints()->getPlexBinding().size() ==0 )
            retVal = false;
        else if(cdmPathName == "dest/print/collate" && jobTicket->getConstraints()->getCollate().size() ==0 )
            retVal = false;
        else if(cdmPathName == "dest/print/printQuality" && jobTicket->getConstraints()->getPrintQuality().size() ==0 )
            retVal = false;
        else if(cdmPathName == "dest/print/mediaDestination" && 
                    ((jobTicket->getConstraints()->getMediaDestinations().size() ==0) || (true == jobTicket->IsInstalledPageBasedFinisherDevice())))
            retVal = false;
        // Workaround check to not broke functionality between products
        else if(cdmPathName == "dest/print/mediaSource" &&
                // Check for printers without dependency of type and size, that check directly source value on csf file
                !(jobTicket->getConstraints()->getMediaPrintSupportedSource().size() > 0 ||
                // Check dependency of printers that source evaluations depends of size and type supported check too
                    (jobTicket->getConstraints()->getMediaSupportedSizes().size() > 0 &&
                     jobTicket->getConstraints()->getMediaSupportedTypes().size() > 0)))
            retVal = false;
        else if(cdmPathName == "dest/print/colorMode") // for now, we're using the 'src/scan/colorMode'; this may change in the future.
            retVal = false;
        else if(cdmPathName == "src/scan/scanCaptureMode" && jobTicket->getConstraints()->getScanCaptureModes().size() ==0 )
            retVal = false;
        else if(cdmPathName == "src/scan/contentOrientation" && false == jobTicket->IsInstalledPageBasedFinisherDevice())    
            retVal = false;
        else if(cdmPathName == "stampLocation" && jobTicket->getConstraints()->getStampLocation().size() == 0)    
            retVal = false;
        else if(cdmPathName == "stampPolicy" && jobTicket->getConstraints()->getStampPolicy().size() == 0)    
            retVal = false;
        else if(cdmPathName == "stampType" && jobTicket->getConstraints()->getStampType().size() == 0)    
            retVal = false;
        else if(cdmPathName == "stampTextColor" && jobTicket->getConstraints()->getStampTextColor().size() == 0)    
            retVal = false;
        else if(cdmPathName == "stampTextFont" && jobTicket->getConstraints()->getStampTextFont().size() == 0)    
            retVal = false;
        else if(cdmPathName == "stampTextSize" && jobTicket->getConstraints()->getStampTextSize().size() == 0)    
            retVal = false;
        else if(cdmPathName == "stampPageNumberingStyle" && jobTicket->getConstraints()->getStampPageNumberingStyle().size() == 0)    
            retVal = false;
    }

    CHECKPOINTC("CopyJobDynamicConstraintRulesStandard::checkIfConstraintIsSupported %s %d", cdmPathName.c_str(), (int)retVal);

    return retVal;
}


}}}}  // namespace dune::copy::Jobs::Copy
