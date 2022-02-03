import os

SS = "\\"
NEW_LINE = "\n"
SRC_FOLDER = "RawData"
RESULTS_HEAD = "eh_heads"
RESULTS_GAZE = "gaze"
UNIT = "unit"
COOR = "coordinate"
TASKS = 4 + 1  # The actual count is 4 but for boundary reasons added +1
VIDEOS = 15 + 1
USERS = 30 + 1
FOLDERS = []


def process(file_path):
	first_line = True
	start = 0
	with open(SRC_FOLDER + SS + file_path) as f:
		file_path = file_path.split(".")[0]
		head_file = open(RESULTS_HEAD + SS + file_path, "w")
		gaze_file_unit = open(RESULTS_GAZE + SS + UNIT + SS + file_path, "w")
		gaze_file_coor = open(RESULTS_GAZE + SS + COOR + SS + file_path, "w")
		lines = f.readlines()
		for line in lines:
			line = line.replace(NEW_LINE, '').split()
			pts = int(line[0])
			if first_line:
				first_line = False
				start = pts
				pts = 0
			else:
				pts -= start
			h_x, h_y = line[2:4]
			g_x_uint, g_y_unit = line[4:6]
			g_x_coor, g_y_coor = line[6:]
			pts = str(pts)
			head_file.write(' '.join([pts, h_x, h_y, str(0)]) + NEW_LINE)
			gaze_file_unit.write(' '.join([pts, g_x_uint, g_y_unit]) + NEW_LINE)
			gaze_file_coor.write(' '.join([pts, g_x_coor, g_y_coor]) + NEW_LINE)


def create_file_name(user, video, task):
	return "User_" + f"{user:02d}" + "_Video_" + f"{video:02d}" + "_Task_" + str(task) + ".txt"


def start():
	user = 0
	while user < USERS:
		for video in range(1, VIDEOS):
			if video % 3 == 1:
				user += 1
				if user == USERS:
					break
			for task in range(1, TASKS):
				file = create_file_name(user, video, task)
				process(file)


def init():
	try:
		os.makedirs(RESULTS_HEAD)
		os.makedirs(RESULTS_GAZE)
		os.makedirs(RESULTS_GAZE + SS + UNIT)
		os.makedirs(RESULTS_GAZE + SS + COOR)
	except:
		print("heads folder is exist. Dont forget to create a backup")


if __name__ == '__main__':
	init()
	start()
