with open("credentials.txt", "r") as f:
    lines = f.readlines()
    USERNAME = lines[0].strip()
    PASSWORD = lines[1].strip()
    print(USERNAME, PASSWORD)