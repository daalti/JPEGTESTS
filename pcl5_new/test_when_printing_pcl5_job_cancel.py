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
        +purpose:Testing cancel of pcl5 jobs 
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-236978
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:66Page-pixel.obj=36342bd755c3212a1782f3f9a1afc6b11910e9dfed1102b4815d01ad532b2bd3
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_job_cancel_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: test_pcl5_job_cancel
            +guid:73f4ffa7-d248-428b-90b9-52acea34f61e
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5   

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_job_cancel_file_then_succeeds(self):
        logging.debug("Perform print job")
        job_id = self.print.raw.start('36342bd755c3212a1782f3f9a1afc6b11910e9dfed1102b4815d01ad532b2bd3')
        self.print.wait_for_job_completion(job_id)

        logging.info('Canceling print job')
        printjob.job.cancel_active_jobs()

        logging.info('Waiting for job cancellation')
        jobstate = self.print.wait_for_job_completion(jobid,120)
        assert 'CANCELED' in jobstate, "Unexpected final job state - {0}".format(jobstate)
