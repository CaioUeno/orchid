import json
from datetime import datetime
from time import sleep
from typing import Any, Callable, Union

from discord_webhook import DiscordWebhook
from slack_sdk.webhook import WebhookClient

# +----------------------------------------------------------------------------------------------------------+
# |                                                  SLACK                                                   |
# +----------------------------------------------------------------------------------------------------------+
# | create a webhook: https://api.slack.com/messaging/webhooks                                               |
# | how to tag a user: https://stackoverflow.com/questions/47491331/mentioning-users-via-slack-in-webhooks   |
# | how to find user id: https://moshfeu.medium.com/how-to-find-my-member-id-in-slack-workspace-d4bba942e38c |
# +----------------------------------------------------------------------------------------------------------+

# +--------------------------------------------------------------------------------------------------------------------------+
# |                                                         DISCORD                                                          |
# +--------------------------------------------------------------------------------------------------------------------------+
# | webhook usage: https://pypi.org/project/discord-webhook/                                                                 |
# | how to tag a user: https://stackoverflow.com/questions/62974139/how-do-i-get-a-discord-bot-to-mention-a-role-and-a-user  |
# | how to find user id: https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID- |
# +--------------------------------------------------------------------------------------------------------------------------+


def get_userid(app: str) -> str:
    """Utils function"""
    with open("webhooks.json") as file:
        webhooks = json.load(file)
        try:
            return webhooks[app]["userid"]
        except KeyError:
            raise ValueError(
                f"Unknown app name: {app}. Must be among {{`slack`, `discord`}}."
            )


def get_webhook(app: str, name: str) -> Union[WebhookClient, DiscordWebhook]:
    """Utils function"""
    wb_mapping = {"slack": WebhookClient, "discord": DiscordWebhook}
    with open("webhooks.json") as file:
        webhooks = json.load(file)

        try:
            for wb in webhooks[app]["webhooks"]:
                if name == wb["name"]:
                    url = wb["url"]
                    return wb_mapping[app](url=url)

            raise ValueError(f"Webhook name for {app} was not found: {name}")

        except KeyError:
            raise ValueError(
                f"Unknown app name: {app}. Must be among {{`slack`, `discord`}}."
            )


def send_message(
    message: str,
    webhook: Union[WebhookClient, DiscordWebhook],
    tag: str = None,
    timestamp: bool = False,
) -> bool:
    """
    Sends a message to the channel as a simple text.

    Arguments
    ---------
        message (str): message to display on channel;
        webhook (Union[WebhookClient, DiscordWebhook]): app webhook;
        tag (str) : If not `None`, send a message tagging a user. Defaults to `None`;
        timestamp (bool) : Whether to display timestamp information at the moment of the request. Defaults to False.
    Returns:
        bool : whether `response status` == 200 or not.
    """

    text = message

    if tag is not None:
        text = f"<@{tag}> - " + text

    if timestamp:
        text += f" ({datetime.now().replace(microsecond=0)})"

    if isinstance(webhook, WebhookClient):
        status_code = webhook.send(text=text).status_code

    else:
        webhook.set_content(content=text)
        status_code = webhook.execute().status_code

    return status_code == 200


def hermes(app: str, name: str, tag: str = None, timestamp: bool = False) -> Callable:
    """
    Decorator to encapsulate a function and `log` its behaviour/progress into an app channel.

    Arguments
    ---------
        app (str) : app name among {`slack`, `discord`};
        name (str) : webhook name;
        tag (str) : If not `None`, send a message tagging a user (tag itself). Defaults to `None`;
        timestamp (bool) : Whether to display timestamp information at the moment of the request. Defaults to `False`.
    """

    def wrapper(func: Callable) -> Callable:
        webhook = get_webhook(app=app, name=name)

        def inner(*args, **kwargs) -> Any:
            # before calling the function
            send_message(
                message=f"Calling {func.__name__}",
                webhook=webhook,
                tag=tag,
                timestamp=timestamp,
            )

            try:
                r = func(*args, **kwargs)
                send_message(
                    message=f"{func.__name__} has finished!",
                    webhook=webhook,
                    tag=tag,
                    timestamp=timestamp,
                )

                return r

            except Exception as e:
                send_message(
                    message=f"{func.__name__} has failed!",
                    webhook=webhook,
                    tag=tag,
                    timestamp=timestamp,
                )
                send_message(
                    message=str(e),
                    webhook=webhook,
                    tag=tag,
                    timestamp=timestamp,
                )

                return None

        return inner

    return wrapper


# SLACK_USER_ID = get_userid("slack")
# DISCORD_USER_ID = get_userid("discord")


# @hermes(app="slack", name="clair", tag=SLACK_USER_ID, timestamp=True)
# def example1(seconds: int = 2) -> None:
#     sleep(seconds)


# @hermes(app="discord", name="clair", tag=DISCORD_USER_ID, timestamp=True)
# def example2(a: Any) -> None:
#     # force an error
#     raise ValueError(f"Raising an error!")


# # calling decorated functions
# example1(seconds=3)
# example2(None)
