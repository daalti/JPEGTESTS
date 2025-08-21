/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   PrintJoltToDuneConverter.h
 * @date   Tue, 06 May 2025
 * @brief  Header for Jolt to Dune print data converter
 *
 * (C) Copyright 2025 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#ifndef DUNE_COPY_JOBS_COPY_PRINT_JOLT_TO_DUNE_CONVERTER_H
#define DUNE_COPY_JOBS_COPY_PRINT_JOLT_TO_DUNE_CONVERTER_H

#include "XmlUtils.h"
#include "com.hp.cdm.domain.glossary.version.1.easybuffers_autogen.h"
#include "com.hp.cdm.service.jobTicket.version.1.easybuffers_autogen.h"
#include "IMedia.h"
#include "typeMappers.h"
#include "PrintQuality_generated.h"
#include "dune_types.h"
#include "ImagingSendTypes_generated.h"
#include "IPrintIntentsConverter.h"


namespace dune { namespace copy { namespace Jobs { namespace Copy {

enum class CustomMediaDimensionUnit{
    MM,
    INCHES,
};

class PrintJoltToDuneConverter : public IPrintIntentsConverter {
public:
    PrintJoltToDuneConverter();
    ~PrintJoltToDuneConverter() override;

    dune::framework::core::APIResult convert(const dune::framework::data::conversion::DataDescriptor& fileDescriptor,
        std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable) override;

    // Mapper function declarations inside the class
    static dune::copy::SheetCollate mapStringToSheetCollate(const std::string& value);
    static dune::imaging::types::PrintQuality mapStringToPrintQuality(const std::string& value);
    //CopyOriginalOutputBinding mapStringToCopyOriginalOutputBinding(const std::string& value);
    static dune::imaging::types::MediaSource mapStringToMediaInputId(const std::string& value);
    static dune::imaging::types::MediaDestinationId mapStringToMediaOutputId(const std::string& value);
    static dune::imaging::types::StapleOptions mapStringToStaple(const std::string& value);
    static dune::imaging::types::PunchingOptions mapStringToPunchingOptions(const std::string& value);
    static dune::imaging::types::BookletMakingOptions mapStringToBookletMaker(const std::string& value);
    //dune::imaging::types::PrintQuality mapStringToPrintQuality2(const std::string& value); // renamed to avoid overload
    static dune::imaging::types::FoldingOptions mapStringToFolding(const std::string& value);
    static dune::imaging::types::MediaIdType mapStringToMediaTypeId(const std::string& value);
    static dune::imaging::types::MediaSizeId mapStringToMediaSizeId(const std::string& value);
    static dune::cdm::glossary_1::PlexMode mapStringToPlexMode(const std::string& value);
    CustomMediaDimensionUnit convertMediaSizeUnit(dune::framework::utils::XmlUtils& xml, const std::string& xPath);
    dune::framework::core::APIResult readXml(
        dune::framework::utils::XmlUtils& xml,
        const dune::framework::data::conversion::DataDescriptor& fileDescriptor,
        std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& jobTicketTable);
    
    dune::framework::core::APIResult performConversion(
        dune::framework::utils::XmlUtils& xml,
        dune::cdm::jobTicket_1::PrintTable* printOptions);
    
    template<typename T, typename ConversionFunc>
    static void convertXml(
        dune::framework::utils::XmlUtils& xml,
        const std::string& xpath,
        dune::cdm::easyBuffers::OptionalProperty<T>& property,
        ConversionFunc mapper);
};

}}}}  // namespace dune::copy::Jobs::Copy

#endif  // DUNE_COPY_JOBS_COPY_PRINT_JOLT_TO_DUNE_CONVERTER_H