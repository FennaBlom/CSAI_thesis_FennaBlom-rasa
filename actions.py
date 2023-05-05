# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
# import torch

from rasa_sdk.events import SlotSet, FollowupAction
#import torch
from actions.classification import LoadModel, PredictionAbstract



#
# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

class ActionLinkDatabase(Action):

    def name(self) -> Text:
        return "action_link_database"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]):
        url = 'https://raw.githubusercontent.com/sebischair/Medical-Abstracts-TC-Corpus/main/medical_tc_train.csv'
        df = pd.read_csv(url,index_col=0,parse_dates=[0],on_bad_lines='skip').reset_index()
        return [SlotSet('database', df.to_json())]
    
class ActionClassifyAbstract(Action):
    def name(self) -> Text:
        return "action_classify_abstract"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        abstract = tracker.get_slot('abstract_text')
        model = LoadModel()
        prediction, confidence = PredictionAbstract(str(abstract), model)
        dispatcher.utter_message(f"Confidence: {confidence}")
        if confidence < 0.7:
            dispatcher.utter_message(f"I am unsure about my prediction. I predicted {prediction}, what would you suggest?")
            return[FollowupAction("choose_category_form")]
        
        else:
           return[ SlotSet('category', prediction)]
        

class ActionAddToDatabase(Action):
    def name(self) -> Text:
        return "action_add_to_database"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        database = tracker.get_slot("database")
        if database == None:
            dispatcher.utter_message("new database!")
            url = 'https://raw.githubusercontent.com/sebischair/Medical-Abstracts-TC-Corpus/main/medical_tc_train.csv'
            df = pd.read_csv(url,index_col=0,parse_dates=[0],on_bad_lines='skip').reset_index()
            df = df[:500]
        else: 
            df = pd.read_json(database)
        abstract = tracker.get_slot('abstract_text')
        category = tracker.get_slot('category')
        new_input = [category, abstract]
        df.loc[len(df)] = new_input
        all_cat = tracker.get_slot('all_categories')

        return [SlotSet('database', df.to_json())]

        
class ActionResetAbstract(Action):
    def name(self) -> Text:
        return "action_reset_abstract"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet('abstract_text',None)]
    
class ActionResetCategory(Action):
    def name(self) -> Text:
        return "action_reset_category"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet('category',None)]    
    
class ActionStoreAllCategories(Action):
    def name(self) -> Text:
        return "action_store_all_categories"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        all_cats = tracker.get_slot('all_categories')
        category = tracker.get_slot('category')
        if all_cats == None:
            all_cats = []
        all_cats.append(category)
        return [SlotSet('all_categories', all_cats)]

class ActionNameAllCategories(Action):
    def name(self) -> Text:
        return "action_name_all_categories"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        all_cats = tracker.get_slot('all_categories')
        dispatcher.utter_message(str(all_cats))

