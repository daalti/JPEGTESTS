import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using cp.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:cp.obj=a60e4a31e61e250a059b382ded3fdfe7c332061ae240faf562fa80c9131efed5
    +test_classification:System
    +name: test_pcl5_hpgl_char_cp
    +test:
        +title: test_pcl5_hpgl_char_cp
        +guid:13706de8-4247-44b8-bac1-a74ca1e78677
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_cp(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a60e4a31e61e250a059b382ded3fdfe7c332061ae240faf562fa80c9131efed5', timeout=600)
    outputsaver.save_output()
