import yaml

with open("config/settings.yaml") as f:
    settings = yaml.safe_load(f)
    