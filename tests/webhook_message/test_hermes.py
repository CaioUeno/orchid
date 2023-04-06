import re
from unittest.mock import Mock, patch

from discord_webhook import DiscordWebhook
from slack_sdk.webhook import WebhookClient

from orchid.decorators import hermes


class TestHermes:
    @staticmethod
    def tmp_file_message(tmp_path, message):
        d = tmp_path / "sub"
        if not d.exists():
            d.mkdir()
        d
        p = d / "tmp.txt"
        p.write_text(message)

    # @patch("discord_webhook.DiscordWebhook", spec=DiscordWebhook)
    # def test_send_message_discord(self, mock_webhook, tmp_path):
    #     message = "a"

    #     mock_webhook.set_content = Mock()

    #     mock_webhook.execute = Mock(
    #         side_effect=lambda: self.tmp_file_message(tmp_path, message)
    #     )

    #     @hermes(webhook=mock_webhook, tag="123")
    #     def dummy():
    #         return True

    #     returned = dummy()

    #     d = tmp_path / "sub"
    #     p = d / "tmp.txt"

    #     messsage_sent = p.read_text()

    #     assert "<@123>" in messsage_sent

    #     assert p.read_text() == "a"

    @patch("slack_sdk.webhook.WebhookClient", spec=WebhookClient)
    def test_send_message_slack(self, mock_webhook, tmp_path):
        mock_webhook.send = Mock(
            side_effect=lambda text: self.tmp_file_message(tmp_path, text)
        )

        @hermes(webhook=mock_webhook, tag="123", timestamp=True)
        def dummy():
            return True

        _ = dummy()

        d = tmp_path / "sub"
        p = d / "tmp.txt"

        messsage_sent = p.read_text()

        assert "<@123>" in messsage_sent
        assert "dummy has finished!" in messsage_sent
        assert bool(re.search("\(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\)", messsage_sent))
