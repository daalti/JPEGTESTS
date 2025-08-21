/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobConstraintRules.cpp
 * @date   Tue, 08 August 2022
 * @brief  Base class for CopyJob Constraint rules
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobConstraintRules.h"
#include "StringIds.h"

#include "common_debug.h"
#include "CopyJobConstraintRules_TraceAutogen.h"
#include "typeMappers.h"
#include "MediaCdmHelper.h"
#include "MediaLib.h"
using namespace dune::copy::Jobs::Copy;
using namespace dune::job::cdm;
using namespace dune::framework::data::constraints;
using namespace dune::scan::Jobs::Scan;


std::vector<dune::cdm::glossary_1::MediaSize> CopyJobConstraintRules::getPossibleMediaSizes(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getPossibleMediaSizes - Enter");

    // Get Media sizes/types for possible values.
    std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaSize>> resForSupMediaSizes;
    std::vector<dune::cdm::glossary_1::MediaSize> mediaSizes;
    APIResult result;

    // When the media source is auto, the size of the add media size/type is fetched. 
    // Because Auto is not physical input device. So we can't get media size/type of auto.
    if(jobTicket->getIntent()->getOutputMediaSource() == dune::imaging::types::MediaSource::AUTOSELECT)
    {
        CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobConstraintRules::getPossibleMediaSizes - MediaSource is Auto");
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
        CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobConstraintRules::getPossibleMediaSizes - MediaSource is %d", (int)jobTicket->getIntent()->getOutputMediaSource());
        // Get media supported sizes from set media source.
        auto outputMediaSource = jobTicket->getIntent()->getOutputMediaSource();
        if (outputMediaSource == dune::imaging::types::MediaSource::MANUALFEED)
        {
            // Manual feed is logically another name for Tray1 in Enterprise.
            outputMediaSource = dune::imaging::types::MediaSource::TRAY1;
        }
        resForSupMediaSizes = jobTicket->getSupportedMediaSizes(outputMediaSource);
        result = std::get<0>(resForSupMediaSizes);
        if(result == APIResult::OK)
        {
            mediaSizes = std::get<1>(resForSupMediaSizes);
        }
    }
    return mediaSizes;
}

