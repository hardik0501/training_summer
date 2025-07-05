import gradio as gr
from linkedin_api import Linkedin

# Paste your LinkedIn session cookie (keep it safe!)
LI_AT = "your_li_at_cookie_here"

def post_to_linkedin(message):
    try:
        api = Linkedin(cookie=LI_AT)
        api.submit_share(comment=message)
        return "✅ Post successfully made to LinkedIn!"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Gradio UI
custom_css = """
textarea {
    padding: 10px;
    border: 2px solid #ccc;
    border-radius: 10px;
    font-size: 16px;
}
button {
    background-color: #0077B5 !important;
    color: white !important;
    padding: 10px 20px !important;
    border-radius: 10px !important;
    font-size: 16px !important;
}
"""

with gr.Blocks(css=custom_css) as app:
    gr.Markdown("## 🔗 Post to LinkedIn using Python + Gradio")
    post_text = gr.Textbox(label="✍️ Post Content", lines=5, placeholder="Write your LinkedIn post with #hashtags here...")
    post_button = gr.Button("🚀 Post to LinkedIn")
    status = gr.Textbox(label="📌 Status")

    post_button.click(fn=post_to_linkedin, inputs=post_text, outputs=status)

app.launch()
