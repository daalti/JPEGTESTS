/***************************************************************************
 * File generated automatically by dune_gmock on Thu 29 Sep 2022 03:02:19 PM CEST
 ***************************************************************************/

#ifndef MOCK_ICOPYPIPELINEBUILDERADAPTER_H
#define MOCK_ICOPYPIPELINEBUILDERADAPTER_H

#include <gmock/gmock.h>
#include "ICopyPipelineBuilderAdapter.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

class MockICopyPipelineBuilderAdapter: public ICopyPipelineBuilderAdapter
{
public:
    MOCK_METHOD0(isPreScanJob, bool());
    MOCK_METHOD0(getDefaultMediaSize, dune::imaging::types::MediaSizeId());
    MOCK_METHOD0(getPrescannedWidth, uint32_t());
    MOCK_METHOD0(getPrescannedHeight, uint32_t());
    MOCK_METHOD0(getPrePrintConfiguration, ICopyPipelineBuilderAdapter::Product());
    MOCK_METHOD0(getSegmentType, dune::job::SegmentType());
    MOCK_METHOD0(getMaxLengthConfig, ICopyPipelineBuilderAdapter::MaxLengthConfig());
};

}}}}

#endif // MOCK_ICOPYPIPELINEBUILDERADAPTER_H
