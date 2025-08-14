#pragma once
#include <memory>
#include <string>
class Brain;

class Body {
public:
    Body();
    ~Body();

    void receiveSensorData(const std::string& data);
    void sendAction(const std::string& action);
    void linkBrain(std::shared_ptr<Brain> brain);

private:
    std::shared_ptr<Brain> brain_;
};