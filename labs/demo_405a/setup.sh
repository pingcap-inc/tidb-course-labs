#!/bin/bash

set -e

wget -qO uv.tar.gz https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz
sudo tar xf uv.tar.gz --strip-components=1 -C /usr/local/bin uv-x86_64-unknown-linux-gnu/uv
uv venv
source .venv/bin/activate
uv pip install python-dotenv dotenv mysql-connector-python pymysql