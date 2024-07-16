#import
import streamlit as st
from openai import OpenAI
import requests


#methods
def generate_story(prompt):
  story_response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{
          "role" : "system",
          "content": "You are a bestseller story writer. You will take user's prompt and generate a 100 words short story for adults age 20-30."
      },
      {
          "role" : "user",
          "content": f'{prompt}'
      }],
      max_tokens = 400,
      temperature = 0.8
  )
  story = story_response.choices[0].message.content
  return story

def redefine_story(story):
  story_response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{
          "role" : "system",
          "content": "Based on the story given, design a detailed image prompt for the cover of this story. The image prompt should include the theme of the story with relevant colors, suitable for adults. No faces should be shown. The output should be between 100 characters."
      },
      {
          "role" : "user",
          "content": f'{story}'
      }],
      max_tokens = 400,
      temperature = 0.8
  )
  redefined = story_response.choices[0].message.content
  return redefined

def generate_image(redefined):
  cover_response = client.images.generate(
      model='dall-e-2',
      prompt=f'{redefined}',
      size='256x256',
      quality='standard',
      n=1
  )

  image_url = cover_response.data[0].url
  return image_url


api_key= st.secrets['OPENAI_SECRET']
client=OpenAI(api_key=api_key)


with st.form(' '):
    st.write('This is for user to key in information')
    msg = st.text_input('Some keywords to generate a story','Enter some keywords')
    submitted = st.form_submit_button("Submit")
    if msg != "Enter some key words" and submitted:
        story = generate_story(msg)
        redefined = redefine_story(story)
        st.write(redefined)
        url=generate_image(redefined)
        st.image(url)