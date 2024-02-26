from trafficSimulator.core import *
from trafficSimulator.core.vehicle_generator import VehicleGenerator
from trafficSimulator.core.simulation import Simulation
from trafficSimulator.visualizer.window import Window
from queue import Queue

import pandas as pd

# Path to your CSV file
csv_file_path = "filtered_results_day_20_Jinnah_Ave_labeled.csv"

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Create a shared queue for (predicted value, hour of day) tuples
value_queue = Queue()

# Enqueue (predicted value, hour of day) tuples
for _, row in df.iterrows():
    value_queue.put((row['Predicted'], row['Hour_of_Day'], row['Predicted_Category'], row['Destination_Location'], row['Starting_Location'], row['Weather']))

print(value_queue.qsize())  # Print the number of items in the queue

# Here we'll assume the VehicleGenerator and simulation have been updated to handle the hour_of_day properly.
if not value_queue.empty():
    initial_predicted_value, initial_hour_of_day, initial_prediction_labeled, initial_destination_labeled, initial_starting_location_labeled, initial_weather_labeled = value_queue.get_nowait()
else:
    initial_predicted_value, initial_hour_of_day = 0, 0 # Default values or handle as needed
    initial_prediction_labeled = ""
    initial_weather_labeled = ""
    initial_starting_location_labeled = ""
    initial_destination_labeled = ""


sim = Simulation(initial_hour_of_day, initial_prediction_labeled, initial_destination_labeled, initial_starting_location_labeled, initial_weather_labeled,df)

lane_space = 4
intersection_size = 12
length = 100

sim.create_segment((50, 3), (-50, 3))
sim.create_segment((-50, -3), (50, -3))


# Pass the shared queue to the VehicleGenerator and simulation object
vg = VehicleGenerator(initial_hour_of_day, initial_prediction_labeled, initial_destination_labeled, initial_starting_location_labeled, initial_weather_labeled,{
    'vehicles': [
        (1, {'path': [0], 'v': 16.6}),
        (1, {'path': [1], 'v': 16.6})
    ], 'value_queue': value_queue
})
sim.add_vehicle_generator(vg)

# Pass the initial_hour_of_day to the Window
win = Window(sim)
sim.set_window(win)
win.run()
win.show()