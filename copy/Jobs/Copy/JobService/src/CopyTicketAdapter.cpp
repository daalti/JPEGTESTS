/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyTicketAdapter.cpp
 * @date   Tue, 06 Aug 2019 12:14:22 +0530
 * @brief  Adapter class between Job Management and copy to serialize/deserialize
 *         information of ticket.
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "ITicketAdapter.hpp"
#include "CopyTicketAdapter.h"
#include "CopyJobTicket.h"
#include "StringIds.h"

#include "common_debug.h"

#include "CopyTicketAdapter_TraceAutogen.h"
#include "PrintQuality_generated.h"
#include "typeMappers.h"
#include "IMedia.h"
#include "MediaHelper.h"
#include "IScanJobIntent.h"
#include "ICopyJobService.h"
#include "Permissions.h"
#include "MediaCdmHelper.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

using dune::cdm::jobTicket_1::CollateModes;
using dune::cdm::jobTicket_1::PrintT;
using dune::cdm::jobTicket_1::jobTicket::DestT;
using dune::cdm::jobTicket_1::jobTicket::PipelineOptionsT;
using dune::cdm::jobTicket_1::jobTicket::SrcT;
using dune::job::cdm::hasValue;
using dune::job::cdm::mapFromCdm;
using dune::job::cdm::mapToCdm;
using dune::ws::cdm::ErrorItemT;
using DeserializeResult = std::tuple<bool, ErrorItemT>;
using PermissionSet = dune::security::ac::PermissionSet;
using Permission = dune::security::ac::Permission;
using namespace dune::framework::data::constraints;
using Product = dune::copy::Jobs::Copy::Product;


CopyTicketAdapter::CopyTicketAdapter(std::shared_ptr<ICopyJobTicket> & copyJobTicket, dune::job::JobServiceFactory<ICopyJobTicket>* jobService)
    : Base{copyJobTicket, jobService}
{
    CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter: constructed");
    this->jobTicket_->setDataSource(dune::job::DataSource::SCANNER);
}

CopyTicketAdapter::~CopyTicketAdapter() = default;

dune::imaging::types::ColorMode CopyTicketAdapter::getFallbackColorMode( std::vector<dune::imaging::types::ColorMode> options)
{
    // we'll select the first one of these options that we find in the options.
    auto colorMode = dune::imaging::types::ColorMode::GRAYSCALE;
    
    for (auto mode : options)
    {
        auto found = false;
        switch (mode)
        {
            case dune::imaging::types::ColorMode::GRAYSCALE:
            case dune::imaging::types::ColorMode::MONOCHROME:
            case dune::imaging::types::ColorMode::BLACKANDWHITE:
                colorMode = mode;
                found = true;
                break;
        }

        if(found)
        {
            break;
        }
    }

    return colorMode;
}

std::shared_ptr<JobTicketTable> CopyTicketAdapter::serializeIntoTable()
{
    CHECKPOINTD("dune::copy::Jobs::Copy::CopyTicketAdapter::serializeIntoTable -- ENTER");
    using dune::cdm::jobTicket_1::jobTicket::DestTable;
    using dune::cdm::jobTicket_1::jobTicket::PipelineOptionsTable;
    using dune::cdm::jobTicket_1::jobTicket::SrcTable;
    using dune::scan::Jobs::Scan::serializeScanStampLocationTable;
    
    auto serializedJobTicketTable = std::make_shared<JobTicketTable>();
    serializedJobTicketTable->beginMergePatch();
    serializedJobTicketTable->ticketId = this->jobTicket_->getTicketId().toString(false);

    auto srcTable = std::make_unique<SrcTable>();
    serializedJobTicketTable->src = *srcTable;
    serializedJobTicketTable->src.beginMergePatch();
    serializedJobTicketTable->pipelineOptions = *(std::make_unique<dune::cdm::jobTicket_1::jobTicket::PipelineOptionsTable>());
    // pipelineOptions
    serializedJobTicketTable->pipelineOptions.getMutable()->beginMergePatch();
    
    // dest
    auto destTable = std::make_unique<DestTable>();
    serializedJobTicketTable->dest = *destTable;

    auto intent = this->jobTicket_->getIntent();

    PermissionSet permission;
    permission.insert(Permission::CP_COPY_COLOR);
    auto securityContext = this->jobTicket_->getSecurityContext();
    dune::imaging::types::ColorMode fallbackColorMode = getFallbackColorMode(jobTicket_->getConstraints()->getColorMode());
    CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::serializeIntoTable fallbackColorMode: %d", (int)fallbackColorMode);
    CHECKPOINTA("PRashant restrict color print %d", jobTicket_->isRestrictColorPrint());
    if (this->jobTicket_->isRestrictColorPrint() || (securityContext && !securityContext->checkPermissions(permission)) ||
        (copyConfigurationHelper_ && !copyConfigurationHelper_->getColorCopyEnabled()))
    {
        CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::serializeIntoTable Security Context Permission::CP_COPY_COLOR"
            " Not Found or copy color disabled so need for colorMode: %d", (int)fallbackColorMode );
        intent->setColorMode(fallbackColorMode);
    }
    
    serializedJobTicketTable->pipelineOptions.getMutable()->generatePreview = dune::job::cdm::mapToCdm(intent->getGeneratePreview());
    serializedJobTicketTable->pipelineOptions.getMutable()->promptForAdditionalPages = dune::job::cdm::mapToCdm(intent->getPromptForMorePages());
    serializedJobTicketTable->intentsValidated = jobTicket_->getIntentsValidated();

    // Deserialize with empty job ticket table, to adjust values if there are errors.
    if(validateTicketOnSerialization_)
    {
        bool updated = false;
        auto deserializeResult = deserializeFromTable(serializedJobTicketTable,updated);
        assert_msg(std::get<0>(deserializeResult), "CopyTicketAdapter::serializeIntoTable Error when deserialize current intent");
        if(updated)
        {
            CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::serializeIntoTable intent was updated.");
        }
    }
    
    // src
    // src.scan
    //serializedJobTicketTable->src.get()->scan = *(serializeScanInfoTable(intent));
    serializedJobTicketTable->src.getMutable()->scan = *(serializeScanInfoTable(intent));

    //pipelineOptions.imageModifications
    serializedJobTicketTable->pipelineOptions.getMutable()->imageModifications = (localeProvider_)?
                                                                                *(serializeImageModsTable(intent, localeProvider_->getMeasurmentUnit())) :
                                                                                *(serializeImageModsTable(intent));
    //pipelineOptions.manualUserOperations
    serializedJobTicketTable->pipelineOptions.getMutable()->manualUserOperations = *(serializeManualOpsTable(intent));
    //pipelineOptions.scaling
    serializedJobTicketTable->pipelineOptions.getMutable()->scaling = *(serializeScalingTable(intent));
    //pipelineOptions.watermark
    serializedJobTicketTable->pipelineOptions.getMutable()->watermark = *(serializeWatermarkDetailsTable(intent));
    
    //pipelineOptions.stamps
    serializedJobTicketTable->pipelineOptions.getMutable()->stampTopLeft      = *(serializeScanStampLocationTable(intent->getStampTopLeft(), dune::imaging::types::StampLocation::TOP_LEFT));
    serializedJobTicketTable->pipelineOptions.getMutable()->stampTopCenter    = *(serializeScanStampLocationTable(intent->getStampTopCenter(), dune::imaging::types::StampLocation::TOP_CENTER));
    serializedJobTicketTable->pipelineOptions.getMutable()->stampTopRight     = *(serializeScanStampLocationTable(intent->getStampTopRight(), dune::imaging::types::StampLocation::TOP_RIGHT));
    serializedJobTicketTable->pipelineOptions.getMutable()->stampBottomLeft   = *(serializeScanStampLocationTable(intent->getStampBottomLeft(), dune::imaging::types::StampLocation::BOTTOM_LEFT));
    serializedJobTicketTable->pipelineOptions.getMutable()->stampBottomCenter = *(serializeScanStampLocationTable(intent->getStampBottomCenter(), dune::imaging::types::StampLocation::BOTTOM_CENTER));
    serializedJobTicketTable->pipelineOptions.getMutable()->stampBottomRight  = *(serializeScanStampLocationTable(intent->getStampBottomRight(), dune::imaging::types::StampLocation::BOTTOM_RIGHT));

    // dest.print
    serializedJobTicketTable->dest.getMutable()->print = *(serializePrintInfoTable(intent));

    //dest.print.sheetsPerFoldSet
    if(jobTicket_->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::FOLD) 
        || jobTicket_->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::BOOKLET_MAKING))
    {
        serializedJobTicketTable->dest.getMutable()->print.getMutable()->sheetsPerFoldSet = *(serializeSheetsPerFoldSet(intent));
    }

    CHECKPOINTD("dune::copy::Jobs::Copy::CopyTicketAdapter::serializeIntoTable -- EXIT");
    return serializedJobTicketTable;
}

