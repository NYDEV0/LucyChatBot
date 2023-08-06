from bardapi import Bard

token = 'YwgJWDYPjj-CbbOmblCEv8NTJiotYOVszCPbVs2jdmsGXNJpATP4-vJinjMSYePh1WtEHw.'
bard = Bard(token=token)

def chat(text):
    """
    Take input text and return bard response.
    Args:
        text: Text which is send to bard AI.
    Return:
        A response from bard.
    """
    response = bard.get_answer(text)['content']
    
    return response