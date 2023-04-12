import matplotlib.pyplot as plt
import mplcursors
import requests
import json

def getName(songId, headers):
	song_req_url = "https://api.spotify.com/v1/tracks/"
	return json.loads(requests.get(song_req_url + songId, headers=headers).text)['name']

def drawScatterPlot(songData, headers):

	data_dict = {}
	songDataRead = json.loads(songData)

	keysList = []
	i = 0

	for key in songDataRead['items'][0].keys():
		if isinstance(songDataRead['items'][0][key], (int, float)):
			keysList.append(key)
			print(i, key)
			i += 1

	while 1:
		featureX = input('x feature: ').strip()
		if featureX.isdigit():
			if int(featureX) <= len(keysList):
				featureX = keysList[int(featureX)]
				break
		elif featureX in keysList:
			break

	while 1:
		featureY = input('y feature: ').strip()
		if featureY.isdigit():
			if int(featureY) <= len(keysList):
				featureY = keysList[int(featureY)]
				break
		elif featureY in keysList:
			break

	highest_value_x = float('-inf')
	highest_id_x = None
	highest_value_y = float('-inf')
	highest_id_y = None
	lowest_value_x = float('inf')
	lowest_id_x = None
	lowest_value_y = float('inf')
	lowest_id_y = None

	for item in songDataRead['items']:
		x_val = item[featureX]
		y_val = item[featureY]
		data_dict[item['id']] = [x_val, y_val]

		# Update highest and lowest values for feature X
		if x_val > highest_value_x:
			highest_value_x = x_val
			highest_id_x = item['id']
		if x_val < lowest_value_x:
			lowest_value_x = x_val
			lowest_id_x = item['id']

		# Update highest and lowest values for feature Y
		if y_val > highest_value_y:
			highest_value_y = y_val
			highest_id_y = item['id']
		if y_val < lowest_value_y:
			lowest_value_y = y_val
			lowest_id_y = item['id']

	# Print highest and lowest values for feature X and Y
	print(f"Highest {featureX} \n  {getName(highest_id_x, headers)}\n  https://open.spotify.com/track/{highest_id_x} \n  value: {highest_value_x}")
	print(f"Lowest {featureX} \n  {getName(lowest_id_x, headers)}\n  https://open.spotify.com/track/{lowest_id_x} \n  value: {lowest_value_x}")
	print(f"Highest {featureY} \n  {getName(highest_id_y, headers)}\n  https://open.spotify.com/track/{highest_id_y} \n  value: {highest_value_y}")
	print(f"Lowest {featureY} \n  {getName(lowest_id_y, headers)}\n  https://open.spotify.com/track/{lowest_id_y} \n  value: {lowest_value_y}")


	x_values = [v[0] for v in data_dict.values()]
	y_values = [v[1] for v in data_dict.values()]

	# Find highest and lowest x y values
	max_x = max(x_values)
	min_x = min(x_values)
	max_y = max(y_values)
	min_y = min(y_values)

	# Define colors for highest and lowest values
	max_color = 'red'
	min_color = 'green'

	fig, ax = plt.subplots()
	points = ax.scatter(x_values, y_values)

	mplcursors.cursor(points, hover=True).connect("add", lambda sel: sel.annotation.set_text(f"{getName(list(data_dict.keys())[sel.index], headers)}\n{featureX}: {x_values[sel.index]}\n{featureY}: {y_values[sel.index]}"))


	for i in range(len(x_values)):
		if y_values[i] == max_y or x_values[i] == max_x:
			ax.scatter(x_values[i], y_values[i], color=max_color)
		elif y_values[i] == min_y or x_values[i] == min_x:
			ax.scatter(x_values[i], y_values[i], color=min_color)

	# Add labels and a title
	plt.xlabel(featureX)
	plt.ylabel(featureY)
	plt.title(f"{featureX} vs. {featureY}")

	# Display the plot
	plt.show()