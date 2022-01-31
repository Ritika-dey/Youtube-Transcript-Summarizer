from urllib import response
from flask import request
from flask import Flask
from youtube_transcript_api import YouTubeTranscriptApi  
from urllib.parse import urlparse, parse_qs 
from contextlib import suppress

app = Flask(__name__)

@app.route('/')
def hello():
    return "<p>Hello world</p>"

####################### api for summarizer  ######################################
@app.route('/api/summarize', methods = ['POST'])
def summarizetext(): 
    # getting URL from frontend
    url = request.json['video_url'] 

    # getting video ID from the URL
    video_id = get_video_id(url)
    
    # fetching transcript for the given video ID
    transcript = getTranscript(video_id)

    # fetching summary of the given transcript
    response = getSummarizedText(transcript)
    return response



#################### for getting summary #################################
def getSummarizedText(transcript):
    # do this
    # print(transcript)
    return transcript







#################### for getting transcript ######################################
def getTranscript(video_id):
    outputStr = ""
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en-IN'])
    
    for i in transcript:
        outputtxt = i['text']
        # print(outtxt)
        outputStr += outputtxt

    return outputStr






#################### function to get video ID from the URL  ######################################
def get_video_id(url, ignore_playlist=False):
    query = urlparse(url)

    # fetching video ID from different type of URLs
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com', 'music.youtube.com'}:
        if not ignore_playlist:
        # use case: get playlist id not current video in playlist
            with suppress(KeyError):
                return parse_qs(query.query)['list'][0]
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/watch/': return query.path.split('/')[1]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]

    # returns None for invalid YouTube url
    return None




##################### main function ###################################
if __name__ == '__main__':
    app.run(debug=True)