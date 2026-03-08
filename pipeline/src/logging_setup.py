from pathlib import Path
import logging
import logging.config
import yaml

def setup_logging() -> None:
    """Setup logging configuration from a YAML file."""
    base_dir = Path(__file__).resolve().parent.parent
    log_config_path = base_dir / "config" / "logging.yaml"
    logs_dir = base_dir / "logs"
    
    # Create logs directory if it doesn't exist
    logs_dir.mkdir(exist_ok=True)
    
    with open(log_config_path, 'r') as f:
        cfg = yaml.safe_load(f.read())
        # Update log file path to be absolute
        if 'file' in cfg.get('handlers', {}):
            cfg['handlers']['file']['filename'] = str(logs_dir / 'etl.json')
        logging.config.dictConfig(cfg)