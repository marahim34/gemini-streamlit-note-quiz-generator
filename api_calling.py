from google import genai
from dotenv import load_dotenv
import os
import gtts
import io

# Loading environment variables from .env file
load_dotenv()

# Getting the API key from environment variable
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the GenAI client with the API key
client = genai.Client(api_key=api_key)



# Note generation
def note_generator(images):

    prompt = """Summarize the picutres in note format at max 100 words, 
    and make sure to add necessary markdownn to differentiate different sections"""

    response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[images, prompt]
)

    return response.text


def audio_transcription(text):
    speech = gtts.gTTS(text=text, lang='en', slow=False)
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer


def quiz_generator(images, difficulty):
    prompt = f"""Generate three quizes based on the {difficulty}. Make sure to add markdown to differentiate options. 
    Add answers after the quiz with the heading "Answer Key" and make sure to differentiate the answer key section with markdown"""

    response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[images, prompt]
)

    return response.text