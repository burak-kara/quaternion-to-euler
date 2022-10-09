import math
import os
import numpy as np

SS = "\\"
NEW_LINE = "\n"
RESULTS_HEAD = "heads"
STATS_FOLDER = "statistics"
TASKS = 4 + 1  # The actual count is 4 but for boundary reasons added +1
VIDEOS = 15 + 1  # for boundary reasons added +1
USERS = 30 + 1  # for boundary reasons added +1


def record_stats(file, speeds):
	stat_file = open(STATS_FOLDER + SS + file + '.txt', 'w')
	quantiles = np.quantile(speeds, [0.25, 0.5, 0.75])
	mean = round(np.mean(speeds), 2)
	stat_file.write(str(mean) + NEW_LINE)
	for q in quantiles:
		stat_file.write(str(q) + NEW_LINE)


def to_float(list_):
	return list(map(float, list_.replace(NEW_LINE, '').split()))


def get_diffs(prev_line, curr_line):
	prev_line, curr_line = to_float(prev_line), to_float(curr_line)
	return [curr_line[0] - prev_line[0], prev_line[1] - curr_line[1], prev_line[2] - curr_line[2]]


def calculate_speed(prev_line, curr_line):
	diffs = get_diffs(prev_line, curr_line)
	return round(math.sqrt(pow(diffs[1], 2) + pow(diffs[2], 2)) / (diffs[0] / 1000), 2)


def record(file, list_, speed):
	file.write(str(speed) + NEW_LINE)  # speed is 0 on the first line
	list_.append(speed)


def write_stats(files):
	task_1_speeds = []
	task_2_speeds = []
	task_3_speeds = []
	task_4_speeds = []
	for file in files:
		if 'Task_1' in file:
			speeds = task_1_speeds
		elif 'Task_2' in file:
			speeds = task_2_speeds
		elif 'Task_3' in file:
			speeds = task_3_speeds
		else:
			speeds = task_4_speeds
		speed_file = open(STATS_FOLDER + SS + file, 'w')
		head_file = open(RESULTS_HEAD + SS + file)
		lines = head_file.readlines()
		record(speed_file, speeds, 0)  # speed is 0 on the first line
		for i in range(1, len(lines)):
			prev_line, curr_line = lines[i - 1], lines[i]
			speed = calculate_speed(prev_line, curr_line)
			record(speed_file, speeds, speed)

	record_stats('stats_task_1', task_1_speeds)
	record_stats('stats_task_2', task_2_speeds)
	record_stats('stats_task_3', task_3_speeds)
	record_stats('stats_task_4', task_4_speeds)


def get_file_names():
	users = [1]
	user_count = 30 + 1
	video_per_user = 1
	tasks = [1, 2, 3, 4]
	# tasks = [1, 3]
	files = []
	for user_start in users:
		for user in range(user_start, user_count, 5):
			for video in range(user_start, user_start + video_per_user):
				for task in tasks:
					u = '0' + str(user) if user < 10 else str(user)
					v = '0' + str(video) if video < 10 else str(video)
					file_name = 'User_' + str(u) + '_Video_' + str(v) + '_Task_' + str(task)
					files.append(file_name)
	return files


def init():
	try:
		os.makedirs(STATS_FOLDER)
	except:
		print("statistics folder is exist. Dont forget to create a backup")


if __name__ == '__main__':
	init()
	files = get_file_names()
	write_stats(files)
