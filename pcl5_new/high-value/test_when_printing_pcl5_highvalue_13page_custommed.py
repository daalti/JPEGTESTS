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
        +purpose: pcl5 highvalue using 13Page_custommed.obj
        +test_tier: 1
        +is_manual: False
        +test_classification: 1
        +reqid: DUNE-37356
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework: TUF
        +external_files:13Page-custommed.obj=5423a3115ab10bbdbb589f019f55addfdf5c0d0be1955fd3be7f4c0eb79fc6e7
        +test_classification:System
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl5_highvalue_13page_custommed_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL5
            +interaction:Headless
            +test_type:Positive
        +test:
            +title: test_pcl5_highvalue_13page_custommed
            +guid:ca4d88ab-20da-49be-9f89-19fa06ae08c3
            +dut:
                +type:Simulator
                +configuration: DocumentFormat=PCL5 &  MediaSizeSupported=Any

        +overrides:
            +Enterprise:
                +is_manual:False
                +timeout:600
                +test:
                    +dut:
                        +type:Emulator


    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_pcl5_highvalue_13page_custommed_file_then_succeeds(self):
        job_id = self.print.raw.start('5423a3115ab10bbdbb589f019f55addfdf5c0d0be1955fd3be7f4c0eb79fc6e7')
        self.print.wait_for_job_completion(job_id)
        outputverifier.save_and_parse_output()
        outputverifier.verify_page_count(Intents.printintent, 29)
