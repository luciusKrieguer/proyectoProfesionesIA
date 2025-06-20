import nltk
nltk.download ('punkt_tab')
import numpy as np 
import pandas as pd 
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


import random
import json

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers  import Dense


from sklearn.preprocessing import LabelEncoder


#cargar los datos 

path= '/content/drive/MyDrive/CHATBOT/intents.json'
with open (path, 'r', encoding='utf-8') as file:
    data= json.load(file)

#creamos el stemmer
stemmer= PorterStemmer()


#preprocesaimento
vocab=[]
tags=[]
patterns= []
labels = []


#VARIABLES
X=[]
Y=[]


for intent in data ['intents']:
    for pattern in intent ['patterns']:
        tokens =word_tokenize(pattern.lower())
        stemmed =[stemmer.stem(w) for w in tokens]
        vocab.extend(stemmed)
        labels.append(intent['tag'])
        patterns.append(stemmed)
    if intent ['tag']not in tags:
        tags.append(intent['tag'])

vocab =sorted (set(vocab))



encoder =LabelEncoder()
encoder_labels= encoder.fit_transform(labels)


for pattern in patterns: 
    bag = [1 if word in pattern else 0 for word in vocab ]
    X.append(bag)

Y= encoder_labels 


#convertimos las variables a a arreglos numpy
X= np.array(X)
Y= np.array(Y)


 

#MODELO
D= len(X[0]) #filas (cuantas filas lelgaron)
C= len(tags) #etiquetas

model= Sequential() #agregar cada uno de los elementos 
# capa de entrada
#8=# neuronas
#input_shape=(entrada, salida(vacio para que el modelo tenga tantos posible resultado como considere necesario))
model.add( Dense(8,input_shape=(D,),activation='relu'))

#capa densa 2 #capaz de entrenamiento 
model. add(Dense(8,activation='relu'))
model.add (Dense(C, activation='softmax'))

#compilamos
model.compile ( 

    loss='sparse_categorical_crossentropy',
    optimizer='adam',
    metrics =['accuracy'],

)



#entrenamos
model.fit(X,Y, epochs =200, verbose=0)

#Funcion para procesas la entrada de etiquetas
def predict_class(text):
    tokens =word_tokenize(text.lower())
    stemmed =[stemmer.stem(w)for w in tokens]

    bag = np.array([1 if word in stemmed else 0 for word in vocab])
    res = model.predict(np.array([bag]), verbose=0)[0]
    idx =np.argmax(res)
    tag =encoder.inverse_transform([idx])[0]
    return tag



# Fuencion para dar la respuestas

def get_response (tag, context):
    for intent in data['intents']:
        if intent['tag']==tag:
            return random.choice(intent['responses'])
    return "No entendi, puedes repetir"

