import re
import smtplib
import dns.resolver
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Change this to your frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_valid_email(email: str) -> bool:
    """Check if the email format is valid."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

@app.get("/check-email/")
def check_email_exists(email: str):
    """Check if the email exists via DNS MX records and SMTP."""
    if not is_valid_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    domain = email.split('@')[-1]
    try:
        # Get MX record of the domain
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(mx_records[0].exchange)

        # Connect to the mail server
        server = smtplib.SMTP(mx_record, 587)  # Using port 587 for secure connection
        server.set_debuglevel(2)  # Set debug level to 2 for detailed logs
        server.starttls()  # Upgrade the connection to TLS
        server.helo()
        server.mail("test@example.com")  # Fake sender email
        code, _ = server.rcpt(email)
        server.quit()

        if code == 250:
            return {"status": "success", "message": "Yes, the email address exists."}
        else:
            return {"status": "failed", "message": "No, the email address does not exist."}
    
    except smtplib.SMTPException as e:
        raise HTTPException(status_code=500, detail=f"SMTP connection failed: {str(e)}")
    except dns.resolver.NoAnswer as e:
        raise HTTPException(status_code=500, detail=f"DNS MX record lookup failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
