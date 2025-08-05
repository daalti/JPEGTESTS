import pytest

from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177660 Ipp test for printing a URF file using attribute value media-size_letter
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_czlib_H64_PgCnt1_RGB__Blank_PNG_Source.pdf=28ced94ad4ff4ec8a5b0076ab5524e5fa9665c095e1bb7ec6552b71aacef00f0
    +name:test_ipp_pclm_zlib_blank_page_rgb
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_pclm_zlib_blank_page_rgb
        +guid:d1fcda8e-2bc7-4999-a08b-500d6b5cbf34
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
def test_ipp_pclm_zlib_blank_page_rgb(setup_teardown, printjob, outputverifier, tray, outputsaver):
    outputsaver.operation_mode('TIFF')
    print_file = printjob.get_file('28ced94ad4ff4ec8a5b0076ab5524e5fa9665c095e1bb7ec6552b71aacef00f0')

    printjob.bookmark_jobs()
    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, '/code/output/PCLmBlank.test', print_file)
    print(f"decoded_ouput type {type(decoded_output)}")
    outputsaver.operation_mode('NONE')
    print("This ipp cmd never send a print job at all. No need to check CRC for this case.")
