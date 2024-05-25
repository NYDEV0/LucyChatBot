from google import generativeai
from config import gemini_key


class Gemini:
    def __init__(self) -> None:
        self.api_key = gemini_key 
        generativeai.configure(api_key=self.api_key)

        self.model = generativeai.GenerativeModel('gemini-pro')

    def get_response(self, query:str) -> str:
        response = self.model.generate_content(query)
            
        return response.text
