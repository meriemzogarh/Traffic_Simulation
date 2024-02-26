from .vehicle import Vehicle
from numpy.random import randint
import time
from queue import Queue


class VehicleGenerator:
    def __init__(self, hour_of_day,prediction_labeled,  destination_location, starting_location, weather, minute, config={}):
        # Set default configurations
        self.set_default_config()
        self.last_added_time = 0
        self.predicted_value = 0  # Initialize predicted value
        self.hour_of_day = hour_of_day
        self.prediction_labeled = prediction_labeled
        self.destination_location = destination_location
        self.starting_location = starting_location
        self.weather = weather
        self.minute = minute
        self.prediction_update_time = time.time() 
        self.current_value_timestamp = time.time()  # Initialize current value timestamp
        self.time_threshold = 7
        # Update configurations
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()

    def set_default_config(self):
        """Set default configuration"""
        self.vehicle_rate = 100
        self.vehicles = [
            (1, {})
        ]
      # Initialize prediction update time
        self.prediction_update_time = time.time()

    def init_properties(self):
        self.upcoming_vehicle = self.generate_vehicle()

    def generate_vehicle(self):
        """Returns a random vehicle from self.vehicles with random proportions"""
        total = sum(pair[0] for pair in self.vehicles)
        r = randint(1, total+1)
        for (weight, config) in self.vehicles:
            r -= weight
            if r <= 0:
                # Create a vehicle with the current predicted value
                return Vehicle(config)

    def update(self, simulation,vr):
        self.vehicle_rate = vr
        if time.time() - self.prediction_update_time >= 8:
            self.predicted_value, self.hour_of_day, self.prediction_labeled, self.destination_location, self.starting_location, self.weather, self.minute = self.get_next_predicted_value()
            # After updating the hour_of_day:
            simulation.update_hour_of_day(self.hour_of_day)
            simulation.update_predicted_value(self.prediction_labeled)
            simulation.update_destination_location(self.destination_location)
            simulation.update_starting_location(self.starting_location)
            simulation.update_weather(self.weather)       
            simulation.update_minute(self.minute)                                
            self.prediction_update_time = time.time()
        """Add vehicles"""
        if simulation.t - self.last_added_time >= 60 / self.vehicle_rate:
            # If time elasped after last added vehicle is
            # greater than vehicle_period; generate a vehicle
            segment = simulation.segments[self.upcoming_vehicle.path[0]]      
            if len(segment.vehicles) == 0\
               or simulation.vehicles[segment.vehicles[-1]].x > self.upcoming_vehicle.s0 + self.upcoming_vehicle.l:
                # If there is space for the generated vehicle; add it
                simulation.add_vehicle(self.upcoming_vehicle)
                # Reset last_added_time and upcoming_vehicle
                self.last_added_time = simulation.t
            self.upcoming_vehicle = self.generate_vehicle()
    
    def get_next_predicted_value(self):
        current_time = time.time()
        time_since_last_update = current_time - self.current_value_timestamp
        if time_since_last_update >= self.time_threshold:
            # Update the timestamp and get the next (predicted value, hour of day) tuple from the queue
            self.current_value_timestamp = current_time
            try:
                predicted_value, hour_of_day, prediction_labeled, destination_location, starting_location, weather, minute = self.value_queue.get_nowait()
                self.predicted_value = predicted_value
                # Store or update hour_of_day as needed
                self.hour_of_day = hour_of_day
                self.prediction_labeled = prediction_labeled
            except Queue.Empty:
                # Handle the case when the queue is empty
                pass
            else:
                print(f"Updated Predicted Value: {self.predicted_value}, Hour of Day: {self.hour_of_day}, Prediction Label: {self.prediction_labeled}")

        return (self.predicted_value, self.hour_of_day, self.prediction_labeled, destination_location, starting_location, weather, minute)

