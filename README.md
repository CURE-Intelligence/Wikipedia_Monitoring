# Wikipedia Content Monitoring

This repository provides a mechanism to track recent changes in specific Wikipedia pages over the last 5 days. It compares the current Wikipedia content against locally stored text files, identifies changes, and notifies a marketing team via email about the update status.

## Overview

The project focuses on three primary objectives:

1. **Monitoring Recent Changes:**  
   We periodically check if the content on certain Wikipedia pages has been edited within the last 5 days.

2. **Content Comparison:**  
   We compare the latest scraped content against previously stored text files on our local server to determine if there have been any differences.

3. **Email Notifications:**  
   Regardless of whether changes are detected, an email is sent to notify the team. This includes the status update and relevant details of any modifications.

## How It Works

1. **Projects and Pages:**  
   Specific Wikipedia pages (the "projects") are defined in [`src/pages.py`](src/pages.py). Each project has a name and a corresponding Wikipedia URL. Currently, we are dealing with local copies of these pages to streamline development and testing.

2. **Scraping Content:**  
   The scraping logic resides in [`src/scraper.py`](src/scraper.py). It extracts the textual content and editing dates from the specified Wikipedia pages.

3. **Comparison Logic:**  
   The main workflow is outlined in [`src/monitoring.py`](src/monitoring.py). Here, we:

   - Fetch the latest editing dates from Wikipedia.
   - Compare these dates with the last-known check (previous snapshots stored locally).
   - Determine if changes occurred in the last 5 days.

   If changes are detected, functions in [`src/text_comparison.py`](src/text_comparison.py) are utilized to identify differences in content.

   **Note:** We always overwrite the local text files with the newest content, ensuring that subsequent checks use the most recent baseline.

4. **Status Tracking:**  
   After each monitoring cycle, a "Last Check" status file is updated, indicating whether or not content changes occurred. This helps keep everyone informed about the current state of the monitored pages.

5. **Email Notification:**  
   Email sending logic is defined in [`src/email_sender.py`](src/email_sender.py), with credentials managed in the `.env` file. The email's subject and body are constructed in [`src/monitoring/prepare_notification.py`](src/monitoring/prepare_notification.py). Emails are sent out to marketing colleagues regardless of whether changes were detected, ensuring a steady communication channel.

## Directory Structure Example

A real-world example of this setup and the local file structure can be seen at:

V:\CURE\Operations\Clients\DZ Privatbank\Wikipedia Monitoring\Page Checks

Here, you'll find the text files representing the local snapshots, the "Last Check" file, and logs for reference.

## Getting Started

### Prerequisites

- Python 3.10.11 (or compatible version)
- A valid `.env` file with email credentials (see `src/email_sender.py` for details)

### Installation Steps

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>

   ```

2. **Select the python version (I worked with 3.10.11):**

   ```bash
   pyenv local 3.10.11

   ```

3. **Create a python virtual environment**

   ```bash
   python -m venv venv

   ```

4. **Create a python virtual environment**

   ```bash
   .\venv\Scripts\activate

   ```

5. **Install the dependencies**

   ```bash
   pip install -r requirements.txt

   ```

6. **Install the modules as packages**

   ```bash
   pip install .

   ```

7. **Go to the directory**

   ```bash
   cd src

   ```

8. **Execute the script**
   ```bash
   python monitoring.py
   ```
