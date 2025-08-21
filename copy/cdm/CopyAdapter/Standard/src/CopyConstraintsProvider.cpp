///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyConstraintsProvider.cpp
 * @date
 * @brief  Implementation of resource providers for Copy constraints
 *
 * (C) Copyright 2023 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyConstraintsProvider.h"
#include "common_debug.h"
#include "IMicroServiceFactory.h"
#include "ResourceConstraintsHelper.h"
#include "ResourceProviderHelpers.h"
#include "CopyConstraintsProvider_TraceAutogen.h"
#include <HttpCommonTypes.h>
#include "com.hp.cdm.domain.glossary.version.1.easybuffers_autogen.h"
#include "StringIds.h"
#include "ILocaleProvider.h"
#include "ICopyAdapter.h"

namespace dune { namespace copy { namespace cdm {

using HttpStatusCodeEnum = dune::ws::framework::HttpStatusCodeEnum;
using FeatureEnabled = dune::cdm::glossary_1::FeatureEnabled;
using namespace dune::localization;

/**
 * CopyConfigurationConstraintsProvider
 */
CopyConfigurationConstraintsProvider::CopyConfigurationConstraintsProvider(ICopyAdapter * copyAdapter, dune::localization::ILocaleProvider * localeProvider, 
                                                                            std::shared_ptr<dune::copy::cdm::ConstraintsStringIdValuesT> constraintsStringIds)
    : copyAdapter_(copyAdapter), 
      localeProvider_(localeProvider), 
      constraintsStringIds_(constraintsStringIds)
{
    CHECKPOINTA("CopyConfigurationConstraintsProvider: constructed");

    copyEventSubscriptionId = copyAdapter_->getCopyAdapterDataChangeEvent().addSubscription(
        EVENT_MAKE_MEMBER_DELEGATE(CopyConfigurationConstraintsProvider::handleCopyAdapterDataChangeEvent, this));
}


void CopyConfigurationConstraintsProvider::onDataChangeEventSubscription(bool active)
{
    CHECKPOINTD("CopyConfigurationConstraintsProvider::onDataChangeEventSubscription ");

    isDataChangeSubscriptionActive_ = active;
}

bool CopyConfigurationConstraintsProvider::handleCopyAdapterDataChangeEvent(dune::copy::cdm::CopyConfigurationEventType event)
{

    CHECKPOINTC("CopyConfigurationConstraintsProvider::handleCopyAdapterDataChangeEvent - ENTER isDataChangeSubscriptionActive_:%s event:%d",
         isDataChangeSubscriptionActive_? "TRUE" : "FALSE",
         (int)event);

    bool isPushedDataChangeEvent{false};

    if ((isDataChangeSubscriptionActive_) && (event == dune::copy::cdm::CopyConfigurationEventType::COPY_MODE))
    {
        auto respData = std::make_unique<ConfigurationConstraintsResourceData>();

        std::shared_ptr<dune::localization::ILocale> locale{nullptr};
        if (localeProvider_ != nullptr)
        {
            locale = localeProvider_->deviceLocale();
        }
        else
        {
            CHECKPOINTD("CopyConfigurationConstraintsProvider::handleCopyAdapterDataChangeEvent locale null");
        }

        std::unique_ptr<dune::framework::data::constraints::ConstraintsGroup> constraintsGroup{nullptr};

        auto copyMode = copyAdapter_->getCopyMode();

        if( copyMode != dune::cdm::copy_1::configuration::CopyMode::_undefined_)
        {
            constraintsGroup = std::make_unique<dune::framework::data::constraints::ConstraintsGroup>();
            auto allowInterruptConstraints = getAllowInterruptConstraints( copyAdapter_->getCopyMode() == dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
            constraintsGroup->set("allowInterrupt", allowInterruptConstraints);
        }
    
        if (constraintsGroup)
        {
            auto constraintsFbt = dune::ws::cdm::ResourceConstraintsHelper::constraintsGroupToConstraintsFbt(std::move(constraintsGroup), locale);

            if (constraintsFbt)
            {
                respData->setFlatBufferT(std::move(constraintsFbt));
                CHECKPOINTD("CopyConfigurationConstraintsProvider::handleCopyAdapterDataChangeEvent pushing event to clients");
                pushDataChangeEvent(std::move(respData));

                isPushedDataChangeEvent = true;
            }
        }
    }
    else
    {
        this->incrementSequenceNumber(nullptr);
    }

    CHECKPOINTD("CopyConfigurationConstraintsProvider::handleCopyAdapterDataChangeEvent - EXIT");
    return isPushedDataChangeEvent;

}

std::string CopyConfigurationConstraintsProvider::getConstraintInterruptMessage()
{
    std::string incompatibleSetings = localeProvider_->deviceLocale()->get(localeProvider_->deviceLocale()->getStringIdForCsfOnly(constraintsStringIds_->incompatibleSettings));

    dune::localization::ParameterizedString parameterizedIncompatibleSettingString(dune::localization::string_id::cStringColon,
            incompatibleSetings);

    dune::localization::ParameterizedString parameterizedCopyIndirectString(dune::localization::string_id::cStringBullet,
            dune::localization::string_id::cCopySendManually);

    dune::localization::ParameterizedString parameterizedEnableString(dune::localization::string_id::cStringBullet,
            dune::localization::string_id::cEnable);

    std::string result =
        localeProvider_->deviceLocale()->get(localeProvider_->deviceLocale()->getStringIdForCsfOnly(constraintsStringIds_->configuringIncompatible)) +
        "\n\n" +
        localeProvider_->deviceLocale()->get(dune::localization::string_id::cCopyJobsToInterrupt) + "\n" +
        localeProvider_->deviceLocale()->format(&parameterizedEnableString) +
        "\n\n" +
        localeProvider_->deviceLocale()->format(&parameterizedIncompatibleSettingString) +
        "\n\n" +
        localeProvider_->deviceLocale()->get(localeProvider_->deviceLocale()->getStringIdForCsfOnly(constraintsStringIds_->copyMode)) + "\n" +
        localeProvider_->deviceLocale()->format(&parameterizedCopyIndirectString) + "\n";

    return result;
}

std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> CopyConfigurationConstraintsProvider::getCopyConfigurationConstraints()
{
    auto constraintsGroup = std::make_unique<dune::framework::data::constraints::ConstraintsGroup>();
    auto copyMode = copyAdapter_->getCopyMode();

    if(copyMode != dune::cdm::copy_1::configuration::CopyMode::_undefined_)
    {
        auto allowInterruptConstraints = getAllowInterruptConstraints(copyMode == dune::cdm::copy_1::configuration::CopyMode::printWhileScanning);
        constraintsGroup->set("allowInterrupt", allowInterruptConstraints);
    }

    // Add constraint for Enable Disable
    //Possible values on an Enum
    auto copyEnabledconstraints = std::make_shared<Constraints>();
    auto values = { FeatureEnabled::true_, FeatureEnabled::false_ };
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<FeatureEnabled>>(values, &dune::cdm::glossary_1::FeatureEnabledEnum::valueToString, string_id::cUnavailable);
    copyEnabledconstraints->add(std::move(enumPossibleValueConstraint));    

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<FeatureEnabled>>(values, string_id::cUnavailable);
    copyEnabledconstraints->add(std::move(enumValidValuesConstraint));

    constraintsGroup->set("copyEnabled", copyEnabledconstraints);

    return constraintsGroup;
}

std::shared_ptr<Constraints> CopyConfigurationConstraintsProvider::getAllowInterruptConstraints(bool isCopyModePrintWhileScanning)
{
    CHECKPOINTC("CopyConfigurationConstraintsProvider::getAllowInterruptConstraints() isCopyModePrintWhileScanning:%s -- Entry",
        isCopyModePrintWhileScanning ? "TRUE" : "FALSE");

    auto constraints = std::make_shared<Constraints>();

    //Possible values on an Enum
    auto values = { FeatureEnabled::true_, FeatureEnabled::false_ };
    auto enumPossibleValueConstraint = std::make_unique<PossibleValuesEnum<FeatureEnabled>>(values, &dune::cdm::glossary_1::FeatureEnabledEnum::valueToString, string_id::cUnavailable);
    constraints->add(std::move(enumPossibleValueConstraint));    

    auto enumValidValuesConstraint = std::make_unique<ValidValuesEnum<FeatureEnabled>>(values, string_id::cUnavailable);
    constraints->add(std::move(enumValidValuesConstraint));

    if( !isCopyModePrintWhileScanning )
    {
        constraints->add(std::make_unique<Lock>(getConstraintInterruptMessage()));
    }

    return constraints;
}

std::unique_ptr<ConfigurationConstraintsResourceData> CopyConfigurationConstraintsProvider::getImplementation(
    const RequestParameters &params, OperationResult &result, dune::ws::cdm::OperationResponseMetadataT &respMetadata)
{
    CHECKPOINTC("CopyConfigurationConstraintsProvider::getImplementation() -- Entry");

    auto respData = std::make_unique<ConfigurationConstraintsResourceData>();

    std::string acceptLanguage;
    dune::ws::cdm::ResourceProviderHelpers::getRequestHeader(params, dune::ws::framework::HttpRequestHeaderNameEnum::ACCEPT_LANGUAGE, acceptLanguage);

    std::shared_ptr<dune::localization::ILocale> locale{nullptr};
    if (localeProvider_ != nullptr)
    {
        locale = localeProvider_->getLocale(acceptLanguage.c_str());
    }

    auto constraintsGroup = getCopyConfigurationConstraints();

    auto constraintsFbt = dune::ws::cdm::ResourceConstraintsHelper::constraintsGroupToConstraintsFbt(std::move(constraintsGroup), locale);
    if (constraintsFbt)
    {
        respData->setFlatBufferT(std::move(constraintsFbt));
        result = OperationResult::SUCCESS;
        respMetadata.httpStatusCode = static_cast<int>(HttpStatusCodeEnum::HTTP_STATUS_200_OK);
    }
    else
    {
        result = OperationResult::ERROR_RESOURCE_NOT_FOUND;
        respMetadata.httpStatusCode = static_cast<int>(HttpStatusCodeEnum::HTTP_STATUS_400_BAD_REQUEST);
    }

   return respData;
}

}}}  // namespace dune::copy::cdm
