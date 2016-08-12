import os
import sys

# Add parent dir to PYTHONPATH to make imports more convenient.
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)

from conversation import responder


def main():
    print("Facebook Chat Bot [local interactive mode]")
    print("Press Ctrl-C to exit.")
    print()

    try:
        while True:
            incoming_message_text = input("Enter a message: ")
            event = {
                "sender": {
                    "id": 42
                },
                "message": {
                    "text": incoming_message_text
                }
            }
            print("Bot response:   ", responder.get_reply(event))
            print("-" * 50)

    except KeyboardInterrupt:
        print()
        print("Bye.")
        sys.exit(0)


if __name__ == "__main__":
    main()
