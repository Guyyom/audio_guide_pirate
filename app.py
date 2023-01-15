#On Heroku, more specificaly on WGSI server, in order to link a function from another file, always add a "." before the file name
from .AWS_interaction import AWS_Creation, AWS_Generation
from boto3 import Session
from flask import Flask, render_template, request, redirect, flash, url_for
import psycopg2
#On Heroku, more specificaly on WGSI server, in order to link a function from another file, always add a "." before the file name
from .wiki import request_api
from os import environ

class AudioGuideRequest: 
    def __init__(self): 
        pass

    #Verify if the input from the user already exists in DB 
    def verify_wikiid(self, wikiid):
        con = psycopg2.connect(
            host=environ["host_postgre"],
            user=environ["user_postgre"],
            password=environ["password_postgre"],
            port="5432"
            )
        db = con.cursor()
        db.execute("""SELECT key_object FROM public.audio WHERE wikiid = (%s)""", (wikiid,))
        result = db.fetchone()
        if result:
            for i in result:
                db.close()
                return i
        else:
            db.close()
            return False

    #Inject in DB the references from the request newly created 
    def insert(self, url, wikiid, key_object, input):
        con = psycopg2.connect(
            host=environ["host_postgre"],
            user=environ["user_postgre"],
            password=environ["password_postgre"],
            port="5432"
            )
        db = con.cursor()
        db.execute("""INSERT INTO audio VALUES(%s, %s, %s, %s)""", (wikiid, url, key_object, input))
        con.commit()
        db.close()


#Inite Flask server app
app = Flask(__name__)
#Set up app secret key in order to allows flash messages (more globally to protect against data tampering)
app.secret_key = environ['app_secret_key']
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = False
#Configures Flask to store sessions on the local filesystem (i.e., disk) 
#as opposed to storing them inside of (digitally signed) cookies, which is Flask’s default
app.config["SESSION_TYPE"] = "filesystem"
#Allow to manage Session on server side 
Session(app)

list_lang = ["FR", "fr", "EN", "en"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST": 
        input = request.form.get("input")
        lang = request.form.get("lang")

        #If Lang is not correct, flash error messages
        if lang not in list_lang:
            flash('This language is not supported please select one from the dropdown list')
            return redirect(url_for("index"))

        #Get wikiid from user's request
        #And if the page on Wikipedia doesn't exist, return flash messages
        if request_api(lang, input) == None:
            flash("This Wikipedia page doesn't exist, for more details on how to use this tool, check our FAQ")
            return redirect(url_for("index"))
        #Else return the description as plain text + wikiid from the wikipedia page
        else:
            tts, wikiid = request_api(lang, input)
        #Verify if wikiid already exist in dataabase
        #Please note that database is a PostGresSQL database
        audio_guide_request = AudioGuideRequest()
        result = audio_guide_request.verify_wikiid(wikiid)
        #If wikiid exists, generate a presigned url on aws and redirect to it
        if result:
            url = AWS_Generation(result)
            return redirect(url)
        #If it doesn't exist, generate a new mp3 with Polly AWS and store the .mp3 on AWS S3
        else:
            url, key_object = AWS_Creation(lang, tts)
            #Insert into database url & wikiid & key_object of the newly created .mp3 + redirect to the new URL 
            audio_guide_request.insert(url, wikiid, key_object, input)
            return redirect(url)
    return render_template("index.html")

#Route to FAQ.html
@app.route("/faq", methods=["GET"])
def faq():
    return render_template("faq.html")