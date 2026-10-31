# API updates: command endpoints migrated to `SendCommandByAPP`

The openapiv3 platform API renamed its methods and changed the command payload
shape. This release updates the library accordingly and adds helpers for two
related endpoints that were previously unavailable.

## What changed

### `API.send_command()` — replaced endpoint and payload

**Before** (no longer available on the server — returns HTTP 500 for any caller):

```python
payload = {
    "DeviceID": self.device_id,   # str
    "Content": content            # raw command text
}
await self.get_request("SendCommand", payload)
```

**After**:

```python
payload = {
    "SN": device_info.sn,          # device serial
    "DeviceID": int(...),          # int, not str
    "CommandType": "808DYD",       # platform command name
    "Model": int(device_info.model),
    "Paramter": "",                # optional extra parameter
    "Key": session_key
}
await self.get_request("SendCommandByAPP", payload)
```

The single-argument call style is unchanged (`send_command("DY")`), and the
legacy short command names are translated automatically:

| Legacy name | `CommandType` | Action |
|---|---|---|
| `"DY"` | `808DYD` | cut oil / engine |
| `"KY"` | `808HFYD` | restore oil / engine |

Names that already match the platform form (e.g. `"808DYD"`) are passed through
untouched, so any platform-catalog command can be sent directly. The full
per-device catalog is available through `get_command_list()`.

### Return value semantics

`SendCommandByAPP` queues the command and dispatches it to the device
asynchronously (usually within seconds, occasionally a minute or more).

| Result code | Meaning |
|---|---|
| `-5` | accepted and queued; dispatch pending |
| `-4` | rejected — invalid `CommandType` for this device |

Because queuing is only the first step, always confirm delivery/acknowledgement
via the new helpers below.

### New helpers

```python
async def get_command_list(page_no=1, page_count=50, time_zones="2:00", language="en")
```
Command history/catalog for the logged-in device. Each entry contains the
command id, `commandName` (platform command name — same format as
`CommandType`), `sendDate`, dispatch state (`isSend`) and the device ack
(`isResponse`, `responseText`, `responseDate`).

```python
async def get_response(command_id, time_zones="2:00")
```
Poll the acknowledgement of one previously queued command by id —
`{"state": ..., "isResponse": "0/1", "responseMsg": "..."}`.

Both require a successful `login()` first (they use `SN`, `DeviceID`,
`Model` and the session key).

### Extension parameter

`send_command(command_type, parameter="")` gained an optional `parameter`
argument, passed to the platform as `Paramter` (the API's own field name) for
commands that require one.

## Usage

```python
async with API("http://www.aika168.com/") as tracker:
    await tracker.login(device_id, password)

    result = await tracker.send_command("DY")     # -> -5 (queued)
    print(result)

    history = await tracker.get_command_list()    # isSend / isResponse per command
    # ... poll get_response(command_id) for the device ack ("Success!")
```

## Tests

`tests/test_api.py` covers the new payloads (aliasing, pass-through of
platform-form names and both new helpers).
