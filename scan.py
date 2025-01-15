import argparse
import csv
import ipaddress
import subprocess
import platform
from datetime import datetime

def ping_ip(ip):
    """Pings an IP address and returns the status and response time."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        start = datetime.now()
        subprocess.run(["ping", param, "1", str(ip)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        elapsed = (datetime.now() - start).microseconds // 1000  # Convert to ms
        return "Active", elapsed
    except subprocess.CalledProcessError:
        return "Inactive", None

def scan_range(ip_range):
    """Scans a range of IP addresses and returns their statuses."""
    results = []
    for ip in ipaddress.IPv4Network(ip_range, strict=False):
        status, response_time = ping_ip(ip)
        results.append((str(ip), status, response_time))
    return results

def save_to_csv(results, filename):
    """Saves scan results to a CSV file."""
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["IP", "Status", "Ping (ms)"])
        for ip, status, ping in results:
            writer.writerow([ip, status, ping if ping is not None else ""])

def main():
    parser = argparse.ArgumentParser(description="Network Scanner for Active/Inactive IPs")
    parser.add_argument("--range", required=True, help="IP range to scan (e.g., 192.168.1.0/24)")
    parser.add_argument("--output", default="results.csv", help="Output CSV file (default: results.csv)")

    args = parser.parse_args()

    print(f"Scanning IP range: {args.range}")
    results = scan_range(args.range)

    print("Scan Results:")
    for ip, status, ping in results:
        print(f"{ip:15} {status:8} {(f'(Ping: {ping}ms)' if ping is not None else '')}")

    save_to_csv(results, args.output)
    print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()
