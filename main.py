from get_spot_access_token import getAccessToken
from get_pl_tracks_feat import getPlTracksFeatures
from plot_songs import drawScatterPlot

headers = getAccessToken()

filename = getPlTracksFeatures(headers)

with open(filename, 'r') as f:
	drawScatterPlot(f.read())