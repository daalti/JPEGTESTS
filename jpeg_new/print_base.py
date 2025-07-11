import logging
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.print.print_new import Print
from dunetuf.media.media import Media


class TestWhenPrinting:
    """Base class providing common print test setup and helpers."""

    @classmethod
    def setup_class(cls):
        cls.job_queue = JobQueue()
        cls.job_history = JobHistory()
        cls.print = Print()
        cls.media = Media()

        # Ensure clean state before tests
        cls.job_queue.cancel_all_jobs()
        cls.job_queue.wait_for_queue_empty()
        cls.job_history.clear()
        cls.job_history.wait_for_history_empty()
        cls.default_configuration = cls.media.get_media_configuration()