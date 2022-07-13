# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from distutils.log import error
from typing import Any, Text, Dict, List
import logging
import datetime as dt
from typing import Dict, Text, List

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.events import EventType, AllSlotsReset, SlotSet, Restarted
from rasa_sdk.executor import CollectingDispatcher, Action
from rasa_sdk.types import DomainDict
import random
import uuid
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

airtable_api_key = os.getenv("AIRTABLE_API_KEY")
base_id = os.getenv("BASE_ID")
table_name = os.getenv("TABLE_NAME")







def create_send_item_log(id, sender_name, sender_email_address, pickup_address, item, item_weight, receiver_name, receiver_phone, receiver_address):
    request_url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
                  

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {airtable_api_key}"

    }

    data = {
        "fields": {
            "date": f"{dt.datetime.now()}",
            "id": id,
            "status": "Logged",
            "sender_name": sender_name,
            "sender_email_address": sender_email_address,
            "pickup_address": pickup_address,
            "item": item,
            "item_weight": item_weight,
            "receiver_name": receiver_name,
            "receiver_phone": receiver_phone,
            "receiver_address": receiver_address

            
        }
    }
    try:
        response = requests.post(
            request_url, headers=headers, data=json.dumps(data) #json dumps converts the data to a json object
        )
        response.raise_for_status()  #executing the call
    except requests.exceptions.HTTPError as err:  #interrupting the call if any http errors are raised
        raise SystemExit(err)

    return response
    print(requests.status_codes)
#still testing
def post_any_data(data, record_id):
    request_url = f"https://api.airtable.com/v0/{base_id}/{table_name}/{record_id}"
                  

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {airtable_api_key}"

    }

    try:
        response = requests.patch(
            request_url, headers=headers, data=json.dumps(data) #json dumps converts the data to a json object
        )
        response.raise_for_status()  #executing the call
    except requests.exceptions.HTTPError as err:  #interrupting the call if any http errors are raised
        raise SystemExit(err)

    return response
    print(requests.status_codes)

def airtable_download(generated_id=None, params_dict={}, table=table_name, api_key=airtable_api_key, base_id=base_id, record_id=None):
    """Makes a request to Airtable for all records from a single table.
        Returns data in dictionary format.
    Keyword Arguments:
    • table: set to table name
        ◦ see: https://support.airtable.com/hc/en-us/articles/360021333094#table
    • params_dict: desired parameters in dictionary format {parameter : value}
        ◦ example: {"maxRecords" : 20, "view" : "Grid view"}
        ◦ see "List Records" in API Documentation (airtable.com/api)
    • api_key: retrievable at https://airtable.com/account
        ◦ looks like "key●●●●●●●●●●●●●●"
    • base_id: retrievable at https://airtable.com/api for specific base
        ◦ looks like "app●●●●●●●●●●●●●●"
    • record_id: optional for single record lookups
        ◦ looks like "rec●●●●●●●●●●●●●●"
        """

    # Authorization Credentials
    if api_key is None:
        print("Enter Airtable API key. \n  *Find under Airtable Account Overview: https://airtable.com/account")
        api_key = input()
    headers = {"Authorization": "Bearer {}".format(api_key)}
    

    # Locate Base
    if base_id is None:
        print("Enter Airtable Base ID. \n  *Find under Airtable API Documentation: https://airtable.com/api for specific base")
        base_id = input()
    url = 'https://api.airtable.com/v0/{}/'.format(base_id)
    path = url + table
    print(path)


    # Format parameters for request
    constant_params = ()
    for parameter in params_dict:
        constant_params += ((parameter, params_dict[parameter]),)
    params = constant_params

    # Start with blank list of records
    airtable_records = []

    # Retrieve single record and return it if needed
    if record_id is not None:
        path = "{}/{}".format(path, record_id)
        response = requests.get(path, headers=headers)
        airtable_response = response.json()
        if 'error' in airtable_response:
            #identify_errors(airtable_response)
            return airtable_response
        return airtable_response

    # Retrieve multiple record
    run = True
    while run is True:
        response = requests.get(path, params=params, headers=headers)
        airtable_response = response.json()

        try:
            airtable_records += (airtable_response['records'][-5:])
        except:
            if 'error' in airtable_response:
                #identify_errors(airtable_response)
                return airtable_response

        if 'offset' in airtable_response:
            run = True
            params = (('offset', airtable_response['offset'])) + constant_params
        else:
            run = False
    #print(airtable_response)
    output = {}
    for i in airtable_records:
            if i['fields']['id']==generated_id:
                output= i['fields']
            
    return output





