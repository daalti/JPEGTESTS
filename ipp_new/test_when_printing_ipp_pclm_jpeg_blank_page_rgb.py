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
        +purpose:C52177664 Ipp test for printing a PCLm file using attribute value media-size_letter
        +test_tier:1
        +is_manual:False
        +test_classification:System
        +reqid:DUNE-58957
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__Blank_PNG_Source.pdf=3107067f9b73e78814f5944d4927435be385a21cf1d94bc5b522a719f1a135da
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_jpeg_blank_page_rgb_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCLm
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_pclm_jpeg_blank_page_rgb
            +guid:b316b729-f218-4cbd-bfa0-ab36e72b24a8
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
    def test_when_using_ipp_pclm_jpeg_blank_page_rgb_file_then_succeeds(self):
        self.outputsaver.operation_mode('TIFF')
        self.outputsaver.validate_crc_tiff()
        ipp_test_attribs = {'document-format': 'application/PCLm', 'ipp-attribute-fidelity': 'true'}
        ipp_test_file = self.print.ipp.generate_test_file_path(**ipp_test_attribs)
        
        job_id = self.print.ipp.start(ipp_test_file, '3107067f9b73e78814f5944d4927435be385a21cf1d94bc5b522a719f1a135da')
        self.print.wait_for_job_completion(job_id)
        self.outputsaver.save_and_parse_output()
        self.outputsaver.operation_mode('NONE')
        Current_crc_value = self.outputsaver.get_crc()
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
