import subprocess

PIXIE_BOARDS_PASSWORD = "pixiepro"
COMMAND_OK_CALLBACK = "OK"
ENABLE_AT_COMMAND = "echo 'ATE1' | socat - /dev/ttyUSB2,cr"
SESSION_STATUS = "echo 'AT+QGPS?' | socat - /dev/ttyUSB2,cr | grep '+QGPS:'"
STOP_SESSION = "echo 'AT+QGPSEND' | socat - /dev/ttyUSB2,cr"
CONFIGURE_GPS_TRACKING = "echo 'AT+QGPS=1,30,50,0,1' | socat - /dev/ttyUSB2,cr"
GET_GPS_LOCATION = "echo 'AT+QGPSLOC?' | socat - /dev/ttyUSB2,cr"
GET_GPS_LOCATION_PRETTY = "echo 'AT+QGPSLOC=2' | socat - /dev/ttyUSB2,cr"


class PixieBoardGPSLocation():		

	def __init__(self):

		self.ModemStatus = ""

		self.UTCTime = ""
		self.Latitude = ""
		self.Longitude = ""
		self.HorizontalPrecision = ""
		self.Altitude = ""
		self.Fix = ""
		self.Cog = ""
		self.SpeedOverGroundKmH = ""
		self.SpeedOverGroundKnots = ""
		self.Date = ""
		self.NumberOfSatellites = ""


	def EnableATCommands(self, shell_command=ENABLE_AT_COMMAND):
		print(shell_command)
		(command_output, error) = self.SendShellCommand(shell_command)
		if self.ParseOKInMsg(command_output):
			return True, command_output, error
		else:
			return False, command_output, error

	def StopSession(self, shell_command=STOP_SESSION):
		sessionStatus, sessionOutput, sessionError = self.SessionStatus()
		if sessionStatus:
			(command_output, error) = self.SendShellCommand(shell_command)
			if self.ParseOKInMsg(command_output):
				return True, command_output, error
			else:
				return False, command_output, error
		else:
			return False, sessionOutput, sessionError

	def SessionStatus(self, shell_command=SESSION_STATUS):
		(command_output, error) = self.SendShellCommand(shell_command)
		if (str(command_output)[-4:-3]) == "1":
			return True, command_output, error
		else:
			return False, command_output, error


	def ConfigureGPSTracking(self, shell_command=CONFIGURE_GPS_TRACKING):
		(command_output, error) = self.SendShellCommand(shell_command)
		if self.ParseOKInMsg(command_output):
			return True, command_output, error
		else:
			return False, command_output, error

	def GetGPSLocation(self, shell_command=GET_GPS_LOCATION):
		(command_output, error) = self.SendShellCommand(shell_command)
		if self.ParseOKInMsg(command_output):
			self.ParseGPSLocation(command_output)
			return True, command_output, error
		else:
			return False, command_output, error

	def GetGPSLocationPretty(self, shell_command=GET_GPS_LOCATION_PRETTY):
		(command_output, error) = self.SendShellCommand(shell_command)
		if self.ParseOKInMsg(command_output):
			self.ParseGPSLocation(command_output)
			return True, command_output, error
		else:
			return False, command_output, error

	def SendShellCommand(self, shellCommand):
		command = subprocess.Popen([shellCommand], stdout=subprocess.PIPE, shell=True)
		(command_output, error) = command.communicate(PIXIE_BOARDS_PASSWORD)
		return command_output, error

	def ParseGPSLocation(self, command_output):
		locationData = str(command_output).split(",")
		self.UTCTime = locationData[0][30:]
		self.Latitude = locationData[1]
		self.Longitude = locationData[2]
		self.HorizontalPrecision = locationData[3]
		self.Altitude = locationData[4]
		self.Fix = locationData[5]
		self.Cog = locationData[6]
		self.SpeedOverGroundKmH = locationData[7]
		self.SpeedOverGroundKnots = locationData[8]
		self.Date = locationData[9]
		self.NumberOfSatellites = locationData[10][0:2]

	def ParseOKInMsg(self, command_output):
		output = str(command_output)
		if COMMAND_OK_CALLBACK in output:
			return True
		else:
			return False


