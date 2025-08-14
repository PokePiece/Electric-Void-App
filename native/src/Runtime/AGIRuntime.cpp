#include "AGIRuntime.hpp"
#include "SensorManager.hpp"
#include "BrainManager.hpp"
#include "GoalManager.hpp"
#include "ActionManager.hpp"
#include "MemoryManager.hpp"

AGIRuntime::AGIRuntime(QObject* parent)
    : QObject(parent), cycleTimer(new QTimer(this)), running(false) {
    connect(cycleTimer, &QTimer::timeout, this, &AGIRuntime::cognitiveCycle);
}

void AGIRuntime::start() {
    running = true;
    cycleTimer->start(100); // 100ms cycle
}

void AGIRuntime::stop() {
    running = false;
    cycleTimer->stop();
}

void AGIRuntime::cognitiveCycle() {
    SensorManager::collectInputs();
    BrainManager::processInputs(); // passive/unconscious
    GoalManager::evaluateGoals();
    ActionManager::decideAndAct();
    MemoryManager::storeEpisode();
}
