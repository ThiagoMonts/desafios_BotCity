"""
WARNING:

Please make sure you install the bot with `pip install -e .` in order to get all the dependencies
on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the bot.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install --upgrade -r requirements.txt`
- Use the same interpreter as the one used to install the bot (`pip install --upgrade -r requirements.txt`)

Please refer to the documentation for more information at https://documentation.botcity.dev/
"""


# Import for the Web Bot
from botcity.web import WebBot, Browser, By

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

import pandas

import variables
import os

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()

    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to change the default Browser to Firefox
    bot.browser = Browser.EDGE

    # Uncomment to set the WebDriver path
    # bot.driver_path = "<path to your WebDriver binary>"

    # Opens the BotCity website.
    bot.browse(variables.url)
    
    if not os.path.exists(r"C:\Users\thiago.honorato\Documents\desafios_BotCity\Desafios\Desafio 04 - Customer Onboarding - Front Office\customer-onboarding-challenge.csv"):
        if not bot.find( "download_button", matching=0.97, waiting_time=10000):
            not_found("download_button")
        bot.click()
        
    else:
        pass

    dados = pandas.read_csv(r"C:\Users\thiago.honorato\Documents\desafios_BotCity\Desafios\Desafio 04 - Customer Onboarding - Front Office\customer-onboarding-challenge.csv", sep=",")

    for index, row in dados.iterrows():
        customer_name_field = bot.find_element("//div[contains(@class, 'form-group')]//input[@id='customerName']", By.XPATH)
        customer_name_field.send_keys(row["Company Name"])


        customer_id_field = bot.find_element("//div[contains(@class, 'form-group')]//input[@id='customerID']", By.XPATH)
        customer_id_field.send_keys(row["Customer ID"])


        primary_contact_field = bot.find_element("//div[contains(@class, 'form-group')]//input[@id='primaryContact']", By.XPATH)
        primary_contact_field.send_keys(row["Primary Contact"])


        street_address_field = bot.find_element("//div[contains(@class, 'form-group')]//input[@id='street']", By.XPATH)
        street_address_field.send_keys(row["Street Address"])     


        city_field = bot.find_element("//div[contains(@class, 'form-row')]//input[@id='city']", By.XPATH)
        city_field.send_keys(row["City"])


        state_field_option = bot.find_element(f"//div[contains(@class, 'form-group')]//select[@id='state']//option [@value='{row['State']}']", By.XPATH)
        state_field_option.click()


        zip_field = bot.find_element("//div[contains(@class, 'form-row')]//input[@id='zip']", By.XPATH)
        zip_field.send_keys(row["Zip"])


        email_field = bot.find_element("//div[contains(@class, 'form-group')]//input[@id='email']", By.XPATH)
        email_field.send_keys(row["Email Address"])


        offers_discount = row["Offers Discounts"]
        if offers_discount == "YES":
            offers_discount_field = bot.find_element("//div[contains(@class, 'form-check')]//input[@id='activeDiscountYes']", By.XPATH)
            offers_discount_field.click()
        else:
            offers_discount_field = bot.find_element("//div[contains(@class, 'form-check')]//input[@id='activeDiscountNo']", By.XPATH)
            offers_discount_field.click()
        

        non_disclosure = row["Non-Disclosure On File"]
        non_disclosure_field = bot.find_element("//div[contains(@class, 'form-group')]//input[@id='NDA']", By.XPATH)
        
        if non_disclosure == "YES":
            non_disclosure_field.click()
        else:
            if non_disclosure_field.is_selected():
                non_disclosure_field.click()



        submit_btn = bot.find_element("//div[contains(@class, 'form-group')]//button[@id='submit_button']", By.XPATH)
        submit_btn.click()


    # Wait 3 seconds before closing
    bot.wait(1000)

    # Finish and clean up the Web Browser
    # You MUST invoke the stop_browser to avoid
    # leaving instances of the webdriver open
    bot.stop_browser()

    # Uncomment to mark this task as finished on BotMaestro
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="Task Finished OK."
    # )


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
