import google.generativeai as genai
from data import Prompt

class LLM:
    def __init__(self, api_key, model_name='gemini-1.5-flash-latest'):
        """
        Initializes the LLM with the necessary API configuration and model selection.

        Parameters:
            api_key (str): The API key required to authenticate requests to the generative AI service.
            model_name (str): The name of the model to be used for generating responses.
        """
        genai.configure(api_key)
        self.model = genai.GenerativeModel(model_name)
        self.document = None
 
    # def load_document(self, file_path):
    #     """
    #     Loads a PDF document, merges its context for use as a reference in generating responses.

    #     Parameters:
    #         file_path (str): Path to the PDF file to load.
    #     """
    #     loader = SinglePDFLoader(file=file_path, clean=True)
    #     self.document = merge_context(loader)

    def generate_response(self, query:str, prompt:Prompt, stream=False):
        """
        Generates a response from the LLM based on the provided prompt and document context.

        Parameters:
            prompt (str): The prompt or question to which the model should respond.
            stream (bool): Indicates whether the response should be streamed (for large responses).

        Returns:
            str: The response generated by the LLM.
        """
        input = prompt.get_prompt(input=query)
        response = self.model.generate_content(input, stream=stream) # TODO: Ensure to handle streaming and non streaming responses
        prompt.add_history(query, response)
        return response