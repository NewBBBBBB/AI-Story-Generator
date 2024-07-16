#import
import streamlit as st
from openai import OpenAI
import requests


#methods
def generate_story(prompt):
    story_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role":
            "system",
            "content":
            "You are a bestseller story writer. You will take user's prompt and generate a 100 words short story for adults age 20-30."
        }, {
            "role": "user",
            "content": f'{prompt}'
        }],
        max_tokens=400,
        temperature=0.8)
    story = story_response.choices[0].message.content
    return story


def redefine_story(story):
    story_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role":
            "system",
            "content":
            "Based on the story given, design a detailed image prompt for the cover of this story. The image prompt should include the theme of the story with relevant colors, suitable for adults. No faces should be shown. The output should be between 100 characters."
        }, {
            "role": "user",
            "content": f'{story}'
        }],
        max_tokens=400,
        temperature=0.8)
    redefined = story_response.choices[0].message.content
    return redefined


def generate_image(redefined):
    cover_response = client.images.generate(model='dall-e-2',
                                            prompt=f'{redefined}',
                                            size='256x256',
                                            quality='standard',
                                            n=1)

    image_url = cover_response.data[0].url
    return image_url


api_key = st.secrets['OPENAI_SECRET']
client = OpenAI(api_key=api_key)

st.title("AI Story and Image Generator")
with st.form(' '):
    st.write('This is for user to key in information')
    msg = st.text_input('Some keywords to generate a story',
                        'Enter some keywords')
    submitted = st.form_submit_button("Submit")
    if msg.strip() != '' and msg != "Enter some keywords" and submitted:
        story = generate_story(msg)
        redefined = redefine_story(story)
        st.write(story)
        url = generate_image(redefined)
        st.markdown(f"<div style='text-align: center;'><img src='{url}' alt='Cover Image'></div>", unsafe_allow_html=True)
        st.write(redefined)
        st.balloons()
    elif msg.strip() == '':
        st.write('Please enter some keywords')
    elif msg == 'Enter some keywords':
        st.write('Please remove the default text and enter some keywords')


st.markdown(
    """
    <div style='display: flex; align-items: center;'>
        <img src='https://img.icons8.com/ios-filled/50/3498db/info.png' 
            alt='Information' 
            style='width: 20px; height: 20px; margin-right: 10px;'/>
        <span style='font-size: 16px; color: #3498db;'>Thank you for using the AI Story and Image Generator!</span>
    </div>
    """, 
    unsafe_allow_html=True
)
