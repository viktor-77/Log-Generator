import random

from faker import Faker

LOG_EVENTS = ("INFO", "TRACE", "WARNING", "EVENT")
fake = Faker()


def _format_events(events: tuple[str, ...]) -> tuple[str, ...]:
    max_length = max(len(event) for event in events)
    return tuple(event.ljust(max_length) for event in events)


formatted_events = _format_events(LOG_EVENTS)


def generate_log(tab_size: int = 5) -> tuple[str, str]:
    log_date = fake.date()
    log_time = fake.time()
    log_event = random.choice(formatted_events)
    log_info = fake.text(fake.random_int(10, 100))

    tab_space = " " * tab_size
    log = tab_space.join((log_date, log_time, log_event, log_info)) + "\n"

    return log, log_event.lower()
