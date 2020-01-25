from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

import pandas as pd


def main():
    
    df=pd.read_csv('projectData.csv')

    credentials = pickle.load(open("tokennew.pkl", "rb"))
    service = build("gmail", "v1", credentials=credentials)

    response = service.users().messages().list(userId='me',q='').execute()

    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])

    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId='me', q='',pageToken=page_token).execute
        messages.extend(response['messages'])


    for i in messages:
        message = service.users().messages().get(userId='me', id=i['id'],
                                                 format='full').execute()

        getstatus=message["labelIds"]
##        print(getstatus)
        if(getstatus[0]== "UNREAD"):
            #service.users().messages().modify(userId='me', id=i['id'], body="READ").execute()
            mail = message['snippet']
            print(mail)


            headers=message["payload"]["headers"]
            subject= [i['value'] for i in headers if i["name"]=="Subject"]
       #     print(subject[0])
            df.iat[0,2]=subject[0]

            


##            print("___________________")
            mailid= [i['value'] for i in headers if i["name"]=="From"]
       #     print(mailid[0])
            df.iat[0,1]=mailid[0]

            df.to_csv('projectData.csv', index=False)

            
        break
    print("msg,mailid,subject done")
    return mail
##        print('Message snippet: %s' % message['snippet'])
##        print("___________________")
    # Query the service object to get User Profile
    #userInfo = service.users().getProfile(userId='me').execute()
    #print("UserInfo is \n %s" % (userInfo))
