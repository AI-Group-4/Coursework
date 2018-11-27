from witA import Wit
import random

access_token = "BKXQLOFJUM5A7EEBLOGEBNTEQQVQSRCZ"
client = Wit(access_token = access_token)

def wit_response(message_text,s_id):
	response = client.message(msg=message_text, context={'session_id':s_id})
	return response

def get_entity_value(entities, entity):
    val=[]
    if entity not in entities:
        return None
    if len(entities[entity]) >1:
        for entry in entities[entity]:
            val.append(entry['value'])
    else:
        val.append(entities[entity][0]['value'])
    if not val:
        return None
    
    return val if isinstance(val, dict) else val

def get_instent(entities, entity):
    if entity not in entities:
        return None
    val=entities[entity][0]['value']
    if not val:
        return None
    
    return val['value'] if isinstance(val, dict) else val

def get_news_elements(response,fb_id,msg_text):
    entities = response['entities']
    print(entities)
    fromA = msg_text.lower().index('from') if msg_text.find('from')>-1 else None
    toB= msg_text.lower().index('to') if msg_text.find('to')>-1 else None
    print(fromA , toB)
    location = get_entity_value(entities,'location')
    greetings = get_entity_value(entities,'greetings')
    datetime = get_entity_value(entities,'datetime')
    duration = get_entity_value(entities,'duration')
    thanks = get_entity_value(entities,'thanks')
    bye = get_entity_value(entities,'bye')

    if greetings:
        text = "Hello"
    elif datetime:
        text = datetime[0]
    elif duration:
        text = duration[0]
    elif thanks:
        text= "It's my pleasure.Thank you for using our service."
    elif bye:
        text = "Hope see you again soon,bye"
    elif location:
        if (fromA is not None and toB is not None) and fromA > toB:
            text = "Do you want to buy ticket from "+location[1]+" to "+location[0] 
        elif (fromA is not None and toB is not None) and fromA < toB:
            text = "Do you want to buy ticket from "+location[0]+" to "+location[1] 
        elif (fromA is not None and  toB is None):
            text = "From "+location[0]+" to where "
        elif (fromA is None and toB is not None):
            text = "TO "+location[0]+" from where "
        else:
            text = "test "
    else:
        text = "Hello, may I help you ? "

    return text