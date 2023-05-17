# Variables
PYTHON = python3
SRC_DIR = srcs
SCRIPT = bot.py

# Targets
.PHONY: all run

all: run

run:
	$(PYTHON) $(SRC_DIR)/$(SCRIPT)