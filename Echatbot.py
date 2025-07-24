import os
import nltk
import ssl
import streamlit as st
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

ssl._create_default_https_context=ssl._create_unverified_context
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt')

# Create Vectorizer and Classifier
vectorizer=TfidfVectorizer()
clf=LogisticRegression(random_state=0, max_iter=10000)

#pre process the data
tags=[]
patterns=[]
for intent in intents:
    for pattern in intent ['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern)
#TRAINING THE MODEL
x=vectorizer.fit_transform(patterns)
y=tags
clf.fit(x,y)
#create chatbot
def chatbot(input_text):
    input_text=vectorizer.transform([input_text])
    tag=clf.predict(input_text)[0]
    for intent in intents:
        if intent['tag']==tag:
            response=random.choice(intent['responses'])
            return response
# End to End Chatbot
counter=0
def main():
    global counter
    st.title("ECHATBOT")
    st.write("welcome to the exceptional chatbot" )

    counter +=1
    user_input=st.text_input("You:", key=f"user_input_{counter}")
    
    if user_input:
        response=chatbot(user_input)
        st.text_area("chatbot:", value=response, height=100, max_chars=None, key = f"chatbot_response_{counter}")

        if response.lower() in ['goodbye', 'bye']:
            st.write("Thanks")
            st.stop()

if __name__=='__main__':
    main()