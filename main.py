from core.app import setup_scheduler

if __name__ == "__main__":
    scheduler = setup_scheduler()
    scheduler.run(minutes=5)
