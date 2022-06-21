import api_calls as a
import classes as c
import csv
from datetime import datetime, timedelta

api_key = "b4523670d4ba81be1c6a2084776093eb"


# Update to desired filepath, but keep dynamic timestamp to avoid writing over your files
timestamp = datetime.now()
analysis_filepath = f'/Users/sethlipman/Desktop/RouteAnalysis/RouteAnalysis_{timestamp}.csv'

# Start time for driver - in GMT
# PST = GMT-7, CST = GMT-5, EST = GMT-4
epoch = datetime.utcfromtimestamp(0)
start_time = datetime.replace((datetime.today() + timedelta(1)), hour=13, minute=0, second=0, microsecond=0)
start_time_u = int((start_time - epoch).total_seconds() * 1000)


def analyze_routes(api_key, start_time_u):
    route_list = []
    workers = a.list_workers(api_key)

    for w in workers:
        w_id = w['id']
        route = c.Route(w_id, start_time_u)
        route.get_tasks(api_key)

        if len(route.tasks) > 0:
            route.route_length(api_key)
            route_dict = {'name': w['name'], 'no_stops': len(route.tasks), 'route_duration': route.route_length_time}

            print(route_dict)

            route_list.append(route_dict)

    with open(analysis_filepath, 'w') as f:
        fieldnames = ['name', 'no_stops', 'route_duration']
        wr = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        wr.writeheader()
        wr.writerows(route_list)

    print("Total number of routes: " + str(len(route_list)))
    return route_list


if __name__ == '__main__':
    analyze_routes(api_key, start_time_u)