# Proiect_Python_Selenium_VideoPlayer

# Operating System:

- Windows 10 Pro (Version 21H2)

# Compiler:

- Python 3.8

# Apps Used:

- Pycharm Community edition

# Libraries:

- pip install numpy - installed numpy-1.23.1

- pip install opencv - ERROR - No matching distribution found for opencv
		     - SOLUTION - pip install opencv-python - installed opencv-python-4.6.0.66

- pip install pyautogui - installed Pillow-9.2.0 PyTweening-1.0.4 mouseinfo-0.1.3 			                                                
			  pyautogui-0.9.53 pygetwindow-0.0.9 pymsgbox-1.0.9 
                          pyperclip-1.8.2 pyrect-0.2.0 pyscreeze-0.1.28

- pip install pyaudio - ERROR - legacy-install-failure
		      - SOLUTION - pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl -
				  	installed backports.zoneinfo-0.2.1 
                                  	beautifulsoup4-4.11.1 certifi-2022.
                                  	6.15 charset-normalizer-2.1.0 docopt-0.6.2 
                                  	idna-3.3 js2py-0.71 packaging-21.3 
                                  	pipwin-0.5.2 pySmartDL-1.3.4 pyjsparser-2.7.1 pyparsing-3.0.9 pyprind-2.11.3 
                                  	pytz-deprecation-shim-0.1.0.post0 requests-2.28.1 six-1.16.0 soupsieve-2.3.2.post1 
                                  	tzdata-2022.1 tzlocal-4.2 urllib3-1.26.10
				 - pipwin install pyaudio - installed PyAudio-0.2.11

- pip install selenium - installed PySocks-1.7.1 async-generator-1.10 attrs-21.4.0 cffi-1.15.1 cryptography-37.0.4 
			 h11-0.13.0 outcome-1.2.0 pyOpenSSL-22.0.0 pycparser-2.21 selenium-4.3.0 
			 sniffio-1.2.0 sortedcontainers-2.4.0 trio-0.21.0 trio-websocket-0.9.2 wsproto-1.1.0

- pip install pywin32 - installed pywin32-304

- pip install scipy - installed scipy-1.8.1

- pip install soundfile - installed SoundFile-0.10.3.post1.dist-info

- pip install moviepy - installed colorama-0.4.5 decorator-4.4.2 imageio-2.19.5 imageio_ffmpeg-0.4.7 moviepy-1.0.3 proglog-0.1.10 tqdm-4.64.0

- pre-installed libraries from PyCharm - time, logging, urllib

# Script Errors and Solutions:

- ERROR - selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH.
  SOLUTION - pip install webdriver-manager - installed python-dotenv-0.20.0 webdriver-manager-3.8.1
  
- ERROR - couldn't run the video and record functions at the same time
  SOLUTION - I used processes to run them in parallel
  
- ERROR - my video was getting corrupted by the record function when used in a process 
  SOLUTION - I used a multiprocess variable manager in order to save my video frames in that variable and then send them in the main section after the process finished
             in order to transform them in video form

- ERROR - my webpage was loading too slow and my webdriver couldn't select the specified elements
  SOLUTION - I used driver.implicitly_wait() to let the page load first

# How to use:

1. Have a functional mic plugged in

2. Open the Sounds menu: enable only your mic in the recording section and only your screen speakers in the playback section

3. Open your PyCharm, download the necessary libraries and copy the script

4. Run the script and wait for its completion

Results: You will get a 2 minute recording, Logs for each main function (VideoLog.txt, AudioLog.txt, SeleniumLog.txt, MainLog.txt) and details about the sound properties (check_dbs)

# How does the script work

The script is split up in different sections. It has the first section in which you set the parameters for your audio and video recorders and then it has it's 3 main functions.

The first function in Selenium(). It it responsible for opening the YouTube page in Chrome. It accepts the Terms of Service, selects a random video and skips its ads.
	
The second function is record_video(). It is the function responsible for recording the YouYube video. It works by screenshoting the video frames and then piecing them up into a full video.
	
The third function is record_audo(). It records the audio. It takes chunks of data reads them and then adds them to a file after processing them.
	
The program also contains a function for analyzing the audio measure_wav_db_level(wavFile) and rms_flat(a), a function for merging the audio and video recordings combine_audio(vidname, audname, outname, fps=17) and a function for checking the internet connection check_connection().

In the final section it calls these functions. It uses multiprocessing in order to run the video and audio record functions at the same time. It then analyzes the audio file and merge the recordings.
	

		

