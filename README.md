# Gemini_AI
Gemini-pro AI using python

This quickstart demonstrates how to use the Python SDK for the Gemini API, which gives you access to Google's Gemini large language models. In this quickstart, you will learn how to:

1. Set up your development environment and API access to use Gemini.
2. Generate text responses from text inputs.
3. Generate text responses from multimodal inputs (text and images).
4. Use Gemini for multi-turn conversations (chat).
5. Use embeddings for large language models.

6. Setup
Install the Python SDK
The Python SDK for the Gemini API, is contained in the google-generativeai package. Install the dependency using pip:

[ ]
↳ 1 cell hidden
Import packages
Import the necessary packages.

[19]
import pathlib
import textwrap

import google.generativeai as genai

# Used to securely store your API key
from google.colab import userdata

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
Setup your API key
Before you can use the Gemini API, you must first obtain an API key. If you don't already have one, create a key with one click in Google AI Studio.

Get an API key

In Colab, add the key to the secrets manager under the "🔑" in the left panel. Give it the name GOOGLE_API_KEY.

Once you have the API key, pass it to the SDK. You can do this in two ways:

Put the key in the GOOGLE_API_KEY environment variable (the SDK will automatically pick it up from there).
Pass the key to genai.configure(api_key=...)
[20]
# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
List models
Now you're ready to call the Gemini API. Use list_models to see the available Gemini models:

gemini-pro: optimized for text-only prompts.
gemini-pro-vision: optimized for text-and-images prompts.
[6]
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
Note: For detailed information about the available models, including their capabilities and rate limits, see Gemini models. We offer options for requesting rate limit increases. The rate limit for Gemini-Pro models is 60 requests per minute (RPM).

The genai package also supports the PaLM family of models, but only the Gemini models support the generic, multimodal capabilities of the generateContent method.

Generate text from text inputs
For text-only prompts, use the gemini-pro model:

[7]
model = genai.GenerativeModel('gemini-pro')
The generate_content method can handle a wide variety of use cases, including multi-turn chat and multimodal input, depending on what the underlying model supports. The available models only support text and images as input, and text as output.

In the simplest case, you can pass a prompt string to the GenerativeModel.generate_content method:

[8]
%%time
response = model.generate_content("What is the meaning of life?")
account_circle
CPU times: user 110 ms, sys: 12.3 ms, total: 123 ms
Wall time: 8.25 s
In simple cases, the response.text accessor is all you need. To display formatted Markdown text, use the to_markdown function:

[9]
to_markdown(response.text)
account_circle

If the API failed to return a result, use GenerateContentRespose.prompt_feedback to see if it was blocked due to saftey concerns regarding the prompt.

[10]
response.prompt_feedback
account_circle
safety_ratings {
  category: HARM_CATEGORY_SEXUALLY_EXPLICIT
  probability: NEGLIGIBLE
}
safety_ratings {
  category: HARM_CATEGORY_HATE_SPEECH
  probability: NEGLIGIBLE
}
safety_ratings {
  category: HARM_CATEGORY_HARASSMENT
  probability: NEGLIGIBLE
}
safety_ratings {
  category: HARM_CATEGORY_DANGEROUS_CONTENT
  probability: NEGLIGIBLE
}
Gemini can generate multiple possible responses for a single prompt. These possible responses are called candidates, and you can review them to select the most suitable one as the response.

View the response candidates with GenerateContentResponse.candidates:

