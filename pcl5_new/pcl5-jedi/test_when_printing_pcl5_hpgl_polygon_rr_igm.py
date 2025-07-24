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
        +purpose: pcl5 hpgl using rr_igm.obj
        +test_tier: 3
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:600
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:ENTA4ProductTest
        +test_framework: TUF
        +external_files:rr_igm.obj=365a1a90377241aa2a1c5636995c8c36a20c213762d76fa4960d688ec183b39f
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_hpgl_polygon_rr_igm_file_then_succeeds
        +test:
            +title: test_pcl5_hpgl_polygon_rr_igm
            +guid:dd959da7-0968-4aaa-bc35-39a42183b9be
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_hpgl_polygon_rr_igm_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('365a1a90377241aa2a1c5636995c8c36a20c213762d76fa4960d688ec183b39f')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
