import logging
import logging.config
import yaml

with open("config/logging.yaml") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)