std::unique_ptr<dune::cdm::jobTicket_1::PrintTable> CopyTicketAdapter::serializePrintInfoTable(std::shared_ptr<ICopyJobIntent> intent)
{
    CHECKPOINTC("dune::copy::Jobs::CopyTicketAdapter::serializePrintInfoTable -- ENTER");
    dune::print::engine::cdm::MediaCdmHelper mediaCdmHelper;
    auto t = std::make_unique<dune::cdm::jobTicket_1::PrintTable>();
    t->beginMergePatch();

    t->copies = intent->getCopies();

    if(supportsProperty("dest/print/collate") )
    {
        if (intent->getCollate() == dune::copy::SheetCollate::Collate)
            t->collate = dune::cdm::jobTicket_1::CollateModes::collated;
        else
            t->collate = dune::cdm::jobTicket_1::CollateModes::uncollated;
    }

    t->mediaSource = mapToCdm(intent->getOutputMediaSource()).toString();
    t->mediaSize = mediaCdmHelper.convertDuneMediaIdSizeToCdm(intent->getOutputMediaSizeId(), intent->getOutputMediaOrientation()).toString();
    t->mediaType = mapToCdm(intent->getOutputMediaIdType()).toString();

    if(supportsProperty("dest/print/foldingStyleId"))
        t->foldingStyleId = intent->getFoldingStyleId();

    if(supportsProperty("dest/print/plexMode") )
    {
        PermissionSet permission;
        permission.insert(Permission::CP_COPY_ONE_SIDED);
        auto securityContext = this->jobTicket_->getSecurityContext();
        if ((securityContext && !securityContext->checkPermissions(permission)))
        {
            CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::serializePrintInfoTable Security Context Permission::CP_COPY_ONE_SIDED"
                " Not Found or copy simplex disabled so need for plexMode: %d", (int)dune::cdm::glossary_1::PlexMode::duplex );
            t->plexMode = dune::cdm::glossary_1::PlexMode::duplex;
            intent->setOutputPlexMode(dune::imaging::types::Plex::DUPLEX);
            
        }
        else
        {
            t->plexMode = mapToCdm(intent->getOutputPlexMode());
        }
    }

    if(supportsProperty("dest/print/printMargins") )
        t->printMargins = mapToCdm(intent->getCopyMargins());

    if(supportsProperty("dest/print/mediaDestination") )
        t->mediaDestination = mapToCdm(intent->getOutputDestination());

    if(supportsProperty("dest/print/duplexBinding") )
    {
        if(dune::cdm::glossary_1::PlexMode::valueFromString(t->plexMode.get()) == dune::cdm::glossary_1::PlexMode::simplex)
            t->duplexBinding = dune::cdm::glossary_1::DuplexBinding::oneSided;
        else
            t->duplexBinding = mapToCdm(intent->getOutputPlexBinding());
    }
    if(supportsProperty("dest/print/printingOrder"))
        t->printingOrder = mapToCdm(intent->getPrintingOrder());

    if(supportsProperty("dest/print/rotate"))
    {
        if (intent->getAutoRotate() == true)
        {
            t->rotate = mapToCdm(dune::imaging::types::Rotate::AUTO);
        }
        else
        {
            t->rotate = dune::job::cdm::mapToCdmRotate(intent->getRotation());
        }
    }

    if(supportsProperty("dest/print/mediaFamily"))
        t->mediaFamily = mapToCdm(intent->getMediaFamily());

    if (supportsProperty("dest/print/stapleOption") 
            && jobTicket_->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::STAPLE))
        t->stapleOption = mapToCdm(intent->getStapleOption());

    if (supportsProperty("dest/print/punchOption") 
            && jobTicket_->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::PUNCH))
        t->punchOption = mapToCdm(intent->getPunchOption());

    if (supportsProperty("dest/print/foldOption")
            && jobTicket_->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::FOLD))
        t->foldOption = mapToCdm(intent->getFoldOption());

    if (supportsProperty("dest/print/bookletMakerOption")
            && jobTicket_->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::BOOKLET_MAKING))
        t->bookletMakerOption = mapToCdm(intent->getBookletMakerOption());

    if (supportsProperty("dest/print/jobOffset"))
        t->jobOffset = dune::job::cdm::mapToCdmJobOffset(intent->getJobOffsetMode());

    //t->colorMode = mapToCdm(intent->getColorMode()); // Why isn't this on the intent?
    if(supportsProperty("dest/print/printQuality") )
        t->printQuality = mapToCdm(intent->getCopyQuality());

    if(supportsProperty("dest/print/customMediaXFeedDimension"))
    {
        t->customMediaXFeedDimension = intent->getCustomMediaXDimension();
    }

    if(supportsProperty("dest/print/customMediaYFeedDimension"))
    {
        t->customMediaYFeedDimension = intent->getCustomMediaYDimension();
    }

    CHECKPOINTC("dune::copy::Jobs::CopyTicketAdapter::serializePrintInfoTable -- EXIT");
    return t;
}


std::unique_ptr<dune::cdm::jobTicket_1::print::SheetsPerFoldSetTable> CopyTicketAdapter::serializeSheetsPerFoldSet(std::shared_ptr<ICopyJobIntent> intent)
{
    CHECKPOINTD("serializeSheetsPerFoldSet -- ENTER");
    auto s = std::make_unique<dune::cdm::jobTicket_1::print::SheetsPerFoldSetTable>();
    if(jobTicket_->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::FOLD))
    {
        s->cFoldSheets = (int)intent->getSheetsPerSetForCFold();
        s->vFoldSheets = (int)intent->getSheetsPerSetForVFold();
    }
    if(jobTicket_->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::BOOKLET_MAKING))
    {
        s->foldAndStitchSheets = (int)intent->getSheetsPerSetForFoldAndStitch();
        s->deviceSetsFoldAndStitchSheetsEnabled = mapToCdm(intent->getDeviceSetsFoldAndStitchSheetsEnabled());
    }
    CHECKPOINTD("serializeSheetsPerFoldSet -- EXIT");
    return s;
}

