import time
import json
import os
import random
import sys
from locust import HttpUser, task, between, SequentialTaskSet

# Get config file.
cur_env = os.getenv('WP_STRESS_TEST')
config = 'settings.json' if None == cur_env else "settings-%s.json" % ( cur_env )
config_file = open(config, 'r')
settings = json.load(config_file)

# Set basic auth.
auth_config = None
if settings.get('auth'):
    auth_user = settings['auth'].get('user')
    auth_pass = settings['auth'].get('pass')
    if auth_user and auth_pass:
        auth_config = ( auth_user, auth_pass )

# Set wait_time
wait_time = [ 1, 3 ]
if settings.get('wait'):
    if settings['wait'].get('min'):
        wait_time[0] = settings['wait']['min']
    if settings['wait'].get('max'):
        wait_time[1] = settings['wait']['max']

# Set requests.
archive_pages = []
single_pages = []
if settings.get('requests'):
    if settings['requests'].get('archives'):
        archive_pages = settings['requests']['archives']
    if settings['requests'].get('singles'):
        single_pages = settings['requests']['singles']

# Define task
class WpStressTestTasks(SequentialTaskSet):

    wait_time = between(wait_time[0], wait_time[1])
    
    auth = auth_config
    
    archives = archive_pages
    
    singles = single_pages
    
    def req(self, path):
        self.client.get( path, auth=self.auth, verify=False) 

    @task
    def view_root(self):
        self.req("/")

    @task
    def view_archive(self):
        self.req(random.choice(self.archives))
    
    @task
    def view_single(self):
        self.req(random.choice(self.singles))


# Define user.
class WpStressTestUser(HttpUser):
    tasks = {WpStressTestTasks}
