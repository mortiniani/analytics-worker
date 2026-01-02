import logging
import os
import json
from datetime import datetime
from typing import Dict

class AnalyticsWorker:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.handler = logging.StreamHandler()
        self.handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(self.handler)

    def process_data(self, data: Dict) -> Dict:
        """
        Process data and return the result.

        Args:
            data (Dict): Input data.

        Returns:
            Dict: Processed data.
        """
        try:
            # Load configuration
            config = self.config.get('config', {})

            # Extract relevant data
            timestamp = data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            metrics = data.get('metrics', {})

            # Process data
            processed_data = {
                'timestamp': timestamp,
                'metrics': {}
            }
            for metric, value in metrics.items():
                processed_data['metrics'][metric] = self._process_metric(value)

            return processed_data
        except Exception as e:
            self.logger.error(f'Error processing data: {e}')
            return {}

    def _process_metric(self, value: str) -> float:
        """
        Process a single metric value.

        Args:
            value (str): Metric value.

        Returns:
            float: Processed metric value.
        """
        try:
            # Convert value to float
            return float(value)
        except ValueError:
            self.logger.warning(f'Invalid metric value: {value}')
            return 0.0

def main():
    # Load configuration
    config_file = os.environ.get('CONFIG_FILE', 'config.json')
    with open(config_file, 'r') as f:
        config = json.load(f)

    # Create analytics worker
    analytics_worker = AnalyticsWorker(config)

    # Process data
    data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'metrics': {
            'metric1': '10.5',
            'metric2': '20.3'
        }
    }
    result = analytics_worker.process_data(data)

    # Log result
    analytics_worker.logger.info(json.dumps(result, indent=4))

if __name__ == '__main__':
    main()