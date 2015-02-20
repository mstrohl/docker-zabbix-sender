# encoding: utf-8

"""Provides collection of events emitters"""

import time
from . import EndPoint

def containers_count(host_fqdn, docker_client, statistics):
    """
    Emit events providing:
      - number of containers
      - number of running containers
      - number of crashed containers

    :param host_fqdn: FQDN of the host where the docker-zabbix-daemon is running, for instance docker.acme.com
    :type host_fqdn: string

    :param docker_client: instance of docker.Client see http://docker-py.readthedocs.org/en/latest/api/
    :type docker_client: docker.Client

    :param statistics: List of dicts providing collected container statistics. see Docker stats API call on https://docs.docker.com/reference/api/docker_remote_api_v1.17/#get-container-stats-based-on-resource-usage

    :return: list of dicts providing additional events to push to Zabbix.
    Each dict is composed of 4 keys:
        - hostname
        - timestamp
        - key
        - value
    """
    running = 0
    crashed = 0
    now = int(time.time())
    containers = docker_client.containers(all=True)
    for container in containers:
        status = container['Status']
        if status.startswith('Up'):
            running += 1
        elif not status.startswith('Exited (0)'):
            crashed += 1
    data = {
        'all': len(containers),
        'running': running,
        'crashed': crashed,
    }
    return [
        {
            'hostname': '-',
            'timestamp': now,
            'key': EndPoint.EVENT_KEY_PREFIX + 'count.' + key,
            'value': value
        }
        for key, value in data.items()
    ]
