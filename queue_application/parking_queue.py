"""
QUEUE: Parking Garage Simulator
Vertical Parking using FIFO Queue

Arrival and Departure values represent
the order of entry and exit, not time
"""

# PARKING GARAGE CLASS DEFINITION
class ParkingGarage:
    def __init__(self, max_parking=10):
        self.max_parking = max_parking      # max parking size
        self.queue = [None] * max_parking   # parking queue
        self.arrival_counter = 1            # counts arrivals
        self.departure_counter = 1          # counts departures

# OPTION 1: ENQUEUE CAR
    def car_arrives(self):
        # If parking is full
        if None not in self.queue:
            print("Parking Garage is Full")
            return
        
        plate_number = input("Enter Plate Number: ")
        
        car = {
            'plate_number': plate_number,
            'arrival_number': self.arrival_counter,
            'departure_number': "-"
        }
        
        # Enqueue car in first empty slot
        for i in range(self.max_parking):
            if self.queue[i] is None:
                self.queue[i] = car
                break
        
        self.arrival_counter += 1
        print("Car Parked Successfully!")

# OPTION 2: DEQUEUE CAR
    def car_departs(self):
        # If parking is empty
        if len(self.queue) == 0:
            print("Parking Garage is Empty")
        else:
            # Dequeue car
            car = self.queue.pop(0)
            car['departure_number'] = self.departure_counter
            self.departure_counter += 1
            print(f"Car with Plate Number {car['plate_number']} Departed Successfully!")

# OPTION 3: DISPLAY PARKING TABLE
    def display_table(self):
        # If parking is empty
        if len(self.queue) == 0:
            print("Parking Garage is Empty")
        else:
            # Display table header
            # : formatting starts ^ center aligned 15 width of column
            print("\n{:^10} | {:^10} | {:^10} | {:^10}".format('Plate Number', 'Arrival No.', 'Departure No.', 'Parking Slot'))
            print("-" * 55)
            for car in self.queue:
                print("{:^10} | {:^10} | {:^10} | {:^10}".format(
                    car['plate_number'],
                    car['arrival_number'],
                    car['departure_number'],
                    car['parking_slot']
                ))

# MAIN PROGRAM LOOP
garage = ParkingGarage(max_parking=10)  # Set max parking size

while True:
    # Display Menu Options
    print("\n===== Parking Garage Menu =====")
    print("1. Car Arrives")
    print("2. Car Departs")
    print("3. Display Parking Table")
    print("4. Exit")
    choice = input("Enter your choice (1-4): ")
    
    if choice == '1':
        garage.car_arrives()
    elif choice == '2':
        garage.car_departs()
    elif choice == '3':
        garage.display_table()
    elif choice == '4':
        print("Exiting Parking Garage Simulator. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
