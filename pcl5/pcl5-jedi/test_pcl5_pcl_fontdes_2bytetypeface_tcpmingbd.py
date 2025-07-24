import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tcpmingbd.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tcpmingbd.obj=264db56a438f50e44bc234f1b5510359b8993c7f7ec773902e4ea54065090099
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_tcpmingbd
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_tcpmingbd
        +guid:10cccab8-35f1-4c54-8190-152d6ba9c9ae
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_tcpmingbd(setup_teardown, printjob, outputsaver):
    printjob.print_verify('264db56a438f50e44bc234f1b5510359b8993c7f7ec773902e4ea54065090099', timeout=600)
    outputsaver.save_output()
