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
        +purpose:Erroneous PCL3GUI file fails successfully without crashes
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-140912
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:cannot_be_canceled.prn=67a05f131f07edbabda1c0214f6eddad160e141780f376fc40dcbfe2b1ca97ba
        +name:TestWhenPrintingJPEGFile::test_when_using_pcl3_cannot_be_canceled_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCL3GUI
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_pcl3_cannot_be_canceled
            +guid:486d7ce5-750a-40dd-aba9-2aad38578be1
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
    def test_when_using_pcl3_cannot_be_canceled_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        job_id = self.print.raw.start('67a05f131f07edbabda1c0214f6eddad160e141780f376fc40dcbfe2b1ca97ba')
        self.print.wait_for_job_completion(job_id)

        self.outputsaver.save_output()
