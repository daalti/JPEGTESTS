DUNE_ADD_FLAVOR()
    DUNE_LINK_LIBRARIES(localization/LocaleProvider
                        localization/StringIds)
    DUNE_ADD_GTEST(framework/component/TestingUtil)
