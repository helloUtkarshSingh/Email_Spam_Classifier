import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum(): 
        #check if the word from text is aplhabe or number if it is the append it in a new list y
            y.append(i)
    text = y[:] # colning the y list in text
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
    return " ".join(y)

tfidf = pickle.load(open('Vectorizer.pkl','rb'))
model1 = pickle.load(open('model1.pkl','rb'))

st.title("Email/SMS Spam Classifier")

input_message = st.text_area("Enter the message")

if st.button("Predict"):
    #1. preprocess
    transform_input_message = transform_text(input_message)
    #2. vectorize
    vector_input = tfidf.transform([transform_input_message])
    #3. predict
    result = model1.predict(vector_input)[0]
    #4. Display
    if result == 1:
        st.header("The given input message is a Spam")
    else:
        st.header("The given input message is not a Spam")    