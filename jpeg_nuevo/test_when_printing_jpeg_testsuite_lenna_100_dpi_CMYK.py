import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver
from jpeg_nuevo.print_base import TestWhenPrinting


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.outputsaver = OutputSaver()

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
    
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite lenna 100 dpi CMYK Page from *lenna_100_dpi_CMYK.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:300
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:lenna_100_dpi_CMYK.jpg=d96f65dbf236961108f2c22f547afc056967c2e26ff5928631108966bdb779c3
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_lenna_100_dpi_CMYK_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_lenna_100_dpi_CMYK
        +guid:0ee7c12d-9c50-4c27-b2cd-3e12ca3ddffe
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_lenna_100_dpi_CMYK_jpg_then_succeeds(self):

        self.outputsaver.validate_crc_tiff()

        default_tray, media_sizes = self._get_tray_and_media_sizes()

        if 'anycustom' in media_sizes:
            self._update_media_input_config(default_tray, 'anycustom', 'stationery')
        else:
            self._update_media_input_config(default_tray, 'custom', 'stationery')

        job_id = self.print.raw.start('d96f65dbf236961108f2c22f547afc056967c2e26ff5928631108966bdb779c3')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        logging.info("JPEG TestSuite lenna 100 dpi CMYK Page - Print job completed successfully")