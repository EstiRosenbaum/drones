import datetime
import os

from modules.setup_env import get_env_instance


def delete_old_logs_files():
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(int(get_env_instance().DAYS_TO_DELETE_LOG))

    for file_name in os.listdir("src/server/utils/logger"):
        try:
            if file_name.endswith(".log"):
                remove_log_file(week_ago, file_name)
        except ValueError:
            continue


def remove_log_file(week_ago, file_name):
    file_date_str = file_name.split(".")[0]
    file_date = datetime.datetime.strptime(file_date_str, "%Y-%m-%d").date()
    if file_date == week_ago:
        file_path = os.path.join("src/server/utils/logger", file_name)
        os.remove(file_path)
