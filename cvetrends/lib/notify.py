import json
from pprint import pprint

import pkg_resources
import requests
from box import Box


def load_file():
    resource = pkg_resources.resource_filename(__name__, "message_payload.json")
    with open(resource) as f:
        data = json.load(f)

    return data


def slack_notify(results, webhook_url, repo_threshold):

    for result in results:
        data = load_file()
        if len(result["github_repos"]) > repo_threshold:
            for l in data["blocks"]:
                try:
                    l["text"]["text"] = l["text"]["text"].replace(
                        "CVE_VAL", result["cve"]
                    )
                except Exception as a:
                    pass

            for l in data["blocks"]:
                try:
                    for x in l["fields"]:
                        if "REPOS" in x["text"]:
                            x["text"] = x["text"].replace(
                                "REPOS", str(len(result["github_repos"]))
                            )

                        if "SEV" in x["text"] and result["severity"] is not None:
                            x["text"] = x["text"].replace("SEV", result["severity"])
                        elif "SEV" in x["text"] and result["severity"] is None:
                            x["text"] = x["text"].replace("SEV", "Unknown")

                        if "SCORE" in x["text"] and result["score"] is not None:
                            x["text"] = x["text"].replace("SCORE", str(result["score"]))
                        elif "SCORE" in x["text"] and result["score"] is None:
                            x["text"] = x["text"].replace("SCORE", "Unknown")

                        if "EMAIL" in x["text"] and result["assigner"] is not None:
                            x["text"] = x["text"].replace("EMAIL", result["assigner"])
                        elif "EMAIL" in x["text"] and result["assigner"] is None:
                            x["text"] = x["text"].replace("EMAIL", "Unknown")

                        if "DESC" in x["text"] and result["description"] is not None:
                            x["text"] = x["text"].replace("DESC", result["description"])
                        elif "DESC" in x["text"] and result["description"] is None:
                            x["text"] = x["text"].replace("DESC", "Unknown")

                except Exception as a:
                    pass

            requests.post(
                webhook_url, json=data, headers={"Content-Type": "application/json"}
            )
            data.clear()
