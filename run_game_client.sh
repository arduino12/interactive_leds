#!/usr/bin/env bash
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ..
python3 ./infra/run/app_runner.py --interface loop --app "interactive_leds.src.game_client.game_client" "$@"
