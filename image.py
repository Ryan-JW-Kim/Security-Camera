from datetime import date, datetime
import time
import os
import sys
import mediapipe 
import cv2

class LogSession:

	def __init__(self):

		self._date = f"{date.today().day}-{date.today().month}-{date.today().year}"

	def _time_str(self):

		return f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"

	def _log_line(self, line):
		
		if os.path.isdir(self._date) == False:
			os.mkdir(self._date)

		working_dir = f"{self._date}/log.txt"

		with open(working_dir, "a") as fh:
			fh.write(line)

	def _save_image(self, frame):

		working_dir = f"{self._date}/images"

		if os.path.isdir(working_dir) == False:
			os.mkdir(working_dir)

		cv2.imwrite(f"{working_dir}/{self._time_str()}.jpg", frame)

	def _check_date_change(self):

		split = self._date.split("-")
		day_changed = False

		if date.today().day != split[0]:
			day_changed = True

		return day_changed

pose = mediapipe.solutions.pose
capture = cv2.VideoCapture(0)

Log = LogSession()

with pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.5) as pose:

	while capture.isOpened():

		time.sleep(5)

		ret, frame = capture.read()

		cv2.imshow("Project", frame)

		image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

		results = pose.process(image)

		if results.pose_landmarks != None:

			if Log._check_date_change() == True:
				Log = LogSession()

			Log._log_line(f"{Log._time_str()}\n")
			Log._save_image(frame)

		if cv2.waitKey(25) & 0xFF == ord("q"):
			break

capture.release()
cv2.destoyAllWindows()