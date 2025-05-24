"""
This uses La Poste's API to validate French addresses.
"""

import time
import requests
import os
import re
import tempfile
from dotenv import load_dotenv

load_dotenv()


def address_integrity_check(regex: str, address: str):
    return bool(re.search(regex, address, re.VERBOSE))


def manual_edit(pre_text: str | list[str] = "") -> str | list[str]:
    """
    Open a notepad window, and ask user to save once done.
    """
    is_list = False
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as f:
        if isinstance(pre_text, list):
            is_list = True
        if is_list:
            pre_text = "\n".join(pre_text)
        f.write(pre_text.encode("utf-8"))  # type: ignore
        f.flush()
        if os.name == "nt":
            os.system(f'start notepad.exe "{f.name}"')
        elif os.name == "posix":
            if os.uname().sysname == "Darwin":  # macOS
                os.system(f'open -a TextEdit "{f.name}"')
            else:  # Linux
                os.system(f'gedit "{f.name}" &')
        else:
            raise Exception("Unsupported OS")
        print("Please edit the address in the notepad window and save it.")
        result = pre_text
        while pre_text == result:
            with open(f.name, "r", encoding="utf-8") as file:
                result = file.read()
            time.sleep(1)

    print("Processed modifications.")
    if is_list and isinstance(result, str):
        result = result.splitlines()
    return result


def check_address(q: str) -> str:  # pylint: disable=R0915
    okapi_key = os.getenv("OKAPI_API_KEY")
    # Check if the API key is valid.
    if not okapi_key or len(okapi_key) < 10:
        print('Ignoring French address check, no valid API key found.')
        return q
    wq = "\n".join(q.splitlines()[1:-1])
    # Remove everything after the 1st space on the last line
    wq = wq.splitlines()[:-1] + [" ".join(wq.splitlines()[-1].split(" ", 1)[:1])]
    manual = []
    resp = requests.get(
        "https://api.laposte.fr/controladresse/v2/adresses",
        headers={
            "X-Okapi-Key": okapi_key,
        },
        params={
            "q": wq,
        },
        timeout=10
    )

    if resp.status_code != 200:
        raise Exception(f"Error {resp.status_code}: {resp.text}")
    data = resp.json()
    if len(data) == 0:
        raise Exception(f"Address not found: {q}")
    if len(data) > 1:
        print("Multiple addresses found:")
        for i, addr in enumerate(data):
            print(f"• {i + 1} - {addr['adresse']}")
        print(f"• {len(data) + 1} - Manual entry")
        x = input("> ")
        if x.isdigit() and 1 <= int(x) <= len(data):
            data = [data[int(x) - 1]]
        elif x == str(len(data) + 1):
            manual = [manual_edit()]
        else:
            raise Exception(f"Invalid choice: {x}")
    else:
        print("Address found:")
        print(f"• {data[0]['adresse']}")
        x = input("Use auto? (y/n)\n> ")
        if x.lower() != "y":
            manual = [manual_edit()]

    if not manual:
        code = data[0]["code"]
        resp = requests.get(
            "https://api.laposte.fr/controladresse/v2/adresses/" + code,
            headers={
                "X-Okapi-Key": okapi_key,
            },
            timeout=10
        )
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        data = resp.json()
        print(data)
        if data["lieuDit"] == "" and len(wq) > 2:
            print("Applied lieu dit")
            data["lieuDit"] = wq[0]
            data["blocAdresse"] = [wq[0].upper()] + data["blocAdresse"]
        if data["lieuDit"] != "":
            print("APPLIED LIEU DIT: " + data["lieuDit"])
            if input("Keep? (y=yes, n=edit)\n> ").lower() == "y":
                pass
            else:
                data["blocAdresse"] = manual_edit(data["blocAdresse"])
        print("Using lieu dit:")
        return "\n".join([q.splitlines()[0].title()] + data["blocAdresse"])
    # Flatten manual if it's a list of lists
    flat_manual: list[str] = []
    for item in manual:
        if isinstance(item, list):
            flat_manual.extend(item)
        else:
            flat_manual.append(item)
    return "\n".join([q.splitlines()[0].title()] + flat_manual)
