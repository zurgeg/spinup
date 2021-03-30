# Example of using makefiles with spinup

PYTHON ?= python3
%.sh:SpinUpFile
  $(PYTHON) main.py generate SpinUpFile --script-file %.sh
