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
        +purpose:Simple print job of a A4 3 pages grayscale rotated 180 degree PCL3GUI file
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-151979
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A4_grayscale_rotated_180.prn=ce02c5089ded111ff642a2098b477332e9d7a70b06711cab85a748c8ddb260f0
        +name:TestWhenPrintingJPEGFile::test_when_using_pdl_intent_pcl3gui_A4_grayscale_rotated_180_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pdl_intent_pcl3gui_A4_grayscale_rotated_180
            +guid:1716d865-22d3-460b-b62a-8f52abac9ef9
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL3GUI & MediaSizeSupported=custom & PrintColorMode=GrayScale & Print=Best & MediaType=Plain & MediaInputInstalled=MainRoll
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pdl_intent_pcl3gui_A4_grayscale_rotated_180_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('ce02c5089ded111ff642a2098b477332e9d7a70b06711cab85a748c8ddb260f0')
        self.print.wait_for_job_completion(job_id)

        outputverifier.save_and_parse_output()
        outputverifier.verify_page_count(Intents.printintent, 3)
        outputverifier.verify_collated_copies(Intents.printintent, 4)
        outputverifier.verify_uncollated_copies(Intents.printintent, 1)
        outputverifier.verify_media_size(Intents.printintent, MediaSize.custom)
        outputverifier.verify_color_mode(Intents.printintent, ColorMode.auto_monochrome)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
        outputverifier.verify_print_quality(Intents.printintent, PrintQuality.best)
        outputverifier.verify_media_type(Intents.printintent, MediaType.stationery)
        outputverifier.verify_media_source(Intents.printintent, MediaSource.mainroll)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
        outputverifier.verify_resolution(Intents.printintent, 600)
        self.outputsaver.save_output()
        self.outputsaver.operation_mode('NONE')
        self.media.tray.reset_trays()
