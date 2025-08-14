#include <QApplication>
#include <QMainWindow>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGroupBox>
#include <QSpacerItem>
#include <QStatusBar>
#include <QFont>
#include <memory>

#include "Brain.h"
#include "Body.h"
#include "VisionComponent.h"
#include "LanguageComponent.h"
#include "VoidBrain.h"
#include "llama.h"
//#include "AGIRuntime.hpp"

int main(int argc, char *argv[])
{

    llama_backend_init(true); 


    QApplication app(argc, argv);

    //AGIRuntime *runtime = new AGIRuntime();
    //runtime->start();

    std::shared_ptr<Brain> brain = std::make_shared<Brain>();
    VoidBrain voidBrain;

    Body body;
    body.linkBrain(brain);

    //model path error
    brain->loadModel("../llama.cpp/models/mistral-7b-instruct-v0.1.Q4_K_M.gguf");
    voidBrain.loadSystem("/path/to/config");

    // Setup main window
    QMainWindow window;
    window.setWindowTitle("Human AGI Control Panel");

    QWidget *centralWidget = new QWidget(&window);

    QVBoxLayout *outerLayout = new QVBoxLayout(centralWidget);

    // Spacer at top
    outerLayout->addStretch(1);

    // Container widget with your existing layout
    QWidget *containerWidget = new QWidget;
    QVBoxLayout *mainLayout = new QVBoxLayout(containerWidget);

    // === AI Output Section ===
    QGroupBox *outputGroup = new QGroupBox("AI Response");
    QVBoxLayout *outputLayout = new QVBoxLayout(outputGroup);

    QLabel *responseLabel = new QLabel("Awaiting input...");
    responseLabel->setWordWrap(true);
    QFont responseFont;
    responseFont.setPointSize(12);
    responseFont.setBold(true);
    responseLabel->setFont(responseFont);
    responseLabel->setAlignment(Qt::AlignTop | Qt::AlignLeft);
    outputLayout->addWidget(responseLabel);

    // === User Input Section ===
    QGroupBox *inputGroup = new QGroupBox("User Input");
    QHBoxLayout *inputLayout = new QHBoxLayout(inputGroup);

    QLineEdit *inputField = new QLineEdit;
    inputField->setPlaceholderText("Type a command or query...");
    QPushButton *submitButton = new QPushButton("Submit");

    inputLayout->addWidget(inputField, 3);
    inputLayout->addWidget(submitButton, 1);

    // Add groups to main layout
    mainLayout->addWidget(outputGroup);
    mainLayout->addWidget(inputGroup);

    // Spacer inside container widget for vertical centering
    mainLayout->addSpacerItem(new QSpacerItem(0, 20, QSizePolicy::Minimum, QSizePolicy::Expanding));

    outerLayout->addWidget(containerWidget, 0, Qt::AlignCenter);

    // Spacer at bottom
    outerLayout->addStretch(1);

    // Set central widget and status bar
    window.setCentralWidget(centralWidget);
    QStatusBar *statusBar = window.statusBar();
    statusBar->showMessage("Model loaded. Ready for input.");

    // Logic connection
    QObject::connect(submitButton, &QPushButton::clicked, [&]()
                     {
        QString inputText = inputField->text().trimmed();
        if (inputText.isEmpty()) {
            statusBar->showMessage("Input is empty.");
            return;
        }

        std::string userInput = inputText.toStdString();

        // 1) Send input to local Brain
        brain->processInput(userInput);
        std::string localBrainResponse = brain->generateResponse();

        // 2) Send local brain response to VoidBrain (cloud AI)
        std::string voidResponse = voidBrain.processInput(localBrainResponse);

        // 3) Display VoidBrain output in UI
        responseLabel->setText(QString::fromStdString(voidResponse));
        statusBar->showMessage("VoidBrain response generated.");
        inputField->clear(); });

    window.resize(800, 500);
    window.show();


    QObject::connect(&app, &QApplication::aboutToQuit, [](){
        llama_backend_free();
        std::cout << "Llama backend freed." << std::endl;
    });



    return app.exec();
}
