///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesLargeFormatParserHelperGTest.cpp
 * @date   Wed 15 Mar 2023 12:17:07 PM UTC
 * @brief  Unit testing of Helper
 * @author yago.cordero.carrera@hp.com (Cordero Carrera, Yago)
 *
 * (C) Copyright 2023 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include "GTestConfigHelper.h"
#include "CopyJobDynamicConstraintRulesLargeFormatParserHelper.h"
#include "PossibleValues.h"

#include "CopyJobDynamicConstraintRulesLargeFormatParserHelperGTest_TraceAutogen.h"

using namespace dune::copy::Jobs::Copy;

namespace DynamicRulesLargeFormatHelper
{
    template<typename FbTable>
    inline CopyIntentValuesUnion createIntentValuesUnion(CopyIntentValues enumType, FbTable* fbTable)
    {
        CopyIntentValuesUnion unionValue = CopyIntentValuesUnion();
        unionValue.type = enumType;
        unionValue.value = fbTable;
        return unionValue;
    }

    template<typename FbTable,typename InjectValue>
    inline CopyIntentValuesUnion createIntentValuesUnion(CopyIntentValues enumType, FbTable* fbTable, InjectValue value)
    {
        CopyIntentValuesUnion unionValue = CopyIntentValuesUnion();
        unionValue.type = enumType;
        fbTable->value = value;
        unionValue.value = fbTable;
        return unionValue;
    }

    template<typename FbTable,typename InjectValue>
    inline CopyIntentValuesUnion createIntentValuesUnionMinMax(CopyIntentValues enumType, FbTable* fbTable, InjectValue value)
    {
        CopyIntentValuesUnion unionValue = CopyIntentValuesUnion();
        unionValue.type = enumType;
        fbTable->minLength = value;
        fbTable->maxLength = value;
        unionValue.value = fbTable;
        return unionValue;
    }

    template<typename FbTable,typename InjectValue>
    inline CopyIntentValuesUnion createIntentValuesUnionRange(CopyIntentValues enumType, FbTable* fbTable, InjectValue value)
    {
        CopyIntentValuesUnion unionValue = CopyIntentValuesUnion();
        unionValue.type = enumType;
        fbTable->min = value;
        fbTable->max = value;
        fbTable->step = value;
        unionValue.value = fbTable;
        return unionValue;
    }

    std::vector<std::shared_ptr<CopyIntentTableValueT>> generateCopyIntentTableValues(CopyIntentValuesUnion unionTable)
    {
        std::shared_ptr<CopyIntentTableValueT> copyIntentTableValue = std::make_shared<CopyIntentTableValueT>();
        copyIntentTableValue->unionValue = unionTable;
        return std::vector<std::shared_ptr<CopyIntentTableValueT>>({copyIntentTableValue});
    }

    std::vector<std::shared_ptr<CopyIntentTableValueT>> generateCopyIntentTableValues(std::vector<CopyIntentValuesUnion> unionTableList)
    {
        std::vector<std::shared_ptr<CopyIntentTableValueT>> result = std::vector<std::shared_ptr<CopyIntentTableValueT>>();
        for (auto unionTable : unionTableList)
        {
            std::shared_ptr<CopyIntentTableValueT> copyIntentTableValue = std::make_shared<CopyIntentTableValueT>();
            copyIntentTableValue->unionValue = unionTable;
            result.push_back(copyIntentTableValue);
        }
        return result;
    }

    template<typename CdmType>
    std::shared_ptr<dune::framework::data::constraints::Constraints> generatePossibleValuesConstraint(CdmType possibleValues)
    {
        std::vector<CdmType> possibleValuesList = std::vector<CdmType>();
        possibleValuesList.push_back(possibleValues);
        return generatePossibleValuesConstraint(possibleValuesList);
    }

    template<typename CdmType>
    std::shared_ptr<dune::framework::data::constraints::Constraints> generatePossibleValuesConstraint(std::vector<CdmType> possibleValues)
    {
        std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints = std::make_shared<dune::framework::data::constraints::Constraints>();

        auto enumPossibleValuesConstraint = std::make_unique<dune::framework::data::constraints::PossibleValuesEnum<CdmType>>(possibleValues, &CdmType::valueToString, "");
        staticConstraints->add(std::move(enumPossibleValuesConstraint));
        return staticConstraints;
    }

    template<typename ConstraintType>
    std::shared_ptr<dune::framework::data::constraints::Constraints> generateStaticConstraint(ConstraintType constraint)
    {
        std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints = std::make_shared<dune::framework::data::constraints::Constraints>();
        staticConstraints->add(std::move(constraint));
        return staticConstraints;
    }
}



class GivenParserHelper : public ::testing::Test
{
public:
    GivenParserHelper(){}

    void checkConstraintRangeInt(std::shared_ptr<CopyIntentTableValueT> unionTable);
    void checkConstraintRangeDouble(std::shared_ptr<CopyIntentTableValueT> unionTable);
    void checkConstraintMinMaxLength(std::shared_ptr<CopyIntentTableValueT> unionTable);

    template<typename CdmType>
    void checkConstraintValidResult(std::shared_ptr<CopyIntentTableValueT> unionTable, std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints = std::make_shared<dune::framework::data::constraints::Constraints>());

    void checkConstraintValidResult(std::shared_ptr<CopyIntentTableValueT> unionTable, std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints = std::make_shared<dune::framework::data::constraints::Constraints>());

    template<typename NumberType>
    void checkConstraintLimitResult(std::shared_ptr<CopyIntentTableValueT> unionTable, std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints = std::make_shared<dune::framework::data::constraints::Constraints>());

    void checkConstraintLimitResult(std::shared_ptr<CopyIntentTableValueT> unionTable, std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints = std::make_shared<dune::framework::data::constraints::Constraints>());

protected:
    virtual void SetUp() override;
    virtual void TearDown() override;
};

void GivenParserHelper::SetUp()
{
}

void GivenParserHelper::TearDown()
{
}

void GivenParserHelper::checkConstraintRangeInt(std::shared_ptr<CopyIntentTableValueT> unionTable)
{
    std::shared_ptr<dune::framework::data::constraints::Constraints> constraints = std::make_shared<dune::framework::data::constraints::Constraints>();

    // Execute Test Method
    FlatBufferParserToCdmType::setValuesOnConstraint({unionTable}, constraints, nullptr,"");
    RangeValueIntT* fbTable = (RangeValueIntT*)unionTable->unionValue.value;

    int min = 0;
    int max = 0;
    int step = 0;
    bool constraintsFounded = false;
    for(auto constraint : constraints->getConstraints())
    {
        if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::RANGE_INT)
        {
            min = (static_cast< dune::framework::data::constraints::RangeInt*>(constraint))->getMin();
            max = (static_cast< dune::framework::data::constraints::RangeInt*>(constraint))->getMax();
            step = (static_cast< dune::framework::data::constraints::RangeInt*>(constraint))->getStep();
            constraintsFounded = true;
            break;
        }
    }

    ASSERT_TRUE(constraintsFounded);
    EXPECT_EQ(min,fbTable->min);
    EXPECT_EQ(max,fbTable->max);
    EXPECT_EQ(step,fbTable->step);
}

void GivenParserHelper::checkConstraintRangeDouble(std::shared_ptr<CopyIntentTableValueT> unionTable)
{
    std::shared_ptr<dune::framework::data::constraints::Constraints> constraints = std::make_shared<dune::framework::data::constraints::Constraints>();

    // Execute Test Method
    FlatBufferParserToCdmType::setValuesOnConstraint({unionTable}, constraints, nullptr,"");
    RangeValueDoubleT* fbTable = (RangeValueDoubleT*)unionTable->unionValue.value;

    double min = 0;
    double max = 0;
    double step = 0;
    bool constraintsFounded = false;
    for(auto constraint : constraints->getConstraints())
    {
        if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::RANGE_DOUBLE)
        {
            min = (static_cast< dune::framework::data::constraints::RangeDouble*>(constraint))->getMin();
            max = (static_cast< dune::framework::data::constraints::RangeDouble*>(constraint))->getMax();
            step = (static_cast< dune::framework::data::constraints::RangeDouble*>(constraint))->getStep();
            constraintsFounded = true;
            break;
        }
    }

    ASSERT_TRUE(constraintsFounded);
    EXPECT_EQ(min,fbTable->min);
    EXPECT_EQ(max,fbTable->max);
    EXPECT_EQ(step,fbTable->step);
}

