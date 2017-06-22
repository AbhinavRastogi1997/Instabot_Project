import requests,urllib
Access_Token="3730820004.c61c48c.92fc2ab8afe1473389f9f9f0dc9f48b6"
Base_URL = "https://api.instagram.com/v1/"
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

        else:
            print("You do not have any posts at the moment.")

    else:
        print("Status code other than 200 was found.")







def start_bot():
    menu_choices=int(raw_input("What would you like to do?:\n 1.Get your own details. \n 2.Get the details of a user by username. \n 3.Get your own post"))

    if menu_choices==1:
        self_info()

    if menu_choices==2:
        username=raw_input("Enter the username of the about whom you want to get the info.")
        get_user_details(username)

    if menu_choices==3:
        get_own_post()


start_bot()
