import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 22Page_height1.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:22Page-height1.obj=a6794c80d148370221f0dd194783aead2ee2baaffde40e838e96e3276e8b757e
    +test_classification:System
    +name: test_pcl5_basicfunctionality_22page_height1
    +test:
        +title: test_pcl5_basicfunctionality_22page_height1
        +guid:5b5c8c12-28e6-4354-9e6c-b4df3faee967
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

def test_pcl5_basicfunctionality_22page_height1(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a6794c80d148370221f0dd194783aead2ee2baaffde40e838e96e3276e8b757e', timeout=300)
    outputsaver.save_output()
