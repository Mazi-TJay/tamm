import requests

from package.core.headers import headers
from package import base


def split_string(input_string):
    # Split the string by <smart-airdrop>
    parts = input_string.split("<smart-airdrop>")

    # Extract wallet and tele_id
    if len(parts) == 2:
        wallet = parts[0].lower()
        tele_id = parts[1]
        return wallet, tele_id
    else:
        raise ValueError("Input string is not in the expected format")


def mining(data, proxies=None):
    url = "https://api.taman.fun/mining"

    try:
        response = requests.get(
            url=url, headers=headers(data), proxies=proxies, timeout=20
        )
        data = response.json()["data"]
        point_per_hour = data["pointPerHour"]
        mined_point = round(data["point"], 2)
        mining_point = round(data["pointCanClaimed"], 4)
        return point_per_hour, mined_point, mining_point
    except:
        return None


def claim_mining(data, proxies=None):
    url = "https://api.taman.fun/mining"

    try:
        response = requests.post(
            url=url, headers=headers(data), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def process_claim_mining(data, proxies=None):
    claim = claim_mining(data=data, proxies=proxies)
    claim_status = claim["success"]
    if claim_status:
        base.log(f"{base.white}Auto Claim: {base.green}Success")
        point_per_hour, mined_point, mining_point = mining(data=data, proxies=proxies)
        base.log(
            f"{base.green}Point per Hour: {base.white}{point_per_hour} - {base.green}Mined Point: {base.white}{mined_point:,} - {base.green}Mining Point: {base.white}{mining_point}"
        )
    else:
        base.log(f"{base.white}Auto Claim: {base.red}Not time to claim")
