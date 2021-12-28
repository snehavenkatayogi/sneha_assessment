import argparse
import sys
import json
from datetime import datetime
from typing import TextIO, Generator, Tuple, Dict
import traceback


def input_reader_generator(input_handler: TextIO) -> Generator:
    line = input_handler.readline()
    while line:
        visit_hits = json.loads(line)
        yield visit_hits
        line = input_handler.readline()


def get_iso_time(timestamp: int) -> str:
    return datetime.fromtimestamp(int(timestamp)).isoformat()


def parse_data(data: Dict) -> Tuple:
    """
    visits: unique_visit_id, full_visitor_id, visit_id, (int)visit_number, visit_start_time, browser, country
    hits: visit_id, (int)hit_number, hit_type, hit_timestamp, page_path, page_title, hostname
    """
    visits = {
        'unique_visit_id': f"{data['fullVisitorId']}_{data['visitId']}",
        'full_visitor_id': data['fullVisitorId'],
        'visit_id': data['visitId'],
        'visit_number': int(data['visitNumber']),
        'visit_start_time': get_iso_time(int(data['visitStartTime'])),
        'browser': data['device']['browser'],
        'country': data['geoNetwork']['country']
    }
    hits = []

    for hit in data['hits']:
        hits.append(
            {
                'visit_id': f"{data['fullVisitorId']}_{data['visitId']}",
                'hit_number': int(hit['hitNumber']),
                'hit_type': hit['type'],
                'hit_timestamp': get_iso_time(int(data['visitStartTime']) + (int(hit['time'])) // 1000),
                'page_path': hit['page']['pagePath'],
                'page_title': hit['page']['pageTitle'],
                'hostname': hit['page']['hostname']
            }
        )

    return visits, hits


def export(input_handler: TextIO, visits_output_handler: TextIO, hits_output_handler: TextIO) -> None:
    visits_file = visits_output_handler
    hits_file = hits_output_handler
    input_iterator = input_reader_generator(input_handler)

    for data in input_iterator:
        visits, hits = parse_data(data)
        json.dump(visits, visits_file)
        visits_file.write('\n')
        for hit in hits:
            json.dump(hit, hits_file)
            hits_file.write('\n')
    return None


if __name__ == '__main__':
    try:
        input_handler = None
        visits_output_handler = None
        hits_output_handler = None
        default_visits_filename = 'visits.json'
        default_hits_filename = 'hits.json'
        result_output_mode = 'w'
        if not sys.stdin.isatty():
            # Input given using STDIN
            input_handler = sys.stdin
            visits_output_handler = open(default_visits_filename, result_output_mode)
            hits_output_handler = open(default_hits_filename, result_output_mode)
        else:
            # No input given using STDIN, expect input as argument
            parser = argparse.ArgumentParser(
                description="Process Google Analytics data into separate 'visits.json' and 'hits.json' files")
            parser.add_argument('file', help="Path to GA data file in line-delimited JSON format",
                                type=argparse.FileType('r'))
            parser.add_argument('-ov', help="Visits JSON output file path", type=argparse.FileType(result_output_mode),
                                default=default_visits_filename)
            parser.add_argument('-oh', help="Hits JSON output file path", type=argparse.FileType(result_output_mode),
                                default=default_hits_filename)
            args = parser.parse_args()
            input_handler = args.file
            visits_output_handler = args.ov
            hits_output_handler = args.oh
        export(input_handler, visits_output_handler, hits_output_handler)
    except Exception as e:
        traceback.print_exc()
    finally:
        try:
            input_handler.close()
            visits_output_handler.close()
            hits_output_handler.close()
        except Exception as e:
            pass
