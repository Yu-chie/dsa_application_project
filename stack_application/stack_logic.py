class Car:
    def __init__(self, plate_number, arrival_count, departure_count):
        self.plate_number = plate_number
        self.arrival_count = arrival_count
        self.departure_count = departure_count

class StackParkingGarage:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.garage_stack = [] 
        self.car_arrival_tracker = {}
        self.car_departure_tracker = {}

    def park_car(self, plate_number):
        if len(self.garage_stack) >= self.capacity:
            return False, "Error: Garage is full."
        
        arr_count = self.car_arrival_tracker.get(plate_number, 0) + 1
        self.car_arrival_tracker[plate_number] = arr_count
        dep_count = self.car_departure_tracker.get(plate_number, 0)
        
        new_car = Car(plate_number, arr_count, dep_count)
        self.garage_stack.append(new_car)
        return True, f"Car {plate_number} parked."

    def remove_top_car(self):
        """Standard Pop: Removes the car at the very top."""
        if not self.garage_stack:
            return False, "Error: Garage is empty."
        
        removed_car = self.garage_stack.pop()
        
        # Update departure count
        new_dep_count = self.car_departure_tracker.get(removed_car.plate_number, 0) + 1
        self.car_departure_tracker[removed_car.plate_number] = new_dep_count
        
        return True, f"Top car {removed_car.plate_number} removed."

    def remove_specific_car(self, target_plate):
        """Shuffle Pop: Moves cars to a temp stack to reach a specific plate."""
        target_plate = target_plate.upper()
        
        plates_in_garage = [car.plate_number for car in self.garage_stack]
        if target_plate not in plates_in_garage:
            return False, f"Error: Car {target_plate} not found."

        # If it's already at the top, just use the simple remove
        if self.garage_stack[-1].plate_number == target_plate:
            return self.remove_top_car()

        temp_stack = []
        
        # 1. Move cars above target to temp stack
        while self.garage_stack[-1].plate_number != target_plate:
            moving_car = self.garage_stack.pop()
            
            # Increment departure for the car moving out of the way
            self.car_departure_tracker[moving_car.plate_number] = \
                self.car_departure_tracker.get(moving_car.plate_number, 0) + 1
            
            temp_stack.append(moving_car)
        

        # 2. Remove the target car
        removed_car = self.garage_stack.pop()
        self.car_departure_tracker[removed_car.plate_number] = \
            self.car_departure_tracker.get(removed_car.plate_number, 0) + 1
        
        # 3. Put the cars back
        while temp_stack:
            returning_car = temp_stack.pop()
            
            # Increment arrival for the car returning to the garage
            self.car_arrival_tracker[returning_car.plate_number] = \
                self.car_arrival_tracker.get(returning_car.plate_number, 0) + 1
            
            # Update the car object with its new counts before pushing it back
            returning_car.arrival_count = self.car_arrival_tracker[returning_car.plate_number]
            returning_car.departure_count = self.car_departure_tracker[returning_car.plate_number]
            
            self.garage_stack.append(returning_car)

        return True, f"Specific car {target_plate} removed. Other cars shifted and re-entered."

    def display_status(self):
        print("\n" + "="*60)
        print("           STACK PARKING GARAGE SIMULATOR")
        print("="*60)
        print("\nPARKING PLACEMENT")
        for i in range(self.capacity, 0, -1):
            car_label = "EMPTY"
            if i <= len(self.garage_stack):
                car_label = self.garage_stack[i-1].plate_number
            print(f"[{i:2}] | {car_label:^18} |")
        
        print("\nTRANSACTION TABLE (Current Cars)")
        print(f"{'No.':<5} {'Plate Number':<18} {'Arrived':<10} {'Departed':<10}")
        for idx, car in enumerate(self.garage_stack):
            print(f"{idx+1:<5} {car.plate_number:<18} {car.arrival_count:<10} {car.departure_count:<10}")
        print("="*60)

if __name__ == "__main__":
    garage = StackParkingGarage(capacity=10)
    
    while True:
        garage.display_status()
        print("\nCommands: 'park [plate]', 'remove' (top), 'remove [plate]' (specific)")
        user_input = input("Enter command: ").strip().split()

        if not user_input: continue
        
        cmd = user_input[0].lower()
        if cmd == "park" and len(user_input) > 1:
            _, msg = garage.park_car(user_input[1].upper())
            print(msg)
        elif cmd == "remove":
            if len(user_input) > 1:
                _, msg = garage.remove_specific_car(user_input[1])
            else:
                _, msg = garage.remove_top_car()
            print(msg)
        elif cmd == "exit":
            break