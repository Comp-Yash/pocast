import streamlit as st
import google.generativeai as genai
from elevenlabs import generate, set_api_key
import os
import re
from playsound import playsound

# Streamlit UI - Title & Key Input
st.title("🎙️ AI Podcast Generator")

gemini_key = st.text_input("🔐 Enter your Google Gemini API key:", type="password")
elevenlabs_key = st.text_input("🔐 Enter your ElevenLabs API key:", type="password")

# Check for required keys before proceeding
if gemini_key and elevenlabs_key:
    genai.configure(api_key=gemini_key)
    set_api_key(elevenlabs_key)

    # Constants
    VOICE_POOL = ["Rachel", "Antoni", "Bella", "Elli"]

    # Functions
    def generate_data(topic):
        prompt = f"I have to create podcast on topic: {topic}. Go through internet sources and give large informative paragraphs with references."
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text.strip()

    def generate_script(num_people, data, topic):
        prompt = f"""You are pro podcast writer. Write humanised dialogue on topic: {topic}, based on data: {data}.
Total speakers = {num_people}. Length: 2-5 min.
Return in this format:
Person 1 : <line>
Person 2 : <line>
Person 3 : <line>...

Example:
Anya Sharma : Welcome to AI in EdTech! I'm your host Anya, and joining me is Mr. Ben Carter.
Ben Carter : Thanks Anya! Happy to be here.
Only return script.
"""
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text.strip()

    def parse_script(script_text):
        pattern = r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*):\s(.+?)(?=\n[A-Z][a-z]+(?:\s[A-Z][a-z]+)*:|$)"
        return re.findall(pattern, script_text, flags=re.DOTALL)

    def assign_voices(names):
        return {name: VOICE_POOL[i % len(VOICE_POOL)] for i, name in enumerate(names)}

    def generate_audio_clips(script_lines, voice_map, output_dir="clips"):
        os.makedirs(output_dir, exist_ok=True)
        audio_paths = []
        for i, (name, line) in enumerate(script_lines, start=1):
            voice = voice_map.get(name, "Rachel")
            try:
                audio = generate(text=line.strip(), voice=voice, model="eleven_monolingual_v1")
                filename = os.path.join(output_dir, f"{i}.mp3")
                with open(filename, "wb") as f:
                    f.write(audio)
                audio_paths.append(filename)
            except Exception as e:
                st.error(f"Error for line {i} ({name}): {e}")
        return audio_paths

    # Main App Inputs
    topic = st.text_input("🎯 Enter podcast topic:", "AI in Education")
    num_people = st.slider("👥 Number of speakers", 2, 4, 2)

    if st.button("🎬 Generate Podcast"):
        with st.spinner("🔄 Generating script and audio..."):
            try:
                data = generate_data(topic)
                script = generate_script(num_people, data, topic)
                st.subheader("📜 Generated Script")
                st.text(script)

                script_lines = parse_script(script)
                unique_names = list({name for name, _ in script_lines})
                voice_map = assign_voices(unique_names)

                st.info("🔊 Generating voice clips...")
                audio_files = generate_audio_clips(script_lines, voice_map)

                if audio_files:
                    merged_audio = os.path.join("clips", "merged_podcast.mp3")
                    with open(merged_audio, "wb") as outfile:
                        for f in audio_files:
                            with open(f, "rb") as infile:
                                outfile.write(infile.read())

                    st.success("✅ Podcast Ready!")
                    st.audio(merged_audio)

                    if st.button("▶️ Play Podcast"):
                        playsound(merged_audio)

            except Exception as e:
                st.error(f"Something went wrong: {e}")

else:
    st.warning("Please enter both Gemini and ElevenLabs API keys to begin.")
