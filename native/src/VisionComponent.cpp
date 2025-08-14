#pragma once
#include "Component.h"
#include <string>

class VisionComponent : public Component {
public:
    void initialize() override;
    void update() override;

    void processImage(const std::string& imagePath);
private:
    // Placeholder for vision model or logic
};
