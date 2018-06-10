import csv
import os


DATA_PATH = os.path.join("./data", "international")

SOURCE_FILE = os.path.join(DATA_PATH, "wc-qualification-europe.csv")
OUTPUT_FILE = os.path.join(DATA_PATH, "wc-qualification-europe_new.csv")

FTHG = 'home_team_goal_count'
FTAG = 'away_team_goal_count'

def get_result(FTHG, FTAG):
    if FTHG > FTAG: return 'H'
    if FTHG < FTAG: return 'A'
    return 'D'

with open(SOURCE_FILE,'r') as csvinput:
    with open(OUTPUT_FILE, 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        all = []
        row = next(reader)
        row.append('result')
        all.append(row)

        FTHG_i = row.index(FTHG)
        FTAG_i = row.index(FTAG)

        for row in reader:
            result = get_result(row[FTHG_i], row[FTAG_i])
            row.append(result)
            all.append(row)

        writer.writerows(all)
