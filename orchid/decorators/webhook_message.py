from datetime import datetime
from typing import Any, Callable, Union

from discord_webhook import DiscordWebhook
from requests import Response
from slack_sdk.webhook import WebhookClient, WebhookResponse

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


def hermes(
    webhook: Union[WebhookClient, DiscordWebhook],
    tag: str = None,
    timestamp: bool = False,
) -> Callable:
    """
    Decorator to encapsulate a function and `log` its behaviour/progress into an app channel.

    Arguments
    ---------
        webhook : Union[WebhookClient, DiscordWebhook]
            App webhook;
        tag : str
            If not `None`, send a message tagging a user (tag itself). Defaults to `None`;
        timestamp : bool
            Whether to display timestamp information at the moment of the request. Defaults to False.
    """

    def format_message(
        message: str,
        tag: str = None,
        timestamp: bool = False,
    ) -> str:
        """
        Function to format a message. It may tag a user and/or add the timestamp.

        Parameters
        ----------
            tag : str
                If not `None`, send a message tagging a user (tag itself). Defaults to `None`;
            timestamp : bool
                Whether to display timestamp information at the moment of the request. Defaults to False.

        Returns
        -------
            formatted_message : str
                Formatted message.
        """
        formatted_message = message

        if tag is not None:
            formatted_message = f"<@{tag}> - " + formatted_message

        if timestamp:
            formatted_message += f" ({datetime.now().replace(microsecond=0)})"

        return formatted_message

    def send_message(
        message: str,
        webhook: Union[WebhookClient, DiscordWebhook],
    ) -> Union[WebhookResponse, Response]:
        """
        Sends a message to the channel as a simple text.

        Parameters
        ---------
            message : str
                Message to send;
            webhook : Union[WebhookClient, DiscordWebhook]
                App webhook.

        Returns
        -------
            status_code : int
                reponse status code.
        """

        if isinstance(webhook, WebhookClient):
            response = webhook.send(text=message)

        else:
            webhook.set_content(content=message)
            response = webhook.execute()

        return response

    def wrapper(func: Callable) -> Callable:
        def inner(*args, **kwargs) -> Any:
            # before calling the function
            send_message(
                message=format_message(
                    f"Calling {func.__name__}", tag=tag, timestamp=timestamp
                ),
                webhook=webhook,
            )

            try:
                r = func(*args, **kwargs)

                # after the fuction was called
                send_message(
                    message=format_message(
                        f"{func.__name__} has finished!", tag=tag, timestamp=timestamp
                    ),
                    webhook=webhook,
                )

                return r

            except Exception as e:
                # exception "warning"
                send_message(
                    message=format_message(
                        f"{func.__name__} has failed!", tag=tag, timestamp=timestamp
                    ),
                    webhook=webhook,
                )
                send_message(
                    message=str(e),
                    webhook=webhook,
                )

                raise e

        return inner

    return wrapper
