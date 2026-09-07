from voice import VoiceSpeaker

speaker = VoiceSpeaker(
    voice="nova",
    speed=1.0
)

print("Generating speech...")

path = speaker.speak(
    "Hello! This is a test of SnackStack voice output."
)

print("Audio file:", path)