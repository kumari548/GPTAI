from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials, firestore

load_dotenv()

app = Flask(__name__)
# Initialize Firebase
import streamlit as st
import firebase_admin
from firebase_admin import credentials

firebase_credentials = {
    "type": st.secrets["FIREBASE_TYPE"],
    "project_id": st.secrets["FIREBASE_PROJECT_ID"],
    "private_key_id": st.secrets["FIREBASE_PRIVATE_KEY_ID"],
    "private_key": st.secrets["FIREBASE_PRIVATE_KEY"],
    "client_email": st.secrets["FIREBASE_CLIENT_EMAIL"],
    "client_id": st.secrets["FIREBASE_CLIENT_ID"],
    "token_uri": "https://oauth2.googleapis.com/token"
}

cred = credentials.Certificate(firebase_credentials)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Firestore DB
db = firestore.client()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Multiple Chats
all_chats = {
    "Chat 1": []
}

current_chat = "Chat 1"
def load_firebase_chats():

    global all_chats

    all_chats = {}

    docs = db.collection("chats").stream()

    for doc in docs:

        data = doc.to_dict()

        chat_name = data.get("chat", "Chat 1")

        if chat_name not in all_chats:
            all_chats[chat_name] = []

        all_chats[chat_name].append({
            "role":"user",
            "content":data["user"]
        })

        all_chats[chat_name].append({
            "role":"assistant",
            "content":data["ai"]
        })

    if len(all_chats) == 0:
        all_chats["Chat 1"] = []
load_firebase_chats()

system_prompt = """
You are FitnessGPT AI.

Answer ONLY fitness related questions.

If user asks outside fitness reply:
'I am FitnessGPT AI. Please ask only fitness-related questions.'
"""
def load_firebase_chats():

    global all_chats

    all_chats = {}

    docs = db.collection("chats").stream()

    for doc in docs:

        data = doc.to_dict()

        chat_name = data.get("chat", "Chat 1")

        if chat_name not in all_chats:
            all_chats[chat_name] = []

        all_chats[chat_name].append({
            "role":"user",
            "content":data["user"]
        })

        all_chats[chat_name].append({
            "role":"assistant",
            "content":data["ai"]
        })

    if len(all_chats) == 0:
        all_chats["Chat 1"] = []
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_chats")
def get_chats():

    global current_chat

    if current_chat not in all_chats:
        current_chat = list(all_chats.keys())[0]

    return jsonify({
        "chats": all_chats,
        "current": current_chat,
        "messages": all_chats[current_chat]
    })



@app.route("/new_chat", methods=["POST"])
def new_chat():

    global current_chat
    global all_chats

    chat_name = f"Chat {len(all_chats)+1}"

    all_chats[chat_name] = []

    current_chat = chat_name

    return jsonify({
        "chat": chat_name,
        "current": current_chat
    })

@app.route("/switch_chat", methods=["POST"])
def switch_chat():

    global current_chat

    data = request.get_json()

    current_chat = data["chat"]

    return jsonify({
        "current": current_chat,
        "messages": all_chats[current_chat]
    })

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data["message"]

    all_chats[current_chat].append({
        "role":"user",
        "content":user_message
    })

    messages = [
        {
            "role":"system",
            "content":system_prompt
        }
    ]

    messages.extend(all_chats[current_chat])

    completion = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=messages
    )

    ai_response = completion.choices[0].message.content

    all_chats[current_chat].append({
        "role":"assistant",
        "content":ai_response
    })

    # Save to Firebase
    db.collection("chats").add({
    "chat": current_chat,
    "user": user_message,
    "ai": ai_response
})

    return jsonify({
        "response": ai_response
    })
#if __name__ == "__main__":
 #S   app.run(debug=True)
