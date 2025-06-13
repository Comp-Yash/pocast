import google.generativeai as genai
import time
import re
from elevenlabs import generate, play, set_api_key

# 🔑 Set up Gemini
genai.configure(api_key="AIzaSyBNDP4ixG27c9zblIBYeXzajhXV5vu1_mk")
model = genai.GenerativeModel("gemini-2.0-flash")

# 🔑 Set up ElevenLabs
set_api_key("sk_0212e4a7b593ed16cbe885ea14baa75c92515c01e37a5da2")

# -------------- GEMINI PART -------------- #

def generate_data(topic):
    prompt = f"I have to create podcast on topic : {topic} . So go through internet and all valid sources collect data along links , names of research paper if any . generate very large infomatove paragphas "
    print("🔍 Sending prompt  to Gemini...")
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_script(number_of_person, data, topic):
    prompt = f"""You are proffesional podcast writer , 
    write post on topic with provided data, topic : {topic}  , data : {data} . 
    Total number of people in podcast is n = {number_of_person} . So 2 to 5 minutes long podcast dialogues script(humanised) .
    
    Here is answer formate  :
    Person 1 : <script>
    Person 2 : <script>
    Person 1 : <script>
    .
    .
    . 
    person n :
    n will be small .

    Note : 
    1) You onlu return script no any adding context 
    2) Start of script will be small intoduction of Host to guest (you give them random name eg Ben , Anya , Alice ,etc)
    eg  Anya Sharma : Welcome back to AI EdTech Today! I'm your host, Dr. Anya Sharma, and today we're diving into the fascinating and sometimes confusing world of AI in education. I’m thrilled to have Mr. Ben Carter, a high school teacher with us today. Ben, welcome to the show!
        Ben Carter: Thanks, Anya! Glad to be here.
        Anya Sharma: Ben, you're on the front lines. What's your gut reaction when you hear "AI in the classroom"? Excitement? Apprehension? A bit of both?
        etc

    
    """
    print("🔍 Sending prompt  to Gemini...")
    response = model.generate_content(prompt)
    return response.text.strip()

# -------------- PODCAST SCRIPT GENERATION -------------- #

data = generate_data("AI in education")
script = generate_script(4, data, "AI in education")


# -------------- VOICE SYNTHESIS USING ELEVENLABS -------------- #

VOICE_POOL = ["Rachel", "Antoni", "Bella", "Elli"]

def assign_voices(num_people):
    return VOICE_POOL[:num_people]

def parse_script(script_text):
    pattern = r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*):\s(.+?)(?=(?:\n[A-Z][a-z]+(?:\s[A-Z][a-z]+)*:)|$)"
    return re.findall(pattern, script_text, flags=re.DOTALL)
import os
from pydub import AudioSegment
from pydub.playback import play as pydub_play
from io import BytesIO


AudioSegment.converter = r"D:\B tech\Intellify(Build fast with AI)\ffmpeg-2025-06-08-git-5fea5e3e11-full_build\ffmpeg-2025-06-08-git-5fea5e3e11-full_build\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"D:\B tech\Intellify(Build fast with AI)\ffmpeg-2025-06-08-git-5fea5e3e11-full_build\ffmpeg-2025-06-08-git-5fea5e3e11-full_build\bin\ffprobe.exe"




from elevenlabs import generate





def generate_clips(script):
    speakers = ["Rachel", "Antoni", "Bella", "Elli"]
    names = ["Ben Carter", "Alice Lee", "David Chen", "Anya Sharma"]

    line_counter = 1

    for line in script.splitlines():
        if not line.strip():
            continue

        for idx, name in enumerate(names):
            if line.startswith(name):
                voice = speakers[idx]
                print(f"\n🎤 {line.strip()}")

                # 🔥 Extract the text **after** the colon (:) for speaking
                parts = line.split(":", 1)
                if len(parts) < 2:
                    print(f"❓ No dialogue found after colon in line: {line}")
                    break

                text_to_speak = parts[1].strip()

                try:
                    audio_bytes = generate(text=text_to_speak, voice=voice, model="eleven_monolingual_v1")
                    filename = f"{line_counter}.mp3"
                    with open(filename, "wb") as f:
                        f.write(audio_bytes)
                    print(f"✅ Saved: {filename}")
                    line_counter += 1

                except Exception as e:
                    print(f"⚠️ Error generating audio: {e}")
                break

    print(f"\n✅ All {line_counter - 1} clips saved.")



generate_clips(script)
print(script)