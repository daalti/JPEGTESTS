///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesLargeFormatParserHelper.cpp
 * @date   Tue, 11 Oct 2022 11:20:06 +0200
 * @brief  Helper used to manage parser of Dynamic Copy Job Constraints on flatbuffer
 * @author yago.cordero.carrera@hp.com (Cordero Carrera, Yago)
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobDynamicConstraintRulesLargeFormatParserHelper.h"
#include "common_debug.h"
#include "CopyJobDynamicConstraintRulesLargeFormatParserHelper_TraceAutogen.h"
#include "ParameterizedString.h"
#include "StringIds.h"
#include "RegularExpression.h"
#include "PossibleValues.h"
#include "ILocale.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

bool FlatBufferParserToCdmType::compareUnionValue(CopyIntentValuesUnion firstUnion, CopyIntentValuesUnion secondUnion)
{
    bool result = false;

    assert_msg(firstUnion.type == secondUnion.type, "Comparing unions with different type, error check, review current csf file, must to be any type bad set or a new getter on cpp helper it's wrong");
    
    switch (firstUnion.type)
    {
        case CopyIntentValues::MinMaxLengthUInt:
            result = firstUnion.AsMinMaxLengthUInt()->minLength == secondUnion.AsMinMaxLengthUInt()->minLength && 
                     firstUnion.AsMinMaxLengthUInt()->maxLength == secondUnion.AsMinMaxLengthUInt()->maxLength;
            break;
        case CopyIntentValues::TEXT:
            result = firstUnion.AsTEXT()->regularExpression == secondUnion.AsTEXT()->regularExpression &&
                     firstUnion.AsTEXT()->length->minLength  == secondUnion.AsTEXT()->length->minLength &&
                     firstUnion.AsTEXT()->length->maxLength  == secondUnion.AsTEXT()->length->maxLength;
            break;
        case CopyIntentValues::RangeValueInt:
            result = firstUnion.AsRangeValueInt()->min  == secondUnion.AsRangeValueInt()->min &&
                     firstUnion.AsRangeValueInt()->max  == secondUnion.AsRangeValueInt()->max &&
                     firstUnion.AsRangeValueInt()->step == secondUnion.AsRangeValueInt()->step;
            break;
        case CopyIntentValues::RangeValueDouble:
            result = firstUnion.AsRangeValueDouble()->min  == secondUnion.AsRangeValueDouble()->min &&
                     firstUnion.AsRangeValueDouble()->max  == secondUnion.AsRangeValueDouble()->max &&
                     firstUnion.AsRangeValueDouble()->step == secondUnion.AsRangeValueDouble()->step;
            break;
        case CopyIntentValues::BOOL:
            result = firstUnion.AsBOOL()->value == secondUnion.AsBOOL()->value;
            break;
        case CopyIntentValues::AttachmentSize:
            result = firstUnion.AsAttachmentSize()->value == secondUnion.AsAttachmentSize()->value;
            break;
        case CopyIntentValues::OriginalMediaType:
            result = firstUnion.AsOriginalMediaType()->value == secondUnion.AsOriginalMediaType()->value;
            break;
        case CopyIntentValues::ScanSource:
            result = firstUnion.AsScanSource()->value == secondUnion.AsScanSource()->value;
            break;
        case CopyIntentValues::ScanFeedOrientation:
            result = firstUnion.AsScanFeedOrientation()->value == secondUnion.AsScanFeedOrientation()->value;
            break;
        case CopyIntentValues::BlankDetectEnum:
            result = firstUnion.AsBlankDetectEnum()->value == secondUnion.AsBlankDetectEnum()->value;
            break;
        case CopyIntentValues::OverScanType:
            result = firstUnion.AsOverScanType()->value == secondUnion.AsOverScanType()->value;
            break;
        case CopyIntentValues::ScanCaptureModeType:
            result = firstUnion.AsScanCaptureModeType()->value == secondUnion.AsScanCaptureModeType()->value;
            break;
        case CopyIntentValues::ScanImagingProfileType:
            result = firstUnion.AsScanImagingProfileType()->value == secondUnion.AsScanImagingProfileType()->value;
            break;
        case CopyIntentValues::CcdChannelEnum:
            result = firstUnion.AsCcdChannelEnum()->value == secondUnion.AsCcdChannelEnum()->value;
            break;
        case CopyIntentValues::BinaryRenderingEnum:
            result = firstUnion.AsBinaryRenderingEnum()->value == secondUnion.AsBinaryRenderingEnum()->value;
            break;
        case CopyIntentValues::AutoColorDetectEnum:
            result = firstUnion.AsAutoColorDetectEnum()->value == secondUnion.AsAutoColorDetectEnum()->value;
            break;
        case CopyIntentValues::ImagePreview:
            result = firstUnion.AsImagePreview()->value == secondUnion.AsImagePreview()->value;
            break;
        case CopyIntentValues::ScanScaleSelectionEnum:
            result = firstUnion.AsScanScaleSelectionEnum()->value == secondUnion.AsScanScaleSelectionEnum()->value;
            break;
        case CopyIntentValues::ScanAcquisitionsSpeedEnum:
            result = firstUnion.AsScanAcquisitionsSpeedEnum()->value == secondUnion.AsScanAcquisitionsSpeedEnum()->value;
            break;
        case CopyIntentValues::ColorMode:
            result = firstUnion.AsColorMode()->value == secondUnion.AsColorMode()->value;
            break;
        case CopyIntentValues::ContentOrientation:
            result = firstUnion.AsContentOrientation()->value == secondUnion.AsContentOrientation()->value;
            break;
        case CopyIntentValues::OriginalContentType:
            result = firstUnion.AsOriginalContentType()->value == secondUnion.AsOriginalContentType()->value;
            break;
        case CopyIntentValues::MediaSizeId:
            result = firstUnion.AsMediaSizeId()->value == secondUnion.AsMediaSizeId()->value;
            break;
        case CopyIntentValues::Plex:
            result = firstUnion.AsPlex()->value == secondUnion.AsPlex()->value;
            break;
        case CopyIntentValues::PlexBinding:
            result = firstUnion.AsPlexBinding()->value == secondUnion.AsPlexBinding()->value;
            break;
        case CopyIntentValues::Resolution:
            result = firstUnion.AsResolution()->value == secondUnion.AsResolution()->value;
            break;
        case CopyIntentValues::MediaSource:
            result = firstUnion.AsMediaSource()->value == secondUnion.AsMediaSource()->value;
            break;
        case CopyIntentValues::OutputCanvas:
            result = firstUnion.AsOutputCanvas()->value == secondUnion.AsOutputCanvas()->value;
            break;
        case CopyIntentValues::OutputCanvasAnchorType:
            result = firstUnion.AsOutputCanvasAnchorType()->value == secondUnion.AsOutputCanvasAnchorType()->value;
            break;
        case CopyIntentValues::MediaOrientation:
            result = firstUnion.AsMediaOrientation()->value == secondUnion.AsMediaOrientation()->value;
            break;
        case CopyIntentValues::MediaIdType:
            result = firstUnion.AsMediaIdType()->value == secondUnion.AsMediaIdType()->value;
            break;
        case CopyIntentValues::MediaDestinationId:
            result = firstUnion.AsMediaDestinationId()->value == secondUnion.AsMediaDestinationId()->value;
            break;
        case CopyIntentValues::PrintQuality:
            result = firstUnion.AsPrintQuality()->value == secondUnion.AsPrintQuality()->value;
            break;
        case CopyIntentValues::PrintingOrder:            
            result = firstUnion.AsPrintingOrder()->value == secondUnion.AsPrintingOrder()->value;
            break;  
        case CopyIntentValues::Rotate:            
            result = firstUnion.AsRotate()->value == secondUnion.AsRotate()->value;
            break;  
        case CopyIntentValues::MediaFamily:            
            result = firstUnion.AsMediaFamily()->value == secondUnion.AsMediaFamily()->value;
            break;  
        case CopyIntentValues::CopyMargins:
            result = firstUnion.AsCopyMargins()->value == secondUnion.AsCopyMargins()->value;
            break;
        case CopyIntentValues::CopyOutputNumberUpCount:
            result = firstUnion.AsCopyOutputNumberUpCount()->value == secondUnion.AsCopyOutputNumberUpCount()->value;
            break;
        case CopyIntentValues::SheetCollate:
            result = firstUnion.AsSheetCollate()->value == secondUnion.AsSheetCollate()->value;
            break;
        case CopyIntentValues::INT8:
            result = firstUnion.AsINT8()->value == secondUnion.AsINT8()->value;
            break;
        case CopyIntentValues::INT16:
            result = firstUnion.AsINT16()->value == secondUnion.AsINT16()->value;
            break;
        case CopyIntentValues::INT32:
            result = firstUnion.AsINT32()->value == secondUnion.AsINT32()->value;
            break;
        case CopyIntentValues::INT64:
            result = firstUnion.AsINT64()->value == secondUnion.AsINT64()->value;
            break;
        case CopyIntentValues::UINT8:
            result = firstUnion.AsUINT8()->value == secondUnion.AsUINT8()->value;
            break;
        case CopyIntentValues::UINT16:
            result = firstUnion.AsUINT16()->value == secondUnion.AsUINT16()->value;
            break;
        case CopyIntentValues::UINT32:
            result = firstUnion.AsUINT32()->value == secondUnion.AsUINT32()->value;
            break;
        case CopyIntentValues::UINT64:
            result = firstUnion.AsUINT64()->value == secondUnion.AsUINT64()->value;
            break;
        case CopyIntentValues::DOUBLE:            
            result = firstUnion.AsDOUBLE()->value == secondUnion.AsDOUBLE()->value;
            break;
        case CopyIntentValues::NONE:
        default:
            break;
    }
    
    return result;
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::FeatureEnabled value)
{
    auto internalTable = new BOOLT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<BOOLT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::FeatureEnabledEnum value)
{
    auto internalTable = new BOOLT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<BOOLT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::ScanMediaType value)
{
    auto internalTable = new OriginalMediaTypeT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<OriginalMediaTypeT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::ScanMediaSourceId value)
{
    auto internalTable = new ScanSourceT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<ScanSourceT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::ScanCaptureMode value)
{
    auto internalTable = new ScanCaptureModeTypeT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<ScanCaptureModeTypeT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::CcdChannel value)
{
    auto internalTable = new CcdChannelEnumT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<CcdChannelEnumT>(enumType,internalTable);
}  

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::BinaryRendering value)
{
    auto internalTable = new BinaryRenderingEnumT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<BinaryRenderingEnumT>(enumType,internalTable);
}    

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::AutoColorDetect value)
{
    auto internalTable = new AutoColorDetectEnumT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<AutoColorDetectEnumT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration value)
{
    auto internalTable = new ImagePreviewT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<ImagePreviewT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::scaling::ScaleSelection value)
{
    auto internalTable = new ScanScaleSelectionEnumT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<ScanScaleSelectionEnumT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::ScanAcquisitionsSpeed value)
{
    auto internalTable = new ScanAcquisitionsSpeedEnumT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<ScanAcquisitionsSpeedEnumT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::ColorModes value)
{
    auto internalTable = new ColorModeT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<ColorModeT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::ContentOrientation value)
{
    auto internalTable = new ContentOrientationT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<ContentOrientationT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::ContentType value)
{
    auto internalTable = new OriginalContentTypeT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<OriginalContentTypeT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::MediaSize value)
{
    auto internalTable = new MediaSizeIdT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<MediaSizeIdT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::PlexMode value)
{
    auto internalTable = new PlexT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<PlexT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::DuplexBinding value)
{
    auto internalTable = new PlexBindingT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<PlexBindingT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::Resolutions value)
{
    auto internalTable = new ResolutionT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<ResolutionT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::MediaSourceId value)
{
    auto internalTable = new MediaSourceT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<MediaSourceT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::OutputCanvasAnchor value)
{
    auto internalTable = new OutputCanvasAnchorTypeT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<OutputCanvasAnchorTypeT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::MediaType value)
{
    auto internalTable = new MediaIdTypeT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<MediaIdTypeT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::MediaDestinationId value)
{
    auto internalTable = new MediaDestinationIdT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<MediaDestinationIdT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::glossary_1::PrintQuality value)
{
    auto internalTable = new PrintQualityT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<PrintQualityT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::PrintingOrder value)
{
    auto internalTable = new PrintingOrderT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<PrintingOrderT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::RotateEnum value)
{
    auto internalTable = new RotateT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<RotateT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::mediaProfile_1::MediaFamilyEnum value)
{
    auto internalTable = new MediaFamilyT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<MediaFamilyT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::PrintMargins value)
{
    auto internalTable = new CopyMarginsT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<CopyMarginsT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::PagesPerSheet value)
{
    auto internalTable = new CopyOutputNumberUpCountT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<CopyOutputNumberUpCountT>(enumType,internalTable);
}

