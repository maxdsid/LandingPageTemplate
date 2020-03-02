# Imports
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import requests
import json

# Setting Flask App
app = Flask(__name__)
CORS(app)
api = Api(app)

class File(Resource):
    """
    This class serves as an API endpoint for adding a new contact to Watson contact list.
    Every time the React page is loaded it sends a GET request which will also generate Auth Token privately for this class via private __get_auth_token method.
    This Token will be used for the same session each time POST method is called.
    POST method verifies API data coming from React page and calls another private method __add_contact to send this request to the Watson DB
    Things to change for each campaign:
    get method:
        no change
    post method:
        Add/change parse arguments according to your campaign requirements. These arguments will be passed from React App to Watson API
    __add_contact method:
        WATSON_API_URL - only change if pod number is changed
        DATABASE_ID - main database id - only change if customer is changed
        CONTACT_LIST_ID - contact list for the campaign
        request - make sure that column names and values are correct
    __get_auth_token method:
        Change WATSON_API_AUTH dictionary if you API credentials for the client has changed (you can obtain those credentials from your admin
    """
    def __get_auth_token(self):
        """This method generates Watson Auth Token
        :return: True if the token was generated
        """
        WATSON_API_AUTH = {
            'api_auth_url': 'http://api7.ibmmarketingcloud.com/oauth/token?grant_type=refresh_token',
            'client_id': 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz',
            'client_secret': 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy',
            'refresh_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        }
        tokenURL = f"{WATSON_API_AUTH['api_auth_url']}&client_id={WATSON_API_AUTH['client_id']}&client_secret={WATSON_API_AUTH['client_secret']}&refresh_token={WATSON_API_AUTH['refresh_token']}"
        getToken = requests.request('POST', tokenURL)
        if getToken.status_code == 200:
            accessToken = getToken.text.split('"')[3]
            # Generating the header that will be used for all API requests
            self.__headers = {'Content-Type': 'text/xml', 'Authorization': 'bearer ' + accessToken}
            return True
        else:
            return False

    def __add_contact(self, args):
        """
        This method generates XML request and sends it to Watson API
        :param args: form data from the React App
        :return: True/False of success
        """
        WATSON_API_URL = 'https://api7.ibmmarketingcloud.com/XMLAPI'
        DATABASE_ID = '45412'
        CONTACT_LIST_ID = '1553214'
        request = f'<Envelope><Body><AddRecipient><LIST_ID>{DATABASE_ID}</LIST_ID>' \
            f'<CREATED_FROM>1</CREATED_FROM>' \
            f'<CONTACT_LISTS><CONTACT_LIST_ID>{CONTACT_LIST_ID}</CONTACT_LIST_ID></CONTACT_LISTS>' \
            f'<COLUMN><NAME>First Name</NAME><VALUE>{args["first_name"]}</VALUE></COLUMN>' \
            f'<COLUMN><NAME>Last Name</NAME><VALUE>{args["last_name"]}</VALUE></COLUMN>' \
            f'<COLUMN><NAME>Date of Birth</NAME>{args["dob"]}</VALUE></COLUMN>' \
            f'<COLUMN><NAME>Mobile</NAME><VALUE>{args["mobile"]}</VALUE></COLUMN>' \
            f'<COLUMN><NAME>Email</NAME><VALUE>{args["email"]}</VALUE></COLUMN>' \
            f'<COLUMN><NAME>PreferredDeparturePoint</NAME><VALUE>{args["pdp"]}</VALUE></COLUMN>' \
            f'</AddRecipient></Body></Envelope>'
        response = requests.request('POST', WATSON_API_URL, data=request, headers=self.__headers)
        response = response.content.decode()
        status = response[response.find('<SUCCESS>')+9:response.find('</SUCCESS>')]
        if status is 'true':
            return True
        else:
            return False

    def get(self):
        if self.__get_auth_token():
            return "Auth Token generated", 200
        else:
            return "Auth Token wasn't generated", 500

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', required=True, type=str, help="Cannot be blank!")
        parser.add_argument('last_name', required=True, type=str, help="Cannot be blank!")
        parser.add_argument('dob', required=True, help="Cannot be blank!")
        parser.add_argument('mobile', required=True, help="Cannot be blank!")
        parser.add_argument('email', required=True, type=str, help="Cannot be blank!")
        parser.add_argument('pdp', required=True, type=str, help="Cannot be blank!")
        args = parser.parse_args()
        if self.__add_contact(args):
            return 'The details were sent successfully', 202
        else:
            return 'Invalid XML Request', 400

api.add_resource(File, '/template')

app.run(debug=True)