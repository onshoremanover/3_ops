# splunk_quiz_training
Simplest Web App for training for splunk exams

# Structure

In app.py 
there are the routes (webpages) for initial page, **question page**, **answer page** and **results page**. 
All the logic happens in here and is pretty much hardcoded.

In questions.json5 
there are all the questions comprising of **question**, **answer**, **choices** and sometimes **explanation**. There is not always an explanation.
It is in the json5 format, because it allows comments and looks a bit cleaner

The **app.py** and **questions.json5** is basically all you need.

The **requirements.txt** describs what python libraries are needed and in which version.

# Before Starting
Create a **venv** outside this app and activate it. (. env/bin/activate) then go into the app and get all the libraries from the requirements.txt.

Start the app.

It is only running in development mode but I mean it does not need to run like a production server. Tweaking it can get you running it on your local server so make 
it accessible for other devices.

Modify the questions and whatever you need.

