# Representative railway GTFS fixture

This is a synthetic CC0 fixture created for TravelManager. It is not copied
from a live timetable and must not be used as passenger information.

It deliberately contains:

- an overnight trip using a time greater than `24:00:00`;
- a weekday service removed on 2030-01-01 and a special service added that day;
- one parent station with two distinct platforms at identical coordinates;
- separate pickup and drop-off restrictions;
- a small shape shared by the test trip.
