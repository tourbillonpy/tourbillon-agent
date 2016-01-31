#!/usr/bin/env python
import json
import os
import sys

import click
import pip
import six
from importlib import import_module
from six.moves.urllib.request import urlopen
# try:
#     from urllib.request import urlopen
# except ImportError:
#     from urllib import urlopen
from terminaltables import AsciiTable

# PY34_PLUS = sys.version_info[0] == 3 and sys.version_info[1] >= 4
# PY27 = sys.version_info[0] == 2 and sys.version_info[1] == 7

LOG_FORMAT_EX = '%(asctime)s %(levelname)s [%(name)s %(filename)s:'\
    '%(funcName)s:%(lineno)d] %(message)s'
LOG_FORMAT_NO = '%(asctime)s %(levelname)s %(message)s'
LOG_FILENAME = '/var/log/tourbillon/tourbillon.log'

INDEX_FILE_URL = 'https://raw.githubusercontent.com/tourbillon-python/'\
    'tourbillon-agent/master/meta/plugin_index.json'


def get_index():
    data = urlopen(INDEX_FILE_URL).read().decode()

    names = []
    table = [['name', 'version', 'description', 'author', 'f']]
    for name, meta in json.loads(data).items():
        if six.PY3 and meta['py3'] or six.PY2 and meta['py2']:
            names.append(name)
            table.append([
                name,
                meta['version'],
                meta['description'],
                meta['author'],
                '*' if meta['featured'] else ''
            ])
    return names, table


@click.group()
@click.version_option(version='0.1')
@click.option('--config',
              '-c',
              type=click.Path(exists=False,
                              file_okay=True,
                              dir_okay=False,
                              writable=False,
                              resolve_path=True),
              default='/etc/tourbillon/tourbillon.conf',
              help='specify a different config file',
              metavar='<config_file>')
@click.option('--pidfile',
              '-p',
              type=click.Path(exists=False,
                              file_okay=True,
                              dir_okay=False,
                              writable=False,
                              resolve_path=True),
              default='/var/run/tourbillon/tourbillon.pid',
              help='specify a different pidfile file',
              metavar='<pidfile_file>')
def cli(config, pidfile):
    """tourbillon: send metrics to an influxdb"""
    pass


@cli.command()
@click.pass_context
def init(ctx):
    """initialize the tourbillon configuration"""
    config_file = ctx.parent.params['config']
    click.echo(click.style('\nConfigure Tourbillon agent\n',
                           fg='blue', bold=True, underline=True))
    click.echo(click.style('InfluxDB configuration\n',
                           fg='magenta', underline=True))
    host = click.prompt('Enter the InfluxDB hostname', default='localhost')
    port = click.prompt('Enter the InfluxDB port', default=8086, type=int)
    username = click.prompt('Enter the InfluxDB username [Enter for no auth]',
                            default='',
                            show_default=False)
    password = None
    if username:
        password = click.prompt('Enter the InfluxDB password',
                                hide_input=True,
                                confirmation_prompt=True)

    click.echo(click.style('\nLogging configuration\n',
                           fg='magenta', underline=True))
    log_level = click.prompt('Enter the log level', type=click.Choice([
                             'CRITICAL',
                             'ERROR',
                             'WARNING',
                             'INFO',
                             'DEBUG'
                             ]), default='INFO')
    log_format = click.prompt('Enter the log format', type=click.Choice([
        'default',
        'extended']), default='default')

    log_file = click.prompt('Enter the log filename', default=LOG_FILENAME)

    fmt = LOG_FORMAT_NO if log_format == 'default' else LOG_FORMAT_EX
    config = {
        'database': {
            'host': host,
            'port': port
        },
        'log_format': fmt,
        'log_level': log_level,
        'log_file': log_file,
        'plugins_conf_dir': '${tourbillon_conf_dir}/conf.d'
    }
    if username:
        config['database']['username'] = username
        config['database']['password'] = password

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)

    click.echo(click.style('\nconfiguration file generated\n', fg='green'))


@cli.command()
@click.pass_context
@click.option('--compact', default=False, is_flag=True)
def list(ctx, compact):
    """list available tourbillon plugins"""
    names, table = get_index()

    if compact:
        for name in names:
            print(name)
    else:
        at = AsciiTable(table)
        at.justify_columns = {
            0: 'left',
            1: 'center',
            2: 'left',
            3: 'left',
            4: 'center'
        }
        print(at.table)


@cli.command()
@click.pass_context
@click.argument('plugin', nargs=1, required=True)
def install(ctx, plugin):
    """install tourbillon plugin"""
    index = get_index()
    if plugin not in index:
        click.echo(click.style(
                   'plugin {} not found!'.format(plugin), fg='red'))
        return
    pip_args = ['install']
    meta = index[plugin]
    if 'pip_cmd' in meta:
        plugin = meta['pip_cmd']
    else:
        plugin = '{}=={}'.format(plugin, meta['version'])
    pip_args.append(plugin)
    pip.main(pip_args)


