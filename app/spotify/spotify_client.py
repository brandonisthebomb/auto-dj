"""
A simple, lightweight Spotify client for Python.

Created by Brandon Liu - brandon@virginia.edu
"""

import requests
import logging
import os

from enum import Enum

logger = logging.getLogger(__name__)

class SpotifyClient:

	# URLs
	API_URL = 'https://api.spotify.com'
	AUTH_URL = 'https://accounts.spotify.com'
	#REDIRECT_URL = 'https://' + os.environ['HOST'] + '/beats/callback' # ngrok host for development

	# Endpoints
	AUTH_ENDPOINT = 'authorize'
	TOKEN_ENDPOINT = 'api/token'

	# Response Formats
	DEFAULT_RESPONSE_TYPE = 'json'
	AUTH_RESPONSE_TYPE = 'code'

	# Grant Types
	AUTH_GRANT = "authorization_code"
	REFRESH_GRANT = 'refresh_token'

	def __init__(self, client_id, client_secret, scopes):
		"""
		:param client_id: spotify client id string	
		:param client_secret: spotify client secret string	
		:param scopes: a list of scope strings to grant	
		"""
		self.client_id = client_id
		self.client_secret = client_secret
		self.scopes = scopes

	def get_auth_request(self, redirect_url):
		"""
		Gets the Spotify authentication url and parameters so that the user can 
		approve scopes and permissions. If authentication is successful, Spotify
		then makes a request to the redirect url with the access token as a query
		parameter.
		:param redirect_url: the page to go to after authentication that must 
		accept authentication query parameters from Spotify. 
		:return: the Spotify url string and a dict of query params to send. 
		"""
		query_params = {
			'client_id': self.client_id,
			'response_type': self.AUTH_RESPONSE_TYPE,
			'redirect_uri': redirect_url,
			'scope': ' '.join(scope.value for scope in self.scopes),
			'show_dialog': 'true'
		}
		url = self._generate_request_url(self.AUTH_URL, self.AUTH_ENDPOINT)
		logger.info("Authentication redirect url: %s" % url)
		return url, query_params

	def get_access_token(self, auth_code, redirect_url):
		"""
		Gets the Spotify API access token required for making API calls, as well as the permanent
		refresh token. The redirect_uri here is just for verification and doesn't actually
		do anything.
		:param auth_code: the auth code received from Spotify.
		:return: the access token and the refresh token
		"""
		url = self._generate_request_url(self.AUTH_URL, self.TOKEN_ENDPOINT)
		query_params = {
			'client_id': self.client_id,
			'client_secret': self.client_secret, 
			'grant_type': self.AUTH_GRANT,
			'code': auth_code,
			'redirect_uri': redirect_url
		}

		response = requests.post(url, query_params).json()

		access_token = response['access_token']
		logger.info('access token: %s', access_token)

		refresh_token = response['refresh_token']
		logger.info('refresh token: %s', refresh_token)

		return response['access_token'], response['refresh_token']

	def refresh_access_token(self, refresh_token):
		"""
		gets a new Spotify API access token
		:param refresh_token: a refresh token
		:return: the next access token
		"""
		url = self._generate_request_url(self.AUTH_URL, self.TOKEN_ENDPOINT)
		query_params = {
			'client_id': self.client_id,
			'client_secret': self.client_secret,
			'grant_type': self.REFRESH_GRANT,
			'refresh_token': refresh_token
		}
		response = requests.post(url, query_params).json()
		access_token = response['access_token']
		logger.info('refreshed access token: %s', access_token)
		return access_token
								
	def get_user_id(self, access_token):
		"""
		GET current users' Spotify ID
		:param access_token:
		:return: string with the user's Spotify ID
		"""
		url = self.API_URL + '/v1/me'
		headers = {
			'Authorization': 'Bearer ' + access_token
		}

		response = requests.get(url, headers=headers).json()

		return response['id']

	def get_user_playlist_ids(self, access_token, limit=50, offset=0):
		"""
		GET current users' playlists
		:param access_token:
		:param limit:
		:param offset:
		:return: a list of playlist ID strings
		"""
		url = self.API_URL + '/v1/me/playlists'
		headers = {
			'Authorization': 'Bearer ' + access_token
		}
		query_params = {
			'limit': limit,
			'offset': offset
		}

		response = requests.get(url, params=query_params, headers=headers).json()
		json_items = response['items']
		playlists = [json_playlist['id'] for json_playlist in json_items]
		logger.info("got user's playlists: %s", playlists)
		return playlists

	def get_playlist(self, access_token, user_id, playlist_id):
		"""
		GET a single playlist
		:param access_token:
		:param user_id:
		:param playlist_id:
		:return: a playlist object
		"""
		url = self.API_URL +  str.format('/v1/users/%s/playlists/%s', user_id, playlist_id)
		headers = self._generate_auth_headers(access_token)
		response = requests.get(url, headers=headers).json()
		# playlist =
		return None

	def _generate_request_url(self, url, endpoint):
		return '%s/%s' % (url, endpoint)

	def _generate_auth_headers(self, access_token):
		return {
			'Authorization': 'Bearer' + access_token
		}



class SpotifyScopes(Enum):
	NO_SCOPE = '-'
	STREAMING = 'streaming'
	PLAYLIST_READ_PRIVATE = 'playlist-read-private'
	PLAYLIST_READ_COLLABORATIVE = 'playlist-read-collaborative'
	PLAYLIST_MODIFY_PRIVATE = 'playlist-modify-private'
	PLAYLIST_MODIFY_PUBLIC = 'playlist-modify-public'
	USER_LIBRARY_READ = 'user-library-read'
	USER_READ_RECENTLY_PLAYED = 'user-read-recently-played'
	USER_TOP_READ = 'user-top-read'