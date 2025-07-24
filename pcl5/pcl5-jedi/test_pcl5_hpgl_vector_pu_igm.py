import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using pu_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pu_igm.obj=110aec0b3fd99a735f9f478fdb971e48d6791a9e691860f8db715674837a6a68
    +test_classification:System
    +name: test_pcl5_hpgl_vector_pu_igm
    +test:
        +title: test_pcl5_hpgl_vector_pu_igm
        +guid:802e419f-c89c-40a3-87d7-16782759a9d6
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_pu_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('110aec0b3fd99a735f9f478fdb971e48d6791a9e691860f8db715674837a6a68', timeout=600)
    outputsaver.save_output()
