import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""

    def teardown_method(self):
        """Clean up resources after each test."""
        # Clear job queue
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        self.job_history.clear()
        self.job_history.wait_for_history_empty()

        # Reset media configuration to default
        self.media.update_media_configuration(self.default_configuration)
        tear_down_output_saver(self.outputsaver)

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Simple print job of Jpeg file of 100kB from *file_example_JPG_100kB.jpg
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:360
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:file_example_JPG_100kB.jpg=88aeb1f4467bd1e50cf624de972fbf3f40801632fedb64aaa7b1a8a9ef786fc6
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_file_example_JPG_100kB_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_file_example_JPG_100kB
            +guid:3a24f23b-1250-4bc9-b1c8-524ded9ff218
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_file_example_JPG_100kB_file_then_succeeds(self):

        self.outputsaver.validate_crc_tiff()

        is_loaded = self.load_custom_tray(
            width_max=85000,
            length_max=110000,
            width_min=85000,
            length_min=110000
        )
        default_tray = self.media.get_default_source()
        media_sizes = self.media.get_media_sizes(default_tray)

        if not is_loaded and self.media.MediaSize.Letter in media_sizes:
            self.media.tray.load(default_tray, self.media.MediaSize.Letter, self.media.MediaType.Stationery)

        job_id = self.print.raw.start('88aeb1f4467bd1e50cf624de972fbf3f40801632fedb64aaa7b1a8a9ef786fc6')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        logging.info("Jpeg file example JPG 100kB Page - Print job completed successfully")