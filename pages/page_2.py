import streamlit as st
from PIL import Image

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

import requests
from openai import OpenAI

client = OpenAI(api_key='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')

def download_image(filename, url):
  response = requests.get(url)
  if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
  else:
        print("Error downloading image from URL:", url)

def filename_from_input(prompt):
   # Remove all non-alphanumeric characters from the prompt except spaces.
    alphanum = ""
    for character in prompt:
        if character.isalnum() or character == " ":
            alphanum += character
    # Split the alphanumeric prompt into words.
    # Take the first three words if there are more than three. Else, take all    of them.
    alphanumSplit = alphanum.split()
    if len(alphanumSplit) > 3:
        alphanumSplit = alphanumSplit[:3]
    # Join the words with underscores and return the result.
    return "images/" + "_".join(alphanumSplit)


# Create an image
# If model is not specified, the default is DALL-E-2.
def get_image(prompt, model="dall-e-2"):
    image = client.images.generate(
        prompt=prompt,
        model=model,
        n=1,
        size="1024x1024"
    )
    # Download the image

    filename = filename_from_input(prompt) + ".png"
    download_image(filename, image.data[0].url)

    return image


#print(response)

with st.form(key = "chat"):
    prompt = st.text_input('Enter some text', 'Enter some text')
    submitted = st.form_submit_button("Submit")
        
    if submitted:
        response = get_image(prompt)
        image = Image.open('images/'+prompt+'.png')
        st.image(image, caption='New Image')

