import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using fi.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:fi.obj=39de0ab3106ac7c523c0a0f38ba697a8721dd44931cae81471830638d0f8e616
    +test_classification:System
    +name: test_pcl5_hpgl_char_fi
    +test:
        +title: test_pcl5_hpgl_char_fi
        +guid:158fe49d-7a68-4f99-8e9c-90cbdbbd4de7
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_fi(setup_teardown, printjob, outputsaver):
    printjob.print_verify('39de0ab3106ac7c523c0a0f38ba697a8721dd44931cae81471830638d0f8e616', timeout=600)
    outputsaver.save_output()
