import httplib2
import os
import sys

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

video_id = "IrPwZ7ejsw8"
channel_id = "UC5aFBZOvtseFQWib1kILbpA"


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains

# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# Authorize the request and store authorization credentials.
def get_authenticated_service():
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage)

  # Trusted testers can download this discovery document from the developers page
  # and it should be in the same directory with the code.
  with open("youtube-v3-api-captions.json", "r", encoding='utf8') as f:
    doc = f.read()
    return build_from_document(doc, http=credentials.authorize(httplib2.Http()))

def get_upload_playlist_id(youtube, channel_id):
    results = youtube.channels().list(
      id=channel_id,
      part="contentDetails"
    ).execute()
    upload_playlist_id = results["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    print(upload_playlist_id)
    return upload_playlist_id

def get_playlist_video_id(youtube, playlist_id, **kwargs):
  results = youtube.playlistItems().list(
    part='contentDetails',
    playlistId = upload_playlist_id,
    **kwargs
  ).execute()
  #next_page_token = results["nextPageToken"]

  return results


def collect_all_pages():
    playlist_videos = get_playlist_video_id(youtube, upload_playlist_id)
    print(playlist_videos["nextPageToken"])
    next_page_token =  playlist_videos["nextPageToken"]

    while ('nextPageToken' in playlist_videos):
        print(next_page_token)
        next_page = get_playlist_video_id(youtube, upload_playlist_id, pageToken=next_page_token)
        playlist_videos['items'] = playlist_videos['items'] + next_page['items']
        if 'nextPageToken' not in next_page:
            playlist_videos.pop('nextPageToken', None)
        else:
            next_page_token = next_page['nextPageToken']
    for i in playlist_videos["items"]:
        print(i["contentDetails"]["videoId"])
    return playlist_videos


# Call the API's captions.list method to list the existing caption tracks.
def get_caption_id(youtube, video_id):

    results = youtube.captions().list(
        part="snippet",
        videoId=video_id
    ).execute()
    try:
        caption_id = results["items"][0]["id"]
        print(caption_id)
        return caption_id
    except:
        print("IndexError %s" % video_id)
        pass
    #   print(caption_id)
    #   return caption_id




# Call the API's captions.download method to download an existing caption track.
def download_caption(youtube, caption_id, tfmt):
    if caption_id is not None:



        subtitle = youtube.captions().download(
            id=caption_id,
            tfmt=tfmt
          ).execute()
  #print(subtitle.decode("utf-8"))
        return subtitle

def write_caption(path_name, object):
    if not os.path.exists(path_name):
        with open(path_name, "wb") as f:
            f.write(object)

if __name__ == "__main__":
    youtube = get_authenticated_service()
    try:
        upload_playlist_id = get_upload_playlist_id(youtube, channel_id)
        pages = collect_all_pages()
        for i in pages["items"]:
            print(i["contentDetails"]["videoId"])
            video_id = i["contentDetails"]["videoId"]
            transcript = download_caption(youtube, get_caption_id(youtube, video_id), 'ttml')
            write_caption("./transcripts/%s.xml" % video_id , transcript)


    #playlist_videos = get_playlist_video_id(youtube, upload_playlist_id)

    #transcript = download_caption(youtube, get_caption_id(youtube, video_id), 'ttml')

    #write_caption("scraped_file1", transcript)
    # download_caption(youtube, args.captionid, 'ttml') # sbv (plaintext) or ttml (xml)
      # use ttml (xml): parse it and get text + time start/end for each line
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
  else:
    print("done")
