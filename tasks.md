# Aspects of the chatbot
## [Example we hope to emulate from my old school](http://askgryph.registrar.uoguelph.ca/)
## Front end
* Can be beautiful, can be hideous, doesn't matter
* Input window for text
* Output section
    * Is this like a chat window with slow line by line responses? Or can it just fill out a page of information?
    * I'm not a fan of pretending to be a person, I'd prefer to just info dump like AskGryph
* Needs to communicate with the backend, with authentication
    * Probably just send raw text, without encryption.
    * We might want to use login tokens

## Back end
* Which language? I want Go. Go is the best.
* Parse input from front end
    * Natural Language Processing for a wide variety of inputs? Need to read up on libraries, which constrains our language choice
    * [Go NLP library](https://github.com/advancedlogic/go-freeling)
    * [Python NLP library](http://www.nltk.org/)
    * Or short, keyword based?
* Query database for knowledge
* Send output to frond end
* login system
    * Probably just a lookup in the database.
    * We could maybe make a mockup of UTSA's authorization token
* segue to real person?
    * I don't know. This looks like a completely separate program

## database
* login table
    * users, passwords (not super secure, i think, for this), priviledge level
* knowledge table
    * ID, pre-written text/html, required priviledge level
* log table
    * ID, datetime, user-level who accessed
