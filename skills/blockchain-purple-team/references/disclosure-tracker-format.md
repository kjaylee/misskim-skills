# Disclosure Tracker Format

Use this format to track each externally reportable finding after it enters the disclosure queue.

## Suggested columns

| Field | Meaning |
|---|---|
| `project` | Project / protocol name |
| `chain` | Chain / testnet |
| `finding_id` | Stable internal ID |
| `tier` | R2 / R3 / R4 / R5 |
| `severity` | low / medium / high / critical |
| `scope` | contract / module / endpoint / ops / oracle / governance |
| `short_title` | One-line summary |
| `repro_type` | local fork / public testnet / live confirmed |
| `contact_channel` | bounty / email / GitHub / Discord / Telegram |
| `contact_target` | address, inbox, maintainer, or form |
| `sent_at` | UTC timestamp |
| `ack_status` | none / acknowledged / rejected / fixed |
| `response_window_days` | target private response window |
| `next_followup_at` | when to follow up |
| `fix_status` | none / in progress / patched / retest-needed / closed |
| `retest_status` | pending / passed / failed |
| `public_disclosure_allowed` | yes / no / deferred |
| `notes` | concise coordination notes |

## Minimal JSONL shape
```json
{"project":"Example","chain":"testnet","finding_id":"PT-03","tier":"R3","severity":"high","scope":"oracle","short_title":"stale price acceptance bypass","repro_type":"public testnet","contact_channel":"email","contact_target":"security@example.org","sent_at":"2026-03-12T00:00:00Z","ack_status":"acknowledged","response_window_days":7,"next_followup_at":"2026-03-19T00:00:00Z","fix_status":"in progress","retest_status":"pending","public_disclosure_allowed":"no","notes":"team confirmed receipt"}
```

## Tracker rules
- Track only R2+ findings here.
- Do not mix internal-only hypotheses into this board.
- Every row must have a `finding_id`, `repro_type`, and `contact_channel` once sent.