std::tuple<bool, dune::ws::cdm::ErrorItemT> CopyTicketAdapter::deserializeFromTable(
    const std::shared_ptr<JobTicketTable>& updatedJobTicketTable,
    bool& isTicketModified )
{
    std::tuple<bool, dune::ws::cdm::ErrorItemT> resultTuple;
    CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializeFromTable -- ENTER");

    // Validate and enforce ticket.
    if (jobTicket_ != nullptr)
    {
        CHECKPOINTD("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializeFromTable - jobTicket is not nullptr");

        // Call to dynamic constraint helper to check if its needed any force change
        if(copyDynamicConstraintsHelper_)
        {
            auto currentConstraints = updateConstraints(updatedJobTicketTable);
            isTicketModified = copyDynamicConstraintsHelper_->checkAndApplyForceSets(
                updatedJobTicketTable, 
                jobTicket_, 
                currentConstraints,
                (staticConstrainsAreCached_ && staticConstraintsGroup_)? staticConstraintsGroup_ : nullptr);

            if(isTicketModified)
            {
                updateConstraints(updatedJobTicketTable);
            }
        }
        else
        {
            CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializeFromTable -- Warning - Dynamic constraints component not hooked up");
        }

        resultTuple = internalDeserializeFromTable(updatedJobTicketTable,isTicketModified);
    }

    CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializeFromTable -- EXIT - Result Tuple: %s", 
        std::get<0>(resultTuple) ? "True" : "False");    
    return resultTuple;
}

std::tuple<bool, dune::ws::cdm::ErrorItemT>  CopyTicketAdapter::internalDeserializeFromTable(
    const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable,
    bool& isTicketModified,
    bool skipValidationErrorReport, 
    std::shared_ptr<ICopyJobIntent> defaultJobIntent)
{
    CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::internalDeserializeFromTable -- ENTER");
    ErrorItemT errorDetails;

    jobTicket_->setIntentsValidated(updatedJobTicketTable->intentsValidated.get());

    if (updatedJobTicketTable->src.get())
    {
        auto res = deserializeScanInfoTable(updatedJobTicketTable->src.get()->scan.get(), jobTicket_->getIntent(), this,
                                            isTicketModified, skipValidationErrorReport, defaultJobIntent);
        if(!std::get<0>(res))
        {
            CHECKPOINTA("dune::copy::CopyTicketAdapter::internalDeserializeFromTable deserializeScanInfoTable returned error: %s", 
                std::get<1>(res).message.c_str());
            return res;
        }
    }
    if (updatedJobTicketTable->dest.get())
    {
        auto res = deserializePrintInfoTable(updatedJobTicketTable->dest.get()->print.get(), jobTicket_->getIntent(),
                                             this, isTicketModified, skipValidationErrorReport, defaultJobIntent);
        if(!std::get<0>(res))
        {
            CHECKPOINTA("dune::copy::CopyTicketAdapter::internalDeserializeFromTable deserializePrintInfoTable returned error: %s", 
                std::get<1>(res).message.c_str());
            return res;
        }
    }
    if (updatedJobTicketTable->pipelineOptions.get())
    {
        jobTicket_->getIntent()->setGeneratePreview(dune::job::cdm::mapFromCdm(updatedJobTicketTable->pipelineOptions.get()->generatePreview.get()));

        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> constraintsGroup = this->getConstraints();
        assert_msg(constraintsGroup,"Always expected a not null constraint group");

        auto isPatch = dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH;
        if(updatedJobTicketTable->pipelineOptions.get()->promptForAdditionalPages.isSet(isPatch))
        {
            auto c = constraintsGroup->getConstraints("pipelineOptions/promptForAdditionalPages");
            dune::cdm::glossary_1::FeatureEnabledEnum promptForAdditionalPagesValue = updatedJobTicketTable->pipelineOptions.get()->promptForAdditionalPages.get();
            auto value = dune::job::cdm::mapFromCdm(promptForAdditionalPagesValue);
            if (c != nullptr && !c->tryValidate(&promptForAdditionalPagesValue)) {
                if(!skipValidationErrorReport)
                {
                    errorDetails.code = "setValueError";
                    errorDetails.message = "promptForAdditionalPages value cannot be set if it is constrained";
                    CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::internalDeserializeFromTable -- validation Error: pipelineoption.promptForAdditionalPages cannot be set if it is constrained");
                    return std::make_tuple(false, errorDetails);
                }
                else if(defaultJobIntent)
                {
                    value = defaultJobIntent->getPromptForMorePages();
                }
            }
            jobTicket_->getIntent()->setPromptForMorePages(value);
        }

        auto res = deserializeScalingTable(updatedJobTicketTable->pipelineOptions.get()->scaling.get(),
                                           jobTicket_->getIntent(), this, isTicketModified, skipValidationErrorReport,
                                           defaultJobIntent);
        if(!std::get<0>(res))
        {
            CHECKPOINTA("dune::copy::CopyTicketAdapter::internalDeserializeFromTable deserializeScalingTable returned error: %s", 
                std::get<1>(res).message.c_str());
            return res;
        }
        
        res = deserializeWatermarkDetailsTable(updatedJobTicketTable->pipelineOptions.get()->watermark.get(), jobTicket_->getIntent(), this, isTicketModified);
        if( std::get<0>(res) == false)
        {
            CHECKPOINTA("dune::copy::CopyTicketAdapter::internalDeserializeFromTable deserializeWatermarkDetailsTable returned error: %s", std::get<1>(res).message.c_str());
            return res;
        }

        res = deserializeImageModsTable(updatedJobTicketTable->pipelineOptions.get()->imageModifications.get(),
                                        jobTicket_->getIntent(), this, isTicketModified, skipValidationErrorReport,
                                        defaultJobIntent);
        if(!std::get<0>(res))        
        {
            CHECKPOINTA("dune::copy::CopyTicketAdapter::internalDeserializeFromTable deserializeImageModsTable returned error: %s", 
                std::get<1>(res).message.c_str());
            return res;
        }

        res = deserializeManualOpsTable(updatedJobTicketTable->pipelineOptions.get()->manualUserOperations.get(),
                                        jobTicket_->getIntent(), this, isTicketModified, skipValidationErrorReport,
                                        defaultJobIntent);
        if(!std::get<0>(res))
        {
            CHECKPOINTA("dune::copy::CopyTicketAdapter::internalDeserializeFromTable deserializeManualOpsTable returned error: %s", 
                std::get<1>(res).message.c_str());
            return res;
        }

        res = deserializeScanStampLocationTable(updatedJobTicketTable->pipelineOptions.get()->stampTopLeft.get(), "stampTopLeft", jobTicket_->getIntent(), this, isTicketModified);
        if( std::get<0>(res) == false)
        {
            CHECKPOINTA("dune::copy::CopyTicketAdapter::internalDeserializeFromTable deserializeScanStampLocationTable stampTopLeft returned error: %s", std::get<1>(res).message.c_str());
            return res;
        }

        res = deserializeScanStampLocationTable(updatedJobTicketTable->pipelineOptions.get()->stampTopCenter.get(), "stampTopCenter", jobTicket_->getIntent(), this, isTicketModified);
        if( std::get<0>(res) == false)
        {
            CHECKPOINTA("dune::copy::CopyTicketAdapter::internalDeserializeFromTable deserializeScanStampLocationTable stampTopCenter returned error: %s", std::get<1>(res).message.c_str());
            return res;
        }

        res = deserializeScanStampLocationTable(updatedJobTicketTable->pipelineOptions.get()->stampTopRight.get(), "stampTopRight", jobTicket_->getIntent(), this, isTicketModified);
        if( std::get<0>(res) == false)
        {
            CHECKPOINTA("dune::copy::CopyTicketAdapter::internalDeserializeFromTable deserializeScanStampLocationTable stampTopRight returned error: %s", std::get<1>(res).message.c_str());
            return res;
        }

        res = deserializeScanStampLocationTable(updatedJobTicketTable->pipelineOptions.get()->stampBottomLeft.get(), "stampBottomLeft", jobTicket_->getIntent(), this, isTicketModified);
        if( std::get<0>(res) == false)
        {
            CHECKPOINTA("dune::copy::CopyTicketAdapter::internalDeserializeFromTable deserializeScanStampLocationTable stampBottomLeft returned error: %s", std::get<1>(res).message.c_str());
            return res;
        }

        res = deserializeScanStampLocationTable(updatedJobTicketTable->pipelineOptions.get()->stampBottomCenter.get(), "stampBottomCenter", jobTicket_->getIntent(), this, isTicketModified);
        if( std::get<0>(res) == false)
        {
            CHECKPOINTA("dune::copy::CopyTicketAdapter::internalDeserializeFromTable deserializeScanStampLocationTable stampBottomCenter returned error: %s", std::get<1>(res).message.c_str());
            return res;
        }

        res = deserializeScanStampLocationTable(updatedJobTicketTable->pipelineOptions.get()->stampBottomRight.get(), "stampBottomRight", jobTicket_->getIntent(), this, isTicketModified);
        if( std::get<0>(res) == false)
        {
            CHECKPOINTA("dune::copy::CopyTicketAdapter::internalDeserializeFromTable deserializeScanStampLocationTable stampBottomRight returned error: %s", std::get<1>(res).message.c_str());
            return res;
        }
    }

    CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::internalDeserializeFromTable -- EXIT");
    return std::make_tuple(true, errorDetails);
}

