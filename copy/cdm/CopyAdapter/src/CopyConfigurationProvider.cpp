///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyConfigurationProvider.cpp
 * @date   May 18, 2022
 * @brief  This is a CDM provider for scan destination configurations
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyConfigurationProvider.h"

#include "common_debug.h"
#include "CopyConfigurationProvider_TraceAutogen.h"
#include "DuneException.h"
#include "HttpCommonTypes.h"

using HttpStatusCodeEnum = dune::ws::framework::HttpStatusCodeEnum;
using ConfigurationData = dune::cdm::copy_1::configuration::ResourceData;
using featureEnabled  = dune::cdm::glossary_1::FeatureEnabled;

dune::cdm::glossary_1::FeatureEnabled mapToCdm(bool value)
{
    if (value)
    {
        return dune::cdm::glossary_1::FeatureEnabled::true_;
    }
    else
    {
        return dune::cdm::glossary_1::FeatureEnabled::false_;
    }
}

namespace dune { namespace copy { namespace cdm {

CopyConfigurationProvider::CopyConfigurationProvider(ICopyAdapter* copyAdapter) : copyAdapter_(copyAdapter)
{
    CHECKPOINTA("CopyConfigurationProvider::Constructor Enter/Exit");
    copyEventSubscriptionId = copyAdapter_->getCopyAdapterDataChangeEvent().addSubscription(
        EVENT_MAKE_MEMBER_DELEGATE(CopyConfigurationProvider::handleCopyAdapterDataChangeEvent, this));
}

/**
 * @brief Resource Configuration getImplementation(GET of resource)
 *
 * @param params [in] Parameters for the get access
 * @param result [out] to return the result of get of resource
 * @return pointer to the resource data buffer
 */
std::unique_ptr<ConfigurationData> CopyConfigurationProvider::getImplementation(
    const RequestParameters &params, OperationResult &result, dune::ws::cdm::OperationResponseMetadataT &respMetadata)
{
    CHECKPOINTB("CopyConfigurationProvider::getImplementation");
    DUNE_UNUSED(params);

    std::shared_ptr<dune::cdm::copy_1::types::Configuration::EasyBufferTable> configuration;
    std::unique_ptr<ConfigurationData> respData;
    bool check = true;

    CHECKPOINTB("Starting CopyConfigurationProvider get Implementation");
    try
    {
        configuration = std::make_shared<dune::cdm::copy_1::types::Configuration::EasyBufferTable>();
        configuration->copyEnabled.set(mapToCdm(copyAdapter_->getCopyEnabled()));
        configuration->colorCopyEnabled.set(mapToCdm(copyAdapter_->getColorCopyEnabled()));
        if (copyAdapter_->getCopyMode() != dune::cdm::copy_1::configuration::CopyMode::_undefined_)
        {
            //Some products do not use this value but we cannot set the value to _undefined_ for schema compliance
            configuration->copyMode.set(copyAdapter_->getCopyMode());
        }
        if (copyAdapter_->getInterruptMode() != featureEnabled::_undefined_)
        {
            configuration->allowInterrupt.set(copyAdapter_->getInterruptMode());
        }
        CHECKPOINTC("CopyConfigurationProvider::getImplementation() - copyEnabled = %d, colorCopyEnabled = %d, copyMode = %d, allowInterrupt = %d",
            static_cast<int>(configuration->copyEnabled.get()),
            static_cast<int>(configuration->colorCopyEnabled.get()),
            static_cast<int>(configuration->copyMode.get()),
            static_cast<int>(configuration->allowInterrupt.get()));
    }

    catch (dune::framework::core::DuneException &ex)
    {
        CHECKPOINTA("CopyConfigurationProvider::Dune Exception, message = %s, \nstacktrace = %s", ex.what(),
                    ex.getThrowBacktrace().c_str());
        result = OperationResult::ERROR_IPC;
        respMetadata.httpStatusCode = static_cast<int>(HttpStatusCodeEnum::HTTP_STATUS_500_INTERNAL_SERVER_ERROR);
        check = false;
    }

    catch (std::exception &ex)
    {
        CHECKPOINTA("CopyConfigurationProvider::General Exception, message = %s", ex.what());
        result = OperationResult::ERROR_IPC;
        respMetadata.httpStatusCode = static_cast<int>(HttpStatusCodeEnum::HTTP_STATUS_500_INTERNAL_SERVER_ERROR);
        check = false;
    }

    if (!check)
    {
        CHECKPOINTA("CopyConfigurationProvider : getImplementation() ends with failure");
        respData = std::make_unique<ConfigurationData>();
        return respData;
    }
    else
    {
        respData = std::make_unique<ConfigurationData>(*configuration);
        result = OperationResult::SUCCESS;
        respMetadata.httpStatusCode = static_cast<int>(HttpStatusCodeEnum::HTTP_STATUS_200_OK);
        CHECKPOINTB("CopyConfigurationProvider : getImplementation() ends");
        return respData;
    }
}

/**
 * @brief setImplementation()
 * This is the CDM PUT functionality implementation.
 * Part of the information is set into destination config.
 */

OperationResult CopyConfigurationProvider::setImplementation(const RequestParameters                   &params,
                                                            std::unique_ptr<ConfigurationData>         data,
                                                            dune::ws::cdm::OperationResponseMetadataT &respMetadata)
{
    CHECKPOINTB("Entering CopyConfigurationProvider::setImplementation()");

    OperationResult operationResult = OperationResult::SUCCESS;
    try
    {
        if (data)
        {
            auto configuration = dune::cdm::copy_1::ConfigurationTable::deserializeFactory(*data);

            CHECKPOINTD(
                "CopyConfigurationProvider::setImplementation Received: colorEnabled: %d / '%s', "
                "colorCopyEnabled: %d / '%s', copyMode: %d / '%s' ",
                static_cast<int>(configuration->copyEnabled.get()),
                dune::cdm::glossary_1::EnumNameFeatureEnabled(configuration->copyEnabled.get()),
                static_cast<int>(configuration->colorCopyEnabled.get()),
                dune::cdm::glossary_1::EnumNameFeatureEnabled(configuration->colorCopyEnabled.get()),
                static_cast<int>(configuration->copyMode.get()),
                dune::cdm::copy_1::configuration::EnumNameCopyMode(configuration->copyMode.get()));
            

            bool isOperationAllowed = isModifyAllowed(params, data);

            if( !isOperationAllowed )
            {
                operationResult = OperationResult::ERROR_NOT_AUTHORIZED;
            }
            else // Modify
            {
                if (configuration->copyEnabled.get() != featureEnabled::_undefined_)
                {
                    copyAdapter_->setCopyEnabled(configuration->copyEnabled.get());
                }

                if (configuration->colorCopyEnabled.get() != featureEnabled::_undefined_)
                {
                    copyAdapter_->setColorCopyEnabled(configuration->colorCopyEnabled.get());
                }

                if (configuration->copyMode.get() != dune::cdm::copy_1::configuration::CopyMode::_undefined_)
                {
                    copyAdapter_->setCopyMode(configuration->copyMode.get());
                }

                if(configuration->allowInterrupt.get() != featureEnabled::_undefined_)
                {
                    copyAdapter_->setInterruptMode(configuration->allowInterrupt.get());
                }
            }
        }
        else
        {
            CHECKPOINTA("CopyConfigurationProvider::setImplementation Failed to set the settings");
            operationResult = OperationResult::ERROR_PARSING_ERROR;
        }

        if (operationResult == OperationResult::SUCCESS)
        {
            CHECKPOINTB("CopyConfigurationProvider::setImplementation successfully set the adapterConfig: HTTP_STATUS_204_NO_CONTENT \n");
            respMetadata.httpStatusCode = static_cast<int>(HttpStatusCodeEnum::HTTP_STATUS_204_NO_CONTENT);
        }
        else
        {
            CHECKPOINTA("CopyConfigurationProvider::setImplementation Failed to set the adapterConfig: HTTP_STATUS_400_BAD_REQUEST \n");
            respMetadata.httpStatusCode = static_cast<int>(HttpStatusCodeEnum::HTTP_STATUS_400_BAD_REQUEST);
        }
    } catch (dune::framework::core::DuneException &ex)
    {
        CHECKPOINTA("CopyConfigurationProvider::setImplementation Dune Exception, message = %s, \nstacktrace = %s", ex.what(),
                    ex.getThrowBacktrace().c_str());
        operationResult = OperationResult::ERROR_IPC;
        respMetadata.httpStatusCode = static_cast<int>(HttpStatusCodeEnum::HTTP_STATUS_500_INTERNAL_SERVER_ERROR);
    } catch (std::exception &ex)
    {
        CHECKPOINTA("CopyConfigurationProvider::setImplementation General Exception, message = %s", ex.what());
        operationResult = OperationResult::ERROR_IPC;
        respMetadata.httpStatusCode = static_cast<int>(HttpStatusCodeEnum::HTTP_STATUS_500_INTERNAL_SERVER_ERROR);
    }
    return operationResult;
}

/**
 * @brief modifyImplementation()
 * This is the CDM PATCH functionality implementation.
 * Part of the information is set into destination config.
 */

OperationResult CopyConfigurationProvider::modifyImplementation(const RequestParameters                   &params,
                                                                std::unique_ptr<ConfigurationData>         data,
                                                                dune::ws::cdm::OperationResponseMetadataT &respMetadata)
{
    CHECKPOINTB("Entering CopyConfigurationProvider::modifyImplementation()");

    OperationResult operationResult = OperationResult::SUCCESS;
    try
    {
        if (data)
        {
            auto configuration = dune::cdm::copy_1::ConfigurationTable::deserializeFactory(*data);
            if (configuration != nullptr)
            {
                auto isPatch = dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH;

                if ( !isModifyAllowed(params, data) )
                {
                    operationResult = OperationResult::ERROR_NOT_AUTHORIZED;
                }
                else
                {
                    if (configuration->copyEnabled.isSet(isPatch))
                    {
                        CHECKPOINTC("CopyConfigurationProvider::modifyImplementation() - copyEnabled set %d -> %d",
                                    (int)(copyAdapter_->getCopyEnabled()), (int)(configuration->copyEnabled.get()));
                        copyAdapter_->setCopyEnabled(configuration->copyEnabled.get());
                    }

                    if (configuration->colorCopyEnabled.isSet(isPatch))
                    {
                        CHECKPOINTC("CopyConfigurationProvider::modifyImplementation() - colorCopyEnabled set %d -> %d",
                                    (int)(copyAdapter_->getColorCopyEnabled()), (int)(configuration->colorCopyEnabled.get()));
                        copyAdapter_->setColorCopyEnabled(configuration->colorCopyEnabled.get());
                    }

                    if (configuration->copyMode.isSet(isPatch))
                    {
                        CHECKPOINTC("CopyConfigurationProvider::modifyImplementation() - copyMode set %d -> %d",
                                    (int)(copyAdapter_->getCopyMode()), (int)(configuration->copyMode.get()));
                        copyAdapter_->setCopyMode(configuration->copyMode.get());
                    }

                    if(configuration->allowInterrupt.isSet(isPatch))
                    {
                        CHECKPOINTC("CopyConfigurationProvider::modifyImplementation() - allowInterrupt set %d -> %d",
                                    (int)(copyAdapter_->getInterruptMode()), (int)(configuration->allowInterrupt.get()));
                        copyAdapter_->setInterruptMode(configuration->allowInterrupt.get());
                    }
                }
            }
            else
            {
                CHECKPOINTA("CopyConfigurationProvider::modifyImplementation configuration is nullptr");
                operationResult = OperationResult::ERROR_PARSING_ERROR;
            }
        }
        else
        {
            CHECKPOINTA("CopyConfigurationProvider::modifyImplementation Failed to set the settings");
            operationResult = OperationResult::ERROR_PARSING_ERROR;
        }

        if (operationResult == OperationResult::SUCCESS)
        {
            CHECKPOINTB("CopyConfigurationProvider::modifyImplementation successfully set the adapterConfig: HTTP_STATUS_204_NO_CONTENT \n");
            respMetadata.httpStatusCode = static_cast<int>(HttpStatusCodeEnum::HTTP_STATUS_204_NO_CONTENT);
        }
        else if ( operationResult == OperationResult::ERROR_NOT_AUTHORIZED )
        {
            CHECKPOINTA("CopyConfigurationProvider::modifyImplementation Failed to set the adapterConfig: HTTP_STATUS_403_FORBIDDEN");
            respMetadata.httpStatusCode = static_cast<int>(HttpStatusCodeEnum::HTTP_STATUS_403_FORBIDDEN);
        }
        else
        {
            CHECKPOINTA("CopyConfigurationProvider::modifyImplementation Failed to set the adapterConfig: HTTP_STATUS_400_BAD_REQUEST \n");
            respMetadata.httpStatusCode = static_cast<int>(HttpStatusCodeEnum::HTTP_STATUS_400_BAD_REQUEST);
        }
    } catch (dune::framework::core::DuneException &ex)
    {
        CHECKPOINTA("CopyConfigurationProvider::modifyImplementation Dune Exception, message = %s, \nstacktrace = %s", ex.what(),
                    ex.getThrowBacktrace().c_str());
        operationResult = OperationResult::ERROR_IPC;
        respMetadata.httpStatusCode = static_cast<int>(HttpStatusCodeEnum::HTTP_STATUS_500_INTERNAL_SERVER_ERROR);
    } catch (std::exception &ex)
    {
        CHECKPOINTA("CopyConfigurationProvider::modifyImplementation General Exception, message = %s", ex.what());
        operationResult = OperationResult::ERROR_IPC;
        respMetadata.httpStatusCode = static_cast<int>(HttpStatusCodeEnum::HTTP_STATUS_500_INTERNAL_SERVER_ERROR);
    }
    return operationResult;
}

bool CopyConfigurationProvider::isModifyAllowed( const RequestParameters &params, std::unique_ptr<ConfigurationData> &data )
{
    auto configuration = dune::cdm::copy_1::ConfigurationTable::deserializeFactory(*data);
    auto isPatch = dune::cdm::easyBuffers::VALUE_IN_MERGE_PATCH;
    bool result = false;
    // Operation is allowed for those products whose original CopyMode or Interrupt is other than undefined
    // or those products who have this value undefined in the configuration

    if (configuration == nullptr)
    {
        CHECKPOINTA("CopyConfigurationProvider::isModifyAllowed configuration is nullptr");
        result = false;
    }

    CHECKPOINTA("CopyConfigurationProvider::isModifyAllowed cdm(copyMode:%d, allowInterrupt:%d) adapter(copyMode:%d, allowInterrupt:%d)",
                static_cast<int>(configuration->copyMode.get()),
                static_cast<int>(configuration->allowInterrupt.get()),
                static_cast<int>(copyAdapter_->getCopyMode()),
                static_cast<int>(copyAdapter_->getInterruptMode()));

    result = (copyAdapter_->getCopyMode() != dune::cdm::copy_1::configuration::CopyMode::_undefined_ 
        || configuration->copyMode.get() == dune::cdm::copy_1::configuration::CopyMode::_undefined_) &&
        
        (copyAdapter_->getInterruptMode() != featureEnabled::_undefined_ 
        || configuration->allowInterrupt.get() == featureEnabled::_undefined_);

    CHECKPOINTB("CopyConfigurationProvider::isModifyAllowed: %s", result ? "true" : "false");

    return result;
}

void CopyConfigurationProvider::onDataChangeEventSubscription(bool active)
{
    isDataChangeSubscriptionActive_ = active;
}

void CopyConfigurationProvider::handleCopyAdapterDataChangeEvent(dune::copy::cdm::CopyConfigurationEventType event)
{
    DUNE_UNUSED(event);
    CHECKPOINTD("CopyConfigurationProvider::handleCopyAdapterDataChangeEvent - ENTER");

    //pushDataChangeEvent
    if (isDataChangeSubscriptionActive_)
    {
        auto configurationTable = std::make_shared<dune::cdm::copy_1::types::Configuration::EasyBufferTable>();
        std::unique_ptr<ConfigurationData> respData;

        configurationTable->copyEnabled.set(mapToCdm(copyAdapter_->getCopyEnabled()));
        configurationTable->colorCopyEnabled.set(mapToCdm(copyAdapter_->getColorCopyEnabled()));
        configurationTable->copyMode.set(copyAdapter_->getCopyMode());
        configurationTable->allowInterrupt.set(copyAdapter_->getInterruptMode());

        respData = std::make_unique<ConfigurationData>(*configurationTable);
        CHECKPOINTD("CopyConfigurationProvider::handleCopyAdapterDataChangeEvent pushing event to clients");
        pushDataChangeEvent(std::move(respData));
    }
    else
    {
        this->incrementSequenceNumber(nullptr);
    }

    CHECKPOINTD("CopyConfigurationProvider::handleCopyAdapterDataChangeEvent - EXIT");
}

}}}  // namespace dune::copy::cdm