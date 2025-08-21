DUNE_ADD_COMPONENT()
    DUNE_INCLUDE_DIRECTORIES(PRIVATE ${DUNE_BASE_PATH}/copy/Jobs/Copy/JobService/inc)
    DUNE_LINK_LIBRARIES(framework/underware/Interpreter
                        framework/component
                        framework/data/DataStore
                        framework/data/constraints
                        job/cdm/JobCdmHelper
                        job/Job
                        job/JobTicketResourceManager
                        job/JobService
                        imaging/types
                        copy/Jobs/Copy
                        copy/Jobs/Copy/CopyJobDynamicConstraintRules
                        scan/Jobs/Scan)
    DUNE_ADD_SRC_COMPONENT()
