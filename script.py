import openpyxl
import smtplib
import time
from twilio.rest import Client
from calendly import CalendlyAPI

# Replace with your Twilio account SID and auth token
TWILIO_ACCOUNT_SID = 'YOUR_TWILIO_ACCOUNT_SID'
TWILIO_AUTH_TOKEN = 'YOUR_TWILIO_AUTH_TOKEN'
TWILIO_PHONE_NUMBER = 'YOUR_TWILIO_PHONE_NUMBER'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:YOUR_TWILIO_WHATSAPP_NUMBER'

# Replace with your Calendly API key
CALENDLY_API_KEY = 'YOUR_CALENDLY_API_KEY'

# Initialize the Calendly API client
calendly = CalendlyAPI(CALENDLY_API_KEY)

# Load the Excel file
workbook = openpyxl.load_workbook('data.xlsx')
sheet = workbook.active

# Iterate through each row in the Excel sheet
for row in range(2, sheet.max_row + 1):
    company_name = sheet.cell(row=row, column=1).value
    calendly_link = sheet.cell(row=row, column=2).value
    interviewee_email = sheet.cell(row=row, column=3).value
    interviewee_phone = sheet.cell(row=row, column=4).value

    # Send the Calendly link to the interviewee
    send_calendly_link(interviewee_email, interviewee_phone, company_name, calendly_link)

    # Check if the interviewee scheduled a meeting
    if check_scheduled_meeting(interviewee_email, interviewee_phone, company_name, calendly_link):
        print(f"Interviewee {interviewee_email}/{interviewee_phone} scheduled a meeting for {company_name}")
    else:
        # Send follow-up communications
        follow_up(interviewee_email, interviewee_phone, company_name, calendly_link)

        # Manual intervention if needed
        manual_intervention(interviewee_email, interviewee_phone, company_name)

# Function to send the Calendly link to the interviewee
def send_calendly_link(email, phone, company_name, calendly_link):
    message = f"Hello, please use the following Calendly link to schedule an interview with {company_name}:\n{calendly_link}"

    try:
        send_whatsapp(phone, message)
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        try:
            make_call(phone, message)
        except Exception as e:
            print(f"Error making call: {e}")
            send_email(email, message)

# Function to check if the interviewee scheduled a meeting
def check_scheduled_meeting(email, phone, company_name, calendly_link):
    # Extract the Calendly event ID from the link
    event_id = calendly_link.split('/')[-1]

    # Query the Calendly API for scheduled events
    scheduled_events = calendly.scheduled_events.list(event_id=event_id)

    # Check if any scheduled events match the interviewee's email or phone number
    for event in scheduled_events:
        if event.invitee_email == email or event.invitee_phone_number == phone:
            return True

    return False

# Function to send follow-up communications
def follow_up(email, phone, company_name, calendly_link):
    message = f"This is a friendly reminder to schedule an interview with {company_name} using the following Calendly link:\n{calendly_link}"

    try:
        send_whatsapp(phone, message)
        send_email(email, message)
    except Exception as e:
        print(f"Error sending follow-up communication: {e}")

    time.sleep(10800)  # Wait for 3 hours

    if not check_scheduled_meeting(email, phone, company_name, calendly_link):
        print(f"Interviewee {email}/{phone} did not schedule a meeting for {company_name}. Escalating to manual intervention.")
        manual_intervention(email, phone, company_name)

# Function for manual intervention
def manual_intervention(email, phone, company_name):
    print(f"Manual intervention required for interviewee {email}/{phone} for {company_name}")
    # Your code for manual intervention (e.g., assigning the case to a team member)

# Function to send an email
def send_email(recipient, message):
    # Replace with your email credentials
    sender_email = "YOUR_EMAIL_ADDRESS"
    sender_password = "YOUR_EMAIL_PASSWORD"

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, message)
        print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()

# Function to make a call
def make_call(phone_number, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        call = client.calls.create(
            twiml=f'<Response><Say>{message}</Say></Response>',
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER
        )
        print(f"Call made to {phone_number}")
    except Exception as e:
        print(f"Error making call: {e}")

# Function to send a WhatsApp message
def send_whatsapp(phone_number, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        message = client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f"whatsapp:{phone_number}"
        )
        print(f"WhatsApp message sent to {phone_number}")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")