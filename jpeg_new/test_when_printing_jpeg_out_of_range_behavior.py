import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from dunetuf.print.new.output.output_verifier import OutputVerifier
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding
from dunetuf.media.media_handling import MediaHandling
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver

class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)
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
        tear_down_output_saver(self.outputsaver)

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Test jpeg out of range behavior on roll
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-155289
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A0-600-L.jpg=b9d02741fadecd94d682bb8b40ec433f5ab27ef63418cdcea21085d7b4e89d90
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_A0_600_L_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_out_of_range_behavior_on_roll
            +guid:3225b518-6407-477f-96ba-92e5c767098f
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_A0_600_L_file_then_succeeds(self):

        self.media.unload_media()

        #Input document is landscape A0 size. It will be printed on roll by rotating it to portrait.
        ipp_test_attribs = {
            'document-format': 'image/jpeg',
            'media-size-name': 'iso_a0_841x1189mm',
            'media-source': 'main-roll'
        }
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)
        job_result = self.print.ipp.start(ipp_test_file, 'b9d02741fadecd94d682bb8b40ec433f5ab27ef63418cdcea21085d7b4e89d90')
        job_id = job_result[0] if isinstance(job_result, tuple) else job_result

        media_sizes = self.media.get_media_sizes('main-roll')
        if "iso_a0_841x1189mm" in media_sizes:
            self.media_handling.wait_for_alerts('mediaLoadFlow', 100)
            self.media.tray.load('main-roll', self.media.MediaSize.iso_a0_841x1189mm, self.media.MediaType.Stationery)
            self.media.load_media('main-roll')
            self.media_handling.alert_action('mediaLoadFlow', 'ok')

        self.print.wait_for_job_completion(job_id)

        self.outputverifier.save_and_parse_output()
        self.media.unload_media()  # Will unload media from all trays
        self.media.load_media()  # Will load media in all trays to default

        self.outputverifier.verify_media_source(Intents.printintent, MediaSource.mainroll)  #type: ignore
        self.outputverifier.verify_media_size(Intents.printintent, MediaSize.a0) #type: ignore

        # CRC check
        self.outputsaver.operation_mode('TIFF')
        self.outputsaver.validate_crc_tiff()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        self.outputsaver.operation_mode('NONE')
