host = "localhost"
portS1 = 5010
portS2 = 5011
portS3 = 5012
portR1 = 5020
portR2 = 5021
portC1 = 5000
user = "hackaton_admin"
password = "admin"
dbConst = "hackaton"
servers = [
    f'http://127.0.0.1:{portS1}',
    f'http://127.0.0.1:{portS2}',
    f'http://127.0.0.1:{portS3}'
]
routers = [
    f"http://127.0.0.1:{portR1}",
    f"http://127.0.0.1:{portR2}"
]
import os

base_dir = os.path.dirname(os.path.abspath(__file__))  # Получите путь к текущему файлу
cert_path = os.path.join(base_dir, 'SSL', 'cert.pem')
