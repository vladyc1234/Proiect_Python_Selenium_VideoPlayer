import socket
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
import multiprocessing as mp
from win32api import GetSystemMetrics
import logging
from scipy.io import wavfile
import soundfile as sf
import urllib.request

check_dbs = open("check_dbs.txt", "w")


##################################################################
# VIDEO PARAMETERS

# Specify resolution
resolution = (GetSystemMetrics(0), GetSystemMetrics(1))

# Specify video codec
codec = cv2.VideoWriter_fourcc(*"XVID")

# Specify name of Output file
filename = "Recording.avi"

# Specify frames rate. We can choose any
# value and experiment with it
fps = 16.0

# Creating a VideoWriter object
out = cv2.VideoWriter(filename, codec, fps, resolution)

##################################################################
##################################################################
# AUDIO PARAMETERS

chunk = 1024  # Each chunk will consist of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1  # Number of audio channels
fs = 44100  # Record at 44100 samples per second
time_in_seconds = 10
filename = "soundsample.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

# Open a Stream with the values we just defined
stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

##################################################################


logging.basicConfig(filename="InternetLog.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
loggerI = logging.getLogger()
loggerI.setLevel(logging.INFO)

# Function to check internet connection

def check_connection():
    try:
        urllib.request.urlopen('http://google.com')
        loggerI.info("Connected to internet")
    except:
        loggerI.error("No connection to internet")


def Selenium():
    # Prepare logger
    logging.basicConfig(filename="SeleniumLog.log",
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
        check_connection()
        driver.get("https://www.youtube.com")
        driver.maximize_window()
        logger.info('Opened YouTube in Chrome and maximized the window\n')
        driver.implicitly_wait(2)
    except:
        logger.error("error\n")

    # WEB PAGE CONTENT HERE

    # Automatically accept Terms of Service for YouTube
    try:
        check_connection()
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
        check_connection()
        video_to_select = np.random.randint(1, 4)
        video = driver.find_element(By.XPATH,
                                    f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[{video_to_select}]/div/ytd-rich-grid-media/div[1]/div[2]/div[1]/h3/a")
        video.click()
        logger.info('Selected a random video\n')
        driver.implicitly_wait(2)
    except:
        logger.error("Page loaded too quickly/ other error\n")

    # Automatically skip adds before recording
    # First it verifies if it is an unskippable ad then it checks if it is a skippable ad
    check_ads = 0
    while check_ads < 3:
        try:
            check_connection()
            check_skip_button = driver.find_element(By.ID, 'ad-image:4').value_of_css_property("display")

            while check_skip_button != "none":
                check_skip_button = driver.find_element(By.ID, 'ad-image:4').value_of_css_property("display")

        except:
            logger.warning("no unskippable adds\n")

        try:
            check_connection()
            skip_button = driver.find_element(By.XPATH, "//button[contains(@class, 'ytp-ad-skip-button ytp-button')]")
            skip_button.click()
            logger.info('Skipped an ad\n')
        except:
            logger.warning("no skippable adds\n")

        check_ads += 1

    # Refresh the page in order for the VideoRecorder script to catch-up with the webpage
    driver.refresh()

    # Automatically put video in fullscreen
    try:
        check_connection()
        video_fullscreen_button = driver.find_element(By.XPATH,
                                                      "//button[contains(@class, 'ytp-fullscreen-button ytp-button')]")
        video_fullscreen_button.click()
        logger.info('Video now in fullscreen\n')
        driver.implicitly_wait(3)
    except:
        logger.error("Page loaded too quickly/ other error\n")


# VIDEO RECORDER

def record_video(frames):
    print("RECORD VIDEO", time.strftime("%H:%M:%S"))
    logging.basicConfig(filename="VideoLog.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    start_record = time.time()
    current_record_time = time.time()
    logger.info("Start video recording\n")
    while True and current_record_time - start_record < time_in_seconds:



        current_record_time = time.time()

        # Take screenshot using PyAutoGUI
        img = pyautogui.screenshot()

        # Convert the screenshot to a numpy array
        frame = np.array(img)

        # Write it to the output file
        frames.append(frame)

        # Stop recording when we press 'q'
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the Video writer

    # Destroy all windows
    cv2.destroyAllWindows()
    logger.info("End video recording\n")


# AUDIO RECORDER

def record_audio():
    logging.basicConfig(filename="AudioLog.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    print("RECORD AUDIO", time.strftime("%H:%M:%S"))

    logger.info("Start audio recording\n")

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

def rms_flat(a):  # from matplotlib.mlab
    """
    Return the root mean square of all the elements of *a*, flattened out.
    """
    return np.sqrt(np.mean(np.absolute(a)**2))


def measure_wav_db_level(wavFile):
    """
    Open a wave or raw audio file and perform the following tasks:
    - compute the overall level in db (RMS of data)
    """
    try:
        fs, x = wavfile.read(wavFile)
        LOG_SCALE = 20*np.log10(32767)
    except:
        x, fs = sf.read(wavFile,
                        channels=1, samplerate=44100,
                        format='RAW', subtype='PCM_16')
        LOG_SCALE = 0
    t = (np.array(x)).astype(np.float64)
    # x holds the int16 data, but it's hard to work on int16
    # t holds the float64 conversion

    check_dbs.writelines(str(fs) + ' Hz\n')
    check_dbs.writelines(str(len(t) / fs) + ' s\n')
    orig_SPL = 20*np.log10(rms_flat(t)) - LOG_SCALE
    check_dbs.writelines('Sound level:   ' + str(orig_SPL) + ' dBFS\n')

def combine_audio(vidname, audname, outname, fps=16):
    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps)

if __name__ == '__main__':

    logging.basicConfig(filename="MainLog.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # PREPARE A QUEUE TO RECEIVE FRAME FROM VIDEO RECORD
    manager = mp.Manager()
    return_frames = manager.list()

    try:
        urllib.request.urlopen('http://www.youtube.com')

        Selenium()

        # DECLARE VIDEO RECORD PROCESS
        process1 = mp.Process(target=record_video, args=(return_frames,))
        print("PROCESS1", time.strftime("%H:%M:%S"))
        logger.info("PROCESS1 starts")

        # DECLARE AUDIO RECORD PROCESS
        process2 = mp.Process(target=record_audio, args=())
        print("PROCESS2", time.strftime("%H:%M:%S"))
        logger.info("PROCESS2 starts")

        # START PROCESSES
        process1.start()
        process2.start()

        # RECEIVE FRAME FROM QUEUE AND WRITE THEM TO FILE

        process1.join()

        for frame in return_frames:
            out.write(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        out.release()

        process1.close()

        process2.join()
        process2.close()

        # MEASURE DBs
        measure_wav_db_level("soundsample.wav")

        # MERGE AUDIO AND VIDEO FILES
        combine_audio("Recording.avi", "soundsample.wav", "FinalRecording.mp4", fps=16)
    except:
        loggerI.error("NO CONNECTION")