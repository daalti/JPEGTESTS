/* -*- c++ -*- */

///////////////////////////////////////////////////////////////////////////////
/**
 * @file   CopyJobDynamicConstraintRulesLargeFormatGtestMain.cpp
 * @date   Tue, 11 Oct 2022 11:20:06 +0200
 * @brief  Component used to manage the Dynamic Copy Job Constraints
 *
 * (C) Copyright 2022 HP Development Company, L.P.
 * All rights reserved.
 */
///////////////////////////////////////////////////////////////////////////////

#include "CopyJobDynamicConstraintRulesLargeFormat.h"

#include "gtest/gtest.h"
#include "gmock/gmock.h"
#include "TestSystemServices.h"
#include "GTestConfigHelper.h"

using GTestConfigHelper = dune::framework::core::gtest::GTestConfigHelper;

GTestConfigHelper testConfigOptions_;

int main(int argc, char  *argv[])
{
    // run google tests
    //
    std::cout << "Main:  " << argv[0] << std::endl;

    testConfigOptions_.parse(argc, argv);
    testConfigOptions_.Configure();

    ::testing::FLAGS_gmock_catch_leaked_mocks = true;
    ::testing::FLAGS_gmock_verbose = "error";

    ::testing::InitGoogleTest(&argc, argv);

    return RUN_ALL_TESTS();
}