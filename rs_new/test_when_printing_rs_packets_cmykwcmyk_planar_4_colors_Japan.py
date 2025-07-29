import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver

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
        +purpose: test_rs_packets_cmykwcmyk_planar_4_colors_Japan
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-XXXX
        +timeout:820
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:packets_cmykwcmyk_planar_4_colors_japan.rs=a7f2e4c9e48cd713cbe4cb044b2ce9c535e210a306c86ed6c971adab8a064b2b
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_packets_cmykwcmyk_planar_4_colors_Japan_file_then_succeeds
        +test:
            +title:test_rs_packets_cmykwcmyk_planar_4_colors_Japan
            +guid:68b7b46a-3d5f-42ad-95a7-2a5ae2db5ac2
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=RasterStreamPlanarICF
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_packets_cmykwcmyk_planar_4_colors_Japan_file_then_succeeds(self):

        self.media.tray.load_simulator_media(tcl, "ADHESIVE_TRANSPARENT", "150106")
        job_id = self.print.raw.start('a7f2e4c9e48cd713cbe4cb044b2ce9c535e210a306c86ed6c971adab8a064b2b')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

        logging.info("RasterStream job finished")
