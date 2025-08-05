import pytest

from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177666 Ipp test for printing a URF file using attribute value media-size_letter
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_czlib_H64_PgCnt1_GRAY__Blank_PNG_Source.pdf=f7dc441c5270051aab55006375ffec95a29896cd06e59b2a74511b510000f4c4
    +name:test_ipp_pclm_zlib_blank_page_gray
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_zlib_blank_page_gray
        +guid:b0bb5cef-7350-4264-a5d5-fa8a702a6e52
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
def test_ipp_pclm_zlib_blank_page_gray(setup_teardown, printjob, outputverifier, tray, outputsaver):
    outputsaver.operation_mode('TIFF')
    print_file = printjob.get_file('f7dc441c5270051aab55006375ffec95a29896cd06e59b2a74511b510000f4c4')

    printjob.bookmark_jobs()
    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, '/code/output/PCLmBlank.test', print_file)
    print(f"decoded_ouput type {type(decoded_output)}")
    outputsaver.operation_mode('NONE')
    print("This ipp cmd never send a print job at all. No need to check CRC for this case.")
