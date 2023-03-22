import numpy as np
import time
import concurrent.futures
import os
import psutil
import matplotlib.pyplot as plt


def mandelbrot(c, max_iter):
    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z * z + c
    return max_iter


def worker_process(args):
    process_id, y_start, y_end, x_range, y_range, max_iter = args
    print(f"Process {process_id}: Starting...")
    img = np.zeros((y_end - y_start, x_range))
    for y in range(y_start, y_end):
        for x in range(x_range):
            real = x * (3.5 / x_range) - 2.5
            imag = y * (2.0 / y_range) - 1.0
            c = complex(real, imag)
            img[y - y_start, x] = mandelbrot(c, max_iter)
    print(f"Process {process_id}: Finished.")
    return y_start, img


def collect_system_stats():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_voltage = None  # Placeholder, as voltage data is not provided by psutil
    
    sensors_temperatures = psutil.sensors_temperatures()
    cpu_temperature = None
    
    if 'coretemp' in sensors_temperatures:
        coretemp = sensors_temperatures['coretemp']
        if isinstance(coretemp, list) and len(coretemp) > 0:
            cpu_temperature = coretemp[0].current
    
    return cpu_percent, cpu_temperature, cpu_voltage

def main():
    height = 800
    cpu_count = os.cpu_count()
    print(f"Number of available CPU cores: {cpu_count}")

    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_count) as executor:
        tasks = [(y, y + height // cpu_count) for y in range(0, height, height // cpu_count)]
        for y_start, img_part in executor.map(worker_process, tasks):
            final_img.paste(img_part, (0, y_start))
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    score = int(final_img.width * final_img.height / elapsed_time)
    print(f"CPU stress test completed in {elapsed_time:.2f} seconds.")
    print(f"Your CPU score is: {score}")

    cpu_load, cpu_temp, cpu_voltage = collect_system_stats()
    print(f"CPU Load: {cpu_load}%")
    print(f"CPU Temperature: {cpu_temp}°C") if cpu_temp else print("CPU Temperature: N/A")
    print(f"CPU Voltage: {cpu_voltage}V") if cpu_voltage else print("CPU Voltage: N/A")

    show_stats_graph(cpu_load, cpu_temp, cpu_voltage)


if __name__ == '__main__':
    main()

