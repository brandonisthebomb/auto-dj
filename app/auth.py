from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from app.spotify.spotify_client import SpotifyClient, SpotifyScopes

"""
Handles all auth-flow functionality.
"""

auth = Blueprint("auth", __name__, url_prefix="/auth")

spotify_client_id = ""
spotify_client_secret = ""

scopes = [SpotifyScopes.USER_TOP_READ, SpotifyScopes.PLAYLIST_MODIFY_PUBLIC]
spotify = SpotifyClient(spotify_client_id, spotify_client_secret, scopes)

@auth.route("/", methods=("GET", "POST"))
def authenticate():
   auth_url = spotify.get_auth_redirect_url
   return "This is the authentication endpoint!"

@auth.route("/callback", methods=("GET", "POST"))
def callback():
    return "This is the callback endpoint!"