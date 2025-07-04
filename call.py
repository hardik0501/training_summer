import gradio as gr
from twilio.rest import Client
from urllib.parse import quote

# Twilio credentials (WARNING: Do not expose in production!)
account_sid = ''
auth_token = ''
twilio_number = '+18145241368'

def make_call(to_number, message_to_speak):
    try:
        client = Client(account_sid, auth_token)

        # Create TwiML (Twilio Markup Language)
        twiml = f"<Response><Say>{message_to_speak}</Say></Response>"
        encoded_twiml = quote(twiml)
        twiml_url = f"http://twimlets.com/echo?Twiml={encoded_twiml}"

        # Initiate call
        call = client.calls.create(
            to=to_number,
            from_=twilio_number,
            url=twiml_url
        )

        return f"📞 Call initiated! SID: {call.sid}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# CSS for styling the UI
custom_css = """
input, textarea {
    padding: 10px;
    border: 2px solid #ccc;
    border-radius: 10px;
    font-size: 16px;
    width: 100%;
}
button {
    background-color: #007BFF !important;
    color: white !important;
    padding: 12px 24px !important;
    border: none;
    border-radius: 10px !important;
    font-size: 16px !important;
}
h1 {
    text-align: center;
    color: #2C3E50;
}
"""

# Gradio app
with gr.Blocks(css=custom_css) as app:
    gr.Markdown("## 📞 Twilio Voice Call with Text-to-Speech")
    with gr.Row():
        number_input = gr.Textbox(label="📲 Phone Number", placeholder="+91xxxxxxxxxx")
    message_input = gr.Textbox(label="💬 Message to Speak", lines=4, placeholder="Type the message to be spoken during the call...")
    call_btn = gr.Button("🚀 Make Call")
    result_output = gr.Textbox(label="Call Status")

    call_btn.click(fn=make_call, inputs=[number_input, message_input], outputs=result_output)

app.launch()
