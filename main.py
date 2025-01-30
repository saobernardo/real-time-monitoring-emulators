import time
import apsw
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import apsw
import apsw.ext
import sys
import logging
import shutil
import os
from pathlib import Path

emulator = sys.argv
emulator.pop(0)

if len(emulator) == 0:
  sys.exit('Nenhum emulador fornecido')

connection = apsw.Connection(f'{os.getcwd()}/db.sqlite', flags=apsw.SQLITE_OPEN_READONLY)
cursor = connection.cursor()

query = "SELECT save_path, destination_path FROM emulators WHERE identification = ?1"
data = (emulator)
cursor.execute(query, data)
dataCursor = cursor.fetchone()

if dataCursor is None:
  sys.exit('Emulador não encontrado')

folder_to_monitor = dataCursor[0]

class EventHandler(FileSystemEventHandler):
  def on_any_event(self, event):
    if event.event_type == "created" or event.event_type == "modified":
      #shutil.copy2(r''+event.src_path, r''+data[1])
      file_path = Path(os.path.dirname(r''+event.src_path))

      if not os.path.exists(os.path.join(dataCursor[1], str(file_path.parts[-1]))):
        os.mkdir(os.path.join(dataCursor[1], str(file_path.parts[-1])))
        print('Pasta %s criado', str(file_path.parts[-1]))

      try:
        shutil.copy2(r''+event.src_path, os.path.join(dataCursor[1], str(file_path.parts[-1])))
        print('''Save files from '''+r''+event.src_path+''' copied to ''' + dataCursor[1])
      except PermissionError as e:
        print(f"Error: Permission denied for {os.path.join(dataCursor[1], str(file_path.parts[-1]))} - {e}")
      except OSError as e:
        print(f"Error copying {str(file_path.parts[-1])} to {os.path.join(dataCursor[1], str(file_path.parts[-1]))} - {e}")

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
  
  event_handler = EventHandler()
  observer = Observer()
  observer.schedule(event_handler, folder_to_monitor, recursive=True)
  observer.start()

  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
    print('parou')

  observer.join

cursor.close()
connection.close()