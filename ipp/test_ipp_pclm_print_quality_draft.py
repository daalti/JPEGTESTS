import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177626 IPP test for PrintQuality-Draft
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-244314
    +timeout:180
    +asset:PDL_Print
    +delivery_team:Home
    +feature_team:RCB-ProductQA
    +test_framework:TUF
    +external_files:PCLm_letter_300_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=7f4e58829a3c72742f84a0625988860643e5efbc5123b20d0b376d3b00a2c414
    +test_classification:System
    +name:test_ipp_pclm_print_quality_draft
    +test:
        +title:test_ipp_pclm_print_quality_draft
        +guid:c5ee00cc-d31c-45e6-b4ac-a0deec4eefc2
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCLm & PrintProtocols=IPP & Print=Draft
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_pclm_print_quality_draft(setup_teardown, printjob, outputsaver, udw):
    outputsaver.validate_crc_tiff(udw)

    ipp_test_file = '/code/tests/print/pdl/ipp/attributes/Draft.test'
    printjob.ipp_print(ipp_test_file, '7f4e58829a3c72742f84a0625988860643e5efbc5123b20d0b376d3b00a2c414')

    outputsaver.save_output()
    Current_crc_value = outputsaver.get_crc()
    logging.info(f"Validate current crc <{Current_crc_value}> with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
