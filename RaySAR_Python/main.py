'''
Created on 13 Dec 2021

@author: rasmus
'''




import sys
import json
import pprint
from application import Application


def main(argv):
        
    app = Application()
     
    with open('para.json') as json_file:
        data = json.load(json_file)
        
    for settings in data:
        if settings['fileName'] == argv[1]:

            print("\nParameters from:\n" + settings['fileName'] + " selected\n")
            pprint.pprint(settings)
            
            app.para.set_azimuth_min(settings['azimuthMin'])
            app.para.set_azimuth_max(settings['azimuthMax'])
            app.para.set_azimuth_spacing(settings['azimuthSpacing'])
            app.para.set_range_min(settings['rangeMin'])
            app.para.set_range_max(settings['rangeMax'])
            app.para.set_range_spacing(settings['rangeSpacing'])
            app.para.set_resolution(settings['resolution'])
            app.para.set_dB_min(settings['dBmin'])
            app.para.set_dB_max(settings['dBmax'])
            app.para.set_dB_rng(settings['dBrng'])
            app.para.set_phase_noise_angle(settings['phaseNoise'])
            app.para.set_trace_level(settings['traceLevel'])
            app.para.set_detection_pix_rng_th(settings['detectionRngPixTh'])
            app.para.set_system_response_th(settings['responseTh'])
            app.para.set_system_response_decay(settings['responseDecey'])
            app.para.set_visual_data(settings['visualData'])
            app.para.set_sar_image_rescale(settings['imageRescalePercent'])
            app.para.set_gaus_blur(settings['gausBlurRadius'])
            app.para.set_gaus_noise(settings['gausNoiseDev'])
            app.para.set_upside_down(settings['upsideDown'])
            app.para.set_image_transparent(settings['transparentLimit'])
            app.para.set_folder_path(settings['path'])
            app.run()
         
    print("\n\nAll selected data is processed\nExiting program...")
    
    
    
if __name__ == '__main__':
    main(sys.argv)
    
    
    
    
    
    