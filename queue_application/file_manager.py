import os

class FileManager:
    def __init__(self, folder='queue_application', default_file='parking_records.txt'):
        self.folder = folder
        self.default_file = default_file
        os.makedirs(self.folder, exist_ok=True) # Ensure folder exists
        self.file_path = None
        if not os.path.exists(self.default_file):
            with open(self.file_path, 'w') as file:
                file.write("Plate Number | Arrival Count | Departure Count\n")
                file.write("-" * 50 + "\n")

    # Load existing records from file
    def load_records(self):
        records = {}
        try:
            with open(self.file_path, 'r') as file:
                next(file)  # Skip header
                next(file)  # Skip separator
                for line in file:
                    plate_number, arrival_count, departure_count = line.strip().split(' | ')
                    records[plate_number] = {
                        'plate_number': plate_number,
                        'arrival_count': int(arrival_count),
                        'departure_count': int(departure_count)
                    }
        except FileNotFoundError:
            pass  # No existing records file
        return records
        
    # Method to save all records in a file
    def save_records(self, records):
        with open(self.file_path, 'w') as file:
            file.write("Plate Number | Arrival Count | Departure Count\n")
            file.write("-" * 50 + "\n")
            for car in records.values():
                file.write(f"{car['plate_number']} | {car['arrival_count']} | {car['departure_count']}\n")
     