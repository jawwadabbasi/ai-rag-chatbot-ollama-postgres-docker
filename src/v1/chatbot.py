from services.ollama import Ollama
from v1.handler import Handler

class Chatbot:

    def Chat(question):

        api_data = {}
        api_data['ApiHttpResponse'] = 500
        api_data['ApiMessages'] = []
        api_data['ApiResult'] = []

        try:
            question = str(question)

        except:
            api_data['ApiHttpResponse'] = 400
            api_data['ApiMessages'] += ['ERROR - Invalid arguments']

            return api_data
        
        context = Handler.Retrieve(question)

        if not context:
            api_data['ApiHttpResponse'] = 500
            api_data['ApiMessages'] += ['ERROR - Failed to retrieve context']

            return api_data
        
        prompt = f"""
            You are Alfred the product assistant.
            Answer using ONLY the provided context.
            If the answer is not explicitly stated in the context, reply exactly:
            \"I couldn't find this in the documentation provided.\"

            [CONTEXT]
            {context}

            [QUESTION]
            {question}

            [INSTRUCTIONS]
            - Do not use outside knowledge.
            - Quote the relevant line(s) from the context when possible.
            - If missing, respond exactly with: I couldn't find this in the documentation provided.

            [ANSWER]
        """

        result = Ollama.Generate(prompt)

        if not result:
            api_data['ApiHttpResponse'] = 500
            api_data['ApiMessages'] += ['ERROR - Failed to generate response']

            return api_data

        api_data['ApiHttpResponse'] = 201
        api_data['ApiMessages'] += ['Request processed successfully']
        api_data['ApiResult'] = result

        return api_data