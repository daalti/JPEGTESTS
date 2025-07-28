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
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Simple print job of urf 10x12 custom job on roll
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-128384
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:10x12_URF.urf=68ad2334e87b103fda5d9502f4a5d34417cc349b8ef0fb182b56385441faa639
        +name:TestWhenPrintingJPEGFile::test_when_using_urf_custom_job_10x12_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:URF
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_urf_custom_job_10x12_on_roll
            +guid:c914f349-2eda-4176-921c-a7c26d829258
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=URF & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_urf_custom_job_10x12_file_then_succeeds(self):
        self.media.tray.unload_media()

        ipp_test_attribs = {
            'document-format': 'image/urf',
            'media-source': 'auto',
            'x-dimension': '25400',
            'y-dimension': '30480',
            'media-bottom-margin': 499,
            'media-left-margin': 499,
            'media-right-margin': 499,
            'media-top-margin': 499,
        }

        ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
        jobid = printjob.start_ipp_print(ipp_test_file, '68ad2334e87b103fda5d9502f4a5d34417cc349b8ef0fb182b56385441faa639')

        if self.media.tray.is_size_supported('iso_a0_841x1189mm', 'main-roll'):
            self.media.wait_for_alerts('allSourcesEmptyPrompt', 100)
            self.media.tray.configure_tray('main-roll', 'iso_a0_841x1189mm', 'stationery')
            self.media.tray.load_media('main-roll')
            self.media.alert_action('allSourcesEmptyPrompt', 'ok')

        printjob.wait_verify_job_completion(jobid,"SUCCESS", timeout=300)

        outputverifier.save_and_parse_output()
        self.media.tray.reset_trays()
        self.media.tray.unload_media() #Will unload media from all trays
        self.media.tray.load_media() #Will load media in all trays to default

        outputverifier.verify_media_source(Intents.printintent, MediaSource.mainroll)
        outputverifier.verify_media_size(Intents.printintent, MediaSize.a0)

        # CRC check
        self.outputsaver.operation_mode('TIFF')
        self.outputsaver.validate_crc_tiff()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
        self.outputsaver.operation_mode('NONE')
