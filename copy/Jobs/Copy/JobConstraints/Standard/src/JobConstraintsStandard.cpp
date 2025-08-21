/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobConstraintsStandard.cpp
 * @date   Tue, 05 Jul 2022 08:29:10 +0200
 * @brief  Component used to manage the Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "JobConstraintsStandard.h"
#include "StringIds.h"

#include "common_debug.h"
#include "JobConstraintsStandard_TraceAutogen.h"
#include "ErrorManager.h"
#include "JobConstraintsStandardUwAdapter.h"
#include "typeMappers.h"
#include "CopyJobStaticConstraintRules.h"

// Factory method

EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_Jobs_Copy_JobConstraintsStandard)
{
    dune::copy::Jobs::Copy::JobConstraintsStandard *instance = new dune::copy::Jobs::Copy::JobConstraintsStandard(instanceName);
    assert(instance != nullptr);
    return static_cast<dune::framework::component::IComponent *>(instance);
}


namespace dune { namespace copy { namespace Jobs { namespace Copy {

using dune::job::cdm::mapToCdm;
using namespace dune::framework::data::constraints;

// Constructor and destructor

JobConstraintsStandard::JobConstraintsStandard(const char *instanceName) :
    instanceName_(instanceName),
    interpreterEnvironment_(nullptr),
    uwAdapter_(nullptr),
    copyJobDynamicConstraintRules_(NULL)
{
    CHECKPOINTC("%s/JobConstraintsStandard: constructed", instanceName_);
}

JobConstraintsStandard::~JobConstraintsStandard()
{
    if ( uwAdapter_ != nullptr )
    {
        delete uwAdapter_;
    }
}

// IComponent methods.

dune::framework::component::ComponentFlavorUid JobConstraintsStandard::getComponentFlavorUid() const
{
    return GET_MODULE_UID(JobConstraintsStandard);
}

const char *JobConstraintsStandard::getComponentInstanceName() const
{
    return instanceName_;
}

void JobConstraintsStandard::initialize(WorkingMode mode, const dune::framework::component::SystemServices *services)
{
    DUNE_UNUSED(mode);
    
    if (nullptr == services)
    {
        CHECKPOINTA("%s/JobConstraintsStandard: initialize services_ value is null during initialize",
                    getComponentInstanceName());
        assert_msg(false, "ERROR:: services_ value is null during initialize");
    }
    else
    {
        interpreterEnvironment_ = services->interpreterEnvironment_;
        
        configuration_ = getConfiguration(services->configurationService_);
        if (nullptr == configuration_)
        {
            CHECKPOINTA("%s/JobConstraintsStandard: initialize configuration_ value is null during initialize",
                        getComponentInstanceName());
            assert_msg(false, "ERROR:: configuration_ value is null during initialize");
        }

        if (nullptr == services->threadPool_)
        {
            CHECKPOINTA("%s/JobConstraintsStandard: initialize services->threadPool_ value is null during initialize",
                        getComponentInstanceName());
            assert_msg(false, "ERROR:: services->threadPool_ value is null during initialize");
        }
    }

    CHECKPOINTC("%s/JobConstraintsStandard: initialized", instanceName_);
}

void * JobConstraintsStandard::getInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName)
{
    DUNE_UNUSED(portName);
    void *interfacePtr = nullptr;
    if (interfaceUid == GET_INTERFACE_UID(IJobConstraints))
    {
        interfacePtr = static_cast<IJobConstraints *>(this);
    }
    CHECKPOINTC("%s/JobConstraintsStandard: getInterface %" PRIu32 " from port %s with addr %p", instanceName_, interfaceUid, portName, interfacePtr);
    return interfacePtr;
}

void JobConstraintsStandard::setInterface(dune::framework::component::InterfaceUid interfaceUid, const char *portName, void *interfacePtr)
{
    DUNE_UNUSED(interfacePtr);
    CHECKPOINTC("%s/JobConstraintsStandard: setInterface %" PRIu32 " to port %s with addr %p", instanceName_, interfaceUid, portName, interfacePtr);

    if (interfacePtr != nullptr)
    {
        if (interfaceUid == GET_INTERFACE_UID(dune::scan::IScanConstraints))
        {
            scanConstraints_ = static_cast<dune::scan::IScanConstraints *>(interfacePtr);
            assert(scanConstraints_);
            CHECKPOINTC("JobConstraintsStandard: setInterface IScanConstraints.");
        }
    }
    else
    {
        CHECKPOINTA("%s/JobConstraintsStandard: setInterface 0x%" PRIx32 " to port %s with addr %p",
                    getComponentInstanceName(), interfaceUid, portName, interfacePtr);
    }
}

void JobConstraintsStandard::connected(dune::framework::component::IComponentManager *componentManager, std::future<void> &asyncCompletion)
{
    DUNE_UNUSED(componentManager);
    DUNE_UNUSED(asyncCompletion);
    assert(scanConstraints_);
    
    // Initialize the underware adapter.
    if ( interpreterEnvironment_ != nullptr )
    {
        uwAdapter_ = new JobConstraintsStandardUwAdapter(interpreterEnvironment_, instanceName_, this);
    }

    CHECKPOINTC("%s/JobConstraintsStandard: connected", instanceName_);
}

void JobConstraintsStandard::shutdown(ShutdownCause cause, std::future<void> &asyncCompletion)
{
    DUNE_UNUSED(cause);
    DUNE_UNUSED(asyncCompletion);
    CHECKPOINTC("%s/JobConstraintsStandard: shutdown", instanceName_);
}

/// @todo implement methods from IJobConstraints here.

std::unique_ptr<JobConstraintsStandardConfigT> JobConstraintsStandard::getConfiguration(
    dune::framework::resources::IConfigurationService *configurationService) const
{
    if(!configurationService)
    {
        CHECKPOINTA("configurationService NULL");
    }
    assert(configurationService);
    dune::framework::resources::IConfigurationService::ConfigurationRawData rawConfiguration =
        configurationService->getConfiguration(GET_MODULE_UID(JobConstraintsStandard), getComponentInstanceName());
    if (rawConfiguration.data && (rawConfiguration.size > 0))
    {
        flatbuffers::Verifier verifier(rawConfiguration.data.get(), rawConfiguration.size);
        assert(VerifyJobConstraintsStandardConfigBuffer(verifier));
        return UnPackJobConstraintsStandardConfig(rawConfiguration.data.get());
    }
    else
    {
        return std::unique_ptr<JobConstraintsStandardConfigT>();
    }
}

std::shared_ptr<CopyJobConstraintsFbT> JobConstraintsStandard::getFbConstraintsTableFromConfiguration(void)
{
    if(constraints_ == nullptr && configuration_ && configuration_->constraints)
    {
        constraints_ = std::move(configuration_->constraints);
    }
    if(constraints_ == nullptr)
    {
        CHECKPOINTA("JobConstraintsStandard::getFbConstraintsTableFromConfiguration: Error! Constraints pointer is NULL! ");
    }
    return constraints_;
}

// The following function should be removed after moving the contained logic to the scan job constraints rules.
// The logic which disables some properties should be moved into various
// 'getXXXConstraints(jobTicket) functions in the scan job constraint rules.
void JobConstraintsStandard::checkIncompatibleTicketConfigurations(std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> 
            constraintsGroup, std::shared_ptr<ICopyJobTicket> jobTicket)
{
    // if there is more than 1 page per sheet, disable scaling
    auto pagesPerSheetEnabled = jobTicket->getIntent()->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp;
    auto prePrintConfiguration = jobTicket->getPrePrintConfiguration();

    // We want to lock out all other scaling options
    // Only Enterprise products are allowed to scaling options
    if (prePrintConfiguration != Product::ENTERPRISE)
    {
        if (pagesPerSheetEnabled)
        {
            CHECKPOINTA("JobConstraintsStandard::checkIncompatibleTicketConfigurations - PagesPerSheet: %d", static_cast<int>( jobTicket->getIntent()->getPagesPerSheet()));
            auto constraints = constraintsGroup->getConstraints("pipelineOptions/scaling/xScalePercent");
            if(constraints != nullptr)
            {
                constraints->add(std::make_unique<Lock>(string_id::cFeatureCurrentNotAvailable));
            }
            
            constraints = constraintsGroup->getConstraints("pipelineOptions/scaling/yScalePercent");
            if(constraints != nullptr)
            {
                constraints->add(std::make_unique<Lock>(string_id::cFeatureCurrentNotAvailable));
            }
            
            constraints = constraintsGroup->getConstraints("pipelineOptions/scaling/scaleSelection");
            if(constraints != nullptr)
            {
                CHECKPOINTA("JobConstraintsStandard::checkIncompatibleTicketConfigurations - LOCK(pagesPerSheetEnabled) ");
                constraints->add(std::make_unique<Lock>(string_id::cFeatureCurrentNotAvailable));
            }
            
            constraints = constraintsGroup->getConstraints("pipelineOptions/scaling/scaleToSize");
            if(constraints != nullptr)
            {
                constraints->add(std::make_unique<Lock>(string_id::cFeatureCurrentNotAvailable));
            }
            constraints = constraintsGroup->getConstraints("pipelineOptions/scaling/scaleToOutput");
            if(constraints != nullptr)
            {
                constraints->add(std::make_unique<Lock>(string_id::cFeatureCurrentNotAvailable));
            }
        }

        CHECKPOINTC("JobConstraintsStandard::checkIncompatibleTicketConfigurations - ScaleSelection: %d", static_cast<int>( jobTicket->getIntent()->getScaleSelection()));
        // gotta disable 2-up if scaling is turned on.
        if(jobTicket->getIntent()->getScaleSelection() != dune::scan::types::ScanScaleSelectionEnum::NONE )
        {
            CHECKPOINTC("JobConstraintsStandard::checkIncompatibleTicketConfigurations - scaleSelection != NONE");
            auto constraints = constraintsGroup->getConstraints("pipelineOptions/imageModifications/pagesPerSheet");
            if(constraints != nullptr)
            {
                CHECKPOINTC("JobConstraintsStandard::checkIncompatibleTicketConfigurations - LOCK(scaleSelection) ");
                constraints->add(std::make_unique<Lock>(string_id::cFeatureCurrentNotAvailable));
            }
        }
    }

    CHECKPOINTC("JobConstraintsStandard::checkIncompatibleTicketConfigurations - BookletFormat: %d", static_cast<int>( jobTicket->getIntent()->getBookletFormat()));
    // gotta disable Staple,Punch,PagesPerSheet,Collate if booklet format is turned on.
    if(jobTicket->getIntent()->getBookletFormat() != dune::imaging::types::BookletFormat::Off )
    {
        CHECKPOINTA("JobConstraintsStandard::checkIncompatibleTicketConfigurations - bookletFormat on");
        auto constraints = constraintsGroup->getConstraints("dest/print/stapleOption");
        if(constraints != nullptr)
        {
            constraints->add(std::make_unique<Lock>(string_id::cFeatureCurrentNotAvailable));
        }
        constraints = constraintsGroup->getConstraints("dest/print/punchOption");
        if(constraints != nullptr)
        {
            constraints->add(std::make_unique<Lock>(string_id::cFeatureCurrentNotAvailable));
        }
        constraints = constraintsGroup->getConstraints("dest/print/collate");
        if(constraints != nullptr)
        {
            constraints->add(std::make_unique<Lock>(string_id::cFeatureCurrentNotAvailable));
        }
    }

    auto stapleEnabled = jobTicket->getIntent()->getStapleOption() != dune::imaging::types::StapleOptions::NONE;
    auto punchEnabled = jobTicket->getIntent()->getPunchOption() != dune::imaging::types::PunchingOptions::NONE;
    auto foldEnabled = (jobTicket->getIntent()->getFoldOption() == dune::imaging::types::FoldingOptions::C_INWARD_TOP ||
                        jobTicket->getIntent()->getFoldOption() == dune::imaging::types::FoldingOptions::C_INWARD_BOTTOM ||
                        jobTicket->getIntent()->getFoldOption() == dune::imaging::types::FoldingOptions::C_OUTWARD_TOP ||
                        jobTicket->getIntent()->getFoldOption() == dune::imaging::types::FoldingOptions::C_OUTWARD_BOTTOM);
    auto scaleSelectionEnabled = !(jobTicket->getIntent()->getScaleSelection() == dune::scan::types::ScanScaleSelectionEnum::NONE ||
                              jobTicket->getIntent()->getScaleSelection() == dune::scan::types::ScanScaleSelectionEnum::FITTOPAGE);
    auto originalSizeEnabled = (jobTicket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::MIXED_A4_A3 ||
                                jobTicket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::MIXED_LETTER_LEDGER ||
                                jobTicket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::MIXED_LETTER_LEGAL ||
                                jobTicket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::PHOTO4X6 ||
                                jobTicket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::PHOTO5X7 ||
                                jobTicket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::PHOTO5X8 ||
                                jobTicket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::A5 ||
                                jobTicket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::A6 ||
                                jobTicket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::B6 ||
                                jobTicket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::PHOTO_10X15IN ||
                                jobTicket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::MEDIA100X150);

    if(stapleEnabled || punchEnabled || foldEnabled || originalSizeEnabled || scaleSelectionEnabled)
    {
        auto constraints = constraintsGroup->getConstraints("pipelineOptions/imageModifications/bookletFormat");
        if(constraints != nullptr)
        {
            constraints->add(std::make_unique<Lock>(string_id::cFeatureCurrentNotAvailable));
        }
    }
}

std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> JobConstraintsStandard::getConstraints(
    std::shared_ptr<ICopyJobTicket> jobTicket, dune::job::ITicketAdapter& ticketAdapter )
{
    CHECKPOINTC("dune::copy::Jobs::Copy::JobConstraintsStandard::getConstraints");

    // ----------------------------------------- BEGIN Gather up data to send to Scan --------------------------------------------------------------------------
    // (IMO)  The following 'setup' code should not have to exist in the copy space.
    // Scan job should figure out what it needs via the job ticket.

    // Get scan constraint, print constraints, then merge the two sets.

        if(jobTicket->getConstraints()->getMediaSupportedSizes().size() == 0 )
        {
            // need to populate the base constraints before we go any further, edit quicksets can follow this path.
            jobTicket->populateDefaultConstraints();
            CHECKPOINTC("dune::copy::Jobs::Copy::JobConstraintsStandard::getConstraints Populating default constraints; mediaSizes.size(): %d collate.size() %d ",
                (int)jobTicket->getConstraints()->getMediaSupportedSizes().size(), (int)jobTicket->getConstraints()->getCollate().size());
        }
        auto constraintsGroup = std::make_shared<ConstraintsGroup>();
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> scanConstraintsGroup;
        // Get Constraints data for valid values from .csf
        // Current Workaround, for future this get action must to be directly related with csf file, not with a proxy class.
        auto constraintsFromFb = jobTicket->getConstraints();
        
        // Get Media sizes/types for possible values.
        std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>> resForSupMediaSizes;
        std::vector<dune::cdm::glossary_1::MediaSize> mediaSizes;

        std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>> resForSupMediaTypes;
        std::vector<dune::cdm::glossary_1::MediaType> mediaTypes;

        // Get Media Sources for Constraints.
        std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSourceId>> resForSupMediaSources;
        std::vector<dune::cdm::glossary_1::MediaSourceId> possibleMediaSources;
        std::vector<dune::cdm::glossary_1::MediaSourceId> validMediaSources;

        APIResult result;
        /* 
        * When the media source is auto, the size of the add media size/type is fetched. 
        * Because Auto is not physical input device. So we can't get media size/type of auto.
        */
        if(jobTicket->getIntent()->getOutputMediaSource() == dune::imaging::types::MediaSource::AUTOSELECT)
        {
            CHECKPOINTC("dune::copy::Jobs::Copy::JobConstraintsStandard::getConstraints - MediaSource is Auto");
            // Get all media supporteds size.
            resForSupMediaSizes = jobTicket->getAllSupportedMediaSizes();
            result = std::get<0>(resForSupMediaSizes);
            if(result == APIResult::OK)
            {
                mediaSizes = std::get<1>(resForSupMediaSizes);
            }

            // Get all media supported types
            resForSupMediaTypes = jobTicket->getAllSupportedMediaTypes();
            result = std::get<0>(resForSupMediaTypes);
            if(result == APIResult::OK)
            {
                mediaTypes = std::get<1>(resForSupMediaTypes);
            }

        }
        else //Media Source is not auto.
        {
            CHECKPOINTC_STR("dune::copy::Jobs::Copy::JobConstraintsStandard::getConstraints - MediaSource is %s", EnumNameMediaSource(jobTicket->getIntent()->getOutputMediaSource()));
            // Get media supported sizes from set media source.
            resForSupMediaSizes = jobTicket->getSupportedMediaSizes(jobTicket->getIntent()->getOutputMediaSource());
            result = std::get<0>(resForSupMediaSizes);
            if(result == APIResult::OK)
            {
                mediaSizes = std::get<1>(resForSupMediaSizes);
            }

            // Get media supported types from set media source.
            resForSupMediaTypes = jobTicket->getSupportedMediaTypes(jobTicket->getIntent()->getOutputMediaSource());
            result = std::get<0>(resForSupMediaTypes);
            if(result == APIResult::OK)
            {
                mediaTypes = std::get<1>(resForSupMediaTypes);
            }
        }

        // Get Possible value for media source. This is also used in 'getScaleToOutputConstraints()' of 'ScanJobConstraintRules.
        resForSupMediaSources = jobTicket->getAllSupportedMediaSources();
        result = std::get<0>(resForSupMediaSources);
        if(result == APIResult::OK)
        {
            possibleMediaSources = std::get<1>(resForSupMediaSources);
            for (auto iter = possibleMediaSources.begin(); iter != possibleMediaSources.end(); iter++)
            {
                CHECKPOINTC_STR("JobConstraintsStandard::getConstraints - PossibleMediaSource1 is %s", (*iter).toString().c_str());
            }
        }

        // Get Valid value for media source. This is also used in 'getScaleToOutputConstraints()' of 'ScanJobConstraintRules.
        std::map<dune::cdm::glossary_1::MediaSourceId, int> mapMediaSources; 
        for(auto it = possibleMediaSources.begin(); it != possibleMediaSources.end(); it++)
        {
            mapMediaSources.insert({*it, 0});
        }

        auto mediaSizeFromTicket = jobTicket->getIntent()->getOutputMediaSizeId();
        auto mediaOrientationFromTicket = jobTicket->getIntent()->getOutputMediaOrientation();
        // Check media sources that support the current media size in flat buffer.
        // If each media source support the currently set media size and type in the jobticket, add 1 to the value.
        auto fbMediaSizes = constraintsFromFb->getMediaSupportedSizes();
        if(mediaSizeFromTicket == dune::imaging::types::MediaSizeId::ANY)
        {
            CHECKPOINTC("JobConstraintsStandard::getConstraints - mediaSizeFromTicket == dune::imaging::types::MediaSizeId::ANY");
            CHECKPOINTC("JobConstraintsStandard::getConstraints - mediaSizeFromTicket supports all media sources");
            for(auto it = mapMediaSources.begin(); it != mapMediaSources.end(); it++)
            {
                mapMediaSources[it->first]++;
                CHECKPOINTC("JobConstraintsStandard::getConstraints - Supported mediaSource map %s (%i)", it->first.toString().c_str(), mapMediaSources[it->first]);
            }
        }
        else if (mediaSizeFromTicket < dune::imaging::types::MediaSizeId::MAX)
        {
            CHECKPOINTC("JobConstraintsStandard::getConstraints - mediaSizeFromTicket < dune::imaging::types::MediaSizeId::UNDEFINED");
            for (auto it = fbMediaSizes.begin(); it != fbMediaSizes.end(); it++)
            {
                CHECKPOINTC_STR("JobConstraintsStandard::getConstraints - Supported MediaSizeId is %s", mapToCdm(it->getId()).toString().c_str());
                        
                if (it->getId() == mediaSizeFromTicket && it->getMediaOrientation() == mediaOrientationFromTicket)
                {
                    auto supportedMediaSources = it->getSupportedMediaSource();
                    for (auto itSupportedMediaSource = supportedMediaSources.begin();
                         itSupportedMediaSource != supportedMediaSources.end(); itSupportedMediaSource++)
                    {
                        auto mediaSource = mapToCdm(*itSupportedMediaSource).toString();
                        CHECKPOINTC_STR("JobConstraintsStandard::getConstraints - Supported MediaSource is %s", mediaSource.c_str());
                        auto retMediaSource = mapMediaSources.find(mediaSource);
                        if (retMediaSource != mapMediaSources.end())
                        {
                            mapMediaSources[retMediaSource->first]++;
                            CHECKPOINTC("JobConstraintsStandard::getConstraints - Supported mediaSource map %s (%i)", retMediaSource->first.toString().c_str(), mapMediaSources[retMediaSource->first]);
                        }
                    }
                    break;
                }
            }
        }

        auto mediaTypeFromTicket = jobTicket->getIntent()->getOutputMediaIdType();
        // Check media sources that support the current media type in flat buffer.
        auto fbMediaTypes = constraintsFromFb->getMediaSupportedTypes();
        if (mediaTypeFromTicket == dune::imaging::types::MediaIdType::ANY)
        {
            CHECKPOINTC("JobConstraintsStandard::getConstraints - mediaTypeFromTicket == dune::imaging::types::MediaIdType::ANY");
            for (auto it = mapMediaSources.begin(); it != mapMediaSources.end(); it++)
            {
                mapMediaSources[it->first]++;
                CHECKPOINTC("JobConstraintsStandard::getConstraints - Supported mediaSource map %s (%i)", it->first.toString().c_str(), mapMediaSources[it->first]);
            }
        }
        else if (mediaTypeFromTicket <= dune::imaging::types::MediaIdType::MAX)
        {
            CHECKPOINTC("JobConstraintsStandard::getConstraints - mediaTypeFromTicket == dune::imaging::types::MediaIdType::UNDEFINED");
            for (auto it = fbMediaTypes.begin(); it != fbMediaTypes.end(); it++)
            {
                CHECKPOINTC_STR("JobConstraintsStandard::getConstraints - Supported MediaTypeId is %s", mapToCdm(it->getId()).toString().c_str());
                
                if (it->getId() == mediaTypeFromTicket)
                {
                    auto supportedMediaSources = it->getSupportedMediaSource();
                    for (auto itSupportedMediaSource = supportedMediaSources.begin();
                         itSupportedMediaSource != supportedMediaSources.end(); itSupportedMediaSource++)
                    {
                        auto mediaSource = mapToCdm(*itSupportedMediaSource).toString();
                        CHECKPOINTC_STR("JobConstraintsStandard::getConstraints - Supported MediaSource is %s", mediaSource.c_str());
                        auto retMediaSource = mapMediaSources.find(mediaSource);
                        if (retMediaSource != mapMediaSources.end())
                        {
                            mapMediaSources[retMediaSource->first]++;
                            CHECKPOINTC("JobConstraintsStandard::getConstraints - Supported mediaSource map %s (%i)", retMediaSource->first.toString().c_str(), mapMediaSources[retMediaSource->first]);
                        }
                    }
                    break;
                }
            }
        }

        for (auto it = mapMediaSources.begin(); it != mapMediaSources.end(); it++)
        {
            if (it->second == 2 || it->first == dune::cdm::glossary_1::MediaSourceId::auto_)  // MediaSource that support the current media size and media type.
            {
                validMediaSources.push_back(it->first);
                CHECKPOINTC_STR("JobConstraintsStandard::getConstraints - ValidMediaSource is %s", (validMediaSources.back()).toString().c_str());
            }
        }

        // ----------------------------------------- END Gather up data to send to Scan --------------------------------------------------------------------------

        if(possibleMediaSources.size() > 0)
        {
            for(auto mediaSource : possibleMediaSources)
            {
                constraintsFromFb->addOutputMediaSourceIds(mediaSource);
            }
        }
        scanConstraintsGroup = scanConstraints_->getScanConstraints(constraintsFromFb, jobTicket->getIntent());

        // Print out the constraints
        CHECKPOINTC("JobConstraintsStandard::getConstraints - Scan Constraints");

        //'dest/print' constraints
        // Workaround part, on near future, supports property must to be connected to csf file empty directly
        auto c = CopyJobStaticConstraintRules::getScaleToOutputConstraints(possibleMediaSources, validMediaSources);
        scanConstraintsGroup->set("pipelineOptions/scaling/scaleToOutput", c);
        if(ticketAdapter.supportsProperty("dest/print/copies"))
        {
            auto c = CopyJobStaticConstraintRules::getCopiesConstraints(jobTicket);
            constraintsGroup->set("dest/print/copies",c);
        }

        if(ticketAdapter.supportsProperty("dest/print/collate"))
        {
            auto c = CopyJobStaticConstraintRules::getCollateConstraints(jobTicket);
            constraintsGroup->set("dest/print/collate",c);
        }
        
        if(ticketAdapter.supportsProperty("dest/print/duplexBinding"))
        {
            auto c = CopyJobStaticConstraintRules::getPlexBindingConstraints(jobTicket);
            constraintsGroup->set("dest/print/duplexBinding",c);
        }
        
        if(ticketAdapter.supportsProperty("dest/print/printQuality"))
        {
            auto c = CopyJobStaticConstraintRules::getPrintQualityConstraints(jobTicket);
            constraintsGroup->set("dest/print/printQuality",c);
        }

        if(ticketAdapter.supportsProperty("dest/print/printMargins"))
        {
            auto c = CopyJobStaticConstraintRules::getCopyMarginsConstraints(jobTicket);
            constraintsGroup->set("dest/print/printMargins",c);
        }

        if(ticketAdapter.supportsProperty("dest/print/printingOrder"))
        {
            auto c = CopyJobStaticConstraintRules::getPrintingOrderConstraints(jobTicket);
            constraintsGroup->set("dest/print/printingOrder",c);
        }

        if(ticketAdapter.supportsProperty("dest/print/rotate"))
        {
            auto c = CopyJobStaticConstraintRules::getRotateConstraints(jobTicket);
            constraintsGroup->set("dest/print/rotate",c);
        }

        if(ticketAdapter.supportsProperty("dest/print/mediaFamily"))
        {
            auto c = CopyJobStaticConstraintRules::getMediaFamilyConstraints(jobTicket);
            constraintsGroup->set("dest/print/mediaFamily",c);
        }

        if(ticketAdapter.supportsProperty("dest/print/stapleOption")
            && jobTicket->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::STAPLE))
        {
            auto c = CopyJobStaticConstraintRules::getStapleOptionConstraints(jobTicket);
            constraintsGroup->set("dest/print/stapleOption",c);
        }

