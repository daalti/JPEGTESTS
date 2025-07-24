import logging
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType
from dunetuf.print.new.output.output_verifier import OutputVerifier
from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver


class TestWhenPrintingJPEGFile(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)
        cls.outputverifier = OutputVerifier(cls.outputsaver)


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
        +purpose:PCL5 high value test using **103785-SAP-M806-data1.prn
        +test_tier: 1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-156300
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:103785-SAP-M806-data1.prn=9f800530a956d952e470869a61563daf98433d6469e158090d8bc3fbf67b6120
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_conf_hv_103785_sap_m806_data1_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl5_conf_hv_103785_sap_m806_data1
            +guid:dd9e1794-ac25-485f-a476-9696d7abee51
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_conf_hv_103785_sap_m806_data1_file_then_succeeds(self):
        job_id = self.print.raw.start('9f800530a956d952e470869a61563daf98433d6469e158090d8bc3fbf67b6120')
        self.print.wait_for_job_completion(job_id)
        self.outputverifier.save_and_parse_output()
