
# import appropriate modules. ---------------------------------------------------

import os
import os.path
import csv
import time
import datetime

# Get start time for the timer. --------------------------------------------------

start = time.time()
start_date_time = datetime.datetime.now()

# Set up CSV files to be read & Validate they are in location defined. -----------

folder = "C:\\Data\\PythonFiles"
instrumentCSV = "071417_tkn"

LabData = folder + "\\" + instrumentCSV + ".csv"

ReviewerReport = folder + "\\" + instrumentCSV + "_reviewed.txt"

if os.path.isfile(LabData):
    print "Lab Data located"
    print "----------------"
else:
    print "Lab Data was not located"

# Define Quality control values (mg/L). ------------------------------------------

ReportingLimit = 0.15
ICV = 0.40
MB = 0.00
BS = 1.00
CCV = 2.00
CCB = 0.00
MaximumDetect = 4.00

# Define acceptable criteria of Quality Control (i.e. +/- 10%) -------------------

Upper_limit = 1.1  # 110% recovery
Lower_limit = 0.9  #  90% recovery

# Open text file to begin the writing the reviewer report. ------------------------

reviewerReport = open(ReviewerReport, "w")

reviewerReport.write("Reviewer Report generated: " + (start_date_time.strftime("%Y-%m-%d   %H:%M"))+ "\n" + "\n" + "\n")
reviewerReport.write( "----------------"+ "\n")


# Open CSV & Skip white space after delimiter when reading. ----------------------

with open(LabData) as LabData:
    LabData_reader = csv.DictReader(LabData)
    csv.Dialect.skipinitialspace = True


# Begin processing Lab Data CSV file. --------------------------------------------

    for line in LabData_reader:

        # Verify the ICV results.
        
        if line['Sample ID'] == "ICV":
            result = float(line['Results'])
            recovery = (result / ICV)*100 
            if (ICV * Lower_limit) <= result and result <= (ICV * Upper_limit):
                reviewerReport.write( "Analyst: " + line['Analyst']+ "\n")
                reviewerReport.write( "Date & Time: " + line['Date and Time']+ "\n")
                reviewerReport.write( "Test: " + line['SEAL AQ2 Test']+ "\n")
                reviewerReport.write( "----------------"+ "\n")
                reviewerReport.write( "Quality Control Summary:"+ "\n")
                reviewerReport.write( "ICV = " + str(recovery) + "%, Acceptable" + "\n" )
            else:
                reviewerReport.write( "ICV = " + str(recovery) + "%, Failed" + "\n")
                
        # Verify the Method Blank (MB) results.
        
        elif line['Sample ID'] == "MB":
            result = float(line['Results'])
            if result < ReportingLimit and (-1*(ReportingLimit)) < result:
                reviewerReport.write( "MB = Acceptable" + "\n" )
            else:
                reviewerReport.write( "MB = Failed" + "\n" )
                
        # Verify the Blank Spikes (BS) results.

        elif line['Sample ID'] == "BS":
            result = float(line['Results'])
            recovery = (result / BS)*100
            if (BS * Lower_limit) <= result and result <= (BS * Upper_limit):
                reviewerReport.write( "BS = " + str(recovery) + "%, Acceptable" + "\n")
            else:
                reviewerReport.write( "BS = " + str(recovery) + "%, Failed" + "\n")

        # Verify the CCV results.

        elif line['Sample ID'] == "CCV":
            result = round(float(line['Results']), 1)
            recovery = (result / CCV)*100
            if (CCV * Lower_limit) <= result and result <= (CCV * Upper_limit):
                reviewerReport.write( "CCV = " + str(recovery) + "%, Acceptable" + "\n")
            else:
                reviewerReport.write( "CCV = " + str(recovery) + "%, Failed" + "\n")
        
        # Verify the CCB results
        
        elif line['Sample ID'] == "CCB":
            result = round(float(line['Results']), 1)
            if result < ReportingLimit and (-1*(ReportingLimit)) < result:
                reviewerReport.write( "CCB = Acceptable" + "\n")
            else:
                reviewerReport.write( "CCB = Failed" + "\n")

        # All samples need to be less than the maximum detection limit. If samples are above the
        # maximum detection limit, they are diluted back into range. If the maximum detection *
        # the dilution factor (manual * auto) is less than the sample result * dilution factor
        # then the sample must be reanalyzed. 
                    
        else:
            result = float(line['Results'])
            manual = float(line['Man Dil Factor'])
            auto = float(line['Auto Dil Factor'])
            dilutionFactor = manual * auto
            if result < (MaximumDetect * dilutionFactor):
                continue
            else:
                reviewerReport.write( line['Sample ID'] + " needs to be reanalyzed at a higher dilution." + "\n")

reviewerReport.write( "----------------" + "\n" + "\n" + "\n")
    
reviewerReport.write( " Report generated using Lab Data Reviewer."+ "\n")
reviewerReport.write( " Author : Zac Hancock " + "\n")
                      
# Get end time for the timer - Print time elapsed. Close reviewer report. ----------------------

end = time.time()
total_time = round(float((end - start)), 4)
print "Function took " + str(total_time) + " seconds to complete."

reviewerReport.close()
