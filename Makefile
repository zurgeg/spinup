# Example of using makefiles with spinup
.PHONY all
PYTHON ?= python3
%.sh:SpinUpFile
  $(PYTHON) main.py generate SpinUpFile --script-file %.sh

all: boot.sh
