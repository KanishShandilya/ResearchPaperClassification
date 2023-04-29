from flask import request,Flask,jsonify
from transformers import AutoModelForSequenceClassification,AutoTokenizer,pipeline
import torch
from helper import preprocess

app=Flask(__name__)

num_labels=6
model = AutoModelForSequenceClassification.from_pretrained("Bert/checkpoint-23500", num_labels=num_labels, problem_type="multi_label_classification")
tokenizer = AutoTokenizer.from_pretrained("Bert/checkpoint-23500",problem_type="multi_label_classification")
layer=torch.nn.Softmax(dim=1)
THRESHOLD=0.35


@app.route("/",methods=["POST"])
def home():
    title=request.json['title']
    abstract=request.json['abstract']
    title=preprocess(title)
    abstract=preprocess(abstract)
    if len(title)==0 or len(abstract)==0:
        return jsonify({'data':"Invalid sentences"})
    inputs = tokenizer(title[:512],abstract[:512], return_tensors="pt")
    op=model(**inputs).logits
    output = layer(op)
    temp=output>THRESHOLD
    res=[]
    print(temp)
    if temp[0][0]:
        res.append("Computer SCience")
    if temp[0][1]:
        res.append("Physics")
    if temp[0][2]:
        res.append("Mathematics")
    if temp[0][3]:
        res.append("Statistics")
    if temp[0][4]:
        res.append("Quantative Biology")
    if temp[0][5]:
        res.append("Quantative Finance")

    return jsonify({'data':res})
    


