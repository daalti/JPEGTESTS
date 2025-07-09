import pytest
import logging
from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print
from dunetuf.print.print_common_types import MediaSize, MediaType
from dunetuf.media.media import Media
from dunetuf.print.output_saver import OutputSaver


class TestWhenPrintingJPEGFile:
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.job_queue = JobQueue()
        cls.job_history = JobHistory()
        cls.print = Print()
        cls.media = Media()
        cls.outputsaver = OutputSaver()

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""

    def setup_method(self):
        """Clean up resources after each test."""
        # Clear job queue
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        self.job_history.clear()
        self.job_history.wait_for_history_empty()

        # Get media configuration
        self.default_configuration = self.media.get_media_configuration()

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
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg testimgp Page from *testimgp.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:testimgp.jpg=e9486e697b7082a324fe2812310303e13b0ddf67b073eacb4b9d8a53e50b7ea7
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_testimgp_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_when_testimgp_jpg_then_succeeds
        +guid:207ec944-accf-4cdc-be7b-5a300be64488
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_testimgp_jpg_then_succeeds(self):


        expected_state = 'SUCCESS'

        response = cdm.get(cdm.CDM_MEDIA_CAPABILITIES)

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

        self.print.raw.start('e9486e697b7082a324fe2812310303e13b0ddf67b073eacb4b9d8a53e50b7ea7',expected_job_state=expected_state, timeout=120)
        self.print.wait_for_job_completion()
        self.outputsaver.save_output()

        logging.info("JPEG testimgp Page- Print job completed successfully")