void GivenParserHelper::checkConstraintMinMaxLength(std::shared_ptr<CopyIntentTableValueT> unionTable)
{
    std::shared_ptr<dune::framework::data::constraints::Constraints> constraints = std::make_shared<dune::framework::data::constraints::Constraints>();

    // Execute Test Method
    FlatBufferParserToCdmType::setValuesOnConstraint({unionTable},constraints,nullptr,"");
    MinMaxLengthUIntT* fbTable = (MinMaxLengthUIntT*)unionTable->unionValue.value;

    size_t minLength = 0;
    size_t maxLength = 0;

    bool constraintsMinFounded = false;
    bool constraintsMaxFounded = false;
    for(auto constraint : constraints->getConstraints())
    {
        if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::MIN_LENGTH)
        {
            minLength = (static_cast< dune::framework::data::constraints::MinLength*>(constraint))->getMinLength();
            constraintsMinFounded = true;
        }
        if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::MAX_LENGTH)
        {
            maxLength = (static_cast< dune::framework::data::constraints::MaxLength*>(constraint))->getMaxLength();
            constraintsMaxFounded = true;
        }
    }

    ASSERT_TRUE(constraintsMinFounded);
    ASSERT_TRUE(constraintsMaxFounded);
    EXPECT_EQ(minLength,size_t{fbTable->minLength});
    EXPECT_EQ(maxLength,size_t{fbTable->maxLength});
}

template<typename CdmType>
void GivenParserHelper::checkConstraintValidResult(std::shared_ptr<CopyIntentTableValueT> unionTable, std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints)
{
    std::shared_ptr<dune::framework::data::constraints::Constraints> constraints = std::make_shared<dune::framework::data::constraints::Constraints>();
    CdmType fbTableValue = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<CdmType>(unionTable->unionValue);
    std::vector<CdmType> vectorValue{fbTableValue};

    auto enumPossibleValuesConstraint = std::make_unique<dune::framework::data::constraints::PossibleValuesEnum<CdmType>>(vectorValue, &CdmType::valueToString, "");
    staticConstraints->add(std::move(enumPossibleValuesConstraint));

    auto enumValidValuesConstraint = std::make_unique<dune::framework::data::constraints::ValidValuesEnum<CdmType>>(vectorValue, "");
    staticConstraints->add(std::move(enumValidValuesConstraint));

    // Execute Test Method
    FlatBufferParserToCdmType::setValuesOnConstraint({unionTable},constraints,staticConstraints,"");

    std::vector<CdmType> dynamicValidValues;
    for(auto constraint : constraints->getConstraints())
    {
        if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM)
        {
            dynamicValidValues = (static_cast< dune::framework::data::constraints::ValidValuesEnum<CdmType>*>(constraint))->getValidValues();
            break;
        }
    }

    // expected only one value
    EXPECT_EQ(1, dynamicValidValues.size());
    EXPECT_EQ(fbTableValue,dynamicValidValues[0]);
}

void GivenParserHelper::checkConstraintValidResult(std::shared_ptr<CopyIntentTableValueT> unionTable, std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints)
{
    switch(unionTable->unionValue.type)
    {
        case CopyIntentValues::BOOL:
            checkConstraintValidResult<dune::cdm::glossary_1::FeatureEnabledEnum>(unionTable);
            break;
        case CopyIntentValues::OriginalMediaType:
            checkConstraintValidResult<dune::cdm::glossary_1::ScanMediaType>(unionTable);
            break;
        case CopyIntentValues::ScanSource:
            checkConstraintValidResult<dune::cdm::glossary_1::ScanMediaSourceId>(unionTable);
            break;
        case CopyIntentValues::ScanCaptureModeType:
            checkConstraintValidResult<dune::cdm::jobTicket_1::ScanCaptureMode>(unionTable);
            break;
        case CopyIntentValues::CcdChannelEnum:
            checkConstraintValidResult<dune::cdm::jobTicket_1::CcdChannel>(unionTable);
            break;
        case CopyIntentValues::BinaryRenderingEnum:
            checkConstraintValidResult<dune::cdm::jobTicket_1::BinaryRendering>(unionTable);
            break;
        case CopyIntentValues::AutoColorDetectEnum:
            checkConstraintValidResult<dune::cdm::jobTicket_1::AutoColorDetect>(unionTable);
            break;
        case CopyIntentValues::ImagePreview:
            checkConstraintValidResult<dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration>(unionTable);
            break;
        case CopyIntentValues::ScanScaleSelectionEnum:
            checkConstraintValidResult<dune::cdm::jobTicket_1::scaling::ScaleSelection>(unionTable);
            break;
        case CopyIntentValues::ScanAcquisitionsSpeedEnum:
            checkConstraintValidResult<dune::cdm::jobTicket_1::ScanAcquisitionsSpeed>(unionTable);
            break;
        case CopyIntentValues::ColorMode:
            checkConstraintValidResult<dune::cdm::jobTicket_1::ColorModes>(unionTable);
            break;
        case CopyIntentValues::ContentOrientation:
            checkConstraintValidResult<dune::cdm::glossary_1::ContentOrientation>(unionTable);
            break;
        case CopyIntentValues::OriginalContentType:
            checkConstraintValidResult<dune::cdm::jobTicket_1::ContentType>(unionTable);
            break;
        case CopyIntentValues::MediaSizeId:
            checkConstraintValidResult<dune::cdm::glossary_1::MediaSize>(unionTable);
            break;
        case CopyIntentValues::Plex:
            checkConstraintValidResult<dune::cdm::glossary_1::PlexMode>(unionTable);
            break;
        case CopyIntentValues::PlexBinding:
            checkConstraintValidResult<dune::cdm::glossary_1::DuplexBinding>(unionTable);
            break;
        case CopyIntentValues::Resolution:
            checkConstraintValidResult<dune::cdm::jobTicket_1::Resolutions>(unionTable);
            break;
        case CopyIntentValues::MediaSource:
            checkConstraintValidResult<dune::cdm::glossary_1::MediaSourceId>(unionTable);
            break;
        case CopyIntentValues::OutputCanvasAnchorType:
            checkConstraintValidResult<dune::cdm::jobTicket_1::OutputCanvasAnchor>(unionTable);
            break;
        case CopyIntentValues::MediaIdType:
            checkConstraintValidResult<dune::cdm::glossary_1::MediaType>(unionTable);
            break;
        case CopyIntentValues::MediaDestinationId:
            checkConstraintValidResult<dune::cdm::glossary_1::MediaDestinationId>(unionTable);
            break;
        case CopyIntentValues::PrintQuality:
            checkConstraintValidResult<dune::cdm::glossary_1::PrintQuality>(unionTable);
            break;
        case CopyIntentValues::CopyMargins:
            checkConstraintValidResult<dune::cdm::jobTicket_1::PrintMargins>(unionTable);
            break;
        case CopyIntentValues::PrintingOrder:
            checkConstraintValidResult<dune::cdm::jobTicket_1::PrintingOrder>(unionTable);
            break;
        case CopyIntentValues::CopyOutputNumberUpCount:
            checkConstraintValidResult<dune::cdm::jobTicket_1::PagesPerSheet>(unionTable);
            break;
        case CopyIntentValues::SheetCollate:
            checkConstraintValidResult<dune::cdm::jobTicket_1::CollateModes>(unionTable);
            break;
        default:
            FAIL();
            break;
    }
}

template<typename NumberType>
void GivenParserHelper::checkConstraintLimitResult(std::shared_ptr<CopyIntentTableValueT> unionTable, std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints)
{
    std::shared_ptr<dune::framework::data::constraints::Constraints> constraints = std::make_shared<dune::framework::data::constraints::Constraints>();
    NumberType fbTableValue = FlatBufferParserToCdmType::parseFlatBufferEnumTypeValueToCdmType<NumberType>(unionTable->unionValue);

    // Execute Test Method
    FlatBufferParserToCdmType::setValuesOnConstraint({unionTable},constraints,staticConstraints,"");

    std::vector<NumberType> dynamicValidValues;
    std::vector<NumberType> dynamicPossibleValues;
    NumberType min = 0;
    NumberType max = 0;
    NumberType step = 0;
    bool constraintsFounded = false;

    ASSERT_FALSE(constraints->getConstraints().empty());
    GTEST_CHECKPOINTA("checkConstraintLimitResult -- Number of constraints created: %d\n", (int) (constraints->getConstraints().size()));

    for(auto constraint : constraints->getConstraints())
    {
        if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM)
        {
            GTEST_CHECKPOINTA("checkConstraintLimitResult -- Valid constraint founded\n");

            dynamicValidValues = (static_cast< dune::framework::data::constraints::ValidValuesEnum<NumberType>*>(constraint))->getValidValues();
        }
        if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::POSSIBLE_VALUE_ENUM)
        {
            GTEST_CHECKPOINTA("checkConstraintLimitResult -- Possible constraint founded\n");
            dynamicPossibleValues = (static_cast< dune::framework::data::constraints::PossibleValuesEnum<NumberType>*>(constraint))->getPossibleValues();
        }
        else if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::RANGE_DOUBLE)
        {
            min = (NumberType) (static_cast< dune::framework::data::constraints::RangeDouble*>(constraint))->getMin();
            max = (NumberType) (static_cast< dune::framework::data::constraints::RangeDouble*>(constraint))->getMax();
            step = (NumberType) (static_cast< dune::framework::data::constraints::RangeDouble*>(constraint))->getStep();
            constraintsFounded = !constraintsFounded;
        }
        else if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::RANGE_INT)
        {
            min = (NumberType) (static_cast< dune::framework::data::constraints::RangeInt*>(constraint))->getMin();
            max = (NumberType) (static_cast< dune::framework::data::constraints::RangeInt*>(constraint))->getMax();
            step = (NumberType) (static_cast< dune::framework::data::constraints::RangeInt*>(constraint))->getStep();
            constraintsFounded = !constraintsFounded; // Constraint founded is invert the original result, to show as error if we have RANGE_INT and RANGE_DOUBLE on same execution result
        }
    }

    // expected only one value for valid, expected same value for range values
    ASSERT_TRUE(constraintsFounded);
    EXPECT_EQ(min,fbTableValue);
    EXPECT_EQ(max,fbTableValue);
    EXPECT_EQ(step,fbTableValue);

    ASSERT_FALSE(dynamicPossibleValues.empty());
    EXPECT_EQ(fbTableValue,dynamicPossibleValues[0]);

    ASSERT_FALSE(dynamicValidValues.empty());
    EXPECT_EQ(fbTableValue,dynamicValidValues[0]);
}