std::shared_ptr<CopyIntentTableValueT> FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(CopyIntentValues enumType, dune::cdm::jobTicket_1::CollateModes value)
{
    auto internalTable = new SheetCollateT();
    internalTable->value = dune::job::cdm::mapFromCdm(value);
    return createCopyIntentUnionValue<SheetCollateT>(enumType,internalTable);
}

void FlatBufferParserToCdmType::setValuesOnConstraint(std::vector<std::shared_ptr<CopyIntentTableValueT>> tableValues, 
    std::shared_ptr<dune::framework::data::constraints::Constraints> constraint, 
    std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints, 
    const std::string &stringLocalized)
{
    // Check that type coincidence between all values in vector.
    auto unionType = tableValues[0]->unionValue.type;
    for(auto unionValueTable : tableValues)
    {
        assert_msg(unionType == unionValueTable->unionValue.type,"Type between union not coincidence, report as an error");
    }

    switch (unionType)
    {
        case CopyIntentValues::INT8:
            FlatBufferParserToCdmType::parseLimitNumberOnConstraint<int8_t>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::INT16:
            FlatBufferParserToCdmType::parseLimitNumberOnConstraint<int16_t>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::INT32:
            FlatBufferParserToCdmType::parseLimitNumberOnConstraint<int32_t>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::INT64:
            FlatBufferParserToCdmType::parseLimitNumberOnConstraint<int64_t>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::UINT8:
            FlatBufferParserToCdmType::parseLimitNumberOnConstraint<uint8_t>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::UINT16:
            FlatBufferParserToCdmType::parseLimitNumberOnConstraint<uint16_t>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::UINT32:
            FlatBufferParserToCdmType::parseLimitNumberOnConstraint<uint32_t>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::UINT64:
            FlatBufferParserToCdmType::parseLimitNumberOnConstraint<uint64_t>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::DOUBLE:
            FlatBufferParserToCdmType::parseLimitNumberOnConstraint<double>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::MinMaxLengthUInt:
            FlatBufferParserToCdmType::parseMinMaxLengthUintOnConstraint(tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::TEXT:
            FlatBufferParserToCdmType::parseTextOnConstraint(tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::RangeValueInt:
            FlatBufferParserToCdmType::parseRangeValueIntOnConstraint(tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::RangeValueDouble:
            FlatBufferParserToCdmType::parseRangeValueDoubleOnConstraint(tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::BOOL:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::glossary_1::FeatureEnabledEnum>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::glossary_1::FeatureEnabledEnum>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::AttachmentSize:
            // Currently not supported on constraints
            // FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<>(staticConstraints,constraint,stringLocalized);
            // FlatBufferParserToCdmType::parseValidEnumOnConstraint(staticConstraints,vtableValuesalues,constraint,stringLocalized);
            break;
        case CopyIntentValues::OriginalMediaType:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::glossary_1::ScanMediaType>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::glossary_1::ScanMediaType>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::ScanSource:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::glossary_1::ScanMediaSourceId>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::glossary_1::ScanMediaSourceId>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::ScanFeedOrientation:
            // Currently not supported on constraints
            // FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<>(staticConstraints,constraint,stringLocalized);
            // FlatBufferParserToCdmType::parseValidEnumOnConstraint(tableValues,constraint,stringLocalized)
            break;
        case CopyIntentValues::BlankDetectEnum:
            // Currently not supported on constraints
            // FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<>(staticConstraints,constraint,stringLocalized);
            // FlatBufferParserToCdmType::parseValidEnumOnConstraint(tableValues,constraint,stringLocalized)
            break;
        case CopyIntentValues::OverScanType:
            // Currently not supported on constraints
            // FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<>(staticConstraints,constraint,stringLocalized);
            // FlatBufferParserToCdmType::parseValidEnumOnConstraint(tableValues,constraint,stringLocalized)
            break;
        case CopyIntentValues::ScanCaptureModeType:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::ScanCaptureMode>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::ScanCaptureMode>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::ScanImagingProfileType:
            // Currently not supported on constraints
            // FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<>(staticConstraints,constraint,stringLocalized);
            // FlatBufferParserToCdmType::parseValidEnumOnConstraint(tableValues,constraint,stringLocalized)
            break;
        case CopyIntentValues::CcdChannelEnum:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::CcdChannel>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::CcdChannel>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::BinaryRenderingEnum:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::BinaryRendering>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::BinaryRendering>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::AutoColorDetectEnum:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::AutoColorDetect>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::AutoColorDetect>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::ImagePreview:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::ScanScaleSelectionEnum:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::scaling::ScaleSelection>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::scaling::ScaleSelection>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::ScanAcquisitionsSpeedEnum:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::ScanAcquisitionsSpeed>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::ScanAcquisitionsSpeed>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::ColorMode:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::ColorModes>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::ColorModes>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::ContentOrientation:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::glossary_1::ContentOrientation>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::glossary_1::ContentOrientation>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::OriginalContentType:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::ContentType>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::ContentType>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::MediaSizeId:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::glossary_1::MediaSize>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::glossary_1::MediaSize>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::Plex:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::glossary_1::PlexMode>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::glossary_1::PlexMode>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::PlexBinding:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::glossary_1::DuplexBinding>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::glossary_1::DuplexBinding>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::Resolution:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::Resolutions>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::Resolutions>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::MediaSource:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::glossary_1::MediaSourceId>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::glossary_1::MediaSourceId>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::OutputCanvas:
            // Special case, need to convert to more than one constraints on cdm
            // Not needed for the moment
            // FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::OutputCanvas>(staticConstraints,constraint,stringLocalized);
            // FlatBufferParserToCdmType::parseValidEnumOnConstraint(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::OutputCanvasAnchorType:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::OutputCanvasAnchor>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::OutputCanvasAnchor>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::MediaOrientation:
            // Special case, Not supported for the moment, complex constraint that could not apply
            // FlatBufferParserToCdmType::parsePossibleEnumOnConstraint(staticConstraints,constraint,stringLocalized);
            // FlatBufferParserToCdmType::parseValidEnumOnConstraint(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::MediaIdType:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::glossary_1::MediaType>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::glossary_1::MediaType>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::MediaDestinationId:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::glossary_1::MediaDestinationId>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::glossary_1::MediaDestinationId>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::PrintQuality:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::glossary_1::PrintQuality>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::glossary_1::PrintQuality>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::PrintingOrder:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::PrintingOrder>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::PrintingOrder>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::Rotate:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::RotateEnum>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::RotateEnum>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::MediaFamily:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::mediaProfile_1::MediaFamilyEnum>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::mediaProfile_1::MediaFamilyEnum>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::CopyMargins:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::PrintMargins>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::PrintMargins>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::CopyOutputNumberUpCount:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::PagesPerSheet>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::PagesPerSheet>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::SheetCollate:
            FlatBufferParserToCdmType::parsePossibleEnumOnConstraint<dune::cdm::jobTicket_1::CollateModes>(staticConstraints,constraint,stringLocalized);
            FlatBufferParserToCdmType::parseValidEnumOnConstraint<dune::cdm::jobTicket_1::CollateModes>(staticConstraints,tableValues,constraint,stringLocalized);
            break;
        case CopyIntentValues::NONE:
        default:
            break;
    }
}

void FlatBufferParserToCdmType::parseMinMaxLengthUintOnConstraint(std::vector<std::shared_ptr<CopyIntentTableValueT>> tableValues, 
    std::shared_ptr<dune::framework::data::constraints::Constraints> constraint, 
    const std::string &stringLocalized)
{
    assert_msg(tableValues.size() == 1,"Length constraints can't be more than one");

    auto lengthValue = tableValues[0]->unionValue.AsMinMaxLengthUInt();

    size_t maxLength{lengthValue->maxLength};
    size_t minLength{lengthValue->minLength};
    auto   maxLengthConstraint = std::make_unique<dune::framework::data::constraints::MaxLength>(maxLength, stringLocalized);
    auto   minLengthConstraint = std::make_unique<dune::framework::data::constraints::MinLength>(minLength, stringLocalized);

    constraint->add(std::move(maxLengthConstraint));
    constraint->add(std::move(minLengthConstraint));
}

void FlatBufferParserToCdmType::parseTextOnConstraint(std::vector<std::shared_ptr<CopyIntentTableValueT>> tableValues, 
    std::shared_ptr<dune::framework::data::constraints::Constraints> constraint, 
    const std::string &stringLocalized)
{
    assert_msg(tableValues.size() == 1,"Text constraints can't be more than one");

    auto textValue = tableValues[0]->unionValue.AsTEXT();

    auto regularExpressionConstraint = std::make_unique<dune::framework::data::constraints::RegularExpression>(textValue->regularExpression, stringLocalized);

    size_t maxLength{textValue->length->maxLength};
    size_t minLength{textValue->length->minLength};
    auto   maxLengthConstraint = std::make_unique<dune::framework::data::constraints::MaxLength>(maxLength, stringLocalized);
    auto   minLengthConstraint = std::make_unique<dune::framework::data::constraints::MinLength>(minLength, stringLocalized);

    constraint->add(std::move(regularExpressionConstraint));
    constraint->add(std::move(maxLengthConstraint));
    constraint->add(std::move(minLengthConstraint));
}

void FlatBufferParserToCdmType::parseRangeValueIntOnConstraint(std::vector<std::shared_ptr<CopyIntentTableValueT>> tableValues, 
    std::shared_ptr<dune::framework::data::constraints::Constraints> constraint, 
    const std::string &stringLocalized)
{
    assert_msg(tableValues.size() == 1,"Range int constraints can't be more than one");

    auto range = tableValues[0]->unionValue.AsRangeValueInt();

    // range - min, max, step - (on a number)
    auto rangeConstraint = std::make_unique<dune::framework::data::constraints::RangeInt>(range->min, range->max, range->step, stringLocalized);
    constraint->add(std::move(rangeConstraint));
}

void FlatBufferParserToCdmType::parseRangeValueDoubleOnConstraint(std::vector<std::shared_ptr<CopyIntentTableValueT>> tableValues, 
    std::shared_ptr<dune::framework::data::constraints::Constraints> constraint, 
    const std::string &stringLocalized)
{
    assert_msg(tableValues.size() == 1,"Range double constraints can't be more than one");

    auto range = tableValues[0]->unionValue.AsRangeValueDouble();
    // range - min, max, step - (on a number)
    auto rangeConstraint = std::make_unique<dune::framework::data::constraints::RangeDouble>(range->min, range->max, range->step, stringLocalized);
    constraint->add(std::move(rangeConstraint));
}

template <typename NumberType>
void FlatBufferParserToCdmType::parseLimitNumberOnConstraint(std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints,
    std::vector<std::shared_ptr<CopyIntentTableValueT>> tableValues, 
    std::shared_ptr<dune::framework::data::constraints::Constraints> constraint, 
    const std::string &stringLocalized)
{
    assert_msg(tableValues.size() == 1,"Number limit constraints expected not more than one");

    // If numeral has a previous range value, set too on dynamic constraints generated
    if(staticConstraints)
    {
        for(auto previousConstraint : staticConstraints->getConstraints())
        {
            if(previousConstraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::RANGE_INT)
            {
                auto castRangeIntValue = static_cast< dune::framework::data::constraints::RangeInt*>(previousConstraint);
                auto rangeConstraint = std::make_unique<dune::framework::data::constraints::RangeInt>(castRangeIntValue->getMin(), castRangeIntValue->getMax(), castRangeIntValue->getStep(), stringLocalized);            
                constraint->add(std::move(rangeConstraint));
                break;
            }
            else if(previousConstraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::RANGE_DOUBLE)
            {
                auto castRangeDoubleValue = static_cast< dune::framework::data::constraints::RangeDouble*>(previousConstraint);
                auto rangeConstraint = std::make_unique<dune::framework::data::constraints::RangeDouble>(castRangeDoubleValue->getMin(), castRangeDoubleValue->getMax(), castRangeDoubleValue->getStep(), stringLocalized);            
                constraint->add(std::move(rangeConstraint));
                break;
            }
        }
    }

    // Create Possible/Valid number limitation
    NumberType value = Map2CheckerTicketMethod::getValue<NumberType>(tableValues[0]->unionValue);
    std::vector<NumberType> values{value};

    auto enumPossibleValuesConstraint   = std::make_unique<dune::framework::data::constraints::PossibleValuesEnum<NumberType>>(values,
        [](const NumberType numberValue){return std::to_string(numberValue);},
        stringLocalized);        
    constraint->add(std::move(enumPossibleValuesConstraint));

    auto enumValidValuesConstraint      = std::make_unique<dune::framework::data::constraints::ValidValuesEnum<NumberType>>(values, stringLocalized);
    constraint->add(std::move(enumValidValuesConstraint));
}


template <typename CdmType>
void FlatBufferParserToCdmType::parseValidEnumOnConstraint(std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints,
    std::vector<std::shared_ptr<CopyIntentTableValueT>> tableValues, 
    std::shared_ptr<dune::framework::data::constraints::Constraints> constraint, 
    const std::string &stringLocalized)
{
    std::vector<CdmType> validValues = std::vector<CdmType>();
    std::vector<CdmType> previousValidValues;

    // Take previous valid values
    for(auto previousConstraint : staticConstraints->getConstraints())
    {
        if(previousConstraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM)
        {
            previousValidValues = (static_cast< dune::framework::data::constraints::ValidValuesEnum<CdmType>*>(previousConstraint))->getValidValues();
            break;
        }
        // Rest of valid values not accepted to be checked at this level for the moment.
    }

    // Take new notified supported valid values
    for(auto unionValueTable : tableValues)
    {
        CdmType cdmValue = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<CdmType>(unionValueTable->unionValue);

        auto iteratorConstraintValues = std::find(previousValidValues.begin(), previousValidValues.end(), cdmValue);

        // Not add accepted valid value, if static constraints not accept them as they expected.
        if (iteratorConstraintValues != previousValidValues.end())
        {
            validValues.push_back(cdmValue);
        }
    }

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<dune::framework::data::constraints::ValidValuesEnum<CdmType>>(validValues, stringLocalized);
    constraint->add(std::move(enumValidValuesConstraint));
}

template <typename CdmType>
void FlatBufferParserToCdmType::parsePossibleEnumOnConstraint(std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints,
    std::shared_ptr<dune::framework::data::constraints::Constraints> newConstraint, 
    const std::string &stringLocalized)
{
    // Search for possible values constraint, and add when find
    for(auto constraint : staticConstraints->getConstraints())
    {
        if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::POSSIBLE_VALUE_ENUM)
        {
            auto castPossibleValue = static_cast< dune::framework::data::constraints::PossibleValuesEnum<CdmType>*>(constraint);
            auto internalUnique = std::make_unique<dune::framework::data::constraints::PossibleValuesEnum<CdmType>>(castPossibleValue->getPossibleValues(),&CdmType::valueToString,stringLocalized);
            newConstraint->add(std::move(internalUnique));
            break;
        } 
        else if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::POSSIBLE_VALUE_SHORT)
        {

            auto castPossibleValue = static_cast< dune::framework::data::constraints::PossibleValuesShort*>(constraint);
            auto internalUnique = std::make_unique<dune::framework::data::constraints::PossibleValuesShort>(castPossibleValue->getPossibleValues(),stringLocalized);
            newConstraint->add(std::move(internalUnique));
            break;
        } 
        else if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::POSSIBLE_VALUE_BOOL)
        {
            auto castPossibleValue = static_cast< dune::framework::data::constraints::PossibleValuesBool*>(constraint);
            auto internalUnique = std::make_unique<dune::framework::data::constraints::PossibleValuesBool>(castPossibleValue->getPossibleValues(),stringLocalized);
            newConstraint->add(std::move(internalUnique));
            break;
        } 
        else if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::POSSIBLE_VALUE_STRING)
        {
            // In this case, it's expected a unique possible encapsulation, if there is more, there is a problem from static constraints.
            auto castPossibleValue = static_cast< dune::framework::data::constraints::PossibleValuesString*>(constraint);
            auto internalUnique = std::make_unique<dune::framework::data::constraints::PossibleValuesString>(castPossibleValue->getPossibleValues(),stringLocalized);
            newConstraint->add(std::move(internalUnique));
            break;
        }
    }
}

