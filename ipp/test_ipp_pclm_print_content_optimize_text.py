import logging
from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485385 Print_Content_Optimize-optimize-text
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:360
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_GRAY__BlackText.pdf=1756a4162fc3ac39348df16bfc605e21bff65224c5d2d79fae07960715d860dc
    +test_classification:System
    +name:test_ipp_pclm_print_pclm_letter_600_cjpeg_h64_pgcnt1_gray_black_text
    +test:
        +title:test_ipp_pclm_print_pclm_letter_600_cjpeg_h64_pgcnt1_gray_black_text
        +guid:8b31c26a-7e76-48b6-b582-1e24095a17b0
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
def test_ipp_pclm_print_pclm_letter_600_cjpeg_h64_pgcnt1_gray_black_text(setup_teardown, printjob, outputverifier, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)

    print_file = printjob.get_file('1756a4162fc3ac39348df16bfc605e21bff65224c5d2d79fae07960715d860dc')
    ipp_test_file = "/code/tests/print/pdl/ipp/attributes/print-content-optimize-text.test"
    
    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, ipp_test_file , print_file)
    assert returncode == 0, f'Unexpected IPP response: {decoded_output[0]}'
    assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
    assert "[FAIL]" not in decoded_output[0], "Ipp print job is Failed with some issue."
    assert "print-content-optimize (keyword) = text" in decoded_output[0], "Text and Graphics should not be seen for the listed attribute."
    assert decoded_output[1] == '', "There is error output for Ipp Print."

    outputverifier.save_and_parse_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
