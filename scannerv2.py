import socket
import requests
import os
import re
import time
import threading
from queue import Queue
from colorama import Fore, Style, init
from faker import Faker


init(autoreset=True)

fake = Faker()

logs = []

print_lock = threading.Lock()


def logo():

    os.system("cls" if os.name == "nt" else "clear")

    print(Fore.RED + r"""


 ██████  ▄████▄   ▄▄▄       ███▄    █  ███▄    █  ██▀███
▒██    ▒ ▒██▀ ▀█  ▒████▄     ██ ▀█   █  ██ ▀█   █ ▓██ ▒ ██▒
░ ▓██▄   ▒▓█    ▄ ▒██  ▀█▄  ▓██  ▀█ ██▒▓██  ▀█ ██▒▓██ ░▄█ ▒
  ▒   ██▒▒▓▓▄ ▄██▒░██▄▄▄▄██ ▓██▒  ▐▌██▒▓██▒  ▐▌██▒▒██▀▀█▄
▒██████▒▒▒ ▓███▀ ░ ▓█   ▓██▒▒██░   ▓██░▒██░   ▓██░░██▓ ▒██▒
▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ ░ ▒░   ▒ ▒ ░ ▒▓ ░▒▓░
░ ░▒  ░ ░  ░  ▒     ▒   ▒▒ ░░ ░░   ░ ▒░░ ░░   ░ ▒░  ░▒ ░ ▒░
░  ░  ░  ░          ░   ▒      ░   ░ ░    ░   ░ ░   ░░   ░
      ░  ░ ░            ░  ░         ░          ░    ░
         ░


""")

    print(Fore.RED + Style.BRIGHT + "               V2\n")

    print(Fore.RED + "by jzxzn. - Contact to Discord: jzxzn.\n")


def username_lookup():

    username = input(Fore.WHITE + "USERNAME > ")

    sites = {

        "GitHub":
        f"https://github.com/{username}",

        "Instagram":
        f"https://instagram.com/{username}",

        "TikTok":
        f"https://www.tiktok.com/@{username}",

        "Reddit":
        f"https://reddit.com/user/{username}",

        "Pinterest":
        f"https://pinterest.com/{username}",

        "Twitch":
        f"https://twitch.tv/{username}",

        "Steam":
        f"https://steamcommunity.com/id/{username}",

        "GitLab":
        f"https://gitlab.com/{username}",

        "Medium":
        f"https://medium.com/@{username}",

        "Roblox":
        f"https://www.roblox.com/user.aspx?username={username}",

        "Kick":
        f"https://kick.com/{username}",

        "SoundCloud":
        f"https://soundcloud.com/{username}",

        "Telegram":
        f"https://t.me/{username}",

        "YouTube":
        f"https://youtube.com/@{username}",

        "Facebook":
        f"https://facebook.com/{username}",

        "Twitter/X":
        f"https://x.com/{username}"
    }

    print(
        Fore.CYAN +
        "\n[~] BUSCANDO\n"
    )

    found = 0

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for site, url in sites.items():

        try:

            r = requests.get(
                url,
                headers=headers,
                timeout=5
            )

            if r.status_code == 200:

                print(
                    Fore.GREEN +
                    f"[FOUND] {site:<15} -> {url}"
                )

                found += 1

            else:

                print(
                    Fore.RED +
                    f"[NOT FOUND] {site}"
                )

        except:

            print(
                Fore.YELLOW +
                f"[ERROR] {site}"
            )

    print(
        Fore.CYAN +
        f"\n[+] TOTAL FOUND: {found}"
    )

    logs.append(
        f"USERNAME SEARCH -> {username}"
    )


def check_port(ip, port, open_ports):

    try:

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(0.7)

        result = sock.connect_ex((ip, port))

        if result == 0:

            with print_lock:

                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"

                print(
                    Fore.GREEN +
                    f"[OPEN] PORT {port:<5} | SERVICE -> {service}"
                )

                open_ports.append(port)

        sock.close()

    except:
        pass


def worker(ip, queue_ports, open_ports):

    while not queue_ports.empty():

        port = queue_ports.get()

        check_port(
            ip,
            port,
            open_ports
        )

        queue_ports.task_done()


