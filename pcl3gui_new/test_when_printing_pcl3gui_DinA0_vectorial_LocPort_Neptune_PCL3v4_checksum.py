import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver
import time
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
    $$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: Print job file *DinA0_vectorial_LocPort_Neptune_PCL3v4.prn
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-3413
        +timeout:350
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:DinA0_vectorial_LocPort_Neptune_PCL3v4.prn=7c58792c27c6a86acac9c38d48accd04cf48f8053907956f534b38a6e450f4bd
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_DinA0_vectorial_LocPort_Neptune_PCL3v4_checksum_file_then_succeeds
        +test:
            +title:test_pcl3gui_DinA0_vectorial_LocPort_Neptune_PCL3v4_checksum
            +guid:2a1d87fb-d3f8-46b6-857b-522eb9f5e3be
            +dut:
                +type:Simulator, Emulator
                +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pcl3gui_DinA0_vectorial_LocPort_Neptune_PCL3v4_checksum_file_then_succeeds(self):

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        self.outputsaver.validate_crc_tiff()

        job_id = self.print.raw.start('7c58792c27c6a86acac9c38d48accd04cf48f8053907956f534b38a6e450f4bd')

        self.print.wait_for_job_completion(job_id)

        logging.info("PRN DinA0_vectorial_LocPort_Neptune_PCL3v4 - Print job completed successfully")

        expected_crc = ["0x68f21c10"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("PRN DinA0_vectorial_LocPort_Neptune_PCL3v4 - Print job completed successfully")
