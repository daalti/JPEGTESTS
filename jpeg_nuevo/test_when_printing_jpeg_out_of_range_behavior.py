import pytest
import logging
from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.media.media import Media
from dunetuf.print.output_saver import OutputSaver
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding


class TestWhenPrintingJPEGFile:
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.job_queue = JobQueue()
        cls.job_history = JobHistory()
        cls.print = Print()
        cls.media = Media()
        cls.outputsaver = OutputSaver()

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""

    def setup_method(self):
        """Clean up resources after each test."""
        # Clear job queue
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        self.job_history.clear()
        self.job_history.wait_for_history_empty()

        # Get media configuration
        self.default_configuration = self.media.get_media_configuration()

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
    +name:TestWhenPrintingJPEGFile::test_when_A0_600_L_jpg_then_succeeds
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
    def test_when_A0_600_L_jpg_then_succeeds(self):

        tray.unload_media()

        #Input document is landscape A0 size. It will be printed on roll by rotating it to portrait.
        ipp_test_attribs = {
            'document-format': 'image/jpeg',
            'media-size-name': 'iso_a0_841x1189mm',
            'media-source': 'main-roll'
        }

        ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
        jobid = printjob.start_ipp_print(ipp_test_file, 'b9d02741fadecd94d682bb8b40ec433f5ab27ef63418cdcea21085d7b4e89d90')

        if tray.is_size_supported('iso_a0_841x1189mm', 'main-roll'):
            media.wait_for_alerts('mediaLoadFlow', 100)
            tray.configure_tray('main-roll', 'iso_a0_841x1189mm', 'stationery')
            tray.load_media('main-roll')
            media.alert_action('mediaLoadFlow', 'ok')

        printjob.wait_verify_job_completion(jobid, "SUCCESS", timeout=300)

        outputverifier.save_and_parse_output()
        tray.unload_media()  # Will unload media from all trays
        tray.load_media()  # Will load media in all trays to default

        outputverifier.verify_media_source(Intents.printintent, MediaSource.mainroll)
        outputverifier.verify_media_size(Intents.printintent, MediaSize.a0)

        # CRC check
        self.outputsaver.operation_mode('TIFF')
        self.outputsaver.validate_crc_tiff(udw)
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        self.outputsaver.operation_mode('NONE')

