DUNE_ADD_FLAVOR()
    DUNE_SPICE_DATA_FILTER_FLAT_BUFFER_FOR(JSON ${DUNE_BASE_PATH}/copy/spice/IDCardCopyApp/Workflow/spiceData/IDCardCopySettings.json FBS ${DUNE_BASE_PATH}/spice/guiCore/pub/MenuNodes.fbs)
    DUNE_LINK_LIBRARIES(
                        spice/guiCore
                        spice/ux/workflow
                        framework/resources/configuration
                        framework/storage/path
                        walkup/spice/WalkupController
                        )
DUNE_ADD_GTEST(
            framework/component/TestingUtil
            spice/testing/environment/workflowFixtures
            ws/cdm/services/Scan
            walkup/spice/Walkup/Standard
            )
DUNE_INCLUDE_DIRECTORIES(PRIVATE ${DUNE_OUTPUT_DIRECTORY}/test/${DUNE_ITEM_NAME}/testResources/generated)
        set (TEST_RESOURCES_DIR ${DUNE_BASE_PATH}/copy/spice/IDCardCopyApp/Workflow/test/testResources)
        set (TEST_OUTPUT_DIR ${DUNE_OUTPUT_DIRECTORY}/test/${DUNE_ITEM_NAME}/testResources/generated)

        add_custom_command(
        COMMAND bash -c "${FLATC} --no-warnings -b -o ${TEST_OUTPUT_DIR} --flexbuffers ${TEST_RESOURCES_DIR}/TestSpiceDataMap.json"

        OUTPUT ${TEST_OUTPUT_DIR}/TestSpiceDataMap.bin

        DEPENDS ${TEST_RESOURCES_DIR}/TestSpiceDataMap.json
        )

        DUNE_ADD_EXTRA_GEN_SRC(${TEST_OUTPUT_DIR}/TestSpiceDataMap.bin)