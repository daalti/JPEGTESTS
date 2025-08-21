#ifndef DUNE_COPY_JOBS_COPY_MOCK_COPY_TICKET_CONVERTER_H
#define DUNE_COPY_JOBS_COPY_MOCK_COPY_TICKET_CONVERTER_H

#include "ICopyTicketConverter.h"
#include <gmock/gmock.h>

namespace dune { namespace copy { namespace Jobs { namespace Copy {

class MockICopyJobTicketConverter : public ICopyTicketConverter {
public:
MockICopyJobTicketConverter(){}
virtual ~MockICopyJobTicketConverter(){}

MOCK_METHOD2(convert,
        dune::framework::data::conversion::ConversionResult(const dune::framework::data::conversion::DataDescriptor&, std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>&)
    );
};

}}}}  // namespace dune::copy::Jobs::Copy

#endif  // DUNE_COPY_JOBS_COPY_MOCK_COPY_TICKET_CONVERTER_H