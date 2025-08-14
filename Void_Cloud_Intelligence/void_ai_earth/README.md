# Void Intelligence Earth

## AI Python Assistant

This project implements a basic AI assistant using the **GPT-2** model to generate responses to user input. The model is hosted locally and interacts with users in a chat-like interface, allowing for flexible responses based on the given **tone** and **style** profile.

## Features

- **Interactive Chat**: A text-based interface where the user can ask questions and receive AI-generated responses.
    
- **Profile Customization**: Adjust the assistant's tone and style for different interactions.
    
- **Customizable**: Modify the AI’s responses by adjusting parameters like temperature, max tokens, and repetition penalties.
    

## Requirements

- **Python 3.x**: Ensure you have Python 3.x installed on your system.
    
- **Dependencies**: Install required libraries via `pip` (listed below).
    

### Dependencies

- **transformers**: For loading and using GPT-2 models.
    
- **torch**: PyTorch is used for running the model.
    
- **CUDA (Optional)**: For GPU acceleration (if you have an NVIDIA GPU and want to use it).
    

To install the dependencies, run:

bash

CopyEdit

`pip install transformers torch`

If you plan to use GPU acceleration, you’ll need the proper **CUDA** setup.

## Usage

### Running the Assistant

1.  **Clone or Download the Project** to your local machine.
    
2.  Navigate to the project directory in your terminal/command line.
    
3.  Run the Python script to launch the AI assistant:
    

bash

CopyEdit

`python aichat.py`

4.  You’ll be prompted with a chat interface where you can interact with the assistant. Type your query and press Enter to receive a response.
    
5.  Type `quit` to exit the program.
    

### Example

bash

CopyEdit

`You: How does the internet work?AI: The internet operates by connecting millions of computers across the globe using standardized protocols, allowing for data to be transferred in the form of packets.`

### Parameters

You can adjust the **tone** and **style** of the assistant by modifying the profile inside the `generate()` function:

python

CopyEdit

`profile = {"tone": "realistic", "style": "technical"}`

## Development

### Adding More Profiles

To make the assistant even more customizable, you can expand the `profile` parameter to include additional tones and styles. Simply modify the `generate()` function's profile section to suit your needs.

### Example of More Profiles

python

CopyEdit

`profile = {"tone": "casual", "style": "funny"}`

## License

This project is open-source and available under the MIT License.

* * *

Feel free to modify and expand it as your project evolves!
