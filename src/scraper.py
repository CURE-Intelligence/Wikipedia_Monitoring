from typing import Tuple
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
import re


def scrape_wikipedia(url: str) -> Tuple[str, str]:
    """Scrape content and last update from Wikipedia page."""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    content = soup.find('div', {'id' : 'mw-content-text'})
    paragraphs = content.find_all('p')
    # Content which is modified
    main_text = '\n\n'.join(paragraph.get_text() for paragraph in paragraphs)
    
    # Date which is modified
    last_modified_date = soup.find('li', {'id' : 'footer-info-lastmod'})
    update = last_modified_date.get_text()
    
    return main_text, update


def get_update_as_date(update_text: str, language: str = "german") -> date:
    
    if language == "german":
        update_text = update_text.replace(" Diese Seite wurde zuletzt am ", "") \
            .replace(" Uhr bearbeitet.", "") \
            .replace(".", "")
    
        # Getting only the first part of the sentence, separated by um, which represents Day Month Year
        update_text = re.split(" um ", update_text)[0]
    
        # German month translations
        german_months = {
            "Januar": "January", "Februar": "February", "März": "March",
            "Mai": "May", "Juni": "June", "Juli": "July",
            "Oktober": "October", "Dezember": "December"
        }
        
        for german_month, english_month in german_months.items():
            if german_month in update_text:
                update_text = update_text.replace(german_month, english_month)
    
    else:
        update_text = update_text.replace(" This page was last edited on ", "") \
        .replace("\xa0(UTC)", "") \
        .replace(".", "")
        update_text = re.split(", at ", update_text)[0]
        
        
    # Get the updated date in the prefered format 
    updated_date = datetime.strptime(update_text, "%d %B %Y")
    
    # Get the updated date like datetime.date(2024, 12, 17)
    return updated_date.date()
    