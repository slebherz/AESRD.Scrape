# Retrieves data from Alberta Environment's website.
# Assumptions:
#   1. The station lists are up to date.
#   2. The url pattern for retrieving .csv data is up to date.
import os
import urllib
import datetime

# Declaration of each data category, url, and list of sites for streamflow,
# precipitation, snowpack, and reservoir levels.
input = [
    ('flow', 'http://www.environment.alberta.ca/apps/Basins/data/text/river/',
        [('Bearspaw Diversion','05BH911'),
        ('Bow River at Banff','05BB001'),
        ('Bow River at Calgary','05BH004'),
        ('Bow River at Lake Louise','05BA001'),
        ('Bow River below Bassano Dam','05BM004'),
        ('Bow River below Carseland Dam','05BM002'),
        ('Bow River near the Mouth','05BN012'),
        ('Crowfoot Creek near Cluny','05BM008'),
        ('Elbow River at Bragg Creek','05BJ004'),
        ('Elbow River at Sarcee Bridge','05BJ010'),
        ('Elbow River below Glenmore Dam','05BJ001'),
        ('Ghost River above Waiparous Creek','05BG010'),
        ('Glenmore Diversion','05BJ917'),
        ('Highwood Diversion Canal near Headgates','05BL025'),
        ('Highwood River near the Mouth','05BL024'),
        ('Little Bow Canal at High River','05BL015'),
        ('Nose Creek above Airdrie','05BH014'),
        ('Pipestone River near Lake Louise','05BA002'),
        ('Sheep River at Okotoks','05BL012'),
        ('Spray River at Banff','05BC001'),
        ('Stimson Creek near Pekisko','05BL007'),
        ('Threepoint Creek near Millarville','05BL013'),
        ('Twelve Mile Creek near Cecil','05BN002'),
        ('Waiparous Creek near the Mouth','05BG006'),
        ('Western Irrigation District Canal near Headgates','05BM015')]),
    
    ('meteor', 'http://www.environment.alberta.ca/apps/Basins/data/text/meteor/', 
        [('Azur - AARD','05AC802'),
        ('Banff - MSC','MSC-001'),
        ('Bassano - AARD','05CJ802'),
        ('Black Diamond - AARD','05BL815'),
        ('Bow Summit','05BA813'),
        ('Bow Valley Provincial Park - MSC','MSC-005'),
        ('Brook CDA Met Site - MSC','MSC-006'),
        ('Burns Creek','05BL813'),
        ('Canmore Meteorological Site - TAU','TAU-010'),
        ('Cascade Reservoir - Tau','TAU-002'),
        ('Compression Ridge','05BJ806'),
        ('Cop Upper - MSC','MSC-013'),
        ('Cox Hill','05BH803'),
        ('Cuthead Lake','05BD801'),
        ('Elbow Ranger Station','05BJ804'),
        ('Evan Thomas Creek','05BF825'),
        ('Forget-me-not Mountain','05BL809'),
        ('Ghost Diversion','05BG802'),
        ('Ghost Lake near Cochrane','05BE005'),
        ('Ghost RS','05BG801'),
        ('Gleichen - AARD','05BM801'),
        ('Jumpingpound  Ranger Station','05BH802'),
        ('Lake Louise - MSC','MSC-028'),
        ('Lathom - AGCM','05CJ806'),
        ('Little Elbow Summit','05BJ805'),
        ('Lost Creek South','05BL811'),
        ('Lower Kananaskis Lake','05BF009'),
        ('Mossleigh - AARD','05BM802'),
        ('Mount Odlum','05BL812'),
        ('Neir - AARD','05BH804'),
        ('Pekisko','05BL814'),
        ('Pika Run','05BA815'),
        ('Priddis Observatory - AARD','05BF827'),
        ('Queenstown - AARD','05AC801'),
        ('Rolling Hills - AARD','05BN801'),
        ('Rosemary - AARD','05CJ804'),
        ('Sheep River II','05BL810'),
        ('South Ghost Headwaters','05BG803'),
        ('Spray Reservoir at Three Sisters Dam','05BC006'),
        ('Strathmore - AARD','05CE808'),
        ('Sullivan Creek','05BL807'),
        ('Sunshine Village','05BB803'),
        ('Three Isle Lake','05BF824')]),
        
    ('snow', 'http://www.environment.alberta.ca/apps/Basins/data/text/snow/',
        [('Akamina Pass','05AD803'),
        ('Akamina Pass','05AD803'),
        ('Flattop Mountain - Snotel','13A19S'),
        ('Gardiner Creek','05AA809'),
        ('Limestone Ridge','05DB802'),
        ('Little Elbow Summit','05BJ805'),
        ('Lost Creek South','05BL811'),
        ('Many Glacier - Snotel','13A27S'),
        ('Mount Odlum','05BL812'),
        ('Skoki Lodge','05CA805'),
        ('South Racehorse Creek','05AA817'),
        ('Sunshine Village','05BB803'),
        ('Three Isle Lake','05BF824')]),
        
    ('lake_level', 'http://www.environment.alberta.ca/apps/Basins/data/text/lake/',
        [('Barrier Lake near Seebe','05BF024'),
        ('Bassano Forebay','05BM907'),
        ('Bearspaw Reservoir near Calgary','05BH010'),
        ('Cascade Reservoir - Tau','TAU-002'),
        ('Chestermere Lake at South Outlet','05BM904'),
        ('Ghost Lake near Cochrane','05BE005'),
        ('Glenmore Reservoir at Calgary','05BJ008'),
        ('Horseshoe Forebay - Tau','TAU-004'),
        ('Lake Newell','05BN901'),
        ('Lower Kananaskis Lake','05BF009'),
        ('Spray Reservoir at Three Sisters Dam','05BC006'),
        ('Upper Kananaskis Lake','05BF005')])]

today = datetime.date.today().isoformat()
log = 'The following data could not be retrieved:\n'

# Process each data category.
for category, url, sites in input:
    # Ensure the output directory exists.
    if not os.path.exists(category):
        os.makedirs(category)

    # Download the data in .csv format for each site.
    for name, id in sites:
        site_url = str.format('{0}{1}.csv', url, id)
        csv_path = str.format('{0}/{1} ; {2} ; {3}.csv', 
            category, today, id, name)
        if urllib.urlopen(site_url).getcode() == 404:
            log += str.format('{0} ({1})\n', site_url, name)
        else:
            print csv_path
            urllib.urlretrieve(site_url, csv_path)
            
# Ensure the log's output directory exists.
if not os.path.exists('logs'):
    os.makedirs('logs')
# Write the log
with open(str.format('logs/{0} ; scrape.txt', today), 'w') as logF:
    logF.write(log)