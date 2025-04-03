import ipaddress
import asyncio
from ping3 import ping
import csv

async def async_ping(ip):
    """Pinge une adresse IP de manière asynchrone."""
    try:
        delay = await asyncio.to_thread(ping, ip, timeout=1)
        if delay is not None and delay is not False:
            return ip, round(delay * 1000, 2)
        return ip, None
    except Exception as e:
        print(f"Erreur lors du ping de {ip}: {e}")
        return ip, None

async def scan_ip_range(ip_range):
    """Scanne une plage d'adresses IP de manière asynchrone."""
    active_ips = []
    inactive_ips = []
    tasks = []

    try:
        network = ipaddress.ip_network(ip_range, strict=False)
        for ip in network.hosts():
            tasks.append(asyncio.ensure_future(async_ping(str(ip))))

        results = await asyncio.gather(*tasks)

        for ip, result in results:
            if result:
                active_ips.append((ip, result))
            else:
                inactive_ips.append(ip)

        return active_ips, inactive_ips
    except ValueError:
        print("Plage d'adresses IP invalide.")
        return [], []

def save_results_to_csv(active_ips, inactive_ips, filename="results.csv"):
    """Sauvegarde les résultats du scan dans un fichier CSV."""
    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["IP", "Status", "Ping (ms)"])

            for ip, ping_time in active_ips:
                writer.writerow([ip, "Active", ping_time])

            for ip in inactive_ips:
                writer.writerow([ip, "Inactive", ""])
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier CSV: {e}")

if __name__ == "__main__":
    ip_range = input("Entrez la plage d'IP à scanner (ex: 192.168.1.0/24): ")
    active_ips, inactive_ips = asyncio.run(scan_ip_range(ip_range))
    save_results_to_csv(active_ips, inactive_ips)
    print(f"Résultats sauvegardés dans 'results.csv'.")
