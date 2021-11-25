# -----------------------------------------------------------------
# swapl_concurrency.py
# -----------------------------------------------------------------

import threading
import time

TX_DELAY = 0.01

class MeetingPoint:

    def __init__(self, num = 1):
        self.num = num
        self.value = 0
        self.count = 0
        self.mutex = threading.Lock()
        self.target = 2**num - 1

    def set(self, num = None):
        try:
            self.mutex.acquire()
            if num is not None:
                self.target = 2**num - 1
            self.value = self.value | (1 << self.count)
            self.count += 1
            return self.count - 1
        finally:
            self.mutex.release()

    def leave(self, _id):
        try:
            self.mutex.acquire()
            self.count -= 1
            if self.count == 0:
                self.value = 0
        finally:
            self.mutex.release()

    def check(self):
        try:
            self.mutex.acquire()
            #print("V: {}, T: {}".format(self.value, self.target))
            if self.value == self.target:
                return True
            else:
                return False
        finally:
            self.mutex.release()

    def meet(self, func = None, num = None):
        #self.log('Meet at {}'.format(meeting_point))
        _id = self.set(num)
        #print("object {}, id {}".format(self, _id))
        while not(self.check()):
            if func is not None:
                if func():
                    return False
            time.sleep(TX_DELAY)
        self.leave(_id)
        return True




class Token:

    def __init__(self):
        self.sem = threading.Semaphore(0)

    def give(self):
        self.sem.release()

    def wait(self):
        return self.sem.acquire(False)


"""
    #
    # synchronization methods
    #
    def wait(self, token):
        t = SW.get_token(token)
        while not(t.wait()):
            if self.force_landing:
                raise ForceLandingException()
            if (self.cf is not None)and(self.flying):
                self.cf.commander.send_position_setpoint(self.target_x,
                                                        self.target_y,
                                                        self.target_z,
                                                        self.target_yaw)
            time.sleep(TX_DELAY)

    def give(self, token):
        t = SW.get_token(token)
        t.give()

"""
