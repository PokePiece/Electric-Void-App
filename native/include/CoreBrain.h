#pragma once
#include <string>
#include <vector>
#include "llama.h"
#include "llama.h"


class CoreBrain {
private:
    llama_context* ctx = nullptr;

public:
    CoreBrain() = default;
    ~CoreBrain();

    bool loadModel(const std::string& modelPath);
    std::string generate(const std::string& prompt, int n_predict = 128, int n_threads = 4);
};

