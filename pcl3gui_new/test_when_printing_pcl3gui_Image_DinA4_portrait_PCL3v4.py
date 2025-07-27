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
        +purpose:Simple print job of PRN of Image_DinA4_portrait_PCL3v4 Page from *Image_DinA4_portrait_PCL3v4.prn file
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-3387
        +timeout:120
        +asset:PDL_New
        +test_framework:TUF
        +external_files:Image_DinA4_portrait_PCL3v4.prn=52949853ab1b37d10ddadba1d127cecac34fd82c956c46e733d88196ae915ca5
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_Image_DinA4_portrait_PCL3v4_file_then_succeeds
        +test:
            +title:test_pcl3gui_Image_DinA4_portrait_PCL3v4
            +guid:0e8d58a1-7e9e-4687-ad9c-6be56d63b0db
            +dut:
                +type:Simulator, Emulator
                +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl3gui_Image_DinA4_portrait_PCL3v4_file_then_succeeds(self):
        
        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')
        
        printjob.print_verify_multi('52949853ab1b37d10ddadba1d127cecac34fd82c956c46e733d88196ae915ca5', 'SUCCESS', 1, 120)
        logging.info("PRN Image_DinA4_portrait_PCL3v4 - Print job completed successfully")
        
        expected_crc = ["0x206da19e"]
        
        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("PRN Image_DinA4_portrait_PCL3v4 - Checksum(s) verified successfully")
