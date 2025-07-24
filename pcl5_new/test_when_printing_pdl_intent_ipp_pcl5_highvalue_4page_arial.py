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
        +purpose: IPP test for printing pcl5 highvalue using 4Page-arial.obj with attribute value
        +test_tier: 1
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-148958
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework: TUF
        +external_files:4Page-arial.obj=c74922027034624c176f82abd10e72e375b8a81ae68fdcdc37af09797d546468
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pdl_intent_ipp_pcl5_highvalue_4page_arial_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: test_pdl_intent_ipp_pcl5_highvalue_4page_arial
            +guid:7fba3b02-3e79-40b8-b48c-c7dee5095e13
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5 & PrintProtocols=IPP & MediaSizeSupported=na_executive_7.25x10.5in & PrintColorMode=GrayScale & Print=Normal & MediaType=Plain & MediaInputInstalled=Tray1 & PrintResolution=Print600

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pdl_intent_ipp_pcl5_highvalue_4page_arial_file_then_succeeds(self):
        if self.media.is_size_supported('na_executive_7.25x10.5in', 'tray-1'):
            self.media.tray.configure_tray('tray-1', 'na_executive_7.25x10.5in', 'stationery')

        ipp_test_attribs = {'document-format': 'application/vnd.hp-PCL5', 'media': 'na_executive_7.25x10.5in','print-color-mode': 'process-monochrome', 'print-quality': 4, 'copies':1, 'sides': 'one-sided', 'media-source': 'tray-1', 'orientation-requested': 3, 'media-type': 'stationery', 'resolution': '600x600dpi'}
        ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

        printjob.ipp_print(ipp_test_file, 'c74922027034624c176f82abd10e72e375b8a81ae68fdcdc37af09797d546468')
        outputverifier.save_and_parse_output()
        outputverifier.verify_page_count(Intents.printintent, 4)
        outputverifier.verify_collated_copies(Intents.printintent, 1)
        outputverifier.verify_uncollated_copies(Intents.printintent, 1)
        outputverifier.verify_media_size(Intents.printintent, MediaSize.executive)
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.grayscale)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
        outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.gray)
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
        outputverifier.verify_print_quality(Intents.printintent, PrintQuality.normal)
        outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
        outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
        outputverifier.verify_resolution(Intents.printintent, 600)
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        self.media.tray.reset_trays()