std::tuple<bool, dune::ws::cdm::ErrorItemT> CopyTicketAdapter::deserializePrintInfoTable(
                                                const dune::cdm::jobTicket_1::PrintTable* printDataTable,
                                                std::shared_ptr<ICopyJobIntent>&&  intent,
                                                CopyTicketAdapter* ticketAdapter,
                                                bool& isTicketModified,
                                                bool skipValidationErrorReport, 
                                                std::shared_ptr<ICopyJobIntent> defaultJobIntent)
{
    CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- ENTER");
    dune::ws::cdm::ErrorItemT errorDetails;

    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> constraintsGroup = ticketAdapter->getConstraints();

    auto isPatch = dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH;
    assert_msg(constraintsGroup,"Always expected a not null constraint group");
    if (printDataTable && intent && constraintsGroup)
    {
        // when copies value is changed
        if (printDataTable->copies.isSet(isPatch))
        {
            auto c = constraintsGroup->getConstraints("dest/print/copies");
            auto value = printDataTable->copies.get();
            if( c!= nullptr && !c->tryValidate(&value))
            {
                if(!skipValidationErrorReport)
                {
                    errorDetails.code = "setValueError";
                    errorDetails.message = "Selection out of range: (ezbuff) dest.print.copies:" + std::to_string(value);
                    CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.copies");
                    return std::make_tuple(false, errorDetails);
                }
                else if(defaultJobIntent)
                {
                    CHECKPOINTC("Validation failed for dest.print.copies, setting default value from defaultJobIntent");
                    value = defaultJobIntent->getCopies();
                }
            }
            if(intent->getCopies() != value)
            {
                intent->setCopies(value);
                isTicketModified = true;
            }
            else
            {
                CHECKPOINTC("deserializePrintInfoTable: copies unchanged");
            }
        }
        if (printDataTable->collate.isSet(isPatch))
        {
            if(supportsProperty("dest/print/collate") )
            {
                auto c = constraintsGroup->getConstraints("dest/print/collate");
                auto cdmValue = printDataTable->collate.get();
                auto value = mapFromCdm(cdmValue);
                if( c!= nullptr && !c->tryValidate(&cdmValue))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.collate:" + std::to_string(cdmValue);
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.collate");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        CHECKPOINTC("Validation failed for dest.print.collate, setting default value from defaultJobIntent");
                        value = defaultJobIntent->getCollate();
                    }
                }

                if( value != intent->getCollate())
                {
                    intent->setCollate(value);
                    isTicketModified = true;
                }
            }
        }
        if (printDataTable->mediaSource.isSet(isPatch))
        {
            auto c = constraintsGroup->getConstraints("dest/print/mediaSource");
            auto cdmValue = printDataTable->mediaSource.get();
            auto value = mapFromCdm(cdmValue);
            CHECKPOINTA(" setMediaSource; cdmValue: %d ; fwValue: %d", static_cast<int>(cdmValue), static_cast<int>(value) );
            if( c!= nullptr && !c->tryValidate(&cdmValue))
            {
                if(!skipValidationErrorReport)
                {
                    errorDetails.code = "setValueError";
                    errorDetails.message = "Selection out of range: dest.print.mediaSource";
                    CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.mediaSource");
                    return std::make_tuple(false, errorDetails);
                }
                else if(defaultJobIntent)
                {
                    CHECKPOINTC("Validation failed for dest.print.mediaSource, setting default value from defaultJobIntent");
                    value = defaultJobIntent->getOutputMediaSource();
                }
            }

            if (intent->getOutputMediaSource() != value)
            {
                intent->setOutputMediaSource(value);
                isTicketModified = true;

                // In case of Beam, constraints will be regenerated, in case of Jupiter not. Because Jupiter
                // Jupiter has an exercise of re-evaluation only for dynamic constraints.
                constraintsGroup = getConstraints(); // We need to recalculate the constraints based on our new plex mode
            }
        }

        if (printDataTable->foldingStyleId.isSet(isPatch))
        {
            if(supportsProperty("dest/print/foldingStyleId") )
            {
                auto c = constraintsGroup->getConstraints("dest/print/foldingStyleId");
                auto cdmValue = printDataTable->foldingStyleId.get();

                if( c!= nullptr && !c->tryValidate(&cdmValue))
                {
                    CHECKPOINTC("deserializePrintInfoTable: foldingStyleId validation failed");
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.foldingStyleId";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.foldingStyleId");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        CHECKPOINTC("Validation failed for dest.print.foldingStyleId, setting default value from defaultJobIntent");
                        cdmValue = defaultJobIntent->getFoldingStyleId();
                    }
                }

                if (intent->getFoldingStyleId() != cdmValue)
                {
                    intent->setFoldingStyleId(cdmValue);
                    CHECKPOINTA("CopyTicketAdapter::deserializePrintInfoTable OK ");
                    isTicketModified = true;
                }
            }
        }
        if (printDataTable->plexMode.isSet(isPatch))
        {
            if(supportsProperty("dest/print/plexMode") )
            {
                auto c = constraintsGroup->getConstraints("dest/print/plexMode");
                auto cdmValue = printDataTable->plexMode.get();
                auto value = mapFromCdm(cdmValue);
                auto bookletFormat = intent->getBookletFormat() != dune::imaging::types::BookletFormat::LeftEdge;
                if( c!= nullptr && !c->tryValidate(&cdmValue) && bookletFormat)
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = " (Copy) Selection out of range: dest.print.plexMode";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.plexMode");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        CHECKPOINTC("Validation failed for dest.print.plexMode, setting default value from defaultJobIntent");
                        value = defaultJobIntent->getOutputPlexMode();
                    }
                }
                if (intent->getOutputPlexMode() != value)
                {
                    intent->setOutputPlexMode(value);
                    isTicketModified = true;
                    constraintsGroup = getConstraints(); // We need to recalculate the constraints based on our new plex mode
                }
            }
        }
        if (printDataTable->mediaSize.isSet(isPatch))
        {
            dune::print::engine::cdm::MediaCdmHelper mediaCdmHelper;
            auto c = constraintsGroup->getConstraints("dest/print/mediaSize");
            auto cdmValue = printDataTable->mediaSize.get();
            auto value = mediaCdmHelper.convertCdmMediaIdSizeAndOrientationToDune(cdmValue);
            if( c!= nullptr && !c->tryValidate(&cdmValue))
            {
                if(!skipValidationErrorReport)
                {
                    errorDetails.code = "setValueError";
                    errorDetails.message = " (Copy) Selection out of range: dest.print.mediaSize";
                    CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.mediaSize");
                    return std::make_tuple(false, errorDetails);
                }
                else
                {
                    CHECKPOINTC("Validation failed for dest.print.mediaSize, setting default value from defaultJobIntent");
                    value = std::make_tuple(intent->getOutputMediaSizeId(), intent->getOutputMediaOrientation());
                }
            }
            
            auto mediaSizeId = std::get<0>(value);
            if (intent->getOutputMediaSizeId() != mediaSizeId)
            {
                intent->setOutputMediaSizeId(mediaSizeId);
                isTicketModified = true;
                constraintsGroup = getConstraints();
            }

            auto mediaOrientation = std::get<1>(value);
            if (intent->getOutputMediaOrientation() != mediaOrientation)
            {
                intent->setOutputMediaOrientation(mediaOrientation);
                isTicketModified = true;
            }
        }
        if (printDataTable->mediaType.isSet(isPatch))
        {
            auto c = constraintsGroup->getConstraints("dest/print/mediaType");
            auto cdmValue = printDataTable->mediaType.get();
            auto value = mapFromCdm(cdmValue);
            if( c!= nullptr && !c->tryValidate(&cdmValue))
            {
                if(!skipValidationErrorReport)
                {
                    errorDetails.code = "setValueError";
                    errorDetails.message = " (copy) Selection out of range: dest.print.mediaType";
                    CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.mediaType");
                    return std::make_tuple(false, errorDetails);
                }
                else if(defaultJobIntent)
                {
                    CHECKPOINTC("Validation failed for dest.print.mediaType, setting default value from defaultJobIntent");
                    value = defaultJobIntent->getOutputMediaIdType();
                }
            }

            if (intent->getOutputMediaIdType() != value)
            {
                intent->setOutputMediaIdType(value);
                isTicketModified = true;
            }
        }
        if (printDataTable->printMargins.isSet(isPatch))
        {
            if(supportsProperty("dest/print/printMargins") )
            {
                auto c = constraintsGroup->getConstraints("dest/print/printMargins");
                auto cdmValue = printDataTable->printMargins.get();
                auto value = mapFromCdm(cdmValue);
                if( c!= nullptr && !c->tryValidate(&cdmValue))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.printMargins";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.printMargins");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        CHECKPOINTC("Validation failed for dest.print.printMargins, setting default value from defaultJobIntent");
                        value = defaultJobIntent->getCopyMargins();
                    }
                }

                if (intent->getCopyMargins() != value)
                {
                    intent->setCopyMargins(value);
                    isTicketModified = true;
                }
            }
        }
        if (printDataTable->printingOrder.isSet(isPatch))
        {
            if(supportsProperty("dest/print/printingOrder") )
            {
                auto c = constraintsGroup->getConstraints("dest/print/printingOrder");
                auto cdmValue = printDataTable->printingOrder.get();
                auto value = mapFromCdm(cdmValue);
                if( c!= nullptr && !c->tryValidate(&cdmValue))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.printingOrder";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.printingOrder");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        CHECKPOINTC("Validation failed for dest.print.printingOrder, setting default value from defaultJobIntent");
                        value = defaultJobIntent->getPrintingOrder();
                    }
                }

                if (intent->getPrintingOrder() != value)
                {
                    intent->setPrintingOrder(value);
                    isTicketModified = true;
                }
            }
        }
        if (printDataTable->rotate.isSet(isPatch))
        {
            if(supportsProperty("dest/print/rotate") )
            {
                auto c = constraintsGroup->getConstraints("dest/print/rotate");
                auto cdmValue = printDataTable->rotate.get();
                auto value = mapFromCdm(dune::cdm::jobTicket_1::Rotate(cdmValue));
                if( c!= nullptr && !c->tryValidate(&cdmValue))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.rotate";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.rotate");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        value = defaultJobIntent->getAutoRotate() ? dune::imaging::types::Rotate::AUTO : value;
                        cdmValue = dune::job::cdm::mapToCdmRotate(defaultJobIntent->getRotation());// verify
                    }
                }

                if (value == dune::imaging::types::Rotate::AUTO)
                {
                    intent->setAutoRotate(true);
                    intent->setRotation(0);
                }
                else
                {
                    intent->setAutoRotate(false);
                    auto integerValue = dune::job::cdm::mapFromCdmRotate(dune::cdm::jobTicket_1::Rotate(cdmValue));
                    intent->setRotation(integerValue);
                }
                isTicketModified = true;
            }
        }
        if (printDataTable->mediaFamily.isSet(isPatch))
        {
            if(supportsProperty("dest/print/mediaFamily") )
            {
                auto c = constraintsGroup->getConstraints("dest/print/mediaFamily");
                auto cdmValue = printDataTable->mediaFamily.get();
                auto value = mapFromCdm(cdmValue);
                if( c!= nullptr && !c->tryValidate(&cdmValue))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.mediaFamily";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.mediaFamily");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        value = defaultJobIntent->getMediaFamily();
                    }
                }

                if (intent->getMediaFamily() != value)
                {
                    intent->setMediaFamily(value);
                    isTicketModified = true;
                }
            }
        }

        if (printDataTable->duplexBinding.isSet(isPatch))
        {
            if(supportsProperty("dest/print/duplexBinding") )
            {
                auto c = constraintsGroup->getConstraints("dest/print/duplexBinding");
                auto cdmValue = printDataTable->duplexBinding.get();
                auto value = mapFromCdm(cdmValue);
                if( c!= nullptr && !c->tryValidate(&cdmValue))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.duplexBinding";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.duplexBinding");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        value = defaultJobIntent->getOutputPlexBinding();
                    }
                }

                if (intent->getOutputPlexBinding() != value)
                {
                    intent->setOutputPlexBinding(value);
                    isTicketModified = true;
                }
            }
        }
        /* When ColorMode is supported on the Copy intent, do this
        if (printDataTable->colorMode.isSet(isPatch))
        {
            auto c = constraintsGroup->getConstraints("dest/print/colorMode");
            auto cdmValue = printDataTable->colorMode.get();
            if( c!= nullptr && !c->tryValidate(&cdmValue))
            {
                errorDetails.code = "setValueError";
                errorDetails.message = "Selection out of range: dest.print.colorMode";
                CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.colorMode");
                return std::make_tuple(false, errorDetails);
            }
            //auto value = mapFromCdm(dune::cdm::jobTicket_1::ColorModesEnum::Values(cdmValue));
            auto value = mapFromCdm(cdmValue);
            if (intent->getColorMode() != value)
            {
                intent->setColorMode(value);
                isTicketModified = true;
            }
        }*/
        if (printDataTable->printQuality.isSet(isPatch))
        {
            if(supportsProperty("dest/print/printQuality") )
            {
                auto c = constraintsGroup->getConstraints("dest/print/printQuality");
                auto cdmValue = printDataTable->printQuality.get();
                auto value = mapFromCdm(cdmValue);
                if( c!= nullptr && !c->tryValidate(&cdmValue))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.printQuality";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.printQuality");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        value = defaultJobIntent->getCopyQuality();
                    }
                }

                if (intent->getCopyQuality() != value)
                {
                    intent->setCopyQuality(value);
                    isTicketModified = true;
                }
            }
        }

        if(printDataTable->mediaDestination.isSet(isPatch))
        {
            if(supportsProperty("dest/print/mediaDestination") )
            {
                auto c = constraintsGroup->getConstraints("dest/print/mediaDestination");
                auto cdmValue = printDataTable->mediaDestination.get();
                auto value = mapFromCdm(cdmValue);
                if( c!= nullptr && !c->tryValidate(&cdmValue))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.mediaDestination";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.mediaDestination"
                            " - value: %s", cdmValue.toString().c_str());
                        return std::make_tuple(false, errorDetails);
                
                    }
                    else if(defaultJobIntent)
                    {
                        value = defaultJobIntent->getOutputDestination();
                    }
                }
                if (intent->getOutputDestination() != value)
                {
                    intent->setOutputDestination(value);
                    isTicketModified = true;
                }
            }
        }

        if (printDataTable->jobOffset.isSet(isPatch))
        {
            if(supportsProperty("dest/print/jobOffset") )
            {
                auto c = constraintsGroup->getConstraints("dest/print/jobOffset");
                auto cdmValue = printDataTable->jobOffset.get();
                auto value = dune::job::cdm::mapFromCdmJobOffset(cdmValue);
                if( c!= nullptr && !c->tryValidate(&cdmValue))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.jobOffset";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.jobOffset");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        value = defaultJobIntent->getJobOffsetMode();
                    }
                }

                if (intent->getJobOffsetMode() != value)
                {
                    intent->setJobOffsetMode(value);
                    isTicketModified = true;
                }
            }
        }

        if(printDataTable->customMediaXFeedDimension.isSet(isPatch))
        {
            if(supportsProperty("dest/print/customMediaXFeedDimension"))
            {
                CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable if(supportsProperty(dest/print/customMediaXFeedDimension))");
                auto c = constraintsGroup->getConstraints("dest/print/customMediaXFeedDimension");
                auto cdmValue = printDataTable->customMediaXFeedDimension.get();
                if( c!= nullptr && !c->tryValidate(&cdmValue) && cdmValue == 0)
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.customMediaXFeedDimension";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.customMediaXFeedDimension");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        cdmValue = defaultJobIntent->getCustomMediaXDimension();
                    }
                }
                
                if (intent->getCustomMediaXDimension() != cdmValue)
                {
                    intent->setCustomMediaXDimension(cdmValue);
                    isTicketModified = true;
                }

            }
        }

        if(printDataTable->customMediaYFeedDimension.isSet(isPatch))
        {
            if(supportsProperty("dest/print/customMediaYFeedDimension"))
            {
                CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable if(supportsProperty(dest/print/customMediaYFeedDimension))");
                auto c = constraintsGroup->getConstraints("dest/print/customMediaYFeedDimension");
                auto cdmValue = printDataTable->customMediaYFeedDimension.get();

                if( c!= nullptr && !c->tryValidate(&cdmValue))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.customMediaYFeedDimension";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.customMediaYFeedDimension");
                        // return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        cdmValue = defaultJobIntent->getCustomMediaYDimension();
                    }
                }

                if (intent->getCustomMediaYDimension() != cdmValue)
                {
                    intent->setCustomMediaYDimension(cdmValue);
                    isTicketModified = true;
                }
            }
        }

        /* Finisher */
        if (printDataTable->stapleOption.isSet(isPatch))
        {
            if(supportsProperty("dest/print/stapleOption") )
            {
                auto c = constraintsGroup->getConstraints("dest/print/stapleOption");
                auto cdmValue = printDataTable->stapleOption.get();
                auto value = mapFromCdm(cdmValue);
                if( c!= nullptr && !c->tryValidate(&cdmValue) && false == jobTicket_->IsInstalledPageBasedFinisherDevice())
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.stapleOption";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.stapleOption");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if (defaultJobIntent)
                    {
                        value = defaultJobIntent->getStapleOption();
                    }
                }

                if (intent->getStapleOption() != value)
                {
                    intent->setStapleOption(value);
                    isTicketModified = true;
                    constraintsGroup = getConstraints();
                }
            }
        }

        if (printDataTable->punchOption.isSet(isPatch))
        {
            if(supportsProperty("dest/print/punchOption") )
            {
                auto c = constraintsGroup->getConstraints("dest/print/punchOption");
                auto cdmValue = printDataTable->punchOption.get();
                auto value = mapFromCdm(cdmValue);

                if( c!= nullptr && !c->tryValidate(&cdmValue))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.punchOption";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.punchOption");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if (defaultJobIntent)
                    {
                        value = defaultJobIntent->getPunchOption();
                    }
                }

                if (intent->getPunchOption() != value)
                {
                    intent->setPunchOption(value);
                    isTicketModified = true;
                    constraintsGroup = getConstraints();
                }
            }
        }

        if (printDataTable->foldOption.isSet(isPatch))
        {
            if(supportsProperty("dest/print/foldOption") )
            {
                auto c = constraintsGroup->getConstraints("dest/print/foldOption");
                auto cdmValue = printDataTable->foldOption.get();
                auto value = mapFromCdm(cdmValue);

                if( c!= nullptr && !c->tryValidate(&cdmValue))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.foldOption";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.foldOption");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        value = defaultJobIntent->getFoldOption();
                    }
                }
                if (intent->getFoldOption() != value)
                {
                    intent->setFoldOption(value);
                    isTicketModified = true;
                }
            }
        }

        if (printDataTable->bookletMakerOption.isSet(isPatch))
        {
            if(supportsProperty("dest/print/bookletMakerOption") )
            {
                auto c = constraintsGroup->getConstraints("dest/print/bookletMakerOption");
                auto cdmValue = printDataTable->bookletMakerOption.get();
                auto value = mapFromCdm(cdmValue);
                if( c!= nullptr && !c->tryValidate(&cdmValue))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: dest.print.bookletMakerOption";
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.bookletMakerOption");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        value = defaultJobIntent->getBookletMakerOption();
                    }
                }
                if (intent->getBookletMakerOption() != value)
                {
                    intent->setBookletMakerOption(value);
                    isTicketModified = true;
                }
            }
        }

        if(printDataTable->sheetsPerFoldSet.get())
        {
            if(printDataTable->sheetsPerFoldSet.get()->vFoldSheets.isSet(isPatch))
            {
                auto c = constraintsGroup->getConstraints("dest/print/sheetsPerFoldSet/vFoldSheets ");
                auto value = printDataTable->sheetsPerFoldSet.get()->vFoldSheets.get();
                if( c!= nullptr && !c->tryValidate(&value))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: (ezbuff) dest.print.sheetsPerFoldSet.vFoldSheets:" + std::to_string(value);
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.sheetsPerFoldSet.vFoldSheets");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        value = defaultJobIntent->getSheetsPerSetForVFold();
                    }
                }
                if(intent->getSheetsPerSetForVFold() != value)
                {
                    intent->setSheetsPerSetForVFold(value);
                    isTicketModified = true;
                }
            }

            if(printDataTable->sheetsPerFoldSet.get()->cFoldSheets.isSet(isPatch))
            {
                auto c = constraintsGroup->getConstraints("dest/print/sheetsPerFoldSet/cFoldSheets ");
                auto value = printDataTable->sheetsPerFoldSet.get()->cFoldSheets.get();
                if( c!= nullptr && !c->tryValidate(&value))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: (ezbuff) dest.print.sheetsPerFoldSet.cFoldSheets:" + std::to_string(value);
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.sheetsPerFoldSet.cFoldSheets");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        value = defaultJobIntent->getSheetsPerSetForCFold();
                    }
                }
                if(intent->getSheetsPerSetForCFold() != value)
                {
                    intent->setSheetsPerSetForCFold(value);
                    isTicketModified = true;
                }
            }

            if(printDataTable->sheetsPerFoldSet.get()->foldAndStitchSheets.isSet(isPatch))
            {
                auto c = constraintsGroup->getConstraints("dest/print/sheetsPerFoldSet/foldAndStitchSheets ");
                auto value = printDataTable->sheetsPerFoldSet.get()->foldAndStitchSheets.get();
                if( c!= nullptr && !c->tryValidate(&value))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: (ezbuff) dest.print.sheetsPerFoldSet.foldAndStitchSheets:" + std::to_string(value);
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.sheetsPerFoldSet.foldAndStitchSheets");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if (defaultJobIntent)
                    {
                        value = defaultJobIntent->getSheetsPerSetForFoldAndStitch();
                    }
                }
                if(intent->getSheetsPerSetForFoldAndStitch() != value)
                {
                    intent->setSheetsPerSetForFoldAndStitch(value);
                    isTicketModified = true;
                }   
            }

            if(printDataTable->sheetsPerFoldSet.get()->deviceSetsFoldAndStitchSheetsEnabled.isSet(isPatch))
            {
                auto c = constraintsGroup->getConstraints("dest/print/sheetsPerFoldSet/deviceSetsFoldAndStitchSheetsEnabled ");
                auto cdmValue = printDataTable->sheetsPerFoldSet.get()->deviceSetsFoldAndStitchSheetsEnabled.get();
                auto value = mapFromCdm(cdmValue);

                if( c!= nullptr && !c->tryValidate(&cdmValue))
                {
                    if(!skipValidationErrorReport)
                    {
                        errorDetails.code = "setValueError";
                        errorDetails.message = "Selection out of range: (ezbuff) dest.print.sheetsPerFoldSet.deviceSetsFoldAndStitchSheetsEnabled:" + std::to_string(value);
                        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- validation error: dest.print.sheetsPerFoldSet.deviceSetsFoldAndStitchSheetsEnabled");
                        return std::make_tuple(false, errorDetails);
                    }
                    else if(defaultJobIntent)
                    {
                        value = defaultJobIntent->getDeviceSetsFoldAndStitchSheetsEnabled();
                    }
                }
                
                if(intent->getDeviceSetsFoldAndStitchSheetsEnabled() != value)
                {
                    intent->setDeviceSetsFoldAndStitchSheetsEnabled(value);
                    isTicketModified = true;
                }
            }
        }
    }
    else
    {
        CHECKPOINTA("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- (printDataTable && intent) did not resolve to true");
    }
    CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializePrintInfoTable -- EXIT");
    return std::make_tuple(true, errorDetails);
}

