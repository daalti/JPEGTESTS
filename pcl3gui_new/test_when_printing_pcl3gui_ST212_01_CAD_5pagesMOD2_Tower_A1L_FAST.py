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
    $$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Print job file ST212-01-CAD-5pages-Tower-A1L checksum
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-4385
        +timeout:700
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:ST212-01-CAD-5pagesMOD2-Tower-A1L-FAST.prn=b3eff59492252078bb8ab0d4c295e860c2ed71ce0572414147ceac92fc486e42
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_ST212_01_CAD_5pagesMOD2_Tower_A1L_FAST_file_then_succeeds
        +test:
            +title:test_pcl3gui_ST212_01_CAD_5pagesMOD2_Tower_A1L_FAST_300dpi
            +guid:b91626c8-3b37-43a8-81c5-325cbabcb323
            +dut:
                +type:Emulator, Simulator
                +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pcl3gui_ST212_01_CAD_5pagesMOD2_Tower_A1L_FAST_file_then_succeeds(self):

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        self.outputsaver.validate_crc_tiff()

        job_id = self.print.raw.start('b3eff59492252078bb8ab0d4c295e860c2ed71ce0572414147ceac92fc486e42')

        self.print.wait_for_job_completion(job_id)

        logging.info("test_pcl3gui_ST212_01_CAD_5pagesMOD2_Tower_A1L_FAST_checksum - Print job completed successfully")

        expected_crc = ['0xd3efd4f7', '0x8e46b3bf', '0xbb89a8ad', '0x7b5a5ffd', '0xcc1c981f']

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("test_pcl3gui_ST212_01_CAD_5pagesMOD2_Tower_A1L_FAST_checksum' - Print job completed successfully")
