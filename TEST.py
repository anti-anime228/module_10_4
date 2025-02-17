import threading
from random import randint
from queue import Queue
import time


class Table:

    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(threading.Thread):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time.sleep(randint(3, 10))


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        for guest in guests:
            if any(table.guest is None for table in self.tables):
                for table in self.tables:
                    if table.guest is None:
                        table.guest = guest
                        guest.start()
                        print(f"{guest.name} сел(-а) за стол номер {table.number}")
                        break
            else:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None
                    break
            if not self.queue.empty() and any(table.guest is None for table in self.tables):
                for table in self.tables:
                    if table.guest is None:
                        guest = self.queue.get()
                        table.guest = guest
                        guest.start()
                        print(f"{guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
                        break


tables = [Table(number + 1) for number in range(5)]
guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman', 'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya',
                'Alexandra']

guests = [Guest(name) for name in guests_names]
cafe = Cafe(*tables)

cafe.guest_arrival(*guests)

cafe.discuss_guests()
