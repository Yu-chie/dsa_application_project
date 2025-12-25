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
        self.queue = [None] * max_parking   # parking queue'
        self.records = {}               # to track all car records
        
    # Method to save all records in a file
    def save_records(self, filename='parking_records.txt'):
        with open(filename, 'w') as file:
            file.write("Plate Number | Arrival Count | Departure Count\n")
            file.write("-" * 50 + "\n")
            for car in self.records.values():
                file.write(f"{car['plate_number']} | {car['arrival_count']} | {car['departure_count']}\n")
        
    # OPTION 1: ENQUEUE CAR
    def car_arrives(self):
        # If parking is full
        if None not in self.queue:
            print("Parking Garage is Full")
            return
        
        plate_number = input("Enter Plate Number: ")
        
        # Prevent duplicate entries
        for car in self.queue:
            if car is not None and car['plate_number'] == plate_number:
                print("Car with this Plate Number is already in the Garage.")
                return
        
        # If car already has a record, update arrival count
        if plate_number in self.records:
            car = self.records[plate_number]
            car['arrival_count'] += 1
        # If new car, create record
        else:
            car = {
                'plate_number': plate_number,
                'arrival_count': 1,
                'departure_count': 0
            }
            self.records[plate_number] = car
         
        # Enqueue car in first empty slot
        for i in range(self.max_parking):
            if self.queue[i] is None:
                self.queue[i] = car
                break
        
        print("Car Parked Successfully!")

    # OPTION 2: DEQUEUE CAR
    def car_departs(self):
        # If parking is empty
        if all(slots is None for slots in self.queue):
            print("Parking Garage is Empty")
            return
        
        target_plate = input("Enter Plate Number to Depart: ")
        temp_queue = []
        found = False
        
        # FIFO
        for car in self.queue:
            if car is None:
                continue
            
            if car['plate_number'] == target_plate and not found:
                # Permanent exit and record
                car['departure_count'] += 1
                found = True
                print(f"Car with Plate Number {target_plate} Departed Successfully!.")
            else:
                # Temporary exit and re-entry
                car['departure_count'] += 1
                car['arrival_count'] += 1
                temp_queue.append(car)
                
        if not found:
            print(f"Car with Plate Number {target_plate} Not Found in Garage.")
            return
        
        self.queue = [None] * self.max_parking
        for i, car in enumerate(temp_queue):
            self.queue[i] = car

# OPTION 3: DISPLAY PARKING TABLE
    def display_table(self):
        # Display table header
        # : formatting starts ^ center aligned 15 width of column
        print("\n{:^7} | {:^20} | {:^20} | {:^20}".format(
            'Slot', 'Plate Number', '# of Arrival.', '# of Departure.'))
        print("-" * 70)
        
        # Display each car in the queue
        for i in range(self.max_parking):
            car = self.queue[i]
            if car is None:
                print("{:^7} | {:^20} | {:^20} | {:^20}".format(
                    i + 1, '-', '-', '-'
                ))
            else:
                print("{:^7} | {:^20} | {:^20} | {:^20}".format(
                    i + 1,
                    car['plate_number'],
                    car['arrival_count'],
                    car['departure_count']
                ))

# MAIN PROGRAM LOOP
garage = ParkingGarage(max_parking=10)  # Set max parking size

while True:
    garage.display_table()
    
    # Display Menu Options
    print("\n===== Parking Garage Menu =====")
    print("1. Car Arrives")
    print("2. Car Departs")
    print("3. Exit")
    choice = input("Enter your choice (1-3): ")
    
    if choice == '1':
        garage.car_arrives()
    elif choice == '2':
        garage.car_departs()
    elif choice == '3':
        print("Exiting Parking Garage Simulator. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 3.")
