# Contributing to HydrateMe

Thank you for choosing to contribute to HydrateMe! Here are the guidelines to help get your features and fixes merged quickly.

## Development Setup

1. Clone the repository and install development dependencies:
   ```bash
   pip install -e .[dev]
   ```

2. Code Formatting & Style:
   We enforce formatting using `black` and `isort`. You can format the code with:
   ```bash
   black src/ tests/
   isort src/ tests/
   ```

3. Code Linting & Static Typing:
   Verify code conventions and run type checking:
   ```bash
   flake8 src/ tests/
   mypy src/
   ```

4. Testing:
   Ensure all tests pass and coverage is above 80%:
   ```bash
   pytest --cov=src/hydrateme
   ```

## Pull Request Guidelines

- Follow SOLID coding practices and split layouts into modular packages.
- Add unit or integration tests for all new modules.
- Maintain XDG specifications for storage and user-safe IPC locks.
- Ensure all CI tests and lints pass.
