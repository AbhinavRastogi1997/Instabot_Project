import requests,urllib,googlemaps
API_KEY="AIzaSyAWPbciqG7n3pDhxPV0Twdg7bHWtAuct8M"
Access_Token="5629236876.1cc9688.86db895c038043b5960dc2949785299a"
Base_URL = "https://api.instagram.com/v1/"
Base_URL2="https://maps.googleapis.com/maps/api/geocode/json"
print("Hello!")
print("Welcome to Instabot!")
print("Let's Get Started!!")

def self_info():
    request_url=(Base_URL+"users/self/?access_token=%s")%(Access_Token)
    print "Get Request Url: %s"%(request_url)
    my_info=requests.get(request_url).json()

    if my_info['meta']['code']==200:
        if len(my_info['data']):
            print("Username : %s"%(my_info['data']['username']))
            print("No. of followers : %s"%(my_info['data']['counts']['followed_by']))
            print("People I follow : %s"%(my_info['data']['counts']['follows']))
            print("No. of posts : %s"%(my_info['data']['counts']['media']))

        else:
            print("User does not exist.")

    else:
        print("Status Code other that 200 was received.")

def get_user_id(username):
    request_url=Base_URL+"users/search?q=%s&access_token=%s"%(username,Access_Token)
    print("Get request URL : %s"%(request_url))
    id = requests.get(request_url).json()

    if id['meta']['code']==200:
        if len(id['data']):
            return id['data'][0]['id']

        else:
            return None

    else:
        print"Status Code other than 200 was found."
        exit()


def get_user_details(username):
    user_id=get_user_id(username)
    if user_id == None:
        print("The user does not exist.")
        exit()
    request_url = Base_URL+'users/%s/?access_token=%s'%(user_id,Access_Token)

    print("GET request url : %s"%(request_url))
    user_info = requests.get(request_url).json()

    if user_info['meta']['code']==200:
        if len(user_info['data']):
            print("Username : %s"%(user_info['data']['username']))
            print("No. of Followers : %s"%(user_info['data']['counts']['followed_by']))
            print("People he/she follows : %s"%(user_info['data']['counts']['follows']))
            print("No. of posts : %s"%(user_info['data']['counts']['media']))

        else:
            print("The user does not exist.")

    else:
        print("Status code other than 200 was received. ")


def get_own_post():
    request_url=Base_URL+'users/self/media/recent/?access_token=%s'%(Access_Token)
    print("Get request url : %s"%(request_url))
    my_media = requests.get(request_url).json()

    if my_media['meta']['code']==200:
        if len(my_media['data']):
            img_name=my_media['data'][0]['id']+'.jpeg'
            img_url=my_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_url,img_name)
            print("Your image has been downloaded.")
            return my_media['data'][0]['id']


        else:
            print("You do not have any posts at the moment.")

    else:
        print("Status code other than 200 was found.")

def get_user_post(username):
    user_id=get_user_id(username)
    if user_id==None:
        print("User does not exist")
        exit()

    request_url=Base_URL+"users/%s/media/recent/?access_token=%s"%(user_id,Access_Token)
    print("Get request url : %s"%(request_url))
    user_media=requests.get(request_url).json()

    if user_media['meta']['code']==200:
        if len(user_media['data']):
            img_name=user_media['data'][0]['id']+".jpeg"
            img_url=user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_url,img_name)

            print("The image has been downloaded.")

            return user_media['data'][0]['id']
        else:
            print("There are no posts.")

    else:
        print("Status code other than 200 was received.")

def get_media_id(username):
    user_id=get_user_id(username)
    if user_id==None:
        print("The user does not exist")
        exit()

    request_url= Base_URL+'users/%s/media/recent/?access_token=%s'%(user_id,Access_Token)
    print("GET request URL : %s"%(request_url))
    media_id=requests.get(request_url).json()

    if media_id['meta']['code']==200:
        if len(media_id['data']):
            return media_id['data'][0]['id']

        else:
            print("There are no posts.")
            exit()

    else:
        print("Status code other than 200 was received. ")


def get_like_list(username):

    media_id=get_media_id(username)

    if media_id==None:
        print("There are no posts.")
        exit()

    request_url=Base_URL+"media/%s/likes?access_token=%s"%(media_id,Access_Token)
    print("GET request URL : %s"%(request_url))
    likes=requests.get(request_url).json()

    if likes['meta']['code']==200:
        if len(likes['data']):
            print("This post has been liked by the following users")
            i=0
            for item in likes['data']:
                print(str(likes['data'][i]['username']))
                i=i+1
        else:
            print("This post has no likes.")

    else:
        print("Status code other than 200 was received.")

