import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using kngcf.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kngcf.obj=c69e21b19db6a79c393e92aada385ccf12b287a6f597b84c244749d275f887ff
    +test_classification:System
    +name: test_pcl5_hpgl_char_tt_2bytetypeface_kngcf
    +test:
        +title: test_pcl5_hpgl_char_tt_2bytetypeface_kngcf
        +guid:c6f4aa1e-0fc3-4cf3-a363-a88fa3799a8e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_tt_2bytetypeface_kngcf(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c69e21b19db6a79c393e92aada385ccf12b287a6f597b84c244749d275f887ff', timeout=600)
    outputsaver.save_output()
