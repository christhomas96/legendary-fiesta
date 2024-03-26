# legendary-fiesta
Automate candidate reach out

Okay so this is how I’m planning to automate this.

Why automation when you have interns?
Because interns might mess up and we cannot mess up. So we make things easier for them by automating boring tasks.

How to make it easier?
By using a python script which will take an excel sheet with the data (which you’ve given as an example) and run it through the script.

What does the script do?
Under the assumption that we have a twilio account, we use this script to take in the interviewee details and this will be the prioritisation to contact: Whatsapp, call, email. Whatsapp has seen a higher interaction rate than any other forms of reaching out to people, and since we are talking about people in tech, they do love messages more than calls and emails.
Now here, we also are assuming that the companies have provided read only API access to calendly, we’ll be using this to check the booked slots on each of the links provided by the company. We need to store the API keys in another file, which will be connected to the application. Api doc link: https://developer.calendly.com/api-docs/decca36cf717f-invitee

Validation, checks, follow ups: We run a check whether the slot has been booked or not- for each message sent (over any form of communication), we run a check after 2 hours if the link was accessed and was booked using the above calendly API. If not, we send another communication, now over two different modes (let’s say email and whatsapp). This time the check happens after 3 hours. If not then, this is where Ram and Shyam come into the picture, and they’ll manually call them and schedule, the only ToDo they need to do is to manually call these candidates (of which a list will be provided by the script we are writing) every 5 hours, and setup a call for them.

Here we are making sure most of the cases are automated, and the interns only jobs would be to do the manual work whenever needed (Which could be close to 10-15%, again an assumption)

Now lets talk about the edge cases:
        I’ve used calendly, and I might end up scheduling multiple meetings (could be because of a network error, or anything tbh), there needs to be a check for this and it’ll need human intervention to understand the right time. In the future also can automate this.
        Time zone difference: Candidate is in India, company is someplace else, here I’ll need to handle the code for reminders.
        Calendly link expiration: Some of the calendly links have expiration set, we need to check that too

Assumptions made:
        Given sheet has correct data.
        Twilio account is present
        Access to read only API from the company’s side- which helps both the company and us.


Function Descriptions:


1. **`extract_calendly_info(calendly_link)`**:
   - This function takes a Calendly link as input and extracts the Calendly event ID and expiration date from the link.
   - The logic to extract this information may vary depending on the structure of the Calendly link provided.
   - In the current implementation, it simply extracts the last part of the URL as the event ID and assumes a hardcoded expiration date (August 1, 2023).
   - Case covered: Extracting relevant information from the Calendly link for further processing.

2. **`notify_company_link_expiration(company_contact, company_name, calendly_link)`**:
   - This function sends an email notification to the company's contact when the provided Calendly link is about to expire (within the next 7 days).
   - It constructs an email message containing the company name and the expiring Calendly link, and sends it to the company's contact email address using the `send_email` function.
   - Case covered: Notifying the company about an expiring Calendly link to avoid disruptions in the scheduling process.

3. **`monitor_calendly_events(event_id, company_contact, company_name)`**:
   - This function monitors updates to Calendly events, such as cancellations or rescheduling, for the given event ID.
   - It queries the Calendly API for event updates and processes them accordingly.
   - If an event is canceled, it notifies the interviewee by calling the `notify_interviewee_event_canceled` function.
   - If an event is rescheduled, it notifies the interviewee by calling the `notify_interviewee_event_rescheduled` function.
   - Additional logic can be added to handle other types of event updates, if needed.
   - Case covered: Monitoring Calendly event updates and notifying interviewees about cancellations or rescheduling.
   - Added notification for the Interviewer if a meeting is scheduled

4. **`follow_up_company_unscheduled(company_contact, company_name, event_id)`**:
   - This function follows up with the company if there are unscheduled interviews after a certain period (one week in this implementation).
   - It queries the Calendly API for unscheduled events related to the given event ID.
   - If any unscheduled interviews are found, it sends a follow-up email to the company's contact, requesting them to review and update their Calendly link or provide additional information to facilitate the scheduling process.
   - Case covered: Following up with the company for unscheduled interviews to ensure timely scheduling.

