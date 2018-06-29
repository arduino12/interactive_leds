#!/usr/bin/env bash
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ..
sudo python3 ./infra/run/app_runner.py --interface rpyc --app "interactive_leds.src.game_server.game_server" "$@"
