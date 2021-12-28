# Sneha Assessment
Requires atleast Python 3.7

Requires no external dependencies

Tested on Python 3.7.9

You can execute the script by passing the input data using either STDIN or as a file argument

Example:

```cat data.json | python export.py```

OR

```python export.py data.json```

You can also specify the output file paths for visits.json and hits.json as:

```python export.py data.json -ov new_dir/new_visits.json -oh new_dir/new_hits.json```

Resulting `hits.json` file has hits with new key `visit_id` as `{fullVisitorId}_{visitId}` which can be related to the new key `unique_visit_id` in `visits.json` which has the same value as `{fullVisitorId}_{visitId}`
