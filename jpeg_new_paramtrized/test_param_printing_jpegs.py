import logging
import pytest
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver
from tests.print.pdl.jpeg_new.print_base import TestWhenPrinting


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""

    def teardown_method(self):
        """Clean up resources after each test."""
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()
        self.job_history.clear()
        self.job_history.wait_for_history_empty()
        self.media.update_media_configuration(self.default_configuration)

    @pytest.mark.parametrize(
        "job_hash, log_message",
        [
            (
                "18f25bed0d24c7ed1203c867676b1d33903edcf6643c77989a31a85721f88357",
                None,
            ),
            (
                "838e346997ab5f2dd6745e9e536de6f9cd68965088354597f2fba016ad40ab2c",
                "Jpeg file example JPG 500kB Page - Print job completed successfully",
            ),
            (
                "d625c95d10545cc5aa1e4ce2f276a7d423c1aa96a683a581a4bc243ee93393a2",
                "JPEG Performance faces Page - Print job completed successfully",
            ),
            (
                "07010aa839653b2355047c770f6f3631997e0e9172537141d42d185c34f39a1d",
                "JPEG Regression 3Dgirls JFIF nounits without EXIF Page - Print job completed successfully",
            ),
            (
                "07010aa839653b2355047c770f6f3631997e0e9172537141d42d185c34f39a1d",
                "JPEG TestSuite 3Dgirls JFIF nounits without EXIF Page - Print job completed successfully",
            ),
            (
                "3c685134a542d477374788bb6a3f1027cd8f433d49a0255b2ac7f5246bd7010c",
                "JPEG TestSuite DemoImages Page - Print job completed successfully",
            ),
            (
                "be12e5937c270ec1d6690cc50cd3e42b1123f0d0fe04a6540e8c3ef19374c305",
                "JPEG TestSuite lenna 20dpcm Page - Print job completed successfully",
            ),
            (
                "a89ef72d5101dabbf55a0722d57141626372518bfd7fa6b3ba53808ba7d1e0f5",
                None,
            ),
        ],
    )
    def test_when_various_jpegs_then_succeeds(self, job_hash, log_message):
        job_id = self.print.raw.start(job_hash)
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        if log_message:
            logging.info(log_message)

