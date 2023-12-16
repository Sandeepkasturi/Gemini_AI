# Sandeep Kasturi
# Code from Google Colab- Goolge AI Studio for Developers
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
#GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')

genai.configure(api_key='YOUR_OWN_API_KEY')
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("What is the meaning of life?") #Here you can write your own query.
print(to_markdown(response.text))
print(response.prompt_feedback)
print(response.candidates)
