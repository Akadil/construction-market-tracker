import csv

"""with open("tenders.csv", 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        print(row)
"""

imp = open('tenders.csv', 'r')

out = open('tenders.csv', 'w')

writer = csv.

for row in csv.DictReader(imp):

    if row['id'] != '123456':

        writer.writerow(row)

imp.close()

out.close()
