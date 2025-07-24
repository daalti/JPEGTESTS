import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tranmode.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tranmode.obj=26bf0041173584021d5d455c03fe9afce8a66ee308f7a026092b55906232be81
    +test_classification:System
    +name: test_pcl5_pcl_printmod_tranmode
    +test:
        +title: test_pcl5_pcl_printmod_tranmode
        +guid:f86bdff5-6941-45d5-a972-59a77d23ba55
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_printmod_tranmode(setup_teardown, printjob, outputsaver):
    printjob.print_verify('26bf0041173584021d5d455c03fe9afce8a66ee308f7a026092b55906232be81', timeout=600)
    outputsaver.save_output()
