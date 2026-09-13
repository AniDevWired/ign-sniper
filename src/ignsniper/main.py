from asyncio import sleep
import os
import random
import string
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()

GEN_FILE = Path("gen.txt")
IGN_FILE = Path("ign.txt")

XBL_API_KEY = os.getenv("XBL_API_KEY")
XBL_HOST = "api.xbl.io"

CHARS = string.ascii_lowercase + string.digits

TIME_DELAY = 25 # bcuz 150 request/hr

def load(path: Path) -> set[str]:
    if not path.exists():
        return set()

    return {
        line.strip().lower()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def save(name: str, path: Path) -> None:
    with path.open("a", encoding="utf-8") as file:
        file.write(f"{name}\n")


def generate(length: int, existing: set[str]) -> str:
    while True:
        name = random.choice(string.ascii_lowercase) + "".join(
            random.choice(CHARS)
            for _ in range(length - 1)
        )

        if name.lower() not in existing:
            return name


def check_gamertag(name: str) -> tuple[bool, dict]:
    if not XBL_API_KEY:
        raise RuntimeError("XBL_API_KEY is missing from .env")

    url = f"https://{XBL_HOST}/v2/friends/search/{name}"

    headers = {
        "X-Authorization": XBL_API_KEY,
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 404:
        return False, {}

    response.raise_for_status()

    try:
        data = response.json()
    except ValueError:
        raise RuntimeError(
            f"Non-JSON response (status {response.status_code}): {response.text[:300]!r}"
        )

    profiles = data.get("content", {}).get("profileUsers", [])
    return bool(profiles), data


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: uv run main.py <length>")

    try:
        length = int(sys.argv[1])
    except ValueError:
        raise SystemExit("Length must be a number.")

    if length < 1:
        raise SystemExit("Length must be at least 1.")

    try: 
        while True: 
            existing = load(GEN_FILE)
            name = generate(length, existing)

            print(f"Generated: {name}")
            print("Checking Xbox...")

            try:
                taken, data = check_gamertag(name)
            except requests.RequestException as exc:
                raise SystemExit(f"Request failed: {exc}")
            except RuntimeError as exc:
                raise SystemExit(str(exc))

            save(name, GEN_FILE)

            if taken:
                profile = data.get("content", {}).get("profileUsers", [{}])[0]
                settings = {s.get("id"): s.get("value") for s in profile.get("settings", [])}
                existing_tag = settings.get("Gamertag", name)
                print(f"[-] {name} -> TAKEN (matched: {existing_tag})")
            else:
                save(name, IGN_FILE)
                print(f"[+] {name} -> AVAILABLE")

            time.sleep(TIME_DELAY)

    except KeyboardInterrupt:
        print("\nStopped by user.")


if __name__ == "__main__":
    main()