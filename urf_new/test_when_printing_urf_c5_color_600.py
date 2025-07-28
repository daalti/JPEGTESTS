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
        +purpose:Simple print job of urf C5 Color 600 from *C5_Color_600.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:C5_Color_600.urf=c5ec056aa515083a82c5e21da869032b191629ce036bd2a6e38b4faecf369bef
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_c5_color_600_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_c5_color_600_page
            +guid:5d0d842b-5eb2-4dc2-b382-8a8369eb6f43
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF & MediaSizeSupported=iso_c5_162x229mm

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_c5_color_600_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
        media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
        media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
        media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
        if self.media.tray.is_size_supported('iso_c5_162x229mm', default):
            self.media.tray.configure_tray(default, 'iso_c5_162x229mm', 'stationery')
        elif self.media.tray.is_size_supported('custom', default) and media_width_maximum >= 63766 and media_length_maximum >= 90133 and  media_width_minimum <= 63766 and media_length_minimum <= 90133:
            self.media.tray.configure_tray(default, 'custom', 'stationery')    

        job_id = self.print.raw.start('c5ec056aa515083a82c5e21da869032b191629ce036bd2a6e38b4faecf369bef')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()

        logging.info("URF C5 Color 600 page - Print job completed successfully")
