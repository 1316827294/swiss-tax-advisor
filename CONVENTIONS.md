# Aider Conventions — Swiss Tax Advisor

## Architecture & Code Standards
- **Standard Library Only**: No external pip packages allowed in core tax scripts. Keep execution lightweight and zero-dependency.
- **Deterministic Math**: Rounding adheres to Swiss 5-Rappen law (`round(v * 20) / 20`).
- **User Privacy**: All user profile operations go through `scripts/user_profile.py` into local `user/` files, which are strictly gitignored.
- **Silent Tool Use**: When assisting a user in chat, execute CLI scripts silently and present formatted markdown tables.
- **Unit Testing**: Run `python3 -m unittest discover -s scripts -p "test_*.py"` before committing any changes.
