import os

class FileManager:
    def __init__(self, folder='queue_application', default_file='parking_records.txt'):
        self.folder = folder
        self.default_file = default_file
        os.makedirs(self.folder, exist_ok=True) # Ensure folder exists
        self.file_path = None
        
    # Choose to create a new file or use an existing file
    def setup_records_file(self):
        print("Choose Records File Option:")
        print("1. Create New File")
        print("2. Use an existing file")
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == '1':
            file_name = input("Enter new filename: ").strip()
            if not file_name:
                file_name = self.default_file
            elif not file_name.endswith(".txt"):
                file_name += ".txt"
                
        elif choice == '2':
            file_name = input("Enter existing filename: ").strip()
            if not file_name.endswith(".txt"):
                file_name += ".txt"
            if not os.path.exists(os.path.join(self.folder, file_name)):
                print("File does not exist. Using default file instead.")
                file_name = self.default_file
        
        else:
            print("Invalid choice. Using default file.")
            file_name = self.default_file
        
        self.file_path = os.path.join(self.folder, file_name)
        
        # Create File if it doesn't exist
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                file.write("Plate Number | Arrival Count | Departure Count\n")
                file.write("-" * 50 + "\n")
                
        return self.file_path

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
     