# A reusable Midtrans client for Django projects.
This projects creates midtrans payment-links not a SNAP.

## Environment settings
```
export MIDTRANS_SERVER_KEY="set-your-midtrans-server-key-here"
export MIDTRANS_CLIENT_KEY="set-your-midtrans-client-key-here"
export MIDTRANS_BASE_URL='https://api.sandbox.midtrans.com/v1/payment-links'
```

## Base settings
```
    MIDTRANS_SERVER_KEY = env(
        "MIDTRANS_SERVER_KEY",
        default=None,
    )
    MIDTRANS_CLIENT_KEY = env(
        "MIDTRANS_CLIENT_KEY",
        default=None,
    )
    MIDTRANS_BASE_URL = env(
        "MIDTRANS_BASE_URL",
        default="https://api.sandbox.midtrans.com/v1/payment-links",
    )
    MIDTRANS_ENABLED_PAYMENTS = []
    DEFAULT_INSTALLMENT_TERMS = []
```
## Site domain
You need to set your site domain name in django admin page, so the callback will redirect to your site.


### Midtrans links
- https://docs.midtrans.com/docs/payment-link-api-reference
- https://simulator.sandbox.midtrans.com/