# submit initial tracking
class ActionSubmitSendItem(Action):
    def name(self) -> Text:
        return "action_submit_send_item"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        item = tracker.get_slot("item")
        item_weight = tracker.get_slot("item_weight")
        receiver_address = tracker.get_slot("receiver_address")
        pickup_address = tracker.get_slot("pickup_address")
        sender_email_address = tracker.get_slot("sender_email_address")
        sender_name = tracker.get_slot("sender_name")
        receiver_name = tracker.get_slot("receiver_name")
        receiver_phone = tracker.get_slot("receiver_phone")
        
         #generate global unique ID before submitting
        global id 
        id = str(uuid.uuid4())

        response = create_send_item_log(
                id=id,
                item=item,
                item_weight=item_weight,
                receiver_address=receiver_address,
                pickup_address=pickup_address,
                sender_email_address=sender_email_address,
                sender_name=sender_name,
                receiver_name=receiver_name,
                receiver_phone = receiver_phone
                
            )

        dispatcher.utter_message("Thanks, your answers have been recorded!") # message to the user about the form
        return []

# the idea of the tracking Id is that it is first sent to the airtable database
# included in it  with a temporary ID, the data is then called back and queried with the temporary ID in order to get the original ID. which is the record ID.
class SetTrackingID(Action): 
    def name(self)-> Text:
        return "action_set_tracking_id"    


    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
       
        #getting tracking ID from th
        #print(airtable_download(generated_id=id))
        print("the id is: ", id)
        tracking_id = airtable_download(generated_id=id)
        print(tracking_id)#['recordid']
        
        dispatcher.utter_message(f"Thanks, your answers have been recorded! Your tracking ID is {tracking_id}, please come along with your money when dropping of the item.") # message to the user about the form
        return[SlotSet("tracking_id", tracking_id)]




# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ValidateDeliveryForm(FormValidationAction):
    def name(self)-> Text:
        return "validate_delivery_form"
    
    def validate_confirm_booking(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict) -> Dict[Text, Any]:
        
        if slot_value != True:
            return {"requested_slot": None}
        else:
            return {"confirm_booking": slot_value}

# get tracking status
class GetTrackingStatus(Action): 
    def name(self)-> Text:
        return "action_get_tracking_status"    


    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
       
        #getting tracking ID from th
        given_id = next(tracker.get_latest_entity_values("tracking_id"), None)
        print(given_id)
        try:
            item_status = airtable_download(record_id=given_id)['fields']['status']
            dispatcher.utter_message(f"Thank you for your feedback. The status for your item with ID: {given_id} is {item_status}") # message to the user about the form
        except:
            dispatcher.utter_message(f"Your tracking ID is incorrect, please start again")
        return []


# request cancel order
class GetTrackingStatus(Action): 
    def name(self)-> Text:
        return "action_request_cancel_order"    


    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
       
        #getting tracking ID from th
        given_id = next(tracker.get_latest_entity_values("tracking_id"), None)
        print(given_id)
        data = {
            "fields": {
                "cancel_request": "Active"
            }
        }
        try:
            cancel = post_any_data(data=data, record_id=given_id)
            dispatcher.utter_message(f"Your request to cancel the shipment with the ID: {given_id} has been receieved. You will get an email when it is processed") # message to the user about the form
        except error as e:
            dispatcher.utter_message(e)#f"Your tracking ID is incorrect, please start again")
        return []

# request cancel order
class GetTrackingStatus(Action): 
    def name(self)-> Text:
        return "action_make_complain"    


    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
       
        #getting tracking ID from th
        given_id = next(tracker.get_latest_entity_values("tracking_id"), None)
        print(given_id)
        data = {
            "fields": {
                "make_complain": "Active"
            }
        }
        try:
            post_complain = post_any_data(data=data, record_id=given_id)
            dispatcher.utter_message(f'''We are sorry that the shipment with our company did't go so well with you
                                        our Customer care service will reach out to you as soon as possoble.''') # message to the user about the form
        except error as e:
            dispatcher.utter_message(e)#f"Your tracking ID is incorrect, please start again")
        return []


class ActionEnd(Action):
    def name(self):
        return "action_end"

    async def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset(), Restarted()]