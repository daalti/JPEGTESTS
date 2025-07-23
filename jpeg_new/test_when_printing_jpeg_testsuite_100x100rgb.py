import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from tests.print.pdl.print_base import setup_output_saver, tear_down_output_saver


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
        +purpose:Simple print job of Jpeg TestSuite 100x100 rgb Page from *100x100rgb.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:200
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:100x100rgb.jpg=d5ac022cb1f519bf43576315cd62acb7dd7ba4de26bcd229fc544023a5da12ab
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_100x100rgb_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testsuite_100x100rgb
            +guid:d9cceda9-54fd-462f-8724-405cea069431
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_100x100rgb_file_then_succeeds(self):

        self.outputsaver.operation_mode('TIFF')

        default_tray = self.media.get_default_source()
        media_sizes = self.media.get_media_sizes(default_tray)
        default_size = self.media.get_default_size(default_tray)

        if default_size in media_sizes:
            logging.info(f"Set paper tray <{default_tray}> to paper size <{default_size}>")
            self.media.tray.load(default_tray, default_size, self.media.MediaType.Stationery)

        job_id = self.print.raw.start('d5ac022cb1f519bf43576315cd62acb7dd7ba4de26bcd229fc544023a5da12ab')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')

        logging.info("JPEG TestSuite 100x100 rgb Page - Print job completed successfully")