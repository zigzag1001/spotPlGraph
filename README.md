# spotPlGraph
Loads tracks from playlist and visualises two selected track features on an x/y graph

![graph example](https://i.ibb.co/7y8CHrK/example.png)

---
## Req's
`pip install matplotlib mplcursors`

## Usage
1. Create an app with spotify api [here](https://developer.spotify.com/dashboard)
2. Click settings in the top right
3. Run main.py and paste in the client id, secret, and redirect uri
4. Select playlist, you can use numbers
5. Select x and y features, explanations [here](https://developer.spotify.com/documentation/web-api/reference/get-several-audio-features)
6. A graph will appear, hover over points to see name, values
7. Min and max values will be printed to console
