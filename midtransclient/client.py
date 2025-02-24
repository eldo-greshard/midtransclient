import base64
import json
from datetime import datetime, timedelta, timezone

import requests
from django.conf import settings
from django.contrib.sites.models import Site
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.utils.timezone import now


class MidtransClient:
    BASE_URL = "https://api.sandbox.midtrans.com/v1/payment-links"
    DEFAULT_ENABLED_PAYMENTS = getattr(
        settings, "MIDTRANS_ENABLED_PAYMENTS", ["credit_card", "bca_va", "indomaret"]
    )
    DEFAULT_INSTALLMENT_TERMS = getattr(
        settings,
        "MIDTRANS_INSTALLMENT_TERMS",
        {
            "bni": [3, 6, 12],
            "mandiri": [3, 6, 12],
            "cimb": [3],
            "bca": [3, 6, 12],
            "offline": [6, 12],
        },
    )

    def __init__(self):
        self.server_key = base64.b64encode(
            f"{settings.MIDTRANS_SERVER_KEY}:".encode()
        ).decode()
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.server_key}",
        }
        self.callback_url = (
            f"https://{Site.objects.get_current().domain}/payment-success/"
        )

    def generate_order_id(self):
        return now().strftime("%Y%m%d%H%M%S")

    def create_payment_payload(self, order_id, gross_amount, item_details):
        expiry_time = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        payload = {
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": gross_amount * 1000,
                "payment_link_id": f"payment-{order_id}",
            },
            "customer_required": True,
            "callbacks": {"finish": self.callback_url},
            "usage_limit": 1,
            "expiry": {
                "start_time": expiry_time,
                "duration": 60,
                "unit": "minutes",
            },
            "item_details": item_details,
        }

        if self.DEFAULT_ENABLED_PAYMENTS is not False:
            payload["enabled_payments"] = self.DEFAULT_ENABLED_PAYMENTS

        if self.DEFAULT_INSTALLMENT_TERMS is not False:
            payload["credit_card"] = {
                "secure": True,
                "bank": "bca",
                "installment": {
                    "required": False,
                    "terms": self.DEFAULT_INSTALLMENT_TERMS,
                },
            }

        return payload

    def process_payment_request(self, payload):
        response = requests.post(
            self.BASE_URL, headers=self.headers, data=json.dumps(payload)
        )
        if response.status_code in [200, 201]:
            return HttpResponseRedirect(response.json()["payment_url"])
        return JsonResponse({"error": "Failed to create payment link"}, status=400)

    def create_payment_link(self, item, item_type, item_details):
        if not item:
            raise Http404(f"{item_type.capitalize()} not found")
        order_id = self.generate_order_id()
        payload = self.create_payment_payload(order_id, item.price, item_details)
        return self.process_payment_request(payload)
