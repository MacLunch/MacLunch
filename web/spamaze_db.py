import os
import sqlite3

class DbControl(object):
	def __init__(self, db_name):
		db_filename = "%s.db" % (db_name)
		
		if not self.db_exist(db_filename):
			new_file = open(db_filename, "w")
			new_file.close()
			self.db_init()

		self.conn = sqlite3.connect(db_filename)
		self.cursor = self.conn.cursor()

		

	def db_exist(self, db_name):
		return os.path.isfile(db_name)

	def db_init(self):
	#	if not self.table_exist('requests'):
		query = "CREATE TABLE requests (\
			id INTEGER PRIMARY KEY AUTOINCREMENT, \
			email varchar(255), \
			text varchar(255));"

		self.cursor.execute(query)
		self.conn.commit()

	#	if not self.table_exist('enrolls'):
		query = "CREATE TABLE enrolls (\
			id INTEGER PRIMARY KEY AUTOINCREMENT, \
			text TEXT, \
			is_spam BOOLEAN)"

		self.cursor.execute(query)
		self.conn.commit()

	def insert_data(self, table, columns, data):
		column_name = "(%s)" % (",".join(columns))



		default_query = "INSERT INTO %s %s" % (table, column_name)

		data_query = ",".join(data)

		query = "%s VALUES (%s)" % (default_query, data_query)

		print(query)
		self.cursor.execute(query)
		self.conn.commit()

		print("success")

	# def upsert_data(self, table, columns, data):
	# 	column_name = "(%s)" % (",".join(columns))
	# 	default_query = "INSERT INTO %s %s" % (table, column_name)

	# 	data_query = ",".join(data)

	# 	query = "%s VALUES (%s)" % (default_query, data_query)

	# 	print(query)
	# 	self.cursor.execute(query)
	# 	self.conn.commit()

	# 	print("success")		
