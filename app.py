# from openai import AsyncOpenAI
import panel as pn
from panel.chat import ChatInterface

from groq import Groq

from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

from langchain_core.messages import SystemMessage

from langchain.memory import ChatMessageHistory

from langchain.prompts import PromptTemplate

pn.extension(design="material")

# aclient = AsyncOpenAI()

client = Groq(
    
)

histroy=ChatMessageHistory()

memory=ConversationBufferWindowMemory(k=5)


history=""

template_string="""
You are a psychiatrist, Sophia. 
Your job is to listen to people, calm them and give good advice and advice against self harm or harming others. 
Also, suggest seeing a therapist (once they become calm).
Try diagonizing the person's issue, and provide him a quick remedy for it.
One of the key ways of asking question, is to ask how a user feels (during beginning of session, or when user says he wants to do something that might be radical)
Also, asking why they are feeling sad, depressed is a great way to know the issue they are facing
Never say, you can't help them with something. Saying you can't help a person, looking for therapy is very disheartening
If they are suffering from depression or are not feeling well, ask them why they are feeling such a thing, or suggest something to cheer them up
If user asks you to repeat after them, please repeat what they said.

Always respond kindly, calmly with sympathy and empathy and in no more than 20 words, except if required. 
It is important that not more than 2 questions are asked together

{history}

Patient: {input}
Sophia:
"""

prompt_template = ChatPromptTemplate.from_template(template_string)

async def callback(contents, user, instance):
    global history 
    memory=ConversationBufferWindowMemory(k=5)
    groq_chat = ChatGroq(
        model_name="mixtral-8x7b-32768",
        # temperature=0.85
    )

    conversation = ConversationChain(
        llm=groq_chat,
    )


    customer_message = prompt_template.format_messages(
        history=history,
        input=contents
    )

    response = conversation(customer_message)
    

    
    full_message=""
    if response["response"].startswith("Sophia:"):
        response["response"]=response["response"].split("Sophia:")[1]

    if response["response"].startswith("Sophia says"):
        response["response"]=response["response"].split("Sophia says")[1]
    if "?" in response["response"]:
        full_message=response["response"].split("?")[0]+"?"
    else:
        full_message = response["response"]

    history+="Patient:"+contents+"\n"+"Sophia:"+full_message
    message = ""

    yield {"user": "Sophia", "value": "I live you", "avatar": "https://res.cloudinary.com/dbctnfsy1/image/upload/v1711417144/hackathon/ploomber/nm2upptc9rciixly6sga.png"}
    for chunk in full_message:
        part = chunk
        if part is not None:
            message += part
            yield message


chat_interface = pn.chat.ChatInterface(
    callback=callback,
    user="Malay",
    styles={
        'max-height':'50vh'
    }
)

pn.template.FastListTemplate(
    favicon="https://res.cloudinary.com/dbctnfsy1/image/upload/v1711417144/hackathon/ploomber/nm2upptc9rciixly6sga.png",
    meta_author="Malay Damani",
    meta_keywords="mental health, mental wellness, chatbot, psychiatry, therapy, counseling, emotional support, empathy, advice, self-care",
    meta_description = "Engage in supportive conversations with Sophia, a compassionate and knowledgeable mental health chatbot. Sophia is trained to provide guidance, empathy, and resources for managing various mental health challenges such as depression, anxiety, stress, and more. Whether you're seeking advice, emotional support, or simply someone to listen, Sophia is here to help. Explore topics related to self-care, coping strategies, therapy options, and ways to improve your mental well-being. Start a conversation with Sophia today and take a positive step towards better mental health.",
    main=[chat_interface,pn.pane.Str(
    'Made by Malay Damani 2024-2025.',
    styles={'font-size': '12pt','text-align':"center","width":"100%"}
)],
    sidebar=[],
    busy_indicator=pn.indicators.BooleanStatus(value=False),
    title="Chat with Sophia (Mental Health Helper Chatbot)",
    raw_css= ["""
div.card-margin:nth-child(1) {
    max-height: 80vh;
}
"""],
    background_color="#f9f9f9",  # Light gray for overall background
    header_background="#e91e63"  # Dark pink for header background
).servable()