5. **`send_calendly_link(email, phone, company_name, calendly_link)`**:
   - This function sends the Calendly link to the interviewee using their preferred contact method (WhatsApp, call, or email).
   - It attempts to send the Calendly link via WhatsApp first, then falls back to a call, and finally to email if the previous methods fail.
   - It constructs a message containing the company name and the Calendly link, and sends it using the respective communication channel.
   - Case covered: Sending the Calendly link to the interviewee using their preferred contact method.

6. **`check_scheduled_meeting(email, phone, company_name, calendly_link)`**:
   - This function checks if the interviewee has scheduled a meeting for the given Calendly link.
   - It queries the Calendly API for scheduled events related to the provided Calendly link.
   - It checks if any of the scheduled events match the interviewee's email or phone number.
   - If a match is found, it returns `True`, indicating that the interviewee has scheduled a meeting.
   - Case covered: Checking if the interviewee has scheduled a meeting using the provided Calendly link.

7. **`follow_up(email, phone, company_name, calendly_link)`**:
   - This function sends a follow-up communication to the interviewee if they have not scheduled a meeting after the initial Calendly link was sent.
   - It sends a reminder message to the interviewee via WhatsApp and email, containing the company name and the Calendly link.
   - After a 3-hour wait, it checks again if the interviewee has scheduled a meeting using the `check_scheduled_meeting` function.
   - If the interviewee still hasn't scheduled a meeting, it escalates the case to manual intervention by calling the `manual_intervention` function.
   - Case covered: Sending follow-up communications to the interviewee and escalating to manual intervention if necessary.

8. **`manual_intervention(email, phone, company_name)`**:
   - This function is called when manual intervention is required for an interviewee who hasn't scheduled a meeting after follow-up communications.
   - It currently only prints a message indicating that manual intervention is required for the given interviewee and company.
   - Additional logic can be added to assign the case to a team member or perform other necessary actions.
   - Case covered: Flagging cases for manual intervention when automated methods fail to schedule a meeting.

9. **`send_email(recipient, message)`**:
   - This is a helper function that sends an email to the specified recipient with the given message.
   - It requires the user to provide their email credentials (sender's email address and password).
   - It uses the `smtplib` library to connect to an SMTP server and send the email.
   - Case covered: Sending email communications.

10. **`make_call(phone_number, message)`**:
    - This is a helper function that makes a voice call to the specified phone number and reads out the given message.
    - It utilizes the Twilio API to initiate the call and uses Twilio's Text-to-Speech (TTS) feature to read the message.
    - It requires the user to provide their Twilio account SID, auth token, and a Twilio phone number.
    - Case covered: Making voice calls for communication.

11. **`send_whatsapp(phone_number, message)`**:
    - This is a helper function that sends a WhatsApp message to the specified phone number with the given message.
    - It utilizes the Twilio API to send the WhatsApp message.
    - It requires the user to provide their Twilio account SID, auth token, and a Twilio WhatsApp number.
    - Case covered: Sending WhatsApp messages for communication.

12. **`notify_interviewee_event_canceled(invitee_email, company_name)`**:
    - This function sends an email notification to the interviewee when their scheduled interview with the company is canceled.
    - It constructs an email message informing the interviewee about the cancellation and sends it to their email address using the `send_email` function.
    - Case covered: Notifying the interviewee about the cancellation of a scheduled interview.

13. **`notify_interviewee_event_rescheduled(invitee_email, company_name, new_event_time)`**:
    - This function sends an email notification to the interviewee when their scheduled interview with the company is rescheduled to a new date and time.
    - It constructs an email message informing the interviewee about the rescheduled interview and sends it to their email address using the `send_email` function.
    - Case covered: Notifying the interviewee about the rescheduling of a scheduled interview.


