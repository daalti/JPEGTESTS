import logging
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.print.new.output.output_saver import OutputSaver
from dunetuf.cdm import get_cdm_instance
from dunetuf.metadata import get_ip
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)
        cls.ip_address = get_ip()
        cls.cdm = get_cdm_instance(cls.ip_address)

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
        +purpose:Simple print job of Jpeg testorig Page from *testorig.jpg file
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-17136
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:testorig.jpg=acc6ec555d41d15b368320edaa3b20958ee6fa97cb6e4a18d1213d5ae8bec73b
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_testorig_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_testorig
            +guid:cbede0ce-4c17-42d1-9b75-6398e1336dde
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_testorig_file_then_succeeds(self):


        expected_state = 'SUCCESS'

        response = self.media.get_media_capabilities()

        media_source= response['supportedInputs'][0]['mediaSourceId']
        resolution = response['supportedInputs'][0]['resolution']
        bottom_margin= response['supportedInputs'][0]['minimumPhysicalBottomMargin']/resolution
        top_margin= response['supportedInputs'][0]['minimumPhysicalTopMargin']/resolution
        left_margin= response['supportedInputs'][0]['minimumPhysicalLeftMargin']/resolution
        right_margin= response['supportedInputs'][0]['minimumPhysicalRightMargin']/resolution
        image_width=227/600  #Didn't have an option to get raw resolution of the image so using 600 as defualt resolution
        image_height=149/600

        if("roll" in media_source):
            if(image_width<(left_margin+right_margin) or image_height<(top_margin+bottom_margin)):
                expected_state='FAILED'

        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('acc6ec555d41d15b368320edaa3b20958ee6fa97cb6e4a18d1213d5ae8bec73b')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

        logging.info("JPEG testorig Page- Print job completed successfully")