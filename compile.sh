#!/bin/bash
ls | grep -v pycache | grep -v .png | grep -v .zip | grep -v .sh | xargs zip AnkiTouchFloat.zip