import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using pp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pp.obj=0d6de21ee72150f340e3584057f9c4a969b4e0988f597c53580cbebfa93160b9
    +test_classification:System
    +name: test_pcl5_pcl_rops_pp
    +test:
        +title: test_pcl5_pcl_rops_pp
        +guid:240b2b32-1dff-49a1-8ae8-b8151242f040
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_rops_pp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0d6de21ee72150f340e3584057f9c4a969b4e0988f597c53580cbebfa93160b9', timeout=600)
    outputsaver.save_output()
