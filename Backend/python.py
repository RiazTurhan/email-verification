import re
import smtplib
import dns.resolver
from fastapi import FastAPI, HTTPException

app = FastAPI()

def is_valid_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

@app.get("/check-email/")
def check_email_exists(email: str):
    if not is_valid_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
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
            return {"status": "success", "message": "Yes, the email address exists."}
        else:
            return {"status": "failed", "message": "No, the email address does not exist."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
