import time
import apsw
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import apsw
import apsw.ext
import sys
import logging
import shutil

emulator = sys.argv
emulator.pop(0)

if len(emulator) == 0:
  sys.exit('Nenhum emulador fornecido')

connection = apsw.Connection('db.sqlite')
cursor = connection.cursor()

query = "SELECT save_path, destination_path FROM emulators WHERE identification = ?1"
data = (emulator)
cursor.execute(query, data)
data = cursor.fetchone()
folder_to_monitor = data[0]

class EventHandler(FileSystemEventHandler):
  def on_any_event(self, event):
    if event.event_type == "created" or event.event_type == "modified":
      shutil.copy2(event.src_path, data[1])

    print(f"Event type: {event.event_type}")
    print(f"File path: {event.src_path}")

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