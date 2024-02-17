import gorniy
import schedule
import time
def start_parse():
    start = gorniy

schedule.every().day.at("16:21").do(start_parse)

while True:
    schedule.run_pending()
    time.sleep(1)
    print(1)