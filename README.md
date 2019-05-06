# GIS_Solar

GEOG 4303 Final Project
Members: Avra Saslow, Trevor Stanley, Xingying Huang 
Project Summary: The primary mechanism by which a municipality or utility develops and acquires solar projects is by issuing Request For Proposals (RFPs) to prospective developers. Typically the window of time to bid into these RFPs is between two to six weeks. Hence, a developer must quickly identify and lock in a large number of suitable sites in order to compete for the RFP. This poses a large challenge, especially for smaller developers, when the service territory of the RFP issuer is large (e.g. it covers many counties or even states). Developers must parse through large datasets and spend large amounts of time trying to manually identify suitable locations via a tool like Google Earth, which lacks critical data such as parcel numbers and owner information.
Our model automates this process and selects suitable solar parcels within Jefferson County based off of standard solar suitability criteria. These include that the parcel is outside of a floodplain, greater than 30 acres, within certain municipal zoning classes, has low vegetation, has an aspect between 90 and 270, has a slope grade of less than 8%, and is within two miles of electric infrastructure. The weighted rank of vegetation, aspect and slope can be changed by the developer using our visualization tool on a local host.
How to Run: Please download, or using Github, “check-out” the code and associative data. All of the data is within a folder called source_data. Download it, move it into your D drive and set your workspace to the inside of the folder.
main.py is our main program and is the program that the user should access and run within Spyder. There are three modules that the main is dependent on. They are suitability.py, floodplain_m.py, and jeff_size_m. They have all of the functions that select the specific criteria for the solar site. Run each of the modules, and then run main.py through Spyder and see results in ArcCatalog.
In order to run the visualization tool, first download the solar.py script into a text editor like Atom, Sublime, or Spyder. Then, go to your terminal, enter the source_data folder where the solar.py script is located (using cd), and run this command in your terminal: python solar.py. This will make your computer a local host. As the following commands in terminal say, copy the following URL into your browser http://127.0.0.1:8050/.
If you would like to change the weighted rank for aspect, first you must go into the main.py. Specify the percent weight you would like in the user input variable. You will then have to recompile and rerun the main.py in Spyder. It will output a new final parcels file. Open the final parcels file in ArcCatalog, enter the table view, and export the table to the source_data folder as a txt file with the name dem.txt. Go back into the solar.py script, and rerun it in the terminal as stated above.
Dependencies: In order to run the full program/project, the user must have the following five files: 
 
source_data
main.py
suitability.py
floodplain_m.py
Jeff_size_m.py
solar.py
Please ensure all four of these files are acquired and accessed before attempting to run the program. The program is also dependent on the following libraries: ArcPy, Numpy, Pandas, Plotly, and Osgeo.
