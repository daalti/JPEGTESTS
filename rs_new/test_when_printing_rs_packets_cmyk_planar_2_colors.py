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
        +purpose: test_rs_packets_cmyk_planar_2_colors
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-3969
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:packets_cmyk_planar_2_colors.rs=85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_rs_packets_cmyk_planar_2_colors_file_then_succeeds
        +test:
            +title:test_rs_packets_cmyk_planar_2_colors
            +guid:296456e6-6dba-4669-be37-6a6f51f05bbf
            +dut:
                +type:Simulator, Emulator
                +configuration:PrintEngineType=MaiaLatex & DocumentFormat=RasterStreamPlanarICF
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_rs_packets_cmyk_planar_2_colors_file_then_succeeds(self):

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        job_id = self.print.raw.start('85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8')
        self.print.wait_for_job_completion(job_id)
        logging.info("packets_cmyk_planar_2_colors.rs - Print job completed successfully")

        expected_crc = ["0xa32323da"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("packets_cmyk_planar_2_colors.rs - Checksum(s) verified successfully")

