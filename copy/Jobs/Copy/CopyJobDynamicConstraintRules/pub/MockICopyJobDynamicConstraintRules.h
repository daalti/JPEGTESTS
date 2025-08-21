/***************************************************************************
 * File generated automatically by dune_gmock on Thu 07 Jul 2022 01:56:47 PM CEST
 ***************************************************************************/

#ifndef MOCK_ICOPYJOBDYNAMICCONSTRAINTRULES_H
#define MOCK_ICOPYJOBDYNAMICCONSTRAINTRULES_H

#include <gmock/gmock.h>
#include "ICopyJobDynamicConstraintRules.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

class MockICopyJobDynamicConstraintRules : public ICopyJobDynamicConstraintRules
{
public:
    MockICopyJobDynamicConstraintRules() {};
    virtual ~MockICopyJobDynamicConstraintRules() {};

    MOCK_METHOD3(getDynamicConstraints, std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup>(std::shared_ptr<ICopyJobTicket> jobTicket, 
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> staticConstraintsGroup, 
        const std::shared_ptr<JobTicketTable>& updatedJobTicketTable));
    MOCK_METHOD4(checkAndApplyForceSets, bool(const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, 
        std::shared_ptr<ICopyJobTicket> ticket, 
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> currentConstraintsGroup,
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> staticConstraintsGroup));
    MOCK_METHOD2(updateWithJobDynamicConstraints, void(std::shared_ptr<ICopyJobTicket> jobTicket, 
        std::shared_ptr<dune::framework::data::constraints::ConstraintsGroup> constraintsGroup));

};

}}}}  // namespace dune::copy::Jobs::Copy

#endif // MOCK_ICOPYJOBDYNAMICCONSTRAINTRULES_H
