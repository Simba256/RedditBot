from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def login_reddit(driver, username, password):

    print("username:", username, "password:", password,"----")

    login_xpath = "/html/body/shreddit-app/reddit-header-large/reddit-header-action-items/header/nav/div[3]/span[3]/faceplate-tracker"
    
    # search for login button if found within 10 seconds then click on it otherwise you are already logged in
    wait = WebDriverWait(driver, 10)
    # login_xpath = "/html/body/shreddit-app/reddit-header-large/reddit-header-action-items/header/nav/div[3]/span[3]/faceplate-tracker/faceplate-tooltip/a"
    # search by id = login-button
    try:
        login_button = wait.until(EC.presence_of_element_located((By.XPATH, login_xpath)))
        try:
            print("XPATH Found:", login_xpath)
            print("Login button found")
            print("Is displayed:", login_button.is_displayed())
            print("Is enabled:", login_button.is_enabled())
            print(login_button)

            login_button_clickable = wait.until(EC.element_to_be_clickable((By.XPATH, login_xpath)))
            print("Clickable login button found")
            login_button_clickable.click()
            print("Login button clicked")

            try:
                email_xpath = "/html/body/shreddit-app/shreddit-overlay-display/span[4]/input"
                email_input = wait.until(EC.presence_of_element_located((By.XPATH, email_xpath)))
                print("Email input found")

                for char in username:
                    email_input.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
                print("Email input filled")

                password_xpath = "/html/body/shreddit-app/shreddit-overlay-display/span[5]/input"
                password_input = wait.until(EC.presence_of_element_located((By.XPATH, password_xpath)))
                print("Password input found")

                for char in password:
                    password_input.send_keys(char)
                    time.sleep(random.uniform(0.05, 0.15))
                print("Password input filled")

                try:
                    # finding login button
                    first_shadow_host = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/shreddit-app/shreddit-overlay-display")))
                    print("First element found")

                    try:
                        first_shadow_root = driver.execute_script('return arguments[0].shadowRoot', first_shadow_host)
                        print("First shadow root found")

                        try:
                            second_shadow_host = first_shadow_root.find_element(By.CSS_SELECTOR, "shreddit-signup-drawer")
                            print("Second host found")

                            try:
                                second_shadow_root = driver.execute_script('return arguments[0].shadowRoot', second_shadow_host)
                                print("Second shadow root found")
                                try:
                                    third_shadow_host = second_shadow_root.find_element(By.CSS_SELECTOR, "shreddit-drawer > div > shreddit-async-loader > div > shreddit-slotter")
                                    print("Third host found")
                                    try:
                                        third_shadow_root = driver.execute_script('return arguments[0].shadowRoot', third_shadow_host)
                                        print("Third shadow root found")
                                        try:
                                            final_login_button = third_shadow_root.find_element(By.CSS_SELECTOR, "#login > auth-flow-modal > div.w-100 > faceplate-tracker > button")
                                            print("Final login button found")

                                            try:
                                                time.sleep(5)
                                                print("Final login button is displayed:", final_login_button.is_displayed())
                                                print("Final login button is enabled:", final_login_button.is_enabled())
                                                while not final_login_button.is_enabled():
                                                    print("Waiting for final signal to be enabled")
                                                    time.sleep(1)
                                                final_login_button.click()
                                                print("Final login button clicked")
                                                return
                                            except:
                                                print("Unable to click final login button")
                                                return

                                        except:
                                            print("Unable to find final login button")
                                            return

                                    except:
                                        print("Unable to find third shadow root")
                                except:
                                    print("Unable to find third shadow root")
                                    return
                            except:
                                print("Unable to find second shadow root")
                                return
                        except:
                            print("Unable to find second shadow host")
                            return

                    except:
                        print("Unable to find first shadow root")
                        return
                except:
                    print("Unable to find final login button")
                    return

            except:
                print("Error filling email and password")
            
        except:
            print("Login button not clickable")
            return
    except:
        print("Alraedy logged in")
        

    return





    # try:
    #     profile_button_xpath = "/html/body/shreddit-app/reddit-header-large/reddit-header-action-items/header/nav/div[3]/div[2]/shreddit-async-loader/faceplate-dropdown-menu/faceplate-tooltip/button"
    #     profile_button = wait.until(EC.presence_of_element_located((By.XPATH, profile_button_xpath)))
    #     profile_button.click()
    #     print("Already logged in")
    #     return
    # except:
    #     try:
    #         profile_button_selector = "#expand-user-drawer-button"
    #         profile_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, profile_button_selector)))
    #         profile_button.click()
    #         print("Profile button found in second attempt")
    #         return
    #     except:
    #         try:
    #             login_button = wait.until(EC.presence_of_element_located((By.ID, "login-button")))
    #             login_button.click()
    #             time.sleep(3)
    #             print("Login button found by ID")
    #             return
    #         except:
    #             try:
    #                 login_button = wait.until(EC.presence_of_element_located((By.XPATH, login_xpath)))
    #                 login_button.click()
    #                 time.sleep(3)
    #                 print("Login button found by XPATH")
# /htlogin_xpath = ody/shreddit-app/reddit-header-large/reddit-header-action-items/header/nav/div[3]/span[3]/faceplate-tracker
     