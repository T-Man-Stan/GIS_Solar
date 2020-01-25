# GIS_Solar
GEOG 4303 Final Project

Project Summary: The primary mechanism by which a municipality or utility develops and acquires solar projects is by issuing Request For Proposals (RFPs) to prospective developers. Typically the window of time to bid into these RFPs is between two to six weeks. Hence, a developer must quickly identify and lock in a large number of suitable sites in order to compete for the RFP. This poses a large challenge, especially for smaller developers, when the service territory of the RFP issuer is large (e.g. it covers many counties or even states). Developers must parse through large datasets and spend large amounts of time trying to manually identify suitable locations via a tool like Google Earth, which lacks critical data such as parcel numbers and owner information.

Our model automates this process and selects suitable solar parcels within Jefferson County based off of standard solar suitability criteria. These include that the parcel is outside of a floodplain, greater than 30 acres, within certain municipal zoning classes, has low vegetation, has an aspect between 90 and 270, has a slope grade of less than 8%, and is within two miles of electric infrastructure. The weighted rank of vegetation, aspect and slope can be changed by the developer using our visualization tool on a local host.
How to Run: Please download from the emailed materials and place them all within the same master folder. Name this folder “Deliverable” and put it in the Z drive. This folder will be the directory that you connect to and set your work environment to in Spyder and ArcCatalog. All of the source data is within a folder called source_data. Make sure everything within this folder is unzipped.

master_script_5.4.19.py is our main program and is the program that the user should access and run within Spyder. There are three modules that the main is dependent on. They are suitability.py, floodplain_m.py, and jeff_size_m. They have all of the functions that select the specific criteria for the solar site. Run each of the modules, and then run master_script_5.4.19.py through Spyder and see results in ArcCatalog. The final output is a DEM named “inter_fp_DEM”. To produce the same visual schema displayed in the results section of the report, go into properties → symbology → classified  → set field value to “MAX” → set number of classes to 4  → make 0 white → make 0-1 green → make 1-2 blue → make 2-3 red. 

In order to run the visualization tool, first download the solar.py script into a text editor like Atom, Sublime, or Spyder. Then, go to your terminal, enter the source_data folder where the solar.py script is located (using cd), and run this command in your terminal: python solar.py. This will make your computer a local host. As the following commands in terminal say, copy the following URL into your browser http://127.0.0.1:8050/. The terminal will take a little while to run, as it is converting from easting/northing values to latitude/longitude values for a few thousands points. Note that the visualization tool is more of a model at this stage than a fully working tool. The user inputs are placeholders to show that various criteria weighted ranks can be changed. 

If you would like to change the weighted rank for aspect, first you must go into the suitability.py. Specify the percent weight (e.g. 0.0 - 100.0) you would like on line 193. You will then have to recompile and rerun both suitability.py and master_script_5.4.19.py  in Spyder. It will output a new inter_fp_DEM that accounts for the new aspect threshold. Open the “inter_fp_DEM” file in ArcCatalog, enter the table view, and export the table to the source_data folder as a txt file with the name dem.txt. Go back into the solar.py script, and rerun it in the terminal as stated above. This is not an effective way of doing this, but because of difficulties with cross platform communication (running Arc on Macs and Plotly on KESDA computers), this is the way to change the weighted rank as of now. 
 
Dependencies: In order to run the full program/project, the user must have the following five files: 
 
source_data
master_script_5.4.19.py
suitability.py
floodplain_m.py
Jeff_size_m.py
solar.py

Please ensure all four of these files are acquired and accessed before attempting to run the program. The program is also dependent on the following libraries: ArcPy, Numpy, Pandas, Plotly, and Osgeo, utm, and us. To import the last four libraries to your computer, please visit Plotly, GDAL,  us and utm.
