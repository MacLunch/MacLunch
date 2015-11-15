import os
import sqlite3

class DbControl(object):
	def __init__(self, db_name):
		db_filename = "%s.db" % (db_name)
		
		db_exist = self.db_exist(db_filename)
		if not db_exist:
			new_file = open(db_filename, "w")
			new_file.close()

		self.conn = sqlite3.connect(db_filename, check_same_thread=False)
		self.cursor = self.conn.cursor()

		if not db_exist:
			self.db_init()

	def db_exist(self, db_name):
		return os.path.isfile(db_name)

	def send_query(self, query):
		try_count = 3
		while try_count > 0:
			try:
				self.cursor.execute(query)
				self.conn.commit()
				break
			except Exception as e:
				print(e.args)
				try_count -= 1

		if try_count == 0:
			return False
		return True

	def db_init(self):
		# create requests table
		query = "CREATE TABLE requests (\
			id INTEGER PRIMARY KEY AUTOINCREMENT, \
			email varchar(255), \
			text varchar(255));"

		self.send_query(query)

		# create enrolls table
		query = "CREATE TABLE enrolls (\
			id INTEGER PRIMARY KEY AUTOINCREMENT, \
			content_id INTEGER, \
			text TEXT, \
			is_spam BOOLEAN, \
			api_key varchar(255))"

		self.send_query(query)

	def insert_data(self, table, columns, data):
		column_name = "(%s)" % (",".join(columns))
		default_query = "INSERT INTO %s %s" % (table, column_name)
		data_query = ",".join(data)

		query = "%s VALUES (%s)" % (default_query, data_query)

		status = self.send_query(query)

		if status == True:
			print("success")
