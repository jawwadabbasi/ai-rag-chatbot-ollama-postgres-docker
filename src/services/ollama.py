import requests
import settings

class Ollama:

	api_endpoint = 'http://127.0.0.1:11434'

	def Generate(prompt):

		data = {
			'model': settings.GEN_MODEL,
            'prompt': prompt,
            'stream': False,
            'options': {
                'temperature': 0,
                'num_ctx': 4096
            }
		}

		try:
			result = requests.post(f'{Ollama.api_endpoint}/api/generate',json = data)

			return result.json()['response'] if result.ok else False

		except:
			return False

	def Embed(text):

		data = {
			'model': settings.EMBED_MODEL,
			'prompt': text
		}

		try:
			result = requests.post(f'{Ollama.api_endpoint}/api/embeddings',json = data)

			return result.json()['embedding'] if result.ok else False

		except:
			return False