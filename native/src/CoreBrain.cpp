#include "CoreBrain.h"
#include <iostream>

// Stub context pointer
struct llama_context {};

CoreBrain::~CoreBrain()
{
    // No real llama_free, just nullify ctx
    ctx = nullptr;
}

bool CoreBrain::loadModel(const std::string &modelPath)
{
    (void)modelPath;  // suppress unused warning
    // Fake successful load: create dummy context
    ctx = new llama_context();
    std::cout << "Model loaded (stub)" << std::endl;
    return true;
}

std::string CoreBrain::generate(const std::string &prompt, int n_predict, int n_threads)
{
    (void)n_predict; (void)n_threads;  // suppress unused warnings
    if (!ctx)
        return "";

    // Stub: just echo prompt
    return prompt;
}
