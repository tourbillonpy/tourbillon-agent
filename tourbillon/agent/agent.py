import functools
import glob
import inspect
import json
import logging
import os
import signal
import threading
from string import Template

import asyncio
from importlib import import_module
from influxdb import InfluxDBClient

logger = logging.getLogger(__name__)


TOURBILLON_HOME = os.path.normpath(os.path.dirname(__file__))


class Tourbillon(object):

    """docstring for ClassName"""

    def __init__(self, config_file):
        super(Tourbillon, self).__init__()
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        logging.basicConfig(level=self.config['log_level'],
                            format=self.config['log_format'])
        logger.info('Use config file: %s', config_file)
        self.tasks = []
        self.pluginconfig = {}

        t = Template(self.config['plugins_conf_dir'])
        plugin_conf_dir = t.safe_substitute(tourbillon_home=TOURBILLON_HOME)
        logger.info('Plugin config dir: %s', plugin_conf_dir)
        config_files = glob.glob(os.path.join(plugin_conf_dir,
                                              '*.conf'))
        for file_name in config_files:
            k = os.path.splitext(os.path.basename(file_name))[0]
            with open(file_name, 'r') as f:
                try:
                    self.pluginconfig[k] = json.load(f)
                except:
                    logger.exception('error loading config file %s', file_name)
        logger.info(self.pluginconfig)
        self._aio_run_event = asyncio.Event()
        self._thr_run_event = threading.Event()
        self.loop = asyncio.get_event_loop()
        self.influxdb = InfluxDBClient(**self.config['database'])

    def push(self, points, database):
        self.influxdb.write_points(points, database=database)

    @property
    def run_event(self):

        """get the asyncio.Event or threading.Event"""

        cf = inspect.currentframe()
        caller_name = cf.f_back.f_code.co_name
        caller = cf.f_back.f_globals[caller_name]
        if asyncio.iscoroutinefunction(caller) or asyncio.iscoroutine(caller):
            return self._aio_run_event
        else:
            return self._thr_run_event

    @asyncio.coroutine
    def async_push(self, points, database):
        yield from self.loop.run_in_executor(
            None,
            functools.partial(self.influxdb.write_points,
                              points, database=database))

    @asyncio.coroutine
    def async_create_database(self, name):
        yield from self.loop.run_in_executor(None,
                                             self.influxdb.create_database,
                                             name)

    @asyncio.coroutine
    def async_create_retention_policy(self, name, duration, replication,
                                      database):
        yield from self.loop.run_in_executor(
            None,
            functools.partial(self.influxdb.create_retention_policy,
                              name, duration, replication, database=database))

    def create_database(self, name):
        self.influxdb.create_database(name)

    def create_retention_policy(self, name, duration, replication, database):
        self.influxdb.create_retention_policy(name, duration, replication,
                                              database=database)

    def load_tasks(self):
        if 'plugins' not in self.config:
            logger.warn('no plugin configured.')
            return
        plugins = self.config['plugins']
        for module_name, functions in plugins.items():
            logger.debug('search for tasks in module %s', module_name)
            module = import_module(module_name)
            logger.debug('module %s successfully imported', module_name)
            for task_name in functions:
                logger.debug('checking declared task %s', task_name)
                if hasattr(module, task_name):
                    candidate_task = getattr(module, task_name)
                    task_type = ''
                    if asyncio.iscoroutinefunction(candidate_task):
                        self.tasks.append(asyncio.async(
                                          candidate_task(self)))
                        task_type = 'coroutine'
                    else:
                        self.tasks.append(self.loop.run_in_executor(
                                          None,
                                          candidate_task,
                                          self))
                        task_type = 'function'
                    logger.info('task found: %s.%s, type=%s',
                                module_name, task_name, task_type)
        logger.debug('configured tasks: %s', self.tasks)

    def stop(self):
        self.loop.remove_signal_handler(signal.SIGINT)
        self.loop.remove_signal_handler(signal.SIGTERM)
        logger.info('shutting down tourbillon...')
        self._aio_run_event.clear()
        self._thr_run_event.clear()

    def run(self):
        logger.info('starting tourbillon...')
        self.loop.add_signal_handler(signal.SIGINT, self.stop)
        self.loop.add_signal_handler(signal.SIGTERM, self.stop)
        self.load_tasks()
        self._aio_run_event.set()
        self._thr_run_event.set()
        logger.info('tourbillon started')
        self.loop.run_until_complete(asyncio.wait(self.tasks))
        logger.info('tourbillon shutdown completed')
