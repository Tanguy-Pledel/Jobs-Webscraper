import requests
from bs4 import BeautifulSoup

# Type GET request
r = requests.get('https://www.welcometothejungle.com/fr/companies/datascientest/jobs/developpeur-python-h-f_puteaux?q=d3210e5fd6fc0fca57024e5ac29d0164&o=1647471')

# Storing the content of the response
webpage_html = r.text

# Initialize a BS object
soup = BeautifulSoup(webpage_html, "lxml")

### Accessing different elements on the page

# Contract type
print("Type de contrat :", soup.find('i', {"name":"contract"}).parent.parent.text)

# Location
print("Job Location:", soup.find('i', {"name":"location"}).parent.parent.text)

# Education level
print("Education Level:", soup.find('i', {"name":"education_level"}).parent.parent.text)

# Remote work
print("Remote possibility:", soup.find('i', {"name":"remote"}).parent.parent.text)

# Experience
print("Experience needed:", soup.find('i', {"name":"suitcase"}).parent.parent.text)

# Sector
print("Domaine:", soup.find('i', {"name":"tag"}).parent.parent.text)

# Number of collaborators
print("Collaborators:", soup.find('i', {"name":"department"}).parent.parent.text)

# Company name
print("\nCompagny Name:", soup.find('h3', {'data-testid':'job-header-organization-title'}).text)

# Company link
print("Company Link :", soup.find('a', {"data-testid":"job-header-organization-link-logo"}).get('href'))

# Job offer text
print(soup.find("section", {"id":"about-section"}).text)
