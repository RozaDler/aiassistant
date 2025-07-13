import streamlit as st
from utils.api import ask_question

def render_chat():
    st.subheader("Chat with your assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render existing chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input and response
    if user_input := st.chat_input("Ask a question..."):
        # Display user message and add to history
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get response from API
        response = ask_question(user_input)

        with st.chat_message("assistant"):
            if response.status_code == 200:
                data = response.json()
                answer = data.get("response", "Sorry, I couldn't get a response.")
                sources = data.get("sources", [])
                
                # Combine the answer and sources into one message
                full_response = answer
                if sources:
                    source_links = "\n".join([f"- '{src}'" for src in sources if src])
                    if source_links:
                        full_response += f"\n\n---\n**Sources:**\n{source_links}"
                
                st.markdown(full_response)
                # Add the complete response to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                # Handle API errors
                st.error(f"Error: {response.text}")

# import streamlit as st
# from utils.api import ask_question

# def render_chat():
#     st.subheader("Chat with your assistant")

#     if "messages" not in st.session_state:
#         st.session_state.messages=[]

#     # render existing chat history
#     for msg in st.session_state.messages:
#         st.chat_message(msg["role"]).markdown(msg["content"])
    
#     # input and response
#     user_input = st.chat_input("Ask a question...")
#     if user_input:
#         st.chat_message("user").markdown(user_input)
#         st.session_state.messages.append({"role":"user","content":user_input})

#         response = ask_question(user_input)
#         if response.status_code==200:
#             data=response.json()
#             answer=data["response"]
#             sources=data.get("sources",[])
#             st.chat_message("assistant").markdown(answer)
#             if sources:
#                 st.markdown("📄 **sources: **")
#                 for src in sources:
#                     st.markdown(f"- '{src}'")
#                 # render llm response as well
#                 st.session_state.messages.append({"role":"assistant","content":answer})
#             else:
#                 st.error(f"Error: {response.text}")
