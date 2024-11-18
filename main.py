import psutil
import os

file_name = r"D:\KWC_2\resource\0_example.txt"

print(f'File Size is {os.stat(file_name).st_size / (1024 * 1024)} MB')

txt_file = open(file_name)

count = 0

for line in txt_file:
    # we can process file line by line here, for simplicity I am taking count of lines
    count += 1

txt_file.close()

print(f'Number of Lines in the file is {count}')
cpu_times = os.times()

process = psutil.Process()
memory_usage = process.memory_info().rss / (1024 * 1024)
print(f"Peak Memory Usage = {memory_usage:.2f} MB")
print(f"User Mode Time = {cpu_times.user:.2f} seconds")
print(f"System Mode Time = {cpu_times.system:.2f} seconds")