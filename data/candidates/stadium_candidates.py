"""
Stadium Project Candidates
High downloads, few maintainers, contributor dominance patterns.
"""

# Already collected - ready for analysis
COLLECTED = [
    "curl/curl",
    "zloirock/core-js",
    "psf/requests",
    "axios/axios",
    "chalk/chalk",
    "sindresorhus/got",
    "tj/commander.js",
    "benjaminp/six",
    "yaml/pyyaml",
    "serde-rs/serde",
    "madler/zlib",
    "glennrp/libpng",
]

# High priority - next to collect
HIGH_PRIORITY = [
    # JavaScript
    "uuidjs/uuid",
    "debug-js/debug",
    "npm/node-semver",
    "vercel/ms",
    "node-fetch/node-fetch",
    "yargs/yargs",

    # Python
    "urllib3/urllib3",
    "dateutil/dateutil",
    "certifi/python-certifi",
    "pallets/click",

    # Rust
    "rust-lang/regex",
    "serde-rs/json",
    "clap-rs/clap",

    # C/C++
    "sqlite/sqlite",
]

# Medium priority - verify maintainer count
MEDIUM_PRIORITY = [
    # JavaScript
    "babel/babel",
    "lodash/lodash",
    "expressjs/express",

    # Python
    "python-attrs/attrs",
    "pypa/pip",

    # Rust
    "tokio-rs/tokio",
    "rust-random/rand",

    # Go
    "spf13/cobra",
    "gorilla/mux",

    # Ruby
    "rack/rack",
    "sparklemotion/nokogiri",
]

# All candidates for batch processing
ALL_CANDIDATES = COLLECTED + HIGH_PRIORITY + MEDIUM_PRIORITY
