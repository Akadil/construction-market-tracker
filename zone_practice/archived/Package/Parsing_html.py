import urllib3
import requests
import json

urllib3.disable_warnings()


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------- HELPER FUNCTIONS ---------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Goal: make sum number more beautiful
# ------------------------------------
# Input: sum string
# Output: updated sum string
def beautiful_number(sum):
    sum = str(sum)
    ostatok = ''
    for i in range(0, len(sum)):
        if sum[i] == ',' or sum[i] == '.':
            ostatok = sum[i + 1:]
            sum = sum[:i]
            break

    count = 1
    for i in range(len(sum) - 1, -1, -1):
        if count == 3:
            if i == 0:
                continue
            sum = sum[:i] + ',' + sum[i:]
            count = 1
            continue
        count = count + 1
    if ostatok != '':
        sum = sum + '.' + ostatok
    return sum


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


# ----------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------- MAIN FUNCTIONS ----------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def getResponse(url):
    payload = ""
    headers = {
        'Authorization': "Bearer 0868fc5569b5384f0655ac49131e536c",
        'cache-control': "no-cache",
        'Postman-Token': "0868fc5569b5384f0655ac49131e536c"
    }
    response = requests.request("GET", url, data=payload, headers=headers, verify=False)
    return json.loads(response.text)


def addTender(info, date, all_tenders, all_announcements, different_statuses):
    for rec in info['items']:
        if 'number_anno' in rec and rec['id'] in all_announcements:
            break
        if 'total_sum' in rec and rec['total_sum'] < 100000000:
            continue
        if 'publish_date' in rec and (isLaterDate(date, rec['publish_date'])):
            continue
        if 'ref_buy_status_id' in rec and not (rec['ref_buy_status_id'] in different_statuses):
            continue
        # if 'name_ru' in rec and rec['name_ru']

        num_anno = ""
        name_ru = ""
        status = ""
        publish = ""
        end_date = ""
        total_sum = ""
        org_bin = ""

        if 'number_anno' in rec:
            all_announcements.append(rec['id'])
            num_anno = rec['id']
        if 'name_ru' in rec:
            name_ru = rec['name_ru']
        if 'ref_buy_status_id' in rec:
            status = different_statuses[rec['ref_buy_status_id']]
        if 'publish_date' in rec:
            publish = rec['publish_date']
        if 'end_date' in rec:
            end_date = rec['end_date']
        if 'total_sum' in rec:
            total_sum = beautiful_number(rec['total_sum'])
        if 'org_bin' in rec:
            org_bin = rec['org_bin']

        all_tenders.append(
            {'anno': num_anno, 'name': name_ru, 'publish': publish, 'date': end_date,
             'sum': total_sum, 'status': status, 'org_bin': org_bin}
        )


def main():
    info1 = getResponse("https://ows.goszakup.gov.kz/v3/trd-buy/bin/920940000211")
    info2 = getResponse("https://ows.goszakup.gov.kz/v3/trd-buy/bin/150240013905")

    all_tenders = []
    all_announcements = []
    different_statuses = {210: 'Опубликовано', 220: 'Прием заявок',
                          250: 'Рассмотрение заявок', 440: 'На обжаловании'}
    date = "2022-02-01"

    addTender(info1, date, all_tenders, all_announcements, different_statuses)
    next_page = info1['next_page']
    i = 0
    while True:
        if i == 10:
            break
        info1 = getResponse("https://ows.goszakup.gov.kz" + next_page)
        addTender(info1, date, all_tenders, all_announcements, different_statuses)
        i = i + 1

    addTender(info2, date, all_tenders, all_announcements, different_statuses)
    next_page = info2['next_page']
    i = 0
    while True:
        if i == 10:
            break
        info2 = getResponse("https://ows.goszakup.gov.kz" + next_page)
        addTender(info2, date, all_tenders, all_announcements, different_statuses)
        i = i + 1

    return all_tenders


#print(main()[0])
