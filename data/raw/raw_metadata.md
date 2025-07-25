This document has been taken from [https://gitlab.com/openpowerlifting/opl-data/blob/main/docs/data-readme.md](https://gitlab.com/openpowerlifting/opl-data/blob/main/docs/data-readme.md).

# OpenPowerlifting Data Distribution README
For a rendered version of this document, [view the README on GitLab](https://gitlab.com/openpowerlifting/opl-data/blob/main/docs/data-readme.md).

## CSV Data Format
The OpenPowerlifting database is distributed as a CSV file for your convenience.

The CSV format used is simple: double-quotes and in-field commas are disallowed.

### Name
Mandatory. The name of the lifter in UTF-8 encoding.

Lifters who share the same name are distinguished by use of a `#` symbol followed by a unique number. For example, two lifters both named `John Doe` would have `Name` values `John Doe #1` and `John Doe #2` respectively.

### Sex
Mandatory. The sex category in which the lifter competed, `M`, `F`, or `Mx`.

Mx (pronounced *Muks*) is a gender-neutral title — like Mr and Ms — originating from the UK. It is a catch-all sex category that is particularly appropriate for non-binary lifters.

The `Sex` column is defined by [crates/opltypes/src/sex.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/opltypes/src/sex.rs).

### Event
Mandatory. The type of competition that the lifter entered.

Values are as follows:

- SBD: Squat-Bench-Deadlift, also commonly called "Full Power".
- BD: Bench-Deadlift, also commonly called "Ironman" or "Push-Pull".
- SD: Squat-Deadlift, very uncommon.
- SB: Squat-Bench, very uncommon.
- S: Squat-only.
- B: Bench-only.
- D: Deadlift-only.

The `Event` column is defined by [crates/opltypes/src/event.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/opltypes/src/event.rs).

### Equipment
Mandatory. The equipment category under which the lifts were performed.

Note that this *does not mean that the lifter was actually wearing that equipment!* For example, GPC-affiliated federations do not have a category that disallows knee wraps. Therefore, all lifters, even if they only wore knee sleeves, nevertheless competed in the `Wraps` equipment category, because they were allowed to wear wraps.

Values are as follows:

- Raw: Bare knees or knee sleeves.
- Wraps: Knee wraps were allowed.
- Single-ply: Equipped, single-ply suits.
- Multi-ply: Equipped, multi-ply suits (includes Double-ply).
- Unlimited: Equipped, multi-ply suits or rubberized gear (like Bench Daddies).
- Straps: Allowed straps on the deadlift (used mostly for exhibitions, not real meets).

The `Equipment` column is defined by [crates/opltypes/src/equipment.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/opltypes/src/equipment.rs).

### Age
Optional. The age of the lifter on the start date of the meet, if known.

Ages can be one of two types: exact or approximate. Exact ages are given as integer numbers, for example `23`. Approximate ages are given as an integer plus `0.5`, for example `23.5`.

Approximate ages mean that the lifter could be either of *two* possible ages. For an approximate age of `n + 0.5`, the possible ages are `n` or `n+1`. For example, a lifter with the given age `23.5` could be either `23` or `24` -- we don't have enough information to know.

Approximate ages occur because some federations only provide us with birth year information. So another way to think about approximate ages is that `23.5` implies that the lifter turns `24` that year.

The `Age` column is defined by [crates/opltypes/src/age.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/opltypes/src/age.rs).

### AgeClass
Optional. The age class in which the filter falls, for example `40-45`. These classes are based on exact age of the lifter on the day of competition.

AgeClass is mostly useful because sometimes a federation will report that a lifter competed in the 50-54 division without providing any further age information. This way, we can still tag them as 50-54, even if the `Age` column is empty.

The full range available to `AgeClass` is defined by [crates/opltypes/src/ageclass.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/opltypes/src/ageclass.rs).

### BirthYearClass
Optional. The birth year class in which the filter falls, for example `40-49`. The ages in the range are the oldest possible ages for the lifter that year. For example, `40-49` means "the year the lifter turns 40 through the full year in which the lifter turns 49."

`BirthYearClass` is used primarily by the IPF and by IPF affiliates. Non-IPF federations tend to use `AgeClass` instead.

The full range available to `BirthYearClass` is defined by [crates/opltypes/src/birthyearclass.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/opltypes/src/birthyearclass.rs).

### Division
Optional. Free-form UTF-8 text describing the division of competition, like `Open` or `Juniors 20-23` or `Professional`.

Some federations are *configured* in our database, which means that we have agreed on a limited set of division options for that federation, and we have rewritten their results to only use that set, and tests enforce that. Even still, divisions are not standardized *between* configured federations: it really is free-form text, just to provide context.

Information about age should not be extracted from the `Division`, but from the `AgeClass` column.

### BodyweightKg
Optional. The recorded bodyweight of the lifter at the time of competition, to two decimal places.

### WeightClassKg
Optional. The weight class in which the lifter competed, to two decimal places.

Weight classes can be specified as a maximum or as a minimum. Maximums are specified by just the number, for example `90` means "up to (and including) 90kg." minimums are specified by a `+` to the right of the number, for example `90+` means "above (and excluding) 90kg."

`WeightClassKg` is defined by [crates/opltypes/src/weightclasskg.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/opltypes/src/weightclasskg.rs).

### Squat1Kg, Bench1Kg, Deadlift1Kg
Optional. First attempts for each of squat, bench, and deadlift, respectively. Maximum of two decimal places.

Negative values indicate failed attempts.

Not all federations report attempt information. Some federations only report Best attempts.

### Squat2Kg, Bench2Kg, Deadlift2Kg
Optional. Second attempts for each of squat, bench, and deadlift, respectively. Maximum of two decimal places.

Negative values indicate failed attempts.

Not all federations report attempt information. Some federations only report Best attempts.

### Squat3Kg, Bench3Kg, Deadlift3Kg
Optional. Third attempts for each of squat, bench, and deadlift, respectively. Maximum of two decimal places.

Negative values indicate failed attempts.

Not all federations report attempt information. Some federations only report Best attempts.

### Squat4Kg, Bench4Kg, Deadlift4Kg
Optional. Fourth attempts for each of squat, bench, and deadlift, respectively. Maximum of two decimal places.

Negative values indicate failed attempts.

Fourth attempts are special, in that they do not count toward the `TotalKg`. They are used for recording single-lift records.

### Best3SquatKg, Best3BenchKg, Best3DeadliftKg
Optional. Maximum of the first three successful attempts for the lift.

Rarely may be negative: that is used by some federations to report the lowest weight the lifter attempted and failed.

### TotalKg
Optional. Sum of `Best3SquatKg`, `Best3BenchKg`, and `Best3DeadliftKg`, if all three lifts were a success.
If one of the lifts was failed, or the lifter was disqualified for some other reason, the `TotalKg` is empty.

Rarely, mostly for older meets, a federation will report the total but not *any* lift information.

### Place
Mandatory. The recorded place of the lifter in the given division at the end of the meet.

Values are as follows:

- Positive number: the place the lifter came in.
- G: Guest lifter. The lifter succeeded, but wasn't eligible for awards.
- DQ: Disqualified. Note that DQ could be for procedural reasons, not just failed attempts.
- DD: Doping Disqualification. The lifter failed a drug test.
- NS: No-Show. The lifter did not show up on the meet day.

The `Place` column is defined by [crates/opltypes/src/place.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/opltypes/src/place.rs).

### Dots
Optional. A positive number if Dots points could be calculated, empty if the lifter was disqualified.

Dots is very similar to (and drop-in compatible with) the original Wilks formula.
It uses an updated, simpler polynomial and is built against data from drug-tested Raw lifters, as opposed to against data from drug-tested Single-ply lifters.
The Dots formula was created by Tim Konertz of the BVDK in 2019.

The calculation of Dots points is defined by [crates/coefficients/src/dots.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/coefficients/src/dots.rs).

### Wilks
Optional. A positive number if Wilks points could be calculated, empty if the lifter was disqualified.

Wilks is the most common formula used for determining Best Lifter in a powerlifting meet.

The calculation of Wilks points is defined by [crates/coefficients/src/wilks.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/coefficients/src/wilks.rs).

### Glossbrenner
Optional. A positive number if Glossbrenner points could be calculated, empty if the lifter was disqualified.

Glossbrenner was created by Herb Glossbrenner as an update of the Wilks formula.
It is most commonly used by GPC-affiliated federations.

The calculation of Glossbrenner points is defined by [crates/coefficients/src/glossbrenner.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/coefficients/src/glossbrenner.rs).

### Goodlift
IPF GL Points. The successor to IPF Points (2019-01-01 through 2020-04-30).

Optional. A positive number if IPF GL Points could be calculated, empty if the lifter was disqualified or IPF GL Points were undefined for the Event type.

IPF GL Points roughly express relative performance to the expected performance of that weight class at an IPF World Championship event, as a percentage.

The calculation of IPF GL points is defined by [crates/coefficients/src/goodlift.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/coefficients/src/goodlift.rs).

### Tested
Optional. `Yes` if the lifter entered a drug-tested category, empty otherwise.

Note that this records whether the results *count as drug-tested*, which does not imply that the lifter actually took a drug test.
Federations do not report which lifters, if any, were subject to drug testing.

### Country
Optional. The home country of the lifter, if known.

The full list of valid Country values is defined by [crates/opltypes/src/country.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/opltypes/src/country.rs).

### State
Optional. The home state/province/oblast/division/etc of the lifter, if known.

The full list of valid State values is defined by [crates/opltypes/src/states.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/opltypes/src/states.rs).
Expanded names are given there in comments.

### Federation
Mandatory. The federation that hosted the meet.

Note that this may be different than the international federation that provided sanction to the meet.
For example, USPA meets are sanctioned by the IPL, but we record USPA meets as `USPA`.

The full list of valid Federation values is defined by [crates/opltypes/src/federation.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/opltypes/src/federation.rs).
Comments in that file help explain what each federation value means.

### ParentFederation
Optional. The topmost federation that sanctioned the meet, usually the international body.

For example, the `ParentFederation` for the `USAPL` and `EPA` is `IPF`.

### Date
Mandatory. The start date of the meet in [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601).
ISO 8601 looks like `YYYY-MM-DD`: as an example, `1996-12-04` would be December 4th, 1996.

Meets that last more than one day only have the start date recorded.

### MeetCountry
Mandatory. The country in which the meet was held.

The full list of valid Country values is defined by [crates/opltypes/src/country.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/opltypes/src/country.rs).

### MeetState
Optional. The state, province, or region in which the meet was held.

The full list of valid State values is defined by [crates/opltypes/src/state.rs](https://gitlab.com/openpowerlifting/opl-data/blob/main/crates/opltypes/src/state.rs).

### MeetName
Mandatory. The name of the meet.

The name is defined to never include the year or the federation.
For example, the meet officially called `2019 USAPL Raw National Championships` would have the MeetName `Raw National Championshps`.

### Sanctioned
Optional. Whether the meet counts as officially sanctioned by a federation we recognize.

Values are "Yes" for sanctioned and "No" for unsanctioned.

Defaults to "Yes".

Sanctioned meets are competitions that are recognized by a standards body that we recognize (a federation).
A federation may also sometimes choose to host an unsanctioned meet with a relaxed ruleset for novices.

Unsanctioned meets are competitions that were put on by individual meet directors, typically outside of a federation.
In OpenPowerlifting, unsanctioned meets are tracked, but do not count for rankings or records.
