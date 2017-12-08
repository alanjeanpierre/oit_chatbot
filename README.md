# OIT Chatbot

OIT Chatbot is an automated support system for UTSA's OIT department. The chatbot is used to answer common questions automatically without the need for human intervention. OIT Chatbot is primarily aimed at the student population and answering questions relating to Blackboard Learn, ASAP, PrintSpot, or Degree Works. OIT Chatbot attempts to simulate a live person in interaction and provide a natural support system.

## Installation
* OIT Chatbot requires the Flask and TextBlob libraries, along with the associated NLTK data for TextBlob. 
* To install Flask, type `pip3 install -U Flask`
* To install TextBlob, type `pip3 install -U textblob`
* TextBlob requires some external dependencies, you can install them with `python3 -m textblob.download_corpora lite`
* Finally, install OIT Chatbot by running `pip3 install /path/to/oit_chatbot/`

## Running
* To run OIT Chatbot, run through Flask
* First, export the name of the application, `export FLASK_APP=oit_chatbot`
* Then initialize the database `flask initdb`
* Then run the application `flask run --host=0.0.0.0 --port=80` or whichever port desired