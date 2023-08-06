from robocorp.tasks import task
from loguru import logger

from src.automation_nyt import AutomationNYT
from src.variables import get_variables


@task
def task():
    logger.info("Start process...")

    automation = AutomationNYT(get_variables())
    automation.run()

    logger.info("Task done.")


if __name__ == "__main__":
    task()
