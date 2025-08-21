DUNE_ADD_COMPONENT()
    DUNE_INCLUDE_DIRECTORIES(PRIVATE ${DUNE_BASE_PATH}/copy/Jobs/Copy/JobService/inc)
    DUNE_LINK_LIBRARIES(framework/component 
                        framework/underware/Interpreter
                        framework/data/DataStore
                        framework/data/constraints
                        job/cdm/JobCdmHelper
                        job/Job
                        job/JobService
                        imaging/types
                        imaging/MediaLib
                        copy/cdm/CopyAdapter
                        copy/Jobs/Copy
                        scan/Jobs/Scan
                        scan/ScanConstraints
                        imaging/directoryFilter
                        )
    DUNE_ADD_SRC_COMPONENT()
