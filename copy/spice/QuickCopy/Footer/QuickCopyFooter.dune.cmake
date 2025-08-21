DUNE_ADD_FLAVOR()
    DUNE_LINK_LIBRARIES(framework/resources/configuration
                        spice/guiCore
                        spice/ux/workflow)
    DUNE_ADD_GTEST(framework/component/TestingUtil
                    spice/testing/environment/workflowFixtures)

