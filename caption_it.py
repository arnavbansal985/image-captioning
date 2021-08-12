    #!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
import json
import pickle
from keras.applications.resnet50 import ResNet50,preprocess_input
from keras.preprocessing import image
from keras.models import Model,load_model
from keras.utils import to_categorical
from keras.layers import Input,Dense,Dropout,Embedding,LSTM
from keras.layers.merge import add


# In[33]:


import os


# In[34]:


from keras.preprocessing.sequence import pad_sequences


# In[58]:


model=load_model('model_weights/model_9.h5')
model._make_predict_function()

# In[59]:


model_temp=ResNet50(weights='imagenet',input_shape=(224,224,3))


# In[73]:


#model_temp.summary()


# In[61]:


#create a new model by removing last layer of the resnet model
model_resnet=Model(model_temp.input,model_temp.layers[-2].output)
model_resnet._make_predict_function()

# In[62]:


with open("word_to_idx.pkl",'rb')as f:
    word_to_idx=pickle.load(f)


# In[63]:


with open("idx_to_word.pkl",'rb')as f:
    idx_to_word=pickle.load(f)


# In[66]:


def preprocess_img(img):
    img=image.load_img(img,target_size=(224,224))
    img=image.img_to_array(img)
    img=np.expand_dims(img,axis=0)
    #normalization
    img=preprocess_input(img)
    return img

def encode_img(img):
    img=preprocess_img(img)
    feature_vector=model_resnet.predict(img)
    feature_vector=feature_vector.reshape(1,feature_vector.shape[1])
    #print(feature_vector.shape)
    return feature_vector


# In[67]:


#enc=encode_img('man_running_test.jpg')


# In[68]:


#enc.shape


# In[69]:


def predict_caption(photo):
    max_len=35
    in_text = "startseq"
    for i in range(max_len):
        sequence = [word_to_idx[w] for w in in_text.split() if w in word_to_idx]
        sequence = pad_sequences([sequence],maxlen=max_len,padding='post')
        
        ypred = model.predict([photo,sequence])
        ypred = ypred.argmax() #WOrd with max prob always - Greedy Sampling
        word = idx_to_word[ypred]
        in_text += (' ' + word)
        
        if word == "endseq":
            break
    
    final_caption = in_text.split()[1:-1]
    final_caption = ' '.join(final_caption)
    return final_caption


# In[70]:


#predict_caption(enc)


# In[77]:


def final_caption(image):
    enc_=encode_img(image)
    cap=predict_caption(enc_)
    return cap


# In[81]:


#final_caption('man_running_test.jpg')


# In[ ]:




