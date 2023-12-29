import textwrap
from IPython.display import display, Markdown
import google.generativeai as genai


# Function to convert plain text to Markdown format
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# Set up the Generative AI configuration with the API key
genai.configure(api_key='AIzaSyBOc7WOykXVHvnU-GsMgCYZwoBqFERjQFI')

# Create a Generative Model instance (assuming 'gemini-pro' is a valid model)
model = genai.GenerativeModel('gemini-pro')

while True:
    # Get user input for the query
    user_query = input("Ask the model a question (or enter 'exit' to quit): ")

    if user_query.lower() == 'exit':
        break

    # Generate content based on the user's query
    response = model.generate_content(user_query)

    # Display the generated content in Markdown format
    display(to_markdown(response.text))

    # Display additional information for analysis
    print(f"Prompt Feedback: {response.prompt_feedback}")
    print(f"Candidates: {response.candidates}")

    for chunk in response:
        print(chunk.text)
        print("_" * 80)
