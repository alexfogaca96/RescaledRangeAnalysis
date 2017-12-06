import csv
import math

# ========== Functions =============

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

# ==================================

def min(array):
	min = float("+inf")

	for i, value in enumerate(array):
		if i < min:
			min = i

	return min

# ==================================

def max(array):
	max = float("-inf")
	for i, value in enumerate(array):
		if i > max:
			max = i

	return max

# ========= RS Algorithm ===========

# Choose your time series
data = []

with open("AbbottHistoric.csv") as csvFile :
	reader = csv.DictReader(csvFile)
	for row in reader :
		data.append(float(row["close"]))


# Choose your ranges
range = [2, 4, 8, 16, 32, 64, 128, 256]


# Get the mean for each group of each range
means = []

for r, rng in enumerate(range):
	out = chunkIt(data, range[r])

	aux_means = []
	for i, colunm in enumerate(out):
		aux_mean = 0
		for j, row in enumerate(out[i]):
			aux_mean += out[i][j]
		
		aux_mean /= len(out[i])
		aux_means.append(aux_mean)

	means.append(aux_means)


# Get a series of deviations for each range and the sum
deviations = []
running_total = []

for r, rng in enumerate(range):
	out = chunkIt(data, range[r])

	aux_aux_running_total = []
	aux_deviations = []
	for i, colunm in enumerate(out):
		aux_deviation = 0
		aux_running_total = []
		for j, row in enumerate(out[i]):
			out[i][j] -= means[r][i]
			aux_deviation += out[i][j]
			aux_running_total.append(aux_deviation)

		aux_deviations.append(out[i])
		aux_aux_running_total.append(aux_running_total)

	deviations.append(aux_deviations)
	running_total.append(aux_aux_running_total)


# Calculate the widest difference in the series of deviations
widest_dif = []

for r, rng in enumerate(range):
	aux_widest_dif = []
	for i, colunm in enumerate(deviations[r]):
		aux_max = max(running_total[r][i])
		aux_min = min(running_total[r][i])
		dif = aux_max - aux_min
		aux_widest_dif.append(dif)

	widest_dif.append(aux_widest_dif)


# Calculate the standard deviation for each range
standard_deviations = []

for r, rng in enumerate(range):
	out = chunkIt(data, range[r])

	aux_standard_deviations = []
	for i, colunm in enumerate(out):
		aux_standard_deviation = 0
		for j, row in enumerate(out[i]):
			out[i][j] -= means[r][i]
			out[i][j] **= 2
			aux_standard_deviation += out[i][j]

		aux_standard_deviation /= len(out[i])
		aux_standard_deviation **= (1/2.0)
		aux_standard_deviations.append(aux_standard_deviation)

	standard_deviations.append(aux_standard_deviations)


# Calculate the rescaled range for each range in the time series
rescaled_range = []

for r, rng in enumerate(range):
	aux_rescaled_range = []
	for i, colunm in enumerate(widest_dif[r]):
		rs = widest_dif[r][i] / standard_deviations[r][i]
		aux_rescaled_range.append(rs)

	rescaled_range.append(aux_rescaled_range)

# Average the rescaled range values for each region to summarize each range
average_rescaled_range = []

for r, rng in enumerate(range):
	average = 0
	for i, colunm in enumerate(rescaled_range[r]):
		average += rescaled_range[r][i]

	average /= range[r];
	average_rescaled_range.append(average)


# Summarize data on one matrix
values = []

average_datapoints_range = []
for r, rng in enumerate(range):
	average_datapoints_range.append(len(data) / range[r])

values.append(range)
values.append(average_datapoints_range)
values.append(average_rescaled_range)


# Print the log-log values
log_log_values = []

size_values = []
for i, index in enumerate(range):
	size_values.append(math.log10(values[1][7 - i]))

rs_values = []
for i, index in enumerate(range):
	rs_values.append(math.log10(values[2][7 - i]))

log_log_values.append(size_values)
log_log_values.append(rs_values)


''' Linear regression on R
	size = -1.82579 + 1.98528 * rs '''
straight_line_points = []

for r, rng in enumerate(range):
	aux_point = -1.82579 + 1.98528 * log_log_values[1][r]
	aux_point_xy = []
	aux_point_xy.append(aux_point)
	aux_point_xy.append(log_log_values[1][r])

	straight_line_points.append(aux_point_xy)


# Slope incoming (as it's a line, there's no need to test other points)
aux_y = straight_line_points[0][1] - straight_line_points[1][1]
aux_x = straight_line_points[0][0] - straight_line_points[1][0]

slope = aux_y / aux_x

print("The slope is {:.3f}!".format(slope))