void GivenParserHelper::checkConstraintLimitResult(std::shared_ptr<CopyIntentTableValueT> unionTable, std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints)
{
    switch(unionTable->unionValue.type)
    {
        case CopyIntentValues::INT8:
            checkConstraintLimitResult<int8_t>(unionTable,staticConstraints);
            break;
        case CopyIntentValues::INT16:
            checkConstraintLimitResult<int16_t>(unionTable,staticConstraints);
            break;
        case CopyIntentValues::INT32:
            checkConstraintLimitResult<int32_t>(unionTable,staticConstraints);
            break;
        case CopyIntentValues::INT64:
            checkConstraintLimitResult<int64_t>(unionTable,staticConstraints);
            break;
        case CopyIntentValues::UINT8:
            checkConstraintLimitResult<uint8_t>(unionTable,staticConstraints);
            break;
        case CopyIntentValues::UINT16:
            checkConstraintLimitResult<uint16_t>(unionTable,staticConstraints);
            break;
        case CopyIntentValues::UINT32:
            checkConstraintLimitResult<uint32_t>(unionTable,staticConstraints);
            break;
        case CopyIntentValues::UINT64:
            checkConstraintLimitResult<uint64_t>(unionTable,staticConstraints);
            break;
        case CopyIntentValues::DOUBLE:
            checkConstraintLimitResult<double>(unionTable,staticConstraints);
            break;
        default:
            FAIL();
            break;
    }
}

TEST_F(GivenParserHelper,WhenCompareUnionNONE_ThenResultAsFalse)
{
    auto unionNONE = CopyIntentValuesUnion();
    EXPECT_FALSE(FlatBufferParserToCdmType::compareUnionValue(unionNONE,unionNONE));
}



class GivenParserHelperParametrizedIntentValuesUnion : public GivenParserHelper,
    public ::testing::WithParamInterface< CopyIntentValuesUnion >
{
public:
    GivenParserHelperParametrizedIntentValuesUnion()
    {
        unionTable = GetParam();
        otherUnionTable = GetParam();
    }

    CopyIntentValuesUnion unionTable, otherUnionTable;
};

TEST_P(GivenParserHelperParametrizedIntentValuesUnion,WhenCompareUnionValueIsCalledWithSameTypeUnion_ThenResultAsTrue)
{
    EXPECT_TRUE(FlatBufferParserToCdmType::compareUnionValue(unionTable,otherUnionTable));
}

TEST_P(GivenParserHelperParametrizedIntentValuesUnion,WhenCompareUnionWithNone_ThenResultIsError)
{
    auto unionNONE = CopyIntentValuesUnion();

# ifndef NDEBUG
    ASSERT_DEATH(FlatBufferParserToCdmType::compareUnionValue(unionTable,unionNONE),"");
# else
    EXPECT_FALSE(FlatBufferParserToCdmType::compareUnionValue(unionTable,unionNONE));
# endif
}

INSTANTIATE_TEST_CASE_P(, GivenParserHelperParametrizedIntentValuesUnion, ::testing::Values(
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT8,                    new INT8T()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT16,                   new INT16T()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT32,                   new INT32T()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT64,                   new INT64T()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT8,                   new UINT8T()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT16,                  new UINT16T()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT32,                  new UINT32T()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT64,                  new UINT64T()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::DOUBLE,                  new DOUBLET()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MinMaxLengthUInt,        new MinMaxLengthUIntT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::RangeValueInt,           new RangeValueIntT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::RangeValueDouble,        new RangeValueDoubleT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BOOL,                    new BOOLT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::AttachmentSize,          new AttachmentSizeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OriginalMediaType,       new OriginalMediaTypeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanSource,              new ScanSourceT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanFeedOrientation,     new ScanFeedOrientationT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BlankDetectEnum,         new BlankDetectEnumT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OverScanType,            new OverScanTypeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanCaptureModeType,     new ScanCaptureModeTypeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanImagingProfileType,  new ScanImagingProfileTypeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CcdChannelEnum,          new CcdChannelEnumT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BinaryRenderingEnum,     new BinaryRenderingEnumT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::AutoColorDetectEnum,     new AutoColorDetectEnumT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ImagePreview,            new ImagePreviewT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanScaleSelectionEnum,  new ScanScaleSelectionEnumT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanAcquisitionsSpeedEnum, new ScanAcquisitionsSpeedEnumT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ColorMode,               new ColorModeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ContentOrientation,      new ContentOrientationT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OriginalContentType,     new OriginalContentTypeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaSizeId,             new MediaSizeIdT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::Plex,                    new PlexT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PlexBinding,             new PlexBindingT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::Resolution,              new ResolutionT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaSource,             new MediaSourceT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OutputCanvasAnchorType,  new OutputCanvasAnchorTypeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaOrientation,        new MediaOrientationT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaIdType,             new MediaIdTypeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaDestinationId,      new MediaDestinationIdT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PrintQuality,            new PrintQualityT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CopyMargins,             new CopyMarginsT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PrintingOrder,           new PrintingOrderT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CopyOutputNumberUpCount, new CopyOutputNumberUpCountT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::SheetCollate,            new SheetCollateT())
));



class GivenParserHelperParametrizedTwoItemsIntentValuesUnion : public GivenParserHelper,
    public ::testing::WithParamInterface< std::tuple<CopyIntentValuesUnion, CopyIntentValuesUnion>>
{
public:
    GivenParserHelperParametrizedTwoItemsIntentValuesUnion()
    {
        unionTable = std::get<0>(GetParam());
        otherUnionTable = std::get<1>(GetParam());
    }

    CopyIntentValuesUnion unionTable, otherUnionTable;
};

TEST_P(GivenParserHelperParametrizedTwoItemsIntentValuesUnion, WhenCompareUnionValueIsCalledWithDifferentTypeUnion_ThenResultAsFalse)
{
    EXPECT_FALSE(FlatBufferParserToCdmType::compareUnionValue(unionTable,otherUnionTable));
}

