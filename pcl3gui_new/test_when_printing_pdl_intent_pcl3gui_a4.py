import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.print.output.intents import Intents, MediaSize, ColorMode, PrintQuality, ColorRenderingType, ContentOrientation, Plex, MediaType, MediaSource, PlexBinding


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
    $$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Simple print job of an A4 PCL3GUI file on tray
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-161185
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:a4.pcl=6cf62f61dde512a2845b18ba53d96f8ade4fdb917d32080fac0285eb00ff5d8f
        +name:TestWhenPrintingJPEGFile::test_when_using_pdl_intent_pcl3gui_a4_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pdl_intent_pcl3gui_a4_on_tray
            +guid:c70eb095-ab26-49c3-8bc4-496fdc82dde5
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL3GUI & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pdl_intent_pcl3gui_a4_file_then_succeeds(self):
        self.media.tray.unload_media()

        ipp_test_attribs = {
            'document-format': 'application/vnd.hp-PCL',
            'media-size-name': 'iso_a4_210x297mm',
            'media-source': 'main'
        }

        ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
        jobid = printjob.start_ipp_print(ipp_test_file, '6cf62f61dde512a2845b18ba53d96f8ade4fdb917d32080fac0285eb00ff5d8f')

        if self.media.tray.is_size_supported('iso_a4_210x297mm', 'main'):
            self.media.wait_for_alerts('mediaLoadFlow', 100)
            self.media.tray.configure_tray('main', 'iso_a4_210x297mm', 'stationery')
            self.media.tray.load_media('main')
            self.media.alert_action('mediaLoadFlow', 'ok')

        printjob.wait_verify_job_completion(jobid,"SUCCESS", timeout=180)

        outputverifier.save_and_parse_output()
        self.media.tray.reset_trays()
        self.media.tray.unload_media() #Will unload media from all trays
        self.media.tray.load_media() #Will load media in all trays to default

        outputverifier.verify_media_source(Intents.printintent, MediaSource.main)
        outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
        
        # CRC check
        self.outputsaver.operation_mode('TIFF')
        self.outputsaver.validate_crc_tiff()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        self.outputsaver.operation_mode('NONE')
