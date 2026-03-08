import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR/"config"/"settings.yaml"


output_file = BASE_DIR/"data"/"users.csv"
print(output_file)
num_records = 10000

# Base data
base_email = "@etlpipeline.com"
base_first_name = "Suresh"
base_last_name = "Tamang"
base_avatar = "https://ktm.datacenter/images/avatar.png"

# opeint csv for writing
with open(output_file, mode="a", newline='') as file:
    writer = csv.writer(file)
    
    # write header first
    writer.writerow(["id", "email", "first_name", "last_name", "avatar"])
    
    # write rows in the csv file
    for i in range(1, num_records + 1):
        email = f"{base_first_name.lower()}{i}{base_email}"
        first_name=f"{base_first_name}{i}"
        last_name=f"{base_last_name}{i}"
        avatar=f"{base_avatar}?id={i}"
        writer.writerow([i, email, first_name, last_name, avatar])
        
        
print(f"Generated {num_records} user records in {output_file}")