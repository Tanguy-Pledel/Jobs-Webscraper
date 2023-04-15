import csv

import requests
from bs4 import BeautifulSoup

# Parameters
offer_link = 'https://www.welcometothejungle.com/fr/companies/datascientest/jobs/developpeur-python-h-f_puteaux?q=d3210e5fd6fc0fca57024e5ac29d0164&o=1647471'

# Type GET request
r = requests.get(offer_link)
# Storing the content of the response
webpage_html = r.text

# Initialize a BS object
soup = BeautifulSoup(webpage_html, "lxml")

### Accessing different elements on the page
job_title = soup.find('h1').text
contract_type = soup.find('i', {"name":"contract"}).parent.parent.text
job_location = soup.find('i', {"name":"location"}).parent.parent.text
remote_work = soup.find('i', {"name":"remote"}).parent.parent.text
education_level = soup.find('i', {"name":"education_level"}).parent.parent.text
experience_needed = soup.find('i', {"name":"suitcase"}).parent.parent.text
sector = soup.find('i', {"name":"tag"}).parent.parent.text
n_employees = soup.find('i', {"name":"department"}).parent.parent.text
company_name = soup.find('h3', {'data-testid':'job-header-organization-title'}).text
company_link = "https://www.welcometothejungle.com" + soup.find('a', {"data-testid":"job-header-organization-link-logo"}).get('href')
offer_text = soup.find("section", {"id":"about-section"}).text.replace('\n', ' ')

# Organizing columns names in a list 
column_names = ["Titre", 'Contrat', 'Localisation', 'Télétravail', 'Etudes', 'Expérience', 'Entreprise', 'Domaine', 'Employés', 'Lien_entreprise', 'Lien_offre', 'Offre' ]
# Organizing variables in a list
job_data = [job_title, contract_type, job_location, remote_work, education_level, experience_needed,  company_name, sector, n_employees, company_link, offer_link, offer_text]

# Opening a file
with open('job_offers.csv', 'a', encoding='utf-8', newline='') as csv_file:
    # Create a writer object
    writer = csv.writer(csv_file)
    # Add a line with columns 
    if csv_file.tell() == 0:
        writer.writerow(column_names)
    # Add data for the offer
    writer.writerow(job_data)

    # Close automatically the file