import requests
import json

BASE = 'http://127.0.0.1:5000'

def main():
    payload = {
        'caption': "Launching our new product: UltraClean 2.0! Big SALE #UltraClean #Launch",
        'tone': 'friendly',
        'emoji': 'yes'
    }
    try:
        r = requests.post(BASE + '/api/comment_helper', json=payload, timeout=15)
        print('status:', r.status_code)
        try:
            print(json.dumps(r.json(), indent=2, ensure_ascii=False))
        except Exception as e:
            print('Failed to parse JSON:', e)
            print('Raw text:', r.text[:1000])
    except Exception as e:
        print('Request failed:', e)

if __name__ == '__main__':
    main()
