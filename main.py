import csv
import time
import os
from email.message import EmailMessage
import smtplib
from datetime import date

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

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
            - Time of the scraping
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
    company_description = soup.find("section", {"id":"about-section"}).text.replace('\n', ' ')
    offer_text = soup.find("section", {"id":"description-section"}).text.replace('\n', ' ')
    # Add profile section if there is one
    if soup.find("section", {"id":"profile-section"}):
        profile_text = offer_text + ' ' + soup.find("section", {"id":"profile-section"}).text.replace('\n', ' ')
    else :
        profile_text = ''

    # Organizing data into a list
    job_data = [date.today(), job_title, contract_type, job_location, salary, start_date, remote_work, education_level, experience_needed,  company_name, sector, n_employees, company_link, offer_link, company_description, offer_text, profile_text]
    # Organizing columns names in a list 
    column_names = ["Date de la collecte","Titre", 'Contrat', 'Localisation', 'Salaire', 'Date de début', 'Télétravail', 'Etudes', 'Expérience', 'Entreprise', 'Domaine', 'Employés', 'Lien_entreprise', 'Lien_offre', "Description_entreprise", 'Offre', "Profil" ]

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
            writer.writerow(columns)
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

def get_dynamic_page_content(target_url: str) -> str:
    """
    Obtient le contenu de la page dynamique en utilisant Selenium et Chrome.

    Args:
        target_url (str): L'URL de la page cible.

    Returns:
    str: Le contenu de la page en tant que chaîne de caractères.
    """
    # Intialize a Chrome object
    driver = webdriver.Chrome(executable_path=r'C:\Users\Tanguy\Desktop\30_Python\Projets_Python\drivers\chromedriver.exe')

    # Accessing the target url
    driver.get("https://www.welcometothejungle.com/fr/jobs?query=d%C3%A9veloppeur%20python")

    # Wait for 5 seconds
    time.sleep(5)

    # Store the content of the webpage
    page_content = driver.page_source

    # Close the web browser and terminates the WebDriver session
    driver.quit()

    return page_content

def get_job_links_list(soup:BeautifulSoup) :
    """
    Extracts the links of the job offers from the HTML content of the Welcome to the Jungle website.
    This function finds the ordered list of job offers on a Welcome to the Jungle search results page and extracts the
    URLs of the job offers from the links in the lines of the list items. The URLs are returned as a list of strings

    Args:
    - soup: A BeautifulSoup object representing the HTML content of a Welcome to the Jungle search results page.

    Returns:
    - A list of strings representing the URLs of the job offers..
    """
    # find the ordered list
    job_list = soup.find('ol', {"id":"job-search-results"})

    # Create an empty list for links
    job_links = []

    # Iterate over the jobs list
    for job in job_list.find_all('li'):
        job_links.append(f"https://www.welcometothejungle.com{job.find('a').get('href')}")

    return job_links   

def scrape_job_offer_data_from_keywords(keywords:str, csv_path:str):
    """
    Extracts data from all the job offers on the job offer first search page with keywords specified.
    Nothing is returned but the data collected is saved to the csv path.

    Args:
    - keywords A string representing the keywords we want to use to get the job offer search results page.
    - csv_path : A string representing the path we want to save the file to.

    Returns:
    - None
    """

    # Get search page dynamic content with selenium
    search_page_content = get_dynamic_page_content(f"https://www.welcometothejungle.com/fr/jobs?query={keywords}&page=1")

    # Initialize a BS object
    soup = BeautifulSoup(search_page_content, "lxml")

    # Get job links from the search page BS object
    job_links = get_job_links_list(soup)

    # Loop over the links to fill the csv
    for i, job_offer in enumerate(job_links):
        print(i, job_offer)
        scrape_data_from_job_offer(job_offer, csv_path)
        time.sleep(1)

    # Get rid of job duplicates

def send_email_with_csv(dest_email: str, csv_path: str, keywords: str) -> None:
    """Sends an email message with a CSV file attachment 
    containing new job offers.

    Args:
        dest_email (str): The email address to send the message to.
        csv_path (str): The file path to the CSV file containing job offer data.
        keywords (str): The search keywords for the new job offers.

    Returns:
        None
    """
    new_entries = get_rid_of_duplicates(csv_path)

    if new_entries > 0 : 
        msg = create_email_message(dest_email, keywords, new_entries)
        msg = attach_csv_file_to_message(msg, csv_path)
        send_email(msg)

def create_email_message(dest_email: str, keywords: str, new_entries:int) -> EmailMessage:
    """Creates an email message object.

    Args:
        dest_email (str): The email address to send the message to.
        keywords (str): The search keywords for the new job offers.

    Returns:
        An EmailMessage object with the specified sender, recipient, subject, and body.
    """

    # Create an instance of EmailMessage
    msg = EmailMessage()

    # Set the headers of the email (sender, recipient, subject)
    msg['From'] = os.environ['EMAIL_USER']
    msg['To'] = dest_email
    msg['Subject'] = f"{keywords} - New job offers available! ({new_entries})"
    # Set the body of the email
    msg.set_content(f"{new_entries} new job offers have appeared for the search '{keywords}'.")
    
    return msg

def attach_csv_file_to_message(msg: EmailMessage, csv_path: str) -> EmailMessage:
    """Reads the contents of a CSV file in binary mode
    and attaches it to an email message.

    Args:
        msg (EmailMessage): The email message object to attach the CSV file to.
        job_offer_data (bytes): The contents of the CSV file.

    Returns:
        None
    """
    
    # Open the CSV file in binary mode and read its contents
    with open(csv_path, 'rb') as f:
        job_offer_data = f.read()

    # Attach the CSV file to the email message
    msg.add_attachment(job_offer_data, maintype='text', subtype='csv', filename="job_offers.csv")

    return msg

def send_email(msg: EmailMessage) -> None:
    """Sends an email message using SMTP.

    Args:
        msg (EmailMessage): The email message object to send.

    Returns:
        None
    """
    
    # Send the email using SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(os.environ["EMAIL_USER"], os.environ["EMAIL_PASSWORD"])
        smtp.send_message(msg)
    
    print("Email was sent successfully !")

def get_rid_of_duplicates(csv_path:str)-> int: 
    """
    This function eliminates duplicatas from the dataset and return the number of real new entries for the current date.

    Args:
        csv_path : The path to the csv file containing job data.

    Returns:
        new_entries : The number of new job offers for the current day.
    """
    df = pd.read_csv(csv_path)
    df = df.drop_duplicates(subset = ["Titre","Contrat","Localisation","Salaire","Date de début","Télétravail","Etudes","Expérience","Entreprise","Domaine","Employés","Offre", "Profil"], keep='first')
    new_entries = df[df["Date de la collecte"] == str(date.today())].shape[0]
    df.to_csv(csv_path, index=False)

    return new_entries

# Parameters
keywords = "Développeur Python"
csv_path = "job_offers.csv"

# scrape_job_offer_data_from_keywords(keywords, csv_path)
send_email_with_csv(os.environ['EMAIL_USER'], csv_path, keywords)



