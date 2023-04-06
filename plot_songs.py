import matplotlib.pyplot as plt
import json

def drawScatterPlot(songData):

	data = []
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
	lowest_value_y = float('inf') # added lowest value initialization for feature Y
	lowest_id_y = None # added lowest value initialization for feature Y

	for item in songDataRead['items']:
		data.append([item[featureX], item[featureY]])

		# Update highest and lowest values for feature X
		value_x = item[featureX]
		if value_x > highest_value_x:
			highest_value_x = value_x
			highest_id_x = item['id']
		if value_x < lowest_value_x:
			lowest_value_x = value_x
			lowest_id_x = item['id']

		# Update highest and lowest values for feature Y
		value_y = item[featureY]
		if value_y > highest_value_y:
			highest_value_y = value_y
			highest_id_y = item['id']
		if value_y < lowest_value_y:
			lowest_value_y = value_y
			lowest_id_y = item['id']

	# Print highest and lowest values for feature X and Y
	print(f"Highest {featureX} is \nhttps://open.spotify.com/track/{highest_id_x} \n  value: {highest_value_x}")
	print(f"Lowest {featureX} is \nhttps://open.spotify.com/track/{lowest_id_x} \n  value: {lowest_value_x}")
	print(f"Highest {featureY} is \nhttps://open.spotify.com/track/{highest_id_y} \n  value: {highest_value_y}")
	print(f"Lowest {featureY} is \nhttps://open.spotify.com/track/{lowest_id_y} \n  value: {lowest_value_y}")


	x_values = [d[0] for d in data]
	y_values = [d[1] for d in data]

	plt.scatter(x_values, y_values)

	# Add labels and a title
	plt.xlabel(featureX)
	plt.ylabel(featureY)
	plt.title(f"{featureX} vs. {featureY}")

	# Display the plot
	plt.show()