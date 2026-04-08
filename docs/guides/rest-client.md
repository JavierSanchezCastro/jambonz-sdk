# REST Client

## Sync vs Async

```python
from jambonz import JambonzClient, AsyncJambonzClient

# Sync
with JambonzClient() as client:
    carriers = client.carriers.list()

# Async
async with AsyncJambonzClient() as client:
    carriers = await client.carriers.list()
```

## Resources

All resources support: `list()`, `get(sid)`, `create(**data)`, `update(sid, **data)`, `delete(sid)`.

### Accounts

```python
accounts = await client.accounts.list()
account = await client.accounts.get("account-sid")
```

### Users

```python
users = await client.users.list()
```

### API Keys

```python
keys = await client.api_keys.list()
new_key = await client.api_keys.create()
```

### Carriers

```python
carriers = await client.carriers.list()
carrier = await client.carriers.create(
    name="my-carrier",
    trunk_type="static_ip",
)
```

### SIP Gateways

```python
gateways = await client.gateways.list(voip_carrier_sid="carrier-sid")
await client.gateways.create(
    ipv4="192.76.120.10",
    port=5060,
    voip_carrier_sid="carrier-sid",
    inbound=True,
)
```

### Phone Numbers

```python
numbers = await client.phone_numbers.list()
await client.phone_numbers.create(
    number="34931228497",
    voip_carrier_sid="carrier-sid",
    application_sid="app-sid",
)
```

### Applications

```python
apps = await client.applications.list()
await client.applications.create(
    name="my-app",
    call_hook="https://example.com/call",
    call_status_hook="https://example.com/status",
)
```

### Speech Services

```python
services = await client.speech_services.list()
```

### Active Calls (Call Control)

```python
# List active calls
active = await client.calls.list()

# Create an outbound call
call = await client.calls.create(
    from_="+34931228497",
    to={"type": "phone", "number": "+34600000000"},
    application_sid="app-sid",
)

# Update a call (mute, hold, whisper, hangup)
await client.calls.update("call-sid", call_status="completed")

# Delete a call
await client.calls.delete("call-sid")
```

### Recent Calls

```python
calls = await client.recent_calls.list(days=7, page=1, count=25)
for call in calls:
    print(f"{call.direction}: {call.from_} -> {call.to} ({call.duration}s)")
```

## Error Handling

```python
from jambonz.exceptions import (
    JambonzAuthError,
    JambonzNotFoundError,
    JambonzRateLimitError,
    JambonzAPIError,
)

try:
    carrier = await client.carriers.get("bad-sid")
except JambonzNotFoundError:
    print("Not found")
except JambonzAuthError:
    print("Invalid credentials")
except JambonzRateLimitError:
    print("Rate limited (SDK retries automatically)")
except JambonzAPIError as e:
    print(f"Error {e.status_code}: {e}")
```

## Request Hooks

```python
client = AsyncJambonzClient(
    on_request=lambda req: print(f"-> {req.method} {req.url}"),
    on_response=lambda res: print(f"<- {res.status_code}"),
)
```
