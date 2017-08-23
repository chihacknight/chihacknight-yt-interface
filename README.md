# chihacknight-yt-scraper

Chi Hack Night Youtube captions scraper/search interface

## Scraper installation

*set up virtual environment:*

* sudo pip install virtualenv
* virtualenv venv
* source venv/bin/activate

*install dependencies:*

* pip install -r requirements.txt

*start using*

* Download your `client_secrets.json`
* Run testscrape.py, authenticate, follow instructions

## Relevant YouTube API functions

### How to Get Transcripts


* Find the channel ID (an easy way is to visit the channel on YouTube and look at the URL)
** For each channel we have playlists, there is a related playlist called 'uploads' that lists all video uploaded by that channel
* [Find the playlist ID of the upload playlist for your channel](https://developers.google.com/youtube/v3/docs/channels/list#try-it)
* [Get the list of uploaded videos by using the playlistItems endpoint with the playlist ID you just found](https://developers.google.com/youtube/v3/docs/playlistItems/list#try-it)

* for each video we have subtitles
* subtitles can be downloaded and parsed, we chose an xml format

## Web interface installation
