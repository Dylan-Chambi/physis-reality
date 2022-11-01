from multiprocessing import Process

share_var = 0

class ASD:
    def __init__(self):
        self.share_var = 0

    def loop_a(self):
        print("loop_a")
        while 1:
            self.share_var = 1
            print(self.share_var)

    def loop_b(self):
        while 1:
            self.share_var += 1
            print(self.share_var)
            if self.share_var == 10:
                p1 = Process(target=self.loop_a).start()

    def run(self):
        self.loop_b()

if __name__ == '__main__':
    asd = ASD()
    asd.run()