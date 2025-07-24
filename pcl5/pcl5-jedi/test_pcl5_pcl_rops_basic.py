import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using basic.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:basic.obj=57b03fa624bb6046524349220c67b15d993bfeae7d18f41b2a0965fb5ffdea81
    +test_classification:System
    +name: test_pcl5_pcl_rops_basic
    +test:
        +title: test_pcl5_pcl_rops_basic
        +guid:fb687024-c7c4-4a8e-a825-5175e64c75ad
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_rops_basic(setup_teardown, printjob, outputsaver):
    printjob.print_verify('57b03fa624bb6046524349220c67b15d993bfeae7d18f41b2a0965fb5ffdea81', timeout=600)
    outputsaver.save_output()
