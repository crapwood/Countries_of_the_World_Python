from csv import DictReader
from math import radians, cos, sin, asin, sqrt
import os

ISRAEL_LAT, ISRAEL_LON = 31.5, 34.75


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


os.makedirs("countries", exist_ok=True)
with open('cow.csv') as f, open('Country_Flags.csv') as country_flags, open('index.html', 'w') as page:
    reader = DictReader(f)
    flag_reader = DictReader(country_flags)
    countries = []
    for flag in flag_reader:
        countries.append([flag['ï»¿Country'], flag['ImageURL']])
    page.write(
        f"""<body style="font-family:monospace;color:white; text-align: justify; background:url(https://cdn.wallpapersafari.com/19/1/cqSuKw.jpg);background-size:100% 100%; ">
                   <table>
                        <th>Flag</th>
                        <th align="left">Country</th>
                        <th>Distance From Israel</th>""")
    for d in reader:
        with open(f"countries/{d['short_name']}.html", 'w') as country_html:
            for i, x in enumerate(countries):
                found = False
                if d['name'] in x[0]:
                    found = True
                    country_html.write(f"""
                            <html>
                            <head>
                                <title>{d['name']}</title>
                            </head>
                            <body style="font-family:monospace;color:black; text-align:center; background:url({x[1]});background-size:cover; height: 100vh;">
                            <h1>{d['name']}</h1>
                            <dl>     
                                <h3>Capital</h3>
                                <h4>{d['capital']}</h4>
                            
                                <h3>Population</h3>
                                <h4>{int(d['population']):,d}</h4>
                            
                                <h3>Land Area</h3>
                                <h4>{d['land']} km<sup>2</sup></h4>
                            
                                <h3>Continent</h3>
                                <h4>{d['continent']}</h4>
                            </dl>
                            </body>
                            </html>""")
                    break
            if not found:
                country_html.write(f"""
                                <html>
                                <head>
                                    <title>{d['name']}</title>
                                </head>
                                <body style="font-family:monospace;color:black; text-align: center; 
                                    background-color:white; height: 100vh;"> 
                                <h1>{d['name']}</h1>
                                <dl>     
                                    <dt>Capital</dt>
                                    <p>{d['capital']}</p>                      
                                    <dt>Population</dt>
                                    <p>{int(d['population']):,d}</p>                       
                                    <dt>Land Area</dt>
                                    <p>{d['land']} km<sup>2</sup></p>                      
                                    <dt>Continent</dt>
                                    <p>{d['continent']}</p>
                                </dl>
                                </body>
                                </html>""")

        page.write(f"""<tr> <td><img src=\"http://static.10x.org.il/flags/{d['short_name'].lower()}.png\"></td>
                                <td> <a style="color:tomato;text-decoration:none" href="countries/{d['short_name']}.html">{d['name']}</a> </td>
                                <td> {haversine(ISRAEL_LON, ISRAEL_LON, float(d['lon']), float(d['lat'])):.2f} km 
                                </td> </tr>""") 
    page.write("</table></body>")
