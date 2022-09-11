# Description
This script is a test/fun project, which automates writing work hours into a certain web application. It reads data from a JSON file and posts it into the web application using Selenium.

Unfortunately, due to it connecting to a live server, timings/delays of loaded elements can lead to web elements not being found, breaking the script. Therefore, in the current state the script lacks robustness and the ability to recover itself. Also, because of simple `time.sleep(x)` lines (instead of properly checking for the availability/state of the next needed element) the script works rather slowly. Additionally it is recommended to not move the mouse during the execution, because it might break Selenium/focus of the web elements.

# Setup
A step-by-step guide can be found either in the [official documentation](https://www.selenium.dev/documentation/) as well as in [another documentation](https://selenium-python.readthedocs.io/index.html).

After installing selenium with `pip install selenium` [install a browser driver](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/#tabs-2-1) e.g. Firefox's [geckodriver](https://github.com/mozilla/geckodriver/releases) and set the path to it inside `main.py`.

# JSON data format
```json
url:
name:
week:
{
    days:
    [
        {
            date_day:
            start_time:
            end_time:
            break_duration:
            mode:
            blocks:
            [ 
                {
                    project_name:
                    activity:
                    duration:
                }
            ]
        }
    ]
}
```