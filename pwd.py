import hashlib
import requests

def check_password_pwned(password: str):
    # Step 1: SHA1 hash the password
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

    prefix = sha1[:5]
    suffix = sha1[5:]

    # This Databse contains around 1 billion compromised passwords to verify against

    # Step 2: Query the HIBP API with the first 5 chars
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)

    if response.status_code != 200:
        raise RuntimeError("Error fetching data from HIBP API")

    hashes = response.text.splitlines()

    # Step 3: Compare suffix with returned hashes
    for h in hashes:
        leaked_hash, count = h.split(":")
        if leaked_hash == suffix:
            return int(count)  # Number of times seen in breaches

    return 0  # Not found


# Example:
password = "YourSecurePassword123!"
password = "Password"
leak_count = check_password_pwned(password)

if leak_count > 0:
    print(f"⚠️ Password found in data breaches {leak_count} times!")
else:
    print("✅ Password NOT found in any known breaches.")
