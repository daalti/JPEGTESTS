import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using khygungp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:khygungp.obj=8af6745dfbf2fcd47f6fcd1b936cb4a561edc0472b1ed41bd6b50f93d89bd2b0
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_khygungp
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_khygungp
        +guid:372a84e6-ed81-4ffd-8877-8ecac6c2798d
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_khygungp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('8af6745dfbf2fcd47f6fcd1b936cb4a561edc0472b1ed41bd6b50f93d89bd2b0', timeout=600)
    outputsaver.save_output()