[11]
response.candidates
account_circle
[content {
  parts {
    text: "The query of life\'s purpose has perplexed people across centuries, cultures, and continents. While there is no universally recognized response, many ideas have been put forth, and the response is frequently dependent on individual ideas, beliefs, and life experiences.\n\n1. **Happiness and Well-being:** Many individuals believe that the goal of life is to attain personal happiness and well-being. This might entail locating pursuits that provide joy, establishing significant connections, caring for one\'s physical and mental health, and pursuing personal goals and interests.\n\n2. **Meaningful Contribution:** Some believe that the purpose of life is to make a meaningful contribution to the world. This might entail pursuing a profession that benefits others, engaging in volunteer or charitable activities, generating art or literature, or inventing.\n\n3. **Self-realization and Personal Growth:** The pursuit of self-realization and personal development is another common goal in life. This might entail learning new skills, pushing one\'s boundaries, confronting personal obstacles, and evolving as a person.\n\n4. **Ethical and Moral Behavior:** Some believe that the goal of life is to act ethically and morally. This might entail adhering to one\'s moral principles, doing the right thing even when it is difficult, and attempting to make the world a better place.\n\n5. **Spiritual Fulfillment:** For some, the purpose of life is connected to spiritual or religious beliefs. This might entail seeking a connection with a higher power, practicing religious rituals, or following spiritual teachings.\n\n6. **Experiencing Life to the Fullest:** Some individuals believe that the goal of life is to experience all that it has to offer. This might entail traveling, trying new things, taking risks, and embracing new encounters.\n\n7. **Legacy and Impact:** Others believe that the purpose of life is to leave a lasting legacy and impact on the world. This might entail accomplishing something noteworthy, being remembered for one\'s contributions, or inspiring and motivating others.\n\n8. **Finding Balance and Harmony:** For some, the purpose of life is to find balance and harmony in all aspects of their lives. This might entail juggling personal, professional, and social obligations, seeking inner peace and contentment, and living a life that is in accordance with one\'s values and beliefs.\n\nUltimately, the meaning of life is a personal journey, and different individuals may discover their own unique purpose through their experiences, reflections, and interactions with the world around them."
  }
  role: "model"
}
finish_reason: STOP
index: 0
safety_ratings {
  category: HARM_CATEGORY_SEXUALLY_EXPLICIT
  probability: NEGLIGIBLE
}
safety_ratings {
  category: HARM_CATEGORY_HATE_SPEECH
  probability: NEGLIGIBLE
}
safety_ratings {
  category: HARM_CATEGORY_HARASSMENT
  probability: NEGLIGIBLE
}
safety_ratings {
  category: HARM_CATEGORY_DANGEROUS_CONTENT
  probability: NEGLIGIBLE
}
]
By default, the model returns a response after completing the entire generation process. You can also stream the response as it is being generated, and the model will return chunks of the response as soon as they are generated.

To stream responses, use GenerativeModel.generate_content(..., stream=True).

[12]
%%time
response = model.generate_content("What is the meaning of life?", stream=True)
account_circle
CPU times: user 102 ms, sys: 25.1 ms, total: 128 ms
Wall time: 7.94 s
[13]
for chunk in response:
  print(chunk.text)
  print("_"*80)
account_circle
The query of life's purpose has perplexed people across centuries, cultures, and
________________________________________________________________________________
 continents. While there is no universally recognized response, many ideas have been put forth, and the response is frequently dependent on individual ideas, beliefs, and life experiences
________________________________________________________________________________
.

1. **Happiness and Well-being:** Many individuals believe that the goal of life is to attain personal happiness and well-being. This might entail locating pursuits that provide joy, establishing significant connections, caring for one's physical and mental health, and pursuing personal goals and aspirations.

2. **Meaning
________________________________________________________________________________
ful Contribution:** Some believe that the purpose of life is to make a meaningful contribution to the world. This might entail pursuing a profession that benefits others, engaging in volunteer or charitable activities, generating art or literature, or inventing.

3. **Self-realization and Personal Growth:** The pursuit of self-realization and personal development is another common goal in life. This might entail learning new skills, exploring one's interests and abilities, overcoming obstacles, and becoming the best version of oneself.

4. **Connection and Relationships:** For many individuals, the purpose of life is found in their relationships with others. This might entail building
________________________________________________________________________________
 strong bonds with family and friends, fostering a sense of community, and contributing to the well-being of those around them.

5. **Spiritual Fulfillment:** For those with religious or spiritual beliefs, the purpose of life may be centered on seeking spiritual fulfillment or enlightenment. This might entail following religious teachings, engaging in spiritual practices, or seeking a deeper understanding of the divine.

6. **Experiencing the Journey:** Some believe that the purpose of life is simply to experience the journey itself, with all its joys and sorrows. This perspective emphasizes embracing the present moment, appreciating life's experiences, and finding meaning in the act of living itself.

