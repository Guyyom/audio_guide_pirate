from boto3 import Session, client
from botocore.config import Config
import urllib3
from os import environ
import xmltodict

#Needed to buffer the loading of the .mp3
def getxml(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    data = xmltodict.parse(response.data)
    return data

def AWS_Creation(lang, input):
    #AWS only authorized signature version 4 in order to generate presigned url 
    #More info : https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
    my_config = Config(region_name = 'eu-west-3',
    signature_version = 's3v4')

    #Select voice on S3 - depending on User input
    if lang == "fr" or lang == "FR":
        voice = "Lea"
    elif lang == "en" or lang == "EN":
        voice = "Emma"

    # Create a client using the credentials and region defined in the [adminuser]
    # section of the AWS credentials file (~/.aws/credentials).
    #Environment variables are used to protect privacy (To set up a envvvar : export varname=value)
    polly_client = Session(
        aws_access_key_id= environ['aws_access_key_id'],
        aws_secret_access_key= environ['aws_secret_access_key'],
        region_name='eu-west-3').client('polly')

    #TextType est le paramètre qui permet de passer les prosody dans Text
    #Get the .mp3 + store it directly on S3 bucket 
    response = polly_client.start_speech_synthesis_task(TextType="ssml",
                                                        VoiceId= voice,
                                                        OutputS3BucketName='audioguide3313',
                                                        OutputS3KeyPrefix='key',
                                                        OutputFormat='mp3',
                                                        Text= "<speak><prosody rate='medium'>" + input + 
                                                              "</prosody></speak>",
                                                        Engine='neural')
    
    #Get TaskID in order to create the Presigned Url
    taskId = response['SynthesisTask']['TaskId']

    #Generate the presigned URL
    url = client(
        's3',
        aws_access_key_id= environ['aws_access_key_id'],
        aws_secret_access_key= environ['aws_secret_access_key'],
        config=my_config).generate_presigned_url(
            ClientMethod='get_object', 
            Params={'Bucket': 'audioguide3313', 'Key': "key." + taskId + ".mp3"},
            ExpiresIn=3600)
    
    #Run in a loop while the .mp3 is generated and the presigned URL is not finalized
    try:
        uri = getxml(url)
        while (uri["Error"]):
            uri = getxml(url)
    except:
        return url, taskId


def AWS_Generation(i):
    #Set up for presigned url request
    #AWS only authorized signature version 4 in order to generate presigned url 
    #More info : https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
    my_config = Config(region_name = 'eu-west-3',
    signature_version = 's3v4')

    #Generate the presigned URL
    url = client(
    's3',
    aws_access_key_id= environ['aws_access_key_id'],
    aws_secret_access_key= environ['aws_secret_access_key'],
    config=my_config).generate_presigned_url(
        ClientMethod='get_object', 
        Params={'Bucket': 'audioguide3313', 'Key': "key." + i + ".mp3"},
        ExpiresIn=3600)

    #Run in a loop while the .mp3 is generated and the presigned URL is not finalized
    try:
        uri = getxml(url)
        while (uri["Error"]):
            uri = getxml(url)
    except:
        return url
