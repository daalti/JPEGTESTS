import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
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
        +purpose:Simple print job of Urf Legal Color from *Legal_Color.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Legal_Color.urf=1d5c80f76d86ac4c24e35788d9c93a744e1269aa0c0a1d354fd90c72c7c79a6d
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_legal_color_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_legal_color_page
            +guid:881c7195-d248-4bc4-a9bf-bbc0416c7af6
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_legal_color_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        media_width_maximum = self.media.tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
        media_length_maximum = self.media.tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
        media_width_minimum = self.media.tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
        media_length_minimum = self.media.tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
        if self.media.tray.is_size_supported('na_legal_8.5x14in', default):
            self.media.tray.configure_tray(default, 'na_legal_8.5x14in', 'stationery')
        elif self.media.tray.is_size_supported('custom', default) and media_width_maximum >= 85000 and media_length_maximum >= 140000 and  media_width_minimum <= 85000 and media_length_minimum <= 140000:
            self.media.tray.configure_tray(default, 'custom', 'stationery')       
    
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('1d5c80f76d86ac4c24e35788d9c93a744e1269aa0c0a1d354fd90c72c7c79a6d')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()
    
        logging.info("URF Legal Color Page - Print job completed successfully")
