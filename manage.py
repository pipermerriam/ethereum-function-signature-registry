#!/usr/bin/env python
import os
import sys
import dotenv

dotenv.load_dotenv('.env')  # Local overrides (not tracked)
dotenv.load_dotenv('.env_defaults')  # Development defaults (tracked)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "func_sig_registry.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
