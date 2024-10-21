import os
import time
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.worker.worker_task import worker_task

# Configure Conductor client settings
os.environ['CONDUCTOR_SERVER_URL'] = 'https://play.orkes.io/api'
os.environ['CONDUCTOR_AUTH_KEY'] = 'b1ff4f18-8e9a-11ef-85a8-ba73d777fd9d'
os.environ['CONDUCTOR_AUTH_SECRET'] = 'JmuUMAtDos9VonrvTru2cWVSKuhSViK9FbCBCbjlBAoa66c9'

# Define the worker task
@worker_task(task_definition_name='fetch_data')
def fetch_data(case_data: dict) -> dict:
    try:
        # Add your data processing logic here
        result = {
            'status': 'success',
            'message': f'Processed data for case: {case_data.get("case_id", "unknown")}',
            'data': case_data
        }
        return result
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'data': None
        }

def main():
    try:
        # Initialize Conductor configuration
        api_config = Configuration(
            server_api_url=os.getenv('CONDUCTOR_SERVER_URL'),
            debug=True,
            authentication_settings={
                'key': os.getenv('CONDUCTOR_AUTH_KEY'),
                'secret': os.getenv('CONDUCTOR_AUTH_SECRET')
            }
        )

        # Create task handler
        task_handler = TaskHandler(
            workers=[fetch_data],
            configuration=api_config,
            polling_interval_in_seconds=5.0
        )

        print("Starting worker task handler...")
        # Start polling for work
        task_handler.start_processes()

        try:
            # Keep the main thread running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping worker task handler...")
            # Stop polling for work
            task_handler.stop_processes()
            print("Worker task handler stopped.")

    except Exception as e:
        print(f"Error initializing worker: {str(e)}")
        raise

if __name__ == "__main__":
    main()
    