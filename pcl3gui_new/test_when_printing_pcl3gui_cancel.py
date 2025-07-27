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
        +purpose:Testing internal cancel due to parsing issue of fuzzed pcl3 job
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-DUNE-140905
        +timeout:200
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:fuzzed_pcl3gui_fail.pcl=eb61eccac4869467a78e6299c32852931355112a2eb5826ec795ac51cb9a65b2
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3gui_cancel_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl3gui_internal_cancel_fuzzedjob
            +guid:d5ce4624-f833-4b6f-8ccd-66cfe7883746
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCL3GUI
        +overrides:
            +Home:
                +is_manual:False
                +timeout:240
                +test:
                    +dut:
                        +type:Engine
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$
    """
    def test_when_using_pcl3gui_cancel_file_then_succeeds(self):
        logging.debug("Perform print job for fuzzed pcl job")
        jobid = printjob.start_print('eb61eccac4869467a78e6299c32852931355112a2eb5826ec795ac51cb9a65b2')

        logging.info('Waiting for job cancellation')
        jobstate = printjob.wait_for_job_completion(jobid,200)
        assert 'FAILED' in jobstate, "Unexpected final job state - {0}".format(jobstate)

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
            +purpose:Testing user cancel of PCL3GUI jobs
            +test_tier:1
            +is_manual:False
            +reqid:DUNE-136515
            +timeout:120
            +asset:PDL_Print
            +delivery_team:PDLJobPQ
            +feature_team:PDLSolns
            +test_framework:TUF
            +external_files:MinumC_A4_P_FD_3pgs.pcl=96d3cab1cd5359404517a12076f2ad8613e4ecea8b071062905785af40e8edce
            +test_classification:System
            +name:test_pcl3gui_user_cancel
            +categorization:
                +segment:Platform
                +area:Print
                +feature:PDL
                +sub_feature:PCL3GUI
                +interaction:Headless
                +test_type:Positive
            +test:
                +title:test_pcl3gui_user_cancel
                +guid:50853826-f96a-452b-8cb3-5b978ca00b3a
                +dut:
                    +type:Simulator
                    +configuration:DocumentFormat=PCL3GUI
            +overrides:
                +Home:
                    +is_manual:False
                    +timeout:240
                    +test:
                        +dut:
                            +type:Engine    
            
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
        """
    def test_when_using_pcl3gui_cancel_file_then_succeeds(self):
        logging.debug("Perform print job")
        jobid = printjob.start_print('96d3cab1cd5359404517a12076f2ad8613e4ecea8b071062905785af40e8edce')

        logging.info('Canceling print job')
        printjob.job.cancel_active_jobs()

        logging.info('Waiting for job cancellation')
        jobstate = printjob.wait_for_job_completion(jobid,120)
        assert 'CANCELED' in jobstate, "Unexpected final job state - {0}".format(jobstate)

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
            +purpose:Testing internal cancel due to parsing issue
            +test_tier:1
            +is_manual:False
            +reqid:DUNE-136730
            +timeout:200
            +asset:PDL_Print
            +delivery_team:PDLJobPQ
            +feature_team:PDLSolns
            +test_framework:TUF
            +external_files:minim_pn.pcl=d572e0aadb86840eea10a254861dcacadc76876f3b6c410a52e1c5efc0f8dced
            +test_classification:System
            +name:test_pcl3gui_internal_cancel
            +categorization:
                +segment:Platform
                +area:Print
                +feature:PDL
                +sub_feature:PCL3GUI
                +interaction:Headless
                +test_type:Positive
            +test:
                +title:test_pcl3gui_internal_cancel
                +guid:8b1c1aff-0e75-45ae-bb01-506156934869
                +dut:
                    +type:Simulator
                    +configuration:DocumentFormat=PCL3GUI
            +overrides:
                +Home:
                    +is_manual:False
                    +timeout:240
                    +test:
                        +dut:
                            +type:Engine    
            
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
        """
    def test_when_using_pcl3gui_cancel_file_then_succeeds(self):
        logging.debug("Perform print job")
        jobid = printjob.start_print('d572e0aadb86840eea10a254861dcacadc76876f3b6c410a52e1c5efc0f8dced')

        logging.info('Waiting for job cancellation')
        jobstate = printjob.wait_for_job_completion(jobid,200)
        assert 'FAILED' in jobstate, "Unexpected final job state - {0}".format(jobstate)
