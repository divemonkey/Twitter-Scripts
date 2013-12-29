import oauth2 as oauth
import urllib2 as urllib
import json

access_token_key = ""
access_token_secret = ""

consumer_key = ""
consumer_secret = ""

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"

http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def getfriends():
  users = []
  cursor = "cursor=-1"
  call_count = 1
  while cursor !=  "cursor=0":
    if call_count == 15:
      print "**** I had to break because I made 15 calls ****"
      break
    response = makerequest(cursor)
    for line in response:
      stripped = line.strip()
    jsonresponse =  json.loads(stripped)
    #print jsonresponse
    userlist = jsonresponse["users"]
    for user in userlist:
      users.append(user["screen_name"])
    #print jsonresponse["next_cursor_str"]
    cursor = "cursor=" + jsonresponse["next_cursor_str"]
    call_count += 1
  for user in users:
    print user

def makerequest(cursor):
  url = "https://api.twitter.com/1.1/friends/list.json?include_user_entities=false&" + cursor
  print url
  parameters = []
  response = twitterreq(url, "GET", parameters)
  return response

if __name__ == '__main__':
  getfriends()
