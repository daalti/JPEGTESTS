import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.output_saver import OutputSaver
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding
from dunetuf.media.media_handling import MediaHandling
from dunetuf.print.output_verifier import OutputVerifier
from tests.print.pdl.jpeg_new.print_base import TestWhenPrinting

class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        cls.outputverifier = OutputVerifier(cls.outputsaver)
        cls.media_handling = MediaHandling()

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
        +purpose:Test jpeg small job on large paper tray
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-153638
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:abbey-4x6-L.jpg=1fcc44e51d4702a75c0487be852ae62fca82a2cab4bf0d19645b83e3264eb1d0
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_abbey_4x6_L_jpg_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_smalljob_on_largepaper_on_tray
            +guid:e474d378-55a7-4ba0-9ed2-47966b39aaae
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_abbey_4x6_L_jpg_then_succeeds(self):

        self.media.unload_media()

        tray, media_sizes = self.media.get_source_and_media_sizes('main')
        if 'iso_a4_210x297mm' in media_sizes:
            self.media.tray.configure('main', 'iso_a4_210x297mm', 'stationery')
            self.media.load_media('main')

        ipp_test_attribs = {
            'document-format': 'image/jpeg',
            'media-source': 'main'
        }

        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)
        job_id = self.print.ipp.start(ipp_test_file, '1fcc44e51d4702a75c0487be852ae62fca82a2cab4bf0d19645b83e3264eb1d0')

        self.print.wait_for_state(job_id, ["completed"])

        self.outputverifier.save_and_parse_output()
        self.media.unload_media()  # Will unload media from all trays
        self.media.load_media()  # Will load media in all trays to default

        self.outputverifier.verify_media_source(Intents.printintent, MediaSource.main)
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)  # coming as a4 due to jpeg scaling

        # CRC check
        self.outputsaver.operation_mode('TIFF')
        self.outputsaver.validate_crc_tiff()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        self.outputsaver.operation_mode('NONE')
