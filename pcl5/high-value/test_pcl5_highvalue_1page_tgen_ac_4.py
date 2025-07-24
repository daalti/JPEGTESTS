import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 highvalue using 1Page_tgen_ac_4.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:1Page-tgen_ac_4.obj=1e618e4a3939bffd3c5f3b35381f541ff29d831d614976f1ba04e0589cddde39
    +test_classification:System
    +name: test_pcl5_highvalue_1page_tgen_ac_4
    +test:
        +title: test_pcl5_highvalue_1page_tgen_ac_4
        +guid:7c082d1d-859a-4bdf-9c6e-02d4a2513c89
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

def test_pcl5_highvalue_1page_tgen_ac_4(setup_teardown, printjob, outputsaver):
    printjob.print_verify('1e618e4a3939bffd3c5f3b35381f541ff29d831d614976f1ba04e0589cddde39', timeout=600)
    outputsaver.save_output()
