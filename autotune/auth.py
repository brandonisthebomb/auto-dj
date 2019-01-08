from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app as app
from autotune.spotify.spotify_client import SpotifyClient, SpotifyScopes
import logging
import urllib

"""
Handles all auth-flow functionality.
"""
host_url = 'https://ce86d44b.ngrok.io'

auth = Blueprint('auth', __name__, url_prefix='/auth')

spotify_client_id = '1947ba3899b7455db58b313fdc32a212'
spotify_client_secret = '4766707613ce49c9be37f20a6ba508ee'

scopes = [SpotifyScopes.USER_TOP_READ, SpotifyScopes.PLAYLIST_MODIFY_PUBLIC]
spotify = SpotifyClient(spotify_client_id, spotify_client_secret, scopes)

@auth.route('/', methods=('GET', 'POST'))
def authenticate():
   app.logger.info('%s GET' % request.path)
   auth_redirect_url = host_url + url_for('.callback') 
   app.logger.debug('Authentication redirect URL: %s' % auth_redirect_url)
   auth_url = spotify.get_auth_request(auth_redirect_url)
   return redirect(auth_url)

@auth.route('/callback', methods=('GET'))
def callback():
   if request.method == 'GET': 
      app.logger.info('%s GET' % request.path)
      try:
         auth_code = request.args['code']
         app.logger.debug('Auth code: %s' % auth_code)
         auth_redirect_url = host_url + url_for('.callback') 
         access_token, refresh_token = spotify.get_access_token(auth_code, auth_redirect_url)
         app.logger.debug('Spotify access token: %s, refresh token: %s' % (access_token, refresh_token))
      except Exception as e:
         app.logger.error('Exception in callback %s' % str(e))
   return 'This is the callback endpoint!'