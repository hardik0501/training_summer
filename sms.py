import gradio as gr
from twilio.rest import Client

# Twilio credentials (WARNING: Replace with environment variables in production)
account_sid = ''
auth_token = ''
twilio_number = ''

def send_sms(to_number, message_body):
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=twilio_number,
            to=to_number
        )
        return f"✅ Message sent! SID: {message.sid}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Custom CSS styling
custom_css = """
input, textarea {
    padding: 10px;
    border: 2px solid #ccc;
    border-radius: 10px;
    font-size: 16px;
}
button {
    background-color: #28a745 !important;
    color: white !important;
    padding: 10px 20px !important;
    border: none;
    border-radius: 10px !important;
    font-size: 16px !important;
}
h1 {
    text-align: center;
    color: #333;
}
"""

# Gradio Interface
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("## 📲 Send SMS via Twilio + Python + Gradio")
    to_input = gr.Textbox(label="📞 Recipient Phone Number", placeholder="+91xxxxxxxxxx")
    msg_input = gr.Textbox(label="💬 Message", lines=5, placeholder="Type your SMS message here...")
    send_btn = gr.Button("🚀 Send SMS")
    status_output = gr.Textbox(label="Status")

    send_btn.click(fn=send_sms, inputs=[to_input, msg_input], outputs=status_output)

demo.launch()
