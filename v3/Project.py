from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from OpenReddit import open_reddit_with_multilogin
from time import sleep
import urllib3
from requests.exceptions import ConnectionError
from SearchReddit import search_reddit
from OpenCommunities import open_communities
from OpenResult import open_random_search_result
from ScrollThrough import scroll_through
from mla_profile_to_id import mla_profile_to_id
from LoginReddit import login_reddit
import threading
from Credentials import credentials_dict

def main(callback, stop_event, scroll_time, upvote_rate, port_number, progress_callback=None):

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
    client = gspread.authorize(creds)
    sheet_id = "1zRsB81g4n6Br8h6cRlStNPBSSbAVQ24LulhZRq2NpTE"
    sheet = client.open_by_key(sheet_id).worksheet("Script data")
    values_list = sheet.get_all_values()
    column_data = [row[6] for row in values_list[1:] if len(row) > 6]
    search_terms = [item for item in column_data if item]

    raw_column_names = [row[0] for row in values_list[1:] if len(row) > 0]
    column_names = []
    for name in raw_column_names:
        if name not in mla_profile_to_id.keys():
            break
        column_names.append(name)
    mla_profile_names = [item for item in column_names if item]
    mla_profile_ids = [mla_profile_to_id[name] for name in mla_profile_names]
    callback(search_terms, None, "Loaded search terms and profiles")

    failed_profiles = []

    username_password_mapping = {row[0]: row[1] for row in values_list[1:] if len(row) > 1 and row[0] in mla_profile_names}

    print(username_password_mapping)

    def find_first_empty_cell_in_column(column):
        """Finds the first empty cell in a given column."""
        col_values = sheet.col_values(column)
        return len(col_values) + 1  # Next empty row index

    def process_profile(profile_id, profile_name):
        start_time = datetime.now()
        start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
        start_row = find_first_empty_cell_in_column(3)

        try:
            # Write start time to the Google Sheet
            sheet.update_cell(start_row, 3, start_time_str)
            callback(None, profile_name, f"Opening profile: {profile_name}")
            driver = open_reddit_with_multilogin(profile_id, port_number)
            login_reddit(driver, profile_name, username_password_mapping[profile_name])
            print("logged in")
            sleep(5)
            
            callback(None, profile_name, "Searching Reddit")
            search_reddit(driver, search_terms)
            sleep(3)
            callback(None, profile_name, "Opening communities tab")
            open_communities(driver)
            sleep(5)
            callback(None, profile_name, "Opening random community")
            subreddit_name = open_random_search_result(driver)
            sheet.update_cell(start_row, 5, subreddit_name)
            sleep(3)
            callback(None, profile_name, "Scrolling through community")

            # Start a thread to update the progress bar
            progress_thread = threading.Thread(target=update_progress, args=(progress_callback, stop_event, 60*scroll_time))
            progress_thread.start()

            # Call scroll_through with the scroll time and upvote rate
            scroll_through(driver, scroll_time, upvote_rate)

            progress_thread.join()  # Ensure the progress thread finishes
            driver.quit()

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds() / 60.0  # Duration in minutes
            sheet.update_cell(start_row, 4, f"{duration:.2f} minutes")

            callback(None, profile_name, "Profile processing complete")
            sleep(20)
            return True
        except (ConnectionError, urllib3.exceptions.NewConnectionError) as e:
            print(f"Connection error with profile ID {profile_id}: {e}")
            sleep(20)
            return False
        except Exception as e:
            print(f"An unexpected error occurred with profile ID {profile_id}: {e}")
            return False

    def update_progress(progress_callback, stop_event, duration):
        for i in range(duration):
            if stop_event.is_set():
                progress_callback(0, duration // 60)  # Reset progress bar
                return
            progress_callback(i + 1, duration // 60)  # Update progress bar
            sleep(1)

    i = 0
    while i < len(mla_profile_ids):
        if stop_event.is_set():
            callback([], "Stopped", "Stopped by user")
            return
        profile_id = mla_profile_ids[i]
        profile_name = mla_profile_names[i]
        if not process_profile(profile_id, profile_name):
            failed_profiles.append(profile_id)
        i += 1

    # Retry failed profiles
    retry_failed = True
    while retry_failed and failed_profiles:
        retry_failed = False
        remaining_profiles = []
        for profile_id in failed_profiles:
            if stop_event.is_set():
                callback([], "Stopped", "Stopped by user")
                return
            if not process_profile(profile_id, profile_name):
                remaining_profiles.append(profile_id)
                retry_failed = True
        if len(remaining_profiles) == len(failed_profiles):
            break
        failed_profiles = remaining_profiles

    callback([], "Finished", "All profiles processed")
