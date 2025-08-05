import pytest

from dunetuf.network.ipp.ipp_utils import execute_ipp_cmd


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52177639 IPP test for printing a pdf file using attribute value sides_two_sided_short_edge
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-47064
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PCLm_letter_600_cjpeg_H64_PgCnt1_RGB__JPG_Source.pdf=b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8
    +test_classification:System
    +name:test_ipp_PCLm_short_edge_duplex_single_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCLm
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_ipp_PCLm_short_edge_duplex_single_page
        +guid:e912853e-4460-4c20-93da-1087e38230cc
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PDF & PrintProtocols=IPP
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ipp_PCLm_short_edge_duplex_single_page(setup_teardown, printjob, outputsaver):
    outputsaver.operation_mode('TIFF')
    # ipp_test_attribs = {'document-format': 'application/PCLm', 'sides': 'two-sided-short-edge'}
    # ipp_test_file = printjob.generate_ipp_test(**ipp_test_attribs)

    # printjob.ipp_print(ipp_test_file, 'b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8')
    # outputsaver.save_output()
    print_file = printjob.get_file('b816ad25f9828ae2c20432e2aac4d5b63991c97b50615a5917452cce74bc21a8')

    printjob.bookmark_jobs()
    returncode, decoded_output = execute_ipp_cmd(printjob.job._cdm.ipaddress, '/code/output/Duplex_Short.test', print_file)
    print(f"decoded_ouput type {type(decoded_output)}")
    outputsaver.operation_mode('NONE')
    print("This ipp cmd never send a print job at all. No need to check CRC for this case.")