def port_scanner():

    target = input(Fore.WHITE + "IP / DOMINIO > ")

    try:

        ip = socket.gethostbyname(target)

    except:

        print(Fore.RED + "[!] INVALID TARGET")
        return

    print(Fore.CYAN + f"\n[~] IP -> {ip}")

    print(Fore.WHITE + "\n[1] ESCANEO RAPIDO")
    print(Fore.WHITE + "[2] ESCANEO COMPLETO")
    print(Fore.WHITE + "[3] PERSONALIZADO")

    mode = input(Fore.CYAN + "\nSCANNR > ")

    if mode == "2":

        start_port = 1
        end_port = 65535

    elif mode == "3":

        try:

            start_port = int(input("START PORT > "))
            end_port = int(input("END PORT > "))

        except:

            print(Fore.RED + "[!] INVALID RANGE")
            return

    else:

        start_port = 1
        end_port = 1024

    print(Fore.YELLOW + "\n[~] SCANNING PORTS...\n")

    open_ports = []

    queue_ports = Queue()

    for port in range(start_port, end_port + 1):

        queue_ports.put(port)

    threads = 100

    for _ in range(threads):

        t = threading.Thread(
            target=worker,
            args=(ip, queue_ports, open_ports)
        )

        t.daemon = True

        t.start()

    queue_ports.join()

    if len(open_ports) == 0:

        print(
            Fore.RED +
            "\n[-] NO OPEN PORTS FOUND"
        )

    else:

        print(
            Fore.CYAN +
            f"\n[+] TOTAL OPEN PORTS: {len(open_ports)}"
        )

    logs.append(
        f"PORT SCAN -> {target} | {open_ports}"
    )


def geo_ip():

    ip = input(Fore.WHITE + "IP > ")

    try:

        data = requests.get(
            f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,zip,isp,lat,lon,proxy,hosting,mobile,query",
            timeout=5
        ).json()

        if data["status"] != "success":
            print(Fore.RED + "[!] IP INVÁLIDA")
            return

        print(Fore.CYAN + "\n===== 🌍 GEOLOCALIZACIÓN IP =====\n")

        print(Fore.GREEN + f"📍 IP        : {data['query']}")
        print(Fore.GREEN + f"🌎 País      : {data['country']}")
        print(Fore.GREEN + f"🗺️ Región    : {data['regionName']}")
        print(Fore.GREEN + f"🏙️ Ciudad    : {data['city']}")
        print(Fore.GREEN + f"📮 ZIP       : {data['zip']}")
        print(Fore.GREEN + f"📡 ISP       : {data['isp']}")
        print(Fore.GREEN + f"📌 Coords    : {data['lat']} / {data['lon']}")

        print(Fore.CYAN + "\n===== 🛡️ RED =====")

        
        if data.get("proxy"):
            print(Fore.RED + "🚨 VPN / PROXY DETECTADO")
        else:
            print(Fore.GREEN + "✅ SIN PROXY DETECTADO")

        
        if data.get("hosting"):
            print(Fore.YELLOW + "⚠️ IP DE DATACENTER (POSIBLE VPS / VPN)")
        else:
            print(Fore.GREEN + "🏠 IP RESIDENCIAL")

        
        if data.get("mobile"):
            print(Fore.BLUE + "📱 RED MÓVIL DETECTADA")
        else:
            print(Fore.WHITE + "💻 RED FIJA")

    except Exception as e:
        print(Fore.RED + f"[!] ERROR REQUEST: {e}")


def dns_lookup():

    domain = input(Fore.WHITE + "🌐 DOMAIN > ").strip()

    if domain.startswith("http://") or domain.startswith("https://"):
        domain = domain.replace("http://", "").replace("https://", "").split("/")[0]

    print(Fore.CYAN + "\n[~] ANALIZANDO DOMINIO...\n")

    try:

        ip = socket.gethostbyname(domain)

        print(Fore.GREEN + "══════════ 🌍 DNS LOOKUP ══════════\n")

        print(Fore.GREEN + f"🌐 DOMINIO    : {domain}")
        print(Fore.GREEN + f"📡 IP ADDRESS : {ip}")

        
        try:

            host = socket.gethostbyaddr(ip)[0]

            print(Fore.YELLOW + f"🖥️ HOSTNAME   : {host}")

        except:

            print(Fore.RED + "🖥️ HOSTNAME   : NOT FOUND")

        
        try:

            data = requests.get(
                f"http://ip-api.com/json/{ip}",
                timeout=5
            ).json()

            if data["status"] == "success":

                print(Fore.CYAN + "\n════ 📍 GEO INFO ════\n")

                print(Fore.YELLOW + f"🌎 COUNTRY    : {data['country']}")
                print(Fore.YELLOW + f"🏙️ CITY       : {data['city']}")
                print(Fore.YELLOW + f"📶 ISP        : {data['isp']}")

        except:
            pass

        print(Fore.GREEN + "\n═══════════════════════════════════\n")

        logs.append(
            f"DNS LOOKUP -> {domain} | {ip}"
        )

    except socket.gaierror:

        print(Fore.RED + "[!] INVALID DOMAIN OR NOT FOUND")

    except Exception as e:

        print(Fore.RED + f"[!] ERROR : {e}")






