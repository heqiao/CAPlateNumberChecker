# CA Plate Number Checker
A script for checking the availability of CA special interest license plate number

## Requirements
* python 3+
* [selenium](https://pypi.org/project/selenium/)
* [webdriver-manager](https://pypi.org/project/webdriver-manager/)

## How to use
1. Edit `plate_numbers.txt`. Put the numbers you want to check into the file.
2. Edit `ca_plate_number_checker.py`. Modify CHROME_WEBDRIVER_PATH to your ChromeDriver path. Modify CURRENT_PLATE and VIN with your own, the website will validate the eligibility. 
3. Run the script.

## Notes
This fork of the code can be fragile as a lot of `xpath`s are being used. Tweak the selectors as needed if any of them is not found due to the DMV website updates.
