import os

import stripe
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from supabase import create_client

load_dotenv()

app = FastAPI(title="LiveCreator AI Stripe Webhook")

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

supabase = None
if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def mark_user_premium(user_id: str | None, email: str | None) -> bool:
    """Mark the matching Supabase user profile as premium.

    Uses user_id first because the Streamlit app sends it to Stripe as
    client_reference_id. Email is a fallback.
    """
    if not supabase:
        raise RuntimeError("Supabase webhook client is not configured.")

    if user_id:
        result = (
            supabase.table("user_profiles")
            .upsert({"id": user_id, "email": email, "is_premium": True}, on_conflict="id")
            .execute()
        )
        return bool(result.data)

    if email:
        result = (
            supabase.table("user_profiles")
            .update({"is_premium": True})
            .eq("email", email)
            .execute()
        )
        return bool(result.data)

    return False


def extract_customer_email(event_object: dict) -> str | None:
    return (
        (event_object.get("customer_details") or {}).get("email")
        or event_object.get("customer_email")
        or event_object.get("receipt_email")
        or (event_object.get("metadata") or {}).get("email")
    )


@app.get("/")
def health_check():
    return {"status": "ok", "service": "LiveCreator AI Stripe Webhook"}


@app.post("/stripe-webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(default="")):
    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="STRIPE_WEBHOOK_SECRET is not configured.")

    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=stripe_signature,
            secret=STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Stripe payload.")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid Stripe signature.")

    event_type = event.get("type")
    event_object = event.get("data", {}).get("object", {})

    if event_type == "checkout.session.completed":
        user_id = event_object.get("client_reference_id")
        email = extract_customer_email(event_object)

        if not mark_user_premium(user_id=user_id, email=email):
            raise HTTPException(
                status_code=404,
                detail="Payment received, but no matching Supabase user profile was found.",
            )

    return {"received": True}
