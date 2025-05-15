Here is your `README.md` file, ready to download and use:

---

### 📄 File Contents: `README.md`

````markdown
# REAL ID Appointment Checker (NJ MVC)

This Python script checks for available REAL ID appointments in New Jersey (via [telegov.njportal.com](https://telegov.njportal.com)) and sends an email alert if appointments are found within the specified date range.

## 🔧 Features

- Checks appointments for up to 30 days ahead
- Scans specific DMV location pages
- Sends email alerts when appointments are available
- Headless Chrome via Selenium
- Can run locally with scheduled interval (default: every 30 minutes)

## 🖥 Requirements

- Python 3.8+
- Chrome installed
- [ChromeDriver](https://chromedriver.chromium.org/downloads) matching your Chrome version
- Gmail account with App Password (for secure email alerts)

### ⚙️ Setting Up ChromeDriver

Make sure `chromedriver` is installed and matches your local Chrome version:

- [Download ChromeDriver](https://chromedriver.chromium.org/downloads)
- Place it in the project folder **or** in your system PATH
- Make it executable (on macOS/Linux):

```bash
chmod +x chromedriver


## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/smenon2710/real_id_appointment_checker.git
cd real_id_appointment_checker
````

### 2. Install Dependencies

Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

Install required packages:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
touch .env
```

Add the following lines and fill in your values:

```env
EMAIL_SENDER=your_email@gmail.com
EMAIL_RECEIVER=your_email@gmail.com
EMAIL_PASSWORD=your_app_specific_password
```

> Never commit this file to GitHub. It's listed in `.gitignore`.

### 4. Run the Script

```bash
python real_id_checker.py
```

It will check every 30 minutes for appointment availability.

---

## 🔐 Security Notes

* Uses `.env` to manage secrets (Gmail app password)
* `.env` is excluded from Git using `.gitignore`
* Never hardcode credentials in Python files

---

## ✅ License

MIT License

```

---

