__author__ = 'vinh.vo@sentifi.com'


from TwitterCaller import TwitterCaller

caller = TwitterCaller().caller
user = caller.get_user_timeline(screen_name='glorevenhite')

print user

