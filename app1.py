from openai import OpenAI
from flask import Flask, render_template, request
import json

app = Flask(__name__)

client = OpenAI(api_key="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")

messagesList = []

# Route to render the chat interface
@app.route('/')
def index():
    return render_template('chat_interface.html')

# Route to handle user messages and send them to ChatGPT
@app.route('/send-message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        user_message = request.form['user_message']

        #Prepare headers and data for the API request
        headers = {
            "Content-Type": "application/json"
        }

        messagesList.append({"role" : "user", "content" : user_message})

        chat_completion = client.chat.completions.create(
            messages= messagesList,
            model="gpt-3.5-turbo",
        )

        answer = chat_completion.choices[0].message.content
        #print("Answer: ", answer)
        messagesList.append({"role" : "assistant", "content" : answer})

        if answer:
            return json.dumps({'status': 'OK', 'response': answer})
        else:
            return json.dumps({'status': 'ERROR', 'response': 'Failed to get response from ChatGPT API'})

if __name__ == '__main__':
    app.run(debug=True)
