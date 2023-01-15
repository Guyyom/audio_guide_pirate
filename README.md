#### Introduction 

Audio Guide Pirate is a tool developed to parse wikipedia pages description and transcript it into audio .mp3 files. 


### How to use it 

> App.py : Manage all the functions to interacte with the web server app Flask. It includes also all the required function to send
POST / GET request to the revelant .html pages

> AWS_Interaction.py : There are 2 functions in the file =
    1. Create and store the .mp3 files on a S3 on AWS
    2. Generate presigned url in order to access the .mp3 from the AWS S3 (a presigned URL is a temporary URL created on the go 
    by the user)

> wiki.py : Includes all the function to parse wikipediage pages and return a plain-text description of the wikipedia pages

> faq.html : Explain how the app works

> index.html : Includes forms to intereact with the app and some functions in Jquery to manipulate and interacte with the webpage.

> layout.html : Main layout of each webpages - includes CDN for Jquery framework (Javascript) and Bootstrap Framework (.css management)

> db : db is a databa in SQLITE3. Due to deployment this DB is deprecated. The deployment of the app has been done via AWS with a POSTGRESQL DB
For this reason the library psycopg2 has been added. 
Additionnaly, due to deployment on Heroku, import functions includes some "." before all files created by the developper - aka
AWS_Interaction.py & wiki.py
Database is on AWS and accessible via DBeaver

> Environment variable : Some envvar are used in this app = 
    - For cookie protection within the FLASK APP // app.secret_key = environ['app_secret_key']
    - For connection on POSTGRESQL Database //
            host=environ["host_postgre"],
            user=environ["user_postgre"],
            password=environ["password_postgre"],
            port="5432"
    - For AWS connection //
            aws_access_key_id= environ['aws_access_key_id'],
            aws_secret_access_key= environ['aws_secret_access_key'],


> Procfile : Is used by the HEROKU App in order to identify which webserver to set up. GUNICORN in our case is a web server.
app.app:app = it signifies that app.py application is in the folder /app 
Simply change app.app:app in app:app if app.py application is in the current folder during deployment.
