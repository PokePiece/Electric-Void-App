cmake_minimum_required(VERSION 3.16)
project(Human_AGI_System VERSION 0.1 LANGUAGES CXX)


set(CMAKE_AUTOUIC_SEARCH_PATHS ${CMAKE_SOURCE_DIR}/src)
set(CMAKE_AUTOUIC_SEARCH_PATHS "${CMAKE_SOURCE_DIR}/src")
 set(CMAKE_AUTOMOC ON)


set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
  
set(CMAKE_CXX_STANDARD 17) 
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(LLAMA_CURL OFF CACHE BOOL "Disable CURL support")

find_package(Qt6 COMPONENTS Widgets REQUIRED)

add_subdirectory(llama.cpp)


# The rest of your code...I d

# Your app source files
set(APP_SOURCES
    src/main.cpp
    src/mainwindow.cpp
    src/mainwindow.ui
    include/mainwindow.h  # <-- ADD THIS LINE
    src/Body.cpp
    src/Brain.cpp
    src/LanguageComponent.cpp
    src/VisionComponent.cpp
    src/VoidBrain.cpp
    include/CoreBrain.h
    src/CoreBrain.cpp
)

# Add main executable
qt_add_executable(Human_AGI
    ${APP_SOURCES}
)

# Link Qt and llama
target_link_libraries(Human_AGI PRIVATE
    Qt6::Widgets
    llama
    ws2_32
)

# Optional: include directories
target_include_directories(Human_AGI PRIVATE
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_SOURCE_DIR}/include
    $<TARGET_PROPERTY:Human_AGI,INTERFACE_INCLUDE_DIRECTORIES>
    ${CMAKE_BINARY_DIR}  # Add this line: build dir includes generated ui files
)

# Optional: copy P ython scripts to output dir
set(PYTHON_SCRIPTS
    scripts/VoidAGI.py
    scripts/VoidAGIPlaceholder.py
    scripts/prompts.py
)

foreach(script ${PYTHON_SCRIPTS})
    configure_file(${script} "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/scripts/${script}" COPYONLY)
endforeach()


# Install
include(GNUInstallDirs)
install(TARGETS Human_AGI
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

# Finalize for Qt 6
if(QT_VERSION_MAJOR EQUAL 6)
    qt_finalize_executable(Human_AGI)
endif()
