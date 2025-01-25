import streamlit as st
import os
import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
import io
import re

# Set up the API key
os.environ["GEMINI_API_KEY"] = "your-gemini-api-key"

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start a chat session with no initial history
chat_session = model.start_chat(history=[])


def chat_with_ai(message):
    response = chat_session.send_message(message)
    return response.text


# Step 1: Chatbot for Museum Ticket Booking
option = st.selectbox(
    'Choose Museum:',
    ('Chhatrapati Shivaji Maharaj Vastu Sangrahalaya', 'Dr. Bhau Daji Lad Museum', 'National Gallery of Modern Art',
     'Mani Bhavan Gandhi Sangrahalaya', 'RBI Monetary Museum')
)
st.title("Museum Ticket Booking Chatbot")

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []

welcome_message = "Welcome to the Museum Ticket Booking Chatbot! I can help you book tickets for our museum. What would you like to do?"
st.write(welcome_message)

user_message = st.text_input("You: ")

context = f"You are a Museum Ticket booking chatbot. The user wants to visit {option}. The price for one Adult ticket is 350Rupees."

if st.button("Submit"):
    if user_message:
        st.session_state['conversation_history'].append(f"You: {user_message}")

        if user_message.lower() == 'book':
            ai_response = chat_with_ai(f"{context} Ask user for Name, Date, Time of visit, and Number of tickets.")
            st.session_state['conversation_history'].append(f"AI: {ai_response}")
            st.write("AI:", ai_response)

        elif user_message.lower() == 'info':
            ai_response = chat_with_ai(f"{context} Give information about {option}.")
            st.session_state['conversation_history'].append(f"AI: {ai_response}")
            st.write("AI:", ai_response)

        else:
            ai_response = chat_with_ai(f'{context} {user_message}')
            st.session_state['conversation_history'].append(f"AI: {ai_response}")
            st.write("AI:", ai_response)

if st.button("Confirm"):
    chat_history_text = "\n".join(st.session_state['conversation_history'])
    ai_response = chat_with_ai(
        f"Extract Name, Date, Time, and Number of tickets from the conversation. Return as 'info = [Name, Date, Time, No of tickets]'\n\n{chat_history_text}")
    st.write("AI:", ai_response)

    # Extract information using regex
    name = re.search(r"Name:\s*(\w+)", ai_response)
    date = re.search(r"Date:\s*([\w-]+)", ai_response)
    time = re.search(r"Time:\s*([\w:]+)", ai_response)
    tickets = re.search(r"Tickets:\s*(\d+)", ai_response)

    if name and date and time and tickets:
        st.session_state['ticket_info'] = [name.group(1), date.group(1), time.group(1), tickets.group(1)]
        st.write(f"Ticket Info: {st.session_state['ticket_info']}")
        with open('ticket_info.txt', 'w') as f:
            f.write(str(st.session_state['ticket_info']))
    else:
        st.write("Error: Could not extract ticket information.")


# Step 2: Ticket Generator
def generate_ticket(ticket_info):
    """Generates a simple ticket with the given info."""
    name, date, time, tickets = ticket_info

    # Create a blank ticket image
    ticket_width = 400
    ticket_height = 200
    ticket_image = Image.new('RGB', (ticket_width, ticket_height), color='white')

    draw = ImageDraw.Draw(ticket_image)

    # Load a font (ensure a valid path to a .ttf font file)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Add text to the ticket
    draw.text((10, 10), "Museum Ticket", fill='black', font=font)
    draw.text((10, 50), f"Name: {name}", fill='black', font=font)
    draw.text((10, 90), f"Date: {date}", fill='black', font=font)
    draw.text((10, 130), f"Time: {time}", fill='black', font=font)
    draw.text((10, 170), f"Tickets: {tickets}", fill='black', font=font)

    return ticket_image


# Example usage after confirming the booking
if st.button("Generate Ticket"):
    if 'ticket_info' in st.session_state and st.session_state['ticket_info']:
        ticket_image = generate_ticket(st.session_state['ticket_info'])

        # Save or display the ticket
        img_buffer = io.BytesIO()
        ticket_image.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        st.image(ticket_image, caption="Your Ticket", use_column_width=True)

        # Save the ticket image
        with open('ticket.png', 'wb') as f:
            f.write(img_buffer.getbuffer())

        st.write("Ticket generated and saved as 'ticket.png'.")
    else:
        st.write("No ticket information available to generate a ticket.")
