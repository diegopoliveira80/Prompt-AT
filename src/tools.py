import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

##################################################### GEMINI LLM
class Gemini(object):
    def __init__(self, model_name, apikey, system_prompt, generation_config=None):
        self.model = self.__create_model(apikey, model_name, 
                                         system_prompt, generation_config)

        
    def __create_model(self, apikey, model_name, system_prompt, generation_config=None):
        genai.configure(api_key=apikey)
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        if generation_config is None:
            generation_config = {
                'temperature': 0.2,
                'max_output_tokens': 1000
            }
        return genai.GenerativeModel(
            model_name,
            system_instruction=system_prompt,
            generation_config = generation_config,
            safety_settings=safety_settings
        )
 
        
##################################################### ex_03
    def llm_ex_03(self,prompt):
        response=self.model.generate_content(prompt)
        return response


##################################################### ex_04
    def llm_ex_04(self,prompt):
        response=self.model.generate_content(prompt)
        return response


##################################################### ex_06
    def llm_ex_06(self,prompt):
        response=self.model.generate_content(prompt)
        return response


##################################################### ex_07
    def llm_ex_07(self,prompt):
        response=self.model.generate_content(prompt)
        return response







