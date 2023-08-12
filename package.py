class Package:
    def __init__(self, id, address, city, state, zip, deadline, kg, note):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.kg = kg
        self.note = note
        self.status = "At Hub"
        self.load_time = None
        self.delivery_time = None

    def __str__(self):
        return f'{self.id}, {self.address}, {self.city}, {self.state}, {self.zip}, ' \
               f'{self.deadline}, {self.kg}, {self.status}, {self.delivery_time}'



