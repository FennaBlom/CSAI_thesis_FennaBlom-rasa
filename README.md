## Building a Conversational Agent with Rasa to Enrich a Medical Abstracts Dataset
# Classification and explanation
This README file provides an overview of the thesis project and instructions on how to understand and use the Rasa chatbot.

# Introduction
The goal of this thesis project was to build a conversational agent using Rasa that enriches a medical abstracts dataset by allowing users to add new papers to the dataset. The chatbot code and action files are included in this repository. The code for the classification and explanation can be found here: https://github.com/FennaBlom/CSAI_thesis_FennaBlom-classification-explanation


# Prerequisites
Before using the code, make sure you have the following prerequisites installed:

- Rasa version 3.5.4
- NLTK version 3.8.1
- scikit-learn 1.0.2
- Huggingface Transformers 4.26.1
- PyTorch 1.13.1
- SHAP 0.41.0

# Installation
To install the required dependencies, you can use the following command:

```pip install -r requirements.txt``` 


# Usage
To use the Rasa chatbot, follow these steps:

1. Train the Rasa model by running the following command in the project directory:
```rasa train```
2. Run the action server by executing the following command:
```rasa run actions -p 5058```
3. Open the chatbot shell by running the following command:
```rasa shell -p 5080```

Once the shell is opened, you can interact with the chatbot and provide inputs for adding new papers to the medical abstracts dataset.

# Known Issues
- The SciBERT classification model is not included in the repository yet.

# Contributing
As this is a thesis project, contributions are not expected. However, if you have any suggestions or improvements, feel free to reach out to the project owner.

# Contact
For any questions or inquiries about this project, please contact the project owner at fennablom@hotmail.com.


