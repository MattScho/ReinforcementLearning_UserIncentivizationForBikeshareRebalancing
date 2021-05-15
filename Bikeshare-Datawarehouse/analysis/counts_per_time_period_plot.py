import matplotlib.pyplot as plt
'''
Plot temporal data

:author: Matthew Schofield
'''

# Settings for plot
plt.set_cmap('jet')


# Raw data pre-computed, kindof messy
years = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
counts_per_year = [1226767, 2028911, 2555541, 2913150, 3185906, 3333994, 3757777, 3542684, 3398417]

year_months = ['2011 Jan.', '2011 Feb.', '2011 Mar.', '2011 Apr.', '2011 May', '2011 Jun.', '2011 July', '2011 Aug.', '2011 Sept.', '2011 Oct.', '2011 Nov.', '2011 Dec.', '2012 Jan.', '2012 Feb.', '2012 Mar.', '2012 Apr.', '2012 May', '2012 Jun.', '2012 July', '2012 Aug.', '2012 Sept.', '2012 Oct.', '2012 Nov.', '2012 Dec.', '2013 Jan.', '2013 Feb.', '2013 Mar.', '2013 Apr.', '2013 May', '2013 Jun.', '2013 July', '2013 Aug.', '2013 Sept.', '2013 Oct.', '2013 Nov.', '2013 Dec.', '2014 Jan.', '2014 Feb.', '2014 Mar.', '2014 Apr.', '2014 May', '2014 Jun.', '2014 July', '2014 Aug.', '2014 Sept.', '2014 Oct.', '2014 Nov.', '2014 Dec.', '2015 Jan.', '2015 Feb.', '2015 Mar.', '2015 Apr.', '2015 May', '2015 Jun.', '2015 July', '2015 Aug.', '2015 Sept.', '2015 Oct.', '2015 Nov.', '2015 Dec.', '2016 Jan.', '2016 Feb.', '2016 Mar.', '2016 Apr.', '2016 May', '2016 Jun.', '2016 July', '2016 Aug.', '2016 Sept.', '2016 Oct.', '2016 Nov.', '2016 Dec.', '2017 Jan.', '2017 Feb.', '2017 Mar.', '2017 Apr.', '2017 May', '2017 Jun.', '2017 July', '2017 Aug.', '2017 Sept.', '2017 Oct.', '2017 Nov.', '2017 Dec.', '2018 Jan.', '2018 Feb.', '2018 Mar.', '2018 Apr.', '2018 May', '2018 Jun.', '2018 July', '2018 Aug.', '2018 Sept.', '2018 Oct.', '2018 Nov.', '2018 Dec.', '2019 Jan.', '2019 Feb.', '2019 Mar.', '2019 Apr.', '2019 May', '2019 Jun.', '2019 July', '2019 Aug.', '2019 Sept.', '2019 Oct.', '2019 Nov.', '2019 Dec.']
counts_per_year_months = [37503, 47558, 63195, 93100, 133785, 141743, 139578, 135020, 125901, 122048, 101024, 86312, 95871, 102235, 163211, 172478, 193718, 200636, 201560, 212093, 216264, 196901, 151328, 122616, 124989, 110102, 157366, 236442, 250463, 253767, 268016, 288793, 281937, 254649, 192417, 136600, 112697, 122663, 165762, 269511, 306734, 316574, 327833, 320870, 323936, 297962, 197048, 151560, 127411, 108052, 188256, 318340, 367185, 314293, 364015, 364313, 328038, 290351, 228295, 187357, 123252, 145654, 283493, 285516, 288720, 368097, 366458, 357328, 344408, 343243, 259106, 168719, 174804, 226303, 245403, 365990, 339677, 398751, 397680, 402534, 391371, 384833, 252534, 177897, 168590, 182378, 238998, 328907, 374115, 392338, 404761, 403866, 325800, 343021, 202376, 177534, 150780, 158130, 253811, 347992, 337704, 350144, 356645, 360044, 360225, 337552, 223512, 161878]

months = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']
average_trips_month = [148967.4, 164103.4, 241992.2, 329349.0, 341480.2, 364724.6, 377911.8, 377617.0, 349968.4, 339800.0, 233164.6, 174677.0]

year_weekdays = ['2015 Sat.', '2015 Mon.', '2015 Tues.', '2015 Wed.', '2015 Thurs.', '2015 Fri.', '2015 Sun.', '2016 Sat.', '2016 Mon.', '2016 Tues.', '2016 Wed.', '2016 Thurs.', '2016 Fri.', '2016 Sun.', '2017 Sat.', '2017 Mon.', '2017 Tues.', '2017 Wed.', '2017 Thurs.', '2017 Fri.', '2017 Sun.', '2018 Sat.', '2018 Mon.', '2018 Tues.', '2018 Wed.', '2018 Thurs.', '2018 Fri.', '2018 Sun.', '2019 Sat.', '2019 Mon.', '2019 Tues.', '2019 Wed.', '2019 Thurs.', '2019 Fri.', '2019 Sun.']
counts_per_year_weekdays = [431605, 447453, 457960, 478829, 460489, 473865, 435705, 419646, 465177, 495809, 510143, 494961, 502056, 446202, 502867, 517282, 551236, 572901, 551710, 541036, 520745, 436512, 495089, 511839, 534591, 536119, 526133, 502401, 399959, 465170, 510178, 513457, 503090, 510515, 496048]

