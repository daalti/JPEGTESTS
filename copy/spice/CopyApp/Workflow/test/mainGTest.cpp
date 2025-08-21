////////////////////////////////////////////////////////////////////////////
/**
 *  @file   mainGtest.cpp
 *  @date   May 2th, 2019
 *
 *  (C) Copyright 2019 HP Development Company, L.P.
 *  All rights reserved.
 */
////////////////////////////////////////////////////////////////////////////

#include <gtest/gtest.h>

#include <QGuiApplication>
#include "QmlUtils.h"

#include "SpiceGuiFixture.h"
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

    dune::spice::guiCore::QmlUtils::registerResource(SpiceGuiGTestEnvironment::resourceDirectory + "/0x5fc863/Walkup.rcc");
    dune::spice::guiCore::QmlUtils::registerResource("/core/product/resources/WalkupController.rcc");

    qmlRegisterType(QUrl("qrc:/Walkup/ActivityTracker.qml"), "Activity", 1, 0, "ActivityTracker");
    

    // TODO - fix warnings
    SpiceGuiFixture::warningsAsErrorsProgram = false;

    return RUN_ALL_TESTS();
}
