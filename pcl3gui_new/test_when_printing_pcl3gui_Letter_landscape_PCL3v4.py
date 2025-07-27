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
        +purpose:Simple print job of pcl3Gui_Letter_landscape_PCL3v4
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-3422
        +timeout:300
        +asset:PDL_New
        +test_framework:TUF
        +external_files:Letter_landscape_PCL3v4.prn=8fbde5ad03e851f1e228f6b235d73ce855e8329a70b026b3ef3fa24689c773a0
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_Letter_landscape_PCL3v4_file_then_succeeds
        +test:
            +title:test_pcl3Gui_Letter_landscape_PCL3v4
            +guid:31c83067-e0ca-48e2-a0f6-4664835bbd0f
            +dut:
                +type:Simulator, Emulator
                +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl3gui_Letter_landscape_PCL3v4_file_then_succeeds(self):
        
        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')

        printjob.print_verify_multi('8fbde5ad03e851f1e228f6b235d73ce855e8329a70b026b3ef3fa24689c773a0','SUCCESS', 1, 300)
        logging.info("Pcl3Gui Letter_landscape_PCL3v4 - Print job completed successfully")
        
        expected_crc = ["0xb03f5e3"]
        
        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("Pcl3Gui Letter_landscape_PCL3v4 - Checksum(s) verified successfully")
