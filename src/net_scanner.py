import ipaddress
from ping3 import ping
import csv

def scan_ip_range(ip_range):
    active_ips = []
    inactive_ips = []
    
    network = ipaddress.ip_network(ip_range, strict=False)
    
    for ip in network.hosts():
        response_time = ping(str(ip), timeout=1)
        if response_time:
            active_ips.append((str(ip), response_time))
        else:
            inactive_ips.append(str(ip))
    
    return active_ips, inactive_ips

def save_results_to_csv(active_ips, inactive_ips, filename="results.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["IP", "Status", "Ping (ms)"])
        
        for ip, ping_time in active_ips:
            writer.writerow([ip, "Active", round(ping_time * 1000, 2)])
        
        for ip in inactive_ips:
            writer.writerow([ip, "Inactive", ""])