std::tuple<bool, dune::ws::cdm::ErrorItemT> CopyTicketAdapter::deserializeFromTableWithRules(
    const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& isTicketModified,
    bool skipValidationErrorReport, std::shared_ptr<ICopyJobIntent> defaultJobIntent)
{
    std::tuple<bool, dune::ws::cdm::ErrorItemT> resultTuple;
    CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializeFromTableWithRules -- ENTER");

    // Validate and enforce ticket.
    if (jobTicket_ != nullptr)
    {
        CHECKPOINTD(
            "dune::copy::Jobs::Copy::CopyTicketAdapter::deserializeFromTableWithRules - jobTicket is not nullptr");

        // Call to dynamic constraint helper to check if its needed any force change
        if (copyDynamicConstraintsHelper_)
        {
            auto currentConstraints = updateConstraints(updatedJobTicketTable);
            isTicketModified = copyDynamicConstraintsHelper_->checkAndApplyForceSets(
                updatedJobTicketTable, jobTicket_, currentConstraints,
                (staticConstrainsAreCached_ && staticConstraintsGroup_) ? staticConstraintsGroup_ : nullptr);

            if (isTicketModified)
            {
                updateConstraints(updatedJobTicketTable);
            }
        }
        else
        {
            CHECKPOINTA(
                "dune::copy::Jobs::Copy::CopyTicketAdapter::deserializeFromTableWithRules -- Warning - Dynamic "
                "constraints "
                "component not hooked up");
        }

        resultTuple = internalDeserializeFromTable(updatedJobTicketTable, isTicketModified, skipValidationErrorReport,
                                                   defaultJobIntent);
    }

    CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::deserializeFromTableWithRules -- EXIT - Result Tuple: %s",
                std::get<0>(resultTuple) ? "True" : "False");
    return resultTuple;
}

