# Jobs Webscraper

## Description

This project provides a script for scraping job offers from the "Welcome to the Jungle" website based on specific search keywords. The scraped data is saved to a CSV file and can be sent via email as an attachment.

This project has been created along with the french titkok video series "30 jours pour apprendre à programmer en Python" on my tiktok account "Tanguy Pledel" : https://www.tiktok.com/@tanguy_pledel

## Installation

1. Clone the repository: `git clone https://github.com/Tanguy-Pledel/Jobs-Webscraper.git`
2. Navigate to the project directory: `cd project-directory`
3. Install the required dependencies: `pip install -r requirements.txt`

## Usage

1. Open the terminal and navigate to the project directory.
2. Run the script with the following command:
`python main.py "keywords"` (replace "keywords" with your desired search keywords)
3. The script will scrape job offers based on the specified keywords, save the data to a CSV file, and send an email with the CSV file attached.

## Configuration

Before running the script, make sure to configure the following:

1. Email configuration:
- Set the `EMAIL_USER` and `EMAIL_PASSWORD` environment variables to your email credentials.
- Update the `dest_email` parameter in the `send_email_with_csv` function to the recipient's email address.

2. Chrome driver path:
- Update the `executable_path` parameter in the `get_dynamic_page_content` function with the path to your Chrome driver executable.

## License

This project is licensed under the [MIT License](LICENSE).