std::string FlatBufferParserToCdmType::parseCopyIntentTableValueToString(std::shared_ptr<CopyIntentTableValueT> value, bool& localizedFromMethod, dune::localization::ILocaleProvider *localization)
{
    CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString enter");

    std::string result = "";
    // Check that type coincidence between all values in vector.
    auto unionType = value->unionValue.type;
    auto unionValue = value->unionValue;

    switch (unionType)
    {
        case CopyIntentValues::INT8:
            if(localization)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString INT8 parse");
                dune::localization::ParameterizedString parameterizedResultString(dune::localization::string_id::cStringBullet,
                                std::to_string(unionValue.AsINT8()->value));
                result = localization->deviceLocale()->format(&parameterizedResultString);
                localizedFromMethod = true;
            }
            else
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString INT8 localization not passed, couldn't be localized");
            } 
            break;
        case CopyIntentValues::INT16:
            if(localization)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString INT16 parse");
                dune::localization::ParameterizedString parameterizedResultString(dune::localization::string_id::cStringBullet,
                                std::to_string(unionValue.AsINT16()->value));
                result = localization->deviceLocale()->format(&parameterizedResultString);
                localizedFromMethod = true;
            }
            else
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString INT16 localization not passed, couldn't be localized");
            } 
            break;
        case CopyIntentValues::INT32:
            if(localization)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString INT32 parse");
                dune::localization::ParameterizedString parameterizedResultString(dune::localization::string_id::cStringBullet,
                                std::to_string(unionValue.AsINT32()->value));
                result = localization->deviceLocale()->format(&parameterizedResultString);
                localizedFromMethod = true;
            }
            else
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString INT32 localization not passed, couldn't be localized");
            } 
            break;
        case CopyIntentValues::INT64:
            if(localization)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString INT64 parse");
                dune::localization::ParameterizedString parameterizedResultString(dune::localization::string_id::cStringBullet,
                                std::to_string(unionValue.AsINT64()->value));
                result = localization->deviceLocale()->format(&parameterizedResultString);
                localizedFromMethod = true;
            }
            else
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString INT64 localization not passed, couldn't be localized");
            } 
            break;
        case CopyIntentValues::UINT8:
            if(localization)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString UINT8 parse");
                dune::localization::ParameterizedString parameterizedResultString(dune::localization::string_id::cStringBullet,
                                std::to_string(unionValue.AsUINT8()->value));
                result = localization->deviceLocale()->format(&parameterizedResultString);
                localizedFromMethod = true;
            }
            else
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString UINT8 localization not passed, couldn't be localized");
            } 
            break;
        case CopyIntentValues::UINT16:
            if(localization)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString UINT16 parse");
                dune::localization::ParameterizedString parameterizedResultString(dune::localization::string_id::cStringBullet,
                                std::to_string(unionValue.AsUINT16()->value));
                result = localization->deviceLocale()->format(&parameterizedResultString);
                localizedFromMethod = true;
            }
            else
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString UINT16 localization not passed, couldn't be localized");
            } 
            break;
        case CopyIntentValues::UINT32:
            if(localization)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString UINT32 parse");
                dune::localization::ParameterizedString parameterizedResultString(dune::localization::string_id::cStringBullet,
                                std::to_string(unionValue.AsUINT32()->value));
                result = localization->deviceLocale()->format(&parameterizedResultString);
                localizedFromMethod = true;
            }
            else
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString UINT32 localization not passed, couldn't be localized");
            } 
            break;
        case CopyIntentValues::UINT64:
            if(localization)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString UINT64 parse");
                dune::localization::ParameterizedString parameterizedResultString(dune::localization::string_id::cStringBullet,
                                std::to_string(unionValue.AsUINT64()->value));
                result = localization->deviceLocale()->format(&parameterizedResultString);
                localizedFromMethod = true;
            }
            else
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString UINT64 localization not passed, couldn't be localized");
            } 
            break;;
        case CopyIntentValues::DOUBLE:
            if(localization)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString DOUBLE parse");
                dune::localization::ParameterizedString parameterizedResultString(dune::localization::string_id::cStringBullet,
                                std::to_string(unionValue.AsDOUBLE()->value));
                result = localization->deviceLocale()->format(&parameterizedResultString);
                localizedFromMethod = true;
            }
            else
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString DOUBLE localization not passed, couldn't be localized");
            } 
            break;          
        case CopyIntentValues::BOOL:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString BOOL parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::glossary_1::FeatureEnabledEnum>(unionValue).toString();
            break;
        case CopyIntentValues::OriginalMediaType:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString OriginalMediaType parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::glossary_1::ScanMediaType>(unionValue).toString();
            break;
        case CopyIntentValues::ScanSource:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString ScanSource parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::glossary_1::ScanMediaSourceId>(unionValue).toString();            
            break;
        case CopyIntentValues::ScanCaptureModeType:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString ScanCaptureModeType parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::ScanCaptureMode>(unionValue).toString();
            break;
        case CopyIntentValues::CcdChannelEnum:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString CcdChannelEnum parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::CcdChannel>(unionValue).toString();
            break;
        case CopyIntentValues::BinaryRenderingEnum:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString BinaryRenderingEnum parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::BinaryRendering>(unionValue).toString();
            break;
        case CopyIntentValues::AutoColorDetectEnum:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString AutoColorDetectEnum parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::AutoColorDetect>(unionValue).toString();
            break;
        case CopyIntentValues::ImagePreview:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString ImagePreview parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration>(unionValue).toString();
            break;
        case CopyIntentValues::ScanScaleSelectionEnum:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString ScanScaleSelectionEnum parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::scaling::ScaleSelection>(unionValue).toString();
            break;
        case CopyIntentValues::ScanAcquisitionsSpeedEnum:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString ScanAcquisitionsSpeedEnum parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::ScanAcquisitionsSpeed>(unionValue).toString();
            break;
        case CopyIntentValues::ColorMode:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString ColorMode parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::ColorModes>(unionValue).toString();
            break;
        case CopyIntentValues::ContentOrientation:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString ContentOrientation parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::glossary_1::ContentOrientation>(unionValue).toString();
            break;
        case CopyIntentValues::OriginalContentType:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString OriginalContentType parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::ContentType>(unionValue).toString();
            break;
        case CopyIntentValues::MediaSizeId:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString MediaSizeId parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::glossary_1::MediaSize>(unionValue).toString();
            break;
        case CopyIntentValues::Plex:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString Plex parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::glossary_1::PlexMode>(unionValue).toString();
            break;
        case CopyIntentValues::PlexBinding:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString PlexBinding parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::glossary_1::DuplexBinding>(unionValue).toString();
            break;
        case CopyIntentValues::Resolution:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString Resolution parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::Resolutions>(unionValue).toString();
            break;
        case CopyIntentValues::MediaSource:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString MediaSource parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::glossary_1::MediaSourceId>(unionValue).toString();
            break;
        case CopyIntentValues::OutputCanvasAnchorType:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString OutputCanvasAnchorType parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::OutputCanvasAnchor>(unionValue).toString();
            break;
        case CopyIntentValues::MediaIdType:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString MediaIdType parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::glossary_1::MediaType>(unionValue).toString();
            break;
        case CopyIntentValues::MediaDestinationId:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString MediaDestinationId parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::glossary_1::MediaDestinationId>(unionValue).toString();
            break;
        case CopyIntentValues::PrintQuality:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString PrintQuality parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::glossary_1::PrintQuality>(unionValue).toString();
            break;
        case CopyIntentValues::PrintingOrder:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString PrintingOrder parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::PrintingOrder>(unionValue).toString();
            break;
        case CopyIntentValues::Rotate:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString Rotate parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::RotateEnum>(unionValue).toString();
            break;
        case CopyIntentValues::MediaFamily:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString MediaFamily parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::mediaProfile_1::MediaFamilyEnum>(unionValue).toString();
            break;
        case CopyIntentValues::CopyMargins:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString CopyMargins parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::PrintMargins>(unionValue).toString();
            break;
        case CopyIntentValues::CopyOutputNumberUpCount:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString CopyOutputNumberUpCount parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::PagesPerSheet>(unionValue).toString();
            break;
        case CopyIntentValues::SheetCollate:
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString sheet collate parse");
            result = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<dune::cdm::jobTicket_1::CollateModes>(unionValue).toString();
            break;
        case CopyIntentValues::MinMaxLengthUInt:
            if(localization)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString MinMaxLengthUInt");
                if(unionValue.AsMinMaxLengthUInt()->minLength == unionValue.AsMinMaxLengthUInt()->maxLength)
                {
                    dune::localization::ParameterizedString otherThanParametrized(dune::localization::string_id::cValueOtherThanDigit,unionValue.AsMinMaxLengthUInt()->minLength);
                    result = localization->deviceLocale()->format(&otherThanParametrized);
                }
                else
                {
                    dune::localization::ParameterizedString lessThanParametrized(dune::localization::string_id::cLessThanX,
                        unionValue.AsMinMaxLengthUInt()->minLength);
                    dune::localization::ParameterizedString moreThanParametrized(dune::localization::string_id::cMoreThanX,
                        unionValue.AsMinMaxLengthUInt()->maxLength);
                    dune::localization::ParameterizedString bulletLessThanParametrized(dune::localization::string_id::cStringBullet,
                        localization->deviceLocale()->format(&lessThanParametrized));   
                    dune::localization::ParameterizedString bulletMoreThanParametrized(dune::localization::string_id::cStringBullet,
                        localization->deviceLocale()->format(&moreThanParametrized));    
 

                    result = localization->deviceLocale()->format(&bulletLessThanParametrized) + "\n"+ localization->deviceLocale()->format(&bulletMoreThanParametrized); 
                }
                
                localizedFromMethod = true;
            }
            else
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString MinMaxLengthUInt localization not passed, couldn't be localized");
            }            
            break;

        case CopyIntentValues::RangeValueInt:
            if(localization)
            {
                CHECKPOINTD("Send::FlatBufferParserToCdmType::parseSendIntentTableValueToString MinMaxLengthUInt");
                if(unionValue.AsRangeValueInt()->min == unionValue.AsRangeValueInt()->max)
                {
                    dune::localization::ParameterizedString otherThanParametrized(dune::localization::string_id::cValueOtherThanDigit,unionValue.AsRangeValueInt()->min);
                    result = localization->deviceLocale()->format(&otherThanParametrized);
                }
                else
                {
                    dune::localization::ParameterizedString lessThanParametrized(dune::localization::string_id::cLessThanX,
                        unionValue.AsRangeValueInt()->min);
                    dune::localization::ParameterizedString moreThanParametrized(dune::localization::string_id::cMoreThanX,
                        unionValue.AsRangeValueInt()->max);
                    dune::localization::ParameterizedString bulletLessThanParametrized(dune::localization::string_id::cStringBullet,
                        localization->deviceLocale()->format(&lessThanParametrized));   
                    dune::localization::ParameterizedString bulletMoreThanParametrized(dune::localization::string_id::cStringBullet,
                        localization->deviceLocale()->format(&moreThanParametrized));    
 

                    result = localization->deviceLocale()->format(&bulletLessThanParametrized) + "\n"+ localization->deviceLocale()->format(&bulletMoreThanParametrized); 
                }
                
                localizedFromMethod = true;
            }
            else
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString RangeValueInt localization not passed, couldn't be localized");
            }
            break;

        case CopyIntentValues::RangeValueDouble:
            if(localization)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString RangeValueDouble");
                if(unionValue.AsRangeValueDouble()->min == unionValue.AsRangeValueDouble()->max)
                {
                    dune::localization::ParameterizedString otherThanParametrized(dune::localization::string_id::cValueOtherThanDigit,unionValue.AsRangeValueDouble()->min);
                    result = localization->deviceLocale()->format(&otherThanParametrized);
                }
                else
                {
                    dune::localization::ParameterizedString lessThanParametrized(dune::localization::string_id::cLessThanX,
                        unionValue.AsRangeValueDouble()->min);
                    dune::localization::ParameterizedString moreThanParametrized(dune::localization::string_id::cMoreThanX,
                        unionValue.AsRangeValueDouble()->max);
                    dune::localization::ParameterizedString bulletLessThanParametrized(dune::localization::string_id::cStringBullet,
                        localization->deviceLocale()->format(&lessThanParametrized));   
                    dune::localization::ParameterizedString bulletMoreThanParametrized(dune::localization::string_id::cStringBullet,
                        localization->deviceLocale()->format(&moreThanParametrized));    

                    result = localization->deviceLocale()->format(&bulletLessThanParametrized) + "\n"+ localization->deviceLocale()->format(&bulletMoreThanParametrized);             
                }
                
                localizedFromMethod = true;
            }
            else
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString RangeValueDouble localization not passed, couldn't be localized");
            }
            break;
        case CopyIntentValues::TEXT:
            if(localization)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString TEXT");
                // Not specified, setting directly not supported message
                dune::localization::ParameterizedString parameterizedResultString(dune::localization::string_id::cStringBullet,
                            dune::localization::string_id::cInputInvalidPattern);
                result = localization->deviceLocale()->format(&parameterizedResultString);
                localizedFromMethod = true;
            }
            else
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString TEXT localization not passed, couldn't be localized");
            }
            break;
        // currently unsupported
        case CopyIntentValues::AttachmentSize:
        case CopyIntentValues::ScanFeedOrientation:
        case CopyIntentValues::BlankDetectEnum:
        case CopyIntentValues::OverScanType:
        case CopyIntentValues::ScanImagingProfileType:
        case CopyIntentValues::OutputCanvas:
        case CopyIntentValues::MediaOrientation:
        case CopyIntentValues::NONE:
        default:
            break;
    }

    CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::parseCopyIntentTableValueToString exit");

    return result;
}

