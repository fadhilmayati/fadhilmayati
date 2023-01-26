from selenium import webdriver

# specify the path of the Brave webdriver
webdriver_path = "path/to/brave_webdriver.exe"

# create a new instance of the Brave driver
driver = webdriver.Brave(executable_path=webdriver_path)

# navigate to the YouTube video URL
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
driver.get(video_url)

# play the video
play_button = driver.find_element_by_xpath("//button[@class='ytp-play-button ytp-button']")
play_button.click()
