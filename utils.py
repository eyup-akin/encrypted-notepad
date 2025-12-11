import os
import sys

# utils.py dosyasının olduğu yerden bir üst klasöre (proje ana dizinine) çıkıyoruz
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_path(filename):
    """Dosya adını alır ve projenin tam yoluyla birleştirir."""
    return os.path.join(BASE_DIR, filename)