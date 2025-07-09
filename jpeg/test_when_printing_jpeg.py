
from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.print.print_new import Print


class TestWhenPrintingJPEGFile():
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        cls.job_queue = JobQueue()
        cls.job_history = JobHistory()
        cls.print = Print()

    @classmethod
    def teardown_class(cls):
        """Clean up shared test resources."""
        pass

    def setup_method(self):
        """Clean up resources after each test."""
        # Clear job queue
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        self.job_history.clear()
        self.job_history.wait_for_history_empty()

    def teardown_method(self):
        """Clean up resources after each test."""
        # Clear job queue
        self.job_queue.cancel_all_jobs()
        self.job_queue.wait_for_queue_empty()

        # Clear job history
        self.job_history.clear()
        self.job_history.wait_for_history_empty()

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:Simple print job of Jpeg file of 500kB from *file_example_JPG_500kB.jpg
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-17136
        +timeout:120
        +asset:PDL_Print
        +delivery_team:PDLJobPQ
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:file_example_JPG_500kB.jpg=838e346997ab5f2dd6745e9e536de6f9cd68965088354597f2fba016ad40ab2c
        +name:TestWhenPrintingJPEGFile::test_using_500KB_then_success
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_jpeg_file_example_JPG_500kB
            +guid:4baa15f8-9ca6-4196-8ab8-c86305914f1e
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_using_500KB_then_success(self):

        job_id = self.print.raw.start('838e346997ab5f2dd6745e9e536de6f9cd68965088354597f2fba016ad40ab2c')

        # Wait for copy job to complete
        self.print.wait_for_job_completion(job_id)


