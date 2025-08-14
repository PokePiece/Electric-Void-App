import sys

def main():
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        # Just echo back for now
        print(f"Void AGI stub response to: {user_input}")
    else:
        print("No input provided.")

if __name__ == "__main__":
    main()
