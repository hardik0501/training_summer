import gradio as gr
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Your Twitter credentials (NOT recommended in production)
USERNAME = "your_username_or_email"
PASSWORD = "your_password"

def post_to_twitter(tweet):
    try:
        # Launch browser
        driver = webdriver.Chrome()
        driver.get("https://twitter.com/login")
        time.sleep(3)

        # Enter username
        user_input = driver.find_element(By.NAME, "text")
        user_input.send_keys(USERNAME)
        user_input.send_keys(u'\ue007')  # Press Enter
        time.sleep(3)

        # Enter password
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(PASSWORD)
        password_input.send_keys(u'\ue007')
        time.sleep(5)

        # Post tweet
        tweet_box = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Tweet text']")
        tweet_box.send_keys(tweet)
        time.sleep(1)

        tweet_button = driver.find_element(By.XPATH, "//div[@data-testid='tweetButtonInline']")
        tweet_button.click()
        time.sleep(3)

        driver.quit()
        return "✅ Tweet posted successfully!"
    except Exception as e:
        driver.quit()
        return f"❌ Error: {str(e)}"

gr.Interface(fn=post_to_twitter, inputs="text", outputs="text", title="Post to Twitter Without API").launch()