template <typename CdmType>
std::vector<std::shared_ptr<CopyIntentTableValueT>> FlatBufferParserToCdmType::getValuesNotAllowedForEnum(std::shared_ptr<ConstrainedValuesT> constraintValues, std::shared_ptr<dune::framework::data::constraints::Constraints> originalConstraints)
{
    CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForEnum Comparing enter");
    std::vector<std::shared_ptr<CopyIntentTableValueT>> result;

    // Get supported values
    auto tableValues = constraintValues->supportedValues;

    // Search for possible values constraint, and add when find
    std::vector<CdmType> possibleValues;

    // Avoid take values when is not original constraints
    if(originalConstraints)
    {
        for(auto constraint : originalConstraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::POSSIBLE_VALUE_ENUM)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForEnum taking possible values");
                auto castPossibleValue = static_cast< dune::framework::data::constraints::PossibleValuesEnum<CdmType>*>(constraint);
                possibleValues = castPossibleValue->getPossibleValues();
                break;
            }
        }
    }    

    // Check and compare with supported values, to add not supported values on vector, as type of 
    for(auto possibleValue : possibleValues)
    {
        CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForEnum checking possible value to add on vector");

        auto iterator = std::find_if(tableValues.begin(),tableValues.end(),
            [&](std::shared_ptr<CopyIntentTableValueT> vectorValue)
            {
                CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowed Comparing values");
                return FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<CdmType>(vectorValue->unionValue) == possibleValue;
            }
        );

        // If item is not on valid values
        if (iterator == tableValues.end())
        {
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForEnum checking to set new not allowed item on vector");
            auto valueAsUnion = FlatBufferParserToCdmType::parseCdmTypeToFlatBufferEnumTypeValue(tableValues[0]->unionValue.type, possibleValue);

            auto iteratorResult = std::find_if(result.begin(),result.end(),
                [&](std::shared_ptr<CopyIntentTableValueT> vectorValue)
                {
                    CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowed Comparing values previous insert on result");
                    return FlatBufferParserToCdmType::compareUnionValue(vectorValue->unionValue,valueAsUnion->unionValue);
                }
            );

            // It item is not on result, insert.
            if(iteratorResult == result.end())
            {
                CHECKPOINTC("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForEnum setting item on vector result");
                result.push_back(valueAsUnion);
            }
        }
        else
        {
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForEnum item is on valid values, so will not be added on vector not supporting");
        }
    }

    CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForEnum Comparing exit");

    return result;
}

