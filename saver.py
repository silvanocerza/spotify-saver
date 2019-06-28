import spotipy
import spotipy.util as util

if __name__ == "__main__":
    import os

    scopes = "user-library-read user-library-modify"
    username = os.environ.get("SPOTIFY_USERNAME")
    token = util.prompt_for_user_token(username, scope=scopes)

    client = spotipy.Spotify(auth=token)
    offset = 0
    limit = 50
    page = 1

    album_ids = []

    while True:
        print("Reading page", page)
        tracks = client.current_user_saved_tracks(offset=offset, limit=limit)

        for item in tracks.get("items"):
            album_ids.append(item["track"]["album"]["id"])

        offset += limit
        page += 1

        if tracks.get("next") is None:
            break

    # Write the album ids to file just to be sure
    with open("album_ids", "w") as f:
        for id in album_ids:
            f.write(id)
            f.write("\n")

    client.current_user_saved_albums_add(albums=album_ids[::-1])

