/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyTicketConverterJoltToDune.cpp
 * @date   Fri, 02 May 2025 23:00:09 +0530
 * @brief
 *
 * (C) Copyright 2025 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyTicketConverterJoltToDune.h"

// Framework includes
#include "common_debug.h"

#include "IComponentManager.h"
// #include "ISystemServices.h"
#include "ISystemConversionHelper.h"
#include "XmlElement.h"
#include "XmlParser.h"
#include "XmlUtils.h"

// Generated includes
#include "CopyTicketConverterJoltToDune_TraceAutogen.h"

#include "DuneSystemEvents.h"
#include "ScanJobIntent_generated.h"

// Component includes
#include "ICopyJobTicket.h"
#include "PipelineOptionsConvertionAdapter.h"
#include "PrintJoltToDuneConverter.h"

using APIResult = dune::framework::core::APIResult;

// Factory method
EXTERN_COMPONENT_FLAVOR_FACTORY(dune_copy_Jobs_Copy_CopyTicketConverterJoltToDune)
{
    dune::copy::Jobs::Copy::CopyTicketConverterJoltToDune* instance =
        new dune::copy::Jobs::Copy::CopyTicketConverterJoltToDune(instanceName);
    assert(instance != nullptr);
    return static_cast<dune::framework::component::IComponent*>(instance);
}

