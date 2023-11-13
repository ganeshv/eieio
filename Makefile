# Makefile

# List of monitor programs
# Edit if you want to disable any
MONITORS := cpu net

# Determine the current directory
# The virtualenv will be created here
BASEDIR := $(shell pwd)

# Virtual environment directory
VENV := $(BASEDIR)/eieio-ve

# Template files
SH_TEMPLATE := eieio_login.sh.tmpl
PLIST_TEMPLATE := plist.tmpl

# Plist install location
PLIST_INSTALL_DIR := $(HOME)/Library/LaunchAgents

# Output files
SH_OUTPUT := $(BASEDIR)/eieio_login.sh

PLIST_OUTPUTS := $(patsubst %,$(BASEDIR)/%.plist,$(MONITORS))
PLIST_INSTALL_OUTPUTS := $(patsubst %,$(PLIST_INSTALL_DIR)/io.github.ganeshv.%.plist,$(MONITORS))


# User ID for launchctl
USER_ID := $(shell id -u)

.PHONY: all install clean

all: $(VENV) $(SH_OUTPUT) $(PLIST_OUTPUTS)

install: all
	@mkdir -p $(PLIST_INSTALL_DIR)
	@$(foreach prog, $(MONITORS), \
		cp $(BASEDIR)/$(prog).plist $(PLIST_INSTALL_DIR)/io.github.ganeshv.eieio-$(prog).plist; \
		launchctl bootstrap gui/$(USER_ID) $(PLIST_INSTALL_DIR)/io.github.ganeshv.eieio-$(prog).plist; \
		launchctl kickstart gui/$(USER_ID)/io.github.ganeshv.eieio-$(prog); \
	)
	@echo "Installation complete."

$(VENV):
	@echo "Creating virtual environment..."
	@virtualenv -p python3 $(VENV)
	@source $(VENV)/bin/activate; pip install -r requirements.txt

$(SH_OUTPUT): $(SH_TEMPLATE)
	@echo "Generating eieio_login.sh..."
	@sed 's|{{BASEDIR}}|$(BASEDIR)|g' $(SH_TEMPLATE) > $(SH_OUTPUT)
	@chmod +x $(SH_OUTPUT)

$(BASEDIR)/%.plist: $(PLIST_TEMPLATE)
	@echo "Generating plist for $*..."
	@MONITOR_NAME=`basename $@ .plist`; \
	sed -e 's|{{BASEDIR}}|$(BASEDIR)|g' -e 's|{{MONITOR}}|'$$MONITOR_NAME'|g' $< > $@

uninstall:
	@$(foreach prog, $(MONITORS), \
		launchctl bootout gui/$(USER_ID) $(PLIST_INSTALL_DIR)/io.github.ganeshv.eieio-$(prog).plist; \
		rm -f $(PLIST_INSTALL_DIR)/io.github.ganeshv.eieio-$(prog).plist; \
	)

clean:
	@rm -f $(SH_OUTPUT)
	@$(foreach prog, $(MONITORS), \
		rm -f $(prog).plist; \
	)
	@if [ -f $(VENV)/bin/activate ]; then \
		rm -rf $(VENV); \
	fi

