import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using khydotp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:khydotp.obj=6e09368cabbb1945e571fc36477d9d9734a364a04dc795ded02919bc7b9c24a0
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_khydotp
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_khydotp
        +guid:6756817d-81d2-4090-875d-25045145f6f0
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_khydotp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('6e09368cabbb1945e571fc36477d9d9734a364a04dc795ded02919bc7b9c24a0', timeout=600)
    outputsaver.save_output()
