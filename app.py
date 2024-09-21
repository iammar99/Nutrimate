import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="NutriMate AI", page_icon=":bar_chart:")


def feet_to_meters(height_in_feet):
    return height_in_feet * 0.3048


client = Groq(
    api_key = st.secrets["groq_API_key"]
)

def generate_diet_plan(weight, height, age):
    user_input = f"The user is {age} years old, weighs {weight} kg, and is {height} feet tall. Generate a diet plan suitable for their profile. Format the diet plan as follows:\n\n" \
                 "7:00 AM  Breakfast\n- [meal details]\n\n" \
                 "10:00 AM  Mid-Morning Snack\n- [meal details]\n\n" \
                 "1:00 PM  Lunch\n- [meal details]\n\n" \
                 "4:00 PM  Afternoon Snack\n- [meal details]\n\n" \
                 "7:00 PM  Dinner\n- [meal details]\n\n" \
                 "9:00 PM  Evening Snack\n- [meal details]"

    try:
        # Create a chat completion using the Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a world-class nutritionist AI. Provide personalized diet plans based on user inputs such as weight, height, and age."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            model="llama3-8b-8192",  # Replace with the appropriate model name
            max_tokens=500,  # Adjust as needed
            temperature=0.7  # Adjust the temperature for creativity
        )
        
        # Extract and return the generated diet plan text
        generated_text = chat_completion.choices[0].message.content
        return generated_text

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Page title
st.title("NutriMate AI")

# Sidebar inputs
with st.sidebar:
    st.header("Input Panel")
    
    weight = st.number_input("Enter your weight in kg:", min_value=0.0, step=0.1)
    height = st.number_input("Enter your height in feet:", min_value=0.0, step=0.1)
    age = st.number_input("Enter your age:", format="%d", step=1)
    st.button("Genrate Diet Plan")



if weight and height and age:
    # Convert height to meters for potential future use (if needed)
    height_meters = feet_to_meters(height)
    
    # Generate and display the diet plan
    result = generate_diet_plan(weight, height, age)
    st.write(result)
    
    

