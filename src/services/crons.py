import requests
import settings

class Crons:

	api_endpoint = 'http://batman-ms-crons'

	def StartJob(job):

		data = {
			'Service': settings.SVC_NAME,
			'Job': job
		}

		try:
			result = requests.post(f'{Crons.api_endpoint}/api/v1/Job/Start',json = data,stream = True)

			return result.json()['ApiResult'] if result.ok else False

		except:
			return False

	def EndJob(log_id,status,result):

		data = {
			'LogId': log_id,
			'Status': status,
			'Result': result
		}

		try:
			result = requests.post(f'{Crons.api_endpoint}/api/v1/Job/End',json = data,stream = True)

			return True if result.ok else False

		except:
			return False