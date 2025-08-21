/* -*- c++ -*- */

#ifndef DUNE_COPY_JOBS_COPY_JOB_CONSTRAINTS_UW_H
#define DUNE_COPY_JOBS_COPY_JOB_CONSTRAINTS_UW_H

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   JobConstraintsUw.h
 * @date   Tue, 05 Jul 2022 08:29:10 +0200
 * @brief  Component used to manage the Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

namespace dune { namespace copy { namespace Jobs { namespace Copy {
/**
 * @brief Interface exported to interpreters, also known as "underware
 * interface".
 */
class JobConstraintsUw
{
public:

    /**
     * Destructor.
     */
    virtual ~JobConstraintsUw() { }

    // @todo add pure virtual methods of the interface here.
};

}}}}  // namespace dune::copy::Jobs::Copy


#endif  // DUNE_COPY_JOBS_COPY_JOB_CONSTRAINTS_UW_H

