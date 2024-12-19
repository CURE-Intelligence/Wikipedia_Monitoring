# Importing modules we have defined

from pages import WIKI_PAGES
from scraper import scrape_wikipedia, get_update_as_date
from text_comparison import compare_texts_similarity
from email_sender import send_email
from config import load_env


from datetime import date, datetime, timedelta
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

def get_last_checked_date(base_path: str)-> date:
    
    """Get the last check date from file or create new one."""
    today = date.today()
    last_check_file = os.path.join(base_path, "Last_Check.txt")
    
    # Check if the path of the file exists; if not then append the current date as the last check
    if not os.path.exists(last_check_file):
        last_check = today
        with open(last_check_file, "w", encoding='utf-8') as f:
            f.write(str(today))
    else:
        with open(last_check_file, "r", encoding='utf-8') as f:
            last_check = datetime.strptime(
                f.readline().strip(), '%Y-%m-%d').date()
        with open(last_check_file, "w") as f:
            f.write(str(today))
            
    return last_check

def process_page_changes(name: str, url: str, last_check: date, base_path: str) -> List[str]:
    """Process a single Wikipedia page and return list of content changes."""
    # Then we will generalize this for all the wikipedia pages we currently have
    changes = []
    content, update_text = scrape_wikipedia(url)
    update_date = get_update_as_date(update_text)
    content_changed = False
    
    # Condition is if there are changes at the last 5 days
    if update_date >= last_check :
        page_file = os.path.join(base_path, f"{name}.txt")
        
        
        with open(page_file, "r", encoding='utf-8') as f:
            old_content = f.read()
            
            # Compares texts between the old content (txt file) and the content scraped from the web
            if compare_texts_similarity(content, old_content):
                # Save the new content to file
                with open(page_file, "w", encoding='utf-8') as f:
                    f.write(content)
                content_changed = True
    
    return content_changed
            
            
def check_wikipedia_changes(base_path: str) -> Dict[str, str]:
    """Main function to detect changes across Wikipedia pages."""
    last_check = get_last_checked_date(base_path)
    changed_results = {}
    
    # iterate each project
    for name, url in WIKI_PAGES.items():
        changed = process_page_changes(name, url, last_check, base_path)
        changed_results[name] = changed
        
        # Log changes to file (For each file name will write if there are Changes detected or not)
        with open(os.path.join(base_path, "Last_Check.txt"), "a", encoding='utf-8') as f:
            if changed:
                f.write(f"\n\n{name}\nCHANGES DETECTED")
            else:
                f.write(f"\n\n{name}\nNO CHANGES")
    
    return changed_results

def prepare_notification(changed_results: Dict[str, str]) -> Dict[str, str]:
    """Prepare email notification based on change results."""
    # Determine if any documents changed (Returns true if at least 1 item is True)
    any_content_changed = any(changed_results.values())
    
    # Create a detailed body message
    if any_content_changed:
        # Find documents with changes
        changed_docs = [name for name, changed in changed_results.items() if changed]
        
        subject = "Wikipedia Pages Content Changes Detected"
        body = "This is an automated e-mail sent by a script programmed by Joscha Krause."
        body += "The following documents have been updated and need your review:\n\n"
        body += "\n".join(f"- {doc}" for doc in changed_docs)
        body += "\n\nPlease check the detailed changes in the respective files."
    else:
        subject = "Wikipedia Pages Check Complete - No Changes"
        body = "This is an automated e-mail sent by a script programmed by Joscha Krause."
        body += "No changes were detected in any of the monitored Wikipedia pages."
    
    return subject, body


def main():

     # True if we want to run it locally, False if we want to run it via Jenkins
    LOCAL_EXEC = False
    
    # Separately define the base path for clarify
    PATH = load_env(LOCAL_EXEC)
    
    # Define the credentials for connecting to the email server
    credentials = {
        # We will get 2 times the SMTP_USERNAME JUST FOR PURPOSE OF CLARITY
        "FROM_EMAIL" : os.getenv('SMTP_USERNAME'),
        "SMTP_SERVER" : os.getenv('SMTP_SERVER'),
        "SMTP_PORT" : os.getenv('SMTP_PORT'),
        "SMTP_USERNAME" : os.getenv('SMTP_USERNAME'),
        "SMTP_PASSWORD" : os.getenv('SMTP_PASSWORD'),
        "TO_TECH_EMAIL" : os.getenv("TO_TECH_EMAIL"),
        "TO_USER_EMAIL" : os.getenv("TO_USER_EMAIL")
    }
    
    #print(credentials['SMTP_PORT'])
    
    # Get the changed results
    changed_results = check_wikipedia_changes(PATH)
    
    # Prepare the email even in case there is not any change
    subject, body = prepare_notification(changed_results)
    
    #print(subject, body)
    
    # Send the email
    send_email(subject, body, credentials)
    
    
    
if __name__ == "__main__":
    main()
    
    
    
    
    
