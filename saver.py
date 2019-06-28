import os
from typing import List, Set

import spotipy
import spotipy.util as util


class Client:
    def __init__(self, *args, **kwargs):
        scopes = "user-library-read user-library-modify"
        username = os.environ.get("SPOTIFY_USERNAME")
        token = util.prompt_for_user_token(username, scope=scopes)
        self.client = spotipy.Spotify(auth=token)
        self.album_file = "album_ids"

    def current_user_saved_albums_contains(self, album_id: List[str]):
        return self.client._get(f"me/albums/contains?ids={','.join(album_id)}")

    def get_albums(self) -> Set[str]:
        album_ids = set()

        if os.path.isfile(self.album_file):
            with open(self.album_file) as f:
                print("Ids read from file")
                return [i.strip() for i in f.readlines()]

        offset = 0
        limit = 50
        page = 1
        while True:
            print("Reading page", page)
            tracks = self.client.current_user_saved_tracks(offset=offset, limit=limit)

            for item in tracks.get("items"):
                album_ids.add(item["track"]["album"]["id"])

            offset += limit
            page += 1

            if tracks.get("next") is None:
                break

        self.write_to_file(album_ids)

    def write_to_file(self, album_ids: Set[str]) -> None:
        # Write the album ids to file just to be sure
        with open(self.album_file, "w") as f:
            for i in album_ids:
                f.write(i)
                f.write("\n")

    def save_albums(self, album_ids: Set[str]) -> None:
        steps = 50
        for n in range(0, len(album_ids), steps):
            print(f"Saving albums from {n} to {n+steps}")
            ids = album_ids[n : n + steps]
            self.client.current_user_saved_albums_add(ids)


if __name__ == "__main__":
    c = Client()

    albums = c.get_albums()
    # Save albums in reverse order
    c.save_albums(album_ids=albums[::-1])

