package app_b

import rego.v1

# Application B OPA. Verdicts are only BLOCK, HOLD_FOR_REVIEW, and EXECUTE.
# Each rule comments the lake item id it applies. This file is written from
# the pin cards. It is not a copy of app_a.rego as the rule source.

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

# lake item rule.untrusted_text.block
r_injection if input.injection == true

r_injection if input.block_flag == true

r_injection if {
	input.corpus_id in corpus_ids
	input.proposed_action in write_from_text
}

# lake item rule.hold.person_only
r_proposer if {
	input.actor_id != ""
	input.actor_id == input.proposed_by
}

# lake item decision.inc_2025_014
r_owner if input.owner_invented == true

any_block if r_injection

any_block if r_proposer

any_block if r_owner

# lake item rule.recipe_release.no_match
r_silence if input.archive_match == "none"

# lake item rule.threshold.silent
r_silent if input.silent_threshold == true

# lake item rule.policy.overlap_or_invalid
r_overlap if input.archive_match == "overlap"

# lake item rule.region.disagreement
r_region if input.region_disagreement == true

# lake item rule.hold.person_only
r_person if input.record_change == true

r_empty if {
	input.citations_empty == true
	input.record_change == true
	input.injection != true
}

any_hold if r_silence

any_hold if r_silent

any_hold if r_overlap

any_hold if r_region

any_hold if r_person

any_hold if r_empty

# lake item rule.threshold.never_999999 — no 999999 branch exists

default verdict := "EXECUTE"

verdict := "BLOCK" if any_block

verdict := "HOLD_FOR_REVIEW" if {
	not any_block
	any_hold
}

verdict := "EXECUTE" if {
	not any_block
	not any_hold
}
