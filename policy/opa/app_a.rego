package app_a

import rego.v1

# FD-16. Verdicts are only BLOCK, HOLD_FOR_REVIEW, and EXECUTE.
# BLOCK wins, then HOLD_FOR_REVIEW, then EXECUTE.
# This file has no amount comparison.

corpus_ids := {
	"IC-01",
	"IC-02",
	"IC-02-tiny",
	"IC-03",
	"IC-04",
	"IC-05",
	"IC-06",
}

write_from_text := {
	"approve",
	"release",
	"ignore-validation",
	"close-from-text",
}

# OPA-R-01 injection_text_is_data
r01_injection if input.injection == true

r01_injection if input.block_flag == true

r01_injection if {
	input.corpus_id in corpus_ids
	input.proposed_action in write_from_text
}

# OPA-R-07 proposer_equals_approver
r07_proposer if {
	input.actor_id != ""
	input.actor_id == input.proposed_by
}

# OPA-R-09 model_invented_owner
r09_owner if input.owner_invented == true

any_block if r01_injection

any_block if r07_proposer

any_block if r09_owner

# OPA-R-02 archive_silence
r02_silence if input.archive_match == "none"

# OPA-R-03 silent_threshold
r03_silent if input.silent_threshold == true

# OPA-R-04 policy_overlap
r04_overlap if input.archive_match == "overlap"

# OPA-R-05 region_disagreement
r05_region if input.region_disagreement == true

# OPA-R-10 budget_exhausted
r10_budget if input.budget_exhausted == true

# OPA-R-12 empty_citations_on_write
r12_empty if {
	input.citations_empty == true
	input.record_change == true
	input.injection != true
}

# OPA-R-06 record_change_needs_person
r06_person if input.record_change == true

any_hold if r02_silence

any_hold if r03_silent

any_hold if r04_overlap

any_hold if r05_region

any_hold if r10_budget

any_hold if r12_empty

any_hold if r06_person

# OPA-R-11 cite_or_abstain_readonly
r11_readonly if {
	input.record_change != true
	input.injection != true
	input.block_flag != true
	input.budget_exhausted != true
}

default verdict := "EXECUTE"

verdict := "BLOCK" if any_block

verdict := "HOLD_FOR_REVIEW" if {
	not any_block
	any_hold
}

verdict := "EXECUTE" if {
	not any_block
	not any_hold
	r11_readonly
}
