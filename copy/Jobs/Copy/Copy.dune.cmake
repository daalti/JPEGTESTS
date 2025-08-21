DUNE_ADD_INTERFACE()
    DUNE_LINK_LIBRARIES(job/JobTicket
                        job/types
                        copy/Jobs
                        copy/types
                        scan/Jobs/Scan
                        scan/Jobs/Scan/ScanPipeline
                        imaging/types
                        imaging/Resources/ImageImporter
                        print/engine/cdm
                        )

