'''Retrieves the playlists of a Spotify user, selects a
specific playlist, retrieves the tracks of the selected 
playlist and their audio features, and stores them in a 
dictionary. If the selected playlist has not been 
previously saved, the function saves the dictionary as 
a JSON file in a specific directory and returns the filename.'''

# Import necessary libraries
import requests
import json
import os

# Define function to get all tracks features for a given playlist
def getPlTracksFeatures(headers):

	# Set URL for getting playlists
	playlist_url = "https://api.spotify.com/v1/me/playlists"

	# Send request to get playlists and get response
	requested = requests.get(playlist_url, headers=headers).text

	# Parse response as JSON
	full_request = json.loads(requested)

	selected_playlist = ''
	playlist_names_list = ['custom playlist (select to input URL)']
	playlist_name = ''
	i = 0

	print(i, playlist_names_list[0])

	i += 1

	# Iterate through each playlist and add its name to the list
	for item in full_request["items"]:
		playlist_names_list.append(item["name"])
		print(i, item["name"])
		i += 1

	# Ask user to select a playlist from the list
	while True:
		playlist_name = input('Select a playlist: ').strip()
		if playlist_name.isdigit():
			if int(playlist_name) < len(playlist_names_list):
				playlist_name = playlist_names_list[int(playlist_name)]
				break
		elif playlist_name in playlist_names_list:
			break

	custom = False
	if playlist_name == 'custom playlist (select to input URL)':
		custom = True
		custom_input = input('Input playlist URL: ').strip()
		if len(custom_input) == 22:
			playlist_name = custom_input
		elif 'spotify' in custom_input and 'playlist' in custom_input:
			playlist_name = custom_input[-22:]
		else:
			print('Input is not a valid playlist URL or ID')
			return

	print('\nLoading...\n')
	filename = playlist_name.replace(' ', '_')
	directory = './playlists/'

	if not os.path.isfile(os.path.join(directory, filename)):
		# Find the selected playlist and get its tracks URL
		if custom:
			selected_playlist = f"https://api.spotify.com/v1/playlists/{playlist_name}/tracks"
		else:
			for item in full_request["items"]:
				if item["name"] == playlist_name:
					selected_playlist = item["tracks"]["href"]
					break

		# Send request to get the tracks for the selected playlist and parse response as JSON
		requested2 = requests.get(selected_playlist, headers=headers).text
		full_request2 = json.loads(requested2)

		tracks_dictionary = {}

		# Loop through the tracks and add their names and IDs to the dictionary
		while True:
			for item in full_request2["items"]:
				tracks_dictionary[item["track"]["name"]] = item["track"]["id"]
			if full_request2["next"] is None:
				break
			requested2 = requests.get(full_request2["next"], headers=headers).text
			full_request2 = json.loads(requested2)


		audio_features_url = "https://api.spotify.com/v1/audio-features"
		tracks_features_list = {'items': []}

		# Break up playlist into chunks of 100 because of Spotify limit
		tracks = list(tracks_dictionary.values())
		for i in range(0, len(tracks), 100):
			chunk = tracks[i:i+100]
			tracks_str = ','.join(chunk)

			req_url = audio_features_url + "?ids=" + tracks_str
		
			request3 = requests.get(req_url, headers=headers).text
			full_request3 = json.loads(request3)

			for track in full_request3['audio_features']:
				tracks_features_list['items'].append(track)

		# Write the audio features to a file
		with open(directory + filename, 'w') as f:
			f.write(json.dumps(tracks_features_list))

	return directory + filename