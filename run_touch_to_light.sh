#!/usr/bin/env bash
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ..
python3 ./infra/run/app_runner.py --interface ipython --app "interactive_leds.src.touch_to_light.touch_to_light" "$@"
