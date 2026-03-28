# E2E Test Design for MusicTUI

## Overview

Design and implement end-to-end tests for MusicTUI, a Textual-based TUI music player.

## Test Strategy

- **Framework**: Textual Pilot (built-in testing system)
- **Environment**: CI/headless with `SDL_AUDIODRIVER=dummy`
- **Test Data**: Real test audio files in fixtures directory

## Test Coverage

| Test Case | Description | Key Validations |
|-----------|-------------|-----------------|
| `test_app_startup` | App launches successfully | All UI components rendered |
| `test_navigate_tracks` | Navigate with j/k keys | Selection changes |
| `test_play_track` | Enter key plays selected track | Player state changes to PLAYING |
| `test_play_pause` | Space toggles play/pause | State toggles correctly |
| `test_next_track` | n key plays next track | Track changes |
| `test_previous_track` | p key plays previous track | Track changes |
| `test_quit` | q key exits app | App exits cleanly |

## Implementation Details

### Test Structure

```
tests/e2e/
├── __init__.py
├── conftest.py          # Shared fixtures
└── test_app_flow.py     # E2E test cases
```

### conftest.py Fixtures

- `test_audio_file`: Path to a valid test audio file
- `test_app`: MusicTUI app instance with pilot

### Key Technical Points

1. Use `pytest.mark.asyncio` for async test support
2. Use `app.run_test(pilot)` context manager
3. Use `await pilot.press()` for key simulation
4. Use `await pilot.pause()` to wait for async operations
5. Mock audio with `SDL_AUDIODRIVER=dummy` environment variable

## Success Criteria

- All E2E tests pass in CI environment
- Tests run in < 60 seconds
- Tests are isolated and can run in parallel