template<typename FbCast>
std::vector<std::shared_ptr<CopyIntentTableValueT>> FlatBufferParserToCdmType::getValuesNotAllowedForUInt(std::shared_ptr<ConstrainedValuesT> constraintValues)
{
    CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForUInt enter");

    std::vector<std::shared_ptr<CopyIntentTableValueT>> result;
    auto internalTable = new MinMaxLengthUIntT();

    bool firstValueSet = false;
    for (auto value : constraintValues->supportedValues)
    {
        auto fbCastValue = reinterpret_cast<FbCast *>((value->unionValue.value));
        assert_msg(fbCastValue,"Casting a value not supported with the origin value");
        uint32_t castValue = static_cast<uint32_t>(fbCastValue->value);

        if(firstValueSet)
        {
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForUInt next value set %zu",castValue);

            if(castValue < internalTable->minLength)
            {
                internalTable->minLength = castValue;
            }
            if(castValue > internalTable->maxLength)
            {
                internalTable->maxLength = castValue;
            }
        }
        else
        {
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForUInt first value set %zu",castValue);

            internalTable->minLength = castValue;
            internalTable->maxLength = castValue;
            firstValueSet = true;
        }
        
    }
    result.push_back(createCopyIntentUnionValue<MinMaxLengthUIntT>(CopyIntentValues::MinMaxLengthUInt,internalTable));

    CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForUInt enter");

    return result;
}

