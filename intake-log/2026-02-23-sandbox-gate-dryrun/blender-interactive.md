# Skill Intake Gate Report

- Path: `/Users/kjaylee/.openclaw/workspace/misskim-skills/skills/blender-interactive`
- Risk: **high** (score=23)
- Recommendation: `reject_or_rewrite`

## Matches by category
- network: 25
- fs_write: 1
- proc_exec: 1

## Top findings
- `blender_socket_addon.py:15` [network] `import socket`
- `blender_socket_addon.py:237` [proc_exec] `exec(code, namespace)`
- `blender_socket_addon.py:553` [network] `self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
- `blender_socket_addon.py:554` [network] `self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)`
- `blender_socket_addon.py:586` [network] `except socket.timeout:`
- `blender_socket_addon.py:641` [network] `except socket.timeout:`
- `scripts/blender_client.py:19` [network] `import socket`
- `scripts/blender_client.py:28` [network] `sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
- `scripts/blender_client.py:55` [network] `except socket.timeout:`
- `scripts/sketchfab.py:20` [network] `from urllib import request, parse, error`
- `scripts/sketchfab.py:22` [network] `API_BASE = "https://api.sketchfab.com/v3"`
- `scripts/sketchfab.py:148` [network] `"https://sketchfab.com/settings/password 에서 발급 후 "`
- `scripts/sketchfab.py:193` [fs_write] `os.remove(zip_path)`
- `scripts/polyhaven.py:26` [network] `Poly Haven API 문서: https://api.polyhaven.com`
- `scripts/polyhaven.py:37` [network] `import requests`
- `scripts/polyhaven.py:40` [network] `import urllib.request`
- `scripts/polyhaven.py:41` [network] `import urllib.parse`
- `scripts/polyhaven.py:45` [network] `API_BASE = "https://api.polyhaven.com"`
- `scripts/polyhaven.py:50` [network] `"""HTTP GET — requests 또는 urllib 사용"""`
- `scripts/polyhaven.py:50` [network] `"""HTTP GET — requests 또는 urllib 사용"""`
- `scripts/polyhaven.py:53` [network] `resp = requests.get(url, params=params, headers=headers, timeout=30)`
- `scripts/polyhaven.py:58` [network] `query = urllib.parse.urlencode(params)`
- `scripts/polyhaven.py:60` [network] `req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})`
- `scripts/polyhaven.py:61` [network] `with urllib.request.urlopen(req, timeout=30) as resp:`
- `scripts/polyhaven.py:70` [network] `resp = requests.get(url, headers=headers, stream=True, timeout=120)`
- `scripts/polyhaven.py:76` [network] `req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})`
- `scripts/polyhaven.py:77` [network] `with urllib.request.urlopen(req, timeout=120) as resp:`
