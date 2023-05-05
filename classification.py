import numpy as np
import pandas as pd
import random
import torch
from torch.utils.data import TensorDataset, random_split
from sklearn.preprocessing import LabelEncoder
from transformers import AutoTokenizer, TextClassificationPipeline
from torch.utils.data import TensorDataset, random_split
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn


def LoadModel():
    if torch.cuda.is_available():    

    # Tell PyTorch to use the GPU.    
        device = torch.device("cuda")

        print('There are %d GPU(s) available.' % torch.cuda.device_count())

        print('We will use the GPU:', torch.cuda.get_device_name(0))

        # If not...
    else:
        print('No GPU available, using the CPU instead.')
        device = torch.device("cpu")

    model = torch.load("actions/model_scibert.pt")
    return model

def PredictionAbstract(abstract, model):
    np.random.seed(17)
    abstract = word_tokenize(abstract)
    filtered_abstract = [w for w in abstract if not w.lower() in stopwords.words('english')]
    join_filtered = ' '.join(str(a) for a in filtered_abstract)
    tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased")
    pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=False)
    prediction = pipe(join_filtered)
    labels = {"LABEL_0": "neoplasms", "LABEL_1": "digestive system diseases", "LABEL_2": "nervous system diseases",
          "LABEL_3": "cardiovascular diseases", "LABEL_4": "general pathological conditions"}
    for l in labels:
        if prediction[0]['label'] == l:
            label = labels[l]
    confidence = prediction[0]['score']
    return label, confidence




