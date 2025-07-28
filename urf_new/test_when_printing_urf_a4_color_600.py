import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation


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
        +purpose:Simple print job of urf A4 Color 600 from *A4_Color_600.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A4_Color_600.urf=2dbe67f5a803639fd902f1a097d90b287de362650cd198829801c9f477337ff0
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_a4_color_600_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_a4_color_600_page
            +guid:55cdf59d-0593-4ef0-be98-f1a0167f3eb3
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
    def test_when_using_urf_a4_color_600_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        default = self.media.tray.get_default_source()
        if self.media.tray.is_size_supported('iso_a4_210x297mm', default):
            if self.get_platform() == 'emulator' and self.configuration.familyname == 'enterprise':
                tray1 = MediaInputIds.Tray1.name
                self.media.tray.open(tray1)
                self.media.tray.load(tray1, MediaSize.A4.name, MediaType.Plain.name)
                self.media.tray.close(tray1)
            else:
                self.media.tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

        job_id = self.print.raw.start('2dbe67f5a803639fd902f1a097d90b287de362650cd198829801c9f477337ff0')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        self.media.tray.reset_trays()

        logging.info("URF A4 Color 600 page - Print job completed successfully")
