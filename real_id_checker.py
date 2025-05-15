from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import time
import schedule
import re
import os

EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"


# === CONFIG ===
# EMAIL_RECEIVER = "smenon2710@gmail.com"
# EMAIL_SENDER = "smenon2710@gmail.com"
# EMAIL_PASSWORD = "yhuj hiur bqfn rtcq"  # Use your Gmail App Password
# CHROMEDRIVER_PATH = "/Users/sujithkumarmenon/Documents/AGS_Purdue/real_id_appointment_checker/chromedriver"

URLS = [
    "https://telegov.njportal.com/njmvc/AppointmentWizard/12",
    "https://telegov.njportal.com/njmvc/AppointmentWizard/289"
]

def get_next_30_days():
    return [(datetime.today() + timedelta(days=i)).date() for i in range(30)]

def send_email(message):
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = "🚨 REAL ID Location Appointment Found!"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

def check_location_pages():
    start_date = datetime.today().date()
    end_date = (datetime.today() + timedelta(days=29)).date()
    print(f"[🔍] Scanning appointments between {start_date} and {end_date}...")
    print(f"[🕒] Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium-browser"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    found = []

    try:
        for url in URLS:
            driver.get(url)
            time.sleep(5)

            cards = driver.find_elements("xpath", "//div[contains(@class, 'card')]")
            for card in cards:
                lines = card.text.splitlines()
                match = re.search(r"Next Available:\s*(\d{2}/\d{2}/\d{4})\s*(\d{1,2}:\d{2} [AP]M)?", card.text)
                if match:
                    appt_date = datetime.strptime(match.group(1), "%m/%d/%Y").date()
                    appt_time = match.group(2) or "Unknown time"

                    if start_date <= appt_date <= end_date:
                        location_name = lines[0] if len(lines) > 0 else "Unknown Location"
                        address_lines = "\n".join(lines[1:4]) if len(lines) >= 4 else "Unknown Address"
                        found.append(
                            f"📍 {location_name}\n"
                            f"📅 Next Available: {match.group(1)} at {appt_time}\n"
                            f"📌 Location: {address_lines}\n"
                            f"🔗 {url}\n"
                        )
    finally:
        driver.quit()

    if found:
        message = (
            f"✅ Appointments found between {start_date} and {end_date}:\n\n" +
            "\n\n".join(found)
        )
        send_email(message)
        print("✅ Appointments found! Email sent.")
    else:
        print("❌ No upcoming appointments found.")



# Run every 30 minutes
schedule.every(15).minutes.do(check_location_pages)

if __name__ == "__main__":
    check_location_pages()
    while True:
        schedule.run_pending()
        time.sleep(1)
