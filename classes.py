import api_calls as a
from haversine import haversine, Unit


class Route:

    def __init__(self, worker, start_time_u):
        self.worker = worker
        self.start_time = start_time_u
        self.tasks = []
        self.last_task = None
        self.total_duration = None
        self.task_count = None
        self.total_distance = 0

    def get_tasks(self, api_key):
        worker_data = a.get_single_worker(api_key, workerid=self.worker)

        self.tasks = self.tasks + worker_data['tasks']

        if len(worker_data['tasks']) > 0:
            self.task_count = len(worker_data['tasks'])
            self.last_task = worker_data['tasks'][-1]

        return

    def route_duration(self, api_key):
        last_task = a.get_single_task(api_key, self.last_task)

        estimated_completion_time = last_task['estimatedCompletionTime']

        self.total_duration = int((estimated_completion_time - self.start_time) / 60000)  # minutes

        return

    def route_distance(self, api_key):

        i = 0
        while i < (len(self.tasks) - 1):
            preceding_task_id = self.tasks[i]
            following_task_id = self.tasks[i + 1]

            start_coordinates_lon = a.get_single_task(api_key, preceding_task_id)['destination']['location'][0]
            start_coordinates_lat = a.get_single_task(api_key, preceding_task_id)['destination']['location'][1]
            end_coordinates_lon = a.get_single_task(api_key, following_task_id)['destination']['location'][0]
            end_coordinates_lat = a.get_single_task(api_key, following_task_id)['destination']['location'][1]

            distance_miles = haversine((start_coordinates_lon, start_coordinates_lat),
                                       (end_coordinates_lon, end_coordinates_lat), unit='mi')

            self.total_distance = self.total_distance + distance_miles

            i += 1

        return





