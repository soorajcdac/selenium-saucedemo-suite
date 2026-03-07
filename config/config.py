import os

class Config:
    # Target app — saucedemo.com
    BASE_URL      = "https://www.saucedemo.com"
    BROWSER       = "chrome"
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    HEADLESS      = False   # Set True later for CI/CD

    # Saucedemo test credentials (these are public)
    VALID_USER   = "standard_user"
    LOCKED_USER  = "locked_out_user"
    PROBLEM_USER = "problem_user"
    PASSWORD     = "secret_sauce"