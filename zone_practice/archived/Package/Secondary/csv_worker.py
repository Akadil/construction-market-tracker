import csv

with open("tenders.csv", 'a', encoding='UTF8') as f:
    writer = csv.writer(f)

    id = '123456'
    name = ''
    sum = ''
    organizer = ''
    client = ''
    start_date = ''
    end_date = ''
    status = ''
    tech_level = ''
    response_level = ''
    time_given = ''
    designer = ''
    designer_date = ''

    row = [id, name, sum, organizer, client, start_date, end_date,
           status, tech_level, response_level, time_given, designer, designer_date]
    writer.writerow(row)
