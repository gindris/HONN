import threading
import queue #import fyrir queue klasann
import time #import fyrir sleep þegar queue er empty
from structured_logging.command_queue.command import Command


#TODO: dependency injection fyrir async_delay

class Queue:
    # TODO: we also need to inject the async delay time into the constructor
    # TODO: finna út hvernig thread draslið virkar
    def __init__(self, async_delay: int):
        self.__thread = threading.Thread(target=self.__process)
        self.__thread.daemon = True
        self.__thread.start()
        self.command_queue = queue.Queue() #queue.Queue() er python queue klasinn til að halda utan um fifo queue
        self.__process() #keyra process fallið

    #bæta við command í queue
    def add(self, command: Command):
        self.command_queue.put(command) #setja command í queue
    #keyra commands, passa async await
    #passa null
    def __process(self):
        while True:
            try:
                command = self.command_queue.get(timeout=command.async_delay) #TODO: remove command.async_delay, nota async_delay sem injected dependency
                if command is not None:
                    command.execute()
                    self.command_queue.task_done()
            except queue.Empty:
                time.sleep(timeout = 5) #sleepa í 5 sek ef queue er tómt
