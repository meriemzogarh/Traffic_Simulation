import dearpygui.dearpygui as dpg
from trafficSimulator.core import *


class Window:
    def __init__(self, simulation):
        self.simulation = simulation


        self.zoom = 7
        self.offset = (0, 0)
        self.speed = 6

        self.is_running = False

        self.is_dragging = False
        self.old_offset = (0, 0)
        self.zoom_speed = 1

        self.setup()
        self.setup_themes()
        self.create_windows()
        self.create_handlers()
        self.resize_windows()
        

    def setup(self):
        dpg.create_context()
        dpg.create_viewport(title="TrafficSimulator", width=1280, height=720)
        dpg.setup_dearpygui()

    def setup_themes(self):
        with dpg.theme() as global_theme:

            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, category=dpg.mvThemeCat_Core)
                # dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, (8, 6), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Button, (90, 90, 95))
                dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 91, 140))
            with dpg.theme_component(dpg.mvInputInt):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (90, 90, 95), category=dpg.mvThemeCat_Core)
            #     dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

        dpg.bind_theme(global_theme)

        # dpg.show_style_editor()

        with dpg.theme(tag="RunButtonTheme"):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (5, 150, 18))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (12, 207, 23))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (2, 120, 10))

        with dpg.theme(tag="StopButtonTheme"):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (150, 5, 18))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (207, 12, 23))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (120, 2, 10))


    def create_windows(self):
        dpg.add_window(
            tag="MainWindow",
            label="     Simulation",
            no_close=True,
            no_collapse=True,
            no_resize=True,
            no_move=True,
            no_scrollbar=True,
            no_scroll_with_mouse=True
        )
        
        dpg.add_draw_node(tag="OverlayCanvas", parent="MainWindow")
        dpg.add_draw_node(tag="Canvas", parent="MainWindow")

        with dpg.window(
            tag="ControlsWindow",
            label="Controls",
            no_close=True,
            no_collapse=True,
            no_resize=True,
            no_move=True
        ):
            with dpg.collapsing_header(label="Simulation Control", default_open=True):

                with dpg.group(horizontal=True):
                    dpg.add_button(label="Run", tag="RunStopButton", callback=self.toggle)
                    #dpg.add_button(label="Next frame", callback=self.simulation.update)

                dpg.add_slider_int(tag="SpeedInput", label="Speed", min_value=1, max_value=100,default_value=8, callback=self.set_speed)
            
            with dpg.collapsing_header(label="Simulation Status", default_open=True):

                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    
                    with dpg.table_row():
                        dpg.add_text("Status:")
                        dpg.add_text("_", tag="StatusText")

                    with dpg.table_row():
                        dpg.add_text("Time:")
                        dpg.add_text("_s", tag="TimeStatus")

                    with dpg.table_row():
                        dpg.add_text("Frame:")
                        dpg.add_text("_", tag="FrameStatus")
            
            
            with dpg.collapsing_header(label="Camera Control", default_open=True):
    
                dpg.add_slider_float(tag="ZoomSlider", label="Zoom", min_value=0.1, max_value=100, default_value=self.zoom,callback=self.set_offset_zoom)            
                with dpg.group():
                    dpg.add_slider_float(tag="OffsetXSlider", label="X Offset", min_value=-100, max_value=100, default_value=self.offset[0], callback=self.set_offset_zoom)
                    dpg.add_slider_float(tag="OffsetYSlider", label="Y Offset", min_value=-100, max_value=100, default_value=self.offset[1], callback=self.set_offset_zoom)
            
            with dpg.collapsing_header(label="Location", default_open=True):

                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    
                    with dpg.table_row():
                        dpg.add_text("Street Name:")
                        dpg.add_text("_", tag="StreetName")

                    with dpg.table_row():
                        dpg.add_text("Date:")
                        dpg.add_text("_", tag="Date")

            with dpg.collapsing_header(label="Details", default_open=True):

                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    dpg.add_table_column()

                    with dpg.table_row():
                        dpg.add_text("Starting Location:")
                        dpg.add_text("_", tag="Starting_location")    

                    with dpg.table_row():
                        dpg.add_text("Destination Location:")
                        dpg.add_text("_", tag="Destination_location")

                    with dpg.table_row():
                        dpg.add_text("Weather:")
                        dpg.add_text("_", tag="Weather")

                    with dpg.table_row():
                        dpg.add_text("Time:")
                        dpg.add_text("_", tag="Time")

                    with dpg.table_row():
                        dpg.add_text("Prediction:")
                        dpg.add_text("_", tag="Prediction")

    def resize_windows(self):
        width = dpg.get_viewport_width()
        height = dpg.get_viewport_height()

        dpg.set_item_width("ControlsWindow", 320)
        dpg.set_item_height("ControlsWindow", height-38)
        dpg.set_item_pos("ControlsWindow", (0, 0))

        dpg.set_item_width("MainWindow", width-315)
        dpg.set_item_height("MainWindow", height-38)
        dpg.set_item_pos("MainWindow", (300, 0))

    def create_handlers(self):
        with dpg.handler_registry():
            dpg.add_mouse_down_handler(callback=self.mouse_down)
            dpg.add_mouse_drag_handler(callback=self.mouse_drag)
            dpg.add_mouse_release_handler(callback=self.mouse_release)
            dpg.add_mouse_wheel_handler(callback=self.mouse_wheel)
        dpg.set_viewport_resize_callback(self.resize_windows)
    

    def update_panels(self):
        # Update status text
        if self.is_running:
            dpg.set_value("StatusText", "Running")
            dpg.configure_item("StatusText", color=(0, 255, 0))
        else:
            dpg.set_value("StatusText", "Stopped")
            dpg.configure_item("StatusText", color=(255, 0, 0))
        
        # Update time and frame text
        dpg.set_value("TimeStatus", f"{self.simulation.t:.2f}s")  # Time is already in seconds
        dpg.set_value("FrameStatus", self.simulation.frame_count)
        dpg.set_value("Date", "Thursday 20 February")
        dpg.set_value("StreetName", "Jinnah Avenue")
        dpg.set_value("Starting_location", f"{self.simulation.starting_location}")  
        dpg.set_value("Destination_location", f"{self.simulation.destination_location}")           
        dpg.set_value("Time", f"{self.simulation.hour_of_day}h{self.simulation.minute:02}min")
        dpg.set_value("Weather", f"{self.simulation.weather}")           
        dpg.set_value("Prediction", f"{self.simulation.prediction_labeled}")   


    def mouse_down(self):
        if not self.is_dragging:
            if dpg.is_item_hovered("MainWindow"):
                self.is_dragging = True
                self.old_offset = self.offset
        
    def mouse_drag(self, sender, app_data):
        if self.is_dragging:
            self.offset = (
                self.old_offset[0] + app_data[1]/self.zoom,
                self.old_offset[1] + app_data[2]/self.zoom
            )

    def mouse_release(self):
        self.is_dragging = False

    def mouse_wheel(self, sender, app_data):
        if dpg.is_item_hovered("MainWindow"):
            self.zoom_speed = 1 + 0.01*app_data

    def update_inertial_zoom(self, clip=0.005):
        if self.zoom_speed != 1:
            self.zoom *= self.zoom_speed
            self.zoom_speed = 1 + (self.zoom_speed - 1) / 1.05
        if abs(self.zoom_speed - 1) < clip:
            self.zoom_speed = 1

    def update_offset_zoom_slider(self):
        dpg.set_value("ZoomSlider", self.zoom)
        dpg.set_value("OffsetXSlider", self.offset[0])
        dpg.set_value("OffsetYSlider", self.offset[1])

    def set_offset_zoom(self):
        self.zoom = dpg.get_value("ZoomSlider")
        self.offset = (dpg.get_value("OffsetXSlider"), dpg.get_value("OffsetYSlider"))

    def set_speed(self):
        self.speed = dpg.get_value("SpeedInput")


    def to_screen(self, x, y):
        return (
            self.canvas_width/2 + (x + self.offset[0] ) * self.zoom,
            self.canvas_height/2 + (y + self.offset[1]) * self.zoom
        )

    def to_world(self, x, y):
        return (
            (x - self.canvas_width/2) / self.zoom - self.offset[0],
            (y - self.canvas_height/2) / self.zoom - self.offset[1] 
        )
    
    @property
    def canvas_width(self):
        return dpg.get_item_width("MainWindow")

    @property
    def canvas_height(self):
        return dpg.get_item_height("MainWindow")

    def draw_bg(self, image_path="intersection.png"):
        width, height, channels, image_path = dpg.load_image(image_path)

        # Check if the texture with the tag "image_id" already exists
        if not dpg.does_item_exist("image_id"):
            with dpg.texture_registry():
                dpg.add_static_texture(width, height, image_path, tag="image_id")

        # Set the drawlist size to match the viewport size
        viewport_width = dpg.get_viewport_width()
        viewport_height = dpg.get_viewport_height()

        with dpg.drawlist(width=viewport_width, height=viewport_height, parent="MainWindow"):
            # Draw the image to cover the entire window
            dpg.draw_image("image_id", (0, 0), (viewport_width, viewport_height), uv_min=(0, 0), uv_max=(1, 1))


    def draw_axes(self, opacity=80):
        x_center, y_center = self.to_screen(0, 0)
        
        dpg.draw_line(
            (-10, y_center),
            (self.canvas_width+10, y_center),
            thickness=2, 
            color=(0, 0, 0, opacity),
            parent="OverlayCanvas"
        )
        dpg.draw_line(
            (x_center, -10),
            (x_center, self.canvas_height+10),
            thickness=2,
            color=(0, 0, 0, opacity),
            parent="OverlayCanvas"
        )

    def draw_grid(self, unit=10, opacity=50):
        x_start, y_start = self.to_world(0, 0)
        x_end, y_end = self.to_world(self.canvas_width, self.canvas_height)

        n_x = int(x_start / unit)
        n_y = int(y_start / unit)
        m_x = int(x_end / unit)+1
        m_y = int(y_end / unit)+1

        for i in range(n_x, m_x):
            dpg.draw_line(
                self.to_screen(unit*i, y_start - 10/self.zoom),
                self.to_screen(unit*i, y_end + 10/self.zoom),
                thickness=1,
                color=(0, 0, 0, opacity),
                parent="OverlayCanvas"
            )

        for i in range(n_y, m_y):
            dpg.draw_line(
                self.to_screen(x_start - 10/self.zoom, unit*i),
                self.to_screen(x_end + 10/self.zoom, unit*i),
                thickness=1,
                color=(0, 0, 0, opacity),
                parent="OverlayCanvas"
            )

    def draw_segments(self):
        for segment in self.simulation.segments:
            dpg.draw_polyline(segment.points, color=(180, 180, 220), thickness=3.5*self.zoom, parent="Canvas")
            # dpg.draw_arrow(segment.points[-1], segment.points[-2], thickness=0, size=2, color=(0, 0, 0, 50), parent="Canvas")

    def draw_vehicles(self):
        for segment in self.simulation.segments:
            for vehicle_id in segment.vehicles:
                vehicle = self.simulation.vehicles[vehicle_id]
                # Ensure progress stays within the valid range [0, 1]
                progress = min(1.0, max(0.0, vehicle.x / segment.get_length()))

                position = segment.get_point(progress)
                heading = segment.get_heading(progress)

                node = dpg.add_draw_node(parent="Canvas")

                # Draw vehicle with conditional color
                dpg.draw_line(
                    (0, 0),
                    (vehicle.l, 0),
                    thickness=1.76*self.zoom,
                    color=(161, 193, 129),  # Use the conditionally determined color
                    parent=node
                )

                translate = dpg.create_translation_matrix(position)
                rotate = dpg.create_rotation_matrix(heading, [0, 0, 1])
                dpg.apply_transform(node, translate * rotate)



    def apply_transformation(self):
        fixed_zoom_value = 11.139
        screen_center = dpg.create_translation_matrix([self.canvas_width/2, self.canvas_height/2, -0.01])
        translate = dpg.create_translation_matrix(self.offset)
        scale = dpg.create_scale_matrix([fixed_zoom_value, fixed_zoom_value])
        dpg.apply_transform("Canvas", screen_center*scale*translate)


    def render_loop(self):
        # Events
        self.update_inertial_zoom()
        self.update_offset_zoom_slider()

        # Remove old drawings
        dpg.delete_item("OverlayCanvas", children_only=True)
        dpg.delete_item("Canvas", children_only=True)
        
        # New drawings
        self.draw_bg(image_path="intersection.png")
        #self.draw_axes()
        #self.draw_grid(unit=10)
        #self.draw_grid(unit=50)
        #self.draw_segments()
        self.draw_vehicles()

        # Apply transformations
        self.apply_transformation()

        # Update panels
        self.update_panels()

        # Update simulation
        if self.is_running:
            self.simulation.run(self.speed)

    def show(self):
        dpg.show_viewport()
        while dpg.is_dearpygui_running():
            self.render_loop()
            dpg.render_dearpygui_frame()
        dpg.destroy_context()

    def run(self):
        self.is_running = True
        dpg.set_item_label("RunStopButton", "Stop")
        dpg.bind_item_theme("RunStopButton", "StopButtonTheme")

    def stop(self):
        self.is_running = False
        dpg.set_item_label("RunStopButton", "Run")
        dpg.bind_item_theme("RunStopButton", "RunButtonTheme")

    def toggle(self):
        if self.is_running: self.stop()
        else: self.run()