INSTANTIATE_TEST_CASE_P(, GivenParserHelperParametrizedTwoItemsIntentValuesUnion, ::testing::Values(
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT8,                      new INT8T()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT8,                      new INT8T(), 2)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT16,                     new INT16T()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT16,                     new INT16T(), 2)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT32,                     new INT32T()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT32,                     new INT32T(), 2)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT64,                     new INT64T()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT64,                     new INT64T(), 2)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT8,                     new UINT8T()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT8,                     new UINT8T(), 2)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT16,                    new UINT16T()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT16,                    new UINT16T(), 2)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT32,                    new UINT32T()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT32,                    new UINT32T(), 2)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT64,                    new UINT64T()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT64,                    new UINT64T(), 2)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::DOUBLE,                    new DOUBLET()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::DOUBLE,                    new DOUBLET(), 2)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BOOL,                      new BOOLT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BOOL,                      new BOOLT(), true)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::AttachmentSize,            new AttachmentSizeT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::AttachmentSize,            new AttachmentSizeT(), dune::scan::types::AttachmentSize::LARGE)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OriginalMediaType,         new OriginalMediaTypeT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OriginalMediaType,         new OriginalMediaTypeT(), dune::scan::types::OriginalMediaType::BLUEPRINTS)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanSource,                new ScanSourceT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanSource,                new ScanSourceT(), dune::scan::types::ScanSource::ADF_DUPLEX)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanFeedOrientation,       new ScanFeedOrientationT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanFeedOrientation,       new ScanFeedOrientationT(), dune::scan::types::ScanFeedOrientation::LONGEDGE)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BlankDetectEnum,           new BlankDetectEnumT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BlankDetectEnum,           new BlankDetectEnumT(), dune::scan::types::BlankDetectEnum::DetectAndSupress)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanCaptureModeType,       new ScanCaptureModeTypeT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanCaptureModeType,       new ScanCaptureModeTypeT(), dune::scan::types::ScanCaptureModeType::BOOKMODE)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanImagingProfileType,    new ScanImagingProfileTypeT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanImagingProfileType,    new ScanImagingProfileTypeT(), dune::scan::types::ScanImagingProfileType::FAX)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CcdChannelEnum,            new CcdChannelEnumT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CcdChannelEnum,            new CcdChannelEnumT(), dune::scan::types::CcdChannelEnum::Blue)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BinaryRenderingEnum,       new BinaryRenderingEnumT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BinaryRenderingEnum,       new BinaryRenderingEnumT(), dune::scan::types::BinaryRenderingEnum::ErrorDiffusion)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::AutoColorDetectEnum,       new AutoColorDetectEnumT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::AutoColorDetectEnum,       new AutoColorDetectEnumT(), dune::scan::types::AutoColorDetectEnum::TreatNonColorAsBlackAndWhite1)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ImagePreview,              new ImagePreviewT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ImagePreview,              new ImagePreviewT(), dune::scan::types::ImagePreview::Enable)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanScaleSelectionEnum,    new ScanScaleSelectionEnumT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanScaleSelectionEnum,    new ScanScaleSelectionEnumT(), dune::scan::types::ScanScaleSelectionEnum::A4TOLETTER)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanAcquisitionsSpeedEnum, new ScanAcquisitionsSpeedEnumT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanAcquisitionsSpeedEnum, new ScanAcquisitionsSpeedEnumT(), dune::scan::types::ScanAcquisitionsSpeedEnum::SLOW)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ColorMode,                 new ColorModeT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ColorMode,                 new ColorModeT(), dune::imaging::types::ColorMode::BLACKANDWHITE)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ContentOrientation,        new ContentOrientationT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ContentOrientation,        new ContentOrientationT(), dune::imaging::types::ContentOrientation::LANDSCAPE)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OriginalContentType,       new OriginalContentTypeT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OriginalContentType,       new OriginalContentTypeT(), dune::imaging::types::OriginalContentType::GLOSSY)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaSizeId,               new MediaSizeIdT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaSizeId,               new MediaSizeIdT(), dune::imaging::types::MediaSizeId::A0)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::Plex,                      new PlexT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::Plex,                      new PlexT(), dune::imaging::types::Plex::DUPLEX)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PlexBinding,               new PlexBindingT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PlexBinding,               new PlexBindingT(), dune::imaging::types::PlexBinding::SHORT_EDGE)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::Resolution,                new ResolutionT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::Resolution,                new ResolutionT(), dune::imaging::types::Resolution::E100DPI)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaSource,               new MediaSourceT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaSource,               new MediaSourceT(), dune::imaging::types::MediaSource::ADF)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OutputCanvasAnchorType,    new OutputCanvasAnchorTypeT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OutputCanvasAnchorType,    new OutputCanvasAnchorTypeT(), dune::imaging::types::OutputCanvasAnchorType::BOTTOMCENTER)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaOrientation,          new MediaOrientationT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaOrientation,          new MediaOrientationT(), dune::imaging::types::MediaOrientation::LANDSCAPE)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaIdType,               new MediaIdTypeT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaIdType,               new MediaIdTypeT(), dune::imaging::types::MediaIdType::ADHESIVE)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaDestinationId,        new MediaDestinationIdT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaDestinationId,        new MediaDestinationIdT(), dune::imaging::types::MediaDestinationId::DEFAULT)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PrintQuality,              new PrintQualityT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PrintQuality,              new PrintQualityT(), dune::imaging::types::PrintQuality::BEST)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CopyMargins,               new CopyMarginsT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CopyMargins,               new CopyMarginsT(), dune::imaging::types::CopyMargins::ADDTOCONTENT)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PrintingOrder,             new PrintingOrderT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PrintingOrder,             new PrintingOrderT(), dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CopyOutputNumberUpCount,   new CopyOutputNumberUpCountT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CopyOutputNumberUpCount,   new CopyOutputNumberUpCountT(), dune::imaging::types::CopyOutputNumberUpCount::EightUp)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::SheetCollate,              new SheetCollateT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::SheetCollate,              new SheetCollateT(), dune::copy::SheetCollate::Uncollate)),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MinMaxLengthUInt,          new MinMaxLengthUIntT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnionMinMax(CopyIntentValues::MinMaxLengthUInt,    new MinMaxLengthUIntT(), 2)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::RangeValueInt,             new RangeValueIntT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnionRange(CopyIntentValues::RangeValueInt,        new RangeValueIntT(), 2)),
    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::RangeValueDouble,          new RangeValueDoubleT()),
                    DynamicRulesLargeFormatHelper::createIntentValuesUnionRange(CopyIntentValues::RangeValueDouble,     new RangeValueDoubleT(), 2))
));



class GivenParserHelperParametrizedUnionAndConstraint : public GivenParserHelper,
    public ::testing::WithParamInterface<std::tuple<std::shared_ptr<CopyIntentTableValueT>,std::shared_ptr<dune::framework::data::constraints::Constraints>>>
{
public:
    GivenParserHelperParametrizedUnionAndConstraint()
    {
        unionTable = std::get<0>(GetParam());
        staticConstraints = std::get<1>(GetParam());
    }

    std::shared_ptr<CopyIntentTableValueT> unionTable;
    std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints;
};

TEST_P(GivenParserHelperParametrizedUnionAndConstraint,WhenSetValuesOnConstraintIsCalled_ThenConstraintIsGeneratedAsExpected)
{
    checkConstraintLimitResult(unionTable,staticConstraints);
}

INSTANTIATE_TEST_CASE_P(, GivenParserHelperParametrizedUnionAndConstraint, ::testing::Values(
    std::make_tuple(FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::INT8, new INT8T()),
        DynamicRulesLargeFormatHelper::generateStaticConstraint(std::make_unique<dune::framework::data::constraints::RangeInt>(0, 0, 0, ""))),

    std::make_tuple(FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::INT16, new INT16T()),
        DynamicRulesLargeFormatHelper::generateStaticConstraint(std::make_unique<dune::framework::data::constraints::RangeInt>(0, 0, 0, ""))),

    std::make_tuple(FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::INT32, new INT32T()),
        DynamicRulesLargeFormatHelper::generateStaticConstraint(std::make_unique<dune::framework::data::constraints::RangeInt>(0, 0, 0, ""))),

    std::make_tuple(FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::INT64, new INT64T()),
        DynamicRulesLargeFormatHelper::generateStaticConstraint(std::make_unique<dune::framework::data::constraints::RangeInt>(0, 0, 0, ""))),

    std::make_tuple(FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::UINT8, new UINT8T()),
        DynamicRulesLargeFormatHelper::generateStaticConstraint(std::make_unique<dune::framework::data::constraints::RangeInt>(0, 0, 0, ""))),

    std::make_tuple(FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::UINT16, new UINT16T()),
        DynamicRulesLargeFormatHelper::generateStaticConstraint(std::make_unique<dune::framework::data::constraints::RangeInt>(0, 0, 0, ""))),

    std::make_tuple(FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::UINT32, new UINT32T()),
        DynamicRulesLargeFormatHelper::generateStaticConstraint(std::make_unique<dune::framework::data::constraints::RangeInt>(0, 0, 0, ""))),

    std::make_tuple(FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::UINT64, new UINT64T()),
        DynamicRulesLargeFormatHelper::generateStaticConstraint(std::make_unique<dune::framework::data::constraints::RangeInt>(0, 0, 0, ""))),

    std::make_tuple(FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::DOUBLE, new DOUBLET()),
        DynamicRulesLargeFormatHelper::generateStaticConstraint(std::make_unique<dune::framework::data::constraints::RangeDouble>(0, 0, 0, "")))
));

TEST_F(GivenParserHelper,WhenSetValuesOnConstraintIsCalledWithMinMaxUnion_ThenConstraintIsGeneratedAsExpected)
{
    auto unionMinMaxLengthUInt = FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::MinMaxLengthUInt,        new MinMaxLengthUIntT());
    checkConstraintMinMaxLength(unionMinMaxLengthUInt);
}

TEST_F(GivenParserHelper,WhenSetValuesOnConstraintIsCalledWithRangeIntUnion_ThenConstraintIsGeneratedAsExpected)
{
    auto unionRangeValueInt = FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::RangeValueInt,           new RangeValueIntT());
    checkConstraintRangeInt(unionRangeValueInt);
}

TEST_F(GivenParserHelper,WhenSetValuesOnConstraintIsCalledWithRangeDoubleUnion_ThenConstraintIsGeneratedAsExpected)
{
    auto unionRangeValueDouble = FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::RangeValueDouble,        new RangeValueDoubleT());
    checkConstraintRangeDouble(unionRangeValueDouble);
}



