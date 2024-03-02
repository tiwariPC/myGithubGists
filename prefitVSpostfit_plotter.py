import re
import csv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import subprocess
import optparse
import os, sys
import glob

usage = "usage: python crSummary_prefit.py -i <input root file> -f <bonly or sb> -c <1b or 2b> -y <year>"
parser = optparse.OptionParser(usage)
parser.add_option("-i", "--infile", type="string", dest="rootFileDir", help="input fit file")
parser.add_option("-c", "--category", type="string", dest="cat", help="1b or 2b")
parser.add_option("-y", "--year", type="string", dest="year", help="year of histogram")
parser.add_option("-f", "--fit", type="string", dest="fit_dir",help="'S+B Fit' or 'B-Only Fit'")
(options, args) = parser.parse_args()

if options.rootFileDir == None:
    print('Please provide input file name')
    sys.exit()
else:
    input_file = options.rootFileDir

if options.cat == None:
    print('Please provide which category to use (1b or 2b)')
    sys.exit()
else:
    cat = str(options.cat)

if options.year == None:
    print('Please provide year')
    sys.exit()
else:
    year = str(options.year)

if options.fit_dir == None:
    print('Please provide which fit directory to use (b or sb)')
    sys.exit()
elif options.fit_dir == 'bonly' :
    fit_ = str('B-Only Fit')
elif options.fit_dir == 'sb' :
    fit_ = str('S+B Fit')


# Run the command and capture its output
result = subprocess.run(['python',os.getcwd()+'/mlfitNormsToText.py',input_file, '-u'], stdout=subprocess.PIPE)

preVSpostfit_file = input_file.split('/')[-2]+'_'+input_file.split('/')[-1].strip('.root')
# Write the output to a file
with open('prefitVSpostfit/'+preVSpostfit_file+'.csv', 'w') as f:
    f.write(result.stdout.decode())

# Open the input text file and read the contents
with open('prefitVSpostfit/'+preVSpostfit_file+'.csv', 'r') as f:
    text = f.read()

# Use regular expressions to extract the data
pattern = r'([a-z0-9_]+)\s+([a-zA-Z0-9_\-\.]+)\s+([0-9\.]+ \+/- [0-9\.]+)\s+([0-9\.]+ \+/- [0-9\.]+)\s+([0-9\.]+ \+/- [0-9\.]+)'
matches = re.findall(pattern, text, re.MULTILINE)

# Write the data to a CSV file
with open('prefitVSpostfit/'+preVSpostfit_file+'_modified1.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Channel', 'Process', 'Pre-fit', 'S+B Fit', 'B-Only Fit'])
    for match in matches:
        writer.writerow(match)


# Load the CSV file into a Pandas dataframe
df = pd.read_csv('prefitVSpostfit/'+preVSpostfit_file+'_modified1.csv')

# Remove the "+/-" and everything after it in the "B-Only Fit" and "Pre-fit" columns
df[fit_] = df[fit_].str.split(' ').str[0]
df['Pre-fit'] = df['Pre-fit'].str.split(' ').str[0]

# Convert the "fit_" and "Pre-fit" columns to numeric
df[fit_] = pd.to_numeric(df[fit_])
df['Pre-fit'] = pd.to_numeric(df['Pre-fit'])

# Calculate the percentage difference between the "B-Only Fit" and "Pre-fit" columns
df['Percentage Difference'] = (df[fit_] - df['Pre-fit']) / df['Pre-fit'] * 100

# Save the modified dataframe to a new CSV file
df.to_csv('prefitVSpostfit/'+preVSpostfit_file+'_modified2.csv', index=False)


# Read in the data
df = pd.read_csv('prefitVSpostfit/'+preVSpostfit_file+'_modified2.csv')

# Filter out the row with the specified Process value
df = df[df['Process'] != '2HDMa_Ma200_MChi1_MA600_tb35_st_0p7']

# Create the bar plot with a width of 12 inches
g = sns.catplot(x='Channel', y='Percentage Difference', hue='Process', data=df, kind='bar', palette='muted', height=15, aspect=3, legend=False)

# Set the plot title and axis labels, increase font size and bold
plt.title(fit_+r'$\mathit{ - }$Pre-fit$(\%)$  '+cat+' '+year, fontsize=60, fontweight='bold')

plt.xlabel('Channel', fontsize=30, fontweight='bold')
plt.ylabel('Difference(%)', fontsize=30, fontweight='bold')

# Rotate the x-axis labels by 90 degrees and increase font size
plt.xticks(rotation=80, fontsize=30)
plt.yticks(fontsize=30)

# Add a grid to the plot
plt.grid(True)

# Add a vertical line after each bin
for i in range(len(df['Channel'].unique()) - 1):
    plt.axvline(x=i + 0.5, color=(1.0, 0.5, 0.5), linestyle='--',linewidth=2)

# Get the underlying AxesSubplot object and set the location of the legend
ax = g.ax
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc='upper right', ncol=4, fontsize=30, title_fontsize=14)

# Save the plot in pdf format with high resolution
plt.savefig('prefitVSpostfit/plot_'+preVSpostfit_file+'_'+options.fit_dir+'.pdf', dpi=300, bbox_inches='tight')

# Delete the text and CSV files
file_list = glob.glob('prefitVSpostfit/*modified*.csv')
for file in file_list:
    os.remove(file)