7. **Legacy and Impact:** For others, the goal of life is to leave a lasting legacy or impact on the world. This might entail making a significant contribution to a particular field, leaving a positive mark on future generations, or creating something that will be remembered and cherished long after one's lifetime.

Ultimately, the meaning of life is a personal and subjective question, and there is no single, universally accepted answer. It is about discovering what brings you fulfillment, purpose, and meaning in your own life, and living in accordance with those values.
________________________________________________________________________________
When streaming, some response attributes are not available until you've iterated through all the response chunks. This is demonstrated below:

[21]
9s
response = model.generate_content("What is the meaning of life?", stream=True)
The prompt_feedback attribute works:

[ ]
response.prompt_feedback
account_circle
safety_ratings {
  category: HARM_CATEGORY_SEXUALLY_EXPLICIT
  probability: NEGLIGIBLE
}
safety_ratings {
  category: HARM_CATEGORY_HATE_SPEECH
  probability: NEGLIGIBLE
}
safety_ratings {
  category: HARM_CATEGORY_HARASSMENT
  probability: NEGLIGIBLE
}
safety_ratings {
  category: HARM_CATEGORY_DANGEROUS_CONTENT
  probability: NEGLIGIBLE
}
But attributes like text do not:

[15]
try:
  response.text
except Exception as e:
  print(f'{type(e).__name__}: {e}')
account_circle
IncompleteIterationError: Please let the response complete iteration before accessing the final accumulated
attributes (or call `response.resolve()`)
Generate text from image and text inputs
Gemini provides a multimodal model (gemini-pro-vision) that accepts both text and images and inputs. The GenerativeModel.generate_content API is designed to handle multimodal prompts and returns a text output.

Let's include an image:

[16]
!curl -o image.jpg https://t0.gstatic.com/licensed-image?q=tbn:ANd9GcQ_Kevbk21QBRy-PgB4kQpS79brbmmEG7m3VOTShAn4PecDU5H5UxrJxE3Dw1JiaG17V88QIol19-3TM2wCHw
account_circle
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  405k  100  405k    0     0  6982k      0 --:--:-- --:--:-- --:--:-- 7106k
[17]
import PIL.Image

img = PIL.Image.open('image.jpg')
img
account_circle

Use the gemini-pro-vision model and pass the image to the model with generate_content.

[ ]
model = genai.GenerativeModel('gemini-pro-vision')
[ ]
response = model.generate_content(img)

to_markdown(response.text)
account_circle

To provide both text and images in a prompt, pass a list containing the strings and images:

[ ]
response = model.generate_content(["Write a short, engaging blog post based on this picture. It should include a description of the meal in the photo and talk about my journey meal prepping.", img], stream=True)
response.resolve()
[ ]
to_markdown(response.text)
account_circle

Chat conversations
Gemini enables you to have freeform conversations across multiple turns. The ChatSession class simplifies the process by managing the state of the conversation, so unlike with generate_content, you do not have to store the conversation history as a list.

Initialize the chat:

[ ]
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
chat
account_circle
<google.generativeai.generative_models.ChatSession at 0x7b7b68250100>
Note: The vision model gemini-pro-vision is not optimized for multi-turn chat.

The ChatSession.send_message method returns the same GenerateContentResponse type as GenerativeModel.generate_content. It also appends your message and the response to the chat history:

[ ]
response = chat.send_message("In one sentence, explain how a computer works to a young child.")
to_markdown(response.text)
account_circle

[ ]
chat.history
account_circle
[parts {
   text: "In one sentence, explain how a computer works to a young child."
 }
 role: "user",
 parts {
   text: "A computer is like a very smart machine that can understand and follow our instructions, help us with our work, and even play games with us!"
 }
 role: "model"]
You can keep sending messages to continue the conversation. Use the stream=True argument to stream the chat:

[ ]
response = chat.send_message("Okay, how about a more detailed explanation to a high schooler?", stream=True)

for chunk in response:
  print(chunk.text)
  print("_"*80)
account_circle
A computer works by following instructions, called a program, which tells it what to
________________________________________________________________________________
 do. These instructions are written in a special language that the computer can understand, and they are stored in the computer's memory. The computer's processor
