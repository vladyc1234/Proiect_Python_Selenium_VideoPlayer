import time
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import numpy as np
import pyautogui
import pyaudio
import wave
import asyncio
import multiprocessing as mp
from win32api import GetSystemMetrics
import logging

# Prepare logger
logging.basicConfig(filename="RecorderLog.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)

# Define the options of your webdriver here
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Define webdriver here
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Select page to open here
try:
    driver.get("https://www.youtube.com")
    driver.maximize_window()
    logger.info('Opened YouTube in Chrome and maximized the window\n')
    driver.implicitly_wait(2)
except:
    logger.error("error\n")

# WEB PAGE CONTENT HERE

# Automatically accept Terms of Service for YouTube
try:
    button = driver.find_element(By.XPATH,
                                 "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/a/tp-yt-paper-button")
    button.click()
    logger.info('Accepted Terms of Service\n')
    driver.implicitly_wait(2)
except:
    logger.error("Terms of Service didn't appear/ Page loaded too quickly/ other error\n")

# Automatically select a random video from the first row
# Refresh page to avoid certain errors
driver.refresh()
try:
    video_to_select = np.random.randint(1, 4)
    video = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[{video_to_select}]/div/ytd-rich-grid-media/div[1]/div[2]/div[1]/h3/a")
    video.click()
    logger.info('Selected a random video\n')
    driver.implicitly_wait(2)
except:
    logger.error("Page loaded too quickly/ other error\n")

# Automatically skip adds before recording
# The program checks up to 4 ads with the variable check_ads
# First it verifies if it is an unskippable ad then it checks if it is a skippable ad
check_ads = 0
while check_ads < 3:
    try:
        check_skip_button = driver.find_element(By.ID, 'ad-image:4').value_of_css_property("display")

        while check_skip_button != "none":
            check_skip_button = driver.find_element(By.ID, 'ad-image:4').value_of_css_property("display")

    except:
        logger.warning("no unskippable adds\n")

    try:
        skip_button = driver.find_element(By.XPATH, "//button[contains(@class, 'ytp-ad-skip-button ytp-button')]")
        skip_button.click()
        logger.info('Skipped an ad\n')
    except:
        logger.warning("no skippable adds\n")

    check_ads += 1

# Refresh the page in order for the VideoRecorder script to catch-up with the webpage
driver.refresh()
driver.implicitly_wait(1)

# Automatically put video in fullscreen
try:
    video_fullscreen_button = driver.find_element(By.XPATH,
                                                  "//button[contains(@class, 'ytp-fullscreen-button ytp-button')]")
    video_fullscreen_button.click()
    logger.info('Video now in fullscreen\n')
    driver.implicitly_wait(3)
except:
    logger.error("Page loaded too quickly/ other error\n")


# AUDIO RECORDER

def record_video():
    # Specify resolution
    resolution = (GetSystemMetrics(0), GetSystemMetrics(1))

    # Specify video codec
    codec = cv2.VideoWriter_fourcc(*"DIVX")

    # Specify name of Output file
    filename = "Recording.avi"

    # Specify frames rate. We can choose any
    # value and experiment with it
    fps = 17.0

    # Creating a VideoWriter object
    out = cv2.VideoWriter(filename, codec, fps, resolution)

    # Create an Empty window
    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

    # Resize this window
    cv2.resizeWindow("Live", 480, 270)

    start_record = time.time()
    current_record_time = time.time()
    logger.info("Start video recording\n")
    while True and current_record_time - start_record < 120:

        current_record_time = time.time()

        # Take screenshot using PyAutoGUI
        img = pyautogui.screenshot()

        # Convert the screenshot to a numpy array
        frame = np.array(img)

        # Convert it from BGR(Blue, Green, Red) to
        # RGB(Red, Green, Blue)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Write it to the output file
        out.write(frame)

        # Optional: Display the recording screen
        cv2.imshow('Live', frame)

        # Stop recording when we press 'q'
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the Video writer
    out.release()
    logger.info("End video recording\n")
    # Destroy all windows
    cv2.destroyAllWindows()

#AUDIO RECORDER

def record_audio():
    chunk = 1024  # Each chunk will consist of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1  # Number of audio channels
    fs = 44100  # Record at 44100 samples per second
    time_in_seconds = 3
    filename = "soundsample.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    logger.info("Start audio recording\n")

    # Open a Stream with the values we just defined
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * time_in_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the Stream and PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()

    logger.info("End audio recording\n")

    # Open and Set the data of the WAV file
    file = wave.open(filename, 'wb')
    file.setnchannels(channels)
    file.setsampwidth(p.get_sample_size(sample_format))
    file.setframerate(fs)

    # Write and Close the File
    file.writeframes(b''.join(frames))
    file.close()


if __name__ == '__main__':
    process1 = mp.Process(target=record_video())
    print(time.strftime("%H:%M:%S"))
    process2 = mp.Process(target=record_audio())
    print(time.strftime("%H:%M:%S"))
    process1.start()
    print(time.strftime("%H:%M:%S"))
    process2.start()
    print(time.strftime("%H:%M:%S"))
    process1.join()
    process2.join()
