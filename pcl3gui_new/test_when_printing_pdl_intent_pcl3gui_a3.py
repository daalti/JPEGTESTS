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
        +purpose:Simple print job of an A3 PCL3GUI file on tray
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-169798
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:a3.pcl=73673f25fd8f3526728f3cef33d394411e28372bd5706f41687a407d6cf341ad
        +name:TestWhenPrintingJPEGFile::test_when_using_pdl_intent_pcl3gui_a3_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pdl_intent_pcl3gui_a3_on_tray
            +guid:c9ab0b58-0d17-4bc3-af8f-b9c516617610
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL3GUI & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pdl_intent_pcl3gui_a3_file_then_succeeds(self):
        self.media.tray.unload_media()

        ipp_test_attribs = {
            'document-format': 'application/vnd.hp-PCL',
            'media-size-name': 'iso_a3_297x420mm',
            'media-source': 'main'
        }

        ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
        jobid = printjob.start_ipp_print(ipp_test_file, '73673f25fd8f3526728f3cef33d394411e28372bd5706f41687a407d6cf341ad')

        if self.media.tray.is_size_supported('iso_a3_297x420mm', 'main'):
            self.media.wait_for_alerts('mediaLoadFlow', 100)
            self.media.tray.configure_tray('main', 'iso_a3_297x420mm', 'stationery')
            self.media.tray.load_media('main')
            self.media.alert_action('mediaLoadFlow', 'ok')

        printjob.wait_verify_job_completion(jobid,"SUCCESS", timeout=180)

        outputverifier.save_and_parse_output()
        self.media.tray.reset_trays()
        self.media.tray.unload_media() #Will unload media from all trays
        self.media.tray.load_media() #Will load media in all trays to default

        outputverifier.verify_media_source(Intents.printintent, MediaSource.main)
        outputverifier.verify_media_size(Intents.printintent, MediaSize.a3)
