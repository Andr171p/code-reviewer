
# Размерность вектора
EMBEDDINGS_DIMENSION = 1024

# Github API URL
GITHUB_API_BASE_URL = "https://api.github.com"

TOP_N = 10
MAX_TELEGRAM_MESSAGE_LENGTH = 4096
DIALECT = 2
DISTANCE_THRESHOLD = 0.1
NUM_RESULTS = 1
LIMIT = 5
DEFAULT_USER_ID = "system"
MOSCOW_TZ = "Europe/Moscow"

TTL_CONFIG: dict[str, int | bool] = {
    "default_ttl": 60,  # Default TTL in minutes
    "refresh_on_read": True,  # Refresh TTL when checkpoint is read
}
