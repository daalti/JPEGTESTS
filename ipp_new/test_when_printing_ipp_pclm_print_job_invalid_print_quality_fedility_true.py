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
        +purpose: IPP test for printing a pdf file using attribute value print_quality_invalid
        +test_tier:1
        +is_manual:False
        +reqid:DUNE-58957
        +timeout:120
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:PDLSolns
        +test_framework:TUF
        +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_print_job_invalid_print_quality_fedility_true_file_then_succeeds
        +categorization:
            +segment:Platform
            +area:Print
            +feature:PDL
            +sub_feature:PCLm
            +interaction:Headless
            +test_type:Positive
        +test:
            +title:test_ipp_pclm_print_job_invalid_print_quality_fedility_true
            +guid:a44d24ba-fab7-41a5-8906-79a21bb3c037
            +dut:
                +type:Simulator
                +configuration:DocumentFormat=PCLm & PrintProtocols=IPP
    
    $$$$$_END_TEST_METADATA_DECLARATION_$$$$$
    """
    
    def test_ipp_pclm_print_job_invalid_print_quality_fedility_true(setup_teardown, printjob, outputsaver):
        outputsaver.operation_mode('TIFF')
        ipp_test_attribs = {'document-format': 'application/PCLm', 'ipp-attribute-fidelity': 'true', 'print-quality': 7}
        ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)
        try:
            logging.info('Verifying fidelity with attribute: print-quality')
    
            printjob.ipp_print(ipp_test_file, '7d4ca44443b3bde01436d323258048f7578b41d6f586e38c5b1ef5b95d52bc23')
            assert False, f"Test was expectd to fail with print-quality as {ipp_test_attribs['print-quality']}"
        except AssertionError as exp:
            if 'Unexpected IPP response' in str(exp):
                logging.info('Test failed as expected with print-quality as %s', ipp_test_attribs['print-quality'])
        outputsaver.operation_mode('NONE')
        logging.info("For invalid quality and fidelity true case, file is not print. No need to check CRC for this case.")
    
    
    
    """
    $$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
        +purpose:C30485296 Print_Quality-invalid print-quality-ipp-fidelity = true
        +test_tier:3
        +is_manual:False
        +reqid:DUNE-244314
        +timeout:180
        +asset:PDL_New
        +delivery_team:QualityGuild
        +feature_team:RCB-ProductQA
        +test_framework:TUF
        +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB.pdf=b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8
        +test_classification:System
        +name:TestWhenPrintingIPPFile::test_when_using_ipp_pclm_print_job_invalid_print_quality_fedility_true_file_then_succeeds
        +test:
            +title:test_ipp_pclm_letter_600_cjpeg_h64_pgcnt1_rgb_invalid_print_quality_fedility_true
            +guid:9578a1f0-9d36-4108-beff-f2c9666447bf
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
    def test_when_using_ipp_pclm_print_job_invalid_print_quality_fedility_true_file_then_succeeds(self):
        job.bookmark_jobs()
        
        print_file = self.print.get_file('b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8')
        test_file_path = "/code/tests/print/pdl/ipp/attributes/print-quality-invalid-values-fidelity-true.test"
        
        returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, test_file_path, print_file)
        assert returncode == 0, f'Unexpected IPP response: {decoded_output[0]}'
        assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
        assert "[FAIL]" not in decoded_output[0], "Ipp print job is Failed with some issue."
        assert decoded_output[1] == '', "There is error output for Ipp Print."
        
        logging.info("The file not printed, Crc is null. No need to check CRC for this case.")
        job.wait_for_no_active_jobs()
        new_job = job.get_newjobs()
        assert len(new_job) == 0, f"there is new job print {new_job}"
