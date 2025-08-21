/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_EXTENSION_H
#define DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_EXTENSION_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesExtension.h
 * @date   Mon, 11 Jul 2022 11:20:06 +0200
 * @brief  Component used to manage the Dynamic Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "InterpreterExtension.h"

namespace dune { namespace copy { namespace Jobs { namespace Copy {

/**
 * Interpreter registration broker singleton for CopyJobDynamicConstraintRulesUw.
 */
class CopyJobDynamicConstraintRulesExtension: public dune::framework::underware::InterpreterExtension
{
public:

    /**
     * Get the singleton instance. The instance is created only the first time
     * this class method is called.
     *
     * @return the singleton instance.
     */
    static CopyJobDynamicConstraintRulesExtension * instance();

    /**
     * @name InterpreterExtension methods.
     * @{
     */

    void init(InterpreterExtension::Language language, void * param);

    /**
     * @}
     */

private:

    /*
     * Hide constructor and destructor.
     */
    CopyJobDynamicConstraintRulesExtension();
    ~CopyJobDynamicConstraintRulesExtension() = default;

    /*
     * remove copy and move constructors and assignments
     */
    CopyJobDynamicConstraintRulesExtension(const CopyJobDynamicConstraintRulesExtension & ext) = delete;
    CopyJobDynamicConstraintRulesExtension & operator=(const CopyJobDynamicConstraintRulesExtension & ext) = delete;
    CopyJobDynamicConstraintRulesExtension(CopyJobDynamicConstraintRulesExtension && ext) = delete;
    CopyJobDynamicConstraintRulesExtension & operator=(CopyJobDynamicConstraintRulesExtension && ext) = delete;
};

}}}}  // namespace dune::copy::Jobs::Copy


#endif  // DUNE_COPY_JOBS_COPY_COPY_JOB_DYNAMIC_CONSTRAINT_RULES_EXTENSION_H

