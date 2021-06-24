import sqlalchemy
import pandas as pd

class Database:
	def __init__(self, user="jaeb", password="jaeb", db="ocr_db", host='192.168.1.35', port='5432'):
		self.user = user
		self.password = password
		self.db = db

		try:
			url = 'postgresql://{}:{}@{}:{}/{}'
			url = url.format(user, password, host, port, db)
			self.con = sqlalchemy.create_engine(url, client_encoding='utf8')

			print(f'===========================\nsuccess to connect database\n===========================')
			print(f'URL  : {url} \nHOST : {host} \nPORT : {port} \nDB   : {db}')

		except ConnectionError as ce:
			print('connection error caused ', ce)


	def select(self, sql):
		"""
		:param sql query
		:return dataframe for query 
		"""
		
		self.data = []
		try:
			self.data.append(pd.read_sql(sql, self.con))
			self.data = pd.concat(self.data)
			return self.data

		except Exception as e:
			return print("database select error : ", e)
		


	def insert(self, df, schema, table, if_exists):
		try:
			df.to_sql(schema=schema, name=table, if_exists=if_exists, con=self.con)
			print(f"===========================\nsuccess to insert data\n===========================")
		except Exception as e:
			print('database insert error : ', e)


# connection = connect('postgres', 'qhdkswp1!', 'mailpoc')

if __name__ == '__main__':
	conn = Database('postgres', 'qhdkswp1!', 'mailpoc')
	sql = "select * from mailpoc.drm limit 10"

	result = conn.select(sql)

	print(result)
