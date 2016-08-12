#!/usr/bin/env bash

# FB Messenger Tokens
export FB_PAGE_ACCESS_TOKEN=SpecifyTokenHere
export FB_WEBHOOK_VERIFY_TOKEN=SpecifyTokenHere

# SSL Certificates
export SSL_CERTIFICATE_FILE="/etc/...../fullchain.pem"
export SSL_PRIVATE_KEY_FILE="/etc/...../privkey.pem"

python3 frontend/fb_messenger.py
