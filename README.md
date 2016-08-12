# facebook-chatbot-template

A Python template for a Facebook Messenger chatbot server that uses Wit.ai for language processing.


## Prerequisites

`$ sudo apt install libxml2-dev libxslt1-dev python-dev`

`$ pip3 install -r requirements.txt`


## Run Local Debug Console

1. Edit `run-local-interactive-frontend.sh`, specify API keys/tokens.
2. Run `run-local-interactive-frontend.sh`.

*Note:* Alternatively, you can use the "Local Interactive Front-End" run configuration in IntelliJ products. Just make sure to edit it and change the `WIT_AI_SERVER_TOKEN` environment variable.


## Run Webhook Server for Facebook Messenger

1. Deploy the `app` folder to a publicly addressable Web server with an HTTPS endpoint (Let's Encrypt certificates work here as well).
2. Edit `run-fb-messenger-frontend.sh`, specify API keys/tokens.
3. Run `run-fb-messenger-frontend.sh`.
4. (First time only) Go to Facebook Developer portal and register the server as a webhook in your app settings. The webhook will get called and your application should be able to respond to the verification request.

