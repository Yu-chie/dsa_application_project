from queue_application.file_manager import FileManager
import random

# PARKING GARAGE CLASS DEFINITION
class ParkingGarage:
    def __init__(self, max_parking=10, file_manager=None, mode="MANUAL"):
        self.max_parking = max_parking      # max parking size
        self.queue = [None] * max_parking   # parking queue'
        
        # File Handling
        self.records = {}                   # to track all car records
        self.file_manager = file_manager    
        if file_manager:
            self.records = file_manager.load_records()
        
        # Game-related attributes
        self.mode = mode           # manual or auto
        self.waiting = []          # Cars waiting to be parked
        self.max_waiting = 3       # limit 3
        self.failed_cars= 0
        self.score = 0
        self.max_failed = 5        # game over condition
        self.game_over = False
        self.available_plates = [f"car{str(i).zfill(2)}" for i in range(1, 11)]
        
    # Save current records to file
    def save_records(self):
        if self.file_manager:
            self.file_manager.save_records(self.records)
            
    # OPTION 1: ENQUEUE CAR
    def car_arrives(self, plate_number):
        # If parking is full
        if None not in self.queue:
            if len(self.waiting) < self.max_waiting:
                self.add_to_waiting(plate_number)
                return "Parking full. Car added to waiting area."
            return "Parking Garage and Waiting Area are Full"

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
        self.score += 10
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
        
        # Fill remaining slots with none
        new_queue += [None] * (self.max_parking - len(new_queue))   # fill remaining with None
        self.queue = new_queue
        self.save_records()
        
        self.score += 2
        return f"Car {target_plate} departed. {len(temp_queue)} cars shuffled."

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
                
    def add_to_waiting(self, plate_number):
        if len(self.waiting) >= self.max_waiting:
            return "Waiting Area Full"
        
        wait_time = random.randint(10, 20)  # Adjusted to a more reasonable range
        self.waiting.append({
            "plate_number": plate_number,
            "time_left": wait_time  # Use the adjusted wait time
        })
        return "Car added to waiting area"
    
    def update_waiting(self):
        expired = []
        for car in self.waiting:
            if car["time_left"] > 0:
                car["time_left"] -= 1  # Decrease time left by 1 second
            if car["time_left"] == 0:
                expired.append(car)

        for car in expired:
            self.waiting.remove(car)
            self.failed_cars += 1
            self.score -= 5  # penalty

            if self.failed_cars >= self.max_failed:
                self.game_over = True

        # Ensure the GUI updates after changes
        if hasattr(self, 'draw_waiting_area'):
            self.draw_waiting_area()

        return expired
    
    def get_stats(self):
        total_arrivals = sum(car["arrival_count"] for car in self.records.values())
        total_departures = sum(car["departure_count"] for car in self.records.values())

        return {
            "total_arrivals": total_arrivals,
            "total_departures": total_departures,
            "failed_cars": self.failed_cars,
            "score": self.score,
            "game_over": self.game_over
        }
        
    def get_random_plate(self):
        used = {car['plate_number'] for car in self.queue if car}
        used |= set(self.waiting[i]["plate_number"] for i in range(len(self.waiting)))
        
        choices = [plate for plate in self.available_plates if plate not in used]
        if not choices:
            return None
        
        return random.choice(choices)
    
    # New round
    def reset_game_state(self):
        self.queue = [None] * self.max_parking
        self.waiting.clear()
        self.failed_cars = 0
        self.score = 0
        self.game_over = False
        self.available_plates = [f"car{str(i).zfill(2)}" for i in range(1, 11)]

    # New game + wiped records
    def reset_all(self):
        self.reset_game_state()
        self.records.clear()
        self.save_records()

