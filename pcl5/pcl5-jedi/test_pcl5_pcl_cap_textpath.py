import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using textpath.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:textpath.obj=7df7b2357d909d0f0cae772f1f0ee2208ee23b599478746115386fc751b8c35f
    +test_classification:System
    +name: test_pcl5_pcl_cap_textpath
    +test:
        +title: test_pcl5_pcl_cap_textpath
        +guid:5b148805-3484-4593-896f-4c4ebeaed61a
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_cap_textpath(setup_teardown, printjob, outputsaver):
    printjob.print_verify('7df7b2357d909d0f0cae772f1f0ee2208ee23b599478746115386fc751b8c35f', timeout=600)
    outputsaver.save_output()
