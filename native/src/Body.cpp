#include "Body.h"
#include "Brain.h"
#include <iostream>

Body::Body() {}
Body::~Body() {}

void Body::linkBrain(std::shared_ptr<Brain> brain) {
    brain_ = brain;
}

void Body::receiveSensorData(const std::string& data) {
    std::cout << "Body received sensor data: " << data << std::endl;
    if (brain_) brain_->processInput(data);
}

void Body::sendAction(const std::string& action) {
    std::cout << "Body executes action: " << action << std::endl;
}  