import inspect
import psycopg
import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from services.logger import Logger

class Db:

	def Connect(write = False,raw = False):
		
		try:
			return psycopg.connect(
				host=settings.DB_HOST_WRITER if write else settings.DB_HOST_READER,
				port=settings.DB_PORT,
				user=settings.DB_USER,
				password=settings.DB_PASS,
				dbname = None if raw else settings.DB_NAME
			)
		
		except:
			return False

	def Disconnect(con):
		
		try:
			return con.close()
		
		except:
			return False

	def ExecuteQuery(query,inputs = None,write = False,raw = False,autocommit = False):
		
		con = Db.Connect(write, raw)
		con.autocommit = autocommit
		
		if not con:
			return False

		try:
			result = False
			
			with con.cursor() as cur:
				if str(query).strip().lower().startswith('select'):
					cur.execute(query, inputs)
					cols = [desc[0] for desc in cur.description]
					rows = cur.fetchall()
					result = [dict(zip(cols, row)) for row in rows]

				else:
					if isinstance(inputs, list) and inputs and isinstance(inputs[0], (list, tuple)):
						cur.executemany(query, inputs)
					
					else:
						cur.execute(query, inputs)
					
					con.commit()

					result = True

			Db.Disconnect(con)

			return result

		except Exception as e:
			Db.Disconnect(con)
			Logger.CreateExceptionLog(inspect.stack()[0][3],str(e),query.strip())
			
			return False

	def GetEngine(write = False):
		
		host = settings.DB_HOST_WRITER if write else settings.DB_HOST_READER
		url = f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASS}@{host}:{settings.DB_PORT}/{settings.DB_NAME}"
		engine = create_engine(url, echo=settings.FLASK_DEBUG)
		
		return engine

	def GetSession(write = False):
		
		engine = Db.GetEngine(write)
		Session = sessionmaker(bind=engine)
		
		return Session()

	@contextmanager
	def SessionScope(write = False):
		
		session = None
		
		try:
			session = Db.GetSession(write)
			yield session
			session.commit()
		
		except Exception as e:
			if session:
				session.rollback()

			Logger.CreateExceptionLog(inspect.stack()[0][3],str(e))
		
		finally:
			if session:
				session.close()