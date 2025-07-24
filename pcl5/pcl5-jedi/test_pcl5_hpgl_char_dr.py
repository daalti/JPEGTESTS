import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using dr.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:dr.obj=c04b499cf2e91f973908e9f693eca32118ddc7c5b4acb1bb0a2b33a1f83d5b84
    +test_classification:System
    +name: test_pcl5_hpgl_char_dr
    +test:
        +title: test_pcl5_hpgl_char_dr
        +guid:81e12d2c-5a18-42ef-9e1b-94790e2a8889
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_dr(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c04b499cf2e91f973908e9f693eca32118ddc7c5b4acb1bb0a2b33a1f83d5b84', timeout=600)
    outputsaver.save_output()