class GivenParserHelperParametrizedUnionEnumValue : public GivenParserHelper,
    public ::testing::WithParamInterface<std::shared_ptr<CopyIntentTableValueT>>
{
public:
    GivenParserHelperParametrizedUnionEnumValue()
    {
        unionTable = GetParam();
    }

    std::shared_ptr<CopyIntentTableValueT> unionTable;
};

TEST_P(GivenParserHelperParametrizedUnionEnumValue,WhenSetValuesOnConstraintIsCalled_ThenConstraintIsGeneratedAsExpected)
{
    checkConstraintValidResult(unionTable);
}

INSTANTIATE_TEST_CASE_P(, GivenParserHelperParametrizedUnionEnumValue, ::testing::Values(
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::BOOL,                    new BOOLT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::OriginalMediaType,       new OriginalMediaTypeT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::ScanSource,              new ScanSourceT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::ScanCaptureModeType,     new ScanCaptureModeTypeT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::CcdChannelEnum,          new CcdChannelEnumT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::BinaryRenderingEnum,     new BinaryRenderingEnumT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::AutoColorDetectEnum,     new AutoColorDetectEnumT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::ImagePreview,            new ImagePreviewT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::ScanScaleSelectionEnum,  new ScanScaleSelectionEnumT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::ScanAcquisitionsSpeedEnum, new ScanAcquisitionsSpeedEnumT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::ColorMode,               new ColorModeT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::ContentOrientation,      new ContentOrientationT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::OriginalContentType,     new OriginalContentTypeT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::MediaSizeId,             new MediaSizeIdT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::Plex,                    new PlexT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::PlexBinding,             new PlexBindingT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::Resolution,              new ResolutionT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::MediaSource,             new MediaSourceT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::OutputCanvasAnchorType,  new OutputCanvasAnchorTypeT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::MediaIdType,             new MediaIdTypeT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::MediaDestinationId,      new MediaDestinationIdT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::PrintQuality,            new PrintQualityT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::CopyMargins,             new CopyMarginsT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::PrintingOrder,           new PrintingOrderT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::CopyOutputNumberUpCount, new CopyOutputNumberUpCountT()),
    FlatBufferParserToCdmType::createCopyIntentUnionValue(CopyIntentValues::SheetCollate,            new SheetCollateT())
));

TEST_F(GivenParserHelper, WhenGetValuesNotAllowedIsCalledWithNoSupportedValues_ThenResultIsError)
{
    std::shared_ptr<ConstrainedValuesT> constraintValues = std::make_shared<ConstrainedValuesT>();
    constraintValues->supportedValues = std::vector<std::shared_ptr<CopyIntentTableValueT>>();

    # ifndef NDEBUG
        ASSERT_DEATH(FlatBufferParserToCdmType::getValuesNotAllowed(constraintValues, nullptr),"");
    # else
        auto result = FlatBufferParserToCdmType::getValuesNotAllowed(constraintValues, nullptr);
        EXPECT_EQ(result.size(), 0);
    # endif
}

TEST_F(GivenParserHelper, WhenGetValuesNotAllowedIsCalledWithConstrainedValuesOfVariousTypes_ThenResultIsError)
{
    std::shared_ptr<ConstrainedValuesT> constraintValues = std::make_shared<ConstrainedValuesT>();

    auto copyIntentTableValue = std::make_shared<CopyIntentTableValueT>();
    copyIntentTableValue->unionValue = CopyIntentValuesUnion(); // Type is CopyIntentValues::NONE by default

    auto copyIntentTableValue2 = std::make_shared<CopyIntentTableValueT>();
    copyIntentTableValue2->unionValue = DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT8, new INT8T());

    constraintValues->supportedValues = std::vector<std::shared_ptr<CopyIntentTableValueT>>({copyIntentTableValue, copyIntentTableValue2});

    # ifndef NDEBUG
        ASSERT_DEATH(FlatBufferParserToCdmType::getValuesNotAllowed(constraintValues, nullptr),"");
    # else
        auto result = FlatBufferParserToCdmType::getValuesNotAllowed(constraintValues, nullptr);
        EXPECT_EQ(result.size(), 0);
    # endif
}

TEST_F(GivenParserHelper, WhenGetValuesNotAllowedIsCalledWithNoneConstraint_ThenResultIsEmpty)
{
    std::shared_ptr<ConstrainedValuesT> constraintValues = std::make_shared<ConstrainedValuesT>();

    auto copyIntentTableValue = std::make_shared<CopyIntentTableValueT>();
    copyIntentTableValue->unionValue = CopyIntentValuesUnion(); // Type is CopyIntentValues::NONE by default

    constraintValues->supportedValues = std::vector<std::shared_ptr<CopyIntentTableValueT>>({copyIntentTableValue});

    auto result = FlatBufferParserToCdmType::getValuesNotAllowed(constraintValues, nullptr);

    EXPECT_EQ(result.size(), 0);
}



class GivenParserHelperParametrizedWithSignedNumeralIntentValues : public GivenParserHelper,
    public ::testing::WithParamInterface< std::tuple<std::vector<std::shared_ptr<CopyIntentTableValueT>>, int, int>>
{
public:
    GivenParserHelperParametrizedWithSignedNumeralIntentValues()
    {
        supportedValues = std::get<0>(GetParam());
        minNotAllowedValue = std::get<1>(GetParam());
        maxNotAllowedValue = std::get<2>(GetParam());
    }

protected:
    std::vector<std::shared_ptr<CopyIntentTableValueT>> supportedValues;

    int minNotAllowedValue {0};
    int maxNotAllowedValue {0};
};

TEST_P(GivenParserHelperParametrizedWithSignedNumeralIntentValues, WhenGetValuesNotAllowedIsCalled_ThenResultIsARangeWithCorrectMinMax)
{
    std::shared_ptr<ConstrainedValuesT> constraintValues = std::make_shared<ConstrainedValuesT>();

    constraintValues->supportedValues = supportedValues;

    auto result = FlatBufferParserToCdmType::getValuesNotAllowed(constraintValues, nullptr);

    EXPECT_EQ(result.size(), 1);
    EXPECT_TRUE(result[0]->unionValue.type == CopyIntentValues::RangeValueInt);

    RangeValueIntT* fbTable = (RangeValueIntT*)result[0]->unionValue.value;
    EXPECT_EQ(fbTable->min, minNotAllowedValue);
    EXPECT_EQ(fbTable->max, maxNotAllowedValue);
}

INSTANTIATE_TEST_CASE_P(, GivenParserHelperParametrizedWithSignedNumeralIntentValues,
::testing::Values(

    // Test: Using only one supported value, results in a range of the same value.
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT8, new INT8T(), 2)), 2, 2),
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT16, new INT16T(), 2)), 2, 2),
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT32, new INT32T(), 2)), 2, 2),
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT64, new INT64T(), 2)), 2, 2),


    // Test: Use of the same supported value dont affect the limit.
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT8, new INT8T(), 1),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT8, new INT8T(), 1)
        }), 1, 1),

    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT16, new INT16T(), 1),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT16, new INT16T(), 1)
        }), 1, 1),

    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT32, new INT32T(), 1),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT32, new INT32T(), 1)
        }), 1, 1),

    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT64, new INT64T(), 1),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT64, new INT64T(), 1)
        }), 1, 1),


    // Test: Different values affect the range min/max
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT8, new INT8T(), -5),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT8, new INT8T(), 5)
        }), -5, 5),

    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT16, new INT16T(), -5),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT16, new INT16T(), 5)
        }), -5, 5),

    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT32, new INT32T(), -5),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT32, new INT32T(), 5)
        }), -5, 5),

    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT64, new INT64T(), -5),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::INT64, new INT64T(), 5)
        }), -5, 5)

    // We could add cases using the variable limits.
));



class GivenParserHelperParametrizedWithUnsignedNumeralIntentValues : public GivenParserHelper,
    public ::testing::WithParamInterface< std::tuple<std::vector<std::shared_ptr<CopyIntentTableValueT>>, uint, uint>>
{
public:
    GivenParserHelperParametrizedWithUnsignedNumeralIntentValues()
    {
        supportedValues = std::get<0>(GetParam());
        minNotAllowedValue = std::get<1>(GetParam());
        maxNotAllowedValue = std::get<2>(GetParam());
    }

protected:
    std::vector<std::shared_ptr<CopyIntentTableValueT>> supportedValues;

    uint minNotAllowedValue {0u};
    uint maxNotAllowedValue {0u};
};

