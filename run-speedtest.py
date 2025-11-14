#!/usr/bin/python3

import time, socket, json
import argparse
from datetime import datetime
from prometheus_client import start_http_server, Summary, Gauge
from subprocess import PIPE, run

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", "--interval", type=int, default=300, help="speedtest check interval"
)
parser.add_argument(
    "-p",
    "--port",
    type=int,
    default=9140,
    help="port the http /metrics server will bind to",
)
parser.add_argument(
    "-s",
    "--servers",
    default=[],
    nargs="+",
    help="list of server names separated by spaces",
)
args = parser.parse_args()


# g_ping = Gauge('speedtest_ping', 'Ping Time', ['name', 'server_id', 'server_name', 'server_cc', 'server_sponsor'])
gauge_speedtest = Gauge(
    "ndt_speedtest", "M-Lab NDT Speedtest", ["name", "server", "metro"]
)


def process_request(t):
    command = f"/usr/local/bin/ndt7-client -quiet -format=json".split(" ")
    _results = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    if _results.returncode != 0:
        print(f"ndt7-client error: {_results.stderr}")
        return

    # Debug output
    print(f"Raw stdout: {repr(_results.stdout)}")

    # Parse the last valid JSON line (summary result)
    lines = _results.stdout.strip().split("\n")
    _dict = None

    for line in reversed(lines):
        line = line.strip()
        if line:
            try:
                _dict = json.loads(line)
                break
            except json.JSONDecodeError:
                continue

    if not _dict:
        print("No valid JSON found in output")
        return

    print(datetime.now().isoformat(), _dict)

    # label vectors
    _server = _dict["ServerFQDN"]
    _metro = _dict["ServerFQDN"].split(".")[-4].split("-")[-1]

    # metric dimensions
    _ping = _dict["MinRTT"]["Value"]
    _retrans = _dict["DownloadRetrans"]["Value"]
    _upload = _dict["Upload"]["Value"]
    _download = _dict["Download"]["Value"]

    gauge_speedtest.labels(
        name="ping",
        server=_server,
        metro=_metro,
    ).set(_ping)

    gauge_speedtest.labels(
        name="upload",
        server=_server,
        metro=_metro,
    ).set(_upload)

    gauge_speedtest.labels(
        name="download",
        server=_server,
        metro=_metro,
    ).set(_download)

    gauge_speedtest.labels(
        name="retrans",
        server=_server,
        metro=_metro,
    ).set(_retrans)

    time.sleep(args.interval)


if __name__ == "__main__":

    # Start up the server to expose the metrics.
    start_http_server(args.port)
    # Generate some requests.
    while True:
        try:
            process_request(args.interval)
        except TypeError as error:
            print(f"TypeError returned from speedtest server\n\n{error}\n")
        except socket.timeout:
            print("socket.timeout returned from speedtest server")
