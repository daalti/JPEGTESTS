import logging

from dunetuf.print.new.output.output_saver import OutputSaver
from tests.print.pdl.print_base import TestWhenPrinting, setup_output_saver, tear_down_output_saver


class TestWhenPrintingFileFromIPP(TestWhenPrinting):
    @classmethod
    def setup_class(cls):
        """Initialize shared test resources."""
        super().setup_class()
        cls.outputsaver = OutputSaver()
        setup_output_saver(cls.outputsaver)

    @classmethod
    def teardown_class(cls):
        """Release shared test resources."""
        # no-op unless the legacy file had a matching teardown
        pass

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
        self.media.reset_inputs()

        tear_down_output_saver(self.outputsaver)

    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$

        +purpose: IPP test for printing a 1200 JPG file using attribute value printquality normal.
        +test_tier:1
        +is_manual:False
        +timeout:700
            +asset:PDL_New
            +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +reqid:DUNE-115947
        +test_framework:TUF
        +external_files:test_file_16Meg6.jpg=211995c4853e73292d67d7a4eb85161090318b23cf516b3469aaee3874720d56
        +test_classification:System
            +name:TestWhenPrintingIPPFile::test_when_using_ipp_printquality_resolver_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_jpg_printquality_resolver_pqNormal
                +guid:e415badc-72fd-46d4-8c58-d91a2233df83
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & PrintResolution=Print1200

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_printquality_resolver_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        ipp_test_file = self.print.ipp.generate_test_file_path()
        job_id = self.print.ipp.start(ipp_test_file, '211995c4853e73292d67d7a4eb85161090318b23cf516b3469aaee3874720d56')
        self.print.wait_for_job_completion(job_id)
