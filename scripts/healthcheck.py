from src.config.settings import settings

def main() -> None:
    print("Project:", settings.project_name)
    print("Environment:", settings.environment)
    print("Postgres host:", settings.postgres_host)
    print("Default symbols:", settings.default_symbols)
    print("Default interval:", settings.default_interval)

if __name__ == "__main__":
    main()
