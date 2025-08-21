////////////////////////////////////////////////////////////////////////////
/**
 *  @file   mainGtest.cpp
 *  @date   18th Feb, 2020
 *  @author Hector Sanchez Gonzalez (hector.sanchez-gonzalez@hp.com)
 *
 *  (C) Copyright 2019 HP Development Company, L.P.
 *  All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////

#include <gtest/gtest.h>

#include <QGuiApplication>
#include "QmlUtils.h"

#include "SpiceProSelectFixture.h"
#include "environmentGui.h"

using namespace dune::spice::testing::environment;

/**
 * @brief Google test main function
 *
 * @param argc
 * @param argv
 * @return int
 */
int main(int argc, char *argv[])
{
    ::testing::InitGoogleTest(&argc, argv);
    ::testing::AddGlobalTestEnvironment(new SpiceGuiGTestEnvironment());

    

    // TODO - fix warnings
    SpiceGuiFixture::warningsAsErrorsProgram = false;

    return RUN_ALL_TESTS();
}
