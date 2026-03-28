# E2E Test Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement end-to-end tests for MusicTUI using Textual Pilot framework

**Architecture:** Create E2E test suite with separate test files for app flow, using Textual's Pilot system to simulate user interactions (key presses) and validate UI state changes

**Tech Stack:** pytest, textual.pilot.Pilot, pygame (with dummy audio driver)

---

### Task 1: Create test directory structure and fixtures

**Files:**
- Create: `tests/e2e/__init__.py`
- Create: `tests/e2e/conftest.py`
- Create: `tests/e2e/test_app_flow.py`

- [ ] **Step 1: Create tests/e2e directory and __init__.py**

```bash
mkdir -p tests/e2e && touch tests/e2e/__init__.py
```

- [ ] **Step 2: Create conftest.py with fixtures**

```python
import os
import pytest
from src.app import MusicTUI

os.environ["SDL_AUDIODRIVER"] = "dummy"

@pytest.fixture
def test_audio_file():
    """Return path to test audio file"""
    return "tests/e2e/fixtures/test.mp3"

@pytest.fixture
async def app_with_pilot():
    """Create app instance with pilot for testing"""
    app = MusicTUI()
    async with app.run_test() as pilot:
        yield app, pilot
```

- [ ] **Step 3: Commit**

```bash
git add tests/e2e/__init__.py tests/e2e/conftest.py
git commit -m "test: add e2e test directory structure and fixtures"
```

---

### Task 2: Create test audio fixture file

**Files:**
- Create: `tests/e2e/fixtures/test.mp3`

- [ ] **Step 1: Create fixtures directory**

```bash
mkdir -p tests/e2e/fixtures
```

- [ ] **Step 2: Create a small valid MP3 file**

Use a minimal valid MP3 file for testing. Download or create a small test file:

```bash
# Create a minimal valid MP3 (silent, tiny)
python3 -c "
import struct
# Simple silent MP3 frame
frame = bytes([0xFF, 0xFB, 0x90, 0x00]) + bytes(417)
with open('tests/e2e/fixtures/test.mp3', 'wb') as f:
    f.write(frame * 100)  # Repeat to make it playable
"
```

- [ ] **Step 3: Commit**

```bash
git add tests/e2e/fixtures/test.mp3
git commit -m "test: add test audio fixture"
```

---

### Task 3: Implement test_app_startup

**Files:**
- Modify: `tests/e2e/test_app_flow.py`

- [ ] **Step 1: Write the failing test**

```python
import pytest

@pytest.mark.asyncio
async def test_app_startup():
    """Test that app starts and all components are rendered"""
    from src.app import MusicTUI
    
    app = MusicTUI()
    async with app.run_test() as pilot:
        # Verify all main components exist
        assert app.query_one("#sidebar") is not None
        assert app.query_one("#track-list") is not None
        assert app.query_one("#player-bar") is not None
        assert app.query_one("#status-bar") is not None
```

- [ ] **Step 2: Run test to verify it runs**

```bash
pytest tests/e2e/test_app_flow.py::test_app_startup -v
```

- [ ] **Step 3: Commit**

```bash
git add tests/e2e/test_app_flow.py
git commit -m "test: add test_app_startup"
```

---

### Task 4: Implement test_navigate_tracks

**Files:**
- Modify: `tests/e2e/test_app_flow.py`

- [ ] **Step 1: Add test_navigate_tracks**

```python
@pytest.mark.asyncio
async def test_navigate_tracks():
    """Test navigating tracks with j/k keys"""
    from src.app import MusicTUI
    
    app = MusicTUI()
    async with app.run_test() as pilot:
        track_list = app.query_one("#track-list")
        initial_index = track_list.index
        
        # Press j to move down
        await pilot.press("j")
        await pilot.pause()
        
        assert track_list.index == initial_index + 1
        
        # Press k to move up
        await pilot.press("k")
        await pilot.pause()
        
        assert track_list.index == initial_index
```

- [ ] **Step 2: Run test**

```bash
pytest tests/e2e/test_app_flow.py::test_navigate_tracks -v
```

- [ ] **Step 3: Commit**

```bash
git add tests/e2e/test_app_flow.py
git commit -m "test: add test_navigate_tracks"
```

---

### Task 5: Implement test_play_track

**Files:**
- Modify: `tests/e2e/test_app_flow.py`

- [ ] **Step 1: Add test_play_track**

