import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 15Page_symset.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:200
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:15Page-symset.obj=ea91f3b39fc815e6cffcc4ec77a8cd594f9860aa9d25139efb8cfbe6b0bd108a
    +test_classification:System
    +name: test_pcl5_highvalue_15page_symset
    +test:
        +title: test_pcl5_highvalue_15page_symset
        +guid:c5cf18ae-ae3b-4899-8a34-13af6ac0add1
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

def test_pcl5_highvalue_15page_symset(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ea91f3b39fc815e6cffcc4ec77a8cd594f9860aa9d25139efb8cfbe6b0bd108a', timeout=200)
    outputsaver.save_output()
