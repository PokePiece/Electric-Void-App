#pragma once

#include <QString>
#include <QProcess>
#include <string>

class VoidBrain {
public:
    VoidBrain() = default;

    void loadSystem(const std::string& configPath) {
        (void)configPath; // Stub
    }

    std::string processInput(const std::string& input) {
        QString response = callPythonScript(QString::fromStdString(input));
        return response.toStdString();
    }

private:
    QString callPythonScript(const QString& input) {
        QProcess process;
        QString pythonExecutable = "python"; // Adjust if needed (e.g., "python3")
        QString scriptPath = "./VoidAGIPlaceholder.py";

        // Arguments: pass input as a command line argument or via stdin
        QStringList arguments;
        arguments << scriptPath << input;

        process.start(pythonExecutable, arguments);
        process.waitForFinished(-1); // wait indefinitely for completion

        QString output = process.readAllStandardOutput().trimmed();
        QString error = process.readAllStandardError().trimmed();

        if (!error.isEmpty()) {
            // Handle error: for now just include it in output
            output += "\n[Python Error]: " + error;
        }

        return output;
    }
};
