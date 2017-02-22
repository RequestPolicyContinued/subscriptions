# NOTE: in this file tab indentation is used.
# Otherwise .RECIPEPREFIX would have to be set.

#
# create variables
#

subscription_lists := official.json

# subscriptions are all json file except those in $(subscription_lists)
all_json_files := $(wildcard *.json)
subscriptions := $(filter-out $(subscription_lists),$(all_json_files))


#
# define targets
#

# set "check" to be the default target
.DEFAULT_GOAL := check

# all checks and their order of execution
checks := check_json_validity \
	check_duplicate_lines \
	check_serials

.PHONY: check test
.PHONY: $(checks)
check test: $(checks)

# ____________________
# check JSON validity
#

check_json_validity:
	@for file in $(all_json_files) ; do \
	echo -n "$$file: "; (cat official.json | python -m json.tool > /dev/null && echo "Valid JSON") || echo "Invalid JSON" ; \
	done

# __________________________
# check for matching serials
#

check_serials:
	python check_serials.py

# _________________________
# check for duplicate lines
#

duplicate_rules := $(shell egrep -ho '\{.*\}' $(subscriptions) | sort | uniq -d)
duplicate_rules_quoted := $(addprefix ',$(addsuffix ',$(duplicate_rules)))

check_duplicate_lines:
	@# go through all duplicates and report in which subscription files they are
	@for rule in $(duplicate_rules_quoted) ; do \
		echo '___Duplicate rule___' ; \
		fgrep -nHT $$rule $(subscriptions) ; \
	done
