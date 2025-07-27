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
        +purpose:Simple print job of a4 glossy 12-page with print only odd pages PCL3GUI file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-150020
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:a4_oddpagesprint.prn=0744f4ca1abcc420491d7973ef4e071f407a4f1347ea6619aca400b887557250
        +name:TestWhenPrintingJPEGFile::test_when_using_pdl_intent_pcl3gui_a4_oddpagesprint_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pdl_intent_pcl3gui_a4_oddpagesprint
            +guid:d7de190b-9650-4aa0-a780-4f6647f18d35
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL3GUI & PrintProtocols=IPP & MediaSizeSupported=iso_a4_210x297mm & PrintColorMode=Color & Print=Normal & MediaInputInstalled=Main & PrintResolution=Print600 & BorderLessPrinting=True
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pdl_intent_pcl3gui_a4_oddpagesprint_file_then_succeeds(self):
        if self.media.tray.is_size_supported('iso_a4_210x297mm', 'tray-1'):
            self.media.tray.configure_tray('tray-1', 'iso_a4_210x297mm', 'com.hp-matte-presentation')
            self.outputsaver.validate_crc_tiff()
            job_id = self.print.raw.start('0744f4ca1abcc420491d7973ef4e071f407a4f1347ea6619aca400b887557250')
            self.print.wait_for_job_completion(job_id)

            outputverifier.save_and_parse_output()
            outputverifier.verify_page_count(Intents.printintent,6)
            outputverifier.verify_collated_copies(Intents.printintent, 1)
            outputverifier.verify_uncollated_copies(Intents.printintent, 1)
            outputverifier.verify_media_size(Intents.printintent, MediaSize.a4)
            outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
            outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
            outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
            outputverifier.verify_plex(Intents.printintent, Plex.simplex)
            outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
            outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
            outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
            outputverifier.verify_resolution(Intents.printintent, 600)
            self.outputsaver.save_output()
            self.outputsaver.operation_mode('NONE')
            self.media.tray.reset_trays()
