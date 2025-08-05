import logging
from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485288 IPP test for printing a PCLm file with Copies supported default
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:120
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB.pdf=b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8
    +test_classification:System
    +name:test_ipp_pclm_copies_supported_and_default
    +test:
        +title:test_ipp_pclm_copies_supported_and_default
        +guid:b29964e9-a15c-416d-81f4-73e57065ead2
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
def test_ipp_pclm_copies_supported_and_default(setup_teardown, printjob):
    logging.info("No print job trigger, CRC is null. No need to check CRC for this case.")
    pirnt_file = printjob.get_file("b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8")
    test_file_path = "/code/tests/print/pdl/ipp/attributes/copies_supported_default.test"
    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, test_file_path, pirnt_file)
    logging.info(f"Ipp print output content is: <{decoded_output}>")
    assert returncode == 0, f'Unexpected IPP response: {returncode}'
    assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
    assert decoded_output[1] == '', "There is error output for Ipp Print."
