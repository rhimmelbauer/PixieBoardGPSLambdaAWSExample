from PixieBoardGPSLocation import PixieBoardGPSLocation
import requests, json

LOGGING_MSG_EXP_PING_TIMOUT = "Time Out"
LOGGING_MSG_EXP_REQUEST_EXCEPTION = "Request Exception"
LOGGING_MSG_EXP_HTTP_ERROR = "HTTPError: "
LOGGING_MSG_EXP_CONN_ERROR = "ConnectionError: "

API_GATEWAY = "https://k2j1e9ygt0.execute-api.us-west-1.amazonaws.com/prod/storelocation"

PIXIE_BOARD_ID = 117

def setLocationServer(pixieboard_id, lat, lng):
	try:
		response = requests.get(SERVER + SET_LOCATION + str(pk) + "/" + str(lat) + "/" + str(lng))
	except requests.exceptions.Timeout:
		print(LOGGING_MSG_EXP_PING_TIMOUT)
	except requests.exceptions.RequestException as e:
		print(LOGGING_MSG_EXP_REQUEST_EXCEPTION + "%s",e)
	except requests.exceptions.HTTPError as err:
		print(LOGGING_MSG_EXP_HTTP_ERROR + "%s",err)
	except requests.exceptions.ConnectionError as err:
		print(LOGGING_MSG_EXP_CONN_ERROR + "%s",err)



if __name__ == "main":
