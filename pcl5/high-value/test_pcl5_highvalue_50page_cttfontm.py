import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 50Page_cttfontm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:50Page-cttfontm.obj=738d0372de177c39b50184f05a8be2c472a2be462b4fdbb56af597a97bd924da
    +test_classification:System
    +name: test_pcl5_highvalue_50page_cttfontm
    +test:
        +title: test_pcl5_highvalue_50page_cttfontm
        +guid:f5cccfed-5c10-4ea5-ad26-2746005cf5c5
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

def test_pcl5_highvalue_50page_cttfontm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('738d0372de177c39b50184f05a8be2c472a2be462b4fdbb56af597a97bd924da', timeout=600)
    outputsaver.save_output()