def email_analyzer():

    email = input(Fore.WHITE + "EMAIL > ")

    print()

    if re.match(r"[^@]+@[^@]+\.[^@]+", email):

        domain = email.split("@")[1]

        print(Fore.GREEN + "[✓] VALID FORMAT")
        print(Fore.CYAN + f"DOMAIN -> {domain}")

        try:

            ip = socket.gethostbyname(domain)

            print(
                Fore.GREEN +
                f"DOMAIN IP -> {ip}"
            )

        except:

            print(
                Fore.RED +
                "DOMAIN NOT RESOLVED"
            )

    else:

        print(
            Fore.RED +
            "[!] INVALIDO EMAIL"
        )


def link_check():

    url = input(Fore.WHITE + "URL > ")

    risk = 0

    suspicious = [
        "grabify",
        "iplogger",
        "2no.co",
        "bit.ly",
        "tinyurl",
        "cutt.ly"
        "maper.info",
    ]

    for x in suspicious:

        if x in url.lower():
            risk += 3

    if "@" in url:
        risk += 1

    if len(url) > 70:
        risk += 1

    print()

    if risk >= 4:

        print(
            Fore.RED +
            "[!!!] 🚨MALICIOSO"
        )

    elif risk >= 2:

        print(
            Fore.YELLOW +
            "[!] ⚠️SOSPECHOSO LINK"
        )

    else:

        print(
            Fore.GREEN +
            "[✓] ☑️NORMAL LINK"
        )


def fake_identity():

    print(Fore.CYAN + "\n[*] GENERANDO IDENTIDAD FALSA...\n")

    print(Fore.GREEN + "══════════ 🧑 IDENTIDAD ══════════\n")

    print(Fore.GREEN + f"👤 NAME      : {fake.name()}")
    print(Fore.GREEN + f"📧 EMAIL     : {fake.email()}")
    print(Fore.GREEN + f"📱 PHONE     : {fake.phone_number()}")
    print(Fore.GREEN + f"🏠 ADDRESS   : {fake.address().replace(chr(10), ', ')}")
    print(Fore.GREEN + f"🏢 COMPANY   : {fake.company()}")
    print(Fore.GREEN + f"💼 JOB       : {fake.job()}")

    print(Fore.CYAN + "\n════ 🌍 EXTRA INFO ════\n")

    print(Fore.YELLOW + f"🎂 BIRTHDATE : {fake.date_of_birth()}")
    print(Fore.YELLOW + f"🌐 USERNAME  : {fake.user_name()}")
    print(Fore.YELLOW + f"🆔 ID NUMBER : {fake.random_number(digits=9)}")
    print(Fore.YELLOW + f"💳 CREDIT    : {fake.credit_card_number()}")

    print(Fore.MAGENTA + f"📶 DOMAIN    : {fake.domain_name()}")
    print(Fore.MAGENTA + f"🌐 IP SAMPLE : {fake.ipv4()}")

    print(Fore.CYAN + "\n═══════════════════════════════════\n")


def export_logs():

    with open(
        "@0_logs.txt",
        "w",
        encoding="utf-8"
    ) as f:

        for line in logs:
            f.write(line + "\n")

    print(
        Fore.GREEN +
        "\n[✓] LOGS SAVED"
    )


def menu():

    while True:

        print(Fore.BLUE + """

[1] Buscar Usuario 
[2] Escaneo de puertos
[3] Geo IP
[4] DNS Lookup
[5] Email Analizer
[6] Link Check
[7] Gen Info Falsa
[8] Exportar Logs
[0] Salir

""")

        op = input(Fore.CYAN + "@0 > ")

        if op == "1":
            username_lookup()

        elif op == "2":
            port_scanner()

        elif op == "3":
            geo_ip()

        elif op == "4":
            dns_lookup()

        elif op == "5":
            email_analyzer()

        elif op == "6":
            link_check()

        elif op == "7":
            fake_identity()

        elif op == "8":
            export_logs()

        elif op == "0":

            print(
                Fore.RED +
                "\n[ EXIT ]"
            )

            time.sleep(1)

            break

        else:

            print(
                Fore.RED +
                "[!] INVALIDA OPCION"
            )

        input(
            Fore.YELLOW +
            "\nPRESIONE ENTER PARA CONTINUAR..."
        )


if __name__ == "__main__":

    logo()
    menu()