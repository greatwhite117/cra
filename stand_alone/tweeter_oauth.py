# -*- coding: utf-8 -*-
"""
Created on Sun Jul 03 16:27:40 2016

@author: sspark
"""

from __future__ import absolute_import, print_function

import tweepy

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key='cciVC37i1f7zQ3ucGqIuDv2xh'
consumer_secret='dDzYkf95wu741aAC8Cwl3fKj7DLHfL5a9oAeWOBKGaGgag4nQg'

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="164612747-93EjyQQ7pCyEiU0Tl7rLKhCnIW0kSCEJjoDKFbLG"
access_token_secret='qajekc1r6ThOBgYRsZ1Ivz31cFxEsKriZxLolrurPsmnT'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print(api.me().name)


# If the application settings are set for "Read and Write" then
# this line should tweet out the message to your account's
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
api.update_status(status='Updating using OAuth authentication via Tweepy!')