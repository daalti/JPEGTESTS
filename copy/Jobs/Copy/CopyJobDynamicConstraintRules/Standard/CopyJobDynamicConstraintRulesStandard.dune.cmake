DUNE_ADD_FLAVOR()
DUNE_INCLUDE_DIRECTORIES(PRIVATE ${DUNE_BASE_PATH}/copy/Jobs/Copy/JobService/inc)
DUNE_LINK_LIBRARIES(framework/component 
                    framework/underware/Interpreter
                    framework/data/DataStore
                    framework/data/constraints
                    job/cdm/JobCdmHelper
                    job/Job
                    job/JobService
                    imaging/types
                    copy/cdm/CopyAdapter
                    copy/Jobs/Copy
                    copy/Jobs/Copy/JobService
                    print/engine/constraints/MediaConstraints
                    scan/Jobs/Scan
                    imaging/ColorAccessControl)
    DUNE_ADD_GTEST(framework/component/TestingUtil)
