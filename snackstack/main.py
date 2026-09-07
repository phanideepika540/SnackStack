from __future__ import annotations

import argparse
import logging

from graph import graph
from voice import VoiceRecorder, VoiceSpeaker



# ============================================================
# Logging
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ============================================================
# Main
# ============================================================

def main():

    # ========================================================
    # Command-line arguments
    # ========================================================

    parser = argparse.ArgumentParser(
        description="SnackStack AI Assistant"
    )

    parser.add_argument(
        "--voice",
        action="store_true",
        help="Use microphone input and voice output"
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=5,
        help="Recording duration in seconds (default: 5)"
    )

    args = parser.parse_args()

    voice_mode = args.voice

    # ========================================================
    # Welcome message
    # ========================================================

    print("🍔 Welcome to SnackStack!")

    # ========================================================
    # Initialize voice components
    # ========================================================

    if voice_mode:

        print("🎤 Voice mode enabled")
        print("Say 'quit' or 'exit' to end the conversation.\n")

        recorder = VoiceRecorder()

        speaker = VoiceSpeaker(
            voice="nova",
            speed=1.0
        )

    else:

        print("⌨️ Text mode enabled")
        print("Type 'quit' or 'exit' to end the conversation.\n")

    # ========================================================
    # Conversation configuration
    # ========================================================

    # Same thread_id = same LangGraph conversation/checkpoint
    #
    # This allows SnackStack to remember previous messages
    # during the conversation.

    config = {
        "configurable": {
            "thread_id": "snackstack-user-1"
        }
    }

    # ========================================================
    # Conversation loop
    # ========================================================

    while True:

        # ====================================================
        # 1. Get user input
        # ====================================================

        if voice_mode:

            # -----------------------------------------------
            # Voice input
            # -----------------------------------------------

            print("\n🎤 Get ready...")

            # record_and_transcribe() returns:
            #
            #   (wav_path, transcript)
            #
            # We don't need the WAV path here, so "_" is used
            # for the first returned value.

            _, user_query = recorder.record_and_transcribe(
                duration=args.duration
            )

            user_query = user_query.strip()

            print(f"\n[DEBUG] Whisper heard: {user_query!r}")

            if not user_query:
                print("⚠️ I couldn't understand that. Please try again.")
                continue

            print(f"You: {user_query}")

        else:

            # -----------------------------------------------
            # Text input
            # -----------------------------------------------

            user_query = input("You: ").strip()

            if not user_query:
                continue

        # ====================================================
        # 2. Check exit command
        # ====================================================

       # Normalize only for command detection
        command = user_query.lower().strip().rstrip(".!?")

        if command in {"quit", "exit", "goodbye", "stop"}:

            goodbye = "Goodbye! See you next time."

            print(f"\nSnackStack: {goodbye}")

            if voice_mode:
                speaker.speak(goodbye)
            break
        # ====================================================
        # 3. Send request to LangGraph
        # ====================================================

        print("\n[LOG] User message received")

        try:

            result = graph.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_query
                        }
                    ],
                    "user_query": user_query,
                },
                config=config
            )

        except Exception:

            logging.exception(
                "Graph execution failed"
            )

            error_message = (
                "Sorry, something went wrong "
                "while processing your request."
            )

            print(
                f"SnackStack: {error_message}"
            )

            if voice_mode:
                speaker.speak(error_message)

            continue

        # ====================================================
        # 4. Get latest assistant response
        # ====================================================

        if not result.get("messages"):

            error_message = (
                "Sorry, I didn't receive a response."
            )

            print(
                f"SnackStack: {error_message}"
            )

            if voice_mode:
                speaker.speak(error_message)

            continue

        last_message = result["messages"][-1]

        response_text = str(last_message.content)

        print(
            f"\nSnackStack: {response_text}"
        )

        # ====================================================
        # 5. Text-to-Speech
        # ====================================================

        if voice_mode:

            try:

                audio_path = speaker.speak(
                    response_text
                )

                if audio_path:

                    print(
                        f"🔊 Response played: {audio_path}"
                    )

                else:

                    print(
                        "⚠️ TTS did not return an audio file."
                    )

            except Exception:

                logging.exception(
                    "TTS playback failed"
                )

                print(
                    "⚠️ I generated a response, "
                    "but couldn't play the audio."
                )


# ============================================================
# Application entry point
# ============================================================

if __name__ == "__main__":
    main()