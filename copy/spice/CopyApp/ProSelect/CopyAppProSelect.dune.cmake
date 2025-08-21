DUNE_ADD_FLAVOR()
    DUNE_SPICE_DATA_FILTER_FLAT_BUFFER_FOR(JSON ${DUNE_BASE_PATH}/copy/spice/CopyApp/ProSelect/spiceData/CopySettings.json FBS ${DUNE_BASE_PATH}/spice/guiCore/pub/MenuNodes.fbs)
    DUNE_LINK_LIBRARIES(
                        spice/guiCore
                        spice/ux/proSelect
                        framework/resources/configuration
                        framework/storage/path
                        )

DUNE_ADD_GTEST(
            framework/component/TestingUtil
            spice/testing/environment/proselectFixtures
            print/spice/PrintApp
            ws/cdm/services/Scan
            )
        set (TEST_RESOURCES_DIR ${DUNE_BASE_PATH}/copy/spice/CopyApp/ProSelect/test/testResources)
        set (TEST_OUTPUT_DIR ${DUNE_OUTPUT_DIRECTORY}/test/${DUNE_ITEM_NAME}/testResources/generated)

        add_custom_command(
        COMMAND bash -c "${FLATC} --no-warnings -b -o ${TEST_OUTPUT_DIR} --flexbuffers ${TEST_RESOURCES_DIR}/TestSpiceDataMap.json"

        OUTPUT ${TEST_OUTPUT_DIR}/TestSpiceDataMap.bin

        DEPENDS ${TEST_RESOURCES_DIR}/TestSpiceDataMap.json
        )

        DUNE_ADD_EXTRA_GEN_SRC(${TEST_OUTPUT_DIR}/TestSpiceDataMap.bin)
