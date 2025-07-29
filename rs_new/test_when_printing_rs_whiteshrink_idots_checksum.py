import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
from dunetuf.utility.systemtestpath import get_system_test_binaries_path

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
        +purpose: Print corner case job with white content and check WhiteShrink processing gives the right output
        +test_tier:1
        +is_manual:False
        +reqid:LFPPOS10987
        +timeout:500
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:tear_effect_plus_wspot_idots_OF60_14p_final.rs=5873062d721fa67dc0f3e0ff53de555af5f5bf186b29d343948da19456bad562
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_whiteshrink_idots_checksum_file_then_succeeds
        +test:
            +title:test_rs_whiteshrink_idots_checksum
            +guid:c70be642-a9f6-4d58-8d69-04d8e7f30ad0
            +dut:
                +type:Simulator, Emulator
                +configuration:DocumentFormat=RasterStreamPlanarICF & ConsumableSupport=WhiteInk
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_whiteshrink_idots_checksum_file_then_succeeds(self):

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        self.print.raw.start("5873062d721fa67dc0f3e0ff53de555af5f5bf186b29d343948da19456bad562", timeout=500)
        logging.info("RS tear_effect_plus_wspot_idots_OF60_14p_final - Print job completed successfully")

        expected_crc = ["0x2d369819"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("RS tear_effect_plus_wspot_idots_OF60_14p_final - Checksum(s) verified successfully")


