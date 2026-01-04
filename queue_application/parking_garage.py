from queue_application.file_manager import FileManager

# PARKING GARAGE CLASS DEFINITION
class ParkingGarage:
    def __init__(self, max_parking=10, file_manager=None, mode="MANUAL"):
        self.max_parking = max_parking      # max parking size
        self.queue = [None] * max_parking   # parking queue'
        self.records = {}                   # to track all car records
        self.file_manager = file_manager    
        if file_manager:
            self.records = file_manager.load_records()
        self.mode = mode                    # manual or auto
        
    # Save current records to file
    def save_records(self):
        if self.file_manager:
            self.file_manager.save_records(self.records)
            
    # OPTION 1: ENQUEUE CAR
    def car_arrives(self, plate_number):
        # If parking is full
        if None not in self.queue:
            return "Parking Garage is Full"
        
        # Prevent duplicate entries
        for car in self.queue:
            if car is not None and car['plate_number'] == plate_number:
                return "Car with this Plate Number is already in the Garage."
        
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
        
        self.save_records()
        return "Car Parked Successfully!"

    # OPTION 2: DEQUEUE CAR
    def car_departs(self, target_plate):
        # If parking is empty
        if all(slots is None for slots in self.queue):
            return "Parking Garage is Empty"
        
        # Find target car index
        target_index = None
        for i, car in enumerate(self.queue):
            if car is not None and car['plate_number'] == target_plate:
                target_index = i
                break
            
        if target_index is None:
            return "Car Not Found"
        
        # Cars in front temporarily leave
        temp_queue = []
        for i in range(target_index):
            car = self.queue[i]
            if car is not None:
                # Temporary exit and re-entry
                car['departure_count'] += 1
                car['arrival_count'] += 1
                temp_queue.append(car)
            
        # target car leaves permanently
        self.queue[target_index]['departure_count'] += 1
                
        # Shift cars behind forward
        new_queue = self.queue[target_index + 1:self.max_parking]   # cars after target
        new_queue = [c for c in new_queue if c is not None]         # remove None values
        new_queue.extend(temp_queue)                                # add temporarily exited cars
        new_queue += [None] * (self.max_parking - len(new_queue))   # fill remaining with None
        self.queue = new_queue
        self.save_records()
        return "Car Departed Successfully!"

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