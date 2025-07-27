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
        +purpose: Print job file ST212-01-CAD-Tower-5pages-A1L-FAST-rev5_-2_600 
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-61462
        +timeout:800
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:LFP_PrintWorkflows
        +test_framework:TUF
        +external_files:ST212-01-CAD-Tower-5pages-A1L-FAST-rev5_-2_600.prn=6dc1f4dd93ceb76877a833d0dae2c1288c0668784aa302d174472c81304b4e19
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3Gui_ST212_01_CAD_Tower_5pages_A1L_FAST_rev5_2_600_file_then_succeeds
        +test:
            +title:test_pcl3Gui_ST212_01_CAD_Tower_5pages_A1L_FAST_rev5_2_600
            +guid:9a7fe0e0-5a31-4c2e-9c4d-e4dd94148e0c
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL3GUI & EngineFirmwareFamily=Maia
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl3Gui_ST212_01_CAD_Tower_5pages_A1L_FAST_rev5_2_600_file_then_succeeds(self):

        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        self.outputsaver.validate_crc_tiff()

        job_id = self.print.raw.start('6dc1f4dd93ceb76877a833d0dae2c1288c0668784aa302d174472c81304b4e19')

        self.print.wait_for_job_completion(job_id)

        logging.info("ST212-01-CAD-Tower-5pages-A1L-FAST-rev5_-2_600.prn - Print job completed successfully")

        expected_crc = ["0x87d8ae1a", "0x5b0631e2", "0xed19c28e", "0xec1adf81", "0x3cad5711"]

        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("ST212-01-CAD-Tower-5pages-A1L-FAST-rev5_-2_600.prn - Print job completed successfully")
