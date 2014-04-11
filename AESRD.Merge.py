# Merges the data from Alberta Environment's website into a single series
# for each station. The data is collected at least every three days to avoid
# a loss of part of the record since the data retrieved is a running three day
# record.
#
# These pieces retrieved daily must then be merged into a single series. This
# script performs the merge step.
#
# Assumptions:
#   1. For now, assumes the data to be merged is the flow data. The code to
#      merge the data formats for the meteorological and snowpack data has
#      not yet been written. The flow data format is expected to be:
#       ln 1-25: file header
#       ln 26: col header, titles
#       ln 27: col header, units
#       ln 28-end: data
#
#       where lines 26-end are expected to contain: station,date,stage,flow
#
# Usage: run this script in the directory containing the 'flow' directory
#        that is written by AESRD.Scrape.
import os
import datetime
from collections import defaultdict

today = datetime.date.today().isoformat()
log = ''
logheader = 'The following series contained no entries:\n'

# TODO: Extract the parsing logic that is specific to the flow files and
#       then write the code to merge the meteorological and snowpack files.
for category in ['flow']: #['flow', 'meteor', 'snow']:
    stations = defaultdict(list)
    station_names = {}

    # Collect all the data files retrieved for the particular category.
    fnames = os.listdir(category)
    # Generate a lookup from station ID to a list of all data files for that station.
    for fname in fnames:
        station_id = fname.split(';')[1].strip()
        station_name = fname.split(';')[2].strip()
        stations[station_id].append(fname)
        station_names[station_id] = station_name

    # Each pairing identifies a station whose merged series should be constructed.
    for station_id in stations:
        series = {}

        # Process each file associated with the station
        log += '\nMerging ' + station_id + '\n'
        for fname in stations[station_id]:
            log += '\tProcessing ' + fname + '\n'
            # Retrieve and prep the data from the file.
            lines = [line.strip().split(',') for line in open(os.path.join(category, fname), 'r')][24:]
            # Load the data into a dictionary to screen out duplicated entries.
            # Assumption: lines have four entries.
            for line in (line for line in lines if len(line) == 4):
                station, date, stage, flow = line
                series[date] = (stage, flow)
        # Write the output unless the series has no entries.
        if len(series) == 0:
            log += '\tSeries has no entries\n'
            logheader += str.format('\t{0} ; {1}\n', station_id, station_names[station_id])
        else:
            # Prepare the output file and directory.
            merged_fname = str.format('{0} ; {1}', station_id, station_names[station_id])
            merged_dir = category + '_merged'
            # Ensure the output directory exists.
            if not os.path.exists(merged_dir):
                os.makedirs(merged_dir)
            # Write the merged series to a file.
            with open(os.path.join(merged_dir, merged_fname), 'w') as outF:
                outF.write(str.format('{0},{1},{2}\n', 'date', 'water level', 'flow'))
                outF.write(str.format('{0},{1},{2}\n', 'MST', 'm', 'm3/s'))
                for date, data in sorted(series.items()):
                    outF.write(str.format('{0},{1},{2}\n', date, stage, flow))
            log += '\tCreated ' + merged_fname + '\n'

# Ensure the log's output directory exists.
if not os.path.exists('logs'):
    os.makedirs('logs')
# Write the log
with open(str.format('logs/{0} ; merge.txt', today), 'w') as logF:
    logF.write(logheader + '\n\nFull Log:\n' + log)
