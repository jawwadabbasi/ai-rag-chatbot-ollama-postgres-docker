# Include all global variables in this file.
# These are used across different modules/packages
# where required.

# Service Name
SVC_NAME = 'batman-ms-chatbot'

# DB Settings
DB_HOST_WRITER = '127.0.0.1'
DB_HOST_READER = '127.0.0.1'
DB_PORT = 5432
DB_NAME = 'batman_chatbot'
DB_USER = 'postgres'
DB_PASS = 'postgres'

# Ollama Settings
OLLAMA_URL = 'http://127.0.0.1:11434'
EMBED_MODEL = 'nomic-embed-text'
GEN_MODEL = 'deepseek-r1'

# Sentry Settings
SENTRY_DSN = ''
SENTRY_TRACES_SAMPLE_RATE = 1.0
SENTRY_PROFILES_SAMPLE_RATE = 1.0
SENTRY_ENV = 'development'

# Flask Settings
FLASK_PORT = 80
FLASK_DEBUG = True