#!/usr/bin/env bash
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ..
sudo python3 ./infra/run/app_runner.py --interface ipython --app "interactive_leds.src.tic_tac_toe.tic_tac_toe" "$@"