TEST_P(GivenParserHelperParametrizedWithUnsignedNumeralIntentValues, WhenGetValuesNotAllowedIsCalled_ThenResultIsMinMaxLengthWithCorrectMinMax)
{
    std::shared_ptr<ConstrainedValuesT> constraintValues = std::make_shared<ConstrainedValuesT>();

    constraintValues->supportedValues = supportedValues;

    auto result = FlatBufferParserToCdmType::getValuesNotAllowed(constraintValues, nullptr);

    EXPECT_EQ(result.size(), 1);
    EXPECT_TRUE(result[0]->unionValue.type == CopyIntentValues::MinMaxLengthUInt);

    MinMaxLengthUIntT* fbTable = (MinMaxLengthUIntT*)result[0]->unionValue.value;
    EXPECT_EQ(fbTable->minLength, minNotAllowedValue);
    EXPECT_EQ(fbTable->maxLength, maxNotAllowedValue);
}

INSTANTIATE_TEST_CASE_P(, GivenParserHelperParametrizedWithUnsignedNumeralIntentValues,
::testing::Values(

    // Test: Using only one supported value, results in a range of the same value.
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT8, new UINT8T(),   2u)), 2u, 2u),
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT16, new UINT16T(), 2u)), 2u, 2u),
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT32, new UINT32T(), 2u)), 2u, 2u),
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT64, new UINT64T(), 2u)), 2u, 2u),


    // Test: Use of the same supported value dont affect the limit.
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT8, new UINT8T(), 1u),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT8, new UINT8T(), 1u)
        }), 1u, 1u),

    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT16, new UINT16T(), 1u),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT16, new UINT16T(), 1u)
        }), 1u, 1u),

    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT32, new UINT32T(), 1u),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT32, new UINT32T(), 1u)
        }), 1u, 1u),

    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT64, new UINT64T(), 1u),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT64, new UINT64T(), 1u)
        }), 1u, 1u),


    // Test: Different values affect the range min/max
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT8, new UINT8T(), 1u),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT8, new UINT8T(), 5u)
        }), 1u, 5u),

    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT16, new UINT16T(), 1u),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT16, new UINT16T(), 5u)
        }), 1u, 5u),

    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT32, new UINT32T(), 1u),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT32, new UINT32T(), 5u)
        }), 1u, 5u),

    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT64, new UINT64T(), 1u),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::UINT64, new UINT64T(), 5u)
        }), 1u, 5u)

    // We could add cases using the variable limits.
));



class GivenParserHelperParametrizedWithDoubleNumeralIntentValues : public GivenParserHelper,
    public ::testing::WithParamInterface< std::tuple<std::vector<std::shared_ptr<CopyIntentTableValueT>>, double, double>>
{
public:
    GivenParserHelperParametrizedWithDoubleNumeralIntentValues()
    {
        supportedValues = std::get<0>(GetParam());
        minNotAllowedValue = std::get<1>(GetParam());
        maxNotAllowedValue = std::get<2>(GetParam());
    }

protected:
    std::vector<std::shared_ptr<CopyIntentTableValueT>> supportedValues;

    double minNotAllowedValue {0.0};
    double maxNotAllowedValue {0.0};
};

TEST_P(GivenParserHelperParametrizedWithDoubleNumeralIntentValues, WhenGetValuesNotAllowedIsCalled_ThenResultIsARangeDoubleWithCorrectMinMax)
{
    std::shared_ptr<ConstrainedValuesT> constraintValues = std::make_shared<ConstrainedValuesT>();

    constraintValues->supportedValues = supportedValues;

    auto result = FlatBufferParserToCdmType::getValuesNotAllowed(constraintValues, nullptr);

    EXPECT_EQ(result.size(), 1);
    EXPECT_TRUE(result[0]->unionValue.type == CopyIntentValues::RangeValueDouble);

    RangeValueDoubleT* fbTable = (RangeValueDoubleT*)result[0]->unionValue.value;
    EXPECT_DOUBLE_EQ(fbTable->min, minNotAllowedValue);
    EXPECT_DOUBLE_EQ(fbTable->max, maxNotAllowedValue);
}

INSTANTIATE_TEST_CASE_P(, GivenParserHelperParametrizedWithDoubleNumeralIntentValues,
::testing::Values(

    // Test: Using only one supported value, results in a range of the same value.
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::DOUBLE, new DOUBLET(), 1.0)), 1.0, 1.0),


    // Test: Use of the same supported value dont affect the limit.
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::DOUBLE, new DOUBLET(), 1.0),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::DOUBLE, new DOUBLET(), 1.0)
        }), 1.0, 1.0),


    // Test: Different values affect the range min/max
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues({
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::DOUBLE, new DOUBLET(), 1.0),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::DOUBLE, new DOUBLET(), 2.0)
        }), 1.0, 2.0)

    // We could add cases using the variable limits.
));



class GivenParserHelperParametrizedWithRangeIntentValues : public GivenParserHelper,
    public ::testing::WithParamInterface< std::tuple<std::vector<std::shared_ptr<CopyIntentTableValueT>>, uint>>
{
public:
    GivenParserHelperParametrizedWithRangeIntentValues()
    {
        supportedValues = std::get<0>(GetParam());
        amountOfValuesNotAllowed = std::get<1>(GetParam());
    }

protected:
    std::vector<std::shared_ptr<CopyIntentTableValueT>> supportedValues;
    uint amountOfValuesNotAllowed {0u};
};

TEST_P(GivenParserHelperParametrizedWithRangeIntentValues, WhenGetValuesNotAllowedIsCalled_ThenResultSizeIsCorrect)
{
    std::shared_ptr<ConstrainedValuesT> constraintValues = std::make_shared<ConstrainedValuesT>();

    constraintValues->supportedValues = supportedValues;

    auto result = FlatBufferParserToCdmType::getValuesNotAllowed(constraintValues, nullptr);

    EXPECT_EQ(result.size(), amountOfValuesNotAllowed);
}

INSTANTIATE_TEST_CASE_P(, GivenParserHelperParametrizedWithRangeIntentValues,
::testing::Values(

    // Supported values of type range are directly translated to not allowed values

    // Therefore, when sending one supported value, only one value not allowed is computed.
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MinMaxLengthUInt, new MinMaxLengthUIntT())), 1),
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::RangeValueInt, new RangeValueIntT())), 1),
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::RangeValueDouble, new RangeValueDoubleT())), 1),
    // std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::TEXT, new TEXTT())), 1), // Not supported yet

    // And... when sending x supported values, x values not allowed are computed.
    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(
        {
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MinMaxLengthUInt, new MinMaxLengthUIntT()),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MinMaxLengthUInt, new MinMaxLengthUIntT())
        }), 2),

    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(
        {
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::RangeValueInt, new RangeValueIntT()),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::RangeValueInt, new RangeValueIntT())
        }), 2),

    std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(
        {
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::RangeValueDouble, new RangeValueDoubleT()),
            DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::RangeValueDouble, new RangeValueDoubleT())
        }), 2)

    // Not supported yet
    // std::make_tuple(DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(
    //     {
    //         DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::TEXT, new TEXTT()),
    //         DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::TEXT, new TEXTT())
    //     }), 2)

));



class GivenParserHelperParametrizedWithEnumIntentValuesAndConstraintsNotDefined : public GivenParserHelper,
    public ::testing::WithParamInterface<CopyIntentValuesUnion>
{
public:
    GivenParserHelperParametrizedWithEnumIntentValuesAndConstraintsNotDefined()
    {
        // Generate copy supported values vector
        supportedValues = DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(GetParam());
    }

protected:
    std::vector<std::shared_ptr<CopyIntentTableValueT>> supportedValues;
};

TEST_P(GivenParserHelperParametrizedWithEnumIntentValuesAndConstraintsNotDefined, WhenGetValuesNotAllowedIsCalled_ThenResultSizeIsCorrect)
{
    std::shared_ptr<ConstrainedValuesT> constraintValues = std::make_shared<ConstrainedValuesT>();

    constraintValues->supportedValues = supportedValues;

    // No constraints defined in this fixture
    std::vector<std::shared_ptr<CopyIntentTableValueT>> result = FlatBufferParserToCdmType::getValuesNotAllowed(constraintValues, nullptr);

    // We expect the result to be empty, since all values are allowed
    EXPECT_TRUE(result.empty());
}

