'''
Created on 20 Jan 2022

@author: rhaapaniemi
'''




import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
import cv2
import os
from contributions_data_class import Contributions_data
from simulation_parameters_class import Simulation_parameters






class Application:
    
    def __init__(self):
        self.data = Contributions_data()
        self.para = Simulation_parameters()
        
        
    '''
    Iterate all Contribution.txt files
    in path folder
    '''
    def run(self):   
        for file in os.listdir(self.para.folder_path):   
            if file.endswith(".txt"):
                print("\n" + file)
                file_path = self.para.folder_path + "/" + file
                self.load_contributions(file_path)
                self.compute(file_path )
    
    
    '''
    Load and select 
    data in region
    '''
    def load_contributions(self, path):           
        try:       
            data = np.genfromtxt(path, delimiter=" ")  
            Az_coordinate   = data[:,0]
            Ra_coordinate   = data[:,1]
            Intensity       = data[:,3]
            Ref_level       = data[:,4]
            print("Number of data rows %d" % Az_coordinate.size)   
                       
            # show data in plots
            if self.para.visual_data:  
                plt.hist(Ra_coordinate, 1000)
                plt.title("Range data distribution")
                plt.ylabel("Number of data points")
                plt.xlabel("Range")
                plt.show()
                plt.hist(Az_coordinate, 1000)
                plt.title("Azimuth data distribution")
                plt.ylabel("Number of data points")
                plt.xlabel("Azimuth")
                plt.show()
                          
            # Remove all data that is out of selected range
            index_select = np.where((Az_coordinate > self.para.az_min)&
                                    (Az_coordinate < self.para.az_max)&
                                    (Ra_coordinate > self.para.ra_min)&
                                    (Ra_coordinate < self.para.ra_max))
            
            self.data.az_coordinate = (np.take(Az_coordinate, index_select)).ravel()
            self.data.ra_coordinate = (np.take(Ra_coordinate, index_select)).ravel()
            self.data.intensity     = (np.take(Intensity, index_select)).ravel()
            self.data.ref_level     = (np.take(Ref_level, index_select)).ravel()      
            print("Number of data rows after removing points outside of region %d" % len(self.data.az_coordinate)) 
            
        except:
            print("Error occurred while downloading file !!!!!")
            
            
            
    def compute(self, path):
        # length of total coordinate system
        azimuth_len = self.para.az_max - self.para.az_min
        range_len = self.para.ra_max - self.para.ra_min
        # coordinate tics
        azimuth_tic = np.ceil(azimuth_len / self.para.az_spacing).astype(int)
        range_tic = np.ceil(range_len / self.para.ra_spacing).astype(int)
        # image matrix
        sensor_plane = np.zeros((range_tic, azimuth_tic), dtype=complex)
        sensor_height = len(sensor_plane)
        sensor_width = len(sensor_plane[0]) 
        
        print("Generated sensor plane size")
        print(sensor_height)
        print(sensor_width)
    
        # picture pixel location offsetted from min coordinate values and centered  
        row_pixel = np.true_divide((self.data.ra_coordinate - self.para.ra_min), self.para.ra_spacing)
        col_pixel = np.true_divide((self.data.az_coordinate - self.para.az_min), self.para.az_spacing)
             
        '''
        Adds amplitude values to correct places in sensor_plane
        Computes phase and adds noise.
        Use detection resolution if wanted
        i range maximum 32bit is 2,147,000,000!!!
        '''
        print("Adding data to sensor plane...")
        for i in range(len(self.data.az_coordinate)):   
            # use only wanted trace levels
            if self.data.ref_level[i] <= self.para.tr_level:
                # compute signal angle along the distance 
                temp_angle = (-4*np.pi)/0.031*self.data.ra_coordinate[i]
                cycles = round(temp_angle/(2*np.pi))
                angle = temp_angle - cycles*2*np.pi
                # complex amplitude
                amplitude = self.data.intensity[i]
                noise = np.deg2rad(self.para.phase_noise) * np.random.uniform(-1, 1)
                signal = amplitude*np.cos(angle + noise) + 1j*amplitude*np.sin(angle + noise)
                
                # Add pixels to multiple rows according to resolution
                resolutionPixelWidth = self.para.resolution/2/self.para.ra_spacing
                y0 = int(row_pixel[i] - resolutionPixelWidth)
                if y0 < 0:
                    y0 = 0
                y1 = int(row_pixel[i] + resolutionPixelWidth)
                if y1 > sensor_height:
                    y1 = sensor_height
                x = int(col_pixel[i])
                sensor_plane[y0:y1+1, x] = sensor_plane[y0:y1+1, x] + signal
            
                            
        ''' 
        Allow pixels to spread mimicking non perfect detection.
        Adds star like shape due to impulse response overflow.
        '''  
        print("Lowering detection and adding impulse...")    
        sensor_plane = np.absolute(sensor_plane) 
        # Holds original old amplitudes to be used in calculations
        sensor_plane_raw_amplitudes = sensor_plane.copy()
        detect_blur_limit = sensor_plane_raw_amplitudes.max() * self.para.detect_rng_th
        # how much positions can vary
        RNG_POS = 1
        response_limit  = sensor_plane_raw_amplitudes.max() * self.para.response_th   
        #values for randomizing impulse stars
        IMP_RNG_AMP = 5.00
        x = np.arange(0, 300, 1)
           
        for i in range(0, sensor_width, 1):
            for j in range(0, sensor_height, 1):
                
                # Add non perfect detection to everything above shadow limit
                if sensor_plane_raw_amplitudes[j,i] > detect_blur_limit:              
                    if j > RNG_POS and j < sensor_height - RNG_POS:
                        if i > RNG_POS and i < sensor_width - RNG_POS:
                            
                            # Allows one pixel to change in wanted are
                            yPositions = np.random.randint(j-RNG_POS, high=j+RNG_POS)
                            xPositions = np.random.randint(i-RNG_POS, high=i+RNG_POS)                  
                            sensor_plane[yPositions, xPositions] += sensor_plane_raw_amplitudes[j,i]

               
                # Add impulse stars for bright pixels 
                if sensor_plane_raw_amplitudes[j,i] > response_limit and self.para.transparent == 0:
                    x0 = i - len(x)
                    x1 = i + len(x)
                    if x0 < 0:
                        x0 = 0
                    if x1 > sensor_width:
                        x1 = sensor_width             
                    y0 = j - len(x)
                    y1 = j + len(x)
                    if y0 < 0:
                        y0 = 0
                    if y1 > sensor_height:
                        y1 = sensor_height
                       
                    x0_i = np.flip(np.arange(0,i-x0))
                    y0_j = np.flip(np.arange(0,j-y0))              
                    i_x1 = np.arange(0, x1-i)
                    j_y1 = np.arange(0, y1-j)
                    
                    xAxis = np.concatenate((x0_i, i_x1))
                    yAxis = np.concatenate((y0_j, j_y1))
                     
                    amplitudes = self.impulse_amplitude(sensor_plane_raw_amplitudes[j,i], yAxis[:,None], xAxis[None,:])   
                    random_temp = np.random.uniform(0.9, IMP_RNG_AMP, size=(len(amplitudes), len(amplitudes[0])))
                    values = np.multiply(amplitudes, random_temp)
                    sensor_plane[y0:y1, x0:x1] += values
                    
                    
        '''
        Blur image by adding amplitudes to another pixels
        using Gaussian-function
        '''  
        if self.para.gaus_blur != 0:
            sensor_plane = gaussian_filter(sensor_plane, sigma=self.para.gaus_blur)    
            print("Absolut SAR values blurred with radius", self.para.gaus_blur)    
            
            
        '''
        Add Gaussian noise
        '''
        if self.para.gaus_noise != 0:
            noise = np.random.normal(0.9, self.para.gaus_noise, (sensor_height, sensor_width))
            noise[noise < 0] = 0
            sensor_plane = np.multiply(sensor_plane, noise)
            print("Absolut SAR values noised with standard deviation of", self.para.gaus_noise)

                
        '''
        dB 10 scaling snesor_plane image to wanted range.
        '''
        with np.errstate(divide='ignore'):
            sensor_plane = np.log10(sensor_plane)*10 
            self.para.dB_min += self.para.dB_min * self.para.dB_rng *  np.random.uniform(-1, 1)
            self.para.dB_max += self.para.dB_max * self.para.dB_rng *  np.random.uniform(-1, 1)
            sensor_plane[sensor_plane < self.para.dB_min] = self.para.dB_min
            sensor_plane[sensor_plane > self.para.dB_max] = self.para.dB_max
            
            if self.para.visual_data:
                plt.hist(sensor_plane.ravel(), 1000)
                plt.title('Histogram for 10dB10')
                plt.show()
                
                  
        '''
        scale image to gray color of 8 bit
        '''   
        amplitude_min = sensor_plane.min()
        amplitude_max = sensor_plane.max()
        interval = amplitude_max - amplitude_min
        # Only points above impulse limit are allowed to be perfect white  
        step_width = 254 / interval
        sensor_plane -= amplitude_min
        sensor_plane = (sensor_plane * step_width).astype(np.uint8)        
        sensor_plane[sensor_plane_raw_amplitudes > response_limit] = 255
        
        if self.para.visual_data:
            plt.hist(sensor_plane.ravel(),256,[0,256])
            plt.title('Histogram for gray scale picture')
            plt.show()
             
             
        '''
        flip if needed
        ''' 
        if self.para.upside_down:
            sensor_plane = cv2.flip(sensor_plane, 0)
            print("Image flipped vertically")
        
        
        '''
        Create a PIL image from Numpy array
        Remove image background
        '''
        im = Image.fromarray(sensor_plane)
        if self.para.transparent > 0:
            im = im.convert("RGBA")
            im_data = im.getdata()
            new_data = []
            for item in im_data:
                if item[0] < 2:
                    # Black transparent shadow is used to adjust shadows in scene images
                    new_data.append((0, 0, 0, 0))
                elif item[0] < self.para.transparent:
                    new_data.append((100, 100, 100, 0))
                elif item[0] > 254:
                    # White transparent points are used to add impulse responses with BG image
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            im.putdata(new_data)
            # There may be odd borders with higher values, that needs to be removed
            im = im.crop((5, 5, im.size[0]-5, im.size[1]-5))
        
        
        '''
        Scale image to another pixel size
        '''
        if self.para.rescale_size != 1:
            im = im.resize((int(im.size[0] * self.para.rescale_size), 
                            int(im.size[1] * self.para.rescale_size)), Image.NEAREST)
            print("Image rescaled to")
            print(im.size[0], im.size[1])
        
        '''
        Create a new name for image
        and save it to same path as 
        contributions
        '''
        path = path.rsplit("/", 1)
        destination = path[0]
        index = path[1].split("_")
        name = "/" + "SAR_" + index[0] + ".png"               
        destination += name      
        im.save(destination, "PNG")      
        print("Image saved to")
        print(destination)
        
        
    #################### HELPERS ########################## 
    
    def impulse_amplitude(self, amp, y, x):          
        value = amp * (1 / (np.power((x/self.para.response_decay),2.1) + 1)) * (1 / (np.power((y/self.para.response_decay),2.1) + 1))   
        return value
    
            
        
