/***************************************************************************
 * File generated automatically by dune_gmock
 ***************************************************************************/

#ifndef MOCK_ICOPYPAGETICKET_H
#define MOCK_ICOPYPAGETICKET_H

#include <gmock/gmock.h>

#include "ICopyPageTicket.h"


namespace dune { namespace copy { namespace Jobs { namespace Copy {

class MockICopyPageTicket : public ICopyPageTicket
{
  public:
    MOCK_CONST_METHOD0(getPageId, dune::framework::core::Uuid());
    MOCK_CONST_METHOD0(getPageNumber, uint32_t());
    MOCK_METHOD1(setPageNumber, void(uint32_t pageNumber));
    MOCK_METHOD0(getPageTicketChanged, dune::job::PageTicketEvent&());
    MOCK_METHOD1(setPageId, void(const dune::framework::core::Uuid& pageId));
    MOCK_CONST_METHOD0(getMediaSize, dune::imaging::types::MediaSizeId());
    MOCK_METHOD1(setMediaSize, void(dune::imaging::types::MediaSizeId mediaSize));
    MOCK_CONST_METHOD0(getPreviewProgress, uint8_t());
    MOCK_CONST_METHOD0(getHighResPreview, dune::job::IPageTicket::Preview());
    MOCK_METHOD1(setHighResPreview, void(const dune::job::IPageTicket::Preview& highResPreview));
    MOCK_CONST_METHOD0(getLowResPreview, dune::job::IPageTicket::Preview());
    MOCK_METHOD1(setLowResPreview, void(const dune::job::IPageTicket::Preview& lowResPreview));
    MOCK_CONST_METHOD0(hasLayer, bool());
    MOCK_CONST_METHOD0(getLayersIds, std::vector<dune::job::LayerId>());
    MOCK_CONST_METHOD1(getLayer, dune::job::IPageTicket::Layer(dune::job::LayerId layerId));
    MOCK_METHOD1(setLayer, void(const dune::job::IPageTicket::Layer& layer));
    MOCK_CONST_METHOD2(getStoredImage, bool(const dune::imaging::types::InstanceType&,
                                            dune::framework::data::SerializedDataBufferPtr&));
    MOCK_METHOD2(addStoredImage, bool(const dune::imaging::types::InstanceType&,
                                      const dune::framework::data::SerializedDataBufferPtr&));
    MOCK_CONST_METHOD0(serializeBase, std::unique_ptr<dune::job::PageTicketFbT>());
    MOCK_METHOD1(deserializeBase, void(const dune::job::PageTicketFbT& fbt));
    MOCK_CONST_METHOD1(getIntent, std::shared_ptr<dune::job::IIntent>(dune::job::IntentType intentType));
    MOCK_METHOD0(getHandler, std::shared_ptr<dune::job::IPageTicketHandler>());
    MOCK_METHOD1(setPrintIntent, void(std::shared_ptr<dune::print::engine::PrintIntents> printIntent));
    MOCK_METHOD1(setImagingIntent, void(std::shared_ptr<dune::imaging::types::IImagingIntent> imagingIntent));
    MOCK_METHOD1(setScanIntent, void(std::shared_ptr<dune::scan::types::ScanTicketStruct> scanPageIntent));
    MOCK_METHOD(void, setPageStorePath, (std::string), (override));
    MOCK_METHOD(std::string, getPageStorePath, (), (const, override));
    MOCK_METHOD(void, setMemoryFileHandle, (uint32_t), (override));
    MOCK_METHOD(uint32_t, getMemoryFileHandle, (), (const, override));
    MOCK_CONST_METHOD0(getPageIntent, std::shared_ptr<dune::job::CopyPageIntent>());
    MOCK_CONST_METHOD0(getPageResult, std::shared_ptr<dune::job::CopyPageResult>());
};

}}}}  // namespace dune::copy::Jobs

#endif  // MOCK_ICOPYPAGETICKET_H
