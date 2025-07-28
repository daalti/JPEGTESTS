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
        +purpose:Simple print job of Urf iso sra4 225x320 from *iso_sra4_225x320.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:iso_sra4_225x320.urf=decebc46d96c90fdc2190bc5e39b6df2482a78f770fc30876d9d9319aa2f020c
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_iso_sra4_225x320_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_iso_sra4_225x320_page
            +guid:5090c155-e145-4104-bc36-b80bbb215a4c
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
    def test_when_using_urf_iso_sra4_225x320_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        media_width_maximum = self.media.tray.capabilities["supportedInputs"][0]["mediaWidthMaximum"]
        media_length_maximum = self.media.tray.capabilities["supportedInputs"][0]["mediaLengthMaximum"]
    
        if self.media.tray.is_size_supported('iso_sra4_225x320mm', default):
            self.media.tray.configure_tray(default, 'iso_sra4_225x320mm', 'stationery')
        elif self.media.tray.is_size_supported('custom', default) and media_width_maximum >= 88567 and media_length_maximum >= 125984:
            self.media.tray.configure_tray(default, 'custom', 'stationery')
    
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('decebc46d96c90fdc2190bc5e39b6df2482a78f770fc30876d9d9319aa2f020c')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()
    
        logging.info("URF iso sra4 225x320 Page - Print job completed successfully")
