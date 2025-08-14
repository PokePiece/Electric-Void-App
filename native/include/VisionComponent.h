#pragma once
#include "Component.h"
#include <iostream>

class VisionComponent : public Component {
public:
    void initialize() override {
        std::cout << "Vision initialized\n";
    }
    void update() override {
        std::cout << "Vision update cycle\n";
    }
};