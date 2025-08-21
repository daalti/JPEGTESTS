#ifndef DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_LARGE_FORMAT_PARSER_HELPER_H
#define DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_LARGE_FORMAT_PARSER_HELPER_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesLargeFormatParserHelper.h
 * @date   Tue, 11 Oct 2022 11:20:06 +0200
 * @brief  Helper used to manage parser of Dynamic Copy Job Constraints on flatbuffer
 * @author yago.cordero.carrera@hp.com (Cordero Carrera, Yago)
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobDynamicConstraintRulesLargeFormatMapper.h"
#include "ILocaleProvider.h"
#include "Constraints.h"
#include "com.hp.cdm.service.jobTicket.version.1.easybuffers_autogen.h"

using dune::cdm::jobTicket_1::JobTicketTable;
namespace dune { namespace copy { namespace Jobs { namespace Copy {

namespace FlatBufferParserToCdmType
{
    // * Helper Methods
    /**
     * @brief Method to Compare two CopyIntentValuesUnion  
     * @param firstUnion one union to compare
     * @param secondUnion next union
     * @return true if unions have the same type and same value
     * @return false if no
     */
    bool compareUnionValue(CopyIntentValuesUnion firstUnion, CopyIntentValuesUnion secondUnion);

    /**
     * @brief Set the Values On Constraint object     
     * @param values union values from fbs
     * @param constraint new constraint to add values
     * @param staticConstraints previous static constraints
     * @param stringLocalized string from localization, that normally will comes from csf file
     */
    void setValuesOnConstraint(std::vector<std::shared_ptr<CopyIntentTableValueT>> tableValues, 
        std::shared_ptr<dune::framework::data::constraints::Constraints> constraint, 
        std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints, 
        const std::string &stringLocalized);

    // * Base parser to cdm specific methods
    /**
     * @brief Parse a Intent Value Union to expected cdm value     
     * @tparam CdmType template to indicate type for cdm
     * @param value union value from flatbuffer
     * @return CdmType cdm type result
     */
    template<typename CdmType>
    inline CdmType parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value);

    // Different parser execution. 
    // ? Add new method here if there is any missed item parsing that is need to be supported

    template<>
    inline int8_t parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsINT8() != nullptr,"Not INT8 value, unsupported parse");
        return value.AsINT8()->value;
    }

