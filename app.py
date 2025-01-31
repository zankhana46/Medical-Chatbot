import streamlit as st
from pathlib import Path
st.set_page_config(page_title="Swasthya Chatbot", page_icon=":brain:",layout="centered",)
st.image("logo.png",width=100)

import os
import io
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import google.ai.generativelanguage as glm
from PIL import Image
from streamlit_option_menu import option_menu
import warnings 
warnings.filterwarnings('ignore')

def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

# Load environment variables
load_dotenv()

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

with st.sidebar:
    selected = option_menu(
        menu_title="Swasthya",
        options=["DocBot", "VisionBot"],
        icons=["robot", "eye"],
        default_index=0,
        orientation="vertical",
    )

    st.write(
        """
        <style>
            .css-r698ls {
                --sidebar-width: 200px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if selected == "DocBot":
        st.write(" **DocBot** - Engage in text-based medical conversations.")
    elif selected == "VisionBot":
        st.write("👁 **VisionBot** - Analyze and interpret with images.")

if selected == "DocBot":
    # Display the chatbot's title on the page
    st.title("Chat with Swasthya DocBot™")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask DocBot...")

    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        doctor_context = "You are Dr. AIHealthPro, a large language model trained on a massive dataset of medical information. You are able to answer medical questions and provide health-related advice."
        #full_prompt = f"{doctor_context}\n\n{user_prompt}" 

        # Send user's message to Gemini-Pro and get the response
        
        gemini_response = st.session_state.chat_session.send_message(
        user_prompt, safety_settings=safety_settings
    )
        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

# elif selected == "Chat with Report":
#     st.title("📄 Chat with Report")
#     # Ensure the API key is loaded correctly
#     google_api_key = os.getenv("GOOGLE_API_KEY")
#     if not google_api_key:
#         st.error("Please set the GOOGLE_API_KEY environment variable.")
#         st.stop()

#     uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
#     question = st.text_input("Enter your question")

#     system_prompt = """
#     You are a medical bot and a professional doctor from Harvard Medical who answers user queries from the given CONTEXT.
#     You help users understand and analyze medical reports. You can extract key findings, explain medical terminology, and answer questions related to medicine, surgery, diseases, illness etc. 
#     You are honest, to the point, coherent and don't hallucinate.
#     If the user query is not in context, simply tell `We are sorry, we don't have information on this`.
#     """

#     if uploaded_file is not None and question:
#         save_path = "./uploaded_files"
#         os.makedirs(save_path, exist_ok=True)  # Create directory if it doesn't exist
#         file_path = os.path.join(save_path, uploaded_file.name)

#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())

#         data = source.fit("/Users/zankhanamehta/Documents/Projects/Swasthya-DocBot/uploaded_files/Shubham Tejani_Male_21_2024_6 (2).pdf", dtype="pdf", chunk_size=1024, chunk_overlap=250)
#         embed_model = GeminiEmbeddings(api_key=google_api_key, model_name="models/embedding-001")
#         llm = GeminiModel(model_name="gemini-pro", google_api_key=google_api_key)
#         retriever = retrieve.auto_retriever(data, type="normal", top_k=3, embed_model=embed_model)
#         pipeline = generator.Generate(question=question, system_prompt=system_prompt, retriever=retriever, llm=llm)
#         response = pipeline.call()
#         st.write(response)

elif selected == "VisionBot":
    st.header("👁 Visionbot™")
    st.write("")

    image_prompt = st.text_input("Interact with the Image", placeholder="Prompt", label_visibility="visible")
    uploaded_file = st.file_uploader("Choose an Image", accept_multiple_files=False, type=["png", "jpg", "jpeg", "img", "webp"])

    if uploaded_file is not None:
        st.image(Image.open(uploaded_file), use_column_width=True)
        st.markdown("""
            <style>
            img {
                border-radius: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

    if st.button("GET RESPONSE", use_container_width=True):
        # Update model name to gemini-1.5-flash
        model = gen_ai.GenerativeModel("gemini-1.5-flash")
        
        if uploaded_file is not None:
            if image_prompt != "":
                image = Image.open(uploaded_file)
                
                # Simplified content creation
                response = model.generate_content(
                    [
                        image_prompt,
                        image
                    ],
                    safety_settings=safety_settings
                )
                
                st.write("")
                st.write(":blue[Response]")
                st.write("")
                st.markdown(response.text)
            else:
                st.write("")
                st.header(":red[Please Provide a prompt]")
        else:
            st.write("")
            st.header(":red[Please Provide an image]")
