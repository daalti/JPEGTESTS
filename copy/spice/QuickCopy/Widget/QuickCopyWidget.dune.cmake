DUNE_ADD_FLAVOR()
    DUNE_LINK_LIBRARIES(framework/resources/configuration
                        spice/ux/workflow
                        framework/storage/path
                        spice/widget/WidgetService)


    DUNE_ADD_GTEST(framework/component/TestingUtil
                    spice/testing/environment/workflowFixtures)

    
set (TEST_RESOURCES_DIR ${DUNE_BASE_PATH}/copy/spice/QuickCopy/Widget/test/testResources)
set (TEST_OUTPUT_DIR ${DUNE_OUTPUT_DIRECTORY}/test/${DUNE_ITEM_NAME}/testResources/generated)

add_custom_command(
    COMMAND bash -c "${FLATC} --no-warnings -b -o ${TEST_OUTPUT_DIR} ${TEST_RESOURCES_DIR}/QuickCopyWidgetConfig.fbs ${TEST_RESOURCES_DIR}/QuickCopyWidgetTestData.json"

    OUTPUT ${TEST_OUTPUT_DIR}/QuickCopyWidgetTestData.bin
    DEPENDS ${TEST_RESOURCES_DIR}/QuickCopyWidgetTestData.json
)

DUNE_ADD_EXTRA_GEN_SRC(${TEST_OUTPUT_DIR}/QuickCopyWidgetTestData.bin)