@cli.command()
@click.pass_context
@click.argument('plugin', nargs=1, required=True)
def upgrade(ctx, plugin):
    """upgrade tourbillon plugin"""
    index = get_index()
    if plugin not in index:
        click.echo(click.style(
                   'plugin {} not found!'.format(plugin), fg='red'))
        return
    pip_args = ['install']
    meta = index[plugin]
    if 'pip_cmd' in meta:
        plugin = meta['pip_cmd']
    else:
        plugin = '{}=={}'.format(plugin, meta['version'])
    pip_args = ['install', '-U']
    pip_args.append(plugin)
    pip.main(pip_args)


@cli.command()
@click.pass_context
@click.argument('plugin', nargs=1, required=True)
def reinstall(ctx, plugin):
    """reinstall tourbillon plugin"""
    index = get_index()
    if plugin not in index:
        click.echo(click.style(
                   'plugin {} not found!'.format(plugin), fg='red'))
        return
    pip_args = ['install']
    meta = index[plugin]
    if 'pip_cmd' in meta:
        plugin = meta['pip_cmd']
    else:
        plugin = '{}=={}'.format(plugin, meta['version'])
    pip_args = ['install', '--force-reinstall', '-U']
    pip_args.append(plugin)
    pip.main(pip_args)


@cli.command()
@click.pass_context
def show(ctx):
    """show the list of enabled plugins"""
    config_file = ctx.parent.params['config']
    with open(config_file, 'r') as f:
        config = json.load(f)

    if 'plugins' not in config:
        click.echo('no enabled plugins')
        return

    for key, value in config['plugins'].items():
        click.echo('module: {0} - functions: {1}'.format(
                   key, ', '.join(value)))


@cli.command()
@click.pass_context
def clear(ctx):
    """remove all plugins from configuration"""
    config_file = ctx.parent.params['config']
    with open(config_file, 'r') as f:
        config = json.load(f)

    if 'plugins' in config:
        del config['plugins']
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2, sort_keys=True)

    click.echo('All plugins removed')


def validate_plugins(ctx, param, value):
    result = {}
    for v in value:
        if '=' not in v:
            raise click.BadParameter('plugin %s in not valid' % v)
        module, functions = v.replace(' ', '').split('=')
        result[module] = functions.split(',')
    return result


@cli.command(short_help='enable one or more plugins')
@click.pass_context
@click.argument('plugins', nargs=-1, required=True,
                callback=validate_plugins)
def enable(ctx, plugins):
    """Enable one or more plugins

PLUGINS are expressed in the form:

    module1.submodule1=function1,function2,... module2=function3,...

Example:

    tourbillon enable tourbillon.linux=get_cpu_usage,get_mem_usage

Enable the functions get_cpu_usage and get_mem_usage of the
'tourbillon.linux' plugin.
    """
    config_file = ctx.parent.params['config']
    with open(config_file, 'r') as f:
        config = json.load(f)
    if 'plugins' not in config:
        config['plugins'] = {}

    for module, functions in plugins.items():
        try:
            m = import_module(module)
        except:
            click.echo('module %s does not exists' % module)
            continue
        if module not in config['plugins']:
            config['plugins'][module] = []
        for f in functions:
            if not hasattr(m, f):
                click.echo('module %s does not contains %s' % (module, f))
                continue
            if f not in config['plugins'][module]:
                config['plugins'][module].append(f)

        if len(config['plugins'][module]) == 0:
            del config['plugins'][module]

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2, sort_keys=True)


@cli.command(short_help='disable one or more plugins')
@click.pass_context
@click.argument('plugins', nargs=-1, required=True, callback=validate_plugins)
def disable(ctx, plugins):
    """Disable one or more plugins

PLUGINS are expressed in the form:

    module1.submodule1=function1,function2,... module2=function3,...

Example:

    tourbillon disable tourbillon.linux=get_cpu_usage,get_mem_usage

Disable the functions get_cpu_usage and get_mem_usage of the
'tourbillon.linux' plugin
    """
    config_file = ctx.parent.params['config']
    with open(config_file, 'r') as f:
        config = json.load(f)
    if 'plugins' not in config:
        return

    for module, functions in plugins.items():
        if module not in config['plugins']:
            continue
        for f in functions:
            if f in config['plugins'][module]:
                config['plugins'][module].remove(f)
        if len(config['plugins'][module]) == 0:
            del config['plugins'][module]

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2, sort_keys=True)


@cli.command()
@click.pass_context
def run(ctx):
    """run the agent"""
    pid_file = ctx.parent.params['pidfile']
    with open(pid_file, 'w') as f:
        f.write(str(os.getpid()))
    config_file = ctx.parent.params['config']
    from .tourbillon import Tourbillon
    ag = Tourbillon(config_file)
    ag.run()


def main():
    cli(prog_name='tourbillon', standalone_mode=False)
