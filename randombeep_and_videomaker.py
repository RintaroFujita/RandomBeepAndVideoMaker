from google.colab import drive
import cv2
import numpy as np
import wave
import struct
import os
import uuid
import random
import moviepy.editor as mp
drive.mount('/content/drive')

width =  900 #nomal 1920
height = 700 #nomal 1080
fps = 30
seconds = 10
total_frames = fps * seconds

output_dir = "/content/drive/My Drive/GeneratedVideos/"
sound_dir = "/content/drive/My Drive/GeneratedVideos/sound"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(sound_dir):
    os.makedirs(sound_dir)
def generate_random_pattern():
    color = np.random.randint(0, 256, size=3)
    x = np.random.randint(0, width)
    y = np.random.randint(0, height)
    shape = np.random.choice(["circle", "rectangle"])
    return x, y, color, shape
def generate_beep_sound(duration_ms, sample_rate=44100, num_freqs=3, freq_range=(500, 5000)):
    num_samples = int(duration_ms * sample_rate / 1000)
    num_channels = 1 
    sample_width = 2 
    max_value = 2 ** (sample_width * 8 - 1) - 1
    freqs = [random.randint(freq_range[0], freq_range[1]) for _ in range(num_freqs)]
    data = np.zeros(num_samples, dtype=np.int16)
    for freq in freqs:
        sine_wave = [int(max_value * np.sin(2 * np.pi * freq * t / sample_rate)) for t in range(num_samples)]
        data += np.array(sine_wave, dtype=np.int16)
    sound_file = os.path.join(sound_dir, str(uuid.uuid4()) + ".wav")
    with wave.open(sound_file, "w") as wf:
        wf.setnchannels(num_channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(data.tobytes())

    return sound_file

for _ in range(15):
    sound_file = generate_beep_sound(10000)
    frames = []
    for frame_number in range(total_frames):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        x, y, color, shape = generate_random_pattern()
        if shape == "circle":
            radius = np.random.randint(10, 100)
            cv2.circle(frame, (x, y), radius, tuple(color.tolist()), -1)
        elif shape == "rectangle":
            width_rect = np.random.randint(10, 200)
            height_rect = np.random.randint(10, 200)
            cv2.rectangle(frame, (x, y), (x+width_rect, y+height_rect), tuple(color.tolist()), -1)

        frames.append(frame)
    video_clip = mp.ImageSequenceClip(frames, fps=fps)
    audio_clip = mp.AudioFileClip(sound_file)
    final_clip = video_clip.set_audio(audio_clip)
    output_filename = os.path.join(output_dir, str(uuid.uuid4()) + ".mp4")
    final_clip.write_videofile(output_filename)
