
from .vehicle_generator import VehicleGenerator
from .geometry.segment import Segment
from .vehicle import Vehicle
import time
from datetime import datetime
from collections import deque
import threading
import threading

class Simulation:
    def __init__(self,hour_of_day,prediction_labeled,  destination_location, starting_location, weather, minute,df):
        self.segments = []
        self.vehicles = {}
        self.vehicle_generator = []
        self.start_time = datetime.now()
        self.t = 0.0
        self.dt = 1 / 60
        self.frame_count = 0
        self.hour_of_day = hour_of_day
        self.prediction_labeled = prediction_labeled
        self.destination_location = destination_location
        self.starting_location = starting_location
        self.weather = weather
        self.minute = minute
        #! DO NOT TOUCH WARNING
        self.df = df
        self.vr = 60
        self.vts = 60
        self.i = 0
        self.exportInsert()
        #!WARNING
        # Assuming predicted_value is dynamically updated elsewhere in the simulation


    def add_vehicle(self, veh):
        self.vehicles[veh.id] = veh
        if len(veh.path) > 0:
            self.segments[veh.path[0]].add_vehicle(veh)

    def add_segment(self, seg):
        self.segments.append(seg)

    def add_vehicle_generator(self, gen):
        self.vehicle_generator.append(gen)

    def create_vehicle(self, predicted_value, **kwargs):
        veh = Vehicle(predicted_value, kwargs)
        self.add_vehicle(veh)

    def create_segment(self, *args):
        seg = Segment(args)
        self.add_segment(seg)
    #! DO NOT TOUCH
    def exportInsert(self):
            if self.i==23:print("end")
            threading.Timer(8.0, self.exportInsert).start()
            self.vr=int(self.df.Actual[self.i])*85 + 200
            self.vts=int((52-self.vr*0.1)*0.5)
            print("self.vehicle_rate=",self.vr)
            print(self.df.Actual[self.i])
            self.i+=1
    #! WARNING 
    def create_vehicle_generator(self, predicted_value, **kwargs):
    # Initialize VehicleGenerator with the predicted value and any additional configurations
        gen = VehicleGenerator( predicted_value, kwargs)
        self.add_vehicle_generator(gen)

    
    def run(self, steps):
        for _ in range(steps):
            self.update()

    def update(self):
        # Update vehicles
        for segment in self.segments:
            if len(segment.vehicles) != 0:
                self.vehicles[segment.vehicles[0]].update(None, self.dt)
            for i in range(1, len(segment.vehicles)):
                self.vehicles[segment.vehicles[i]].update(
                    self.vehicles[segment.vehicles[i - 1]], self.dt)

        # Check roads for out of bounds vehicle
        for segment in self.segments:
            # If road has no vehicles, continue
            if len(segment.vehicles) == 0:
                continue
            # If not
            vehicle_id = segment.vehicles[0]
            vehicle = self.vehicles[vehicle_id]
            vehicle.v_max=self.vts
            # If first vehicle is out of road bounds
            if vehicle.x >= segment.get_length():
                # If vehicle has a next road
                if vehicle.current_road_index + 1 < len(vehicle.path):
                    # Update current road to next road
                    vehicle.current_road_index += 1
                    # Add it to the next road
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    self.segments[next_road_index].vehicles.append(vehicle_id)
                # Reset vehicle properties
                vehicle.x = 0
                # In all cases, remove it from its road
                segment.vehicles.popleft()
    #! DO NOT TOUCH
        # Update vehicle generators
        for gen in self.vehicle_generator:
            gen.update(self,self.vr)
    #! WARNING 
        # Calculate elapsed time in seconds
        current_time = datetime.now()
        elapsed_time = (current_time - self.start_time).total_seconds()

        # Update simulation time
        self.t = elapsed_time
        self.frame_count += 1

    def set_window(self, window):
        self.window = window
    
    def update_hour_of_day(self, hour_of_day):
        self.hour_of_day = hour_of_day

    def update_predicted_value(self, prediction_labeled):
        self.prediction_labeled = prediction_labeled

    def update_destination_location(self, destination_location):
        self.destination_location = destination_location

    def update_starting_location(self, starting_location):
        self.starting_location = starting_location

    def update_weather(self, weather):
        self.weather = weather
    
    def update_minute(self, minute):
        self.minute = minute
    
    def clear_simulation(self):
        """Clear the simulation from existing vehicles"""
        self.vehicles.clear()  # Remove all vehicles from the simulation
        # Clear vehicles from each segment
        for segment in self.segments:
            segment.vehicles = deque()  # Clear the deque of vehicles in the segment

    
    def reset_simulation(self):
        """Resets the entire simulation"""
        self.clear_simulation()  # Clear all vehicles
        # Reset any other states or parameters to their initial values
        self.t = 0.0
        self.frame_count = 0
