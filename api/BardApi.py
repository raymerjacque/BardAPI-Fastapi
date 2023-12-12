from flask import Flask, request, jsonify
from bardapi import Bard
import requests
import os


BARD_API_KEY = os.environ.get('BARD_API_KEY') or 'eAi19LXBjrcfeackbhezep8ZqVqI0YEOTTJrqmbict0TDcYku3DAizOhu2HJ0cOyiWHZuQ.'



session = requests.Session()
session.headers = {
    "Host": "bard.google.com",
    "X-Same-Domain": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Origin": "https://bard.google.com",
    "Referer": "https://bard.google.com/",
}
session.cookies.set("__Secure-1PSID", BARD_API_KEY)

bard = Bard(token=BARD_API_KEY, session=session, timeout=30)

# Initial conversation

# personality = bard.get_answer("")['content']

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def get_response():
    try:
        user_input = request.args.get('user_input', '')
        response = process_input(user_input)
        return (response)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Start interactive loop

def process_input(user_input):
    # Continued conversation without setting a new session
    response = bard.get_answer(user_input)
    # print(f"Bard: {response['content']}")
    print("++++++++++++++++++++")
    # Display images if any
    result = {'content': response['content']}
    
    if 'images' in response:
        result['images'] = response['images']

    if 'links' in response:
        result['links'] = response['links']

    return result



if __name__ == '__main__':
    app.run(debug=True)