std::vector<dune::cdm::glossary_1::MediaType> CopyJobConstraintRules::getPossibleMediaTypes(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    APIResult result;

    // Get Media types for possible values.
    std::tuple<APIResult, std::vector<dune::cdm::glossary_1::MediaType>> resForSupMediaTypes;
    std::vector<dune::cdm::glossary_1::MediaType> mediaTypes;

    // When the media source is auto, the size of the add media size/type is fetched. 
    // Because Auto is not physical input device. So we can't get media size/type of auto.
    if(jobTicket->getIntent()->getOutputMediaSource() == dune::imaging::types::MediaSource::AUTOSELECT)
    {
        CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobConstraintRules::getPossibleMediaTypes - MediaSource is Auto");
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
        CHECKPOINTC("dune::copy::Jobs::Copy::CopyJobConstraintRules::getPossibleMediaTypes - MediaSource is %d", (int)jobTicket->getIntent()->getOutputMediaSource());
        // Get media supported types from set media source.
        auto outputMediaSource = jobTicket->getIntent()->getOutputMediaSource();
        if (outputMediaSource == dune::imaging::types::MediaSource::MANUALFEED)
        {
            // Manual feed is logically another name for Tray1 in Enterprise.
            outputMediaSource = dune::imaging::types::MediaSource::TRAY1;
        }
        resForSupMediaTypes = jobTicket->getSupportedMediaTypes(outputMediaSource);
        result = std::get<0>(resForSupMediaTypes);
        if(result == APIResult::OK)
        {
            mediaTypes = std::get<1>(resForSupMediaTypes);
        }
    }
    return mediaTypes;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getMediaSizeIdConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
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
        if (mediaSourceFromTicket == dune::imaging::types::MediaSource::MANUALFEED)
        {
            // Manual feed is logically another name for Tray1 in Enterprise.
            mediaSourceFromTicket = dune::imaging::types::MediaSource::TRAY1;
        }
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

    auto resVaidMediaSize = jobTicket->getPageBasedFinisherValidMediaSizes();
    auto result = std::get<0>(resVaidMediaSize);
    if(result == true)
    {
        bool exist = false;
        auto enumUpdateValidValues = std::vector<dune::cdm::glossary_1::MediaSize>();
        std::vector<dune::cdm::glossary_1::MediaSize> validMediaSizes = std::get<1>(resVaidMediaSize);
        for(auto it = validMediaSizes.begin() ; it != validMediaSizes.end() ; it++)
        {
            exist = std::any_of(enumValidValues.begin(), enumValidValues.end(),
                                            [&](dune::cdm::glossary_1::MediaSize size) { return size == *it; });
            if(exist == true)
            {
                enumUpdateValidValues.push_back(*it);
            }
        }
        auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>>(enumUpdateValidValues, string_id::cThisOptionUnavailable);
        constraints->add(std::move(enumValidValuesConstraint));
    }
    else
    {
        auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>>(enumValidValues, string_id::cThisOptionUnavailable);
        constraints->add(std::move(enumValidValuesConstraint));
    }

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getMediaIdTypeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    auto constraints = std::make_shared<Constraints>();

    std::vector<CopyJobMediaSupportedType> vecMediaTypes = jobTicket->getConstraints()->getMediaSupportedTypes();
    CHECKPOINTB("CopyJobDynamicConstraintRules::getMediaIdTypeConstraints - vecMediaTypes from csf file size: %d", vecMediaTypes.size());
    std::vector<dune::cdm::glossary_1::MediaType> vecPosMediaTypes = getPossibleMediaTypes(jobTicket);
    std::vector<dune::cdm::glossary_1::MediaType> enabledMediaTypes;
    auto isMediaTypeVisibilityTogglingSupported = jobTicket->isMediaTypeVisibilityTogglingSupported();
    if(isMediaTypeVisibilityTogglingSupported)
        enabledMediaTypes = std::get<1>(jobTicket->getEnabledMediaTypes());
    //Possible values on an Enum
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::MediaType>>(vecPosMediaTypes, &dune::cdm::glossary_1::MediaType::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValues = std::vector<dune::cdm::glossary_1::MediaType>();

    if (vecMediaTypes.size() > 0)
    {
        // Get Media source from the Ticket
        auto mediaSourceFromTicket = jobTicket->getIntent()->getOutputMediaSource();
        if (mediaSourceFromTicket == dune::imaging::types::MediaSource::MANUALFEED)
        {
            // Manual feed is logically another name for Tray1 in Enterprise.
            mediaSourceFromTicket = dune::imaging::types::MediaSource::TRAY1;
        }
        // Get Plex from the Ticket
        auto plexFromTicket = jobTicket->getIntent()->getOutputPlexMode();
        // Get color mode from the Ticket
        auto colorModeFromTicket = jobTicket->getIntent()->getColorMode();

        // Get MediaTypeId from CopyJobMediaSupportedType and push to ValidValues.
        for(auto it = vecMediaTypes.begin() ; it != vecMediaTypes.end() ; it++)
        {
            if(isMediaTypeVisibilityTogglingSupported)
            {
                if (std::find(enabledMediaTypes.begin(), enabledMediaTypes.end(), mapToCdm(it->getId())) ==
                        enabledMediaTypes.end())
                {
                    CHECKPOINTC("CopyJobDynamicConstraintRules::getMediaIdTypeConstraints - media type %d is not enabled", static_cast<int>(it->getId()));
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
            * Check if the plex of each element of 'vecMediaTypes' that
            * stores from csf file has the same plex value from the ticket.
            */
            auto colorMode = it->getColorMode();
            auto findColorMode = colorMode.find(colorModeFromTicket);

            /*
            * If element of 'vecMediaTypes' have same media source and plex that getting from jobticket
            * add current element to valid values.
            */
            if((findMediaSource != mediaSources.end()) && (findPlex != plexs.end()) && (findColorMode != colorMode.end()))
            {
                dune::cdm::glossary_1::MediaType glossaryMediaType = mapToCdm(it->getId());
                enumValidValues.push_back(glossaryMediaType);
            } else {
                CHECKPOINTC("CopyJobDynamicConstraintRules::getMediaIdTypeConstraints - media type %d is not enabled", static_cast<int>(it->getId()));
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

    auto resValidMediaType = jobTicket->getPageBasedFinisherValidMediaTypes();
    auto result = std::get<0>(resValidMediaType);
    if(result == true)
    {
        bool exist = false;
        std::vector<dune::cdm::glossary_1::MediaType> enumUpdateValidValues;
        std::vector<dune::cdm::glossary_1::MediaType> validMediaTypes = std::get<1>(resValidMediaType);
        for(auto it = validMediaTypes.begin() ; it != validMediaTypes.end() ; it++)
        {
            exist = std::any_of(enumValidValues.begin(), enumValidValues.end(),
                                            [&](dune::cdm::glossary_1::MediaType type) { return type == *it; });
            if(exist == true)
            {
                enumUpdateValidValues.push_back(*it);
            }
        }
        auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaType>>(enumUpdateValidValues, string_id::cThisOptionUnavailable);
        constraints->add(std::move(enumValidValuesConstraint));
    }
    else
    {
        auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaType>>(enumValidValues, string_id::cThisOptionUnavailable);
        constraints->add(std::move(enumValidValuesConstraint));
    }

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getMediaSourceConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
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

    auto inputMediaSizeFromTicket = jobTicket->getIntent()->getInputMediaSizeId();
    if (inputMediaSizeFromTicket <= dune::imaging::types::MediaSizeId::MIXED_A4_A3 &&
        inputMediaSizeFromTicket >= dune::imaging::types::MediaSizeId::MIXED_LETTER_LEGAL)
    {
        CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - mediaSizeFromTicket == dune::imaging::types::MediaSizeId::MIXED");
        CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - mediaSizeFromTicket supports only AUTOSELECT media sources");
        for(auto it = mapMediaSources.begin(); it != mapMediaSources.end(); it++)
        {
            mapMediaSources[it->first];
            CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - Supported mediaSource map %s (%i)", it->first.toString().c_str(), mapMediaSources[it->first]);
        }
    }
    else
    {
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
                mapMediaSources[it->first]++;
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
                            mapMediaSources[retMediaSource->first]++;
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
                mapMediaSources[it->first]++;
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
                            mapMediaSources[retMediaSource->first]++;
                            CHECKPOINTC("CopyJobConstraints::getMediaSourceConstraints() - Supported mediaSource map %s (%i)", retMediaSource->first.toString().c_str(), mapMediaSources[retMediaSource->first]);
                        }
                    }
                    break;
                }
            }
        }
    }

    for (auto it = mapMediaSources.begin(); it != mapMediaSources.end(); it++)
    {
        if (it->second == 2 || it->first == dune::cdm::glossary_1::MediaSourceId::auto_ || it->first == dune::cdm::glossary_1::MediaSourceId::manual) // MediaSource that support the current media size and media type.
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

std::shared_ptr<Constraints> CopyJobConstraintRules::getPlexModeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getPlexModeConstraints - Enter");

    auto tempPlexMode = jobTicket->getConstraints()->getPlexMode();
    auto possiblePlexMode = std::vector<dune::cdm::glossary_1::PlexMode>();
    std::vector<dune::cdm::glossary_1::PlexMode> validPlexMode = {
                                dune::cdm::glossary_1::PlexMode::simplex,
                                dune::cdm::glossary_1::PlexMode::duplex
    };

    for(auto iter = tempPlexMode.begin(); iter != tempPlexMode.end(); iter++)
    {
        possiblePlexMode.push_back(mapToCdm(*iter));
    }

    auto bookletFormatValue = jobTicket->getIntent()->getBookletFormat();
    if(bookletFormatValue == dune::imaging::types::BookletFormat::LeftEdge)
    {
        validPlexMode = { dune::cdm::glossary_1::PlexMode::duplex }; // not simplex-able
        CHECKPOINTC("CopyJobConstraintRules::getPlexModeConstraints - bookletFormatValue is LeftEdge");
    }
    else{
        // is the current media Type duplex-able?
        dune::imaging::types::MediaIdType currentMediaType = jobTicket->getIntent()->getOutputMediaIdType();
        dune::copy::Jobs::Copy::CopyJobMediaSupportedType* typeDude = jobTicket->getConstraints()->findCopyJobMediaSupportedType(currentMediaType);

        if(typeDude != NULL)
        {
            CHECKPOINTC("CopyJobConstraintRules::getPlexModeConstraints - Found the mediaType: %d; size: %d", static_cast<int>(currentMediaType), typeDude->getDuplex().size() );
            if(typeDude->getDuplex().size() < 2)
            {
                validPlexMode = { dune::cdm::glossary_1::PlexMode::simplex }; // not duplex-able
                CHECKPOINTC("CopyJobConstraintRules::getPlexModeConstraints - mediaType: %d is only simplex", static_cast<int>(currentMediaType));
            }
        }

        // is the current media Size duplex-able?
        dune::imaging::types::MediaSizeId currentMediaSize = jobTicket->getIntent()->getOutputMediaSizeId();
        if(currentMediaSize == dune::imaging::types::MediaSizeId::ANY)
        {
            // output media is equal to match original, then check the duplex support of input media
            CHECKPOINTB("CopyJobConstraintRules::getPlexModeConstraints - output media is Match Original, So checking input media");
            currentMediaSize = jobTicket->getIntent()->getInputMediaSizeId();
        }
        dune::copy::Jobs::Copy::CopyJobMediaSupportedSize* sizeDude = jobTicket->getConstraints()->findCopyJobMediaSupportedSize(currentMediaSize);

        if(sizeDude != NULL)
        {
            CHECKPOINTC("CopyJobConstraintRules::getPlexModeConstraints - Found the mediaSize %d ; size: %d ", static_cast<int>(currentMediaSize), sizeDude->getDuplex().size());
            if(sizeDude->getDuplex().size() < 2)
            {
                validPlexMode = { dune::cdm::glossary_1::PlexMode::simplex }; // not duplex-able
                CHECKPOINTC("CopyJobConstraintRules::getPlexModeConstraints - mediaSize: %d is only simplex", static_cast<int>(currentMediaSize));
            }
        }
    }
    auto constraints = std::make_shared<Constraints>();

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::PlexMode>>(possiblePlexMode, &dune::cdm::glossary_1::PlexMode::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::PlexMode>>(validPlexMode, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

bool CopyJobConstraintRules::hasColorPermission(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    bool hasPrintColorPermission = true;
    auto securityContext = jobTicket->getSecurityContext();
    if(securityContext != NULL)
    {
        dune::security::ac::PermissionSet permission;
        permission.insert(dune::security::ac::Permission::CP_COPY_COLOR);
        
        for(const auto & currentPermission:securityContext->getAllPermissions())
        {
            CHECKPOINTC("CopyJobConstraintRules::hasColorPermission - Security Permission %u" , uint32_t(currentPermission));
        }
        
        hasPrintColorPermission = securityContext->checkPermissions(permission);
    }
    CHECKPOINTC("CopyJobConstraintRules::hasColorPermission - colorPermission: %d", hasPrintColorPermission);
    return hasPrintColorPermission;
}

bool CopyJobConstraintRules::checkIfColorIsNotRestricted(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    // Check if color printing is restricted by the system configuration.
    
    bool restrictColor = jobTicket->isRestrictColorPrint();
    if(restrictColor)
    {
        CHECKPOINTA("CopyJobConstraintRules::checkIfColorIsRestricted - Color printing is restricted by system configuration.");
        return false;
    }
    else
    {

        bool hasPrintColorPermission = hasColorPermission(jobTicket);
        CHECKPOINTA("CopyJobConstraintRules::checkIfColorIsRestricted - Color printing is not restricted by system configuration, hasPrintColorPermission: %d", hasPrintColorPermission);
        //If user has color permission return false, implying color is not restricted
        return hasPrintColorPermission;
    }
    
}

// Does a permission check 
std::shared_ptr<Constraints> CopyJobConstraintRules::getPrintColorModeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getPrintColorModeConstraints - Enter");
    auto constraints = std::make_shared<Constraints>();
    //bool hasPrintColorPermission = hasColorPermission(jobTicket);
    bool colorNotRestricted = checkIfColorIsNotRestricted(jobTicket);
    dune::imaging::types::MediaIdType currentMediaType = jobTicket->getIntent()->getOutputMediaIdType();
    std::vector<dune::cdm::jobTicket_1::ColorModes> possibleColorModes = std::vector<dune::cdm::jobTicket_1::ColorModes>();
    std::vector<dune::cdm::jobTicket_1::ColorModes> validColorModes = std::vector<dune::cdm::jobTicket_1::ColorModes>();
    
    for(auto colorMode : jobTicket->getConstraints()->getColorMode())
    {
        possibleColorModes.push_back(mapToCdm(colorMode));

        // Determine if color printing is permitted.
        bool permissionCheckOk = (colorNotRestricted || ((colorMode != dune::imaging::types::ColorMode::COLOR) && (colorMode != dune::imaging::types::ColorMode::AUTODETECT)));

        // Determine if the current colorMode is supported by the current media type.
        dune::copy::Jobs::Copy::CopyJobMediaSupportedType* typeDude = jobTicket->getConstraints()->findCopyJobMediaSupportedType(currentMediaType);
        bool mediaTypeCheckOk = false;
        if(typeDude != NULL)
        {
            auto mediaSupportedColorModes = typeDude->getColorMode();
            CHECKPOINTC("CopyJobConstraintRules::getPrintColorModeConstraints - Found the mediaType: %d; size: %d", static_cast<int>(currentMediaType), mediaSupportedColorModes.size() );
            mediaTypeCheckOk = (mediaSupportedColorModes.find(colorMode) != mediaSupportedColorModes.end());
        }

        // Add the color mode to the valid list if it is permitted and supported.
        if(permissionCheckOk && mediaTypeCheckOk) {
            CHECKPOINTC("CopyJobConstraintRules::getPrintColorModeConstraints - ColorMode %d Added", (int)colorMode);
            validColorModes.push_back(mapToCdm(colorMode));
        } else {
            CHECKPOINTC("CopyJobConstraintRules::getPrintColorModeConstraints - ColorMode %d eliminated: permission %d mediaType %d",
                        (int)colorMode, (int)permissionCheckOk, (int)mediaTypeCheckOk);
        }
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::jobTicket_1::ColorModes>>(possibleColorModes, &dune::cdm::jobTicket_1::ColorModes::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValueConstraint = std::make_unique<ValidValuesEnum<dune::cdm::jobTicket_1::ColorModes>>(validColorModes, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValueConstraint));

    CHECKPOINTC("CopyJobConstraintRules::getPrintColorModeConstraints - Exit");
    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getMediaPrintSupportedSource(std::vector<dune::imaging::types::MediaSource> mediaPrintSupportedSource, std::vector<dune::cdm::glossary_1::MediaSourceId> vecPosMediaSources)
{
    CHECKPOINTC("CopyJobConstraintRules::getMediaPrintSupportedSource - Enter");

    if(vecPosMediaSources.empty())
    {
        CHECKPOINTC("CopyJobConstraintRules::getMediaPrintSupportedSource - vector of possible values ​​comes empty");
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
        CHECKPOINTC("CopyJobConstraintRules::getMediaPrintSupportedSource - enumValidValues mapToCdm: %d",static_cast<int>(glossaryMediaSource));
        enumValidValues.push_back(glossaryMediaSource);
    }
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaSourceId>>(enumValidValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));
    
    CHECKPOINTC("CopyJobConstraintRules::getMediaPrintSupportedSource - Exit");
    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getMediaPrintSupportedSize(std::vector<dune::imaging::types::MediaSizeId> mediaPrintSupportedSize, std::vector<dune::cdm::glossary_1::MediaSize> vecPosMediaSizes)
{
    CHECKPOINTC("CopyJobConstraintRules::getMediaPrintSupportedSize - Enter");

    if(vecPosMediaSizes.empty())
    {
        CHECKPOINTC("CopyJobConstraintRules::getMediaPrintSupportedSize - vector of possible values ​​comes empty");
        for(auto it = mediaPrintSupportedSize.begin() ; it != mediaPrintSupportedSize.end() ; it++)
        {
            dune::cdm::glossary_1::MediaSize glossaryMediaSize = mapToCdm(*it);
            vecPosMediaSizes.push_back(glossaryMediaSize);
        }
    }

    // Always add any value
    vecPosMediaSizes.push_back(dune::cdm::glossary_1::MediaSize::any);
    
    auto constraints = std::make_shared<Constraints>();
    //Possible values on an Enum
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::MediaSize>>(vecPosMediaSizes, &dune::cdm::glossary_1::MediaSize::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValues = std::vector<dune::cdm::glossary_1::MediaSize>();
    for(auto it = mediaPrintSupportedSize.begin() ; it != mediaPrintSupportedSize.end() ; it++)
    {
        dune::cdm::glossary_1::MediaSize glossaryMediaSize = mapToCdm(*it);
        CHECKPOINTC("CopyJobConstraintRules::getMediaPrintSupportedSize - enumValidValues mapToCdm: %d",static_cast<int>(glossaryMediaSize));
        enumValidValues.push_back(glossaryMediaSize);
    }
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaSize>>(enumValidValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));
    
    CHECKPOINTC("CopyJobConstraintRules::getMediaPrintSupportedSize - Exit");
    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getMediaPrintSupportedType(std::vector<dune::imaging::types::MediaIdType> mediaPrintSupportedType, std::vector<dune::cdm::glossary_1::MediaType> vecPosMediaTypes)
{
    CHECKPOINTC("CopyJobConstraintRules::getMediaPrintSupportedType - Enter");

    if(vecPosMediaTypes.empty())
    {
        CHECKPOINTC("CopyJobConstraintRules::getMediaPrintSupportedType - vector of possible values ​​comes empty");
        for(auto it = mediaPrintSupportedType.begin() ; it != mediaPrintSupportedType.end() ; it++)
        {
            dune::cdm::glossary_1::MediaType glossaryMediaType = mapToCdm(*it);
            vecPosMediaTypes.push_back(glossaryMediaType);
        }
    }
    
    // Always add any value
    vecPosMediaTypes.push_back(dune::cdm::glossary_1::MediaType::any);
    
    auto constraints = std::make_shared<Constraints>();
    //Possible values on an Enum
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::MediaType>>(vecPosMediaTypes, &dune::cdm::glossary_1::MediaType::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValues = std::vector<dune::cdm::glossary_1::MediaType>();
    for(auto it = mediaPrintSupportedType.begin() ; it != mediaPrintSupportedType.end() ; it++)
    {
        dune::cdm::glossary_1::MediaType glossaryMediaType = mapToCdm(*it);
        CHECKPOINTC("CopyJobConstraintRules::getMediaPrintSupportedType - enumValidValues mapToCdm: %d",static_cast<int>(glossaryMediaType));
        enumValidValues.push_back(glossaryMediaType);
    }
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaType>>(enumValidValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));
    
    CHECKPOINTC("CopyJobConstraintRules::getMediaPrintSupportedType - Exit");
    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getOutputPrintMediaConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getOutputPrintMediaConstraints - Enter");
    std::tuple<APIResult, std::vector<dune::imaging::types::MediaDestinationId>> result = jobTicket->getOutputList();
    auto possibleValues = std::get<1>(result);
    std::vector<dune::imaging::types::MediaDestinationId>                        validValues    = jobTicket->getConstraints()->getMediaDestinations();

    auto constraints = std::make_shared<Constraints>();

    //Possible values on an Enum
    auto enumPossibleValues = std::vector<dune::cdm::glossary_1::MediaDestinationId>();
    for(auto value : possibleValues)
    {
        dune::cdm::glossary_1::MediaDestinationId mediaDestinationType = mapToCdm(value);
        CHECKPOINTC("CopyJobConstraintRules::getOutputPrintMediaConstraints - enumPossibleValues mapToCdm: %d",static_cast<int>(mediaDestinationType));
        enumPossibleValues.push_back(mediaDestinationType);
    }

    // If no possible values, set a default at least
    if(enumPossibleValues.size() == 0)
    {
        enumPossibleValues.push_back(dune::cdm::glossary_1::MediaDestinationId::default_);
    }

    // Add possibles on constraint list
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::glossary_1::MediaDestinationId>>(enumPossibleValues, &dune::cdm::glossary_1::MediaDestinationId::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    // Valid Values on an Enum
    auto enumValidValues = std::vector<dune::cdm::glossary_1::MediaDestinationId>();
    for(auto value : validValues)
    {
        dune::cdm::glossary_1::MediaDestinationId mediaDestinationType = mapToCdm(value);
        CHECKPOINTC("CopyJobConstraintRules::getOutputPrintMediaConstraints - enumValidValues mapToCdm: %d",static_cast<int>(mediaDestinationType));
        enumValidValues.push_back(mediaDestinationType);
    }

    // If no valid values, set a default a least
    if(enumValidValues.size() == 0)
    {
        enumValidValues.push_back(dune::cdm::glossary_1::MediaDestinationId::default_);
    }

    // Add valid values on constraint list
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::MediaDestinationId>>(enumValidValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    CHECKPOINTC("CopyJobConstraintRules::getOutputPrintMediaConstraints - Exit");
    return constraints;
}

// for now we place the pagesPerSheet constraints in here;
// At some point these should probably move to the scanJobConstraintsRules and implement them with the jobTicket pattern.
// But before we do that we'll need to discuss the re-factor with Om & Krzysztof 
std::shared_ptr<Constraints> CopyJobConstraintRules::getPagesPerSheetConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getPagesPerSheetConstraints - Enter");
    auto constraints = std::make_shared<Constraints>();
    auto prePrintConfiguration = jobTicket->getPrePrintConfiguration();
    std::vector<dune::cdm::jobTicket_1::PagesPerSheet> possiblePagesPerSheet = std::vector<dune::cdm::jobTicket_1::PagesPerSheet>();
    std::vector<dune::cdm::jobTicket_1::PagesPerSheet> validPagesPerSheet = std::vector<dune::cdm::jobTicket_1::PagesPerSheet>();
    
    auto bookletFormatValue = jobTicket->getIntent()->getBookletFormat();

    if(bookletFormatValue == dune::imaging::types::BookletFormat::LeftEdge)
    {
        CHECKPOINTC("JobConstraintsStandard::checkIncompatibleTicketConfigurations - LOCK(booklet format) ");
        constraints->add(std::make_unique<Lock>(string_id::cFeatureCurrentNotAvailable));
    }

    if(jobTicket->getIntent()->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD)
    {
        // Product Specific config is needed
        // constraints->add(std::make_unique<Lock>(string_id::cPagesPerSheetOption));
        constraints->add(std::make_unique<Lock>(string_id::cFeatureCurrentNotAvailable));
    }
    for (uint32_t i = 0; i < jobTicket->getConstraints()->getPagesPerSheet().size(); i++)
    {
        possiblePagesPerSheet.push_back(mapToCdm(jobTicket->getConstraints()->getPagesPerSheet()[i]));
        if(((jobTicket->getIntent()->getScaleSelection() == dune::scan::types::ScanScaleSelectionEnum::NONE || 
        (prePrintConfiguration == Product::ENTERPRISE && jobTicket->getIntent()->getScaleSelection() == dune::scan::types::ScanScaleSelectionEnum::FITTOPAGE )) && 
        (jobTicket->getIntent()->getInputMediaSizeId() > dune::imaging::types::MediaSizeId::MIXED_A4_A3 ||
        jobTicket->getIntent()->getInputMediaSizeId() < dune::imaging::types::MediaSizeId::MIXED_LETTER_LEGAL)) ||
        jobTicket->getConstraints()->getPagesPerSheet()[i] == dune::imaging::types::CopyOutputNumberUpCount::OneUp)
        {
            validPagesPerSheet.push_back(mapToCdm(jobTicket->getConstraints()->getPagesPerSheet()[i]));
        }
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::jobTicket_1::PagesPerSheet>>(possiblePagesPerSheet, &dune::cdm::jobTicket_1::PagesPerSheet::valueToString, string_id::cFeatureCurrentNotAvailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValueConstraint = std::make_unique<ValidValuesEnum<dune::cdm::jobTicket_1::PagesPerSheet>>(validPagesPerSheet, string_id::cFeatureCurrentNotAvailable);
    constraints->add(std::move(enumValidValueConstraint));

    return constraints;    
};

std::shared_ptr<Constraints> CopyJobConstraintRules::getInputMediaSizeIdConstraints(std::shared_ptr<ICopyJobTicket> jobTicket, std::shared_ptr<dune::framework::data::constraints::Constraints> mediaSizeIdConstraints)
{
    CHECKPOINTC("CopyJobConstraintRules::getInputMediaSizeIdConstraints - Enter");
    dune::print::engine::cdm::MediaCdmHelper mediaCdmHelper;
    auto pagesPerSheetValue = jobTicket->getIntent()->getPagesPerSheet();
    auto mediaSourceValue = jobTicket->getIntent()->getOutputMediaSource();
    auto outputScaleValue = jobTicket->getIntent()->getScaleSelection();
    auto scanSourceValue = jobTicket->getIntent()->getScanSource();
    auto bookletFormatValue = jobTicket->getIntent()->getBookletFormat();
    auto constraints = std::make_shared<Constraints>();
    std::vector<MediaSize> dynamicValidValues;
    std::vector<MediaSize> finalValidValues;
    std::vector<MediaSize> possibleValues;
    if(mediaSizeIdConstraints)
    {
        for(auto constraint : mediaSizeIdConstraints->getConstraints())
        {
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM)
            {
                dynamicValidValues = (static_cast< dune::framework::data::constraints::ValidValuesEnum<MediaSize>*>(constraint))->getValidValues();
            }
            if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::POSSIBLE_VALUE_ENUM)
            {
                possibleValues = (static_cast< dune::framework::data::constraints::PossibleValuesEnum<MediaSize>*>(constraint))->getPossibleValues();
            }
        }
    }

    bool bookMode = (jobTicket->getIntent()->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::BOOKMODE);
    bool idCardMode = (jobTicket->getIntent()->getScanCaptureMode() == dune::scan::types::ScanCaptureModeType::IDCARD);

    for (const auto& mediaSize : dynamicValidValues)
    {
        auto mSize = mediaCdmHelper.convertCdmMediaIdSizeToDune(mediaSize);
        if(bookMode || idCardMode)
        {
            continue;
        }
        else if(mSize == dune::imaging::types::MediaSizeId::MIXED_LETTER_LEGAL ||
            mSize == dune::imaging::types::MediaSizeId::MIXED_LETTER_LEDGER ||
            mSize == dune::imaging::types::MediaSizeId::MIXED_A4_A3)
        {
            if(pagesPerSheetValue != dune::imaging::types::CopyOutputNumberUpCount::OneUp ||
                mediaSourceValue != dune::imaging::types::MediaSource::AUTOSELECT ||
                (outputScaleValue != dune::scan::types::ScanScaleSelectionEnum::NONE &&
                outputScaleValue != dune::scan::types::ScanScaleSelectionEnum::FITTOPAGE) ||
                bookletFormatValue == dune::imaging::types::BookletFormat::LeftEdge)
            {
                continue;  
            }     
        }
        else if(mSize == dune::imaging::types::MediaSizeId::PHOTO4X6 ||
                mSize == dune::imaging::types::MediaSizeId::PHOTO5X7 ||
                mSize == dune::imaging::types::MediaSizeId::PHOTO5X8 ||
                mSize == dune::imaging::types::MediaSizeId::A5 ||
                mSize == dune::imaging::types::MediaSizeId::A6 ||
                mSize == dune::imaging::types::MediaSizeId::B6 ||
                mSize == dune::imaging::types::MediaSizeId::PHOTO_10X15IN ||
                mSize == dune::imaging::types::MediaSizeId::MEDIA100X150)
        {
            if(bookletFormatValue == dune::imaging::types::BookletFormat::LeftEdge)
            {
                continue;
            }
        }
        finalValidValues.push_back(mediaSize);
    }

    if(bookMode || idCardMode)
    {
        finalValidValues.clear();
        finalValidValues.push_back(MediaSize::iso_a4_210x297mm);
        finalValidValues.push_back(MediaSize::na_letter_8_dot_5x11in);
    }
    
    if(dynamicValidValues.size() == 0)
    {
        CHECKPOINTA("WARNING - CopyJobConstraintRules::getInputMediaSizeIdConstraints enumValidValues size is 0. Manually add a generic value.");
        finalValidValues.push_back(MediaSize::any);  
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<MediaSize>>(possibleValues, &MediaSize::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<MediaSize>>(finalValidValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));
    
    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getScaleSelectionConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getScaleSelectionConstraints - Enter");
    auto constraints = std::make_shared<Constraints>();
    auto prePrintConfiguration = jobTicket->getPrePrintConfiguration();
    std::vector<dune::cdm::jobTicket_1::scaling::ScaleSelection> possibleScaleSelection = std::vector<dune::cdm::jobTicket_1::scaling::ScaleSelection>();
    std::vector<dune::cdm::jobTicket_1::scaling::ScaleSelection> validScaleSelection = std::vector<dune::cdm::jobTicket_1::scaling::ScaleSelection>();

    // In future we have to make this kind of checks Configurable
    if(jobTicket->getIntent()->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp && 
        prePrintConfiguration == Product::HOME_PRO)
    {
        CHECKPOINTC("CopyJobConstraintRules::getScaleSelectionConstraints - LOCK(pagesPerSheet) ");
        constraints->add(std::make_unique<Lock>(string_id::cFeatureCurrentNotAvailable));
    }

    for (uint32_t i = 0; i < jobTicket->getConstraints()->getScaleSelection().size(); i++)
    {
        possibleScaleSelection.push_back(mapToCdm(jobTicket->getConstraints()->getScaleSelection()[i]));
        if(mapToCdm(jobTicket->getConstraints()->getScaleSelection()[i]) == dune::cdm::jobTicket_1::scaling::ScaleSelection::custom ||
            mapToCdm(jobTicket->getConstraints()->getScaleSelection()[i]) == dune::cdm::jobTicket_1::scaling::ScaleSelection::fullPage ||
            mapToCdm(jobTicket->getConstraints()->getScaleSelection()[i]) == dune::cdm::jobTicket_1::scaling::ScaleSelection::legalToLetter ||
            mapToCdm(jobTicket->getConstraints()->getScaleSelection()[i]) == dune::cdm::jobTicket_1::scaling::ScaleSelection::a4ToLetter ||
            mapToCdm(jobTicket->getConstraints()->getScaleSelection()[i]) == dune::cdm::jobTicket_1::scaling::ScaleSelection::letterToA4)
        {
            if(jobTicket->getIntent()->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp ||
            jobTicket->getIntent()->getBookletFormat() == dune::imaging::types::BookletFormat::LeftEdge ||
            jobTicket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::MIXED_LETTER_LEDGER ||
            jobTicket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::MIXED_A4_A3 ||
            jobTicket->getIntent()->getInputMediaSizeId() == dune::imaging::types::MediaSizeId::MIXED_LETTER_LEGAL)
            {
                continue;
            }
            validScaleSelection.push_back(mapToCdm(jobTicket->getConstraints()->getScaleSelection()[i]));  
        }
        else{
        validScaleSelection.push_back(mapToCdm(jobTicket->getConstraints()->getScaleSelection()[i]));
        }
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>>(possibleScaleSelection, &dune::cdm::jobTicket_1::scaling::ScaleSelection::valueToString, string_id::cFeatureCurrentNotAvailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValueConstraint = std::make_unique<ValidValuesEnum<dune::cdm::jobTicket_1::scaling::ScaleSelection>>(validScaleSelection, string_id::cFeatureCurrentNotAvailable);
    constraints->add(std::move(enumValidValueConstraint));

    return constraints;
};

std::shared_ptr<Constraints> CopyJobConstraintRules::getCustomMediaXFeedDimension(dune::print::engine::constraints::IMediaConstraints* mediaConstraints)
{
    auto mediaWidthConstraintsTuple = mediaConstraints->getMediaWidthConstraintsForMediaSource();
    auto constraints = std::get<1>(mediaWidthConstraintsTuple);
    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getCustomMediaYFeedDimension(dune::print::engine::constraints::IMediaConstraints* mediaConstraints)
{
    auto mediaLengthConstraintsTuple = mediaConstraints->getMediaLengthConstraintsForMediaSource();
    auto constraints = std::get<1>(mediaLengthConstraintsTuple);
    return constraints;
}

std::vector<dune::cdm::overlay_1::StampType> CopyJobConstraintRules::getStampContents(dune::cdm::overlay_1::StampLocation stampLocation, std::shared_ptr<ICopyJobTicket> jobTicket)
{
    std::vector<dune::cdm::overlay_1::StampType> stampContents;

    // Map StampLocation to the corresponding getter function
    const std::map<dune::cdm::overlay_1::StampLocation, std::function<std::vector<std::unique_ptr<dune::imaging::types::StampContentT>>()>> locationMap = {
        {dune::cdm::overlay_1::StampLocation::topLeft, [&]() { return jobTicket->getIntent()->getStampTopLeft().stampContents; }},
        {dune::cdm::overlay_1::StampLocation::topCenter, [&]() { return jobTicket->getIntent()->getStampTopCenter().stampContents; }},
        {dune::cdm::overlay_1::StampLocation::topRight, [&]() { return jobTicket->getIntent()->getStampTopRight().stampContents; }},
        {dune::cdm::overlay_1::StampLocation::bottomLeft, [&]() { return jobTicket->getIntent()->getStampBottomLeft().stampContents; }},
        {dune::cdm::overlay_1::StampLocation::bottomCenter, [&]() { return jobTicket->getIntent()->getStampBottomCenter().stampContents; }},
        {dune::cdm::overlay_1::StampLocation::bottomRight, [&]() { return jobTicket->getIntent()->getStampBottomRight().stampContents; }},
    };

    auto it = locationMap.find(stampLocation);
    if (it != locationMap.end())
    {
        auto contents = it->second(); // Copy the contents to avoid returning a reference to a temporary
        for (const auto& content : contents)
        {
            if (content) // Ensure the pointer is valid
            {
                stampContents.push_back(mapToCdm(content->stampId));
            }
        }
    }
    else
    {
        CHECKPOINTB("CopyJobConstraintRules::getStampContents Invalid stampLocation");
    }

    return stampContents;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getStampLocationConstraints(dune::cdm::overlay_1::StampLocation stampLocation, std::shared_ptr<ICopyJobTicket> jobTicket)
{
    auto constraints = std::make_shared<Constraints>();

    std::vector<dune::cdm::overlay_1::StampLocation> validValues;
    auto staticConstraints = jobTicket->getConstraints()->getStampLocation();
    auto possibleValues = std::vector<dune::cdm::overlay_1::StampLocation>();

    for(auto & location : staticConstraints)
    {
        possibleValues.push_back(mapToCdm(location));
    }
    
    for(dune::cdm::overlay_1::StampLocation location : possibleValues)
    {
        if(location == stampLocation)
        {
            validValues.push_back(location);
        }
        else
        {
            continue;
        }
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::overlay_1::StampLocation>>(possibleValues, &dune::cdm::overlay_1::StampLocation::valueToString, string_id::cUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::overlay_1::StampLocation>>(validValues, string_id::cUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getStampPolicyConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    auto constraints = std::make_shared<Constraints>();

    auto staticConstraints = jobTicket->getConstraints()->getStampPolicy();
    auto possibleValues = std::vector<dune::cdm::overlay_1::StampPolicy>();

    for(auto & policy : staticConstraints)
    {
        possibleValues.push_back(mapToCdm(policy));
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::overlay_1::StampPolicy>>(possibleValues, &dune::cdm::overlay_1::StampPolicy::valueToString, string_id::cUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::overlay_1::StampPolicy>>(possibleValues, string_id::cUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getStampTypeConstraints(dune::cdm::overlay_1::StampLocation stampLocation, std::shared_ptr<ICopyJobTicket> jobTicket, dune::imaging::types::StampPolicy stampPolicy)
{
    auto constraints = std::make_shared<Constraints>();
    std::vector<dune::cdm::overlay_1::StampType> newPossibleStampType = {dune::cdm::overlay_1::StampType::none};
    auto staticConstraints = jobTicket->getConstraints()->getStampType();
    auto possibleValues = std::vector<dune::cdm::overlay_1::StampType>();

    for(auto & stampType : staticConstraints)
    {
        possibleValues.push_back(mapToCdm(stampType));
    }

    if (stampPolicy == dune::imaging::types::StampPolicy::NONE)
    {
        std::vector<dune::cdm::overlay_1::StampType> stampContents = getStampContents(stampLocation, jobTicket);

        // Add all items from stampContents to newPossibleStampType, excluding "none"
        for (const auto& stampType : stampContents) {
            if (stampType != dune::cdm::overlay_1::StampType::none) {
                newPossibleStampType.push_back(stampType);
            }
        }

        // Add items from possibleValues that are not in stampContents
        for (const auto& stampType : possibleValues) {
            if (stampType != dune::cdm::overlay_1::StampType::none  &&
                std::find(stampContents.begin(), stampContents.end(), stampType) == stampContents.end()) {
                newPossibleStampType.push_back(stampType);
            }
        }
    }
    else if (stampPolicy == dune::imaging::types::StampPolicy::GUIDED)
    {
        // ----------------------------
        // DUNE-66884
        // --------------------------------------------------------------------------------------------------------------------------
        // TBD: In the future, validStampType will be specified differently depending on scanStamps or policy (enforced/guided). 
        //      For now, we assign the same vector as possibleValues to ValidValuesEnum.
        // --------------------------------------------------------------------------------------------------------------------------
        std::vector<dune::cdm::overlay_1::StampType> stampContents = getStampContents(stampLocation, jobTicket);

        for (const auto& stampType : stampContents) {
            if (stampType != dune::cdm::overlay_1::StampType::none) {
                newPossibleStampType.push_back(stampType);
            }
        }

        for (const auto& stampType : possibleValues) {
            if (stampType != dune::cdm::overlay_1::StampType::none  &&
                std::find(stampContents.begin(), stampContents.end(), stampType) == stampContents.end()) {
                newPossibleStampType.push_back(stampType);
            }
        }
    }
    
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::overlay_1::StampType>>(newPossibleStampType, &dune::cdm::overlay_1::StampType::valueToString, string_id::cUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));
    
    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::overlay_1::StampType>>(newPossibleStampType, string_id::cUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getStampTextColorConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    auto constraints = std::make_shared<Constraints>();
    auto staticConstraints = jobTicket->getConstraints()->getStampTextColor();
    auto possibleValues = std::vector<dune::cdm::overlay_1::StampWatermarkTextColor>();

    for(auto & textColor : staticConstraints)
    {
        possibleValues.push_back(mapToCdm(textColor));
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::overlay_1::StampWatermarkTextColor>>(possibleValues, &dune::cdm::overlay_1::StampWatermarkTextColor::valueToString, string_id::cUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::overlay_1::StampWatermarkTextColor>>(possibleValues, string_id::cUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getStampTextFontConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    auto constraints = std::make_shared<Constraints>();
    auto staticConstraints = jobTicket->getConstraints()->getStampTextFont();
    auto possibleValues = std::vector<dune::cdm::overlay_1::StampWatermarkTextFont>();

    for(auto & textFont : staticConstraints)
    {
        possibleValues.push_back(mapToCdm(textFont));
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::overlay_1::StampWatermarkTextFont>>(possibleValues, &dune::cdm::overlay_1::StampWatermarkTextFont::valueToString, string_id::cUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::overlay_1::StampWatermarkTextFont>>(possibleValues, string_id::cUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getStampTextSizeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    auto constraints = std::make_shared<Constraints>();
    auto staticConstraints = jobTicket->getConstraints()->getStampTextSize();
    auto possibleValues = std::vector<dune::cdm::overlay_1::StampWatermarkTextSize>();

    for(auto & textSize : staticConstraints)
    {
        possibleValues.push_back(mapToCdm(textSize));
    }

    // Remove thirtyPoint, fortyPoint, and sixtyPoint from the list of possible values
    // Stamp does not support thirtyPoint, fortyPoint, and sixtyPoint
    possibleValues.erase(
        std::remove_if(possibleValues.begin(), possibleValues.end(),
                    [](dune::cdm::overlay_1::StampWatermarkTextSize size) {
                        return size == dune::cdm::overlay_1::StampWatermarkTextSize::thirtyPoint ||
                                size == dune::cdm::overlay_1::StampWatermarkTextSize::fortyPoint ||
                                size == dune::cdm::overlay_1::StampWatermarkTextSize::sixtyPoint;
                    }),
        possibleValues.end());

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::overlay_1::StampWatermarkTextSize>>(possibleValues, &dune::cdm::overlay_1::StampWatermarkTextSize::valueToString, string_id::cUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::overlay_1::StampWatermarkTextSize>>(possibleValues, string_id::cUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getStampPageNumberingStyleConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    auto constraints = std::make_shared<Constraints>();
    auto staticConstraints = jobTicket->getConstraints()->getStampPageNumberingStyle();
    auto possibleValues = std::vector<dune::cdm::overlay_1::scanStampLocation::PageNumberingStyle>();

    for(auto & pageNumbering : staticConstraints)
    {
        possibleValues.push_back(mapToCdm(pageNumbering));
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::overlay_1::scanStampLocation::PageNumberingStyle>>(possibleValues, &dune::cdm::overlay_1::scanStampLocation::PageNumberingStyle::valueToString, string_id::cUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::overlay_1::scanStampLocation::PageNumberingStyle>>(possibleValues, string_id::cUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getScanCaptureModeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getScanCaptureModeConstraints - Enter");

    auto staticScanCaptureModes = jobTicket->getConstraints()->getScanCaptureModes();
    auto possibleValues = std::vector<dune::cdm::jobTicket_1::ScanCaptureMode>();
    auto validValues = std::vector<dune::cdm::jobTicket_1::ScanCaptureMode>();
    auto constraints = std::make_shared<Constraints>();

    for(auto & mode : staticScanCaptureModes)
    {
        possibleValues.push_back(mapToCdm(mode));
        if(mode == dune::scan::types::ScanCaptureModeType::BOOKMODE)
        {
            // if plex mode is simplex and media size is A4 or Letter
            if(jobTicket->getIntent()->getInputPlexMode() == dune::imaging::types::Plex::SIMPLEX)
            {
                validValues.push_back(mapToCdm(mode));
            }
        }
        else if((jobTicket->getIntent()->getPagesPerSheet() != dune::imaging::types::CopyOutputNumberUpCount::OneUp)  && mode == dune::scan::types::ScanCaptureModeType::IDCARD)
        {
            continue;
        }
        else {
            validValues.push_back(mapToCdm(mode));
        }
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<dune::cdm::jobTicket_1::ScanCaptureMode>>(possibleValues, &dune::cdm::jobTicket_1::ScanCaptureMode::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<ScanCaptureMode>>(validValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getWatermarkTypeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getWatermarkTypeConstraints - Enter");

    auto staticWatermarkType = jobTicket->getConstraints()->getWatermarkTypes();
    auto possibleValues = std::vector<dune::cdm::overlay_1::watermarkDetails::WatermarkType>();
    auto validValues = std::vector<dune::cdm::overlay_1::watermarkDetails::WatermarkType>();
    auto constraints = std::make_shared<Constraints>();

    for(auto & mode : staticWatermarkType)
    {
        possibleValues.push_back(mapToCdm(mode));
        validValues.push_back(mapToCdm(mode));
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<WatermarkType>>(possibleValues, &dune::cdm::overlay_1::watermarkDetails::WatermarkType::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<WatermarkType>>(validValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getWatermarkIdConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getWatermarkIdConstraints - Enter");

    auto staticWatermarkId = jobTicket->getConstraints()->getWatermarkIds();
    auto possibleValues = std::vector<dune::cdm::overlay_1::WatermarkTextType>();
    auto validValues = std::vector<dune::cdm::overlay_1::WatermarkTextType>();
    auto constraints = std::make_shared<Constraints>();

    for(auto & id : staticWatermarkId)
    {
        possibleValues.push_back(mapToCdm(id));
        validValues.push_back(mapToCdm(id));
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<WatermarkTextType>>(possibleValues, &dune::cdm::overlay_1::WatermarkTextType::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<WatermarkTextType>>(validValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getWatermarkTextFontConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getWatermarkTextFontConstraints - Enter");

    auto staticWatermarkTextFont = jobTicket->getConstraints()->getWatermarkTextFonts();
    auto possibleValues = std::vector<dune::cdm::overlay_1::StampWatermarkTextFont>();
    auto validValues = std::vector<dune::cdm::overlay_1::StampWatermarkTextFont>();
    auto constraints = std::make_shared<Constraints>();

    for(auto & font : staticWatermarkTextFont)
    {
        possibleValues.push_back(mapToCdm(font));
        validValues.push_back(mapToCdm(font));
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<StampWatermarkTextFont>>(possibleValues, &dune::cdm::overlay_1::StampWatermarkTextFont::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<StampWatermarkTextFont>>(validValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getWatermarkTextSizeConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getWatermarkTextSizeConstraints - Enter");

    auto staticWatermarkTextSize = jobTicket->getConstraints()->getWatermarkTextSizes();
    auto possibleValues = std::vector<dune::cdm::overlay_1::StampWatermarkTextSize>();
    auto validValues = std::vector<dune::cdm::overlay_1::StampWatermarkTextSize>();
    auto constraints = std::make_shared<Constraints>();

    for(auto & size : staticWatermarkTextSize)
    {
        possibleValues.push_back(mapToCdm(size));
        validValues.push_back(mapToCdm(size));
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<StampWatermarkTextSize>>(possibleValues, &dune::cdm::overlay_1::StampWatermarkTextSize::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<StampWatermarkTextSize>>(validValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getWatermarkTextColorConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getWatermarkTextColorConstraints - Enter");

    auto staticWatermarkTextColor = jobTicket->getConstraints()->getWatermarkTextColors();
    auto possibleValues = std::vector<dune::cdm::overlay_1::StampWatermarkTextColor>();
    auto validValues = std::vector<dune::cdm::overlay_1::StampWatermarkTextColor>();
    auto constraints = std::make_shared<Constraints>();

    for(auto & color : staticWatermarkTextColor)
    {
        possibleValues.push_back(mapToCdm(color));
        validValues.push_back(mapToCdm(color));
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<StampWatermarkTextColor>>(possibleValues, &dune::cdm::overlay_1::StampWatermarkTextColor::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<StampWatermarkTextColor>>(validValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getWatermarkOnlyFirstPageConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getWatermarkOnlyFirstPageConstraints - Enter");
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

std::shared_ptr<Constraints> CopyJobConstraintRules::getWatermarkRotate45Constraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getWatermarkRotate45Constraints - Enter");
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

std::shared_ptr<Constraints> CopyJobConstraintRules::getWatermarkBackgroundColorConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getWatermarkBackgroundColorConstraints - Enter");

    auto staticWatermarkBackgroundColor = jobTicket->getConstraints()->getWatermarkBackgroundColors();
    auto possibleValues = std::vector<dune::cdm::overlay_1::watermarkDetails::BackgroundColor>();
    auto validValues = std::vector<dune::cdm::overlay_1::watermarkDetails::BackgroundColor>();
    auto constraints = std::make_shared<Constraints>();

    for(auto & color : staticWatermarkBackgroundColor)
    {
        possibleValues.push_back(mapToCdm(color));
        validValues.push_back(mapToCdm(color));
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<BackgroundColor>>(possibleValues, &dune::cdm::overlay_1::watermarkDetails::BackgroundColor::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<BackgroundColor>>(validValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getWatermarkBackgroundPatternConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
{
    CHECKPOINTC("CopyJobConstraintRules::getWatermarkBackgroundPatternConstraints - Enter");

    auto staticWatermarkBackgroundPattern = jobTicket->getConstraints()->getWatermarkBackgroundPatterns();
    auto possibleValues = std::vector<dune::cdm::overlay_1::watermarkDetails::BackgroundPattern>();
    auto validValues = std::vector<dune::cdm::overlay_1::watermarkDetails::BackgroundPattern>();
    auto constraints = std::make_shared<Constraints>();

    for(auto & pattern : staticWatermarkBackgroundPattern)
    {
        possibleValues.push_back(mapToCdm(pattern));
        validValues.push_back(mapToCdm(pattern));
    }

    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<BackgroundPattern>>(possibleValues, &dune::cdm::overlay_1::watermarkDetails::BackgroundPattern::valueToString, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<BackgroundPattern>>(validValues, string_id::cThisOptionUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    return constraints;
}

std::shared_ptr<Constraints> CopyJobConstraintRules::getWatermarkDarknessConstraints(std::shared_ptr<ICopyJobTicket> jobTicket)
    {
        int minWatermarkDarkness  = jobTicket->getConstraints()->getMinWatermarkDarkness();
        int maxWatermarkDarkness  = jobTicket->getConstraints()->getMaxWatermarkDarkness();
        int stepWatermarkDarkness = jobTicket->getConstraints()->getStepWatermarkDarkness();

        auto constraints = std::make_shared<Constraints>();

        // range - min, max, step - (on a number)
        auto rangeConstraint = std::make_unique<RangeInt>(minWatermarkDarkness, maxWatermarkDarkness, stepWatermarkDarkness, string_id::cThisOptionUnavailable);
        constraints->add(std::move(rangeConstraint));

        return constraints;
    }

void CopyJobConstraintRules::updateScanContentOrientationConstraints(std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> scanConstraintsGroup, 
                                                            std::shared_ptr<ICopyJobTicket> jobTicket)
{
    /* Update contentOrientation */
    if(scanConstraintsGroup->getConstraints("src/scan/contentOrientation") != nullptr 
            && jobTicket->IsInstalledPageBasedFinisherDevice())
    {
        bool isLocked = false;
        std::vector<dune::cdm::glossary_1::ContentOrientation> previousValidValues;
        std::vector<dune::cdm::glossary_1::ContentOrientation> updateValidValues;

        std::shared_ptr<dune::framework::data::constraints::Constraints> constraints = scanConstraintsGroup->getConstraints("src/scan/contentOrientation");
        if(constraints)
        {
            for(auto constraint : constraints->getConstraints())
            {
                if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::LOCK)
                {
                    isLocked = true;
                    break;
                }
                else if(constraint->getConstraintType() == dune::framework::data::constraints::ConstraintType::VALID_VALUE_ENUM)
                {
                    previousValidValues = static_cast<dune::framework::data::constraints::ValidValuesEnum<dune::cdm::glossary_1::ContentOrientation>*>(constraint)->getValidValues();
                }
            }
        }

        if(!isLocked)
        {
            auto resValidOrientation = jobTicket->getPageBasedFinisherValidContentOrientation();
            auto result = std::get<0>(resValidOrientation);
            if(result == true)
            {
                std::vector<dune::cdm::glossary_1::ContentOrientation> validOrientation = std::get<1>(resValidOrientation);
                bool exist = false;
                for(auto it = validOrientation.begin() ; it != validOrientation.end() ; it++)
                {
                    exist = std::any_of(previousValidValues.begin(), previousValidValues.end(),
                                                    [&](dune::cdm::glossary_1::ContentOrientation orientation) { return orientation == *it; });
                    if(exist == true)
                    {
                        updateValidValues.push_back(*it);
                    }
                }
                auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<dune::cdm::glossary_1::ContentOrientation>>(updateValidValues, string_id::cThisOptionUnavailable);
                constraints->add(std::move(enumValidValuesConstraint));
            }
        }
    }
}
