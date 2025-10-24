import requests
import settings

class Logger:

	api_endpoint = 'http://batman-ms-logger'

	def CreateServiceLog(endpoint,request,response):

		data = {
			'Service': settings.SVC_NAME,
			'Endpoint': endpoint,
			'Request': request,
			'Response': response
		}

		try:
			result = requests.post(f'{Logger.api_endpoint}/api/v1/Service/CreateLog',json = data,stream = True)

			return True if result.ok else False

		except:
			return False

	def CreateExceptionLog(method,exception,comments = ''):

		data = {
			'Service': settings.SVC_NAME,
			'Method': method,
			'Exception': exception,
			'Comments': comments
		}

		try:
			result = requests.post(f'{Logger.api_endpoint}/api/v1/Exception/CreateLog',json = data,stream = True)

			return True if result.ok else False

		except:
			return False

	def SendAlert(method,message):

		data = {
			'Service': settings.SVC_NAME,
			'Method': method,
			'Message': message
		}

		try:
			result = requests.post(f'{Logger.api_endpoint}/api/v1/Slack/SendAlert',json = data,stream = True)

			return True if result.ok else False

		except:
			return False