INSTANTIATE_TEST_CASE_P(, GivenParserHelperParametrizedWithEnumIntentValuesAndConstraintsNotDefined,
::testing::Values(

    // Since we are not defining a constraint, all values should be allowed.
    // Thus getValuesNotAllowed return an empty vector. We expect 0 results in this case. (Empty vector)
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BOOL,                      new BOOLT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::AttachmentSize,            new AttachmentSizeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OriginalMediaType,         new OriginalMediaTypeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanSource,                new ScanSourceT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanFeedOrientation,       new ScanFeedOrientationT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BlankDetectEnum,           new BlankDetectEnumT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OverScanType,              new OverScanTypeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanCaptureModeType,       new ScanCaptureModeTypeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanImagingProfileType,    new ScanImagingProfileTypeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CcdChannelEnum,            new CcdChannelEnumT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BinaryRenderingEnum,       new BinaryRenderingEnumT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::AutoColorDetectEnum,       new AutoColorDetectEnumT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ImagePreview,              new ImagePreviewT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanScaleSelectionEnum,    new ScanScaleSelectionEnumT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanAcquisitionsSpeedEnum, new ScanAcquisitionsSpeedEnumT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ColorMode,                 new ColorModeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ContentOrientation,        new ContentOrientationT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OriginalContentType,       new OriginalContentTypeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaSizeId,               new MediaSizeIdT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::Plex,                      new PlexT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PlexBinding,               new PlexBindingT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::Resolution,                new ResolutionT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaSource,               new MediaSourceT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OutputCanvasAnchorType,    new OutputCanvasAnchorTypeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaOrientation,          new MediaOrientationT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaIdType,               new MediaIdTypeT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaDestinationId,        new MediaDestinationIdT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PrintQuality,              new PrintQualityT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CopyMargins,               new CopyMarginsT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PrintingOrder,             new PrintingOrderT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CopyOutputNumberUpCount,   new CopyOutputNumberUpCountT()),
    DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::SheetCollate,              new SheetCollateT())
));



class GivenParserHelperParametrizedWithEnumIntentValuesAndAllConstraintsAreSupported : public GivenParserHelper,
    public ::testing::WithParamInterface<std::tuple<CopyIntentValuesUnion, std::shared_ptr<dune::framework::data::constraints::Constraints>>>
{
public:
    GivenParserHelperParametrizedWithEnumIntentValuesAndAllConstraintsAreSupported()
    {
        supportedValues = DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(std::get<0>(GetParam()));
        staticConstraints = std::get<1>(GetParam());
    }

protected:
    std::vector<std::shared_ptr<CopyIntentTableValueT>> supportedValues;
    std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints {nullptr};
};

TEST_P(GivenParserHelperParametrizedWithEnumIntentValuesAndAllConstraintsAreSupported, WhenGetValuesNotAllowedIsCalled_ThenResultSizeIsCorrect)
{
    std::shared_ptr<ConstrainedValuesT> constraintValues = std::make_shared<ConstrainedValuesT>();

    constraintValues->supportedValues = supportedValues;
    std::vector<std::shared_ptr<CopyIntentTableValueT>> result = FlatBufferParserToCdmType::getValuesNotAllowed(constraintValues, staticConstraints);

    // We expect the result to be empty, since all values are allowed
    EXPECT_TRUE(result.empty());
}

INSTANTIATE_TEST_CASE_P(, GivenParserHelperParametrizedWithEnumIntentValuesAndAllConstraintsAreSupported,
::testing::Values(

    // All the constraints are included in the supported values. All values are supported. (We expect an empty vector)
    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BOOL, new BOOLT(), true),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::FeatureEnabledEnum>({dune::cdm::glossary_1::FeatureEnabled::true_})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OriginalMediaType, new OriginalMediaTypeT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::ScanMediaType>({dune::cdm::glossary_1::ScanMediaType::whitePaper})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanSource, new ScanSourceT(), dune::scan::types::ScanSource::MDF),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::ScanMediaSourceId>({dune::cdm::glossary_1::ScanMediaSourceId::mdf})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanCaptureModeType, new ScanCaptureModeTypeT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::ScanCaptureMode>({dune::cdm::jobTicket_1::ScanCaptureMode::standard})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CcdChannelEnum, new CcdChannelEnumT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::CcdChannel>({dune::cdm::jobTicket_1::CcdChannel::ntsc})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BinaryRenderingEnum, new BinaryRenderingEnumT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::BinaryRendering>({dune::cdm::jobTicket_1::BinaryRendering::halftone})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::AutoColorDetectEnum, new AutoColorDetectEnumT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::AutoColorDetect>({dune::cdm::jobTicket_1::AutoColorDetect::detectOnly})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ImagePreview, new ImagePreviewT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration>({dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration::disable})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanScaleSelectionEnum, new ScanScaleSelectionEnumT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::scaling::ScaleSelection>({dune::cdm::jobTicket_1::scaling::ScaleSelection::none})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanAcquisitionsSpeedEnum, new ScanAcquisitionsSpeedEnumT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::ScanAcquisitionsSpeed>({dune::cdm::jobTicket_1::ScanAcquisitionsSpeed::auto_})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ColorMode, new ColorModeT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::ColorModes>({dune::cdm::jobTicket_1::ColorModes::autoDetect})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ContentOrientation, new ContentOrientationT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::ContentOrientation>({dune::cdm::glossary_1::ContentOrientation::portrait})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OriginalContentType, new OriginalContentTypeT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::ContentType>({dune::cdm::jobTicket_1::ContentType::autoDetect})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaSizeId, new MediaSizeIdT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::MediaSize>({dune::cdm::glossary_1::MediaSize::any})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::Plex, new PlexT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::PlexMode>({dune::cdm::glossary_1::PlexMode::simplex})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PlexBinding, new PlexBindingT(), dune::imaging::types::PlexBinding::SHORT_EDGE),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::DuplexBinding>({dune::cdm::glossary_1::DuplexBinding::twoSidedShortEdge})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::Resolution, new ResolutionT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::Resolutions>({dune::cdm::jobTicket_1::Resolutions::e75Dpi})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaSource, new MediaSourceT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::MediaSourceId>({dune::cdm::glossary_1::MediaSourceId::auto_})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OutputCanvasAnchorType, new OutputCanvasAnchorTypeT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::OutputCanvasAnchor>({dune::cdm::jobTicket_1::OutputCanvasAnchor::topLeft})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaIdType, new MediaIdTypeT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::MediaType>({dune::cdm::glossary_1::MediaType::custom})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaDestinationId, new MediaDestinationIdT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::MediaDestinationId>({dune::cdm::glossary_1::MediaDestinationId::standard_dash_bin})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PrintQuality, new PrintQualityT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::PrintQuality>({dune::cdm::glossary_1::PrintQuality::draft})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CopyMargins, new CopyMarginsT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::PrintMargins>({dune::cdm::jobTicket_1::PrintMargins::oversize})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PrintingOrder, new PrintingOrderT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::PrintingOrder>({dune::cdm::jobTicket_1::PrintingOrder::firstPageOnTop})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CopyOutputNumberUpCount, new CopyOutputNumberUpCountT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::PagesPerSheet>({dune::cdm::jobTicket_1::PagesPerSheet::oneUp})
    ),

    std::make_tuple(DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::SheetCollate, new SheetCollateT()),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::CollateModes>({dune::cdm::jobTicket_1::CollateModes::collated})
    )
));



class GivenParserHelperParametrizedWithEnumIntentValuesAndNoConstraintIsSupported : public GivenParserHelper,
    public ::testing::WithParamInterface< std::tuple<CopyIntentValuesUnion, std::shared_ptr<dune::framework::data::constraints::Constraints>, CopyIntentValuesUnion>>
{
public:
    GivenParserHelperParametrizedWithEnumIntentValuesAndNoConstraintIsSupported()
    {
        supportedValues = DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(std::get<0>(GetParam()));
        staticConstraints = std::get<1>(GetParam());
        expectedResult = DynamicRulesLargeFormatHelper::generateCopyIntentTableValues(std::get<2>(GetParam()));
    }

protected:
    std::vector<std::shared_ptr<CopyIntentTableValueT>> supportedValues;
    std::shared_ptr<dune::framework::data::constraints::Constraints> staticConstraints {nullptr};
    std::vector<std::shared_ptr<CopyIntentTableValueT>> expectedResult;
};

TEST_P(GivenParserHelperParametrizedWithEnumIntentValuesAndNoConstraintIsSupported, WhenGetValuesNotAllowedIsCalled_ThenResultContainsTheCorrectValuesNotAllowed)
{
    std::shared_ptr<ConstrainedValuesT> constraintValues = std::make_shared<ConstrainedValuesT>();

    constraintValues->supportedValues = supportedValues;

    std::vector<std::shared_ptr<CopyIntentTableValueT>> result = FlatBufferParserToCdmType::getValuesNotAllowed(constraintValues, staticConstraints);

    // Compare result with expectedResult.
    ASSERT_EQ(result.size(), expectedResult.size());

    // Both arrays are unordered, seems like the best solution is O(N^2)
    for (auto expectedResultItem : expectedResult)
    {
        // Search expectedResultItem in the getValuesNotAllowed result vector.
        auto iterator = std::find_if(result.begin(),result.end(),
            [&](std::shared_ptr<CopyIntentTableValueT> resultValue)
            {
                // This function is safe to use, we have testing above in this file.
                return FlatBufferParserToCdmType::compareUnionValue(expectedResultItem->unionValue, resultValue->unionValue);
            }
        );

        // We expect to find the item always
        EXPECT_FALSE(iterator == result.end());
    }
}

