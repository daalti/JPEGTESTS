import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from tests.network.print.ipp_utils import get_supported_job_preset_name_dict
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
        +purpose:IPP test for printing a pcl5 basic functionality using 1Page-fpri600.obj with attribute value
        +test_tier: 1
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-148958
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework: TUF
        +external_files:1Page-fpri600.obj=980cabbf08033824f1375b2ffc25963578d63833a42e3a1d20321495d35186b4
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pdl_intent_ipp_pcl5_basicfunctionality_1page_fpri600_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: test_pdl_intent_ipp_pcl5_basicfunctionality_1page_fpri600
            +guid:4507f160-faa7-4454-9ffb-165379a90b1a
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5 & PrintProtocols=IPP & MediaSizeSupported=na_index-4x6_4x6in & PrintColorMode=Color & Print=Best & MediaType=HPTri-foldBrochureGlossy150g & MediaInputInstalled=Tray1 & PrintResolution=Print600
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pdl_intent_ipp_pcl5_basicfunctionality_1page_fpri600_file_then_succeeds(self):
        if self.media.is_size_supported('na_index-4x6_4x6in', 'tray-1'):
            self.media.tray.configure_tray('tray-1', 'na_index-4x6_4x6in', 'com.hp-trifold-brochure-glossy-150gsm')
        job_preset_names = get_supported_job_preset_name_dict(printjob.ip_address)
        print_quality_high = 5
        ipp_test_attribs = {'document-format': 'application/vnd.hp-PCL5', 'media': 'na_index-4x6_4x6in', 'print-color-mode': 'color', 'print-quality': print_quality_high, 'copies':2, 'sides': 'one-sided', 'media-source': 'tray-1', 'media-type': 'com.hp-trifold-brochure-glossy-150gsm' , 'orientation-requested': 4, 'resolution': '600x600dpi'}
        ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

        printjob.ipp_print(ipp_test_file, '980cabbf08033824f1375b2ffc25963578d63833a42e3a1d20321495d35186b4')
        outputverifier.save_and_parse_output()
        outputverifier.verify_page_count(Intents.printintent, 1)
        outputverifier.verify_collated_copies(Intents.printintent, 1)
        outputverifier.verify_uncollated_copies(Intents.printintent, 2)
        outputverifier.verify_media_size(Intents.printintent, MediaSize.photo4x6)
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.color)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
        outputverifier.verify_color_rendering(Intents.printintent, ColorRenderingType.office_rgb)
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
        outputverifier.verify_print_quality(Intents.printintent, PrintQuality[job_preset_names[print_quality_high]])
        outputverifier.verify_media_type(Intents.printintent, MediaType.hptrifoldglossy150g)
        outputverifier.verify_media_source(Intents.printintent, MediaSource.tray1)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
        outputverifier.verify_resolution(Intents.printintent, 600)
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        self.media.tray.reset_trays()
