import logging
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
        +purpose:simple print job of jpeg file of photoimages differentfilesize 3m dsc00696
        +test_tier:1
        +is_manual:False
        +reqid:DUNEPA-126
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:photoimages_differentfilesize_3M_DSC00696.JPG=9ba3d34b6493769d9d1b40252c3ed9e360de6f4e3e0c93029f616516698637c4
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_photoimages_differentfilesize_3M_DSC00696_JPG_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_photoimages_differentfilesize_3m_dsc00696
            +guid:15b9c8c3-80a1-4281-894f-ad6e78aea13d
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_photoimages_differentfilesize_3M_DSC00696_JPG_then_succeeds(self):

        capabilities = self.media.get_media_capabilities()   
        media_width_maximum = capabilities["supportedInputs"][0]["mediaWidthMaximum"]
        media_length_maximum = capabilities["supportedInputs"][0]["mediaLengthMaximum"]
        media_width_minimum = capabilities["supportedInputs"][0]["mediaWidthMinimum"]
        media_length_minimum = capabilities["supportedInputs"][0]["mediaLengthMinimum"]
        default_tray, media_sizes = self.media.get_source_and_media_sizes()
        if 'anycustom' in media_sizes:
            self.media.tray.configure(default_tray, 'anycustom', 'stationery')
        elif 'custom' in media_sizes and media_width_maximum >= 453333 and media_length_maximum >= 340000 and  media_width_minimum <= 453333 and media_length_minimum <= 340000:
            self.media.tray.configure(default_tray, 'custom', 'stationery')


        job_id = self.print.raw.start('9ba3d34b6493769d9d1b40252c3ed9e360de6f4e3e0c93029f616516698637c4')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("Jpeg file example photoimages differentfilesize 3M DSC00696 - Print job completed successfully")