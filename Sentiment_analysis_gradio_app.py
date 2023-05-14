# -*- coding: utf-8 -*-
"""Docker Sentiment analysis Gradio App

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jmtHBPMgFa9smfSKtVcwupGejCAZQE5a
"""

!pip install transformers

!pip install gradio

# Import the required Libraries
import gradio as gr
import numpy as np
import transformers
from transformers import AutoTokenizer, AutoConfig, AutoModelForSequenceClassification, TFAutoModelForSequenceClassification
from scipy.special import softmax


# Requirements
model_path = "flokabukie/Finetuned-Distilbert-base-model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
config = AutoConfig.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = "@user" if t.startswith("@") and len(t) > 1 else t
        t = "http" if t.startswith("http") else t
        new_text.append(t)
    return " ".join(new_text)

#Function to process the input and return prediction
def sentiment_analysis(text):
    text = preprocess(text)

    encoded_input = tokenizer(text, return_tensors = "pt") # for PyTorch-based models
    output = model(**encoded_input)
    scores_ = output[0][0].detach().numpy()
    scores_ = softmax(scores_)
    
    #Output of scores by converting a list of labels and scores into a dictionary format
    labels = ["Negative", "Neutral", "Positive"]
    scores = {l:float(s) for (l,s) in zip(labels, scores_) }
    return scores
#App interface with gradio
app = gr.Interface(fn = sentiment_analysis,
                   inputs = gr.Textbox("Write your text or tweet here..."),
                   outputs = "label",
                   title = "Sentiment Analysis of Tweets on COVID-19 Vaccines",
                   description  = "This app analyzes sentiment of text based on tweets about COVID-19 Vaccines using a fine-tuned DistilBERT model",
                   interpretation = "default"
                  )

app.launch()

!pip install docker

import docker

# Define your Gradio app function
def run_container(image, command):
    # Run a Docker container with the specified image and command
    container = client.containers.run(image, command)
    # Get the logs from the container
    logs = container.logs().decode('utf-8')
    # Return the logs
    return logs

# Define your Gradio interface
iface = gr.Interface(
    run_container,
    inputs=["text", "text"],
    outputs="text",
    title="Docker Gradio App",
    description="Run Docker containers from within Gradio!"
)

# Run the Gradio app
iface.launch()

