import csv

fieldnames = ['id', 'name', 'sum', 'organizer', 'client', 'start_date', 'end_date', 'status', 'tech_level',
              'response_level', 'time_given', 'designer', 'designer_date']

with open("tenders.csv", 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
