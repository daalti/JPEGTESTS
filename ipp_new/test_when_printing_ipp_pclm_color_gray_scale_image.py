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
        +purpose:Ipp test for printing a PCL file using attribute value print-color-mode_process-monochrome
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-47064
        +timeout:300
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_GRAY__JPG_Source.pdf=321d8bd87003851c01f847d1299cbdd0655a096cd9c7b585a1a6f26a340536c0
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_color_gray_scale_image_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCLm
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_pclm_color_gray_scale_image
            +guid:7db1a6c4-87a6-47dc-bda0-45752cdd3f5d
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCLm & PrintProtocols=IPP
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pclm_color_gray_scale_image_file_then_succeeds(self):
        ipp_test_attribs = {'document-format': 'application/PCLm', 'print-color-mode': 'monochrome', 'ipp-attribute-fidelity': 'false'}
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)
        job_id = self.print.ipp.start(ipp_test_file, '321d8bd87003851c01f847d1299cbdd0655a096cd9c7b585a1a6f26a340536c0')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_output()
