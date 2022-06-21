import api_calls as r


class Route:

    def __init__(self, worker, start_time_u):
        self.worker = worker
        self.start_time = start_time_u
        self.tasks = []
        self.last_task = None
        self.route_length_time = None
        self.task_count = None

    def get_tasks(self, api_key):
        worker_data = r.get_single_worker(api_key, workerid=self.worker)

        self.tasks = self.tasks + worker_data['tasks']

        if len(worker_data['tasks']) > 0:
            self.task_count = len(worker_data['tasks'])
            self.last_task = worker_data['tasks'][-1]

        return

    def route_length(self, api_key):
        last_task = r.get_single_task(api_key, self.last_task)

        estimated_completion_time = last_task['estimatedCompletionTime']

        self.route_length_time = int((estimated_completion_time - self.start_time) / 60000)  # minutes

        return





