import socket
import requests
from concurrent.futures import ThreadPoolExecutor

class CyberEngine:
    def __init__(self, target):
        self.target = target.replace("http://", "").replace("https://", "").split("/")[0]
        self.timeout = 1.0

    def check_port(self, port):
        """Быстрый чек порта"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                return s.connect_ex((self.target, port)) == 0
        except: return False

    def brute_paths(self):
        """Ищем забытые файлы БД и конфигов"""
        paths = [".env", ".git/config", "backup.sql", "db.sql", "config.php.bak", "admin/"]
        found = []
        for p in paths:
            try:
                r = requests.get(f"http://{self.target}/{p}", timeout=1.5, allow_redirects=False)
                if r.status_code == 200: found.append(p)
            except: pass
        return found

    def check_subdomains(self):
        """Простейший брут поддоменов (для примера пару штук)"""
        subs = ["dev", "test", "admin", "api", "staging"]
        found = []
        for s in subs:
            full_url = f"{s}.{self.target}"
            try:
                socket.gethostbyname(full_url)
                found.append(full_url)
            except: pass
        return found
