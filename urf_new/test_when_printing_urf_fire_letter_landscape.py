import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.print.print_common_types import MediaSize, MediaType, MediaOrientation, TrayLevel


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
        +purpose:Simple print job of Urf Fire Letter Landscape from *Fire_Letter_Landscape.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:Fire_Letter_Landscape.urf=bb7a23ef6e64d35e1c87946fb314df3c3871319f855aa4c7e89e0cc5951e8d74
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_fire_letter_landscape_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_fire_letter_landscape_page
            +guid:05a3fcee-069a-4ed0-b35a-b69fc7329ba8
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
    def test_when_using_urf_fire_letter_landscape_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        default = self.media.tray.get_default_source()
        if self.get_platform() == 'emulator':
            self.media.tray.setup_tray(
                trayid="all",
                media_size=MediaSize.Letter.name,
                media_type=MediaType.Plain.name,
                orientation=MediaOrientation.Default.name,
                level=TrayLevel.Full.name
            )
        elif self.media.tray.is_size_supported('na_letter_8.5x11in', default):
            self.media.tray.configure_tray(default, 'na_letter_8.5x11in', 'stationery')
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('bb7a23ef6e64d35e1c87946fb314df3c3871319f855aa4c7e89e0cc5951e8d74')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        self.media.tray.reset_trays()
    
        logging.info("URF Fire Letter Landscape page - Print job completed successfully")
