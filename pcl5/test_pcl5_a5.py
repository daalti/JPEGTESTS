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
    +external_files:a5.pcl=831bfada72d92e0f3ab8cb9fac5f090773490f35bbb1045b026811f4b1cc3a96
    +name:test_pcl5_a5
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_a5
        +guid:3f1f63a1-044f-4aad-b52c-7cb68d14152c
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_a5(setup_teardown, printjob, outputsaver,tray):
    if tray.is_size_supported('iso_a5_148x210mm','tray-1'):
        tray.configure_tray('tray-1', 'iso_a5_148x210mm', 'any')
    printjob.print_verify_multi('831bfada72d92e0f3ab8cb9fac5f090773490f35bbb1045b026811f4b1cc3a96')
    outputsaver.save_output()