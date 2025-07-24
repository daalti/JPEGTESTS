import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 59Page_mpm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:1320
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:59Page-mpm.obj=18ab49384e5d965da25514c39b0fc2e0a78bbf61f2f03c75d20161b83692d86b
    +test_classification:System
    +name: test_pcl5_highvalue_59page_mpm
    +test:
        +title: test_pcl5_highvalue_59page_mpm
        +guid:0aa3808b-402b-4b1e-88fd-8a6a28ca44f0
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_highvalue_59page_mpm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('18ab49384e5d965da25514c39b0fc2e0a78bbf61f2f03c75d20161b83692d86b', timeout=1200)
    outputsaver.save_output()
