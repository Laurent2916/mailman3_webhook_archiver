"""Archiver sending notifications to an HTTP webhook."""

import logging
from configparser import NoOptionError

import requests
from mailman.config import config
from mailman.config.config import external_configuration
from mailman.interfaces.archiver import IArchiver
from zope.interface import implementer

logger = logging.getLogger("mailman.archiver.webhook")


@implementer(IArchiver)
class WebhookArchiver:
    """Archiver sending notifications to an HTTP webhook."""

    name = "mailman3_webhook_archiver"
    is_enabled = False

    @staticmethod
    def list_url(mlist):
        """Return the url to the top of the list's archive.

        The archiver is not web-accessible, return None.
        """
        return

    @staticmethod
    def permalink(mlist, msg):
        """Return the url to the message in the archive.

        The archiver is not web-accessible, return None.
        """
        return

    def __init__(self):
        """Initialize the archiver, parse mailman configuration file.

        The configuration file is located at /etc/mailman3/mailman-webhook-archiver.cfg
        """
        # read mailman configuration file
        archiver_config = external_configuration(config.archiver.mailman3_webhook_archiver.configuration)

        # parse webhook url
        self.url = archiver_config.get("global", "url")
        logger.debug(f"webhook url: {self.url}")

        # parse webhook key
        self.key = archiver_config.get("global", "key")
        logger.debug(f"webhook key: {self.key}")

        try:  # parse webhook spam filter option
            self.filter_spam = archiver_config.get("global", "filter_spam")
            logger.debug(f"filter_spam: {self.filter_spam}")
        except (KeyError, NoOptionError):
            self.filter_spam = False
            logger.debug("filter_spam option not found, set to False")

        try:  # parse webhook monitored lists
            lists = archiver_config.get("global", "monitored_lists")
            self.monitored_lists = [lst.strip() for lst in lists.split(",")]
            logger.debug(f"monitored_lists: {self.monitored_lists}")
        except (KeyError, NoOptionError):
            self.monitored_lists = None
            logger.debug("monitored_lists option not found, set to None")

    def archive_message(self, mlist, msg) -> None:
        """Get message from mailman and notify webhook."""
        # check if message is from monitored list
        if self.monitored_lists and mlist.list_name not in self.monitored_lists:
            logger.debug(f"{mlist.list_name} list is not monitored lists")
            return

        # retreive email subject
        subject = msg["subject"] if "subject" in msg else "No subject"
        logger.debug(f"subject: {subject}")

        # check if message is spam
        if self.filter_spam and str(subject).startswith("[SPAM"):
            logger.debug("message is spam")
            return

        # build HTTP request body
        data = {
            "body": f"You got mail !<br/>{msg['from']}: {subject}",
            "key": self.key,
        }

        # send request to webhook
        response = requests.post(
            url=self.url,
            timeout=5,
            json=data,
        )

        # check response
        if response.status_code != 200:
            logger.error(f"Error while sending message: {response.text}")
        else:
            logger.debug("Message sent to webhook !")
