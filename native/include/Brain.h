#ifndef BRAIN_H
#define BRAIN_H

#include <string>
#include <memory> // For std::unique_ptr or std::shared_ptr if you choose that
#include "CoreBrain.h" // Include the CoreBrain header

class Brain {
public:
    Brain();
    ~Brain();

    void loadModel(const std::string& modelPath);
    void processInput(const std::string& input);
    std::string generateResponse();

private:
    CoreBrain coreBrain; // An instance of CoreBrain
    std::string lastInput;
    std::string lastCoreBrainResponse;

    // Remove mock functions as they won't be needed
    // void mockSendToCoreBrain(const std::string& message);
    // std::string mockReceiveFromCoreBrain();
};

#endif // BRAIN_H