import subprocess
import os

# --- Step 1: Define the model name and output directory ---
model_name = "EleutherAI/pythia-410m"
output_dir = "./pythia-410m-onnx"

# --- Use the absolute path to the optimum-cli executable ---
# NOTE: You MUST replace the path below with the exact path on your system.
OPTIMUM_CLI_PATH = r"C:\Users\Dillon\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts\optimum-cli.exe"

# --- Step 2: Use the optimum-cli command to export the model ---
print(f"--- Exporting model to ONNX using optimum-cli: {model_name} ---")

command = [
    OPTIMUM_CLI_PATH, # Use the full path here
    "export",
    "onnx",
    "--model", model_name,
    "--task", "causal-lm",
    output_dir
]

try:
    subprocess.run(command, check=True)
    print(f"Model exported successfully to: {output_dir}")

    onnx_file_path = os.path.join(output_dir, "model.onnx")
    if os.path.exists(onnx_file_path):
        print(f"ONNX model file found at: {onnx_file_path}")
    else:
        print("Error: The model.onnx file was not created. Check for previous error messages.")

except subprocess.CalledProcessError as e:
    print(f"An error occurred during ONNX export: {e}")
    print("Please check the output above for details from the optimum-cli command.")
except FileNotFoundError:
    print("Error: The specified path for 'optimum-cli' was not found. Please double-check the path.")

