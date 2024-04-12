import multiprocessing
import random as rd
import time
import threading


# creating trapezoid class
class Trapezoid:

    def __init__(self, trap=None):
        if trap is None:
            trap = [0, 0, 0]
        self.a = min(trap)
        self.b = max(trap)
        self.h = sum(trap) - self.a - self.b

    def __str__(self):
        return 'ტოლფერდა ტრაპეციის დიდი ფუძეა -> {}, პატარა ფუძეა -> {}, ხოლო სიმაღლეა ->{}'.format(self.b, self.a,
                                                                                                    self.h)

    def area(self):
        return (self.a + self.b) / 2 * self.h

    def __lt__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() < other.area()
        return False

    def __eq__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() == other.area()

        return False

    def __ge__(self, other):
        if isinstance(other, Trapezoid):
            return not self.__lt__(other)
        return False

    def __add__(self, other):
        return self.area() + other.area()

    def __sub__(self, other):
        return self.area() - other.area()

    def __mod__(self, other):
        return self.area() % other.area()


# creating rectangle class which is child of trapezoid
class Rectangle(Trapezoid):
    def __init__(self, re=None):
        if re is None:
            re = [0, 0]
        super().__init__([re[0], re[0], re[1]])

    # ტრაპეზოიდის ფართობი არასწორად მუშაოს Rectangle კლასისთვის, მაგიტომ აქ გადავუტვირთე
    def area(self):
        return self.a * self.b

    def __str__(self):
        return "მართკუთხედის სიმაღლეა -> {}, ხოლო სიგანე -> {}".format(self.a, self.h)


# creating square class which is child of rectangle
class Square(Rectangle):
    def __init__(self, c):
        super().__init__([c, c])

    def __str__(self):
        return "კვადრატის გვერდია -> {}".format(self.a)


# functions to calculate generate areas
def trapezoid_area(arr):
    for i in arr:
        T = Trapezoid(i)
        T.area()
        # you can print here parameters if you want
        # print(T, "ფართობით", T.area())


def rectangle_area(arr):
    for i in arr:
        R = Rectangle(i)
        R.area()
        # you can print here parameters if you want
        # print(R,"ფართობით",  R.area())


def square_area(arr):
    for i in arr:
        S = Square(i)
        S.area()
        # you can print here parameters if you want
        # print(S, "ფართობით", S.area())


# this function is used to calculate time to compute areas of 10000 trapezoid, rectangle and square in general
# without threads or processes
def regular(arr):
    start = time.perf_counter()

    trapezoid_area(arr)
    rectangle_area(arr)
    square_area(arr[0])

    finish = time.perf_counter()

    print('in general Finished in: ', round(finish - start, 2), 'second(s)')


# this function is used to calculate time to compute areas of 10000 trapezoid, rectangle and square using threads


def threads(arr):
    start1 = time.perf_counter()

    t1 = threading.Thread(target=trapezoid_area, args=(arr,))
    t1.start()
    t2 = threading.Thread(target=rectangle_area, args=(arr,))
    t2.start()

    t1.join()
    t2.join()

    finish1 = time.perf_counter()
    print('with threads Finished in: ', round(
        finish1 - start1, 2), 'second(s)')


# this function is used to calculate time to compute areas of 10000 trapezoid, rectangle and square using processes
def multiprocess(arr):
    start2 = time.perf_counter()

    p1 = multiprocessing.Process(target=trapezoid_area, args=(arr,))
    p2 = multiprocessing.Process(target=rectangle_area, args=(arr,))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    finish2 = time.perf_counter()
    print('with pools Finished in: ', round(finish2 - start2, 2), 'second(s)')


def run_threads(arr):
    for _ in range(20):
        t1 = threading.Thread(target=trapezoid_area, args=(arr,))
        t2 = threading.Thread(target=rectangle_area, args=(arr,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()


# შეჯვარებული ვერსია
def multiprocess_and_threads(arr):
    start3 = time.perf_counter()
    processes = []
    for _ in range(5):
        process = multiprocessing.Process(target=run_threads, args=(arr,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    finish3 = time.perf_counter()
    print('with multiprocess and threads in: ', round(finish3 - start3, 2), 'second(s)')


if __name__ == "__main__":
    # Generating parameters for 10000 trapezoids: big base, small base and height
    trapezoids = [[rd.randint(1, 200), rd.randint(
        1, 200), rd.randint(1, 200)] for _ in range(100000)]

    # Generating parameters for 10000 rectangles: width and height
    rectangles = [[rd.randint(1, 200), rd.randint(1, 200)] for _ in range(100000)]

    # Generating parameters for 10000 squares
    squares = [rd.randint(1, 200) for _ in range(100000)]

    regular(trapezoids)
    # in general Finished in:  0.18 second(s)

    threads(trapezoids)
    # with threads Finished in:  0.19 second(s)
    # ყველაზე სწრაფია გამოთვლა ჩვეულებრივი პითონით და Threads ბიბლიოთეკით

    multiprocess(trapezoids)
    # with pools Finished in:  0.78 second(s)

    multiprocess_and_threads(trapezoids)
    # with multiprocess and threads in:  5.24 second(s)
    # როგორც ვხედავთ ჰიბრიდული გამოვიდა ყველაზე ნელი

    rectangle1 = Rectangle([10, 5])
    square1 = Square(10)

    print(f'Sum: {rectangle1 + square1},'
          f' Difference: {rectangle1 - square1},'
          f' Dividing with remains: {rectangle1 % square1}')
    # ასევე ლოგიკური ოპერატორებიც მუშაობენ
