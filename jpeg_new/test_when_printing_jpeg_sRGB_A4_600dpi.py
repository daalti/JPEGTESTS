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
        +purpose:Simple print job of jpeg_sRGB_A4_600dpi
        +test_tier:1
        +is_manual:True
        +reqid:DUNE-18107
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:sRGB_A4_600dpi.jpg=86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_sRGB_A4_600dpi_file_then_succeeds
        +test:
            +title:test_jpeg_sRGB_A4_600dpi
            +guid:07072c6f-336c-488b-82bd-c1053f546e91
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_sRGB_A4_600dpi_file_then_succeeds(self):

        self.outputsaver.operation_mode('TIFF')

        default_tray = self.media.get_default_source()
        self.media.tray.load(default_tray, self.media.MediaSize.Custom, self.media.MediaType.Stationery)

        job_id = self.print.raw.start('86c81bfee5d3a323f7faf4026db8bf534e9d8edf624b9170bb60e3cf2d59773b')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')

        logging.info("Jpeg sRGB_A4_600dpi- Print job completed successfully")