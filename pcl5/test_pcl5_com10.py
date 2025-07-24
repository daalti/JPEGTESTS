import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Adding new system tests for PCL5 missing coverage
    +test_tier:1
    +is_manual:False
    +test_classification:1
    +reqid:DUNE-197464
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:com10.pcl=66ab177d91aa66c5ca406812fe4e8d68ed66a73b2b1fa171b4b1b3fa01d84612
    +name:test_pcl5_com10
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_com10
        +guid:dbe7c413-078a-4bc5-8049-6b91e57fa981
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_com10(setup_teardown, printjob, outputsaver,tray):
    if tray.is_size_supported('na_number-10_4.125x9.5in','tray-1'):
        tray.configure_tray('tray-1', 'na_number-10_4.125x9.5in', 'any')
    printjob.print_verify_multi('66ab177d91aa66c5ca406812fe4e8d68ed66a73b2b1fa171b4b1b3fa01d84612')
    outputsaver.save_output() 