import datetime
from flask import Flask, render_template, jsonify, Response, request


app = Flask(__name__)

@app.route('/')
def index_view():
    username = request.args.get('username')
    userstring = str(username)   #username is of nonetype
    with open('./users.json','r') as f:
        Users = f.readlines()
        followArray=[]
        for i in range(len(Users)):   #generating an array of all users that we follow
                if (Users[i].find(userstring) > 0 and Users[i].find(userstring) < 10):
                    Following = Users[i][Users[i].find("[")+1:Users[i].find("]")]
                    Following = Following.replace(" ","")
                    Following = Following.replace("\"","")
                    followArray = Following.split(",")
                    break
    timeline = []
    if len(followArray)!=0:  #Ensures that we only execute this code when we are trying to generate a users timeline
        with open('./posts.json','r') as g:
            Posts = g.readlines()
            k=0
            while k < len(Posts):
                if Posts[k].find("\"") ==-1: #We want to skip over lines that don't contain names or tweets
                    k=k+1
                    continue
                else:
                    temp = Posts[k][Posts[k].find("\"")+1:Posts[k].find("\"",Posts[k].find("\"")+1)]
                    if temp in followArray:
                        k=k+1
                        while Posts[k-1].find("]") == -1: #Adding all tweets and times to a timeline array after checking that we follow that person
                            tweet = temp+": "+ Posts[k][Posts[k].find(":")+2: Posts[k].find(",")]+"       "
                            timeline.append(tweet)
                            timeline.append(Posts[k+1][Posts[k+1].find("\"")::].replace("\"",""))
                            k=k+3
                    else:
                        k=k+1
                        continue
            for l in range(1,len(timeline)-2,2): #Comparison method to ensure that tweets on our timeline are ordered from newest to oldest
                for m in range(l+2,len(timeline),2):
                    d1 = timeline[l][timeline[l].find(":")+2:timeline[l].find("T")]
                    t1 = timeline[l][timeline[l].find("T")+1:timeline[l].find("Z")]
                    d2 = timeline[m][timeline[m].find(":")+2:timeline[m].find("T")]
                    t2 = timeline[m][timeline[m].find("T")+1:timeline[m].find("Z")]
                    year1, month1, day1 = [int(x) for x in d1.split('-')]
                    hour1, minute1,second1 = [int(y) for y in t1.split(':')]
                    year2, month2, day2 = [int(v) for v in d2.split('-')]
                    hour2, minute2,second2 = [int(w) for w in t2.split(':')]
                    dt1= datetime.datetime(year1,month1,day1,hour1,minute1,second1)
                    dt2= datetime.datetime(year2,month2,day2,hour2,minute2,second2)
                    if dt1<dt2:
                        temptweet = timeline[l-1]
                        temptime = timeline[l]
                        timeline[l-1]= timeline[m-1]
                        timeline[l]=timeline[m]
                        timeline[m-1]= temptweet
                        timeline[m]=temptime

    return render_template('index.html', username = username, timeline = timeline)

@app.route('/users')
def users_view():
    with open('./users.json', 'r') as f:
        users = f.read()
    return Response(users, mimetype="application/json")

@app.route('/posts')
def posts_view():
    with open('./posts.json', 'r') as f:
        posts = f.read()
    return Response(posts, mimetype="application/json")

if __name__ == '__main__':
    app.run(host='127.0.0.1')