namespace dune { namespace copy { namespace Jobs { namespace Copy {

CopyTicketConverterJoltToDune::CopyTicketConverterJoltToDune(const char* instanceName) : instanceName_(instanceName)
{
    CHECKPOINTC("%s/CopyTicketConverterJoltToDune: constructed", instanceName_);
    pipelineOptionsConverter_ = new dune::imaging::Jobs::PipelineOptionsConvertionAdapter();
    printJoltToDuneConverter_ = new PrintJoltToDuneConverter();
}

CopyTicketConverterJoltToDune::~CopyTicketConverterJoltToDune() 
{
    if (pipelineOptionsConverter_) {
        delete pipelineOptionsConverter_;
        pipelineOptionsConverter_ = nullptr;
    }
    
    if (printJoltToDuneConverter_) {
        delete printJoltToDuneConverter_;
        printJoltToDuneConverter_ = nullptr;
    }
}

// IComponent methods
dune::framework::component::ComponentFlavorUid CopyTicketConverterJoltToDune::getComponentFlavorUid() const
{
    return GET_MODULE_UID(CopyTicketConverterJoltToDune);
}

const char* CopyTicketConverterJoltToDune::getComponentInstanceName() const
{
    return instanceName_;
}

void CopyTicketConverterJoltToDune::initialize(WorkingMode                                       mode,
                                               const dune::framework::component::SystemServices* services)
{
    DUNE_UNUSED(mode);
    DUNE_UNUSED(services);
    CHECKPOINTA("%s/CopyTicketConverterJoltToDune: initialize", instanceName_);
}

void* CopyTicketConverterJoltToDune::getInterface(dune::framework::component::InterfaceUid interfaceUid,
                                                  const char*                              portName)
{
    DUNE_UNUSED(portName);
    void* interfacePtr = nullptr;
    if (interfaceUid == GET_INTERFACE_UID(ICopyTicketConverter))
    {
        interfacePtr = static_cast<ICopyTicketConverter*>(this);
    }
    return interfacePtr;
}

void CopyTicketConverterJoltToDune::setInterface(dune::framework::component::InterfaceUid interfaceUid,
                                                 const char* portName, void* interfacePtr)
{
    CHECKPOINTA("%s/CopyTicketConverterJoltToDune::setInterface - interfaceUid: %d, portName: %s", instanceName_,
                interfaceUid, portName);

    if (interfacePtr != nullptr)
    {
        if (interfaceUid == GET_INTERFACE_UID(IScanJoltToDuneConverter))
        {
            scanJoltToDuneConverter_ = static_cast<IScanJoltToDuneConverter*>(interfacePtr);
            CHECKPOINTC("%s/CopyTicketConverterJoltToDune: setInterface ISystemConversionHelper to port %s with addr %p",
                        getComponentInstanceName(), portName, interfacePtr);
        }
        else
        {
            CHECKPOINTA("%s/CopyTicketConverterJoltToDune: setInterface not handled for interfaceUid %" PRIu32
                        " to port %s with addr %p",
                        getComponentInstanceName(), interfaceUid, portName, interfacePtr);
        }
    }
    else
    {
        CHECKPOINTA("%s/CopyTicketConverterJoltToDune: setInterface 0x%" PRIx32 " to port %s with addr %p",
                    getComponentInstanceName(), interfaceUid, portName, interfacePtr);
    }
}

void CopyTicketConverterJoltToDune::connected(dune::framework::component::IComponentManager* componentManager,
                                              std::future<void>&                             asyncCompletion)
{
    DUNE_UNUSED(componentManager);
    DUNE_UNUSED(asyncCompletion);

    if (!scanJoltToDuneConverter_) {
        CHECKPOINTA("%s/CopyTicketConverterJoltToDune::connected - scanJoltToDuneConverter_ is null", instanceName_);
    }

    CHECKPOINTA("%s/CopyTicketConverterJoltToDune::connected", instanceName_);
}

void CopyTicketConverterJoltToDune::shutdown(ShutdownCause cause, std::future<void>& asyncCompletion)
{
    DUNE_UNUSED(cause);
    DUNE_UNUSED(asyncCompletion);

    CHECKPOINTA("%s/CopyTicketConverterJoltToDune::shutdown", instanceName_);
}

dune::framework::data::conversion::ConversionResult CopyTicketConverterJoltToDune::convert(
    const dune::framework::data::conversion::DataDescriptor& fileDescriptor,
    std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& jobTicketTable)
{
    CHECKPOINTA("CopyTicketConverterJoltToDune: Entering convert");
    dune::framework::data::conversion::ConversionResult result =
        dune::framework::data::conversion::ConversionResult::SUCCESS;

    if (jobTicketTable == nullptr)
    {
        CHECKPOINTA("CopyTicketConverterJoltToDune: Convert: jobTicketTable is null");
        return dune::framework::data::conversion::ConversionResult::ERROR;
    }

    auto fileName = fileDescriptor.fileName_;
    auto dataNodePath = fileDescriptor.dataNodePath_;

    CHECKPOINTB("CopyTicketConverterJoltToDune: Convert: Processing file %s with xpath %s", fileName.c_str(),
                dataNodePath.c_str());

    dune::framework::utils::XmlUtils xml;
    if (!xml.load(fileName, dataNodePath))
    {
        CHECKPOINTA("CopyTicketConverterJoltToDune: Convert: Failed to load file");
        return dune::framework::data::conversion::ConversionResult::ERROR;
    }

    // Convert scan settings
    //TO DO: optimize the call to scan converter
    {
        dune::framework::data::conversion::DataDescriptor fileDesc{fileName, dataNodePath + "/dsd:ScanSettings"};
        auto scanResult = scanJoltToDuneConverter_->convert(fileDesc, jobTicketTable);
        if (scanResult == APIResult::ERROR)
        {
            CHECKPOINTA("CopyTicketConverterJoltToDune::performJoltToDuneConversion: Failed to convert scan settings");
            return dune::framework::data::conversion::ConversionResult::ERROR;
        }

        fileDesc = {fileName, dataNodePath + "/copy:CopySettings"};
        scanResult = scanJoltToDuneConverter_->convert(fileDesc, jobTicketTable);
        if (scanResult == APIResult::ERROR)
        {
            CHECKPOINTA("CopyTicketConverterJoltToDune::performJoltToDuneConversion: Failed to convert scan settings");
            return dune::framework::data::conversion::ConversionResult::ERROR;
        }

        // 
        fileDesc = {fileName, dataNodePath};
        scanResult = scanJoltToDuneConverter_->convert(fileDesc, jobTicketTable);
        if (scanResult == APIResult::ERROR)
        {
            CHECKPOINTA("CopyTicketConverterJoltToDune::performJoltToDuneConversion: Failed to convert copy 2 settings");
            return dune::framework::data::conversion::ConversionResult::ERROR;
        }

    }

    auto convertionRes = pipelineOptionsConverter_->convert(fileDescriptor, jobTicketTable,
                                                        {"/dsd:ScanSettings", "/copy:CopySettings", ""});
    if (convertionRes == APIResult::ERROR)
    {
        CHECKPOINTA("CopyTicketConverterJoltToDune::performJoltToDuneConversion: Failed to convert pipeline options");
        return dune::framework::data::conversion::ConversionResult::ERROR;
    }

    if (xml.isKeyAvailable("/copy:CopySettings"))
    {
        dune::framework::data::conversion::DataDescriptor fileDesc{fileName, dataNodePath + "/copy:CopySettings"};
        auto printResult = printJoltToDuneConverter_->convert(fileDesc, jobTicketTable);
        if (printResult == APIResult::ERROR)
        {
            CHECKPOINTA("CopyTicketConverterJoltToDune::performJoltToDuneConversion: Failed to convert print settings");
            return dune::framework::data::conversion::ConversionResult::ERROR;
        }
    }

    CHECKPOINTA("CopyTicketConverterJoltToDune: Convert: Conversion -Exit");
    return result;
}

}}}}  // namespace dune::copy::Jobs::Copy