bool CopyTicketAdapter::supportsProperty(const std::string& propertyName)
{
    bool retVal = true;

    // TODO src.scan properties After discussion with Send apps team
    // Current implement is a workaround using old Constraint class encapsulation
    // This method must to be cleaned on near future to get supported directly from static constraints table.
    if(jobTicket_->getConstraints())
    {
        // dest.print properties
        if(propertyName == "dest/print/printMargins" && jobTicket_->getConstraints()->getCopyMargins().size() ==0 )
            retVal = false;
        else if(propertyName == "dest/print/plexMode" && jobTicket_->getConstraints()->getPlexMode().size() ==0 )
            retVal = false;
        else if(propertyName == "dest/print/mediaType" &&   jobTicket_->getConstraints()->getMediaSupportedTypes().size()     == 0 &&
                                                            jobTicket_->getConstraints()->getMediaPrintSupportedType().size() == 0    )
            retVal = false;
        else if(propertyName == "dest/print/duplexBinding" && jobTicket_->getConstraints()->getPlexBinding().size() ==0 )
            retVal = false;
        else if(propertyName == "dest/print/collate" && jobTicket_->getConstraints()->getCollate().size() ==0 )
            retVal = false;
        else if(propertyName == "dest/print/printQuality" && jobTicket_->getConstraints()->getPrintQuality().size() ==0 )
            retVal = false;
        else if(propertyName == "dest/print/mediaDestination" && jobTicket_->getConstraints()->getMediaDestinations().size() ==0 )
            retVal = false;
        else if(propertyName == "dest/print/foldingStyleId" )
        {
            if(jobTicket_->getConstraints()->getMediaDestinations().size() == 0 )
            {
                retVal = false;
            }
            else
            {
                for(auto mediaDestination : jobTicket_->getConstraints()->getMediaDestinations())
                {
                    if( mediaDestination == dune::imaging::types::MediaDestinationId::FOLDER  ||
                        mediaDestination == dune::imaging::types::MediaDestinationId::FOLDER2 ||
                        mediaDestination == dune::imaging::types::MediaDestinationId::FOLDER3 ||
                        mediaDestination == dune::imaging::types::MediaDestinationId::FOLDER4 )
                    {
                        retVal = true;
                        break;
                    }
                }
            }
        }
        else if(propertyName == "dest/print/printingOrder" && jobTicket_->getConstraints()->getPrintingOrder().size() ==0 )
            retVal = false;
        else if(propertyName == "dest/print/rotate" && jobTicket_->getConstraints()->getMaxRotation() == 0 && jobTicket_->getConstraints()->getAutoRotate().size() == 0)
            retVal = false;
        else if(propertyName == "dest/print/mediaFamily" && jobTicket_->getConstraints()->getMediaFamily().size() ==0 )
            retVal = false;
        else if(propertyName == "dest/print/stapleOption" && jobTicket_->getConstraints()->getStapleOption().size() ==0 )
            retVal = false;
        else if(propertyName == "dest/print/punchOption" && jobTicket_->getConstraints()->getPunchOption().size() ==0 )
            retVal = false;
        else if(propertyName == "dest/print/foldOption" && jobTicket_->getConstraints()->getFoldOption().size() ==0 )
            retVal = false;
        else if(propertyName == "dest/print/bookletMakerOption" && jobTicket_->getConstraints()->getBookletMakerOption().size() ==0 )
            retVal = false; 
        else if(propertyName == "dest/print/jobOffset" && jobTicket_->getConstraints()->getJobOffsetMode().size() ==0 )
            retVal = false;
        // Workaround check to not broke functionality between products
        else if(propertyName == "dest/print/mediaSource" &&
                // Check for printers without dependency of type and size, that check directly source value on csf file
                !(jobTicket_->getConstraints()->getMediaPrintSupportedSource().size() > 0 ||
                // Check dependency of printers that source evaluations depends of size and type supported check too
                    (jobTicket_->getConstraints()->getMediaSupportedSizes().size() > 0 &&
                     jobTicket_->getConstraints()->getMediaSupportedTypes().size() > 0)))
            retVal = false;
        else if(propertyName == "dest/print/colorMode") // for now, we're using the 'src/scan/colorMode'; this may change in the future.
            retVal = false;
        else if(propertyName == "dest/print/customMediaXFeedDimension" && jobTicket_->getPrePrintConfiguration() != Product::ENTERPRISE)
            retVal = false;
        else if(propertyName == "dest/print/customMediaYFeedDimension" && jobTicket_->getPrePrintConfiguration() != Product::ENTERPRISE)
            retVal = false;
    }

    CHECKPOINTC("CopyTicketAdapter::supportsProperty %ssupport settting %s",retVal?"":"not ",propertyName.c_str());

    return retVal;
}

