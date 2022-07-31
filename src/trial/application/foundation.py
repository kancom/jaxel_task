from pydantic import constr

Pair = constr(regex=r"[A-Z0-9]{3,7}")
