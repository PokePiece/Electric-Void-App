#ifndef AGIRUNTIME_HPP
#define AGIRUNTIME_HPP

#include <QObject>
#include <QTimer>

class AGIRuntime : public QObject {
    Q_OBJECT

public:
    explicit AGIRuntime(QObject* parent = nullptr);
    void start();
    void stop();

private slots:
    void cognitiveCycle();

private:
    QTimer* cycleTimer;
    bool running;
};

#endif // AGIRUNTIME_HPP