    template<>
    inline int16_t parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsINT16() != nullptr,"Not INT16 value, unsupported parse");
        return value.AsINT16()->value;
    }

    template<>
    inline int32_t parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsINT32() != nullptr,"Not INT32 value, unsupported parse");
        return value.AsINT32()->value;
    }

    template<>
    inline int64_t parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsINT64() != nullptr,"Not INT64 value, unsupported parse");
        return value.AsINT64()->value;
    }

    template<>
    inline uint8_t parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsUINT8() != nullptr,"Not UINT8 value, unsupported parse");
        return value.AsUINT8()->value;
    }

    template<>
    inline uint16_t parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsUINT16() != nullptr,"Not UINT16 value, unsupported parse");
        return value.AsUINT16()->value;
    }

    template<>
    inline uint32_t parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsUINT32() != nullptr,"Not UINT32 value, unsupported parse");
        return value.AsUINT32()->value;
    }

    template<>
    inline uint64_t parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsUINT64() != nullptr,"Not UINT64 value, unsupported parse");
        return value.AsUINT64()->value;
    }

    template<>
    inline double parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsDOUBLE() != nullptr,"Not DOUBLE value, unsupported parse");
        return value.AsDOUBLE()->value;
    }

    template<>
    inline dune::cdm::glossary_1::FeatureEnabledEnum parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsBOOL() != nullptr,"Not BOOL value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsBOOL()->value);            
    }

    template<>
    inline dune::cdm::glossary_1::ScanMediaType parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsOriginalMediaType() != nullptr,"Not OriginalMediaType value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsOriginalMediaType()->value);
    }
         
    template <>
    inline dune::cdm::glossary_1::ScanMediaSourceId parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsScanSource() != nullptr,"Not ScanSource value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsScanSource()->value);
    }

    template <>
    inline dune::cdm::jobTicket_1::ScanCaptureMode parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsScanCaptureModeType() != nullptr,"Not ScanCaptureModeType value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsScanCaptureModeType()->value);
    }

    template <>
    inline dune::cdm::jobTicket_1::CcdChannel parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsCcdChannelEnum() != nullptr,"Not CcdChannelEnum value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsCcdChannelEnum()->value);
    }

    template <>
    inline dune::cdm::jobTicket_1::BinaryRendering parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsBinaryRenderingEnum() != nullptr,"Not BinaryRenderingEnum value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsBinaryRenderingEnum()->value);
    }

    template <>
    inline dune::cdm::jobTicket_1::AutoColorDetect parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsAutoColorDetectEnum() != nullptr,"Not AutoColorDetectEnum value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsAutoColorDetectEnum()->value);
    }
        
    template <>
    inline dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsImagePreview() != nullptr,"Not ImagePreview value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsImagePreview()->value);
    }

    template <>
    inline dune::cdm::jobTicket_1::scaling::ScaleSelection parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsScanScaleSelectionEnum() != nullptr,"Not ScanScaleSelectionEnum value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsScanScaleSelectionEnum()->value);
    }

    template <>
    inline dune::cdm::jobTicket_1::ScanAcquisitionsSpeed parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsScanAcquisitionsSpeedEnum() != nullptr,"Not ScanAcquisitionsSpeedEnum value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsScanAcquisitionsSpeedEnum()->value);
    }

    template <>
    inline dune::cdm::jobTicket_1::ColorModes parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsColorMode() != nullptr,"Not ColorMode value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsColorMode()->value);
    }

    template <>
    inline dune::cdm::glossary_1::ContentOrientation parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsContentOrientation() != nullptr,"Not ContentOrientation value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsContentOrientation()->value);
    }

    template <>
    inline dune::cdm::jobTicket_1::ContentType parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsOriginalContentType() != nullptr,"Not OriginalContentType value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsOriginalContentType()->value);
    }

    template <>
    inline dune::cdm::glossary_1::MediaSize parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsMediaSizeId() != nullptr,"Not MediaSizeId value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsMediaSizeId()->value);
    }

    template <>
    inline dune::cdm::glossary_1::PlexMode parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsPlex() != nullptr,"Not Plex value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsPlex()->value);
    }

    template <>
    inline dune::cdm::glossary_1::DuplexBinding parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsPlexBinding() != nullptr,"Not PlexBinding value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsPlexBinding()->value);
    }

    template <>
    inline dune::cdm::jobTicket_1::Resolutions parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsResolution() != nullptr,"Not Resolution value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsResolution()->value);
    }

    template <>
    inline dune::cdm::glossary_1::MediaSourceId parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsMediaSource() != nullptr,"Not MediaSource value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsMediaSource()->value);
    }

    template <>
    inline dune::cdm::jobTicket_1::OutputCanvasAnchor parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsOutputCanvasAnchorType() != nullptr,"Not OutputCanvasAnchorType value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsOutputCanvasAnchorType()->value);
    }

    template <>
    inline dune::cdm::glossary_1::MediaType parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsMediaIdType() != nullptr,"Not MediaIdType value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsMediaIdType()->value);
    }

    template <>
    inline dune::cdm::glossary_1::MediaDestinationId parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsMediaDestinationId() != nullptr,"Not MediaDestinationId value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsMediaDestinationId()->value);
    }

    template <>
    inline dune::cdm::glossary_1::PrintQuality parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsPrintQuality() != nullptr,"Not PrintQuality value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsPrintQuality()->value);
    }

    template <>
    inline dune::cdm::jobTicket_1::PrintingOrder parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsPrintingOrder() != nullptr,"Not PrintingOrder value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsPrintingOrder()->value);
    }

    template <>
    inline dune::cdm::jobTicket_1::RotateEnum parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsRotate() != nullptr,"Not Rotate value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsRotate()->value);
    }

    template <>
    inline dune::cdm::mediaProfile_1::MediaFamilyEnum parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsMediaFamily() != nullptr,"Not MediaFamily value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsMediaFamily()->value);
    }

    template <>
    inline dune::cdm::jobTicket_1::PrintMargins parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsCopyMargins() != nullptr,"Not CopyMargins value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsCopyMargins()->value);
    }

    template <>
    inline dune::cdm::jobTicket_1::PagesPerSheet parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsCopyOutputNumberUpCount() != nullptr,"Not CopyOutputNumberUpCount value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsCopyOutputNumberUpCount()->value);
    }

    template <>
    inline dune::cdm::jobTicket_1::CollateModes parseFlatBufferEnumTypeValueToCdmType(CopyIntentValuesUnion value)
    {
        assert_msg(value.AsSheetCollate() != nullptr,"Not SheetCollate value, unsupported parse");
        return dune::job::cdm::mapToCdm(value.AsSheetCollate()->value);
    }

    /**
     * @brief Create a Copy Intent Union Value object     
     * @param enumType expected type from flatbuffer union enum
     * @param fbTable pointer for union internal value
     * @return std::shared_ptr<CopyIntentTableValueT> shared pointer result expected
     */
    template<typename FbTable>
    inline std::shared_ptr<CopyIntentTableValueT> createCopyIntentUnionValue(CopyIntentValues enumType, FbTable* fbTable)
    {
        auto unionValue = CopyIntentValuesUnion();
        unionValue.type = enumType;
        unionValue.value = fbTable;
        auto sharedTable = std::make_shared<CopyIntentTableValueT>();
        sharedTable->unionValue = unionValue;
        return sharedTable;
    }

    /**
     * @brief Methods to parse any cdm type supported to their fb table expected     
     * @param enumType type expected of table
     * @param value value from cdm
     * @return std::shared_ptr<CopyIntentTableValueT> shared pointer of fb table
     */
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::FeatureEnabled value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::FeatureEnabledEnum value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::ScanMediaType value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::ScanMediaSourceId value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::ScanCaptureMode value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::CcdChannel value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::BinaryRendering value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::AutoColorDetect value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::scaling::ScaleSelection value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::ScanAcquisitionsSpeed value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::ColorModes value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::ContentOrientation value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::ContentType value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::MediaSize value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::PlexMode value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::DuplexBinding value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::Resolutions value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::MediaSourceId value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::OutputCanvasAnchor value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::OutputCanvasAnchor value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::MediaType value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::MediaDestinationId value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::PrintQuality value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::PrintingOrder value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::RotateEnum value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::mediaProfile_1::MediaFamilyEnum value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::PrintMargins value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::PagesPerSheet value);
    std::shared_ptr<CopyIntentTableValueT> parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::CollateModes value);

    // * Parsers Methods to specific Contraint from
    // ? If there any parser from a flatbuffer type on config that is not here and it's needed to convert to constraints values
    // ? Create a new method on this case and insert on switch / case setValuesOnConstraint
    /**
     * @brief Parser a MinMaxLengthUint to the expected constraint equivalence -> Max Length, Min Length
     * @param values union encapsulation vector
     * @param constraint new constraint to add values
     * @param stringLocalized string from localization, that normally will comes from csf file
     */
    void parseMinMaxLengthUintOnConstraint(std::vector<std::shared_ptr<CopyIntentTableValueT>> tableValues, std::shared_ptr<dune::framework::data::constraints::Constraints> constraint, const std::string &stringLocalized);

    /**
     * @brief Parser a MinMaxCountUint to the expected constraint equivalence -> Max Count, Min Count
     * @param values union encapsulation vector
     * @param constraint new constraint to add values
     * @param stringLocalized string from localization, that normally will comes from csf file
     */
    void parseMinMaxCountUintOnConstraint(std::vector<std::shared_ptr<CopyIntentTableValueT>> tableValues, std::shared_ptr<dune::framework::data::constraints::Constraints> constraint, const std::string &stringLocalized);

    /**
     * @brief Parse a text to the expected constraint equivalence -> Regular Expresion, Max Length, Min Length
     * @param values union encapsulation vector
     * @param constraint new constraint to add values
     * @param stringLocalized string from localization, that normally will comes from csf file
     */
    void parseTextOnConstraint(std::vector<std::shared_ptr<CopyIntentTableValueT>> tableValues, std::shared_ptr<dune::framework::data::constraints::Constraints> constraint, const std::string &stringLocalized);

    /**
     * @brief Parse a RangeValueInt to the expected constraint equivalence -> RangeInt     
     * @param values union encapsulation vector
     * @param constraint new constraint to add values
     * @param stringLocalized string from localization, that normally will comes from csf file
     */
    void parseRangeValueIntOnConstraint(std::vector<std::shared_ptr<CopyIntentTableValueT>> tableValues, std::shared_ptr<dune::framework::data::constraints::Constraints> constraint, const std::string &stringLocalized);

    /**
     * @brief Parse a RangeValueDouble to the expected constraint equivalence -> RangeDouble
     * @param values union encapsulation vector
     * @param constraint new constraint to add values
     * @param stringLocalized string from localization, that normally will comes from csf file
     */
    void parseRangeValueDoubleOnConstraint(std::vector<std::shared_ptr<CopyIntentTableValueT>> tableValues, std::shared_ptr<dune::framework::data::constraints::Constraints> constraint, const std::string &stringLocalized);

    /**
     * @brief Parse a number value to the expect contraint equivalence -> Number    
     * @tparam NumberType template basic value number type.       
     * @param values union encapsulation vector
     * @param constraint new constraint to add values
     * @param stringLocalized string from localization, that normally will comes from csf file
     */
    template <typename NumberType>
    void parseLimitNumberOnConstraint(std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints, 
        std::vector<std::shared_ptr<CopyIntentTableValueT>> tableValues, 
        std::shared_ptr<dune::framework::data::constraints::Constraints> constraint, 
        const std::string &stringLocalized);

    /**
     * @brief Parse a TableEnum type from fbs to the expected constraint equivalence -> ValidValuesEnum
     * @tparam CdmType template enum type to enum cdm type to parser. 
     * @param values union encapsulation vector
     * @param constraint new constraint to add values
     * @param stringLocalized string from localization, that normally will comes from csf file
     */
    template <typename CdmType>
    void parseValidEnumOnConstraint(std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints, 
        std::vector<std::shared_ptr<CopyIntentTableValueT>> tableValues, std::shared_ptr<dune::framework::data::constraints::Constraints> constraint, 
        const std::string &stringLocalized);

    /**
     * @brief Parse a TableEnum type from fbs to the expected constraint equivalence -> PossibleValuesEnum, PossibleValuesShort, PossibleValuesBool, PossibleValuesString
     * @tparam CdmType template enum type to enum cdm type to parser. 
     * @param values union encapsulation vector
     * @param constraint new constraint to add values
     * @param stringLocalized string from localization, that normally will comes from csf file
     */
    template <typename CdmType>
    void parsePossibleEnumOnConstraint(std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints, 
        std::shared_ptr<dune::framework::data::constraints::Constraints> newConstraint, 
        const std::string &stringLocalized);

    /**
     * @brief Method to obtain the string representation of an intent value, doing parsing to cdm and then with toString method
     * @param value TableValue
     * @param localizedFromMethod flag to notify when intent is localized from here
     * @return std::string result as string
     */
    std::string parseCopyIntentTableValueToString(std::shared_ptr<CopyIntentTableValueT> value, bool& localizedFromMethod, dune::localization::ILocaleProvider *localization = nullptr);

    /**
     * @brief Get the Values Not Allowed For Enum object     
     * @tparam CdmType type of cdm to be parsed internally
     * @param constraintValues valid values to be ignored
     * @param originalConstraints original values to take possible or range values expected
     * @return std::vector<std::shared_ptr<CopyIntentTableValueT>> result
     */
    template <typename CdmType>
    std::vector<std::shared_ptr<CopyIntentTableValueT>> getValuesNotAllowedForEnum(std::shared_ptr<ConstrainedValuesT> constraintValues, std::shared_ptr<dune::framework::data::constraints::Constraints> originalConstraints);

    /**
     * @brief Get the Values Not Allowed For U Int object      
     * @tparam FbCast cast to flatbuffer type
     * @param constraintValues new values to generate filter
     * @return std::vector<std::shared_ptr<CopyIntentTableValueT>> result
     */
    template<typename FbCast>
    std::vector<std::shared_ptr<CopyIntentTableValueT>> getValuesNotAllowedForUInt(std::shared_ptr<ConstrainedValuesT> constraintValues);

    /**
     * @brief Get the Values Not Allowed For Int object     
     * @tparam FbCast cast to flatbuffer type only uint are supported
     * @param constraintValues new values to generate filter
     * @return std::vector<std::shared_ptr<CopyIntentTableValueT>> result
     */
    template<typename FbCast>
    std::vector<std::shared_ptr<CopyIntentTableValueT>> getValuesNotAllowedForInt(std::shared_ptr<ConstrainedValuesT> constraintValues);

    /**
     * @brief Get the Values Not Allowed For Double object
     * @param constraintValues new values to generate filter
     * @return std::vector<std::shared_ptr<CopyIntentTableValueT>> result
     */
    std::vector<std::shared_ptr<CopyIntentTableValueT>> getValuesNotAllowedForDouble(std::shared_ptr<ConstrainedValuesT> constraintValues);

    /**
     * @brief Get the Values Not Allowed object 
     * @param constraintValues current values accepted 
     * @param originalConstraints constraints with all possibilities, relative to specific setting to check
     * @return std::vector<std::shared_ptr<CopyIntentTableValueT>> 
     */
    std::vector<std::shared_ptr<CopyIntentTableValueT>> getValuesNotAllowed(std::shared_ptr<ConstrainedValuesT> constraintValues, std::shared_ptr<dune::framework::data::constraints::Constraints> originalConstraints);
};

