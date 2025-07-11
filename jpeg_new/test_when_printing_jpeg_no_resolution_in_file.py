import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_verifier import OutputVerifier
from dunetuf.print.output_saver import OutputSaver
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding
from tests.print.pdl.jpeg_new.print_base import TestWhenPrinting


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        cls.outputverifier = OutputVerifier(cls.outputsaver)

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
        +purpose:Test jpeg job when no resolution in specified in file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-215024
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:road_nores.jpeg=116ef2798a4d195fd1e3ea20d81af3b8c20373587e119d10a6ff0f0d70ee6f86
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_road_nores_jpeg_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_no_resolution_in_file
            +guid:8511f918-a79f-49e1-a5ac-d083a5e11287
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & EngineFirmwareFamily=DoX & PrintResolution=Print300

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_road_nores_jpeg_then_succeeds(self):

        default_tray, media_sizes = self.media.get_source_and_media_sizes()
        if 'custom' in media_sizes:
            self.media.tray.configure(default_tray, 'custom', 'stationery')

        self.outputsaver.validate_crc_tiff()

        job_id = self.print.raw.start('116ef2798a4d195fd1e3ea20d81af3b8c20373587e119d10a6ff0f0d70ee6f86')
        self.print.wait_for_job_completion(job_id)
        self.outputverifier.save_and_parse_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        self.outputverifier.verify_resolution(Intents.printintent, 600)
        self.outputverifier.verify_page_width(Intents.printintent, 3000)
        self.outputverifier.verify_page_height(Intents.printintent, 3749)
        self.outputsaver.operation_mode('NONE')
