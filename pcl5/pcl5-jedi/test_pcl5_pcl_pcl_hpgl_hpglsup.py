import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using hpglsup.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:hpglsup.obj=365481d13c23b81a6454d26c9dee9d0e5f6556b4b09bfd8eecb56de4967b606e
    +test_classification:System
    +name: test_pcl5_pcl_pcl_hpgl_hpglsup
    +test:
        +title: test_pcl5_pcl_pcl_hpgl_hpglsup
        +guid:3764a077-8205-4e3f-a829-38c389be051b
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pcl_hpgl_hpglsup(setup_teardown, printjob, outputsaver):
    printjob.print_verify('365481d13c23b81a6454d26c9dee9d0e5f6556b4b09bfd8eecb56de4967b606e', timeout=600)
    outputsaver.save_output()
