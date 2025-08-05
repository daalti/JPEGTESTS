import logging
from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485291 Print_Orientation- unsupported orientation-ipp-fidelity=true
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:360
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB.pdf=b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8
    +test_classification:System
    +name:test_ipp_pclm_orientation_unsupport_ipp_fidelity_true
    +test:
        +title:test_ipp_pclm_orientation_unsupport_ipp_fidelity_true
        +guid:13fa69d4-2c34-462a-bc51-d25924247540
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
def test_ipp_pclm_orientation_unsupport_ipp_fidelity_true(setup_teardown, net, printjob, outputsaver):
    if 'landscape' in printjob.capabilities.ipp.get('orientation-requested-supported'):
        logging.warning('Device support landscape as orientation-requested, not suit this case. No need run this case for current device.')
        return

    print_file = printjob.get_file('b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8')
    ipp_test_file = "/code/tests/print/pdl/ipp/attributes/orientation-unsupported-ipp-fidelity-true.test"

    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, ipp_test_file, print_file)
    assert returncode == 0, f'Unexpected IPP response: {decoded_output[0]}'
    assert "[PASS]" in decoded_output[0], "Ipp print job is not complete with no issues."
    assert "[FAIL]" not in decoded_output[0], "Ipp print job is Failed with some issue."
    assert decoded_output[1] == '', "There is error output for Ipp Print."
    logging.info("The file not printed, Crc is null. No need to check CRC for this case.")
    outputsaver.operation_mode('NONE')
