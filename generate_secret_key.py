from pathlib import Path


def set_env(key: str, value: str, env_file: str = ".env"):
    path = Path(env_file)

    # Read existing lines if the file exists
    lines = path.read_text().splitlines() if path.exists() else []

    new_line = f"{key}={value}"
    key_found = False
    updated_lines = []

    for line in lines:
        # Preserve comments and blank lines
        if not line.strip() or line.lstrip().startswith("#"):
            updated_lines.append(line)
            continue

        # Check whether this line defines the key
        existing_key = line.split("=", 1)[0].strip()

        if existing_key == key:
            updated_lines.append(new_line)
            key_found = True
        else:
            updated_lines.append(line)

    # Add the variable if it didn't already exist
    if not key_found:
        updated_lines.append(new_line)

    path.write_text("\n".join(updated_lines) + "\n")


def generate_secret_key(length: int = 32) -> str:
    import secrets

    return secrets.token_hex(length)

set_env("SECRET_KEY", generate_secret_key())