def like_a_post(username):
    media_id=get_media_id(username)
    request_url=Base_URL+"media/%s/likes"%(media_id)

    payload={"access_token":Access_Token}
    print("POST request url : %s" % (request_url))
    like_post = requests.post(request_url,payload).json()

    if like_post['meta']['code']==200:
        print("Your like was successful!")

    else:
        print("Your like was unsuccessful!")

def list_of_comments(username):
    media_id=get_media_id(username)

    if media_id==None:
        print("There are no posts.")
        exit()

    request_url=Base_URL+"media/%s/comments?access_token=%s"%(media_id,Access_Token)
    print("POST request URL : %s"%(request_url))
    comment_list=requests.get(request_url).json()

    if comment_list['meta']['code']==200:
        if len(comment_list['data']):
            i=0;
            for items in comment_list['data']:
                print("Comment: %s By:  %s"%(comment_list['data'][i]['text'],comment_list['data'][i]['from']['username']))
                i=i+1

        else:
            print("There are no comments on this post.")

    else:
        print("Status code other than 200 was received.")

def comment_on_post(username):

    media_id=get_media_id(username)
    if media_id==None:
        print("There are no posts")
        exit()

    request_url=Base_URL+"media/%s/comments"%(media_id)
    comment_text=raw_input("Enter your comment")
    payload={"access_token":Access_Token,"text":comment_text}
    print("POST request URL : %s"%(request_url))
    post_comment=requests.post(request_url,payload)

    if post_comment.status_code==200:
        print("Comment was successfully added!")

    else:
        print("Comment could not be added! Try again!")

def analyse_the_geographical_coordinate():
    address=raw_input("Enter the location:")
    request_url = Base_URL2+"?address=%s&key=%s"%(address,API_KEY)
    print("GET request URL : %s"%(request_url))
    location=requests.get(request_url).json()

    Latitude=location['results'][0]['geometry']['location']["lat"]
    Longitude=location['results'][0]['geometry']['location']["lng"]
    print("Latitude:%s"%(Latitude))
    print("Longitude:%s"%(Longitude))

    req_url=Base_URL+"locations/search?lat=%s&lng=%s&access_token=%s"%(Latitude,Longitude,Access_Token)
    print("GET request URL : %s"%(req_url))
    location_info=requests.get(req_url).json()

    for item in range(0,len(location_info['data'])):
        id=location_info['data'][item]['id']
        REQUEST_URL=Base_URL+"locations/%s/media/recent?access_token=%s"%(id,Access_Token)
        location_media=requests.get(REQUEST_URL).json()
        if location_media['meta']['code']==200:
            if len(location_media['data']):
                if location_media['data'][0]['tags'].Upper()=="Earthquake":
                    print("Detected! Natural Calamity:Earthquake")
                elif location_media['data'][0]['tags'].Upper()=="Floods":
                    print("Detected! Natural Calamity:Flood")
                elif location_media['data'][0]['tags'].Upper()=="Drought":
                    print("Detected! Natural Calamity:Drought")
                elif location_media['data'][0]['tags'].Upper()=="Landslide":
                    print("Detected! Natural Calamity:Landslide")
                elif location_media['data'][0]['tags'].Upper()=="Tsunami":
                    print("Detected! Natural Calamity:Tsunami")
                else:
                    print("No Natural Calamity was detected at this place")

            else:
                print("There are no posts for thi sparticular location")

        else:
            print("Status code other than 200 was received!")




def start_bot():
    menu_choices=int(raw_input("What would you like to do?:\n 1.Get your own details. \n 2.Get the details of a user by username. \n 3.Fetch your own post \n 4.Fetch your friend's post. \n 5.Get like list \n 6.Like the post of a user \n 7.Get the list of comments on the recent post of a user \n 8.Comment on a user's post \n 9. Analyse various geographical coordinates and check whether a natural calamity took place in that region." ))

    if menu_choices==1:
        self_info()

    if menu_choices==2:
        username=raw_input("Enter the username of the about whom you want to get the info.")
        get_user_details(username)

    if menu_choices==3:
        my_post_id=get_own_post()
        print("The ID of the most recent post is %s"%(my_post_id))

    if menu_choices==4:
         username=raw_input("Enter the username")
         user_post_id=get_user_post(username)
         print("The ID of the most recent post shared by your friend is %s"%(user_post_id))

    if menu_choices==5:
        username = raw_input("Enter the username:")
        get_like_list(username)

    if menu_choices==6:
        username=raw_input("Enter the username:")
        like_a_post(username)

    if menu_choices==7:
        username=raw_input(("Enter the username:"))
        list_of_comments(username)

    if menu_choices==8:
        username=raw_input("Enter the username")
        comment_on_post(username)

    if menu_choices==9:
        analyse_the_geographical_coordinate()
start_bot()
