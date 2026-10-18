# OM Digital RS foot pedal on macOS

Status: done
Claimed by: none
Blocked by: none

## Outcome

The active Karabiner rule and the reusable Mac setup file match both the older
Olympus RS foot switch (`1972:660`) and the connected OM Digital RS foot switch
(`13218:660`). The pedal still sends Apple Dictation through Karabiner.

## Decisions so far

- 2026-10-18, agent: Keep both vendor IDs in one `device_if` condition so the
  existing pedal setup keeps working on either RS Series variant.

## Authorizations and deferrals

- 2026-10-18, owner: "If so, could you add this series as well" authorized the
  additional device ID in the live rule and repository setup file.
- 2026-10-18, owner: "If you need to push anything, go ahead" authorized
  publishing this fix after integrating current `origin/main`. This ends with
  that push.

## Verification

- Karabiner listed the connected `13218:660` keyboard interface and loaded the
  updated active profile. Its complex-modification linter accepted both copies
  of the rule.
- The owner confirmed that pressing the Windows+H pedal starts Apple Dictation.
- Change commit: `2c6ec5ec`. Integrated `origin/main` by merge commit
  `d857eaf7`. After the merge, the full test suite passed: 85 tests.
