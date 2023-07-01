#!/bin/python3

import datetime as dt
import sys

START_DAY = 0
YEAR = int(sys.argv[1]) if len(sys.argv) > 1 else dt.datetime.now().year
ONEDAY = dt.timedelta(days=1)

sun_col = (6 - START_DAY) % 7 + 1 + 2
sat_col = (6 - START_DAY - 1) % 7 + 1 + 2

print(
    """<!DOCTYPE html>
<html>
<head>
<title>YEAR Calendar</title>
<style>
body { font-family: sans-serif; }
table { border-collapse: collapse; }
th { background: #fafafa; }
td, th {
	font-size: 12px;
	padding: 4px 10px;
	text-align: right;
}
th:nth-child(2) { text-align: left; }
td:nth-child(2):not(:empty) {
	text-align: left;
	background: COLOR;
	border-top: solid 2px COLOR;
}
td:first-child, th:first-child { color: #aaa; }
td:nth-child(WEEKEND_1), th:nth-child(WEEKEND_1),
td:nth-child(WEEKEND_2), th:nth-child(WEEKEND_2) { color: #999; }
.first {
	border-left: solid 2px COLOR;
	background: linear-gradient(to bottom right, COLOR 25%, #ffff 60%);
}
.mend { border-bottom: solid 2px COLOR; }
.mstart { border-top: solid 2px COLOR; }
#cal { display: inline-block; }
h1 {
	text-align: right;
	margin: 5px 0;
}
h1::before {
	content: 'Calendar ';
	font-size: smaller;
	font-weight: lighter;
}
@page { margin: 0.5cm; }
</style>
</head>
<body>
""".replace(
        "YEAR", str(YEAR)
    )
    .replace("COLOR", "#CDE7F0")
    .replace("WEEKEND_1", str(sat_col))
    .replace("WEEKEND_2", str(sun_col))
)


def transform_start(start_date):
    while start_date.weekday() != (START_DAY % 7):
        start_date -= ONEDAY

    return start_date  # - ONEDAY * 7


def rotate(l, n):
    return l[n:] + l[:n]


start_date = transform_start(dt.date(YEAR, 1, 1))
end_date = dt.date(YEAR + 1, 1, 1)

weekdays = "</th><th>".join(
    ["#", "Month"] + rotate(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"], START_DAY)
)

print("<div id=cal>")
print(f"<h1>{YEAR}</h1>")
print("<table>")
print("<thead><tr><th>" + weekdays + "</th></tr></thead>")

while start_date <= end_date:
    print(f"<tr><td>{start_date.isocalendar()[1]}</td>")

    week_end = start_date + ONEDAY * 6
    has_first = week_end.day <= 7

    if (start_date.month == week_end.month) and (week_end.day < 14):
        print(f"<td>{start_date.strftime('%B')}</td>")
    else:
        print("<td></td>")

    for _ in range(0, 7):
        d = start_date.day

        classes = []
        if d == 1:
            classes += ["first"]

        if has_first and d <= 7:
            classes += ["mstart"]
        elif has_first and d >= 24:
            classes += ["mend"]

        classes = (' class="' + " ".join(classes) + '"') if len(classes) > 0 else ""
        print(f"<td{classes}>{d}</td>")

        start_date += ONEDAY

    print("</tr>")

print(
    """</table>
</div>
</body>
</html>
"""
)
