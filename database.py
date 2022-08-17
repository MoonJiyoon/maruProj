import os
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# scope = [
#     'https://spreadsheets.google.com/feeds',
#     'https://www.googleapis.com/auth/drive',
# ]
#
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')
#
# json_file_name = os.path.join(data_dir,'maru-project-359711-74f2b1e9471f.json')
#
# credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
# gc = gspread.authorize(credentials)
#
# spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1JtOx1b1XiB-DGHNkpFrKEATCNvc-btbuYVwqtMU86Vo/edit?usp=sharing'
#
# doc = gc.open_by_url(spreadsheet_url)
# worksheet = doc.worksheet('score')
# worksheet.clear()
# worksheet.insert_row(['name','score','accuracy'],1)
# worksheet.insert_row(['jiyoon',2,0.8],2)






class Database(object):
    path = os.path.join(data_dir, 'hiScores.db')
    numScores = 15

    @staticmethod
    def getSound(music=False):
        conn = sqlite3.connect(Database.path)
        c = conn.cursor()
        if music:
            c.execute("CREATE TABLE if not exists music (setting integer)")
            c.execute("SELECT * FROM music")
        else:
            c.execute("CREATE TABLE if not exists sound (setting integer)")
            c.execute("SELECT * FROM sound")
        setting = c.fetchall()
        conn.close()
        return bool(setting[0][0]) if len(setting) > 0 else False

    @staticmethod
    def setSound(setting, music=False):
        conn = sqlite3.connect(Database.path)
        c = conn.cursor()
        if music:
            c.execute("DELETE FROM music")
            c.execute("INSERT INTO music VALUES (?)", (setting,))
        else:
            c.execute("DELETE FROM sound")
            c.execute("INSERT INTO sound VALUES (?)", (setting,))
        conn.commit()
        conn.close()

    @staticmethod
    def getScores():
        conn = sqlite3.connect(Database.path)
        c = conn.cursor()
        c.execute('''CREATE TABLE if not exists scores
                     (name text, score integer, accuracy real)''')
        c.execute("SELECT * FROM scores ORDER BY score DESC")
        hiScores = c.fetchall()
        conn.close()
        return hiScores

    @staticmethod
    def setScore(hiScores, entry):
        name, score, accuracy =entry
        # worksheet.insert_row([name,score,accuracy],2)

        conn = sqlite3.connect(Database.path)
        c = conn.cursor()
        if len(hiScores) == Database.numScores:
            lowScoreName = hiScores[-1][0]
            lowScore = hiScores[-1][1]
            c.execute("DELETE FROM scores WHERE (name = ? AND score = ?)",
                      (lowScoreName, lowScore))
        c.execute("INSERT INTO scores VALUES (?,?,?)", entry)
        conn.commit()
        conn.close()


