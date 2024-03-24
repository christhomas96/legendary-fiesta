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

Assumptions made:
        Given sheet has correct data.
        Twilio account is present
        Access to read only API from the company’s side- which helps both the company and us.
