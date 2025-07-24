import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 42Page_pal_con.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:42Page-pal_con.obj=b82e696348a4c25fd6ecea14a7a01acaccfafdea2a9f2fca0cb146f8394e03d4
    +test_classification:System
    +name: test_pcl5_highvalue_42page_pal_con
    +test:
        +title: test_pcl5_highvalue_42page_pal_con
        +guid:03091508-9e6a-4549-a16f-4a5cb1f6d3d9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_42page_pal_con(setup_teardown, printjob, outputsaver):
    printjob.print_verify_multi('b82e696348a4c25fd6ecea14a7a01acaccfafdea2a9f2fca0cb146f8394e03d4', timeout=720,expected_jobs=2)
    outputsaver.save_output()
