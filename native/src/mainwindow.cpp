#include "mainwindow.h"
#include <QPushButton>
#include <QVBoxLayout>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    // Create widgets manually
    QWidget *central = new QWidget(this);
    QVBoxLayout *layout = new QVBoxLayout(central);

    QPushButton *button = new QPushButton("Click me", central);
    layout->addWidget(button);

    setCentralWidget(central);
}

MainWindow::~MainWindow() = default;  // no Ui pointer to delete

