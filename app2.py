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
query = input("Ask the model a Question: ")
response = model.generate_content(query)
print(to_markdown(response.text))
print(response.prompt_feedback)
print(response.candidates)
