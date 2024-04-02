import requests
from transformers import pipeline
from pydub import AudioSegment
import os


def download_and_convert_audio(url):
    # Determine the filename and format
    filename = url.split("/")[-1]
    file_format = filename.split(".")[-1]
    temp_path = f"./data/temp.{file_format}"
    final_path = f"./data/{filename}"

    # Supported formats
    supported_formats = ["mp3", "wav", "flac"]

    # Create the data directory if it doesn't exist
    if not os.path.exists("./data"):
        os.makedirs("./data")

    # Download the audio file
    response = requests.get(url)
    with open(temp_path, "wb") as audio_file:
        audio_file.write(response.content)

    # Convert if not in supported formats
    if file_format not in supported_formats:
        audio = AudioSegment.from_file(temp_path)
        final_path = final_path.replace(
            file_format, "mp3"
        )  # Change the extension to .mp3
        audio.export(final_path, format="mp3")
        os.remove(temp_path)  # Remove the temporary file
    else:
        # If already in a supported format, just rename the temp file
        os.rename(temp_path, final_path)

    print(f"File saved to {final_path}")

    return final_path


def transcribe(file_path: str) -> str:
    # Initialize the Whisper model pipeline
    whisper_pipeline = pipeline(
        model="openai/whisper-small",
        task="automatic-speech-recognition",
    )

    # Perform transcription
    try:
        # Apply Whisper model
        result = whisper_pipeline(
            file_path,
            chunk_length_s=30,
            batch_size=24,
            return_timestamps=False,
        )
        return result["text"]
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


# given a file path, delete the file
def delete_file(file_path: str):
    try:
        os.remove(file_path)
        print(f"File {file_path} deleted")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")
