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
        +purpose: IPP test for printing a JPG file when all sources are empty.
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-168730
        +timeout:240
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:A3_margin_portrait.jpg=d6b956d1775efee42d23dafa8ff0309a12614c6d4f0e7cea35a485057e63ab76
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_jpg_media_size_allSourcesEmpty_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_jpg_media_size_allSourcesEmpty
            +guid:87f0a6e5-c274-47bb-a7e2-60ff408afda0
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaInputInstalled=MainRoll & MediaInputInstalled=Main
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_jpg_media_size_allSourcesEmpty_file_then_succeeds(self):
        ipp_test_attribs = {
            'document-format': 'image/jpeg',
            'print-scaling': 'fit',
            'media-size-name': 'iso_a3_297x420mm',
            'media-bottom-margin': 499,
            'media-left-margin': 499,
            'media-right-margin': 499,
            'media-top-margin': 499,
            'print-quality': 3,
        }
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)
        job_id = self.print.ipp.start(ipp_test_file, 'd6b956d1775efee42d23dafa8ff0309a12614c6d4f0e7cea35a485057e63ab76')
        self.print.wait_for_job_completion(job_id)
