import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ubuline.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ubuline.obj=3b6566dc1470ee39b5934583c40f4f8b9688417c740c55239477fb8022163a1a
    +test_classification:System
    +name: test_pcl5_pcl_fontr_if_ubuline
    +test:
        +title: test_pcl5_pcl_fontr_if_ubuline
        +guid:9d8cc4ff-1c28-4510-8e5b-64a1b7c73204
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontr_if_ubuline(setup_teardown, printjob, outputsaver):
    printjob.print_verify('3b6566dc1470ee39b5934583c40f4f8b9688417c740c55239477fb8022163a1a', timeout=600)
    outputsaver.save_output()
