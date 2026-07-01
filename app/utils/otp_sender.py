# app/utils/otp_sender.py
import logging

from app.config import settings

logger = logging.getLogger(__name__)

async def send_otp(destination: str, otp: str, channel: str) -> None:
    """
    channel: 'sms' | 'email'
    """
    if settings.OTP_DEV_MODE:
        logger.warning(
            "[OTP_DEV_MODE] channel=%s destination=%s otp=%s",
            channel, destination, otp,
        )
        print(f"\n>>> DEV OTP for {destination}: {otp} <<<\n")
        return

    if channel == "sms":
        await _send_sms(destination, otp)
    else:
        await _send_email(destination, otp)

async def _send_sms(phone: str, otp: str) -> None:
  # TODO: Twilio integration
    if not settings.TWILIO_ACCOUNT_SID:
        raise RuntimeError("Twilio not configured")
    # from twilio.rest import Client
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # client.messages.create(body=f"Your Baithak code: {otp}", from_=..., to=phone)

async def _send_email(email: str, otp: str) -> None:
  # TODO: aiosmtplib integration
    if not settings.SMTP_HOST:
        raise RuntimeError("SMTP not configured")
    # send mail with otp