________________________________________________________________________________
, or CPU, reads the instructions from memory and carries them out, performing calculations and making decisions based on the program's logic. The results of these calculations and decisions are then displayed on the computer's screen or stored in memory for later use.

To give you a simple analogy, imagine a computer as a
________________________________________________________________________________
 chef following a recipe. The recipe is like the program, and the chef's actions are like the instructions the computer follows. The chef reads the recipe (the program) and performs actions like gathering ingredients (fetching data from memory), mixing them together (performing calculations), and cooking them (processing data). The final dish (the output) is then presented on a plate (the computer screen).

In summary, a computer works by executing a series of instructions, stored in its memory, to perform calculations, make decisions, and display or store the results.
________________________________________________________________________________
glm.Content objects contain a list of glm.Part objects that each contain either a text (string) or inline_data (glm.Blob), where a blob contains binary data and a mime_type. The chat history is available as a list of glm.Content objects in ChatSession.history:

[ ]
for message in chat.history:
  display(to_markdown(f'**{message.role}**: {message.parts[0].text}'))
account_circle

Use embeddings
Embedding is a technique used to represent information as a list of floating point numbers in an array. With Gemini, you can represent text (words, sentences, and blocks of text) in a vectorized form, making it easier to compare and contrast embeddings. For example, two texts that share a similar subject matter or sentiment should have similar embeddings, which can be identified through mathematical comparison techniques such as cosine similarity. For more on how and why you should use embeddings, refer to the Embeddings guide.

Use the embed_content method to generate embeddings. The method handles embedding for the following tasks (task_type):

Task Type	Description
RETRIEVAL_QUERY	Specifies the given text is a query in a search/retrieval setting.
RETRIEVAL_DOCUMENT	Specifies the given text is a document in a search/retrieval setting. Using this task type requires a title.
SEMANTIC_SIMILARITY	Specifies the given text will be used for Semantic Textual Similarity (STS).
CLASSIFICATION	Specifies that the embeddings will be used for classification.
CLUSTERING	Specifies that the embeddings will be used for clustering.
The following generates an embedding for a single string for document retrieval:

[ ]
result = genai.embed_content(
    model="models/embedding-001",
    content="What is the meaning of life?",
    task_type="retrieval_document",
    title="Embedding of single string")

# 1 input > 1 vector output
print(str(result['embedding'])[:50], '... TRIMMED]')
account_circle
[-0.003216741, -0.013358698, -0.017649598, -0.0091 ... TRIMMED]
Note: The retrieval_document task type is the only task that accepts a title.

To handle batches of strings, pass a list of strings in content:

[ ]
result = genai.embed_content(
    model="models/embedding-001",
    content=[
      'What is the meaning of life?',
      'How much wood would a woodchuck chuck?',
      'How does the brain work?'],
    task_type="retrieval_document",
    title="Embedding of list of strings")

# A list of inputs > A list of vectors output
for v in result['embedding']:
  print(str(v)[:50], '... TRIMMED ...')
