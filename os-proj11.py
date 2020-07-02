import threading
import time
import asyncio

NEMutex = threading.Semaphore(1)
SEMutex = threading.Semaphore(1)
SWMutex = threading.Semaphore(1)
NWMutex = threading.Semaphore(1)


def wayfounder(loc, des):
    switcher = {
        "12": [SWMutex],
        "14": [SWMutex, SEMutex, NEMutex],
        "13": [SWMutex, SEMutex],
        "21": [SEMutex, NEMutex, NWMutex],
        "23": [SEMutex],
        "24": [SEMutex, NEMutex],
        "31": [NEMutex, NWMutex],
        "32": [NEMutex, NWMutex, SWMutex],
        "34": [NEMutex],
        "41": [NWMutex],
        "42": [NWMutex, SWMutex],
        "43": [NWMutex, SWMutex, SEMutex],
    }
    return switcher.get("{}{}".format(loc, des))


class Car(threading.Thread):
    def __init__(self, loc, des):
        threading.Thread.__init__(self)
        self.requiredsemaphores = wayfounder(loc, des)
        self.loc = loc
        self.des = des

    def run(self):
        time.sleep(1)
        # print("Car {} to {} ready to move".format(self.loc, self.des))
        for i in range(0, self.requiredsemaphores.__len__()):
            sem = self.requiredsemaphores[i]
            while not sem.acquire(blocking=False):
                for sem0 in self.requiredsemaphores:
                    if sem0 == sem:
                        break
                    else:
                        sem0.release()
                # print("Car {} to {} waits".format(self.loc, self.des))
                time.sleep(2)
                i = 0
                sem = self.requiredsemaphores[i]

        print("Car {} to {} entered".format(self.loc, self.des))
        for sem in self.requiredsemaphores:
            time.sleep(1)
            # print("Car {} to {} moving".format(self.loc, self.des))
            sem.release()
        print("Car {} to {} passed".format(self.loc, self.des))


if __name__ == '__main__':
    t1 = Car(1, 3)
    t2 = Car(3, 1)
    t3 = Car(1, 4)
    t4 = Car(2, 4)
    t5 = Car(3, 1)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
