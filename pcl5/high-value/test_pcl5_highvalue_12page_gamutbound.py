import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 12Page_gamutbound.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:300
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:12Page-gamutbound.obj=70fdae69d570e79e353dfe5ef80e815734c7a3b7f25e91d962305a4370669b1a
    +test_classification:System
    +name: test_pcl5_highvalue_12page_gamutbound
    +test:
        +title: test_pcl5_highvalue_12page_gamutbound
        +guid:e075e053-88aa-4d97-9614-cd0eec57c990
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

def test_pcl5_highvalue_12page_gamutbound(setup_teardown, printjob, outputsaver):
    printjob.print_verify('70fdae69d570e79e353dfe5ef80e815734c7a3b7f25e91d962305a4370669b1a', timeout=300)
    outputsaver.save_output()
