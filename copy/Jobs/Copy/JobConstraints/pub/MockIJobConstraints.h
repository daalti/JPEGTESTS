/***************************************************************************
 * File generated automatically by dune_gmock on Tue 28 Jun 2022 08:17:21 AM CEST
 ***************************************************************************/

#ifndef MOCK_IJOBCONSTRAINTS_H
#define MOCK_IJOBCONSTRAINTS_H

#include <gmock/gmock.h>
#include "IJobConstraints.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

class MockIJobConstraints : public IJobConstraints
{
    public:
    MockIJobConstraints() {};
    virtual ~MockIJobConstraints() {};

    MOCK_METHOD2(getConstraints, std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup>(
        std::shared_ptr<ICopyJobTicket> jobTicket, dune::job::ITicketAdapter& ticketAdapter));
    MOCK_METHOD0(getFbConstraintsTableFromConfiguration, std::shared_ptr<CopyJobConstraintsFbT>());
};

}}}}  // namespace dune::copy::Jobs::Copy

#endif // MOCK_IJOBCONSTRAINTS_H
