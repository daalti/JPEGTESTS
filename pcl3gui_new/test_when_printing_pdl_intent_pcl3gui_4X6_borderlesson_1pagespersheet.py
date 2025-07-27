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
        +purpose:Simple print job of a 4X6 glossy 4-page simplex borderlesson 1page per sheet  PCL3GUI file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-150020
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:4X6_borderlesson_1pagespersheet.prn=a85d10c75c0e389d69940b5e550e202804fde6d9f997a041b35cbd5cb0e7ad49
        +name:TestWhenPrintingJPEGFile::test_when_using_pdl_intent_pcl3gui_4X6_borderlesson_1pagespersheet_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pdl_intent_pcl3gui_4X6_borderlesson_1pagespersheet
            +guid:da489037-cb18-457d-b24a-819810a2a13c
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL3GUI & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in & PrintColorMode=GrayScale & Print=Normal & MediaType=HPTri-foldBrochurepaper-Glossy & PrintResolution=Print1200
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pdl_intent_pcl3gui_4X6_borderlesson_1pagespersheet_file_then_succeeds(self):
        if self.media.tray.is_size_supported('na_index-4x6_4x6in', 'tray-1'):
            self.media.tray.configure_tray('tray-1', 'na_index-4x6_4x6in', 'com.hp-trifold-brochure-glossy-180gsm')

        self.outputsaver.validate_crc_tiff()

        job_id = self.print.raw.start('a85d10c75c0e389d69940b5e550e202804fde6d9f997a041b35cbd5cb0e7ad49')

        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_page_count(Intents.printintent, 4)
        outputverifier.verify_collated_copies(Intents.printintent, 1)
        outputverifier.verify_uncollated_copies(Intents.printintent, 1)
        outputverifier.verify_media_size(Intents.printintent, MediaSize.photo4x6)
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.grayscale)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
        outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
        outputverifier.verify_media_type(Intents.printintent, MediaType.trifold_brochure_glossy)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
        outputverifier.verify_resolution(Intents.printintent, 1200)
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        self.media.tray.reset_trays()
