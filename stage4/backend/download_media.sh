#!/bin/bash
pip install gdown
gdown https://drive.google.com/drive/folders/1tCYiEiYwLagJAN0OKQOdKivf30HSud_F?usp=sharing -O media.zip
unzip media.zip -d media/
rm media.zip
