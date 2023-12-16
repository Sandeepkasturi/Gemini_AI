import textwrap
from IPython.display import display, Markdown
from google.generativeai import genai

# Function to convert plain text to Markdown format
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Set up the Generative AI configuration with the API key
genai.configure(api_key='YOUR_OWN_API_KEY')

# Create a Generative Model instance (assuming 'gemini-pro' is a valid model)
model = genai.GenerativeModel('gemini-pro')

# Get user input for the query
user_query = input("Ask the model a question: ")

# Generate content based on the user's query
response = model.generate_content(user_query)

# Display the generated content in Markdown format
display(to_markdown(response.text))

# Display additional information for analysis
print(f"Prompt Feedback: {response.prompt_feedback}")
print(f"Candidates: {response.candidates}")
