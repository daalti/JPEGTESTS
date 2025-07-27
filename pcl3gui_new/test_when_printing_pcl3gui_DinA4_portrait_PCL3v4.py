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
        +purpose:Simple print job of PRN of DinA4_portrait_PCL3v4 Page from *DinA4_portrait_PCL3v4.prn file
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-3387
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:DinA4_portrait_PCL3v4.prn=4310ea462c1447ae96b04cd713cc458d97897c269a102dc02ee46a1576754b16
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_DinA4_portrait_PCL3v4_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl3gui_DinA4_portrait_PCL3v4_300dpi
            +guid:2de6ba70-5a8b-465e-9beb-3c4f77147be9
            +dut:
                +type:Simulator
                +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pcl3gui_DinA4_portrait_PCL3v4_file_then_succeeds(self):
        
        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')
        
        printjob.print_verify_multi('4310ea462c1447ae96b04cd713cc458d97897c269a102dc02ee46a1576754b16', 'SUCCESS', 1, 120)
        logging.info("PRN DinA4_portrait_PCL3v4 - Print job completed successfully")
        
        expected_crc = ['0x45982007']
        
        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("PRN DinA4_portrait_PCL3v4 - Checksum(s) verified successfully")
