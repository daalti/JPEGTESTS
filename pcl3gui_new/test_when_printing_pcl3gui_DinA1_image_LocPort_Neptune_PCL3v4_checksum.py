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
    $$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose: Print job file pcl3Gui_DinA1_image_LocPort_Neptune_PCL3v4
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:500
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:DinA1_image_LocPort_Neptune_PCL3v4.prn=d12c32dc8c21ab67365790c727bfc924722f4a7e590e7a1c44a7ea9ada089610
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_DinA1_image_LocPort_Neptune_PCL3v4_checksum_file_then_succeeds
        +test:
            +title:test_pcl3Gui_DinA1_image_LocPort_Neptune_PCL3v4_checksum
            +guid:353d3916-3ad0-4641-9500-096f7a14cbac
            +dut:
                +type:Simulator, Emulator
                +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pcl3gui_DinA1_image_LocPort_Neptune_PCL3v4_checksum_file_then_succeeds(self):

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('d12c32dc8c21ab67365790c727bfc924722f4a7e590e7a1c44a7ea9ada089610')
        self.print.wait_for_job_completion(job_id)

        logging.info("Pcl3Gui DinA1_image_LocPort_Neptune_PCL3v4 - Print job completed successfully")

        expected_crc = ["0x4c84272"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("Pcl3Gui DinA1_image_LocPort_Neptune_PCL3v4 - Print job completed successfully")
