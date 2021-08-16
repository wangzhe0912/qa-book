add_library(MathFunctions mysqrt.cxx)

# state that anybody linking to us needs to include the current source dir
# to find MathFunctions.h, while we don't.
target_include_directories(MathFunctions
          INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
          )

# install
install(TARGETS MathFunctions DESTINATION lib)  # 对应lib
install(FILES MathFunctions.h DESTINATION include)  # 对应include
