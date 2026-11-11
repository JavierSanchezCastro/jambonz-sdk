# Installation

## Requirements

- Python 3.10+
- For static typing of verbs: mypy >= 2.4 (see [Type checking](#type-checking))
- A jambonz account ([jambonz.cloud](https://jambonz.cloud) or self-hosted)

## Install

=== "pip"

    ```bash
    pip install jambonz-sdk
    ```

=== "uv"

    ```bash
    uv add jambonz-sdk
    ```

=== "poetry"

    ```bash
    poetry add jambonz-sdk
    ```

## Type checking

Optional verb fields are typed `T | MISSING` (pydantic's PEP 661 sentinel), so a
type checker rejects `Say(text=None)` and makes you narrow `say.loop is not MISSING`.
That needs a checker with sentinel support:

- **mypy >= 2.4** (older versions treat `MISSING` as `Any` and silently accept `None`)
- pyright 1.1.414 (via basedpyright 1.40.2) was checked against the typing test cases and works

## Configuration

The SDK reads credentials automatically from environment variables or a `.env` file:

```bash title=".env"
JAMBONZ_ACCOUNT_SID=your-account-sid
JAMBONZ_API_KEY=your-api-key
```

Or pass them directly:

```python
from jambonz import JambonzClient

client = JambonzClient(
    account_sid="your-account-sid",
    api_key="your-api-key",
)
```

Get your Account SID and API Key from the [jambonz portal](https://jambonz.cloud) under **Account** settings.

### Optional settings

| Variable | Default | Description |
|---|---|---|
| `JAMBONZ_ACCOUNT_SID` | — | Your account identifier |
| `JAMBONZ_API_KEY` | — | Your API key |
| `JAMBONZ_BASE_URL` | `https://api.jambonz.cloud` | API base URL (change for self-hosted) |
