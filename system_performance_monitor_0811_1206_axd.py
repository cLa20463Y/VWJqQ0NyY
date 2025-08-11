# 代码生成时间: 2025-08-11 12:06:41
# system_performance_monitor.py

"""
A Pyramid-based web application for monitoring system performance.
"""

from pyramid.config import Configurator
from pyramid.response import Response
import psutil
import json

# Constants for system performance metrics
CPU_USAGE_METRICS = ['cpu_percent', 'cpu_count_logical']
MEMORY_METRICS = ['memory_percent', 'memory_total', 'memory_available']
DISK_METRICS = ['disk_partitions', 'disk_usage']
NETWORK_METRICS = ['net_io_counters', 'net_connections']


class SystemPerformanceMonitor(object):
    """
    This class is responsible for collecting system performance data.
    """
    def get_cpu_usage(self):
        """Get CPU usage metrics."""
        return {metric: psutil.cpu_percent(interval=None, percpu=True) if metric == 'cpu_percent' else getattr(psutil, f'cpu_count_{metric}')() for metric in CPU_USAGE_METRICS}

    def get_memory_usage(self):
        """Get memory usage metrics."""
        return {metric: psutil.virtual_memory()[metric] for metric in MEMORY_METRICS}

    def get_disk_usage(self):
        """Get disk usage metrics."""
        return {metric: psutil.disk_partitions() if metric == 'disk_partitions' else psutil.disk_usage('/') for metric in DISK_METRICS}

    def get_network_usage(self):
        """Get network usage metrics."""
        return {metric: psutil.net_io_counters(pernic=True) if metric == 'net_io_counters' else psutil.net_connections(kind='all') for metric in NETWORK_METRICS}



def system_performance_view(request):
    """
    A Pyramid view that returns system performance data in JSON format.
    """
    try:
        # Initialize the SystemPerformanceMonitor object
        monitor = SystemPerformanceMonitor()

        # Collect system performance metrics
        cpu_data = monitor.get_cpu_usage()
        memory_data = monitor.get_memory_usage()
        disk_data = monitor.get_disk_usage()
        network_data = monitor.get_network_usage()

        # Combine all metrics into a single dictionary
        data = {
            'cpu_usage': cpu_data,
            'memory_usage': memory_data,
            'disk_usage': disk_data,
            'network_usage': network_data
        }

        # Return the data in JSON format
        return Response(json.dumps(data), content_type='application/json')
    except Exception as e:
        # Handle any exceptions and return a JSON error message
        return Response(json.dumps({'error': str(e)}), content_type='application/json', status=500)


if __name__ == '__main__':
    # Configure the Pyramid application
    with Configurator() as config:
        # Add the system performance view
        config.add_route('system_performance', '/performance')
        config.add_view(system_performance_view, route_name='system_performance')
        config.scan()

        # Run the Pyramid application
        config.run()