template<typename FbCast>
std::vector<std::shared_ptr<CopyIntentTableValueT>> FlatBufferParserToCdmType::getValuesNotAllowedForInt(std::shared_ptr<ConstrainedValuesT> constraintValues)
{
    CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForInt enter");

    std::vector<std::shared_ptr<CopyIntentTableValueT>> result;
    auto internalTable = new RangeValueIntT();

    bool firstValueSet = false;
    for (auto value : constraintValues->supportedValues)
    {
        auto fbCastValue = reinterpret_cast<FbCast *>((value->unionValue.value));
        assert_msg(fbCastValue,"Casting a value not supported with the origin value");
        int32_t castValue = static_cast<int32_t>(fbCastValue->value);
        if(firstValueSet)
        {
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForInt next value set %" PRId32,castValue);

            if(castValue < internalTable->min)
            {
                internalTable->min = castValue;
            }
            if(castValue > internalTable->max)
            {
                internalTable->max = castValue;
            }
        }
        else
        {
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForInt first value set %" PRId32,castValue);

            internalTable->min = castValue;
            internalTable->max = castValue;
            firstValueSet = true;
        }
    }
    result.push_back(createCopyIntentUnionValue<RangeValueIntT>(CopyIntentValues::RangeValueInt,internalTable));

    CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForInt exit");

    return result;
}

