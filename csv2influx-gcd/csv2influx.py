#!/usr/bin/env python

import logging
import logging.config
import urllib.parse

from os import path
from csv2influx.parser.csv_parser import CSVParser
from docopt import docopt
from csv2influx.constants import MAX_BATCH_SIZE, MIN_BATCH_SIZE

__status__ = 'testing'

__doc__ = """csv2influx-gcd - A tool for populating InfluxDB timeseries with Google cluster data (https://github.com/google/cluster-data).

Usage:
    csv2influx-gcd <source_path> [--influxdb-url=<http://hostname:port>] [--auth=<USER:PASSWORD>] [--dbname=<dbname>] 
    [--cpu=<N_CPU>] [--batch-size=<SIZE>] [--skip-first] [--replace-strategy=<REPLACE_REMOVE|REPLACE_ONLY|NOTHING>]

Options:
    -h --help                       Show this screen
    --version                       Show version
    --influxdb-url=INFLUXDB_URL     The URL of InfluxDB Server          [default: http://localhost:8086]
    --auth=USER:PASSWORD            Authentication                      [default: user:password]
    --dbname=DB_NAME                The database name                   [default: test]
    --cpu=N_CPU                     Set the number of CPU used          [default: 4]
    --batch-size=SIZE               The size of a batch of points       [default: 10000]
    --skip-first                    Skip the first interval
    --replace-strategy=STRATEGY     Replace strategy of missing values  [default: REPLACE_REMOVE]
"""

class CSV2Influx:

    def __init__(self,
                 path_csv,
                 batch_size,
                 host,
                 port,
                 user,
                 password,
                 dbname,
                 n_cpu,
                 skip_first,
                 replace_strategy):

        self.csv_parser = CSVParser(
            path_csv,
            batch_size,
            host,
            port,
            user,
            password,
            dbname,
            n_cpu=n_cpu,
            skip_first=skip_first,
            replace_strategy=replace_strategy)

        self.logger = logging.getLogger(__class__.__name__)
        self.logger.info(__class__.__name__ + "logger started")

    def run(self):

        try:

            self.csv_parser.start()
            self.csv_parser.join()

        except ConnectionError:
            raise
        except ValueError:
            raise


if __name__ == '__main__':

    args = docopt(__doc__, version=csv2influx.__version__)

    path_log_file = path.dirname(path.abspath(__file__)) + '/logs/logging.conf'
    logging.config.fileConfig(path_log_file)
    logger = logging.getLogger()
    logger.info("Log Initialized @" + path_log_file)

    url = urllib.parse.urlparse(args['--influxdb-url']).netloc.split(":")
    auth = args['--auth'].split(":")

    # batch size options
    batch_size = int(args['--batch-size'])

    if batch_size < MIN_BATCH_SIZE or batch_size > MAX_BATCH_SIZE:
        logger.error('Batch size must be between ' + str(MIN_BATCH_SIZE) + ' and ' + str(MAX_BATCH_SIZE))
        exit(1)

    csv2influx = CSV2Influx(
        args['<source_path>'],
        batch_size,
        url[0],
        url[1],
        auth[0],
        auth[1],
        args['--dbname'],
        args['--cpu'],
        args['--skip-first'],
        args['--replace-strategy'].upper())

    csv2influx.run()
