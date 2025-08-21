/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobStaticConstraintRules.cpp
 * @date   Tue, 08 August 2022
 * @brief  Base class for CopyJob Constraint rules
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobStaticConstraintRules.h"
#include "StringIds.h"

#include "common_debug.h"
#include "CopyJobStaticConstraintRules_TraceAutogen.h"
#include "CopyJobTicket.h"
#include "typeMappers.h"
#include "MediaCdmHelper.h"
#include "ParameterizedString.h"
#include "FoldingStyle_generated.h"

using namespace dune::copy::Jobs::Copy;
using namespace dune::job::cdm;
using namespace dune::cdm::glossary_1;

#define MEDIA_SOURCE_MAP_COUNTER_ACCEPTED 2


std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getCopyMarginsConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    // Get printMargins for valid values.
    auto tempCopyMargins =  jobTicket->getConstraints()->getCopyMargins();
    auto possibleCopyMargins = std::vector<dune::cdm::jobTicket_1::PrintMargins>();
    auto validCopyMargins = std::vector<dune::cdm::jobTicket_1::PrintMargins>();
    for(auto iter = tempCopyMargins.begin(); iter != tempCopyMargins.end(); iter++)
    {
        possibleCopyMargins.push_back(mapToCdm(*iter));
        //if(!SomethingPreventsThisFromBeingValid(*iter)) // if something prevents a valid value for this, add the logic here
        validCopyMargins.push_back(mapToCdm(*iter));
    }

    auto constraints = std::make_shared<Constraints>();

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::jobTicket_1::PrintMargins>>(possibleCopyMargins, &dune::cdm::jobTicket_1::PrintMargins::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::jobTicket_1::PrintMargins>>(validCopyMargins, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getPrintingOrderConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    // Get PrintingOrder for valid values.
    auto tempPrintingOrder =  jobTicket->getConstraints()->getPrintingOrder();
    auto possiblePrintingOrder = std::vector<dune::cdm::jobTicket_1::PrintingOrder>();
    auto validPrintingOrder = std::vector<dune::cdm::jobTicket_1::PrintingOrder>();
    for(auto iter = tempPrintingOrder.begin(); iter != tempPrintingOrder.end(); iter++)
    {
        possiblePrintingOrder.push_back(mapToCdm(*iter));
        //if(!SomethingPreventsThisFromBeingValid(*iter)) // if something prevents a valid value for this, add the logic here
        validPrintingOrder.push_back(mapToCdm(*iter));
    }

    auto constraints = std::make_shared<Constraints>();

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::jobTicket_1::PrintingOrder>>(possiblePrintingOrder, &dune::cdm::jobTicket_1::PrintingOrder::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::jobTicket_1::PrintingOrder>>(validPrintingOrder, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getMediaFamilyConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    // Get MediaFamily for valid values.
    auto tempMediaFamily =  jobTicket->getConstraints()->getMediaFamily();
    auto possibleMediaFamily = std::vector<dune::cdm::mediaProfile_1::MediaFamily>();
    auto validMediaFamily = std::vector<dune::cdm::mediaProfile_1::MediaFamily>();
    for(auto iter = tempMediaFamily.begin(); iter != tempMediaFamily.end(); iter++)
    {
        possibleMediaFamily.push_back(mapToCdm(*iter));
        //if(!SomethingPreventsThisFromBeingValid(*iter)) // if something prevents a valid value for this, add the logic here
        validMediaFamily.push_back(mapToCdm(*iter));
    }

    auto constraints = std::make_shared<Constraints>();

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::mediaProfile_1::MediaFamily>>(possibleMediaFamily, &dune::cdm::mediaProfile_1::MediaFamilyEnum::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::mediaProfile_1::MediaFamily>>(validMediaFamily, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getRotateConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    // Get Rotate for valid values.
    auto minRotation    =  jobTicket->getConstraints()->getMinRotation();
    auto maxRotation    =  jobTicket->getConstraints()->getMaxRotation();
    auto stepRotation   =  jobTicket->getConstraints()->getStepRotation();
    auto tempAutoRotate =  jobTicket->getConstraints()->getAutoRotate();
    auto tempRotate     = std::vector<dune::cdm::jobTicket_1::Rotate>();

    //We want to add the AUTO constraint only if autorotate can be true
    if (std::find(tempAutoRotate.begin(), tempAutoRotate.end(), true) != tempAutoRotate.end())
    {
        tempRotate.push_back(dune::cdm::jobTicket_1::Rotate::auto_);
    }
    //We want to add each possible case to Rotate appart from AUTO
    for (int i = minRotation; i <= maxRotation; i += stepRotation) 
    {
        //TODO: see how we can control errors here
        tempRotate.push_back(mapToCdmRotate(i));
    }

    auto possibleRotate = std::vector<dune::cdm::jobTicket_1::Rotate>();
    auto validRotate = std::vector<dune::cdm::jobTicket_1::Rotate>();
    for(auto iter = tempRotate.begin(); iter != tempRotate.end(); iter++)
    {
        possibleRotate.push_back(*iter);
        //if(!SomethingPreventsThisFromBeingValid(*iter)) // if something prevents a valid value for this, add the logic here
        validRotate.push_back(*iter);
    }

    auto constraints = std::make_shared<Constraints>();

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::jobTicket_1::Rotate>>(possibleRotate, &dune::cdm::jobTicket_1::RotateEnum::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::jobTicket_1::Rotate>>(validRotate, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getStapleOptionConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    // Get StapleOption for possible & valid values.
    std::string constraintsmsg="";
    auto resPossibleOptions = jobTicket->getPossibleStaplingOptions();
    APIResult possibleResult = std::get<0>(resPossibleOptions);
    auto resValidOptions = jobTicket->getValidStaplingOptions(constraintsmsg);
    APIResult validResult = std::get<0>(resValidOptions);
    
    auto possibleStapleOption = std::vector<dune::cdm::jobTicket_1::StapleOptions>();
    auto validStapleOption = std::vector<dune::cdm::jobTicket_1::StapleOptions>();

    auto constraints = std::make_shared<Constraints>();

    CHECKPOINTC("CopyJobStaticConstraintRules::getStapleOptionConstraints %d / %d", static_cast<int>(possibleResult), static_cast<int>(validResult));

    if(possibleResult == APIResult::OK && validResult == APIResult::OK)
    {
        possibleStapleOption = std::get<1>(resPossibleOptions);
        validStapleOption = std::get<1>(resValidOptions);
    }
    else
    {
        if(jobTicket->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::STAPLE))
        {
            constraints->add(std::make_unique<Lock>(jobTicket->getConstraintsMsgBetweenFinisherOption(dune::imaging::types::MediaProcessingTypes::STAPLE).c_str()));  
        }
        possibleStapleOption.push_back(dune::cdm::jobTicket_1::StapleOptions::none);
        validStapleOption.push_back(dune::cdm::jobTicket_1::StapleOptions::none);
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::jobTicket_1::StapleOptions>>(possibleStapleOption, &dune::cdm::jobTicket_1::StapleOptionsEnum::valueToString, constraintsmsg);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::jobTicket_1::StapleOptions>>(validStapleOption, constraintsmsg);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getPunchOptionConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    std::string constraintsmsg="";
    // Get punchOption for possible & valid values.
    auto resPossibleOptions = jobTicket->getPossiblePunchingOptions();
    APIResult possibleResult = std::get<0>(resPossibleOptions);
    auto resValidOptions = jobTicket->getValidPunchingOptions(constraintsmsg);
    APIResult validResult = std::get<0>(resValidOptions);
    
    auto possiblePunchOption = std::vector<dune::cdm::jobTicket_1::PunchOptions>();
    auto validPunchOption = std::vector<dune::cdm::jobTicket_1::PunchOptions>();

    auto constraints = std::make_shared<Constraints>();
    CHECKPOINTC("CopyJobStaticConstraintRules::getPunchOptionConstraints %d / %d", static_cast<int>(possibleResult), static_cast<int>(validResult));

    if(possibleResult == APIResult::OK && validResult == APIResult::OK)
    {
        possiblePunchOption = std::get<1>(resPossibleOptions);
        validPunchOption = std::get<1>(resValidOptions);
    }
    else
    {
        if(jobTicket->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::PUNCH))
        {
            constraints->add(std::make_unique<Lock>(jobTicket->getConstraintsMsgBetweenFinisherOption(dune::imaging::types::MediaProcessingTypes::PUNCH).c_str()));  
        }
        possiblePunchOption.push_back(dune::cdm::jobTicket_1::PunchOptions::none);
        validPunchOption.push_back(dune::cdm::jobTicket_1::PunchOptions::none);
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::jobTicket_1::PunchOptions>>(possiblePunchOption, &dune::cdm::jobTicket_1::PunchOptionsEnum::valueToString, constraintsmsg);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::jobTicket_1::PunchOptions>>(validPunchOption, constraintsmsg);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getFoldOptionConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    std::string constraintsmsg="";
    // Get punchOption for possible & valid values.
    auto resPossibleOptions = jobTicket->getPossibleFoldingOptions();
    APIResult possibleResult = std::get<0>(resPossibleOptions);
    auto resValidOptions = jobTicket->getValidFoldingOptions(constraintsmsg);
    APIResult validResult = std::get<0>(resValidOptions);
    
    auto possibleFoldOption = std::vector<dune::cdm::jobTicket_1::FoldOptions>();
    auto validFoldOption = std::vector<dune::cdm::jobTicket_1::FoldOptions>();

    auto constraints = std::make_shared<Constraints>();
    CHECKPOINTC("CopyJobStaticConstraintRules::getFoldOptionConstraints %d / %d", static_cast<int>(possibleResult), static_cast<int>(validResult));

    if(possibleResult == APIResult::OK && validResult == APIResult::OK)
    {
        possibleFoldOption = std::get<1>(resPossibleOptions);
        validFoldOption = std::get<1>(resValidOptions);
    }
    else
    {
        if(jobTicket->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::FOLD))
        {
            constraints->add(std::make_unique<Lock>(jobTicket->getConstraintsMsgBetweenFinisherOption(dune::imaging::types::MediaProcessingTypes::FOLD).c_str()));  
        }
        possibleFoldOption.push_back(dune::cdm::jobTicket_1::FoldOptions::none);
        validFoldOption.push_back(dune::cdm::jobTicket_1::FoldOptions::none);
    }

    if(CopyJobStaticConstraintRules::isStampEnabled(jobTicket))
    {
        constraints->add(std::make_unique<Lock>(string_id::cFeatureCurrentNotAvailable));
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::jobTicket_1::FoldOptions>>(possibleFoldOption, &dune::cdm::jobTicket_1::FoldOptionsEnum::valueToString, constraintsmsg);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::jobTicket_1::FoldOptions>>(validFoldOption, constraintsmsg);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getSheetsPerFoldSetForCFoldConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    auto resSheets = jobTicket->getPagesPerSetLimitForFinishingOption(dune::imaging::types::FoldingOptions::C_INWARD_TOP, dune::imaging::types::BookletMakingOptions::NONE); 

    int minSheets = std::get<0>(resSheets);
    int maxSheets = std::get<1>(resSheets);
    int stepSheets = 1;

    auto constraints = std::make_shared<Constraints>();

    // range - min, max, step - (on a number)
    auto rangeConstraint = std::make_unique<RangeInt>(minSheets, maxSheets, stepSheets, string_id::cThisOptionUnavailable);
    constraints->add(std::move(rangeConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getSheetsPerFoldSetForVFoldConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    auto resSheets = jobTicket->getPagesPerSetLimitForFinishingOption(dune::imaging::types::FoldingOptions::V_INWARD_TOP, dune::imaging::types::BookletMakingOptions::NONE); 

    int minSheets = std::get<0>(resSheets);
    int maxSheets = std::get<1>(resSheets);
    int stepSheets = 1;

    auto constraints = std::make_shared<Constraints>();

    // range - min, max, step - (on a number)
    auto rangeConstraint = std::make_unique<RangeInt>(minSheets, maxSheets, stepSheets, string_id::cThisOptionUnavailable);
    constraints->add(std::move(rangeConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getBookletMakerOptionConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    std::string constraintsmsg="";
    // Get BookletMakerOption for possible & valid values.
    auto resPossibleOptions = jobTicket->getPossibleBookletMakingOptions();
    APIResult possibleResult = std::get<0>(resPossibleOptions);
    auto resValidOptions = jobTicket->getValidBookletMakingOptions(constraintsmsg);
    APIResult validResult = std::get<0>(resValidOptions);
    
    auto possibleBookletMakerOption = std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>();
    auto validBookletMakerOption = std::vector<dune::cdm::jobTicket_1::BookletMakerOptions>();

    CHECKPOINTC("CopyJobStaticConstraintRules::getBookletMakerOptionConstraints %d / %d", static_cast<int>(possibleResult), static_cast<int>(validResult));

    auto constraints = std::make_shared<Constraints>();
    if(possibleResult == APIResult::OK && validResult == APIResult::OK)
    {
        possibleBookletMakerOption = std::get<1>(resPossibleOptions);
        validBookletMakerOption = std::get<1>(resValidOptions);
    }
    else
    {
        if(jobTicket->IsInstalledSpecificPageBasedFinisherDevice(dune::imaging::types::MediaProcessingTypes::BOOKLET_MAKING))
        {
            constraints->add(std::make_unique<Lock>(jobTicket->getConstraintsMsgBetweenFinisherOption(dune::imaging::types::MediaProcessingTypes::BOOKLET_MAKING).c_str()));  
        }
        possibleBookletMakerOption.push_back(dune::cdm::jobTicket_1::BookletMakerOptions::none);
        validBookletMakerOption.push_back(dune::cdm::jobTicket_1::BookletMakerOptions::none);
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::jobTicket_1::BookletMakerOptions>>(possibleBookletMakerOption, &dune::cdm::jobTicket_1::BookletMakerOptionsEnum::valueToString, constraintsmsg);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::jobTicket_1::BookletMakerOptions>>(validBookletMakerOption, constraintsmsg);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getSheetsPerFoldSetForFoldAndStitchConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    auto resSheets = jobTicket->getPagesPerSetLimitForFinishingOption(dune::imaging::types::FoldingOptions::NONE, dune::imaging::types::BookletMakingOptions::SADDLE_STITCH); 

    int minSheets = std::get<0>(resSheets);
    int maxSheets = std::get<1>(resSheets);
    int stepSheets = 1;

    auto constraints = std::make_shared<Constraints>();

    // range - min, max, step - (on a number)
    auto rangeConstraint = std::make_unique<RangeInt>(minSheets, maxSheets, stepSheets, string_id::cThisOptionUnavailable);
    constraints->add(std::move(rangeConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getSheetsPerFoldSetForDeviceSetsFoldAndStitchSheetsEnabledConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    auto constraints = std::make_shared<Constraints>();

    //Possible values on an Enum
    auto enumPossibleValues = { dune::cdm::glossary_1::FeatureEnabled::true_, dune::cdm::glossary_1::FeatureEnabled::false_ };
    auto enumPossibleValueConstraint =
        std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::FeatureEnabled>>(enumPossibleValues, &dune::cdm::glossary_1::FeatureEnabledEnum::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValues = std::vector<dune::cdm::glossary_1::FeatureEnabled>();
    enumValidValues.push_back(dune::cdm::glossary_1::FeatureEnabled::true_);
    enumValidValues.push_back(dune::cdm::glossary_1::FeatureEnabled::false_);

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::FeatureEnabled>>(enumValidValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getJobOffsetConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    auto constraints = std::make_shared<Constraints>();

    //Possible values on an Enum
    auto enumPossibleValues = { dune::cdm::glossary_1::FeatureEnabled::true_, dune::cdm::glossary_1::FeatureEnabled::false_ };
    auto enumPossibleValueConstraint =
        std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::FeatureEnabled>>(enumPossibleValues, &dune::cdm::glossary_1::FeatureEnabledEnum::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValues = std::vector<dune::cdm::glossary_1::FeatureEnabled>();
    enumValidValues.push_back(dune::cdm::glossary_1::FeatureEnabled::true_);
    enumValidValues.push_back(dune::cdm::glossary_1::FeatureEnabled::false_);

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::FeatureEnabled>>(enumValidValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getPlexBindingConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    // Get plex binding for valid values.
    auto tempPlexBinding = jobTicket->getConstraints()->getPlexBinding();
    auto possiblePlexBinding = std::vector<dune::cdm::glossary_1::DuplexBinding>();
    auto validPlexBinding = std::vector<dune::cdm::glossary_1::DuplexBinding>();
    for(auto iter = tempPlexBinding.begin(); iter != tempPlexBinding.end(); iter++)
    {
        possiblePlexBinding.push_back(mapToCdm(*iter));
        //if(!SomethingPreventsThisFromBeingValid(*iter)) // if something prevents a valid value for this, add the logic here
        validPlexBinding.push_back(mapToCdm(*iter));
    }
    
    auto constraints = std::make_shared<Constraints>();

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::DuplexBinding>>(possiblePlexBinding, &dune::cdm::glossary_1::DuplexBinding::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::DuplexBinding>>(validPlexBinding, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getCollateConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    // Get collate for valid values.
    auto tempCollate = jobTicket->getConstraints()->getCollate();
    auto possibleCollate = std::vector<CollateModes>();
    auto validCollate = std::vector<CollateModes>();
    for(auto iter = tempCollate.begin(); iter != tempCollate.end(); iter++)
    {
        possibleCollate.push_back(dune::job::cdm::mapToCdm(*iter));
        //if(!SomethingPreventsThisFromBeingValid(*iter)) // if something prevents a valid value for this, add the logic here
        validCollate.push_back(dune::job::cdm::mapToCdm(*iter));
    }
    auto constraints = std::make_shared<Constraints>();

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<CollateModes>>(possibleCollate, &CollateModes::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<CollateModes>>(validCollate, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getCopiesConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    int minCopies  = jobTicket->getConstraints()->getMinCopies();
    int maxCopies  = jobTicket->getConstraints()->getMaxCopies();
    int stepCopies = jobTicket->getConstraints()->getStepCopies();

    auto constraints = std::make_shared<Constraints>();

    // range - min, max, step - (on a number)
    auto rangeConstraint = std::make_unique<RangeInt>(minCopies, maxCopies, stepCopies, string_id::cThisOptionUnavailable);
    constraints->add(std::move(rangeConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getPrintQualityConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    auto tempPrintQuality = jobTicket->getConstraints()->getPrintQuality();
    auto possiblePrintQuality = std::vector<dune::cdm::glossary_1::PrintQuality>();
    auto validPrintQuality = std::vector<dune::cdm::glossary_1::PrintQuality>();
    for(auto iter = tempPrintQuality.begin(); iter != tempPrintQuality.end(); iter++)
    {
        possiblePrintQuality.push_back(mapToCdm(*iter));
        validPrintQuality.push_back(mapToCdm(*iter));
    }

    auto constraints = std::make_shared<Constraints>();

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::PrintQuality>>(possiblePrintQuality, &dune::cdm::glossary_1::PrintQuality::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::PrintQuality>>(validPrintQuality, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getMediaPrintSupportedSource(std::vector<dune::imaging::types::MediaSource> mediaPrintSupportedSource, std::vector<dune::cdm::glossary_1::MediaSourceId> vecPosMediaSources)
{
    CHECKPOINTC("CopyJobStaticConstraintRules::getMediaPrintSupportedSource - Enter");

    if(vecPosMediaSources.empty())
    {
        CHECKPOINTC("CopyJobStaticConstraintRules::getMediaPrintSupportedSource - vector of possible values ​​comes empty");
        for(auto it = mediaPrintSupportedSource.begin() ; it != mediaPrintSupportedSource.end() ; it++)
        {
            dune::cdm::glossary_1::MediaSourceId glossaryMediaSource = mapToCdm(*it);
            vecPosMediaSources.push_back(glossaryMediaSource);
        }
    }
    
    auto constraints = std::make_shared<Constraints>();
    //Possible values on an Enum
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::MediaSourceId>>(vecPosMediaSources, &dune::cdm::glossary_1::MediaSourceId::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValues = std::vector<dune::cdm::glossary_1::MediaSourceId>();
    for(auto it = mediaPrintSupportedSource.begin() ; it != mediaPrintSupportedSource.end() ; it++)
    {
        dune::cdm::glossary_1::MediaSourceId glossaryMediaSource = mapToCdm(*it);
        CHECKPOINTC("CopyJobStaticConstraintRules::getMediaPrintSupportedSource - enumValidValues mapToCdm: %d",static_cast<int>(glossaryMediaSource));
        enumValidValues.push_back(glossaryMediaSource);
    }
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaSourceId>>(enumValidValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));
    
    CHECKPOINTC("CopyJobStaticConstraintRules::getMediaPrintSupportedSource - Exit");
    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getOutputPrintMediaConstraints(
    std::shared_ptr<ICopyJobTicket> jobTicket, dune::imaging::types::MediaDestinationId defaultMediaConstraint)
{
    CHECKPOINTC("CopyJobStaticConstraintRules::getOutputPrintMediaConstraints - Enter");
    auto constraints = std::make_shared<Constraints>();
    auto defaultMediaConstraintAsCdm = mapToCdm(defaultMediaConstraint);
    
    if(jobTicket->IsInstalledPageBasedFinisherDevice()) // enterprise finisher
    {
        CHECKPOINTC("CopyJobStaticConstraintRules::getOutputPrintMediaConstraints  Finisher Installed");
        auto resPossibleOptions = jobTicket->getPossibleOutputBins();
        APIResult possibleResult = std::get<0>(resPossibleOptions);
        auto resValidOptions = jobTicket->getValidOutputBins();
        APIResult validResult = std::get<0>(resValidOptions);
        
        auto enumPossibleValues = std::vector<dune::cdm::glossary_1::MediaDestinationId>();
        auto enumValidValues = std::vector<dune::cdm::glossary_1::MediaDestinationId>();

        CHECKPOINTC("CopyJobStaticConstraintRules::getOutputPrintMediaConstraints %d / %d", static_cast<int>(possibleResult), static_cast<int>(validResult));

        if((possibleResult == APIResult::OK) && (validResult == APIResult::OK))
        {
            enumPossibleValues = std::get<1>(resPossibleOptions);
            enumValidValues = std::get<1>(resValidOptions);
        }
        else // Default auto cannot be configured from defaultMediaConstraint because only applies to cdm level and only for enterprise hpMfp currently
        {
            enumPossibleValues.push_back(dune::cdm::glossary_1::MediaDestinationId::auto_);
            enumValidValues.push_back(dune::cdm::glossary_1::MediaDestinationId::auto_);
        }

        auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::MediaDestinationId>>(enumPossibleValues, &dune::cdm::glossary_1::MediaDestinationId::valueToString, string_id::cThisOptionUnavailable);
        constraints->add(std::move(enumPossibleValueConstraint));

        auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaDestinationId>>(enumValidValues, string_id::cThisOptionUnavailable);
        constraints->add(std::move(enumValidValuesConstraint));    
    }
    else
    {
        std::tuple<APIResult, std::vector<dune::imaging::types::MediaDestinationId>> result = jobTicket->getOutputList();
        auto possibleValues = std::get<1>(result);
        std::vector<dune::imaging::types::MediaDestinationId> validValues = jobTicket->getConstraints()->getMediaDestinations();
        
        //Possible values on an Enum
        auto enumPossibleValues = std::vector<dune::cdm::glossary_1::MediaDestinationId>();
        for(auto value : validValues)
        {
            if(std::find(possibleValues.begin(),possibleValues.end(),value) != possibleValues.end())
            {
                dune::cdm::glossary_1::MediaDestinationId mediaDestinationType = mapToCdm(value);
                CHECKPOINTC("CopyJobStaticConstraintRules::getOutputPrintMediaConstraints - enumPossibleValues mapToCdm: %d",static_cast<int>(mediaDestinationType));
                enumPossibleValues.push_back(mediaDestinationType);
            }
        }

        // If no possible values, set a default at least
        if(enumPossibleValues.size() == 0)
        {
            enumPossibleValues.push_back(defaultMediaConstraintAsCdm);
        }

        // Add possibles on constraint list
        auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::MediaDestinationId>>(enumPossibleValues, &dune::cdm::glossary_1::MediaDestinationId::valueToString, string_id::cThisOptionUnavailable);
        constraints->add(std::move(enumPossibleValueConstraint));

        // Valid Values on an Enum
        auto enumValidValues = std::vector<dune::cdm::glossary_1::MediaDestinationId>();
        for(auto value : validValues)
        {
            dune::cdm::glossary_1::MediaDestinationId mediaDestinationType = mapToCdm(value);
            CHECKPOINTC("CopyJobStaticConstraintRules::getOutputPrintMediaConstraints - enumValidValues mapToCdm: %d",static_cast<int>(mediaDestinationType));
            enumValidValues.push_back(mediaDestinationType);
        }

        // If no valid values, set a default a least
        if(enumValidValues.size() == 0)
        {
            enumValidValues.push_back(defaultMediaConstraintAsCdm);
        }

        // Add valid values on constraint list
        auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaDestinationId>>(enumValidValues, string_id::cThisOptionUnavailable);
        constraints->add(std::move(enumValidValuesConstraint));
    }
    CHECKPOINTC("CopyJobStaticConstraintRules::getOutputPrintMediaConstraints - Exit");
    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getMediaSizeIdConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    dune::print::engine::cdm::MediaCdmHelper mediaCdmHelper;
    auto constraints = std::make_shared<Constraints>();
    std::vector<CopyJobMediaSupportedSize> vecMediaSizes = jobTicket->getConstraints()->getMediaSupportedSizes();
    std::vector<dune::cdm::glossary_1::MediaSize> vecPossibleMediaSizes = getPossibleMediaSizes(jobTicket);
    
    // Valid Values on an Enum
    auto enumValidValues = std::vector<dune::cdm::glossary_1::MediaSize>();

    if (vecMediaSizes.size() > 0)
    {
        // Get Media source from the Ticket
        auto mediaSourceFromTicket = jobTicket->getIntent()->getOutputMediaSource();
        // Get Plex from the Ticket
        auto plexFromTicket = jobTicket->getIntent()->getOutputPlexMode();
        
        // Get MediaSizeId from CopyJobMediaSupportedSize and push to ValidValues.
        for(auto it = vecMediaSizes.begin() ; it != vecMediaSizes.end() ; it++)
        {
            // Check if the media source of each element of 'vecMediaSizes' that
            // stores from csf file has the same media source value from the ticket.
            auto mediaSources = it->getSupportedMediaSource();
            mediaSources.insert( dune::imaging::types::MediaSource::AUTOSELECT );// Autoselect is always good
            auto findMediaSource = mediaSources.find(mediaSourceFromTicket);
            
            auto plexs = it->getDuplex();
            auto findPlex = plexs.find(plexFromTicket);
            // If element of 'vecMediaSizes' have same media source and plex that getting from jobticket
            // add current element to valid values.
            if((findMediaSource != mediaSources.end()) && (findPlex != plexs.end()))
            {
                dune::cdm::glossary_1::MediaSize glossaryMediaSize = mediaCdmHelper.convertDuneMediaIdSizeToCdm(it->getId(), it->getMediaOrientation());
                enumValidValues.push_back(glossaryMediaSize);
            }
        }
    }
    else
    {
        vecPossibleMediaSizes.push_back(mediaCdmHelper.convertDuneMediaIdSizeToCdm(dune::imaging::types::MediaSizeId::ANY)); // Any is always good

        std::vector<dune::imaging::types::MediaSizeId> vecMediaSizesId = jobTicket->getConstraints()->getMediaPrintSupportedSize();
        for(auto it = vecMediaSizesId.begin() ; it != vecMediaSizesId.end() ; it++)
        {
            dune::cdm::glossary_1::MediaSize glossaryMediaSize = mediaCdmHelper.convertDuneMediaIdSizeToCdm(*it);
            enumValidValues.push_back(glossaryMediaSize);
        }
    }

    //Possible values on an Enum
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::MediaSize>>(vecPossibleMediaSizes, &dune::cdm::glossary_1::MediaSize::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>>(enumValidValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getMediaIdTypeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    auto constraints = std::make_shared<Constraints>();

    std::vector<CopyJobMediaSupportedType> vecMediaTypes = jobTicket->getConstraints()->getMediaSupportedTypes();
    std::vector<dune::cdm::glossary_1::MediaType> vecPosMediaTypes = getPossibleMediaTypes(jobTicket);
    std::vector<dune::cdm::glossary_1::MediaType> enabledMediaTypes;
    CHECKPOINTB("CopyJobStaticConstraintRules::getMediaIdTypeConstraints - vecMediaTypes from csf file size: %d", vecMediaTypes.size());
    auto isMediaTypeVisibilityTogglingSupported = jobTicket->isMediaTypeVisibilityTogglingSupported();
    CHECKPOINTB("CopyJobStaticConstraintRules::getMediaIdTypeConstraints - isMediaTypeVisibilityTogglingSupported: %d", isMediaTypeVisibilityTogglingSupported);
    if(isMediaTypeVisibilityTogglingSupported)
    {
        enabledMediaTypes = std::get<1>(jobTicket->getEnabledMediaTypes());
    }
    
    // Valid Values on an Enum
    auto enumValidValues = std::vector<dune::cdm::glossary_1::MediaType>();

    if (vecMediaTypes.size() > 0)
    {
        // Get Media source from the Ticket
        auto mediaSourceFromTicket = jobTicket->getIntent()->getOutputMediaSource();
        // Get Plex from the Ticket
        auto plexFromTicket = jobTicket->getIntent()->getOutputPlexMode();
        // Get MediaTypeId from CopyJobMediaSupportedType and push to ValidValues.
        for(auto it = vecMediaTypes.begin() ; it != vecMediaTypes.end() ; it++)
        {
            if(isMediaTypeVisibilityTogglingSupported)
            {
                if (std::find(enabledMediaTypes.begin(), enabledMediaTypes.end(), mapToCdm(it->getId())) ==
                        enabledMediaTypes.end())
                {
                    CHECKPOINTC("CopyJobStaticConstraintRules::getMediaIdTypeConstraints - media type %d is not enabled", static_cast<int>(it->getId()));
                    continue;
                }
            }

            /*
            * Check if the media source of each element of 'vecMediaTypes' that
            * stores from csf file has the same media source value from the ticket.
            */
            auto mediaSources = it->getSupportedMediaSource();
            mediaSources.insert( dune::imaging::types::MediaSource::AUTOSELECT );// Autoselect is always good
            auto findMediaSource = mediaSources.find(mediaSourceFromTicket);

            /*
             * Check if the plex of each element of 'vecMediaTypes' that
             * stores from csf file has the same plex value from the ticket.
             */
            auto plexs = it->getDuplex();
            auto findPlex = plexs.find(plexFromTicket);

            /*
            * If element of 'vecMediaTypes' have same media source and plex that getting from jobticket
            * add current element to valid values.
            */
            if((findMediaSource != mediaSources.end()) && (findPlex != plexs.end()))
            {
                dune::cdm::glossary_1::MediaType glossaryMediaType = mapToCdm(it->getId());
                enumValidValues.push_back(glossaryMediaType);
            }
        }
    }
    else
    {
        dune::print::engine::cdm::MediaCdmHelper mediaCdmHelper;
        
        vecPosMediaTypes.push_back(mediaCdmHelper.convertDuneMediaIdTypeToCdm(dune::imaging::types::MediaIdType::ANY)); // Any is always good

        std::vector<dune::imaging::types::MediaIdType> vecMediaIdTypes = jobTicket->getConstraints()->getMediaPrintSupportedType();
        for(auto it = vecMediaIdTypes.begin() ; it != vecMediaIdTypes.end() ; it++)
        {
            dune::cdm::glossary_1::MediaType glossaryMediaType = mediaCdmHelper.convertDuneMediaIdTypeToCdm(*it);
            enumValidValues.push_back(glossaryMediaType);
        }
    }

    //Possible values on an Enum
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::MediaType>>(vecPosMediaTypes, &dune::cdm::glossary_1::MediaType::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaType>>(enumValidValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::vector<dune::cdm::glossary_1::MediaSize> CopyJobStaticConstraintRules::getPossibleMediaSizes(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    // Get Media sizes/types for possible values.
    std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>> resForSupMediaSizes;
    std::vector<dune::cdm::glossary_1::MediaSize> mediaSizes;
    APIResult result;

    // When the media source is auto, the size of the add media size/type is fetched. 
    // Because Auto is not physical input device. So we can't get media size/type of auto.
    if(jobTicket->getIntent()->getOutputMediaSource() == dune::imaging::types::MediaSource::AUTOSELECT)
    {
        CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getPossibleMediaSizes - MediaSource is Auto");
        // Get all media supporteds size.
        resForSupMediaSizes = jobTicket->getAllSupportedMediaSizes();
        result = std::get<0>(resForSupMediaSizes);
        if(result == APIResult::OK)
        {
            mediaSizes = std::get<1>(resForSupMediaSizes);
        }
    }
    else //Media Source is not auto.
    {
        CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getPossibleMediaSizes - MediaSource is %d", (int)jobTicket->getIntent()->getOutputMediaSource());
        // Get media supported sizes from set media source.
        resForSupMediaSizes = jobTicket->getSupportedMediaSizes(jobTicket->getIntent()->getOutputMediaSource());
        result = std::get<0>(resForSupMediaSizes);
        if(result == APIResult::OK)
        {
            mediaSizes = std::get<1>(resForSupMediaSizes);
        }
    }
    return mediaSizes;
}

std::vector<dune::cdm::glossary_1::MediaType> CopyJobStaticConstraintRules::getPossibleMediaTypes(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    APIResult result;

    // Get Media types for possible values.
    std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>> resForSupMediaTypes;
    std::vector<dune::cdm::glossary_1::MediaType> mediaTypes;

    // When the media source is auto, the size of the add media size/type is fetched. 
    // Because Auto is not physical input device. So we can't get media size/type of auto.
    if(jobTicket->getIntent()->getOutputMediaSource() == dune::imaging::types::MediaSource::AUTOSELECT)
    {
        CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getPossibleMediaTypes - MediaSource is Auto");
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
        CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobStaticConstraintRules::getPossibleMediaTypes - MediaSource is %d", (int)jobTicket->getIntent()->getOutputMediaSource());
        // Get media supported types from set media source.
        resForSupMediaTypes = jobTicket->getSupportedMediaTypes(jobTicket->getIntent()->getOutputMediaSource());
        result = std::get<0>(resForSupMediaTypes);
        if(result == APIResult::OK)
        {
            mediaTypes = std::get<1>(resForSupMediaTypes);
        }
    }
    return mediaTypes;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getFoldingStyleIdConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTD("CopyJobStaticConstraintRules::getFoldingStyleIdConstraints - Enter");
    auto foldingStyles = jobTicket->getConstraints()->getFoldingStyles();
    auto constraints = std::make_shared<Constraints>();

    // Empty vector of short. Folding styles that are finisher dependant are read as dynamic.
    std::vector<short> supportedValuesShort;
    if(foldingStyles.size() > 0)
    {
        for(short id : foldingStyles )
        {
            supportedValuesShort.push_back(id);
        }
    }
    else
    {
        // Force 0 / UNDEFINED / Do Not fold option, value in case of method is called without folding styles.
        supportedValuesShort.push_back( static_cast<short>(dune::imaging::types::FoldingStyle::UNDEFINED));
    }    

    auto validValuesConstraint = std::make_unique<ValidValuesShort>(supportedValuesShort, string_id::cUnavailable);
    constraints->add(std::move(validValuesConstraint));

    auto possibleValueConstraint = std::make_unique<PossibleValuesShort>(supportedValuesShort, string_id::cUnavailable);
    constraints->add(std::move(possibleValueConstraint));

    CHECKPOINTC("CopyJobStaticConstraintRules::getFoldingStyleIdConstraints %d static folding styles.", supportedValuesShort.size());
    CHECKPOINTD("CopyJobStaticConstraintRules::getFoldingStyleIdConstraints - Exit");
    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getMediaSourceConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    std::shared_ptr<Constraints> mediaSourceConstraints{nullptr};
    // Get Media Sources for Constraints.
    std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSourceId>> resForSupMediaSources;
    std::vector<dune::cdm::glossary_1::MediaSourceId> possibleMediaSources;
    std::vector<dune::cdm::glossary_1::MediaSourceId> validMediaSources;
    
    // Get Possible value for media source.
    resForSupMediaSources = jobTicket->getAllSupportedMediaSources();
    APIResult result = std::get<0>(resForSupMediaSources);
    if(result == APIResult::OK)
    {
        possibleMediaSources = std::get<1>(resForSupMediaSources);
        for (auto iter = possibleMediaSources.begin(); iter != possibleMediaSources.end(); iter++)
        {
            CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - PossibleMediaSource1 is %s", (*iter).toString().c_str());
        }
    }

    // Get Valid value for media source.
    std::map<dune::cdm::glossary_1::MediaSourceId, int> mapMediaSources; 
    for(auto it = possibleMediaSources.begin(); it != possibleMediaSources.end(); it++)
    {
        mapMediaSources.insert({*it, 0});
    }

    auto mediaSizeFromTicket = jobTicket->getIntent()->getOutputMediaSizeId();
    auto mediaOrientationFromTicket = jobTicket->getIntent()->getOutputMediaOrientation();
    // Check media sources that support the current media size in flat buffer.
    // If each media source support the currently set media size and type in the jobTicket, add 1 to the value.
    auto fbMediaSizes = jobTicket->getConstraints()->getMediaSupportedSizes();
    if(mediaSizeFromTicket == dune::imaging::types::MediaSizeId::ANY)
    {
        CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - mediaSizeFromTicket == dune::imaging::types::MediaSizeId::ANY");
        CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - mediaSizeFromTicket supports all media sources");
        for(auto it = mapMediaSources.begin(); it != mapMediaSources.end(); it++)
        {
            mapMediaSources[it->first]++; // update counter to set that media source is supported based on media size
            CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - Supported mediaSource map %s (%i)", it->first.toString().c_str(), mapMediaSources[it->first]);
        }
    }
    else if (mediaSizeFromTicket < dune::imaging::types::MediaSizeId::MAX)
    {
        CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - mediaSizeFromTicket == dune::imaging::types::MediaSizeId::UNDEFINED");
        for (auto it = fbMediaSizes.begin(); it != fbMediaSizes.end(); it++)
        {
            CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - Supported MediaSizeId is %s", mapToCdm(it->getId()).toString().c_str());
                    
            if (it->getId() == mediaSizeFromTicket && it->getMediaOrientation() == mediaOrientationFromTicket)
            {
                auto supportedMediaSources = it->getSupportedMediaSource();
                for (auto itSupportedMediaSource = supportedMediaSources.begin();
                        itSupportedMediaSource != supportedMediaSources.end(); itSupportedMediaSource++)
                {
                    auto mediaSource = mapToCdm(*itSupportedMediaSource).toString();
                    CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - Supported MediaSource is %s", mediaSource.c_str());
                    auto retMediaSource = mapMediaSources.find(mediaSource);
                    if (retMediaSource != mapMediaSources.end())
                    {
                        mapMediaSources[retMediaSource->first]++; // update counter to set that media source is supported based on media size
                        CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - Supported mediaSource map %s (%i)", retMediaSource->first.toString().c_str(), mapMediaSources[retMediaSource->first]);
                    }
                }
                break;
            }
        }
    }
    
    auto mediaTypeFromTicket = jobTicket->getIntent()->getOutputMediaIdType();
    // Check media sources that support the current media type in flat buffer.
    auto fbMediaTypes = jobTicket->getConstraints()->getMediaSupportedTypes();
    if (mediaTypeFromTicket == dune::imaging::types::MediaIdType::ANY)
    {
        CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - mediaTypeFromTicket == dune::imaging::types::MediaIdType::ANY");
        for (auto it = mapMediaSources.begin(); it != mapMediaSources.end(); it++)
        {
            mapMediaSources[it->first]++; // update counter to set that media source is supported based on media type
            CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - Supported mediaSource map %s (%i)", it->first.toString().c_str(), mapMediaSources[it->first]);
        }
    }
    else if (mediaTypeFromTicket <= dune::imaging::types::MediaIdType::MAX)
    {
        CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - mediaTypeFromTicket == dune::imaging::types::MediaIdType::UNDEFINED");
        for (auto it = fbMediaTypes.begin(); it != fbMediaTypes.end(); it++)
        {
            CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - Supported MediaTypeId is %s", mapToCdm(it->getId()).toString().c_str());
            
            if (it->getId() == mediaTypeFromTicket)
            {
                auto supportedMediaSources = it->getSupportedMediaSource();
                for (auto itSupportedMediaSource = supportedMediaSources.begin();
                        itSupportedMediaSource != supportedMediaSources.end(); itSupportedMediaSource++)
                {
                    auto mediaSource = mapToCdm(*itSupportedMediaSource).toString();
                    CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - Supported MediaSource is %s", mediaSource.c_str());
                    auto retMediaSource = mapMediaSources.find(mediaSource);
                    if (retMediaSource != mapMediaSources.end())
                    {
                        mapMediaSources[retMediaSource->first]++; // update counter to set that media source is supported based on media type
                        CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - Supported mediaSource map %s (%i)", retMediaSource->first.toString().c_str(), mapMediaSources[retMediaSource->first]);
                    }
                }
                break;
            }
        }
    }

    

    for (auto it = mapMediaSources.begin(); it != mapMediaSources.end(); it++)
    {
        if (it->second == MEDIA_SOURCE_MAP_COUNTER_ACCEPTED || it->first == dune::cdm::glossary_1::MediaSourceId::auto_)  // MediaSource that support the current media size and media type.
        {
            validMediaSources.push_back(it->first);
            CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - ValidMediaSource is %s", (validMediaSources.back()).toString().c_str());
        }
    }

    for (auto it = mapMediaSources.begin(); it != mapMediaSources.end(); it++)
    {
        if (it->second == MEDIA_SOURCE_MAP_COUNTER_ACCEPTED || it->first == dune::cdm::glossary_1::MediaSourceId::auto_)  // MediaSource that support the current media size and media type.
        {
            validMediaSources.push_back(it->first);
            CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - ValidMediaSource is %s", (validMediaSources.back()).toString().c_str());
        }
    }

    if (!possibleMediaSources.empty())
    {
        for (auto iter = possibleMediaSources.begin(); iter != possibleMediaSources.end(); iter++)
        {
            CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - PossibleMediaSource is %s", (*iter).toString().c_str());
        }
        for (auto iter = validMediaSources.begin(); iter != validMediaSources.end(); iter++)
        {
            CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - ValidMediaSource is %s", (*iter).toString().c_str());
        }
        //mediaSourceConstraints = getMediaSourceConstraints(possibleMediaSources, validMediaSources);
        auto constraints = std::make_shared<Constraints>();

        //Possible values on an Enum
        auto enumPossibleValues = possibleMediaSources;

        auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum< dune::cdm::glossary_1::MediaSourceId>>(enumPossibleValues, &dune::cdm::glossary_1::MediaSourceId::valueToString, string_id::cThisOptionUnavailable);
        constraints->add(std::move(enumPossibleValueConstraint));

        // Valid Values on an Enum
        // //TODO: allow only available trays
        auto enumValidValues = validMediaSources;

        auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum< dune::cdm::glossary_1::MediaSourceId>>(enumValidValues, string_id::cThisOptionUnavailable);
        constraints->add(std::move(enumValidValuesConstraint));
        mediaSourceConstraints = constraints;
    }
    else
    {
        // Get supported print Sources for constraint.
        std::vector<dune::imaging::types::MediaSource> mediaPrintSupportedSource = jobTicket->getConstraints()->getMediaPrintSupportedSource();
        for (auto iter = mediaPrintSupportedSource.begin(); iter != mediaPrintSupportedSource.end(); iter++)
        {
            auto SupportedToCdm = mapToCdm(*iter);
            CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - PossibleMediaSource is %s", (SupportedToCdm).toString().c_str());
        }
        for (auto iter = validMediaSources.begin(); iter != validMediaSources.end(); iter++)
        {
            CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - ValidMediaSource is %s", (*iter).toString().c_str());
        }
        // Get Constraint
        mediaSourceConstraints = getMediaPrintSupportedSource(mediaPrintSupportedSource, validMediaSources);
    }
    return mediaSourceConstraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getPlexModeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    auto tempPlexMode = jobTicket->getConstraints()->getPlexMode();
    auto possiblePlexMode = std::vector<dune::cdm::glossary_1::PlexMode>();
    auto validPlexMode = std::vector<dune::cdm::glossary_1::PlexMode>();
    if (tempPlexMode.empty())
    {
        return nullptr;
    }
    for(auto iter = tempPlexMode.begin(); iter != tempPlexMode.end(); iter++)
    {
        possiblePlexMode.push_back(mapToCdm(*iter));
        //if(!SomethingPreventsThisFromBeingValid(*iter)) // if something prevents a valid value for this, add the logic here
        validPlexMode.push_back(mapToCdm(*iter));
    }
    
    auto constraints = std::make_shared<Constraints>();

    // Possible Values on an Enum
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::PlexMode>>(possiblePlexMode, &dune::cdm::glossary_1::PlexMode::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::PlexMode>>(validPlexMode, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

/*static*/ std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getCustomMediaXFeedDimensionConstraints()
{
    auto constraints = std::make_shared<Constraints>();
    /** based on Jasper product */
    double minValue = 38600, maxValue = 125900;

    // range - min, max, step - (on a number)
    auto rangeConstraint = std::make_unique<RangeDouble>(minValue, maxValue, 1, string_id::cThisOptionUnavailable);
    constraints->add(std::move(rangeConstraint));

    return constraints;
}

/*static*/ std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getCustomMediaYFeedDimensionConstraints()
{
    auto constraints = std::make_shared<Constraints>();
    /** based on Jasper product */
    double minValue = 55000, maxValue = 180000;

    // range - min, max, step - (on a number)
    auto rangeConstraint = std::make_unique<RangeDouble>(minValue, maxValue, 1, string_id::cThisOptionUnavailable);
    constraints->add(std::move(rangeConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobStaticConstraintRules::getScaleToOutputConstraints(std::vector<dune::cdm::glossary_1::MediaSourceId> enumPossibleValues, std::vector<dune::cdm::glossary_1::MediaSourceId> enumValidValues)
{
    auto constraints = std::make_shared<Constraints>();
    // Valid Values on an Enum
    if(enumValidValues.size() == 0)
    {
        CHECKPOINTA("WARNING - CopyJobStaticConstraintRules::getScaleToOutputConstraints enumValidValues size is 0. Manually push data.");
        enumValidValues = enumPossibleValues;
    }
    //remove auto 
    enumPossibleValues.erase(std::remove_if(enumPossibleValues.begin(), enumPossibleValues.end(), [&](dune::cdm::glossary_1::MediaSourceId mediaSource) {
    return mediaSource == dune::cdm::glossary_1::MediaSourceId::auto_;
    }), enumPossibleValues.end());

        enumValidValues.erase(std::remove_if(enumValidValues.begin(), enumValidValues.end(), [&](dune::cdm::glossary_1::MediaSourceId mediaSource) {
    return mediaSource == dune::cdm::glossary_1::MediaSourceId::auto_;
    }), enumValidValues.end());

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<MediaSourceId>>(enumPossibleValues, &MediaSourceId::valueToString, string_id::cUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum< dune::cdm::glossary_1::MediaSourceId>>(enumValidValues, string_id::cUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

bool CopyJobStaticConstraintRules::isStampEnabled(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    std::vector<dune::imaging::types::StampType> allStampContents;
    std::vector<dune::imaging::types::StampPolicy> allStampPolicies;

    std::vector<dune::cdm::overlay_1::StampLocation> locations = {
        dune::cdm::overlay_1::StampLocation::topLeft,
        dune::cdm::overlay_1::StampLocation::topCenter,
        dune::cdm::overlay_1::StampLocation::topRight,
        dune::cdm::overlay_1::StampLocation::bottomLeft,
        dune::cdm::overlay_1::StampLocation::bottomCenter,
        dune::cdm::overlay_1::StampLocation::bottomRight
    };

    for (auto loc : locations) {
        std::vector<std::unique_ptr<dune::imaging::types::StampContentT>> contentsPtr;
        dune::imaging::types::StampPolicy policy = dune::imaging::types::StampPolicy::NONE;

        switch (loc) {
            case dune::cdm::overlay_1::StampLocation::topLeft:
                contentsPtr = jobTicket->getIntent()->getStampTopLeft().stampContents;
                policy = jobTicket->getIntent()->getStampTopLeft().stampPolicy;
                break;
            case dune::cdm::overlay_1::StampLocation::topCenter:
                contentsPtr = jobTicket->getIntent()->getStampTopCenter().stampContents;
                policy = jobTicket->getIntent()->getStampTopCenter().stampPolicy;
                break;
            case dune::cdm::overlay_1::StampLocation::topRight:
                contentsPtr = jobTicket->getIntent()->getStampTopRight().stampContents;
                policy = jobTicket->getIntent()->getStampTopRight().stampPolicy;
                break;
            case dune::cdm::overlay_1::StampLocation::bottomLeft:
                contentsPtr = jobTicket->getIntent()->getStampBottomLeft().stampContents;
                policy = jobTicket->getIntent()->getStampBottomLeft().stampPolicy;
                break;
            case dune::cdm::overlay_1::StampLocation::bottomCenter:
                contentsPtr = jobTicket->getIntent()->getStampBottomCenter().stampContents;
                policy = jobTicket->getIntent()->getStampBottomCenter().stampPolicy;
                break;
            case dune::cdm::overlay_1::StampLocation::bottomRight:
                contentsPtr = jobTicket->getIntent()->getStampBottomRight().stampContents;
                policy = jobTicket->getIntent()->getStampBottomRight().stampPolicy;
                break;
            case dune::cdm::overlay_1::StampLocation::_undefined_:
            default:
                break;
        }

        if (contentsPtr.size() > 0) {
            for (const auto& content : contentsPtr) {
                if (content) {
                    allStampContents.push_back(content->stampId);
                }
            }
        }
        allStampPolicies.push_back(policy);
    }

    for (const auto& stamp : allStampContents) {
        if (stamp != dune::imaging::types::StampType::NONE) {
            CHECKPOINTC("CopyJobStaticConstraintRules::isStampEnabled -> is not None, retrun true");
            return true;
        }
    }

    for (const auto& policy : allStampPolicies) {
        if (policy != dune::imaging::types::StampPolicy::NONE) {
            CHECKPOINTC("CopyJobStaticConstraintRules::isStampEnabled -> is policy Guided, retrun true");
            return true;
        }
    }
    CHECKPOINTC("CopyJobStaticConstraintRules::isStampEnabled -- retrun false");
    return false;
}