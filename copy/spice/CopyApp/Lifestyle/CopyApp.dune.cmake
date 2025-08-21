DUNE_ADD_FLAVOR()
DUNE_SET_SCOPE_PROPERTY(CMAKE_INCLUDE_CURRENT_DIR ON)
    DUNE_LINK_LIBRARIES(
                        spice/core
                        )
DUNE_QT_WRAP_CPP(moc_files  ${DUNE_BASE_PATH}/copy/spice/CopyApp/Lifestyle/inc/CopyAppController.h
    ${DUNE_BASE_PATH}/copy/spice/CopyApp/Lifestyle/inc/CopyInitView.h
    ${DUNE_BASE_PATH}/copy/spice/CopyApp/Lifestyle/inc/CopyStartView.h
    )
DUNE_ADD_EXTRA_GEN_SRC(${moc_files}
                  )
