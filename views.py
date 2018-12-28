from .spotify import Spotify, SpotifyScopes

import logging
import os

# Logging setup
logger = logging.getLogger('web.logger')

# Spotify client setup
SCOPES = [SpotifyScopes.USER_TOP_READ, SpotifyScopes.PLAYLIST_MODIFY_PUBLIC]
CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
spotify = Spotify(
        CLIENT_ID,
        CLIENT_SECRET,
        SCOPES
    )   


def index(request):
    """
    Render the home page.
    """
    return render(request, 'index.html')


def beats(request):
    """
    Render the Beats landing page.
    """
    if request.method == 'GET':
        return _handle_beats_get(request)
    else:
        return _handle_beats_post(request)


def _handle_beats_get(request):
    """
    Renders the login page.
    Generates the redirect URL and necessary query params for Spotify auth.
    """
    logger.info('/beats GET')
    auth_redirect_url, query_params = spotify.get_auth_redirect_url()
    context = {
        'auth_redirect_url': auth_redirect_url
    }
    context.update(query_params)
    logger.info(context)
    return render(request, 'beats.html', context=context)


def _handle_beats_post(request):
    logger.info('/beats POST')
    return render(request, 'beats_home.html')


def beats_callback(request):
    """
    Redirect here after the user has chosen to authorize.
    Receive the authorization code.
    If successful authorization - returns to the home screen, which renders the user's playlists.
    """
    logger.info("/beats/callback")
    auth_code = request.GET.get('code', None)
    if auth_code:       # successful authorization
        logger.info("access granted")

        token = spotify.get_access_token(auth_code)[0]
        user_id = spotify.get_user_id(token)
        playlist_ids = spotify.get_user_playlist_ids(token)     # gets the ids of the playlists
        playlists = []

        for playlist_id in playlist_ids:    # get a playlist of names of playlists for display
            playlists.append(spotify.get_playlist(token, user_id, playlist_id))


        return render(request, )

    else:               # access denied
        logger.info("access denied")
        return redirect('index')


