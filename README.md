# Mailman3 webhook archiver

![GitHub](https://img.shields.io/github/license/Laurent2916/mailman3_webhook_archiver)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)

A simple mailman3 archiver to notify a webhook of mails.

## Installation

A mailman archiver is a simple python package, to install it you can either use pip or install it manually.

If your use-case doesn't fit the this archiver feel free to fork this project, create an issue or a pull request.

### Install using pip (recommended)

Activate the python environment used by mailman.

Install the package using pip:
```bash
pip install git+https://github.com/Laurent2916/mailman3_webhook_archiver.git
```

### Install manually (not recommended)

Clone the repository:
```bash
git clone https://github.com/Laurent2916/mailman3_webhook_archiver.git
cd mailman3_webhook_archiver
```

Copy the `mailman3_webhook_archiver` folder into your environment libraries.
The process may look something like one of the following lines:
```bash
cp -r mailman3_webhook_archiver /usr/lib/python3/dist-packages/
cp -r mailman3_webhook_archiver /path/to/.venv/lib/python3.11/site-packages/
```

## Configuration

The archiver loads its configuration using an external configuration file.
Create and fill `/etc/mailman3/mailman-webhook-archiver.cfg` with the relevant informations.

```ini
[global]
url = https://webhook.example.com/foo/bar
key = SUPER_SECRET_TOKEN_KEY

filter_spam = false
monitored_lists = my_mailing_list, another_list, foo, bar, test
```

Modify the mailman configuration to enable the newly added archiver.
Append the following to `/etc/mailman3/mailman.cfg`.

```ini
[archiver.mailman3_webhook_archiver]
class: mailman3_webhook_archiver.WebhookArchiver
configuration: /etc/mailman3/mailman3_webhook_archiver.cfg
enable: yes
```

## Special thanks

- https://gitlab.com/mailman/mailman/blob/master/src/mailman/archiving/prototype.py
- https://github.com/nim65s/matrix-webhook/
