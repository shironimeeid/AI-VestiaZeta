import asyncio
from flask import Flask, render_template, request, jsonify
from characterai import aiocai

app = Flask(__name__)


# Ganti dengan token API
API_TOKEN = '2f15f76f**************'
client = aiocai.Client(API_TOKEN)
CHARACTER_ID = 'ISI DENGAN ID ZETA'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']

    response = asyncio.run(chat_with_character(CHARACTER_ID, user_input))
    return jsonify(response)

async def chat_with_character(char_id, user_input):
    try:
        me = await client.get_me()
        async with await client.connect() as chat:
            new, answer = await chat.new_chat(char_id, me.id)
            message = await chat.send_message(char_id, new.chat_id, user_input)
            return {'user_message': user_input, 'ai_message': message.text}
    except Exception as e:
        return {'user_message': user_input, 'ai_message': f"Error: {e}"}

if __name__ == '__main__':
    app.run(debug=True)
