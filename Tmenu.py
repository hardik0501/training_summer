import gradio as gr
import os
from twilio.rest import Client
from instagrapi import Client as InstaClient
from linkedin_api import Linkedin
import tweepy
from dotenv import load_dotenv
load_dotenv()

# --- Credentials from .env or direct ---
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH = os.getenv("TWILIO_AUTH")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")
YOUR_PHONE = os.getenv("YOUR_PHONE")
WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE")

LINKEDIN_COOKIE = os.getenv("LI_AT")

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

INSTA_USER = os.getenv("INSTA_USER")
INSTA_PASS = os.getenv("INSTA_PASS")

# --- Function Definitions ---

def send_sms(message):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)
        msg = client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to=YOUR_PHONE
        )
        return f"✅ SMS sent: SID {msg.sid}"
    except Exception as e:
        return f"❌ SMS Error: {e}"

def make_call(text):
    from urllib.parse import quote
    twiml = f"<Response><Say>{text}</Say></Response>"
    url = f"http://twimlets.com/echo?Twiml={quote(twiml)}"
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)
        call = client.calls.create(to=YOUR_PHONE, from_=TWILIO_PHONE, url=url)
        return f"📞 Call placed! SID: {call.sid}"
    except Exception as e:
        return f"❌ Call Error: {e}"

def send_whatsapp(message):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH)
        msg = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message,
            to=f'whatsapp:{WHATSAPP_PHONE}'
        )
        return f"✅ WhatsApp sent: SID {msg.sid}"
    except Exception as e:
        return f"❌ WhatsApp Error: {e}"

def post_linkedin(message):
    try:
        api = Linkedin(cookie=LINKEDIN_COOKIE)
        api.submit_share(comment=message)
        return "✅ LinkedIn post successful!"
    except Exception as e:
        return f"❌ LinkedIn Error: {e}"

def post_twitter(tweet):
    try:
        auth = tweepy.OAuth1UserHandler(
            TWITTER_API_KEY, TWITTER_API_SECRET,
            TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
        )
        api = tweepy.API(auth)
        api.update_status(tweet)
        return "✅ Tweet posted!"
    except Exception as e:
        return f"❌ Twitter Error: {e}"

def post_instagram(image, caption):
    try:
        path = "temp.jpg"
        image.save(path)
        insta = InstaClient()
        insta.login(INSTA_USER, INSTA_PASS)
        insta.photo_upload(path, caption)
        os.remove(path)
        return "✅ Instagram post uploaded!"
    except Exception as e:
        return f"❌ Instagram Error: {e}"

# --- Gradio UI ---

with gr.Blocks() as app:
    gr.Markdown("## 💬 Multi-Platform Automation Tool (Python + Gradio)")

    with gr.Tab("📧 Send Email"):
        email_message = gr.Textbox(label="Email Message")
        email_btn = gr.Button("Send Email")
        email_out = gr.Textbox()
        # Optional: Add SMTP-based email if desired
        email_btn.click(lambda x: "Email logic skipped. Use SMTP or EmailJS.", inputs=email_message, outputs=email_out)

    with gr.Tab("📲 Send SMS"):
        sms_input = gr.Textbox(label="Message")
        sms_btn = gr.Button("Send SMS")
        sms_out = gr.Textbox()
        sms_btn.click(send_sms, inputs=sms_input, outputs=sms_out)

    with gr.Tab("📞 Make Call"):
        call_input = gr.Textbox(label="Text to Speak")
        call_btn = gr.Button("Place Call")
        call_out = gr.Textbox()
        call_btn.click(make_call, inputs=call_input, outputs=call_out)

    with gr.Tab("💬 WhatsApp Message"):
        wa_input = gr.Textbox(label="Message")
        wa_btn = gr.Button("Send WhatsApp")
        wa_out = gr.Textbox()
        wa_btn.click(send_whatsapp, inputs=wa_input, outputs=wa_out)

    with gr.Tab("🔗 Post to LinkedIn"):
        li_input = gr.Textbox(label="Post Content", lines=3)
        li_btn = gr.Button("Post")
        li_out = gr.Textbox()
        li_btn.click(post_linkedin, inputs=li_input, outputs=li_out)

    with gr.Tab("🐦 Post to Twitter"):
        tweet_input = gr.Textbox(label="Tweet", lines=3)
        tweet_btn = gr.Button("Post Tweet")
        tweet_out = gr.Textbox()
        tweet_btn.click(post_twitter, inputs=tweet_input, outputs=tweet_out)

    with gr.Tab("📸 Post to Instagram"):
        insta_img = gr.Image(type="pil", label="Upload Image")
        insta_caption = gr.Textbox(label="Caption")
        insta_btn = gr.Button("Post to Instagram")
        insta_out = gr.Textbox()
        insta_btn.click(post_instagram, inputs=[insta_img, insta_caption], outputs=insta_out)

app.launch()