std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> CopyTicketAdapter::getConstraints()
{
    return (staticConstrainsAreCached_ && lastConstraintsGroup_) ? lastConstraintsGroup_ : updateConstraints();
}

std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> CopyTicketAdapter::updateConstraints(
    const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable)
{
    CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::updateConstraints() -- Enter");
    //Get the Static constraints to ConstraintsGroup, get the dynamic constraints and merge them and then return the constraints group
    std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> constraintsGroup
        = std::make_shared<dune::framework::data::constraints::ConstraintsGroup>();

    if(staticConstraintsGroup_)
    {
        // If static constraints group was generated previously, fill current constraint group with static constraints.
        constraintsGroup = std::make_shared<dune::framework::data::constraints::ConstraintsGroup>(*staticConstraintsGroup_);
    }
    else if(copyJobConstraintsHelper_)
    {
        CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::updateConstraints() base static constraints");
        constraintsGroup = copyJobConstraintsHelper_->getConstraints(jobTicket_, *this);
        
        if(staticConstrainsAreCached_ && constraintsGroup)
        {
            CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::updateConstraints() copy and save static constraints");
            staticConstraintsGroup_ = std::make_shared<dune::framework::data::constraints::ConstraintsGroup>(*constraintsGroup);
        }
    }

    if(copyDynamicConstraintsHelper_ && constraintsGroup)
    {
        auto dynamicConstraintsGroup = copyDynamicConstraintsHelper_->getDynamicConstraints(jobTicket_,constraintsGroup,updatedJobTicketTable);
        if(dynamicConstraintsGroup)
        {
            //Merge the static and dynamicConstraints
            //At the moment dynamic and static constraints are in the "constraintsGroup" variable
            auto dynamicConstraints = dynamicConstraintsGroup->getAllConstraints();
            for ( auto &constraint : dynamicConstraints )
            {
                CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::updateConstraints - dynamicConstraintsGroup %s", (constraint.first).c_str());
                constraintsGroup->remove(constraint.first);
                constraintsGroup->set(constraint.first, constraint.second);
            }

            //Add job settings constraints in job is in processing state
            copyDynamicConstraintsHelper_->updateWithJobDynamicConstraints(jobTicket_, constraintsGroup);
        }
    }

    if(staticConstrainsAreCached_)
    {
        lastConstraintsGroup_ = constraintsGroup;
    }

    CHECKPOINTC("dune::copy::Jobs::Copy::CopyTicketAdapter::updateConstraints() -- Exit");
    return constraintsGroup;
}

void CopyTicketAdapter::setStaticConstrainsAreCached(const bool val)
{
    staticConstrainsAreCached_ = val;
}

void CopyTicketAdapter::setValidateTicketOnSerialization(const bool value)
{
    validateTicketOnSerialization_ = value;
}

void CopyTicketAdapter::setLocaleProvider(dune::localization::ILocaleProvider* localeProvider)
{
    localeProvider_ = localeProvider;
}

}}}}  // namespace dune::copy::Jobs::Copy