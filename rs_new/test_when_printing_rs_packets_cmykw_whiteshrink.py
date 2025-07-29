import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
import time

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
        +purpose: test_rs_packets_cmykw_whiteshrink
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-62762
        +timeout:900
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:tear_effect_plus_wspot_Inv_OF60_14p_Choke3px.rs=a86aea37bb0395ef38fd9339d6794922448db2f51a040f92b28776eb38176f88
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_packets_cmykw_whiteshrink_file_then_succeeds
        +test:
            +title:test_rs_packets_cmykw_whiteshrink
            +guid:3cd41bf2-48e3-4b61-b975-804169e620c4
            +dut:
                +type:Simulator, Emulator
                +configuration:DocumentFormat=RasterStreamPlanarICF & ConsumableSupport=WhiteInk
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_packets_cmykw_whiteshrink_file_then_succeeds(self):

        self.print.raw.start(
            'a86aea37bb0395ef38fd9339d6794922448db2f51a040f92b28776eb38176f88', timeout=850)
        self.outputsaver.save_output()

        logging.info("RasterStream job finished")


