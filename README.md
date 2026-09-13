# Xbox Gamertag Generator & Checker

Generates one random candidate Xbox gamertag of a given length and checks it
against [OpenXBL](https://xbl.io) — one generate, one check, per run.

- Available → saved to `ign.txt`
- Taken (or checked either way) → saved to `gen.txt`, so it's never
  generated or checked again on future runs

## Requirements

- Python 3.9+
- [uv](https://docs.astral.sh/uv/) — used to run the script and manage its
  two dependencies (`requests`, `python-dotenv`) automatically
- A free [xbl.io](https://xbl.io) account for an API key

## 1. Install uv

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Alternatives: `winget install --id=astral-sh.uv -e` or, if you already have
Python, `pip install uv`.

### Linux / macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Alternative: `pip install uv`.

### Verify (both platforms)

```bash
uv --version
```

Restart your terminal first if the command isn't found.

## 2. Get an xbl.io API key

1. Go to [xbl.io](https://xbl.io) and sign in with your Microsoft/Xbox
   account.
2. Open your **Profile** page.
3. Generate a new **API key** and copy it.

Free accounts get **150 requests/hour** — this script uses exactly one
request per 25 secs

## 3. Configure your key

```

Open `.env` in any text editor and set:

```
XBL_API_KEY=your_key_here
```

## 4. Run it

From the project folder, on either platform:

```bash
uv run main.py <length>
```

Example — generate and check a 6-character gamertag:

```bash
uv run main.py 6
```

The first run installs `requests` and `python-dotenv` automatically (no
`pip install` or virtual environment setup needed) since they're declared
right at the top of `main.py`. Every run after that is instant.

Sample output:

```
Generated: kd9plq
Checking Xbox...
[+] kd9plq -> AVAILABLE
```

Run the command again whenever you want to try another candidate — each
run does after 25 secs, if it's more it will get too many request error.

## Files

| File           | Purpose                                                        |
| -------------- | --------------------------------------------------------------- |
| `main.py`      | The script itself                                                |
| `.env`         | Your personal API key (not committed to version control)        |
| `gen.txt`      | Every candidate already checked — doubles as the dedup lookup   |
| `ign.txt`      | Confirmed-available gamertags only                               |

If you're using git, add `.env` to your `.gitignore` so your key never gets
committed.