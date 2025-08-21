/* -*- c++ -*- */

////////////////////////////////////////////////////////////////////////////////
/**
 * @file  ForceSets.cpp
 * @brief force sets
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////////

#include "ForceSets.h"

#include "ForceSets_TraceAutogen.h"
#include "typeMappers.h"
#include "ScanJobIntent.h"
#include "ICapabilities.h"
#include "common_debug.h"


namespace dune { namespace copy { namespace Jobs { namespace Copy {

using dune::job::cdm::mapToCdm;
using FeatureEnabled = dune::cdm::glossary_1::FeatureEnabled;

bool ForceSets::ScannerHasADFDuplex(std::shared_ptr<ICopyJobTicket> ticket)
{
    dune::scan::scanningsystem::IScannerCapabilities* scannerCaps =  ticket->getScanCapabilitiesInterface();
    bool retVal = false;
    scannerCaps->hasDuplexSupport(retVal);
    CHECKPOINTA("ForceSets::ScannerHasADFDuplex:: duplex == %d", (int)retVal);
    return retVal;
}

void ForceSets::checkAndApplyScanMediaSourceForceSets(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<ICopyJobTicket> ticket)
{
    auto prePrintConfiguration = ticket->getPrePrintConfiguration();
    CHECKPOINTD("dune::copy::Jobs::Copy::ForceSets::CheckAndApplyScanMediaSourceForceSets Entry");
    auto isPatch = dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH;
    // if mediaSource ==> adf and we are at a high res 
    if(updatedJobTicketTable->src.get() != nullptr && 
       updatedJobTicketTable->src.get()->scan.get() != nullptr && 
       updatedJobTicketTable->src.get()->scan.get()->mediaSource.isSet(isPatch) )
    {
        auto cdmMediaSourceVal = updatedJobTicketTable->src.get()->scan.get()->mediaSource.get();
        
        if( prePrintConfiguration != Product::ENTERPRISE ){
            if( cdmMediaSourceVal == dune::cdm::glossary_1::ScanMediaSourceId::adf && 
            ticket->getIntent()->getInputPlexMode() == dune::imaging::types::Plex::DUPLEX && 
            ScannerHasADFDuplex(ticket) == false )
            {
                // force input plex to simplex 
                updatedJobTicketTable->src.getMutable()->scan.getMutable()->plexMode = dune::cdm::glossary_1::PlexMode::simplex;
                CHECKPOINTB("dune::copy::Jobs::Copy::ForceSets::checkAndApplyScanMediaSourceForceSets -- ForceSet(src.scan.plexMode, simplex)");
            }
            if(ticket->getIntent()->getCopyQuality() == dune::imaging::types::PrintQuality::BEST )
            {
                    setHighestResolution(updatedJobTicketTable, ticket);
            }

            //To-Do Remove this in future once DUNE-89051 is Implemented.
            //If scan source is changed to ADF and media size is ANY Then=> ForceSet(inputMediaSize,letter)
            if( cdmMediaSourceVal == dune::cdm::glossary_1::ScanMediaSourceId::adf && 
                ticket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::ANY)
            {
                updatedJobTicketTable->src.getMutable()->scan.getMutable()->mediaSize = dune::cdm::glossary_1::MediaSize::na_letter_8_dot_5x11in;
                CHECKPOINTB("dune::copy::Jobs::Copy::ForceSets::checkAndApplyScanMediaSourceForceSets -- ForceSet(src.scan.MediaSize, letter)"); 
            }
        }

        if( prePrintConfiguration == Product::ENTERPRISE ){
            if( cdmMediaSourceVal == dune::cdm::glossary_1::ScanMediaSourceId::flatbed && 
            (ticket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::MIXED_LETTER_LEGAL ||
                ticket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::MIXED_LETTER_LEDGER ||
                ticket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::MIXED_A4_A3))
            {
                updatedJobTicketTable->src.getMutable()->scan.getMutable()->mediaSize = dune::cdm::glossary_1::MediaSize::any;
                CHECKPOINTA("dune::copy::Jobs::Copy::ForceSets::checkAndApplyScanMediaSourceForceSets -- Mixed ForceSet(src.scan.MediaSize, any)"); 
            }
        }
    }
}

void ForceSets::checkAndApplyPrintQualityForceSets(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<ICopyJobTicket> ticket)
{
    CHECKPOINTB("dune::copy::Jobs::Copy::ForceSets::checkAndApplyPrintQualityForceSets Entry");
    auto isPatch = dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH;

    //When print quality is set to Best, force Scan resolution to highest dpi.
    if(updatedJobTicketTable->dest.get() != nullptr && 
       updatedJobTicketTable->dest.get()->print.get() != nullptr && 
       updatedJobTicketTable->dest.get()->print.get()->printQuality.isSet(isPatch) )
    {
        auto cdmPrintQuality = updatedJobTicketTable->dest.get()->print.get()->printQuality.get();
        if(cdmPrintQuality == dune::cdm::glossary_1::PrintQuality::best )
        {
           setHighestResolution(updatedJobTicketTable, ticket);
        }
        else if(ticket->getIntent()->getOutputXResolution() != dune::imaging::types::Resolution::E300DPI)
        {
            // Normal = 300dpi, Draft= 300dpi, Best = 600dpi(flatbed) 300dpi(adf)
            setResolution(updatedJobTicketTable, dune::cdm::jobTicket_1::Resolutions::e300Dpi);
        }
    }
}


void ForceSets::checkAndApplyForceSets(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> currentConstraintsGroup, dune::scan::IScanConstraints* scanConstraints)
{
    DUNE_UNUSED(scanConstraints);
    DUNE_UNUSED(currentConstraintsGroup);
    auto prePrintConfiguration = ticket->getPrePrintConfiguration();

    if( prePrintConfiguration != Product::ENTERPRISE ){
        checkAndApplyPrintQualityForceSets(updatedJobTicketTable, ticket);
        checkAndApplyTwoPagesPerSheetForceSets(updatedJobTicketTable, dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH);
    }
    checkAndApplyScanMediaSourceForceSets(updatedJobTicketTable, ticket);
    scanConstraints->checkAndApplyScanForceSets(updatedJobTicketTable, ticket->getIntent(), currentConstraintsGroup);
}

void ForceSets::setHighestResolution(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<ICopyJobTicket> ticket )
{
    CHECKPOINTB("dune::copy::Jobs::Copy::ForceSets::setHighestResolution()");
    auto scanSource = ticket->getIntent()->getScanSource();
    auto isPatch = dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH;
    if(updatedJobTicketTable->src.get() != nullptr && 
       updatedJobTicketTable->src.get()->scan.get() != nullptr && 
       updatedJobTicketTable->src.get()->scan.get()->mediaSource.isSet(isPatch) )
    {
        auto cdmMediaSourceVal = updatedJobTicketTable->src.get()->scan.get()->mediaSource.get();
        if(cdmMediaSourceVal == dune::cdm::glossary_1::ScanMediaSourceId::flatbed )
            scanSource = dune::scan::types::ScanSource::GLASS;
        else if(cdmMediaSourceVal == dune::cdm::glossary_1::ScanMediaSourceId::adf )
            scanSource = dune::scan::types::ScanSource::ADF_DUPLEX;
    }
    if(scanSource == dune::scan::types::ScanSource::GLASS)
    {
        if(ticket->getIntent()->getOutputXResolution() != dune::imaging::types::Resolution::E600DPI)
        {
            setResolution(updatedJobTicketTable,dune::cdm::jobTicket_1::Resolutions::e600Dpi);
        }
    }
    else if(scanSource == dune::scan::types::ScanSource::ADF_SIMPLEX ||
            scanSource == dune::scan::types::ScanSource::ADF_DUPLEX    )
    {
        if(ticket->getIntent()->getOutputXResolution() != dune::imaging::types::Resolution::E300DPI)
        {
            setResolution(updatedJobTicketTable,dune::cdm::jobTicket_1::Resolutions::e300Dpi);
        }
    }
}

void ForceSets::setResolution(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, dune::cdm::jobTicket_1::Resolutions res )
{
    auto src = updatedJobTicketTable->src.getMutable();
    if(src == NULL)
    {
        CHECKPOINTB("dune::copy::Jobs::Copy::ForceSets::setResolution -- Creating 'src' table");
        updatedJobTicketTable->src = dune::cdm::jobTicket_1::jobTicket::SrcTable();
    }
    auto scan = updatedJobTicketTable->src.getMutable()->scan.getMutable();
    if( scan == NULL)
    {
        updatedJobTicketTable->src.getMutable()->scan = dune::cdm::jobTicket_1::ScanTable();
        CHECKPOINTB("dune::copy::Jobs::Copy::ForceSets::setResolution -- Creating 'scan' table");
    }
    updatedJobTicketTable->src.getMutable()->scan.getMutable()->resolution = res;
    CHECKPOINTB("dune::copy::Jobs::Copy::ForceSets::setResolution -- ForceSet(src.scan.resolution, %d)", (int) res);
}

void ForceSets::checkAndApplyTwoPagesPerSheetForceSets(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, bool isPatch)
{
    CHECKPOINTB("ForceSets::checkAndApplyTwoPagesPerSheetForceSets Entry");

    //check what values are set
    auto collateSet = false;
    auto pagesPerSheetSet = false;

    //collateSet
    if (updatedJobTicketTable->dest.get() != nullptr &&
        updatedJobTicketTable->dest.get()->print.get() != nullptr &&
        updatedJobTicketTable->dest.get()->print.get()->collate.isSet(isPatch))
    {
        collateSet = true;
    }

    //pagesPerSheetSet
    if (updatedJobTicketTable->pipelineOptions.get() != nullptr &&
        updatedJobTicketTable->pipelineOptions.get()->imageModifications.get() != nullptr &&
        updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->pagesPerSheet.isSet(isPatch))
    {
        pagesPerSheetSet = true;
    }

    //When Collate is turned on, force 2 pages per sheet off
    if(collateSet && updatedJobTicketTable->dest.get()->print.get()->collate.get() ==  dune::cdm::jobTicket_1::CollateModes::collated)
    {
        auto pipelineOptions = updatedJobTicketTable->pipelineOptions.getMutable();
        if(pipelineOptions == NULL)
        {
            CHECKPOINTB("ForceSets::checkAndApplyTwoPagesPerSheetForceSets Creating 'pipeline options' table");
            updatedJobTicketTable->pipelineOptions = dune::cdm::jobTicket_1::jobTicket::PipelineOptionsTable();
        }
        auto imageModifications = updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable();
        if( imageModifications == NULL)
        {
            updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications = dune::cdm::jobTicket_1::ImageModificationsTable();
            CHECKPOINTB("ForceSets::checkAndApplyTwoPagesPerSheetForceSets Creating 'imageModifications' table");
        }
        updatedJobTicketTable->pipelineOptions.getMutable()->imageModifications.getMutable()->pagesPerSheet = dune::cdm::jobTicket_1::PagesPerSheet::oneUp;
    }

    //When 2 pages per sheet modified, force incompatible settings to alternate with this change
    if(pagesPerSheetSet)
    {
        auto dest = updatedJobTicketTable->dest.getMutable();
        if(dest == NULL)
        {
            CHECKPOINTB("ForceSets::checkAndApplyTwoPagesPerSheetForceSets  Creating 'dest options' table");
            updatedJobTicketTable->dest = dune::cdm::jobTicket_1::jobTicket::DestTable();
        }
        auto print = updatedJobTicketTable->dest.getMutable()->print.getMutable();
        if( print == NULL)
        {
            updatedJobTicketTable->dest.getMutable()->print = dune::cdm::jobTicket_1::PrintTable();
            CHECKPOINTB("ForceSets::checkAndApplyTwoPagesPerSheetForceSets Creating 'print' table");
        }

        auto pagesPerSheet = updatedJobTicketTable->pipelineOptions.get()->imageModifications.get()->pagesPerSheet.get();
        if (pagesPerSheet == dune::cdm::jobTicket_1::PagesPerSheet::twoUp)
        {
            //Disallow Collate
            CHECKPOINTB("ForceSets::checkAndApplyTwoPagesPerSheetForceSets twoUp set, setting uncollated");
            updatedJobTicketTable->dest.getMutable()->print.getMutable()->collate = dune::cdm::jobTicket_1::CollateModes::uncollated;
        }
        else if (!collateSet)
        {
            //Enable default collate on as pagesPerSheet changes to 1
            CHECKPOINTB("ForceSets::checkAndApplyTwoPagesPerSheetForceSets oneUp set, setting collated");
            updatedJobTicketTable->dest.getMutable()->print.getMutable()->collate = dune::cdm::jobTicket_1::CollateModes::collated;
        }
    }
}

}}}}  // namespace dune::copy::Jobs::Copy
