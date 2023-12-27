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

import variables

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

    auction_time_left_str = bot.find_element("//div[contains(@class, 'info-aside')]//span[@id='time-left']", By.XPATH).text

    auction_time_left_int = int(''.join(filter(str.isdigit, auction_time_left_str)))

    place_bid_field = bot.find_element("//div[contains(@class, 'info-aside')]//input[@id='ending-soonest-bid']", By.XPATH)
    place_bid_field.send_keys("500")

    quick_bid_btn = bot.find_element("//div[contains(@class, 'info-aside')]//a[@id='auctionQuickBid']", By.XPATH)
    quick_bid_btn.click()

    while auction_time_left_int > 1:
        auction_time_left_str = bot.find_element("//div[contains(@class, 'info-aside')]//span[@id='time-left']", By.XPATH).text

        auction_time_left_int = int(''.join(filter(str.isdigit, auction_time_left_str)))
    place_bid_btn = bot.find_element("//div[contains(@class, 'modal')]//button[@id='bidPlaced-btn']", By.XPATH)
    place_bid_btn.click()

    #bot.wait(3000)

    try: 
        success_title = bot.find_element("//div[contains(@class, 'modal')]//h4[@id='success-title']", By.XPATH)

        bot.wait_for_element_visibility(element=success_title, visible=True, waiting_time=10000)

        success_title = success_title.text

        print(success_title)

        if success_title == "Score! You Won the Auction!":
            print("Parabéns! Você ganhou o leilão!")
        else:
            print("Você perdeu o leilão!")

        auction_price = bot.find_element("//div[contains(@class, 'modal')]//h3[@id='accuracy']", By.XPATH).text
        print(f"O valor do leilão vencedor foi {auction_price}.")
        bid_time = bot.find_element("//div[contains(@class, 'modal')]//h4[@id='processing-time']", By.XPATH).text
        print(bid_time)
    
    except Exception as e:
        print(e)

    # Wait 3 seconds before closing
    bot.wait(3000)

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