namespace CopyTicketCheckerFromFlatBufferEnum
{
    /**
     * @brief Main method to call to compare value on ticket     
     * @param ticketType enum to indicate field that must to be checked on ticket
     * @param value value from flatbuffer
     * @param ticket copy ticket
     * @return true if value is on current
     * @return false if value is not on current ticket or enum is not currently supported
     */
    bool compareValueOnTicket(const std::string &ticketType, CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket);

    /**
     * @brief Main method to call to compare value on a ticket table
     * @param ticketType enum to indicate field that must to be checked on ticket
     * @param value value from flatbuffer
     * @param ticketTable copy ticket table
     * @param bool& settingIsSetOnCdm param as reference to indicate if setting is in cdm and should be taken as main current value to check.
     * @return true if value is on current
     * @return false if value is not on current ticket or enum is not currently supported
     */
    bool compareValueOnTicketTable(const std::string &ticketSetting, CopyIntentValuesUnion value, std::shared_ptr<JobTicketTable> ticketTable, bool& settingIsSetOnCdm);
};

namespace CopyTicketCdmHelper
{
    /**
     * @brief Method to check if a value is needed to be changed on update of current ticket
     * @param cdmSettingPath cdm path of the setting to check
     * @param updatedJobTicketTable job ticket table with new values to check the new value to deserialize
     * @param ticket current ticket values
     * @param currentConstraintsGroup current constraints
     * @param checkCurrentIntent if ticket should be checked, or otherwise only use the updatedJobTicketTable
     * @return true if setting is needed to be updated
     * @return false if setting not need to be updated
     */
    bool checkIfValueNeedToBeUpdatedOnJobTicketTable(const std::string &cdmSettingPath,
        const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, 
        std::shared_ptr<ICopyJobTicket> ticket, 
        std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints,
        bool checkCurrentIntent = true);

    /**
     * @brief Method to update a value on job ticket table, based on accepted from constraints  
     * @param cdmSettingPath cdm path of the setting to check
     * @param updatedJobTicketTable job ticket table to set a new value
     * @param currentConstraints current constraints for actual setting
     */
    bool updateValue(const std::string &cdmSettingPath, 
        const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, 
        std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints);
};

}}}}  // namespace dune::copy::Jobs::Copy

#endif // DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_LARGE_FORMAT_PARSER_HELPER_H