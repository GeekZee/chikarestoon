from typing import List
from datetime import datetime, timedelta
from ..db.models import User
from ..utils.config import get_settings

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import jwt


SITE_URL = get_settings().SITE_URL
SITE_NAME = get_settings().SITE_NAME


conf = ConnectionConfig(
    MAIL_USERNAME=get_settings().MAIL_USERNAME,
    MAIL_PASSWORD=get_settings().MAIL_PASSWORD,
    MAIL_FROM=get_settings().MAIL_FROM,
    MAIL_PORT=get_settings().MAIL_PORT,
    MAIL_SERVER=get_settings().MAIL_SERVER,
    MAIL_TLS=get_settings().MAIL_TLS,
    MAIL_SSL=get_settings().MAIL_SSL,
    USE_CREDENTIALS=get_settings().USE_CREDENTIALS,
    VALIDATE_CERTS=get_settings().VALIDATE_CERTS
)


async def send_mail(email: List, instance: User):
    """send Account Verification mail"""

    token_data = {
        "id": instance.id,
        "type": "email_verification",
        "exp": datetime.utcnow() + timedelta(days=1)
    }

    token = jwt.encode(token_data, get_settings().SECRET, algorithm="HS256")

    template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <div style = "display:flex; align-items: center; flex-direction: column" >
            <h3>Chikarestoon Account Verification</H3>

            <br>

            <p>
                Thanx for choosing us, please click on the button below
                to verify your account
            </p> 
            
            <a style = "display:marign-top: 1rem ; padding: 1rem; border-redius: 0.5rem;
             font-size:1rem; text-decoration: no; background: #0275d8; color:white"
             href="{SITE_URL}/users/verification/email/?token={token}">
                Verify your email
             </a>
        </div>
    </body>
    </html>
    """

    message = MessageSchema(
        subject=SITE_NAME + " account verification",
        recipients=email,  # List of recipients,
        body=template,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
