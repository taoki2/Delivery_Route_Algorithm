class Truck:
    def __init__(self, packages, depart_time):
        self.capacity = 16
        self.speed = 18
        self.packages = packages
        self.miles = 0.00
        self.address = "4001 South 700 East"
        self.depart_time = depart_time

    def __str__(self):
        return f'{self.capacity}, {self.speed}, {self.packages}, ' \
               f'{self.miles}, {self.address}, {self.depart_time}'
