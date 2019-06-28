Spotify saver
=============

Reads your saved tracks and saves the albums they belong to.

# WARNING

**This is not currently working because of a [bug](https://github.com/spotify/web-api/issues/1284) with the Spotify Web API.**


Installation
============

To install dependencies:

    poetry install

Minimum version of `poetry` required is `0.12`.

Usage
=====

Set the necessary env vars, notice that the first is `SPOTIFY` with an F, the others `SPOTIPY`.

* SPOTIFY_USERNAME
* SPOTIPY_CLIENT_ID
* SPOTIPY_CLIENT_SECRET
* SPOTIPY_REDIRECT_URI

`SPOTIPY_REDIRECT_URI` can be `http://localhost/`.

Run the script and follow its instructions:

    python saver.py

You should see your Spotify library updated accordingly.
