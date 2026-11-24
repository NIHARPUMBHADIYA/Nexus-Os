cmake_minimum_required(VERSION 3.28)
project(nexus-devhub VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 6.8 REQUIRED COMPONENTS Core Gui Quick Qml)

qt_standard_project_setup()

qt_add_executable(nexus-devhub
    src/main.cpp
)

qt_add_qml_module(nexus-devhub
    URI Nexus.DevHub
    VERSION 1.0
    QML_FILES
        src/qml/Main.qml
)

target_link_libraries(nexus-devhub PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Quick
    Qt6::Qml
)
