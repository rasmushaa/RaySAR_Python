'''
Created on 21 Jan 2022

@author: rhaapaniemi
'''




class Simulation_parameters():
     
    def __init__(self):
        self.az_spacing     = 0.2
        self.ra_spacing     = 0.2
        self.az_min         = -30
        self.az_max         =  30
        self.ra_min         = 100
        self.ra_max         = 180
        self.az_res         = 1
        self.ra_res         = 1
        self.phase_noise    = 0
        self.tr_level       = 3
        self.dB_min         = -30
        self.dB_max         = 100
        self.dB_rng         = 0.0
        self.detect_rng_th  = 0.5
        self.response_th    = 0.9
        self.response_decay = 0.7
        self.rescale_size   = 172
        self.upside_down    = 0
        self.transparent    = 0
        self.gaus_blur      = 0
        self.gaus_noise     = 0
        self.resolution     = 1.00
        self.visual_data    = 0
        self.folder_path    = ""
        
        
    #################### SETTINGS ##########################
    
    def set_visual_data(self, value):
        self.visual_data = value
    
    def set_folder_path(self, folder_path):
        self.folder_path = folder_path
    
    def set_azimuth_spacing(self, value):
        self.az_spacing = float(value)
        
    def set_range_spacing(self, value):
        self.ra_spacing = float(value)
        
    def set_azimuth_min(self, value):
        self.az_min = float(value)
    
    def set_azimuth_max(self, value):
        self.az_max = float(value)
        
    def set_range_min(self, value):
        self.ra_min = float(value)
    
    def set_range_max(self, value):
        self.ra_max = float(value)
        
    def set_azimuth_res(self, value):
        self.az_res = float(value)
        
    def set_range_res(self, value):
        self.ra_res = float(value)
        
    def set_resolution(self, value):
        self.resolution = value
    
    def set_trace_level(self, value):
        self.tr_level = float(value)
    
    def set_dB_min(self, value):
        self.dB_min = float(value)
        
    def set_dB_max(self, value):
        self.dB_max = float(value)
        
    def set_dB_rng(self, value):
        self.dB_rng = value
    
    def set_phase_noise_angle(self, value):
        self.phase_noise = float(value)
        
    def set_detection_pix_rng_th(self, value):
        self.detect_rng_th = value

    def set_system_response_th(self, value):
        self.response_th = value
            
    def set_system_response_decay(self,value):
        self.response_decay = value
        
    def set_sar_image_rescale(self, value):
        self.rescale_size = value
        
    def set_image_transparent(self, value):
        self.transparent = value
        
    def set_gaus_blur(self, value):
        self.gaus_blur = value
        
    def set_gaus_noise(self, value):
        self.gaus_noise = value
    
    def set_upside_down(self, value):
        self.upside_down = value
    