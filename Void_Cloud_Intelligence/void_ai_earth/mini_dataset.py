# mini_dataset.py

from datasets import Dataset

train_data = {
    "input": [
        # --- HELLO ---
        "Hi there, how are you?",
        "What's up, buddy?",
        "Hello!",
        "Hey, how’s it going?",
        "Good to see you.",
        "Greetings, assistant.",
        "Yo.",
        "Hi friend.",
        "Hey there!",
        "Hi.",
        "Howdy!",
        "Morning!",
        "Good morning.",
        "Hi, assistant.",
        "Greetings.",
        "Hello again.",
        "What's going on?",
        "Hi Surreal.",
        "Salutations.",
        "Pleasure to meet you.",

        # --- GOODBYE ---
        "Bye for now.",
        "Talk later, friend.",
        "Catch you later.",
        "Goodbye!",
        "See you around.",
        "I'm heading out.",
        "Gotta run, bye.",
        "See ya.",
        "Later.",
        "Talk to you soon.",
        "I'm signing off.",
        "Bye assistant.",
        "Thanks, goodbye.",
        "Peace out.",
        "Logging off.",
        "That's all, bye.",
        "Closing this now.",
        "Exiting now.",
        "See you later.",
        "That's it for now.",

        # --- UI SWITCH ---
        "Switch to the settings menu.",
        "Take me to the home screen.",
        "Go back to the dashboard.",
        "Open the main menu.",
        "Show the configuration panel.",
        "Return to the previous screen.",
        "Navigate to settings.",
        "Launch the control center.",
        "Change the view to settings.",
        "I want to see the dashboard.",
        "Go to main.",
        "Can you take me to settings?",
        "Back to home screen, please.",
        "Open up preferences.",
        "Settings, now.",
        "Please show controls.",
        "Go to the UI panel.",
        "Take me back.",
        "Where’s the home screen?",
        "I want the config view.",
    ],
    "label": [
        # hello
        *["hello"] * 20,
        # goodbye
        *["goodbye"] * 20,
        # ui_switch
        *["ui_switch"] * 20,
    ]
}

dataset = Dataset.from_dict(train_data)
