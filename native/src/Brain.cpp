#include "Brain.h"
#include <iostream> // For std::cerr, though CoreBrain handles most errors

Brain::Brain() {}

Brain::~Brain() {}

void Brain::loadModel(const std::string& modelPath) {
    std::cout << "Brain: Attempting to load model via CoreBrain from " << modelPath << std::endl;
    if (!coreBrain.loadModel(modelPath)) {
        std::cerr << "Brain: Failed to load model through CoreBrain." << std::endl;
        // You might want to throw an exception or set an internal error flag here
    } else {
        std::cout << "Brain: Model successfully loaded via CoreBrain." << std::endl;
    }
}

void Brain::processInput(const std::string& input) {
    lastInput = input;
    std::cout << "Brain: Processing input: " << input << std::endl;
    // The actual "sending to CoreBrain" happens when generateResponse is called.
    // For now, we just store the last input.
}

std::string Brain::generateResponse() {
    if (lastInput.empty()) {
        std::cerr << "Brain: No input to generate a response from." << std::endl;
        return "Error: No input provided.";
    }

    std::cout << "Brain: Generating response from CoreBrain for input: '" << lastInput << "'" << std::endl;

    // These values should ideally be configurable or passed in
    int n_predict_tokens = 256; // Example: Generate up to 256 tokens
    int n_threads = 8;          // Example: Use 8 threads

    // This is the real call to CoreBrain's generate method
    std::string generatedText = coreBrain.generate(lastInput, n_predict_tokens, n_threads);

    if (generatedText.empty()) {
        std::cerr << "Brain: CoreBrain generated an empty response or failed." << std::endl;
        lastCoreBrainResponse = "Error: CoreBrain could not generate a response.";
    } else {
        lastCoreBrainResponse = generatedText;
        std::cout << "Brain: CoreBrain response received." << std::endl;
    }

    return lastCoreBrainResponse;
}

// Mock functions are removed as they are no longer needed.
// void Brain::mockSendToCoreBrain(const std::string& message) { ... }
// std::string Brain::mockReceiveFromCoreBrain() { ... }