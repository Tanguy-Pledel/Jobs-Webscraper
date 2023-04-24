import csv

import requests
from bs4 import BeautifulSoup

def get_webpage_html(url:str)-> str:
    """
    Sends an HTTP GET request to the specified URL,
    retrieves the text content of the response, 
    and returns it as a string.

    Args:
        url (str): The URL to send the request to

    Returns:
        str: The text content of the HTTP response
    """


    # Type GET request
    response = requests.get(url)
    # Accessing the content of the response
    webpage_html = response.text
    
    return webpage_html

def get_info_via_icon(soup:BeautifulSoup ,icon_name:str)-> str:
    """
    Extracts information from an HTML document represented
    by the `soup` object, based on the name of an icon
    passed as `icon_name`. Searches for an HTML element
    of the "i" tag type, whose "name" attribute matches
    `icon_name`, and retrieves the text of the parent of
    the parent element of this "i" tag, which presumably
    contains the information associated with the icon.

    Args:
    soup (BeautifulSoup): A BeautifulSoup object representing an HTML document
    icon_name (str): The name of the icon to search for

    Returns:
    str: The information associated with the icon, or an empty string if it cannot be found
    """

    try :
        info = soup.find('i', {"name":icon_name}).parent.parent.text
    except AttributeError:
        info = ''

    return info

def get_info_from_offer(soup, offer_link)-> list:
    """
    Extracts job information from a Beautiful Soup object 
    created from a job offer HTML code.

    Args:
        soup (BeautifulSoup): A Beautiful Soup object created from the HTML code of a job offer page.
        offer_link (str): The URL of the job offer page.

    Returns:
        A tuple containing:
        - A list of job information extracted from the
          offer page. The list contains the following 
          elements in order:
            - Job title
            - Contract type
            - Job location
            - Salary
            - Start date
            - Remote work availability
            - Required education level
            - Required experience
            - Company name
            - Industry sector
            - Number of employees
            - Link to the company page
            - Link to the job offer page
            - Job offer description text
        - A list of column names corresponding to the
          job information extracted.

    """
	
    ### Accessing different elements on the page
    job_title = soup.find('h1').text
    contract_type = get_info_via_icon(soup, 'contract')
    job_location = get_info_via_icon(soup, 'location')
    salary = get_info_via_icon(soup, 'salary')
    start_date = get_info_via_icon(soup, 'clock')
    remote_work = get_info_via_icon(soup, 'remote')
    education_level = get_info_via_icon(soup, 'education_level')
    experience_needed = get_info_via_icon(soup, 'suitcase')
    sector = get_info_via_icon(soup, 'tag')
    n_employees = get_info_via_icon(soup, 'department')
    company_name = soup.find('h3', {'data-testid':'job-header-organization-title'}).text
    company_link = "https://www.welcometothejungle.com" + soup.find('a', {"data-testid":"job-header-organization-link-logo"}).get('href')
    offer_text = soup.find("section", {"id":"about-section"}).text.replace('\n', ' ')

    # Organizing data into a list
    job_data = [job_title, contract_type, job_location, salary, start_date, remote_work, education_level, experience_needed,  company_name, sector, n_employees, company_link, offer_link, offer_text]
    # Organizing columns names in a list 
    column_names = ["Titre", 'Contrat', 'Localisation', 'Salaire', 'Date de début' 'Télétravail', 'Etudes', 'Expérience', 'Entreprise', 'Domaine', 'Employés', 'Lien_entreprise', 'Lien_offre', 'Offre' ]

    return job_data, column_names

def add_line_to_csv(new_line:list, columns:list, csv_path:str):
    """
    Writes a new line in CSV format to the specified 
    file path.

    Args:
    new_line (list): A list of values to add as a new row in the CSV file.
    columns (list): A list of column names for the CSV file.
    csv_path (str): The file path of the CSV file to write to.

    Raises:
    FileNotFoundError: If the specified file path does not exist.

    If the CSV file does not exist, this function will 
    create it and write the column names before adding 
    the new line. If the CSV file already exists, this
    function will append the new line to the end of the
    file.

    Returns:
    None.
    """

    # Opening a file
    with open(csv_path, 'a', encoding='utf-8', newline='') as csv_file:
        # Create a writer object
        writer = csv.writer(csv_file)
        # Add a line with columns 
        if csv_file.tell() == 0:
            writer.writerow(column_names)
        # Add data for the offer
        writer.writerow(new_line)

        # Close automatically the file

def scrape_data_from_job_offer(offer_link:str, job_offers_csv_path:str):
    """
    Scrapes information from a job offer webpage and 
    saves it to a CSV file.

    Args:
    offer_link (str): The URL of the job offer webpage to scrape.
    job_offers_csv_path (str) : The path of the CSV file to save the job offer information to.

    Returns:
    None
    """
    # Get the HTML code of the webpage
    webpage_html = get_webpage_html(offer_link)
    # Initialize a BS object
    soup = BeautifulSoup(webpage_html, "lxml")
    # Getting info from job offer
    job_data, column_names = get_info_from_offer(soup, offer_link)
    # Save results to csv
    add_line_to_csv(job_data, column_names, job_offers_csv_path)


job_offer_list =["https://www.welcometothejungle.com/fr/companies/nickel/jobs/developpeur-web-python-f-h-python-sur-google-cloud_charenton-le-pont?q=740dab72640f27ab2c29b35b4b850858&o=1792771",
"https://www.welcometothejungle.com/fr/companies/ratp-smart-systems/jobs/developpeur-map-f-h_paris?q=740dab72640f27ab2c29b35b4b850858&o=1643270",
"https://www.welcometothejungle.com/fr/companies/helloasso/jobs/lead-developpeur-euse-python_begles?q=740dab72640f27ab2c29b35b4b850858&o=1470841"]

for offer_link in job_offer_list:
    scrape_data_from_job_offer(offer_link, 'job_offers.csv')
