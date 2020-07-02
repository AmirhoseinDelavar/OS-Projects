import threading
import time

mainMutex = threading.Semaphore()
pathoccupation = []


def wayfounder(loc, des):
    switcher = {
        "12": ["SW"],
        "14": ["SW", "SE", "NE"],
        "13": ["SW", "SE"],
        "21": ["SE", "NE", "NW"],
        "23": ["SE"],
        "24": ["SE", "NE"],
        "31": ["NE", "NW"],
        "32": ["NE", "NW", "SW"],
        "34": ["NE"],
        "41": ["NW"],
        "42": ["NW", "SW"],
        "43": ["NW", "SW", "SE"],
    }
    return switcher.get("{}{}".format(loc, des))


class car(threading.Thread):
    def __init__(self, loc, des):
        threading.Thread.__init__(self)
        self.requiredway = wayfounder(loc, des)
        self.loc = loc
        self.des = des

    def run(self):
        time.sleep(1)
        # print("Car {} to {} ready to move".format(self.loc, self.des))
        flag = True
        while flag:
            occupypath = True
            for cell in self.requiredway:
                mainMutex.acquire()
                if cell in pathoccupation:
                    occupypath = False
                    mainMutex.release()
                    break
                mainMutex.release()
            if occupypath:
                mainMutex.acquire()
                pathoccupation.extend(self.requiredway)
                print("Car {} to {} entered".format(self.loc, self.des))
                mainMutex.release()
                flag = False
            else:
                # print("Car {} to {} wait 2 secs".format(self.loc, self.des))
                time.sleep(2)

        for cell in self.requiredway:
            time.sleep(1)
            mainMutex.acquire()
            pathoccupation.remove(cell)
            mainMutex.release()
            # print("Car {} to {} moved from {}".format(self.loc, self.des, cell))

        print("Car {} to {} moved successfuly".format(self.loc, self.des))


if __name__ == '__main__':
    t1 = car(1, 3)
    t2 = car(3, 1)
    t3 = car(1, 4)
    t4 = car(2, 4)
    t5 = car(3, 1)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()