import logging
import logging.config
import yaml
from pathlib import Path


def setup_logging() -> None:
    """Set up logging configuration from a YAML file."""
    base_dir = Path(__file__).resolve().parent.parent
    log_config_path = base_dir/"config"/"logging.yaml"
    logs_dir = base_dir/"logs"
    
    #Create logs directory if it doenst exist make it
    logs_dir.mkdir(exist_ok=True)
    
    with open(log_config_path, 'r') as f:
        config = yaml.safe_load(f.read())
        # update log file path to absolute
        if 'file' in config.get('handlers', {}):
            config['handlers']['file']['filename']=str(logs_dir/'etl.log')
        logging.config.dictConfig(config)
        

