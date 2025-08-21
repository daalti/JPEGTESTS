DUNE_ADD_FLAVOR()
DUNE_LINK_LIBRARIES(job/cdm/JobCdmHelper
     ws/cdm/framework/types
     imaging/Jobs/PipelineOptionsConverter)
DUNE_ADD_GTEST(framework/component/TestingUtil)
