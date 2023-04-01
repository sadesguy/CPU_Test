import os
import time
import concurrent.futures
from PIL import Image
import psutil

def mandelbrot(y_start, y_end, x_range, y_range, max_iter):
    img = Image.new('RGB', (x_range, y_range))
    for y in range(y_start, y_end):
        for x in range(x_range):
            zx, zy = x * (3.5 / x_range) - 2.5, y * (2 / y_range) - 1
            c = zx + zy * 1j
            z = c
            for i in range(max_iter):
                if abs(z) > 2.0:
                    break 
                z = z * z + c
            img.putpixel((x, y - y_start), (i % 8 * 32, i % 16 * 16, i % 32 * 8))
    return img

def worker_process(args):
    y_start, y_end = args
    x_range, y_range, max_iter = (800, 800, 1000)
    img_part = mandelbrot(y_start, y_end, x_range, y_range, max_iter)
    return y_start, img_part

def collect_system_stats():
    cpu_load = psutil.cpu_percent(interval=1)
    cpu_temperature = psutil.sensors_temperatures().get('coretemp', [])[0].current
    cpu_voltage = psutil.sensors_battery().power_plugged
    return cpu_load, cpu_temperature, cpu_voltage

def main():
    height = 800
    final_img = Image.new('RGB', (800, 800))
    cpu_count = os.cpu_count()
    print(f"Number of available CPU cores: {cpu_count}")

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_count) as executor:
        tasks = [(y, y + height // cpu_count) for y in range(0, height, height // cpu_count)]
        for y_start, img_part in executor.map(worker_process, tasks):
            final_img.paste(img_part, (0, y_start))

    final_img.save('output.png', 'PNG')

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"CPU stress test completed in {elapsed_time:.2f} seconds.")
    print(f"Your CPU score is: {int(800 * 800 / elapsed_time)}")

    cpu_load, cpu_temperature, cpu_voltage = collect_system_stats()
    print(f"CPU Load: {cpu_load}%")
    print(f"CPU Temperature: {cpu_temperature}°C")
    print(f"CPU Voltage: {cpu_voltage}V")

if __name__ == '__main__':
    main()

