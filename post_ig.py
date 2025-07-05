import gradio as gr
from instagrapi import Client
import os

# Instagram login (hardcoded for demo — use env vars in production!)
USERNAME = "your_instagram_username"
PASSWORD = "your_instagram_password"

# Login once when app starts
cl = Client()
try:
    cl.login(USERNAME, PASSWORD)
except Exception as e:
    print("Login failed:", e)

def upload_to_instagram(image, caption):
    try:
        # Save uploaded image temporarily
        temp_image_path = "temp_instagram_image.jpg"
        image.save(temp_image_path)

        # Upload to Instagram
        cl.photo_upload(temp_image_path, caption)
        os.remove(temp_image_path)

        return "✅ Posted to Instagram successfully!"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# CSS Styling
custom_css = """
input, textarea {
    padding: 10px;
    border: 2px solid #ccc;
    border-radius: 10px;
    font-size: 16px;
}
button {
    background-color: #E1306C !important;
    color: white !important;
    padding: 12px 24px !important;
    border: none;
    border-radius: 10px !important;
    font-size: 16px !important;
}
h1 {
    text-align: center;
    color: #E1306C;
}
"""

# Gradio UI
with gr.Blocks(css=custom_css) as app:
    gr.Markdown("## 📸 Instagram Auto Poster with Python + Gradio")
    img_input = gr.Image(type="pil", label="Upload Image")
    caption_input = gr.Textbox(label="✍️ Caption", lines=3, placeholder="Write your caption with hashtags...")
    post_btn = gr.Button("🚀 Post to Instagram")
    status_output = gr.Textbox(label="Status")

    post_btn.click(upload_to_instagram, inputs=[img_input, caption_input], outputs=status_output)

app.launch()
