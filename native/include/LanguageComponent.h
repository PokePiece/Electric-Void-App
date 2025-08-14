#pragma once
#include "Component.h"
#include <string>

class LanguageComponent : public Component {
public:
    void initialize() override;
    void update() override;

    std::string processText(const std::string& input);
private:
    // Placeholder for NLP model or external API call
};
