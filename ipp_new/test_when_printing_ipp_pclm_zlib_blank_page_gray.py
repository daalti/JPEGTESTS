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
        +purpose:C52177666 Ipp test for printing a URF file using attribute value media-size_letter
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-47064
        +timeout:120
            +asset:PDL_New
            +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:PCLm_letter_600_czlib_H64_PgCnt1_GRAY__Blank_PNG_Source.pdf=f7dc441c5270051aab55006375ffec95a29896cd06e59b2a74511b510000f4c4
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_zlib_blank_page_gray_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCLm
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_pclm_zlib_blank_page_gray
                    +guid:6e65b10b-003b-473d-a6aa-9c71a1270a36
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCLm & PrintProtocols=IPP
        +overrides:
            +Home:
                +is_manual:False
                +timeout:300
                +test:
                    +dut:
                        +type:Engine
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    def test_when_using_ipp_pclm_zlib_blank_page_gray_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        ipp_test_file = self.print.ipp.generate_test_file_path()
        job_id = self.print.ipp.start(ipp_test_file, 'f7dc441c5270051aab55006375ffec95a29896cd06e59b2a74511b510000f4c4')
        self.print.wait_for_job_completion(job_id)