std::vector<std::shared_ptr<CopyIntentTableValueT>> FlatBufferParserToCdmType::getValuesNotAllowedForDouble(std::shared_ptr<ConstrainedValuesT> constraintValues)
{
    CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForDouble enter");

    std::vector<std::shared_ptr<CopyIntentTableValueT>> result;
    auto internalTable = new RangeValueDoubleT();

    bool firstValueSet = false;
    for (auto value : constraintValues->supportedValues)
    {
        auto castValue = static_cast<double>((value->unionValue.AsDOUBLE())->value);
        if(firstValueSet)
        {
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForDouble next value set %f",castValue);

            if(castValue < internalTable->min)
            {
                internalTable->min = castValue;
            }
            if(castValue > internalTable->max)
            {
                internalTable->max = castValue;
            }
        }
        else
        {
            CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForDouble first value set %f",castValue);

            internalTable->min = castValue;
            internalTable->max = castValue;
            firstValueSet = true;
        }
    }
    result.push_back(createCopyIntentUnionValue<RangeValueDoubleT>(CopyIntentValues::RangeValueDouble,internalTable));

    CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowedForDouble exit");

    return result;
}

std::vector<std::shared_ptr<CopyIntentTableValueT>> FlatBufferParserToCdmType::getValuesNotAllowed(std::shared_ptr<ConstrainedValuesT> constraintValues, 
    std::shared_ptr<dune::framework::data::constraints::Constraints> originalConstraints)
{
    CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowed enter");
    std::vector<std::shared_ptr<CopyIntentTableValueT>> result;

    // Get supported values
    auto tableValues = constraintValues->supportedValues;
    assert_msg(!tableValues.empty(),"Never enter here without items. must to be previously controlled");
    
    // Check that type coincidence between all values in vector.
    auto unionType = tableValues[0]->unionValue.type;
    for(auto unionValueTable : tableValues)
    {
        assert_msg(unionType == unionValueTable->unionValue.type,"Type between union not coincidence, report as an error");
    }
    
    switch (unionType)
    {
        case CopyIntentValues::BOOL:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::glossary_1::FeatureEnabledEnum>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::OriginalMediaType:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::glossary_1::ScanMediaType>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::ScanSource:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::glossary_1::ScanMediaSourceId>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::ScanCaptureModeType:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::ScanCaptureMode>(constraintValues,originalConstraints);
            break;        
        case CopyIntentValues::CcdChannelEnum:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::CcdChannel>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::BinaryRenderingEnum:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::BinaryRendering>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::AutoColorDetectEnum:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::AutoColorDetect>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::ImagePreview:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::ScanScaleSelectionEnum:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::ScanAcquisitionsSpeedEnum:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::ScanAcquisitionsSpeed>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::ColorMode:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::ColorModes>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::ContentOrientation:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::glossary_1::ContentOrientation>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::OriginalContentType:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::ContentType>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::MediaSizeId:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::glossary_1::MediaSize>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::Plex:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::glossary_1::PlexMode>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::PlexBinding:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::glossary_1::DuplexBinding>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::Resolution:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::Resolutions>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::MediaSource:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::glossary_1::MediaSourceId>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::OutputCanvasAnchorType:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::OutputCanvasAnchor>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::MediaIdType:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::glossary_1::MediaType>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::MediaDestinationId:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::glossary_1::MediaDestinationId>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::PrintQuality:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::glossary_1::PrintQuality>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::PrintingOrder:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::PrintingOrder>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::Rotate:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::RotateEnum>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::MediaFamily:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::mediaProfile_1::MediaFamilyEnum>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::CopyMargins:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::PrintMargins>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::CopyOutputNumberUpCount:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::PagesPerSheet>(constraintValues,originalConstraints);
            break;
        case CopyIntentValues::SheetCollate:
            result = FlatBufferParserToCdmType::getValuesNotAllowedForEnum<dune::cdm::jobTicket_1::CollateModes>(constraintValues,originalConstraints);            
            break;
        // With next enums, set directly supported values, message will be generated directly with this
        case CopyIntentValues::MinMaxLengthUInt:
        case CopyIntentValues::RangeValueInt:
        case CopyIntentValues::RangeValueDouble:
        case CopyIntentValues::TEXT:
            result = constraintValues->supportedValues;
            break;
        case CopyIntentValues::INT8:
            result = getValuesNotAllowedForInt<dune::copy::Jobs::Copy::INT8T>(constraintValues);
            break;
        case CopyIntentValues::INT16:
            result = getValuesNotAllowedForInt<dune::copy::Jobs::Copy::INT16T>(constraintValues);
            break;
        case CopyIntentValues::INT32:
            result = getValuesNotAllowedForInt<dune::copy::Jobs::Copy::INT32T>(constraintValues);
            break;
        case CopyIntentValues::INT64:
            result = getValuesNotAllowedForInt<dune::copy::Jobs::Copy::INT64T>(constraintValues);
            break;
        case CopyIntentValues::UINT8:
            result = getValuesNotAllowedForUInt<dune::copy::Jobs::Copy::UINT8T>(constraintValues);
            break;
        case CopyIntentValues::UINT16:
            result = getValuesNotAllowedForUInt<dune::copy::Jobs::Copy::UINT16T>(constraintValues);
            break;
        case CopyIntentValues::UINT32:
            result = getValuesNotAllowedForUInt<dune::copy::Jobs::Copy::UINT32T>(constraintValues);
            break;
        case CopyIntentValues::UINT64:
            result = getValuesNotAllowedForUInt<dune::copy::Jobs::Copy::UINT64T>(constraintValues);
            break;
        case CopyIntentValues::DOUBLE:            
            result = getValuesNotAllowedForDouble(constraintValues);
            break;   
        // Next values currently are not supported on checks (Not exist on constraints)
        case CopyIntentValues::OutputCanvas:
        case CopyIntentValues::MediaOrientation:
        case CopyIntentValues::ScanImagingProfileType:
        case CopyIntentValues::ScanFeedOrientation:
        case CopyIntentValues::BlankDetectEnum:
        case CopyIntentValues::OverScanType:
        case CopyIntentValues::AttachmentSize:
        case CopyIntentValues::NONE:
        default:
            break;
    }

    CHECKPOINTD("dune::copy::Jobs::Copy::FlatBufferParserToCdmType::getValuesNotAllowed exit");

    return result;
}

