import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ea_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ea_igm.obj=aefd4f04d7e36dc00164dbe7b49ffdeb55f6805ef59f52bfa8ce33b5d3793e43
    +test_classification:System
    +name: test_pcl5_hpgl_polygon_ea_igm
    +test:
        +title: test_pcl5_hpgl_polygon_ea_igm
        +guid:99ce003a-f953-45d7-ac92-d5ec6722e6d8
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_polygon_ea_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('aefd4f04d7e36dc00164dbe7b49ffdeb55f6805ef59f52bfa8ce33b5d3793e43', timeout=600)
    outputsaver.save_output()
