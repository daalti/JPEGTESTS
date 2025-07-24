import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Japanese New Era Font in PCL5
    +test_tier:3
    +is_manual: False
    +reqid: DUNE-107248
    +timeout: 600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files: JapaneseNewEra_PCL_Test.prn=3739e2db13da0d4d81d504e60001efec297331e8adf8c0d74817477e7b837acf
    +test_classification: System
    +name: test_pcl5_JapaneseNewEraFont
    +test:
        +title:test_pcl5_JapaneseNewEraFont
        +guid:fb51c0ef-4c3e-4f52-bbeb-439c1c67c268
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5 

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_JapaneseNewEraFont(setup_teardown,printjob,outputsaver,udw):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify("3739e2db13da0d4d81d504e60001efec297331e8adf8c0d74817477e7b837acf")
    outputsaver.save_output()
    Current_crc_value = outputsaver.get_crc()
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
   