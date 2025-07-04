import gradio as gr
from twilio.rest import Client

# Twilio credentials (NOTE: Secure these in production!)
account_sid = ''
auth_token = ''
twilio_whatsapp_number = 'whatsapp:+14155238886'  # Twilio sandbox number

def send_whatsapp(to_number, message_text):
    try:
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_=twilio_whatsapp_number,
            body=message_text,
            to=f'whatsapp:{to_number}'  # format: +91xxxxxxxxxx
        )

        return f"✅ WhatsApp message sent!\nSID: {message.sid}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Custom CSS
custom_css = """
input, textarea {
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 10px;
  font-size: 16px;
}
button {
  background-color: #25D366 !important;
  color: white !important;
  padding: 12px 24px !important;
  border: none;
  border-radius: 10px !important;
  font-size: 16px !important;
}
h1 {
  text-align: center;
  color: #128C7E;
}
"""

# Gradio App
with gr.Blocks(css=custom_css) as app:
    gr.Markdown("## 📲 Send WhatsApp Message via Twilio API")
    phone_input = gr.Textbox(label="📞 Recipient Number", placeholder="+91xxxxxxxxxx")
    message_input = gr.Textbox(label="💬 Message", lines=5, placeholder="Type your WhatsApp message...")
    send_button = gr.Button("🚀 Send Message")
    status_output = gr.Textbox(label="Status")

    send_button.click(fn=send_whatsapp, inputs=[phone_input, message_input], outputs=status_output)

app.launch()

