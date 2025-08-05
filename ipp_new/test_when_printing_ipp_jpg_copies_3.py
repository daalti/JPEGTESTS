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
        +purpose: IPP test for printing a JPG file using attribute value copies_3.
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-47064
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:broken2.jpg=746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_jpg_copies_3_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:JPEG
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_jpg_copies_3
            +guid:4ff18a1e-27dc-4ec1-b75f-26560df1d23f
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=JPEG & PrintProtocols=IPP & MediaSizeSupported=custom

    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_jpg_copies_3_file_then_succeeds(self):
        ipp_test_attribs = {'document-format': 'image/jpeg', 'copies': 3}
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)

            # the size of print file should in max/min custom size of printer supported, then could set custom size

        job_id = self.print.ipp.start(ipp_test_file, '746e460c805d937276f65426644ccb475358352a1cf5b7184a157650bcf3a9fc')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()