```python
@pytest.mark.asyncio
async def test_play_track():
    """Test pressing Enter plays the selected track"""
    from src.app import MusicTUI
    from src.models import PlayerState
    
    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Press Enter to play
        await pilot.press("enter")
        await pilot.pause()
        
        # Verify player state changed
        assert app.player.state == PlayerState.PLAYING
```

- [ ] **Step 2: Run test**

```bash
pytest tests/e2e/test_app_flow.py::test_play_track -v
```

- [ ] **Step 3: Commit**

```bash
git add tests/e2e/test_app_flow.py
git commit -m "test: add test_play_track"
```

---

### Task 6: Implement test_play_pause

**Files:**
- Modify: `tests/e2e/test_app_flow.py`

- [ ] **Step 1: Add test_play_pause**

```python
@pytest.mark.asyncio
async def test_play_pause():
    """Test space toggles play/pause"""
    from src.app import MusicTUI
    from src.models import PlayerState
    
    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Start playing
        await pilot.press("enter")
        await pilot.pause()
        assert app.player.state == PlayerState.PLAYING
        
        # Pause
        await pilot.press("space")
        await pilot.pause()
        assert app.player.state == PlayerState.PAUSED
        
        # Resume
        await pilot.press("space")
        await pilot.pause()
        assert app.player.state == PlayerState.PLAYING
```

- [ ] **Step 2: Run test**

```bash
pytest tests/e2e/test_app_flow.py::test_play_pause -v
```

- [ ] **Step 3: Commit**

```bash
git add tests/e2e/test_app_flow.py
git commit -m "test: add test_play_pause"
```

---

### Task 7: Implement test_next_previous_track

**Files:**
- Modify: `tests/e2e/test_app_flow.py`

- [ ] **Step 1: Add test_next_previous_track**

```python
@pytest.mark.asyncio
async def test_next_previous_track():
    """Test n/p keys for next/previous track"""
    from src.app import MusicTUI
    from src.models import PlayerState
    
    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Play first track
        await pilot.press("enter")
        await pilot.pause()
        
        initial_track = app.player.get_current_track()
        
        # Next track
        await pilot.press("n")
        await pilot.pause()
        
        next_track = app.player.get_current_track()
        assert next_track != initial_track
        
        # Previous track
        await pilot.press("p")
        await pilot.pause()
        
        prev_track = app.player.get_current_track()
        assert prev_track == initial_track
```

- [ ] **Step 2: Run test**

```bash
pytest tests/e2e/test_app_flow.py::test_next_previous_track -v
```

- [ ] **Step 3: Commit**

```bash
git add tests/e2e/test_app_flow.py
git commit -m "test: add test_next_previous_track"
```

---

### Task 8: Implement test_quit

**Files:**
- Modify: `tests/e2e/test_app_flow.py`

- [ ] **Step 1: Add test_quit**

```python
@pytest.mark.asyncio
async def test_quit():
    """Test q key exits the app"""
    from src.app import MusicTUI
    
    app = MusicTUI()
    async with app.run_test() as pilot:
        await pilot.pause()
        
        # Press q to quit
        await pilot.press("q")
        await pilot.pause()
        
        # App should have exited
        assert app._exit
```

- [ ] **Step 2: Run test**

```bash
pytest tests/e2e/test_app_flow.py::test_quit -v
```

- [ ] **Step 3: Commit**

```bash
git add tests/e2e/test_app_flow.py
git commit -m "test: add test_quit"
```

---

### Task 9: Update CI to run E2E tests

**Files:**
- Modify: `.github/workflows/python-app.yml`

- [ ] **Step 1: Update workflow to set SDL_AUDIODRIVER**

```yaml
    - name: Test with pytest
      run: |
        SDL_AUDIODRIVER=dummy pytest
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/python-app.yml
git commit -m "ci: add SDL_AUDIODRIVER for pygame tests"
```

- [ ] **Step 3: Push and verify CI**

```bash
git push
gh run list --limit 3
```

---

### Task 10: Final verification

**Files:**
- All created files

- [ ] **Step 1: Run all E2E tests**

```bash
SDL_AUDIODRIVER=dummy pytest tests/e2e/ -v
```

- [ ] **Step 2: Run full test suite**

```bash
SDL_AUDIODRIVER=dummy pytest -v
```

- [ ] **Step 3: Final commit with all changes**

```bash
git status
git log --oneline -10
```
