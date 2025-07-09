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

    def _update_media_input_config(self, default_tray, media_size, media_type):
        """Update media configuration for a specific tray."""
        media_input = self.media.get_media_configuration().get("inputs", [])

        for input_config in media_input:
            if input_config.get("mediaSourceId") == default_tray:
                if media_size == "custom":
                    supported_inputs = self.media.get_media_capabilities().get(
                        "supportedInputs", []
                    )
                    capability = next(
                        (
                            cap
                            for cap in supported_inputs
                            if cap.get("mediaSourceId") == default_tray
                        ),
                        {},
                    )
                    input_config["currentMediaWidth"] = capability.get(
                        "mediaWidthMaximum"
                    )
                    input_config["currentMediaLength"] = capability.get(
                        "mediaLengthMaximum"
                    )
                    input_config["currentResolution"] = capability.get("resolution")

                input_config["mediaSize"] = media_size
                input_config["mediaType"] = media_type

                self.media.update_media_configuration({"inputs": [input_config]})
                return

        logging.warning(f"No media input found for tray: {default_tray}")

    def _get_tray_and_media_sizes(self, tray=None):
        """Get the default tray and its supported media sizes."""
        if tray is None:
            tray = self.media.get_default_source()
        supported_inputs = self.media.get_media_capabilities().get(
            "supportedInputs", []
        )
        media_sizes = next(
            (
                i.get("supportedMediaSizes", [])
                for i in supported_inputs
                if i.get("mediaSourceId") == tray
            ),
            [],
        )
        logging.info("Supported Media Sizes (%s): %s", tray, media_sizes)
        return tray, media_sizes
