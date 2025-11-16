# Contributing

Thank you for your interest in contributing to the PCI DSS PDF Control Tree Parser.

## Ground Rules

- Do not commit or include any actual cardholder data (CHD) or sensitive authentication data (SAD).
- Treat all parser outputs as **draft artifacts**; they require human review by a qualified assessor.
- Follow the security practices described in `docs/SECURITY_STANDARDS.md`.
- Use feature branches and pull requests for all changes.

## Development Workflow

1. Fork the repository and clone your fork.
2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Make changes in the `src/` directory.
4. Add or update tests in `tests/`.
5. Run tests.
6. Submit a pull request with a clear description.

## AI-Assisted Contributions

If you use AI tools to assist with code or documentation:
- Ensure the resulting code is fully understood, reviewed, and tested by you.
- Confirm that no proprietary or sensitive content was pasted into AI prompts.
