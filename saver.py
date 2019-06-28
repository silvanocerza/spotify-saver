import os
from typing import List

import spotipy
import spotipy.util as util


class Client:
    def __init__(self, *args, **kwargs):
        scopes = "user-library-read user-library-modify"
        username = os.environ.get("SPOTIFY_USERNAME")
        token = util.prompt_for_user_token(username, scope=scopes)
        self.client = spotipy.Spotify(auth=token)
        self.album_file = "album_ids"

    def current_user_saved_albums_contains(self, albums=None):
        return self.client._get("me/albums/contains?ids=" + ",".join(albums))

    def get_albums(self) -> List[str]:
        album_ids = []

        if os.path.isfile(self.album_file):
            with open(self.album_file) as f:
                album_ids = [i for i in f.readlines()]
            print("Ids read from file")
            return album_ids

        offset = 0
        limit = 50
        page = 1
        while True:
            print("Reading page", page)
            tracks = self.client.current_user_saved_tracks(offset=offset, limit=limit)

            for item in tracks.get("items"):
                album_ids.append(item["track"]["album"]["id"])

            offset += limit
            page += 1

            if tracks.get("next") is None:
                break

        self.write_to_file(album_ids)

    def write_to_file(self, album_ids: List[str]) -> None:
        # Write the album ids to file just to be sure
        with open(self.album_file, "w") as f:
            for i in album_ids:
                f.write(i)
                f.write("\n")

    def save_albums(self, album_ids: List[str]) -> None:
        mask = self.current_user_saved_albums_contains(album_ids)

        # Filter out those already saved in library and invert the result
        to_add = [i for i, m in zip(album_ids, mask) if not m]
        to_add = to_add[::-1]

        self.client.current_user_saved_albums_add(to_add)


if __name__ == "__main__":
    c = Client()

    albums = c.get_albums()
    c.save_albums(album_ids=albums)

