import time

import cv2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import numpy as np
import pyautogui


# Define the options of your webdriver here
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# Define webdriver here
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Select page to open here
driver.get("https://www.youtube.com")
driver.maximize_window()
driver.implicitly_wait(2)

# WEB PAGE CONTENT HERE

# Automatically accept Terms of Service for YouTube
try:
    button = driver.find_element(By.XPATH, "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/a/tp-yt-paper-button")
    button.click()
    driver.implicitly_wait(2)
except:
    print("Terms of Service didn't appear/ Page loaded too quickly/ other error")


# Automatically select a random video from the first row
# Refresh page to avoid certain errors
driver.refresh()
try:
    video_to_select = np.random.randint(1, 4)
    video = driver.find_element(By.XPATH, f"/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[{video_to_select}]/div/ytd-rich-grid-media/div[1]/div[2]/div[1]/h3/a")
    video.click()
    driver.implicitly_wait(2)
except:
    print("Page loaded too quickly/ other error")

# Automatically skip adds before recording
# The program checks up to 4 ads with the variable check_ads
# First it verifies if it is an unskippable ad then it checks if it is a skippable ad
check_ads = 0
while check_ads < 3:
    try:
        check_skip_button = driver.find_element(By.ID, 'ad-image:4').value_of_css_property("display")

        while check_skip_button != "none":
            check_skip_button = driver.find_element(By.ID, 'ad-image:4').value_of_css_property("display")
            print(check_skip_button)

    except:
        print("no unskippable adds")

    try:
        skip_button = driver.find_element(By.XPATH, "//button[contains(@class, 'ytp-ad-skip-button ytp-button')]")
        skip_button.click()
    except:
        print("no skippable adds")

    check_ads += 1

# Refresh the page in order for the VideoRecorder script to catch-up with the webpage
driver.refresh()
driver.implicitly_wait(1)

# Automatically put video in fullscreen
try:
    video_fullscreen_button = driver.find_element(By.XPATH, "//button[contains(@class, 'ytp-fullscreen-button ytp-button')]")
    video_fullscreen_button.click()
    driver.implicitly_wait(3)
except:
    print("Page loaded too quickly/ other error")


# Specify resolution
resolution = (1920, 1080)

# Specify video codec
codec = cv2.VideoWriter_fourcc(*"DIVX")

# Specify name of Output file
filename = "Recording.avi"

# Specify frames rate. We can choose any
# value and experiment with it
fps = 60.0

# Creating a VideoWriter object
out = cv2.VideoWriter(filename, codec, fps, resolution)

# Create an Empty window
cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

# Resize this window
cv2.resizeWindow("Live", 480, 270)

while True:
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

# Destroy all windows
cv2.destroyAllWindows()