bool CopyTicketCheckerFromFlatBufferEnum::compareValueOnTicket(const std::string &ticketSetting, CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket)
{
    // Find method to compare on ticket the Value from FBS
    auto pair = Map2CheckerTicketMethod::MAP.find(ticketSetting);
    assert_msg(pair != Map2CheckerTicketMethod::MAP.end(),"string ticket setting that you are trying to use is not supported and added on map."
        " Insert on CopyTicketCheckerFromFlatBufferEnum::Map2CheckerTicketMethod::MAP map to support it %s",ticketSetting.c_str());
    
    // Execute method contained on second part
    return pair->second(value, ticket);
}

bool CopyTicketCheckerFromFlatBufferEnum::compareValueOnTicketTable(const std::string &ticketSetting, CopyIntentValuesUnion value, 
    std::shared_ptr<JobTicketTable> ticketTable, bool& settingIsSetOnCdm)
{
    bool result = false;
    Map2CheckerCdmTableProperty::executeMapFunction(ticketSetting, ticketTable, settingIsSetOnCdm);
    if(settingIsSetOnCdm)
    {
        // Find method to compare on ticket the Value from FBS
        auto pair = Map2CheckerTicketTableMethod::MAP.find(ticketSetting);
        assert_msg(pair != Map2CheckerTicketTableMethod::MAP.end(),"string ticket setting that you are trying to use is not supported and added on map."
            " Insert on CopyTicketCheckerFromFlatBufferEnum::Map2CheckerTicketTableMethod::MAP map to support it %s",ticketSetting.c_str());
        
        // Execute method contained on second part
        result = pair->second(value, ticketTable);
    }
    return result;
}

bool CopyTicketCdmHelper::checkIfValueNeedToBeUpdatedOnJobTicketTable(const std::string &cdmSettingPath, 
    const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, 
    std::shared_ptr<ICopyJobTicket> ticket, 
    std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints,
    bool checkCurrentIntent)
{
    CHECKPOINTD("CopyTicketCdmHelper::checkIfValueNeedToBeUpdatedOnJobTicketTable - Enter for setting %s",cdmSettingPath.c_str());

    bool settingIsSetOnCdm = false;

    // Check setting on JobTicketTable
    CHECKPOINTD("CopyTicketCdmHelper::checkIfValueNeedToBeUpdatedOnJobTicketTable - Enter - going to check on job ticket table easybuffer");
    bool result = Map2CheckerCdmTableProperty::executeMapFunction(cdmSettingPath, updatedJobTicketTable, settingIsSetOnCdm, currentConstraints);

    // If setting wasn't set on cdm, take from ticket
    if(!settingIsSetOnCdm)
    {
        if (checkCurrentIntent)
        {
            CHECKPOINTD("CopyTicketCdmHelper::checkIfValueNeedToBeUpdatedOnJobTicketTable - going to check on copy job ticket");
            // Check setting on current ICopyJobTicket
            result = Map2CheckerCopyJobTicketProperty::executeMapFunction(cdmSettingPath, ticket, currentConstraints);
        }
        else
        {
            CHECKPOINTD("CopyTicketCdmHelper::checkIfValueNeedToBeUpdatedOnJobTicketTable - skip ticket check");
        }
    }
    else
    {
        CHECKPOINTD("CopyTicketCdmHelper::checkIfValueNeedToBeUpdatedOnJobTicketTable - setting was founded on job ticket table easybuffer");
    }

    CHECKPOINTD("CopyTicketCdmHelper::checkIfValueNeedToBeUpdatedOnJobTicketTable - exit -> setting %s was %s",cdmSettingPath.c_str(),(result)?"founded and need updated":"not founded or not need an updated");
    return result;        
}

bool CopyTicketCdmHelper::updateValue(const std::string &cdmSettingPath, 
    const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, 
    std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints)
{
    CHECKPOINTD("CopyTicketCdmHelper::updateValue - enter to update setting %s",cdmSettingPath.c_str());

    // Check setting on JobTicketTable
    bool result = Map2UpdateTableProperty::executeMapFunction(cdmSettingPath, updatedJobTicketTable, currentConstraints);

    CHECKPOINTD("CopyTicketCdmHelper::updateValue - exit setting %s was %s updated",cdmSettingPath.c_str(),(result)?"":"not");

    return result;
}

}}}}
