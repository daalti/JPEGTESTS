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
        +purpose:Simple print job of pcl3Gui_DINA3_image_LocPort_Neptune_PCL3v4
        +test_tier:1
        +is_manual:False
        +reqid:LFPSWQAA-3415
        +timeout:360
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:DINA3_image_LocPort_Neptune_PCL3v4.prn=923cb9de885b1014d38b687628065985686a9b05aa5a8bf84dc634e25eb0ed20
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_DINA3_image_LocPort_Neptune_PCL3v4_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl3Gui_DINA3_image_LocPort_Neptune_PCL3v4
            +guid:11a5361c-d379-4899-b822-bb422dfecc47
            +dut:
                +type:Simulator
                +configuration:PrintEngineType=Maia & DocumentFormat=PCL3GUI
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pcl3gui_DINA3_image_LocPort_Neptune_PCL3v4_file_then_succeeds(self):
        
        # CRC will be calculated using the payload of all the RasterDatas
        self.outputsaver.operation_mode('CRC')
        
        printjob.print_verify_multi('923cb9de885b1014d38b687628065985686a9b05aa5a8bf84dc634e25eb0ed20', 'SUCCESS', 1, 300)
        logging.info("Pcl3Gui DINA3_image_LocPort_Neptune_PCL3v4 - Print job completed successfully")
        
        expected_crc = ["0x7998988f"]
        
        # Read and verify that obtained checksums are the expected ones
        self.outputsaver.save_output()
        self.outputsaver.verify_output_crc(expected_crc)
        logging.info("Pcl3Gui DINA3_image_LocPort_Neptune_PCL3v4 - Checksum(s) verified successfully")
