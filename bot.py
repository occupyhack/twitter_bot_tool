#could use an threaded Timer from the Timer class to run this on an interval
#every 60 seconds, or could have it make the calls every 60 seconds if the timer has not yet expired, this is more manual and ugly code-wise, but prevents possible overlapping calls to users

import time, twitter, urllib, urllib2, json

httptime = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())

#all this oauth stuff now required by twitter, python-twitter uses this fine
client = twitter.Api(consumer_key='', consumer_secret='',access_token_key='',access_token_secret='')

#should be able to safely store a followerList in memory, each follower = 64 bytes
followerList = {}
followers = client.GetFriends()

#creating the initial follower list, any successful DM will add the user to this list
#one distinction used throughout is that Twitter user/message objects are not dictionaries, but can be converted into them if necessary
for f in followers:
	followerList[f.id] = f

interval = 30 
lastuserid = 0
lastmessageid = 0
count = 0
url = 'http://www.google.com'

while 1:
	start  = time.time()
	mentions = client.GetReplies(since_id=lastuserid)
	for m in mentions:
		userid = m.user.id 
		print followerList
		if not(userid in followerList):
			try:
				client.PostDirectMessage(user=userid,text='')
				followerList[userid] = m.user
				client.CreateFriendship(user=userid)	
			except:
				print "message send failed, user is not following us"
		lastuserid = m.id

	if lastmessageid == 0:
		print "using since time"
		messages = client.GetDirectMessages(since=httptime)
	else:
		messages = client.GetDirectMessages(since_id=lastmessageid)
	for m in messages:
		print m
		address = m.text
		data["q"] = address
		edata = urllib.urlencode(data)
		response = json.load(urllib2.urlopen(url+edata))
		print response
		if len(response["locations"]) <= 0:
			reply = "Sorry, could not find a data for this location"
		else:
			location = response["locations"][0]
			address = location["address"]
			reply = str('')#parsed data from address
		try:
			status = client.PostDirectMessage(user=m.sender_id,text=reply)
			lastmessageid = m.id
		except:
			continue
	
	time.sleep(count)
	end = time.time()
	processtime = end-start
	pause = interval - processtime
	if pause > 0:
		time.sleep(pause)
	else: #right now if this is getting too many messages, it will stop. This should eventually be removed since this will just call twitter again if it is over the time limit 
		break
