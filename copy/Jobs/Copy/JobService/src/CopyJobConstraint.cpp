/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobConstraint.cpp
 * @date   Wed, 23 Dec 2020 16:00:15
 * @brief  Copy Job Constraint
 *
 * (C) Copyright 2019 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobConstraint.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

/**
 * @brief Construct a new Copy JobConstraint:: Copy Job Constraint object
 *
 */
CopyJobConstraint::CopyJobConstraint()
{
}

dune::copy::Jobs::Copy::CopyJobMediaSupportedType* CopyJobConstraint::findCopyJobMediaSupportedType(dune::imaging::types::MediaIdType mediaType)
{
    dune::copy::Jobs::Copy::CopyJobMediaSupportedType* retVal = NULL;
    for(auto it = mediaSupportType_.begin() ; it != mediaSupportType_.end() ; it++)
    {
        if(it->getId() == mediaType)
        {
            retVal = &(*it);
            break;
        }
    }
    return retVal;
}

dune::copy::Jobs::Copy::CopyJobMediaSupportedSize* CopyJobConstraint::findCopyJobMediaSupportedSize(dune::imaging::types::MediaSizeId mediaSize)
{
    dune::copy::Jobs::Copy::CopyJobMediaSupportedSize* retVal = NULL;
    for(auto it = mediaSupportSize_.begin() ; it != mediaSupportSize_.end() ; it++)
    {
        if(it->getId() == mediaSize)
        {
            retVal = &(*it);
            break;
        }
    }
    return retVal;
}

void CopyJobMediaSupportedSize::addSupportedMediaSource(std::vector<dune::imaging::types::MediaSource> supportedMediaSource)
{
    for(auto iter = supportedMediaSource.begin() ; iter != supportedMediaSource.end(); iter++)
    {
        supportedMediaSource_.insert(*iter);
    }
}

void CopyJobMediaSupportedSize::addDuplex(std::vector<dune::imaging::types::Plex> duplex)
{
    for(auto iter = duplex.begin() ; iter != duplex.end(); iter++)
    {
        duplex_.insert(*iter);
    }
}

void CopyJobMediaSupportedType::addSupportedMediaSource(std::vector<dune::imaging::types::MediaSource> supportedMediaSource)
{
    for(auto iter = supportedMediaSource.begin() ; iter != supportedMediaSource.end(); iter++)
    {
        supportedMediaSource_.insert(*iter);
    }
}

void CopyJobMediaSupportedType::addDuplex(std::vector<dune::imaging::types::Plex> duplex)
{
    for(auto iter = duplex.begin() ; iter != duplex.end(); iter++)
    {
        duplex_.insert(*iter);
    }
}


void CopyJobMediaSupportedType::addColorMode(std::vector<dune::imaging::types::ColorMode> colorMode)
{
    for(auto iter = colorMode.begin() ; iter != colorMode.end(); iter++)
    {
        colorMode_.insert(*iter);
    }
}

}}}}
