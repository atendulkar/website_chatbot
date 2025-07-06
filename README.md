# Initial Setup:
Clone repo and create a virtual environment

$ git clone https://github.com/atendulkar/chatbot_for_website.git
$ cd chatbot-deployment
$ python3 -m venv venv
$ . venv/bin/activate

# Install dependencies
Run below commands

    pip install -r requirements.txt
    python app.py

Then open http://localhost:5000

## To Run in DOCKER environment
# Build the image
docker build -t naic-chatbot .

# Run the container
docker run -p 5000:5000 naic-chatbot

Then open your browser and visit:
http://localhost:5000

naic_chatbot/
├── app.py
├── requirements.txt
├── Dockerfile
├── chatbot/
│   ├── __init__.py
|   ├── logic.py
│   ├── hybrid_search.py
│   ├── live_search.py
|   └── ...
└── templates/
    └── index.html
