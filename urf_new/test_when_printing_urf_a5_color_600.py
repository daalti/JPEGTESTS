import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.print.print_common_types import MediaInputIds,MediaSize, MediaType, MediaOrientation, TrayLevel


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
        +purpose:Simple print job of urf A5 Color 600 from *A5_Color_600.urf file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-15734
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A5_Color_600.urf=66a70b02f29cfc9a5c4ec43e4527ac51d359e9c10cbb7d6ab68ed14c7417f6a4
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_a5_color_600_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_a5_color_600_page
            +guid:0b4a57e8-7475-439c-95c8-029b0330d70b
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF & MediaSizeSupported=iso_a5_148x210mm

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_a5_color_600_file_then_succeeds(self):
        default = self.media.tray.get_default_source()
        if self.get_platform() == 'emulator':
            self.media.tray.setup_tray(trayid="all", media_size=MediaSize.A5.name, media_type=MediaType.Plain.name,
                                        orientation=MediaOrientation.Default.name, level=TrayLevel.Full.name)

        elif self.media.tray.is_size_supported('iso_a5_148x210mm', default):
            self.media.tray.configure_tray(default, 'iso_a5_148x210mm', 'stationery')

        job_id = self.print.raw.start('66a70b02f29cfc9a5c4ec43e4527ac51d359e9c10cbb7d6ab68ed14c7417f6a4')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        self.media.tray.reset_trays()

        logging.info("URF A5 Color 600 page - Print job completed successfully")
