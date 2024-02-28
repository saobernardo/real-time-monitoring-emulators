import apsw

connection = apsw.Connection('db.sqlite')
cursor = connection.cursor()

emulator = r'duckstation'
query = f"SELECT save_path, destination_path FROM emulators WHERE identification = '{emulator}'"
cursor.execute(query)
data_res = cursor.fetchone()

if data_res is not None:
  print(data_res)
else:
  print('Emulador não encontrado')