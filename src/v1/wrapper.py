import concurrent.futures
import inspect

from services.logger import Logger

class Wrapper:
	
	def ListBatsignal(x):
		
		try:
			return {
				'Id': str(x['announcement_id']),
                'Sender': str(x['sender']),
				'CreatedBy': str(x['created_by']),
				'UserId': str(x['user_id']),
                'Subject': str(x['subject']),
                'Content': x['content'],
                'Broadcast': bool(x['broadcast']),
                'Date': str(x['date'])
			}
		
		except Exception as e:
			Logger.CreateExceptionLog(inspect.stack()[0][3],str(e),'ERROR - Could not wrap data')

			return False
		
	def Pagination(limit,offset,sort,result):

		return {
			"Page": offset,
			"Size": limit,
			"Total": result[0]['Total'] if result else 0,
			"Sort": sort if sort else {}
		}
		
	def Package(result,kind):

		data = []

		if type(result) != list:
			return data
		
		if kind not in [
			'list-batsginal',
		]:
			return data

		threads = []
		
		with concurrent.futures.ThreadPoolExecutor() as executor:
			for x in result:
				if kind == 'list-batsginal':
					threads.append(executor.submit(Wrapper.ListBatsignal,x))

		for x in threads:
			z = x.result()

			if z:
				data.append(z)

		return data