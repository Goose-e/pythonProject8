host = "localhost"
user = "hackaton_admin"
password = "admin"
dbConst = "hackaton"
servers = [
    'http://localhost:5001',
    'http://localhost:5011',
    'http://localhost:5012'
]
portS1 = 5010
portS2 = 5011
portS3 = 5012
portR1 = 5020
portR2 = 5021
portC1 = 5000
import os

base_dir = os.path.dirname(os.path.abspath(__file__))  # Получите путь к текущему файлу
cert_path = os.path.join(base_dir, 'SSL', 'cert.pem')