hours = [h+1 for h in list(range(24))]
average_trips_hour = [521.6973180076628, 297.8199233716475, 185.04980842911877, 93.19157088122606, 88.21072796934865, 432.5938697318008, 1422.83908045977, 3587.904214559387, 5590.862068965517, 3353.7471264367814, 2672.8735632183907, 3132.2605363984676, 3689.27969348659, 3702.590038314176, 3612.8352490421457, 4027.4865900383143, 5065.16091954023, 7243.199233716475, 5983.766283524904, 4049.7816091954023, 2805.256704980843, 2040.1340996168583, 1474.521072796935, 916.9501915708812]
# Normalize
average_trips_hour = [hour/sum(average_trips_hour) for hour in average_trips_hour]

duration_bins = [0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3300]
durations = [2501212, 4905246, 3416547, 2191858, 1433656, 878392, 408472, 232391, 165650, 133135, 113514, 95586]

# Plot data
# Yearly activity plot
plt.plot(years, counts_per_year, marker='o', mec='y', mfc='y', linestyle="--", linewidth=5, markersize=16)
plt.yticks(list(range(1000000, 4000001, 500000)), labels=["{:,}".format(elem) for elem in list(range(1000000, 4000001, 500000))], fontsize=24)
plt.xticks(years, labels=years, fontsize=24)
plt.xlabel("Year", fontsize=24)
plt.ylabel("Trips", fontsize=24)
plt.title("Trips per Year in the Capital Bikeshare System 2011-2019", fontsize=32)
plt.show()

# Monthly activity plot
plt.plot(year_months, counts_per_year_months, marker='o', mec='y', mfc='y',  linestyle="--", linewidth=5, markersize=16)
plt.yticks(list(range(0, 400000, 100000)), labels=list(range(0, 400000, 100000)), fontsize=24)
plt.xticks(range(0, 9*12, 12), labels=years, fontsize=24)
plt.xlabel("Month", fontsize=24)
plt.ylabel("Trips", fontsize=24)
plt.title("Trips per Month in the Capital Bikeshare System 2011-2019", fontsize=32)
plt.show()

# Average monthly plot
plt.plot(months, average_trips_month, marker='o', mec='y', mfc='y',  linestyle="--", linewidth=5, markersize=16)
plt.yticks(list(range(0, 400001, 100000)), labels=["{:,}".format(elem) for elem in list(range(0, 400001, 100000))], fontsize=24)
plt.xticks(range(len(months)), labels=months, fontsize=24)
plt.xlabel("Month", fontsize=24)
plt.ylabel("Average Trips", fontsize=24)
plt.title("Average Trips per Month in the Capital Bikeshare System 2015-2019", fontsize=32)
plt.show()

# Weekday per year plot
weekday_count = [0 for _ in range(7)]
for i, weekday in enumerate(["Sat.", "Mon.", "Tues.", "Wed.", "Thurs.", "Fri.", "Sun."]):
    for j, year_weekday in enumerate(year_weekdays):
        if weekday in year_weekday:
            weekday_count[i] += counts_per_year_weekdays[j]

weekday_count = [cnt/5 for cnt in weekday_count]
weekday_count = [cnt/sum(weekday_count) for cnt in weekday_count]

# Trips per weekday
plt.plot(range(7), weekday_count, marker='o', mec='y', mfc='y',  linestyle="--", linewidth=5, markersize=16)
plt.yticks([0.0, 0.05, 0.1, 0.15, 0.2], labels=["0%", "5%", "10%", "15%", "20%"], fontsize=24)
plt.xticks(range(7), labels=["Sat.", "Mon.", "Tues.", "Wed.", "Thurs.", "Fri.", "Sun."], fontsize=24)
plt.xlabel("Weekday", fontsize=24)
plt.ylabel("Relative Trips", fontsize=24)
plt.title("Trips per Weekday in the Capital Bikeshare System 2015-2019", fontsize=32)
plt.show()

# Average hourly plot
plt.plot(hours, average_trips_hour, marker='o', mec='y', mfc='y',  linestyle="--", linewidth=5, markersize=16)
plt.yticks([0.0, 0.03, 0.06, 0.09, 0.12], labels=["0%", "3%", "6%", "9%", "12%"], fontsize=24)
plt.xticks(hours, labels=hours, fontsize=24)
plt.xlabel("Hour", fontsize=24)
plt.ylabel("Relative Trips", fontsize=24)
plt.title("Average Trips per Hour in the Capital Bikeshare System 2015-2019", fontsize=32)
plt.show()

# Duration histogram plot
trips_2015_2019 = sum(counts_per_year[4:])
plt.bar(range(len(durations)), [dur/trips_2015_2019 for dur in durations])
plt.yticks([0.0, 0.1, 0.2, 0.3], labels=[0.0, 0.1, 0.2, 0.3], fontsize=24)
plt.xticks(range(len(durations)), labels=[int(dur/60 + 5) for dur in duration_bins], fontsize=24)
plt.xlabel("Duration Bin (Minutes)", fontsize=24)
plt.ylabel("Percentage of Trips", fontsize=24)
plt.title("Trip Duration Histogram in the Capital Bikeshare System 2015-2019", fontsize=32)
plt.show()