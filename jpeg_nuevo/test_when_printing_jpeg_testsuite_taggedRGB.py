import logging
from dunetuf.print.output_saver import OutputSaver
from jpeg_nuevo.print_base import TestWhenPrinting


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.outputsaver = OutputSaver()

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
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of Jpeg TestSuite taggedRGB Page from *taggedRGB.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:300
    +asset:PDL_New
    +delivery_team:QualityGuild
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:taggedRGB.jpg=34027bf1e1808b1cf5995aedea2a805a35b12f77eb725ebb44dc662715fc295c
    +test_classification:System
    +name:TestWhenPrintingJPEGFile::test_when_taggedRGB_jpg_then_succeeds
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_taggedRGB
        +guid:b0c5ede3-101e-487b-9fa0-e97471a63002
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_taggedRGB_jpg_then_succeeds(self):

        expected_state = 'SUCCESS'

        response = self.media.get_media_capabilities()

        media_source= response['supportedInputs'][0]['mediaSourceId']
        resolution = response['supportedInputs'][0]['resolution']
        bottom_margin= response['supportedInputs'][0]['minimumPhysicalBottomMargin']/resolution
        top_margin= response['supportedInputs'][0]['minimumPhysicalTopMargin']/resolution
        left_margin= response['supportedInputs'][0]['minimumPhysicalLeftMargin']/resolution
        right_margin= response['supportedInputs'][0]['minimumPhysicalRightMargin']/resolution
        image_width=499/600  #Didn't have an option to get raw resolution of the image so using 600 as defualt resolution
        image_height=202/600

        if("roll" in media_source):
            if(image_width<(left_margin+right_margin) or image_height<(top_margin+bottom_margin)):
                expected_state='FAILED'

        job_id = self.print.raw.start('34027bf1e1808b1cf5995aedea2a805a35b12f77eb725ebb44dc662715fc295c')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
        logging.info("JPEG TestSuite taggedRGB Page - Print job completed successfully")
