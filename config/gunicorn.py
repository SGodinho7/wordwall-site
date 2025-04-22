import os
import multiprocessing

bind = os.getenv('WEB_BIND', '0.0.0.0:5000')
workers = int(os.getenv('WEB_WORKERS', multiprocessing.cpu_count() * 2))
threads = int(os.getenv('WEB_THREADS', 1))
