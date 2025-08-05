import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C30485290 Print_Orientation- unsupported orientation-ipp-fidelity=False
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
    +name:test_ipp_pclm_orientation_unsupport_ipp_fidelity_false
    +test:
        +title:test_ipp_pclm_orientation_unsupport_ipp_fidelity_false
        +guid:d58a3411-f5d0-40ba-96e5-ff721ca7aaa8
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
def test_ipp_pclm_orientation_unsupport_ipp_fidelity_false(setup_teardown, net, printjob, outputsaver, udw):
    if 'landscape' in printjob.capabilities.ipp.get('orientation-requested-supported'):
        logging.warning('Device support landscape as orientation-requested, not suit this case. No need run this case for current device.')
        return

    outputsaver.validate_crc_tiff(udw)

    ipp_test_file = "/code/tests/print/pdl/ipp/attributes/orientation-unsupported-ipp-fidelity-false.test"
    printjob.ipp_print(ipp_test_file, 'b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8')

    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    outputsaver.operation_mode('NONE')
