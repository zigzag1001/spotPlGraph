"""Sets up authentication parameters and headers to access the Spotify API, 
sends an authentication request, and extracts the access token from the response. 
If a refresh token exists, it is used to get a new access token. If a refresh token does not exist,
the user is prompted to input an auth code. Finally, the function returns headers that can be used
to access the Spotify API with the obtained access token."""

# Import necessary libraries
import subprocess
import requests
import base64
import json
import os

# Define function to get access token
def getAccessToken():

    # Check if credentials file exists and load credentials
    creds_path = "credentials.json"
    if os.path.isfile(creds_path):
        with open(creds_path, "r") as f:
            creds = json.load(f)
    else:
        # Prompt user for client ID and client secret
        print("Enter your Spotify API client ID, client secret and redirect uri:")
        CLIENT_ID = input("Client ID: ")
        CLIENT_SECRET = input("Client secret: ")
        REDIRECT_URI = input("Redirect uri: ")
        creds = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "redirect_uri": REDIRECT_URI}

    # Set authentication URL
    authUrl = "https://accounts.spotify.com/api/token"

    # Define authentication parameters
    data = {"grant_type": "authorization_code",
            "code": "x",
            "redirect_uri": creds["redirect_uri"],
            "client_id": creds["client_id"],
            "client_secret": creds["client_secret"]}

    # Set authentication headers
    authHeaders = {"Content-Type": "application/x-www-form-urlencoded"}

    # Check if refresh token exists in credentials file
    if "refresh_token" in creds:
        data["grant_type"] = "refresh_token"
        data["refresh_token"] = creds["refresh_token"]
    else:
        # If refresh token does not exist, prompt user for auth code
        print('\nYou need to allow app to read data from your acc\nGo to this url, allow access, and copy everything after "code=" in the url')
        # Define authentication parameters
        response_type= 'code'
        client_id= creds["client_id"]
        scope= "playlist-read-private"
        redirect_uri= creds["redirect_uri"]

        # Set up authentication request URL
        url = f"https://accounts.spotify.com/authorize?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"

        # Print the authentication request URL
        print(url)

        data["code"] = input("=============\nInput Auth Code:")

    # Send authentication request and get response
    req0 = requests.post(authUrl, data = data, headers = authHeaders).text

    # Extract access token from response
    access_token = json.loads(req0)["access_token"]

    # If refresh token does not exist, save it to the credentials file
    if "refresh_token" not in creds:
        refresh_token = json.loads(req0)["refresh_token"]
        creds["refresh_token"] = refresh_token
        with open(creds_path, "w") as f:
            json.dump(creds, f)

    # Set headers for accessing Spotify API with access token
    headers = {"Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"}

    # Return headers for accessing Spotify API
    return headers