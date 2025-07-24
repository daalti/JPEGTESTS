import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using disov_nc.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:disov_nc.obj=4d8d59b95bb23ae730b9253e27aa4e237707222de4b410bfaa500df7b42ab7c7
    +test_classification:System
    +name: test_pcl5_pcl_macros_macrosrc_disov_nc
    +test:
        +title: test_pcl5_pcl_macros_macrosrc_disov_nc
        +guid:af0bd381-af8c-4b6c-b9ed-332e88fe0e45
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_macros_macrosrc_disov_nc(setup_teardown, printjob, outputsaver):
    printjob.print_verify('4d8d59b95bb23ae730b9253e27aa4e237707222de4b410bfaa500df7b42ab7c7', timeout=600)
    outputsaver.save_output()
