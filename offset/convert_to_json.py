import sqlite3
import json


db = sqlite3.connect('workua.sqlite')
cur = db.cursor()

result_list = []

info = cur.execute("SELECT * FROM jobs")
for row in info:
        tmp_dict = {
            'workua_id': row[0],
            'company': {
                'name': row[2],
                'address': row[3]
            },
            'vacancy': {
                'position': row[1],
                'salary': row[4]
            }
        }
        result_list.append(tmp_dict)

with open("workua.json", "w", encoding="utf-8") as file:
    json.dump(result_list, file, ensure_ascii=False)

db.close()
