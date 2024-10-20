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
    f'http://localhost:{portS1}',
    f'http://localhost:{portS2}',
    f'http://localhost:{portS3}'
]

import os

base_dir = os.path.dirname(os.path.abspath(__file__))  # Получите путь к текущему файлу
cert_path = os.path.join(base_dir, 'SSL', 'cert.pem')