        if(ticketAdapter.supportsProperty("dest/print/punchOption")
            && jobTicket->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::PUNCH))
        {
            auto c = CopyJobStaticConstraintRules::getPunchOptionConstraints(jobTicket);
            constraintsGroup->set("dest/print/punchOption",c);
        }

        if(ticketAdapter.supportsProperty("dest/print/foldOption")
            && jobTicket->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::FOLD))
        {
            auto c = CopyJobStaticConstraintRules::getFoldOptionConstraints(jobTicket);
            constraintsGroup->set("dest/print/foldOption",c);

            c = CopyJobStaticConstraintRules::getSheetsPerFoldSetForCFoldConstraints(jobTicket);
            constraintsGroup->set("dest/print/sheetsPerFoldSet/cFoldSheets",c);

            c = CopyJobStaticConstraintRules::getSheetsPerFoldSetForVFoldConstraints(jobTicket);
            constraintsGroup->set("dest/print/sheetsPerFoldSet/vFoldSheets",c);
        }
        
        if(ticketAdapter.supportsProperty("dest/print/bookletMakerOption")
            && jobTicket->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::BOOKLET_MAKING))
        {
            auto c = CopyJobStaticConstraintRules::getBookletMakerOptionConstraints(jobTicket);
            constraintsGroup->set("dest/print/bookletMakerOption",c);

            c = CopyJobStaticConstraintRules::getSheetsPerFoldSetForFoldAndStitchConstraints(jobTicket);
            constraintsGroup->set("dest/print/sheetsPerFoldSet/foldAndStitchSheets",c);

            c = CopyJobStaticConstraintRules::getSheetsPerFoldSetForDeviceSetsFoldAndStitchSheetsEnabledConstraints(jobTicket);
            constraintsGroup->set("dest/print/sheetsPerFoldSet/deviceSetsFoldAndStitchSheetsEnabled",c);
        }

        if(ticketAdapter.supportsProperty("dest/print/jobOffset"))
        {
            auto c = CopyJobStaticConstraintRules::getJobOffsetConstraints(jobTicket);
            constraintsGroup->set("dest/print/jobOffset",c);
        }

        if(ticketAdapter.supportsProperty("dest/print/mediaSource"))
        {
            // Current workaround method to not broke between products.
            // On next iteration, the idea is remove one of the method to only support decide print media based on real static constraints

            // Possible value comes from print media interface
            // valid values comes from csf constraints
            if(!constraintsFromFb->getMediaPrintSupportedSource().empty())
            {
                auto c = CopyJobStaticConstraintRules::getMediaPrintSupportedSource(constraintsFromFb->getMediaPrintSupportedSource(), possibleMediaSources);
                constraintsGroup->set("dest/print/mediaSource",c);
            }
            else
            {
                auto c = CopyJobStaticConstraintRules::getMediaSourceConstraints(jobTicket);
                constraintsGroup->set("dest/print/mediaSource",c);
            }            
        }
        
        if(ticketAdapter.supportsProperty("dest/print/mediaDestination"))
        {
            auto defaultMediaDestination = configuration_->defaultMediaDestinationConstraint;
            auto c = CopyJobStaticConstraintRules::getOutputPrintMediaConstraints(jobTicket, defaultMediaDestination);
            constraintsGroup->set("dest/print/mediaDestination",c);
        }

        if(ticketAdapter.supportsProperty("dest/print/mediaSize"))     
        {
            auto c = CopyJobStaticConstraintRules::getMediaSizeIdConstraints(jobTicket);
            constraintsGroup->set("dest/print/mediaSize",c);
        }

        if(ticketAdapter.supportsProperty("dest/print/foldingStyleId"))
        {
            auto c = CopyJobStaticConstraintRules::getFoldingStyleIdConstraints(jobTicket);
            constraintsGroup->set("dest/print/foldingStyleId",c);
        }
    
        if(ticketAdapter.supportsProperty("dest/print/mediaType"))     
        {
            auto c = CopyJobStaticConstraintRules::getMediaIdTypeConstraints(jobTicket);
            constraintsGroup->set("dest/print/mediaType",c);
        }

        if(ticketAdapter.supportsProperty("dest/print/plexMode"))
        {
            auto c = CopyJobStaticConstraintRules::getPlexModeConstraints(jobTicket);
            constraintsGroup->set("dest/print/plexMode",c);
        }

        if(ticketAdapter.supportsProperty("dest/print/customMediaXFeedDimension"))
        {
            CHECKPOINTA("%s/JobConstraintsStandard: customMediaXFeedDimension", instanceName_);
            auto c = CopyJobStaticConstraintRules::getCustomMediaXFeedDimensionConstraints();
            constraintsGroup->set("dest/print/customMediaXFeedDimension",c);
        }

        if(ticketAdapter.supportsProperty("dest/print/customMediaYFeedDimension"))
        {
            CHECKPOINTA("%s/JobConstraintsStandard: customMediaXFeedDimension", instanceName_);
            auto c = CopyJobStaticConstraintRules::getCustomMediaYFeedDimensionConstraints();
            constraintsGroup->set("dest/print/customMediaYFeedDimension",c);
        }
          
        // Merge the two sets of constraints
        auto scanConstraints = scanConstraintsGroup->getAllConstraints();

        for ( auto &constraint : scanConstraints )
        {
            constraintsGroup->set(constraint.first, constraint.second);
        }
      
        checkIncompatibleTicketConfigurations(constraintsGroup, jobTicket);
        
    return constraintsGroup;
}

}}}}  // namespace dune::copy::Jobs::Copy

