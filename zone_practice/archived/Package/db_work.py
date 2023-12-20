import sqlite3
from datetime import date


# ----------------------------------------------------------------------------------
# -------------------------------   HELPER FUNCTIONS -------------------------------
# ----------------------------------------------------------------------------------

# Goal: remove " and ' from string
# --------------------------------
# Input: string
# Output: updated string
# Comments: " and ' in strings clashes with sql commands
def clear(strin):
    for letter in strin:
        if letter == "\'" or letter == "\"":
            strin = strin.replace(letter, '')
    return strin


# Goal: Check which date is later
# -------------------------------
# Input: two dates in string format
# Output: 1 if later, 0 if earlier or same day
# Comment: some sql commands needs retrieval of later dates than some date
def isLaterDate(date1, date2):
    # Same day will return 0

    year1, month1, day1 = date1[:4], date1[5:7], date1[8:10]
    year2, month2, day2 = date2[:4], date2[5:7], date2[8:10]

    if year1 > year2:
        return 1
    if year1 < year2:
        return 0

    if month1 > month2:
        return 1
    if month1 < month2:
        return 0

    if day1 > day2:
        return 1
    if day1 < day2:
        return 0

    return 0


def add_to_db_short(row):
    try:
        conn = sqlite3.connect("first_db.db")
        cursor = conn.cursor()

        print(f'insert into active_tenders_short values({row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, '
              f'{row[5]}, {row[6]})')

        cursor.execute(
            f'insert into active_tenders_short values("{row[0]}", "{clear(row[1])}", "{row[2]}", "{row[3]}", '
            f'"{row[4]}", "{row[5]}", "{row[6]}")')

        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        print("Error", error)


def add_to_db_full(row):
    try:
        conn = sqlite3.connect("first_db.db")
        cursor = conn.cursor()

        print(f'insert into active_tenders_full values({row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, '
              f'{row[5]}, {row[6]})')

        cursor.execute(f'insert into active_tenders_full values("{row[0]}", "{clear(row[1])}", "{row[2]}", "{row[3]}", '
                       f'"{row[4]}", "{clear(row[5])}", "{row[6]}")')

        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        print("Error", error)


def show_all_tenders():
    return_container = []
    try:
        conn = sqlite3.connect("first_db.db")
        cursor = conn.cursor()

        short = cursor.execute("select * from active_tenders_short")
        list_short = short.fetchall()  # that will give me list of lists

        full = cursor.execute("select * from active_tenders_full")
        list_full = full.fetchall()

        conn.commit()
        conn.close()

        for k in range(0, len(list_short)):
            return_container.append([list_short[k][0], list_short[k][1], list_short[k][2], list_short[k][3],
                                     list_short[k][4], list_short[k][5], list_short[k][6], list_full[k][1],
                                     list_full[k][2], list_full[k][3], list_full[k][4], list_full[k][5],
                                     list_full[k][6]])

    except sqlite3.Error as error:
        print("Error", error)

    return return_container


def retrieve_expired_to_analyze():
    tenders_to_pass = []

    try:
        conn = sqlite3.connect("first_db.db")
        cursor = conn.cursor()

        expired_tenders = cursor.execute("select id, name, end_date from active_tenders_short").fetchall()
        conn.close()

        for tender in expired_tenders:
            # tender is set E.g. ("123456", "name of tender", "2022-06-09 19:30:01")
            if isLaterDate(str(date.today()), tender[2][:10]):
                tenders_to_pass.append(tender)

    except sqlite3.Error as error:
        print("Error", error)

    return tenders_to_pass

# print(len(retrieve_expired_to_analyze()))
