from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.worker.worker_task import worker_task
import os

os.environ['CONDUCTOR_SERVER_URL'] = 'https://play.orkes.io/api'
os.environ['CONDUCTOR_AUTH_KEY'] = 'b1ff4f18-8e9a-11ef-85a8-ba73d777fd9d'
os.environ['CONDUCTOR_AUTH_SECRET'] = 'JmuUMAtDos9VonrvTru2cWVSKuhSViK9FbCBCbjlBAoa66c9'

@worker_task(task_definition_name='fetch_data')
def greet(case_data: str) -> str:
    return f'Hello {case_data}'

api_config = Configuration()

task_handler = TaskHandler(configuration=api_config)
task_handler.start_processes() # starts polling for work
task_handler.stop_processes() # stops polling for work  