INSTANTIATE_TEST_CASE_P(, GivenParserHelperParametrizedWithEnumIntentValuesAndNoConstraintIsSupported,
::testing::Values(

    // Here the constraint doesn't appear in the supported values. Therefore its not supported && appears in the expectedResult vector.
    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BOOL, new BOOLT(), false),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::FeatureEnabledEnum>({dune::cdm::glossary_1::FeatureEnabled::true_}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BOOL, new BOOLT(), true)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OriginalMediaType, new OriginalMediaTypeT(), dune::scan::types::OriginalMediaType::PHOTO_PAPER),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::ScanMediaType>({dune::cdm::glossary_1::ScanMediaType::whitePaper}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OriginalMediaType, new OriginalMediaTypeT(), dune::scan::types::OriginalMediaType::WHITE_PAPER)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanSource, new ScanSourceT(), dune::scan::types::ScanSource::GLASS),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::ScanMediaSourceId>({dune::cdm::glossary_1::ScanMediaSourceId::mdf}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanSource, new ScanSourceT(), dune::scan::types::ScanSource::MDF)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanCaptureModeType, new ScanCaptureModeTypeT(), dune::scan::types::ScanCaptureModeType::JOBBUILD),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::ScanCaptureMode>({dune::cdm::jobTicket_1::ScanCaptureMode::standard}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanCaptureModeType, new ScanCaptureModeTypeT(), dune::scan::types::ScanCaptureModeType::STANDARD)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CcdChannelEnum, new CcdChannelEnumT(), dune::scan::types::CcdChannelEnum::GrayCcd),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::CcdChannel>({dune::cdm::jobTicket_1::CcdChannel::ntsc}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CcdChannelEnum, new CcdChannelEnumT(), dune::scan::types::CcdChannelEnum::NTSC)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BinaryRenderingEnum, new BinaryRenderingEnumT(), dune::scan::types::BinaryRenderingEnum::Threshold),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::BinaryRendering>({dune::cdm::jobTicket_1::BinaryRendering::halftone}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::BinaryRenderingEnum, new BinaryRenderingEnumT(), dune::scan::types::BinaryRenderingEnum::Halftone)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::AutoColorDetectEnum, new AutoColorDetectEnumT(), dune::scan::types::AutoColorDetectEnum::TreatNonColorAsBlackAndWhite1),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::AutoColorDetect>({dune::cdm::jobTicket_1::AutoColorDetect::detectOnly}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::AutoColorDetectEnum, new AutoColorDetectEnumT(), dune::scan::types::AutoColorDetectEnum::DetectOnly)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ImagePreview, new ImagePreviewT(), dune::scan::types::ImagePreview::Enable),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration>({dune::cdm::jobTicket_1::manualUserOperations::ImagePreviewConfiguration::disable}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ImagePreview, new ImagePreviewT(), dune::scan::types::ImagePreview::Disable)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanScaleSelectionEnum, new ScanScaleSelectionEnumT(), dune::scan::types::ScanScaleSelectionEnum::CUSTOM),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::scaling::ScaleSelection>({dune::cdm::jobTicket_1::scaling::ScaleSelection::none}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanScaleSelectionEnum, new ScanScaleSelectionEnumT(), dune::scan::types::ScanScaleSelectionEnum::NONE)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanAcquisitionsSpeedEnum, new ScanAcquisitionsSpeedEnumT(), dune::scan::types::ScanAcquisitionsSpeedEnum::SLOW),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::ScanAcquisitionsSpeed>({dune::cdm::jobTicket_1::ScanAcquisitionsSpeed::auto_}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ScanAcquisitionsSpeedEnum, new ScanAcquisitionsSpeedEnumT(), dune::scan::types::ScanAcquisitionsSpeedEnum::AUTO)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ColorMode, new ColorModeT(), dune::imaging::types::ColorMode::MONOCHROME),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::ColorModes>({dune::cdm::jobTicket_1::ColorModes::autoDetect}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ColorMode, new ColorModeT(), dune::imaging::types::ColorMode::AUTODETECT)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ContentOrientation, new ContentOrientationT(), dune::imaging::types::ContentOrientation::LANDSCAPE),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::ContentOrientation>({dune::cdm::glossary_1::ContentOrientation::portrait}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::ContentOrientation, new ContentOrientationT(), dune::imaging::types::ContentOrientation::PORTRAIT)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OriginalContentType, new OriginalContentTypeT(), dune::imaging::types::OriginalContentType::TEXT),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::ContentType>({dune::cdm::jobTicket_1::ContentType::autoDetect}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OriginalContentType, new OriginalContentTypeT(), dune::imaging::types::OriginalContentType::AUTO)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaSizeId, new MediaSizeIdT(), dune::imaging::types::MediaSizeId::A0),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::MediaSize>({dune::cdm::glossary_1::MediaSize::any}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaSizeId, new MediaSizeIdT(), dune::imaging::types::MediaSizeId::ANY)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::Plex, new PlexT(), dune::imaging::types::Plex::DUPLEX),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::PlexMode>({dune::cdm::glossary_1::PlexMode::simplex}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::Plex, new PlexT(), dune::imaging::types::Plex::SIMPLEX)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PlexBinding, new PlexBindingT(), dune::imaging::types::PlexBinding::LONG_EDGE),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::DuplexBinding>({dune::cdm::glossary_1::DuplexBinding::twoSidedShortEdge}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PlexBinding, new PlexBindingT(), dune::imaging::types::PlexBinding::SHORT_EDGE)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::Resolution, new ResolutionT(), dune::imaging::types::Resolution::E100DPI),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::Resolutions>({dune::cdm::jobTicket_1::Resolutions::e75Dpi}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::Resolution, new ResolutionT(), dune::imaging::types::Resolution::E75DPI)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaSource, new MediaSourceT(), dune::imaging::types::MediaSource::TRAY1),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::MediaSourceId>({dune::cdm::glossary_1::MediaSourceId::auto_}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaSource, new MediaSourceT(), dune::imaging::types::MediaSource::AUTOSELECT)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OutputCanvasAnchorType, new OutputCanvasAnchorTypeT(), dune::imaging::types::OutputCanvasAnchorType::TOPCENTER),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::OutputCanvasAnchor>({dune::cdm::jobTicket_1::OutputCanvasAnchor::topLeft}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::OutputCanvasAnchorType, new OutputCanvasAnchorTypeT(), dune::imaging::types::OutputCanvasAnchorType::TOPLEFT)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaIdType, new MediaIdTypeT(), dune::imaging::types::MediaIdType::ANY),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::MediaType>({dune::cdm::glossary_1::MediaType::custom}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaIdType, new MediaIdTypeT(), dune::imaging::types::MediaIdType::CUSTOM)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaDestinationId, new MediaDestinationIdT(), dune::imaging::types::MediaDestinationId::OUTPUTBIN1),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::MediaDestinationId>({dune::cdm::glossary_1::MediaDestinationId::standard_dash_bin}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::MediaDestinationId, new MediaDestinationIdT(), dune::imaging::types::MediaDestinationId::STANDARDBIN)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PrintQuality, new PrintQualityT(), dune::imaging::types::PrintQuality::NORMAL),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::glossary_1::PrintQuality>({dune::cdm::glossary_1::PrintQuality::draft}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PrintQuality, new PrintQualityT(), dune::imaging::types::PrintQuality::DRAFT)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CopyMargins, new CopyMarginsT(), dune::imaging::types::CopyMargins::CLIPCONTENT),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::PrintMargins>({dune::cdm::jobTicket_1::PrintMargins::oversize}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CopyMargins, new CopyMarginsT(), dune::imaging::types::CopyMargins::OVERSIZE)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PrintingOrder, new PrintingOrderT(), dune::imaging::types::PrintingOrder::LAST_PAGE_ON_TOP),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::PrintingOrder>({dune::cdm::jobTicket_1::PrintingOrder::firstPageOnTop}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::PrintingOrder, new PrintingOrderT(), dune::imaging::types::PrintingOrder::FIRST_PAGE_ON_TOP)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CopyOutputNumberUpCount, new CopyOutputNumberUpCountT(), dune::imaging::types::CopyOutputNumberUpCount::TwoUp),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::PagesPerSheet>({dune::cdm::jobTicket_1::PagesPerSheet::oneUp}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::CopyOutputNumberUpCount, new CopyOutputNumberUpCountT(), dune::imaging::types::CopyOutputNumberUpCount::OneUp)
    ),

    std::make_tuple(
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::SheetCollate, new SheetCollateT(), dune::copy::SheetCollate::Uncollate),
        DynamicRulesLargeFormatHelper::generatePossibleValuesConstraint<dune::cdm::jobTicket_1::CollateModes>({dune::cdm::jobTicket_1::CollateModes::collated}),
        DynamicRulesLargeFormatHelper::createIntentValuesUnion(CopyIntentValues::SheetCollate, new SheetCollateT(), dune::copy::SheetCollate::Collate)
    )
));