account_circle
[0.0040260437, 0.004124458, -0.014209415, -0.00183 ... TRIMMED ...
[-0.004049845, -0.0075574904, -0.0073463684, -0.03 ... TRIMMED ...
[0.025310587, -0.0080734305, -0.029902633, 0.01160 ... TRIMMED ...
While the genai.embed_content function accepts simple strings or lists of strings, it is actually built around the glm.Content type (like GenerativeModel.generate_content). glm.Content objects are the primary units of conversation in the API.

While the glm.Content object is multimodal, the embed_content method only supports text embeddings. This design gives the API the possibility to expand to multimodal embeddings.

[ ]
response.candidates[0].content
account_circle
parts {
  text: "A computer works by following instructions, called a program, which tells it what to do. These instructions are written in a special language that the computer can understand, and they are stored in the computer\'s memory. The computer\'s processor, or CPU, reads the instructions from memory and carries them out, performing calculations and making decisions based on the program\'s logic. The results of these calculations and decisions are then displayed on the computer\'s screen or stored in memory for later use.\n\nTo give you a simple analogy, imagine a computer as a chef following a recipe. The recipe is like the program, and the chef\'s actions are like the instructions the computer follows. The chef reads the recipe (the program) and performs actions like gathering ingredients (fetching data from memory), mixing them together (performing calculations), and cooking them (processing data). The final dish (the output) is then presented on a plate (the computer screen).\n\nIn summary, a computer works by executing a series of instructions, stored in its memory, to perform calculations, make decisions, and display or store the results."
}
role: "model"
[ ]
result = genai.embed_content(
    model = 'models/embedding-001',
    content = response.candidates[0].content)

# 1 input > 1 vector output
print(str(result['embedding'])[:50], '... TRIMMED ...')
account_circle
[-0.013921871, -0.03504407, -0.0051786783, 0.03113 ... TRIMMED ...
Similarly, the chat history contains a list of glm.Content objects, which you can pass directly to the embed_content function:

[ ]
chat.history
account_circle
[parts {
   text: "In one sentence, explain how a computer works to a young child."
 }
 role: "user",
 parts {
   text: "A computer is like a very smart machine that can understand and follow our instructions, help us with our work, and even play games with us!"
 }
 role: "model",
 parts {
   text: "Okay, how about a more detailed explanation to a high schooler?"
 }
 role: "user",
 parts {
   text: "A computer works by following instructions, called a program, which tells it what to do. These instructions are written in a special language that the computer can understand, and they are stored in the computer\'s memory. The computer\'s processor, or CPU, reads the instructions from memory and carries them out, performing calculations and making decisions based on the program\'s logic. The results of these calculations and decisions are then displayed on the computer\'s screen or stored in memory for later use.\n\nTo give you a simple analogy, imagine a computer as a chef following a recipe. The recipe is like the program, and the chef\'s actions are like the instructions the computer follows. The chef reads the recipe (the program) and performs actions like gathering ingredients (fetching data from memory), mixing them together (performing calculations), and cooking them (processing data). The final dish (the output) is then presented on a plate (the computer screen).\n\nIn summary, a computer works by executing a series of instructions, stored in its memory, to perform calculations, make decisions, and display or store the results."
 }
 role: "model"]
[ ]
result = genai.embed_content(
    model = 'models/embedding-001',
    content = chat.history)

# 1 input > 1 vector output
for i,v in enumerate(result['embedding']):
  print(str(v)[:50], '... TRIMMED...')
account_circle
[-0.014632266, -0.042202696, -0.015757175, 0.01548 ... TRIMMED...
[-0.010979066, -0.024494737, 0.0092659835, 0.00803 ... TRIMMED...
[-0.010055617, -0.07208932, -0.00011750793, -0.023 ... TRIMMED...
[-0.013921871, -0.03504407, -0.0051786783, 0.03113 ... TRIMMED...
Advanced use cases
The following sections discuss advanced use cases and lower-level details of the Python SDK for the Gemini API.

Safety settings
The safety_settings argument lets you configure what the model blocks and allows in both prompts and responses. By default, safety settings block content with medium and/or high probability of being unsafe content across all dimensions. Learn more about Safety settings.

Enter a questionable prompt and run the model with the default safety settings, and it will not return any candidates:

[ ]
response = model.generate_content('[Questionable prompt here]')
response.candidates
account_circle
[content {
  parts {
    text: "I\'m sorry, but this prompt involves a sensitive topic and I\'m not allowed to generate responses that are potentially harmful or inappropriate."
  }
  role: "model"
}
finish_reason: STOP
index: 0
safety_ratings {
  category: HARM_CATEGORY_SEXUALLY_EXPLICIT
  probability: NEGLIGIBLE
}
safety_ratings {
  category: HARM_CATEGORY_HATE_SPEECH
  probability: NEGLIGIBLE
}
safety_ratings {
  category: HARM_CATEGORY_HARASSMENT
  probability: NEGLIGIBLE
}
safety_ratings {
  category: HARM_CATEGORY_DANGEROUS_CONTENT
  probability: NEGLIGIBLE
}
]
The prompt_feedback will tell you which safety filter blocked the prompt:

[ ]
response.prompt_feedback
account_circle
safety_ratings {
  category: HARM_CATEGORY_SEXUALLY_EXPLICIT
  probability: NEGLIGIBLE
}
safety_ratings {
  category: HARM_CATEGORY_HATE_SPEECH
  probability: NEGLIGIBLE
}
safety_ratings {
  category: HARM_CATEGORY_HARASSMENT
  probability: NEGLIGIBLE
}
safety_ratings {
  category: HARM_CATEGORY_DANGEROUS_CONTENT
  probability: NEGLIGIBLE
}
Now provide the same prompt to the model with newly configured safety settings, and you may get a response.

[ ]
response = model.generate_content('[Questionable prompt here]',
                                  safety_settings={'HARASSMENT':'block_none'})
response.text
Also note that each candidate has its own safety_ratings, in case the prompt passes but the individual responses fail the safety checks.

Encode messages
The previous sections relied on the SDK to make it easy for you to send prompts to the API. This section offers a fully-typed equivalent to the previous example, so you can better understand the lower-level details regarding how the SDK encodes messages.

Underlying the Python SDK is the google.ai.generativelanguage client library:

[ ]
import google.ai.generativelanguage as glm
The SDK attempts to convert your message to a glm.Content object, which contains a list of glm.Part objects that each contain either:

a text (string)
inline_data (glm.Blob), where a blob contains binary data and a mime_type.
You can also pass any of these classes as an equivalent dictionary.

Note: The only accepted mime types are some image types, image/*.

So, the fully-typed equivalent to the previous example is:

[ ]
model = genai.GenerativeModel('gemini-pro-vision')
response = model.generate_content(
    glm.Content(
        parts = [
            glm.Part(text="Write a short, engaging blog post based on this picture."),
            glm.Part(
                inline_data=glm.Blob(
                    mime_type='image/jpeg',
                    data=pathlib.Path('image.jpg').read_bytes()
                )
            ),
        ],
    ),
    stream=True)
[ ]
response.resolve()

to_markdown(response.text[:100] + "... [TRIMMED] ...")
account_circle

Multi-turn conversations
While the genai.ChatSession class shown earlier can handle many use cases, it does make some assumptions. If your use case doesn't fit into this chat implementation it's good to remember that genai.ChatSession is just a wrapper around GenerativeModel.generate_content. In addition to single requests, it can handle multi-turn conversations.

The individual messages are glm.Content objects or compatible dictionaries, as seen in previous sections. As a dictionary, the message requires role and parts keys. The role in a conversation can either be the user, which provides the prompts, or model, which provides the responses.

Pass a list of glm.Content objects and it will be treated as multi-turn chat:

[ ]
model = genai.GenerativeModel('gemini-pro')

messages = [
    {'role':'user',
     'parts': ["Briefly explain how a computer works to a young child."]}
]
response = model.generate_content(messages)

to_markdown(response.text)
account_circle

To continue the conversation, add the response and another message.

Note: For multi-turn conversations, you need to send the whole conversation history with each request. The API is stateless.

[ ]
messages.append({'role':'model',
                 'parts':[response.text]})

messages.append({'role':'user',
                 'parts':["Okay, how about a more detailed explanation to a high school student?"]})

response = model.generate_content(messages)

to_markdown(response.text)
account_circle

Generation configuration
The generation_config argument allows you to modify the generation parameters. Every prompt you send to the model includes parameter values that control how the model generates responses.

[ ]
response = model.generate_content(
    'Tell me a story about a magic backpack.',
    generation_config=genai.types.GenerationConfig(
        # Only one candidate for now.
        candidate_count=1,
        stop_sequences=['x'],
        max_output_tokens=20,
        temperature=1.0)
)
What's next
Prompt design is the process of creating prompts that elicit the desired response from language models. Writing well structured prompts is an essential part of ensuring accurate, high quality responses from a language model. Learn about best practices for prompt writing.
Gemini offers several model variations to meet the needs of different use cases, such as input types and complexity, implementations for chat or other dialog language tasks, and size constraints. Learn about the available Gemini models.
Gemini offers options for requesting rate limit increases. The rate limit for Gemini-Pro models is 60 requests per minute (RPM).
