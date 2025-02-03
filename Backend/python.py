import re
import smtplib
import dns.resolver

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

def check_email_exists(email):
    if not is_valid_email(email):
        return "Invalid email format"
    
    domain = email.split('@')[-1]

    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(mx_records[0].exchange)
        

        server = smtplib.SMTP(mx_record)
        server.set_debuglevel(0) 
        server.helo()
        server.mail("test@example.com")  
        code, message = server.rcpt(email)
        server.quit()

        if code == 250:
            return "Yes, the email address exists."
        else:
            return "No, the email address does not exist."
    
    except Exception as e:
        return f"Error: {e}"


email = input('Enter Your Email ')  
print(check_email_exists(email))
