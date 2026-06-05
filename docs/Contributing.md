# Contributing

1. Fork → branch `feat/<name>`.
2. Backend changes: keep `core/gestures.py` pure (no cv2 import) so tests stay
   camera-free. Add a test in `tests/`.
3. New filter: add a pure `np.ndarray→np.ndarray` fn in `filters/filters.py`
   and register it in `FILTERS`. It auto-appears in the cycle + `/api/filters`.
4. Run `pytest -q` and `npm run build` before opening a PR.
5. Conventional commits (`feat:`, `fix:`, `docs:`). Write commit messages in
   plain prose.

## Dev setup
`pip install -r backend/requirements-dev.txt`
