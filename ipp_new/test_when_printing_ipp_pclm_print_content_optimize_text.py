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
        +purpose:C30485385 Print_Content_Optimize-optimize-text
        +test_tier:3
        +is_manual:False
        +reqid:DUNE-244314
        +timeout:360
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:RCB-ProductQA
        +test_framework:TUF
        +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_GRAY__BlackText.pdf=1756a4162fc3ac39348df16bfc605e21bff65224c5d2d79fae07960715d860dc
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_print_content_optimize_text_file_then_succeeds
        +test:
            +title:test_ipp_pclm_print_pclm_letter_600_cjpeg_h64_pgcnt1_gray_black_text
            +guid:53d77f40-e788-4969-aeda-d93cae28cf10
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
    def test_when_using_ipp_pclm_print_content_optimize_text_file_then_succeeds(self):
        self.outputsaver.validate_crc_tiff()
        
        print_file = self.print.get_file('1756a4162fc3ac39348df16bfc605e21bff65224c5d2d79fae07960715d860dc')
        ipp_test_file = "/code/tests/print/pdl/ipp/attributes/print-content-optimize-text.test"
        
        returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, ipp_test_file , print_file)
        assert returncode == 0, f'Unexpected IPP response: {decoded_output[0]}'
        assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
        assert "[FAIL]" not in decoded_output[0], "Ipp print job is Failed with some issue."
        assert "print-content-optimize (keyword) = text" in decoded_output[0], "Text and Graphics should not be seen for the listed attribute."
        assert decoded_output[1] == '', "There is error output for Ipp Print."
        
        self.outputsaver.save_and_parse_output()
        logging.info("Get crc value for the current print job")
        Current_crc_value = self.outputsaver.get_crc()
        logging.info("Validate current crc with master crc")
        assert self.outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
