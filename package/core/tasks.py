import requests

from package.core.headers import headers
from package import base


def quests(data, proxies=None):
    url = "https://api.taman.fun/quests"

    try:
        response = requests.get(
            url=url, headers=headers(data), proxies=proxies, timeout=20
        )
        data = response.json()["data"]
        return data
    except:
        return None


def take_task(data, task_id, tele_id, proxies=None):
    url = "https://api.taman.fun/take-task"
    payload = {"taskId": task_id, "teleId": tele_id}  # task_id in tasks, not quest id

    try:
        response = requests.post(
            url=url, headers=headers(data), json=payload, proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


def return_quest(data, quest_id, proxies=None):
    url = "https://api.taman.fun/return-quest"
    payload = {"questId": quest_id}

    try:
        response = requests.post(
            url=url, headers=headers(data), json=payload, proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None


# Status:
## Finished: Completed
## Done: Can Claim -> Run return_quest
## Doing: Doing -> Do nothing
## Pending: Do task -> Run take_task
def process_do_task(data, tele_id, proxies=None):
    quest_list = quests(data=data, proxies=proxies)
    for inner_quest in quest_list.values():
        if inner_quest:
            for quest in inner_quest:
                quest_id = quest["id"]
                quest_name = quest["name"]
                quest_status = quest["status"]
                tasks = quest["tasks"]
                if quest_status == "Finished":
                    base.log(f"{base.white}{quest_name}: {base.green}Completed")
                elif quest_status == "Done":
                    claim_quest = return_quest(
                        data=data, quest_id=quest_id, proxies=proxies
                    )
                    claim_status = claim_quest["success"]
                    if claim_status:
                        base.log(f"{base.white}{quest_name}: {base.green}Completed")
                    else:
                        base.log(f"{base.white}{quest_name}: {base.red}Claim Fail")
                elif quest_status == "Pending":
                    for task in tasks:
                        task_id = task["id"]
                        task_status = task["status"]
                        do_task = take_task(
                            data=data, task_id=task_id, tele_id=tele_id, proxies=proxies
                        )
                        do_task_status = do_task["success"]
                        if do_task_status:
                            base.log(
                                f"{base.white}{quest_name}: {base.yellow}In Doing Status (wait for the next claim or you have to do yourself)"
                            )
                        else:
                            base.log(
                                f"{base.white}{quest_name}: {base.red}Do Task Fail"
                            )
                elif quest_status == "Doing":
                    base.log(
                        f"{base.white}{quest_name}: {base.yellow}In Doing Status (wait for the next claim or you have to do yourself)"
                    )
                else:
                    base.log(f"{base.white}{quest_name}: {base.red}Unknown Status")
