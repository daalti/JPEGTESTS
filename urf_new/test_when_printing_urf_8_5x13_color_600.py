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
        +purpose:Simple print job of urf 8_5x13 color 600 page from *8_5x13_Color_600.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:8_5x13_Color_600.urf=8d1b6933fe1f14a687571c4995c49236b5054fb5c6fbe8742d475583763955de
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_8_5x13_color_600_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_8_5x13_color_600_page
            +guid:6fa9ebbc-6b2b-43fd-97d9-fa2a669a020e
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_8_5x13_color_600_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        default = self.media.tray.get_default_source()
        media_width_maximum = tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
        media_length_maximum = tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
        media_width_minimum = tray.capabilities["supportedInputs"][0]["mediaWidthMinimum"]
        media_length_minimum = tray.capabilities["supportedInputs"][0]["mediaLengthMinimum"]
        if self.media.tray.is_size_supported('na_foolscap_8.5x13in', default):
            self.media.tray.configure_tray(default, 'na_foolscap_8.5x13in', 'stationery')
        elif self.media.tray.is_size_supported('custom', default) and media_width_maximum >= 85000 and media_length_maximum >= 130000 and  media_width_minimum <= 85000 and media_length_minimum <= 130000:
            self.media.tray.configure_tray(default, 'custom', 'stationery')


        job_id = self.print.raw.start('8d1b6933fe1f14a687571c4995c49236b5054fb5c6fbe8742d475583763955de')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()

        logging.info("URF 8_5x13 Color 600 page - Print job completed successfully")
