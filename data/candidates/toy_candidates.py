"""
Toy Project Candidates
Personal projects, single-maintainer utilities, hobby projects.
Typically single author, low governance complexity, high downloads.
"""

# Candidates to collect
CANDIDATES = [
    # ==========================================================================
    # JavaScript/Node.js - Single maintainer micro-utilities
    # ==========================================================================
    "lukeed/kleur",                 # Terminal string styling, single author
    "juliangruber/isarray",         # Array check polyfill, billions of downloads
    "jonschlinkert/is-number",      # Check if value is number
    "feross/safe-buffer",           # Buffer polyfill, single author
    "mafintosh/pump",               # Pipe streams properly
    "minimistjs/minimist",          # Argument parser (was substack/minimist)
    "isaacs/once",                  # Run function once
    "isaacs/inherits",              # Inheritance utility

    # ==========================================================================
    # Python - Personal utilities
    # ==========================================================================
    "tartley/colorama",             # Terminal colors, single maintainer
    "docopt/docopt",                # CLI argument parser, single vision
    "keleshev/schema",              # Data validation, personal project

    # ==========================================================================
    # Rust - dtolnay & BurntSushi personal projects
    # ==========================================================================
    "dtolnay/anyhow",               # Error handling, single author
    "dtolnay/thiserror",            # Error derive macro
    "BurntSushi/ripgrep",           # Fast grep, single author
    "BurntSushi/xsv",               # CSV toolkit, single author

    # ==========================================================================
    # Go - Personal utilities
    # ==========================================================================
    "fatih/color",                  # Terminal colors, single maintainer
    "sirupsen/logrus",              # Logging, personal project origin
    "mitchellh/mapstructure",       # Map decoder, personal project

    # ==========================================================================
    # Already collected
    # ==========================================================================
    "ibrahimcesar/react-lite-youtube-embed",  # Personal project
]

# High priority for collection (not yet collected)
HIGH_PRIORITY = [
    # JavaScript
    "lukeed/kleur",
    "juliangruber/isarray",
    "jonschlinkert/is-number",
    "feross/safe-buffer",
    "mafintosh/pump",
    "minimistjs/minimist",
    "isaacs/once",
    "isaacs/inherits",

    # Python
    "tartley/colorama",
    "docopt/docopt",
    "keleshev/schema",

    # Rust
    "dtolnay/anyhow",
    "dtolnay/thiserror",
    "BurntSushi/ripgrep",
    "BurntSushi/xsv",

    # Go
    "fatih/color",
    "sirupsen/logrus",
    "mitchellh/mapstructure",
]

# Already collected
COLLECTED = [
    "ibrahimcesar/react-lite-youtube-embed",
]

# Note: Toy projects are characterized by:
# - Single maintainer (usually the author)
# - Personal use case or utility
# - High downloads but minimal governance structure
# - Often created for fun, learning, or solving personal needs
# - Low bus factor (typically 1)
# - Minimal or no GOVERNANCE.md, MAINTAINERS.md files
