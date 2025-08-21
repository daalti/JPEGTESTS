DUNE_ADD_FLAVOR()

    DUNE_LINK_LIBRARIES(
                        spice/guiCore
                        spice/ux/workflow
                        framework/resources/configuration
                        framework/storage/path
                        spice/lottie
                        admin/spice/QuickSetsApp
                        walkup/spice/WalkupController
                        )
DUNE_INCLUDE_DIRECTORIES(PRIVATE ${DUNE_BASE_PATH}/print/spice/Preview/Standard/inc)
DUNE_ADD_GTEST(
            framework/component/TestingUtil
            spice/testing/environment/workflowFixtures
            ws/cdm/services/Scan
            print/spice/Preview/Standard
            admin/spice/QuickSetsApp
            walkup/spice/WalkupController
            )
DUNE_INCLUDE_DIRECTORIES(PRIVATE ${DUNE_OUTPUT_DIRECTORY}/test/${DUNE_ITEM_NAME}/testResources/generated)

set (TEST_RESOURCES_DIR ${DUNE_BASE_PATH}/copy/spice/CopyApp/Workflow/test/testResources)
set (TEST_OUTPUT_DIR ${DUNE_OUTPUT_DIRECTORY}/test/${DUNE_ITEM_NAME}/testResources/generated)

add_custom_command(
    COMMAND bash -c "${FLATC} --no-warnings -b -o ${TEST_OUTPUT_DIR} --flexbuffers ${TEST_RESOURCES_DIR}/TestSpiceDataMap.json"

    OUTPUT ${TEST_OUTPUT_DIR}/TestSpiceDataMap.bin

    DEPENDS ${TEST_RESOURCES_DIR}/TestSpiceDataMap.json
)

DUNE_ADD_EXTRA_GEN_SRC(${TEST_OUTPUT_DIR}/TestSpiceDataMap.bin)