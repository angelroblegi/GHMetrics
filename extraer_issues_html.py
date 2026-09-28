s = requests.Session()
s.headers["Authorization"] = f"Bearer {token}"
s.verify = False
