////////////////////////////////////////////////////////////////////////////
/**
 *  @file   mainGtest.cpp
 *  @date   5th Apr, 2021
 *  @author Shubham Khandelwal
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

    qmlRegisterType(QUrl("qrc:/WalkupControllerMain.qml"), "Walkup", 1, 0, "WalkupController");
    

    // TODO - fix warnings
    SpiceGuiFixture::warningsAsErrorsProgram = false;

    return RUN_ALL_TESTS();
}
