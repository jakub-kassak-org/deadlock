import schedule
import time
from notifications import notify_for_errors
from users import update_users

schedule.every(10).minutes.do(notify_for_errors)
schedule.every(10).minutes.do(update_users)

while True:
    try:
        schedule.run_pending()
    except Exception:
        pass
    time.sleep(60)
